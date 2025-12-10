---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-knn-search.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# kNN search in {{es}} [knn-search]

A *k-nearest neighbor* (kNN) search finds the *k* nearest vectors to a query vector using a similarity metric such as cosine or L2 norm.  
With {{es}} kNN search, you can retrieve results based on semantic meaning rather than exact keyword matches.

Common use cases for kNN vector similarity search include:

* **Search**
  * Semantic text search
  * Image and video similarity

* **Recommendations**
  * Product recommendations
  * Collaborative filtering
  * Personalized content discovery

* **Analysis**
  * Anomaly detection
  * Pattern matching

## Prerequisites for kNN search [knn-prereqs]

To run a kNN search in {{es}}:

* Your data must be vectorized. You can [use an NLP model in {{es}}](../../../explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md) or generate vectors outside {{es}}.
  * Use the [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) field type for dense vectors.
  * Query vectors must have the same dimension and be created with the same model as the document vectors.
  * Already have vectors? Refer to [Bring your own dense vectors](bring-own-vectors.md).

* Required [index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices):
  * `create_index` or `manage` to create an index with a `dense_vector` field
  * `create`, `index`, or `write` to add data
  * `read` to search the index

:::{tip}
The default type of {{es-serverless}} project is suitable for this use case unless you plan to use uncompressed dense vectors (`int4` or `int8` quantization strategies) with high dimensionality.
Refer to [](dense-vector.md#vector-profiles).
:::

## kNN search methods: approximate and exact kNN [knn-methods]

{{es}} supports two methods for kNN search:

* [**Approximate kNN**](#approximate-knn): Fast, scalable similarity search using the `knn` option, `knn` query, or a `knn` retriever. Ideal for most production workloads.  
* [**Exact, brute-force kNN**](#exact-knn): Uses a `script_score` query with a vector function. Best for small datasets or precise scoring.

Approximate kNN offers low latency and good accuracy, while exact kNN guarantees accurate results but does not scale well for large datasets. With this approach, a `script_score` query must scan each matching document to compute the vector function, which can result in slow search speeds. However, you can improve latency by using a [query](../../../explore-analyze/query-filter/languages/querydsl.md) to limit the number of matching documents passed to the function. If you filter your data to a small subset of documents, you can get good search performance using this approach.

## Approximate kNN search [approximate-knn]

::::{warning}
Approximate kNN search has specific resource requirements. For instance, for HNSW, all vector data must fit in the node’s page cache for efficient performance. Refer to the [approximate kNN tuning guide](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md) for configuration tips.
::::

To run an approximate kNN search:

1. Map one or more `dense_vector` fields. Approximate kNN search requires the following mapping options:  

    * A `similarity` value. This value determines the similarity metric used to score documents based on similarity between the query and document vector. For a list of available metrics, see the [`similarity`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-similarity) parameter documentation. The `similarity` setting defaults to `cosine`.

    ```console
    PUT image-index
    {
      "mappings": {
        "properties": {
          "image-vector": {
            "type": "dense_vector",
            "dims": 3,
            "similarity": "l2_norm"
          },
          "title-vector": {
            "type": "dense_vector",
            "dims": 5,
            "similarity": "l2_norm"
          },
          "title": {
            "type": "text"
          },
          "file-type": {
            "type": "keyword"
          }
        }
      }
    }
    ```

2. Index your data with embeddings.  

    ```console
    POST image-index/_bulk?refresh=true
    { "index": { "_id": "1" } }
    { "image-vector": [1, 5, -20], "title-vector": [12, 50, -10, 0, 1], "title": "moose family", "file-type": "jpg" }
    { "index": { "_id": "2" } }
    { "image-vector": [42, 8, -15], "title-vector": [25, 1, 4, -12, 2], "title": "alpine lake", "file-type": "png" }
    { "index": { "_id": "3" } }
    { "image-vector": [15, 11, 23], "title-vector": [1, 5, 25, 50, 20], "title": "full moon", "file-type": "jpg" }
    ...
    ```

3. Query using the [`knn` option](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-knn) or a [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md).

    ```console
    POST image-index/_search
    {
      "knn": {
        "field": "image-vector",
        "query_vector": [-5, 9, -12],
        "k": 10,
        "num_candidates": 100
      },
      "fields": [ "title", "file-type" ]
    }
    ```

The document `_score` is a positive 32-bit floating-point number that ranks result relevance. In {{es}} kNN search, `_score` is derived from the chosen vector similarity metric between the query and document vectors. Refer to [`similarity`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-similarity) for details on how kNN scores are computed.

::::{note}
Support for approximate kNN search was added in version 8.0. Before 8.0, `dense_vector` fields did not support enabling `index` in the mapping. If you created an index prior to 8.0 with `dense_vector` fields, reindex using a new mapping with `index: true` (which is the default value) to use approximate kNN.
::::

### Indexing considerations for approximate kNN search [knn-indexing-considerations]


For approximate kNN, {{es}} stores dense vector values per segment as an [HNSW graph](https://arxiv.org/abs/1603.09320) or per segment as clusters using [DiskBBQ](https://www.elastic.co/search-labs/blog/diskbbq-elasticsearch-introduction). Building these approximate kNN structures is compute-intensive, which means indexing vectors can be time-consuming. As a result, you might need to increase client request timeouts for index and bulk operations. The [approximate kNN tuning guide](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md) covers indexing performance, sizing, and configuration trade-offs that affect search performance.

{applies_to}`stack: ga 9.2` In addition to search-time parameters, HNSW and DiskBBQ expose index-time settings that balance graph build cost, search speed, and accuracy. When defining your `dense_vector` mapping, use [`index_options`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-index-options) to set these parameters:

```console
PUT image-index
{
  "mappings": {
    "properties": {
      "image-vector": {
        "type": "dense_vector",
        "dims": 3,
        "similarity": "l2_norm",
        "index_options": {
          "type": "hnsw",
          "m": 32,
          "ef_construction": 100
        }
      }
    }
  }
}
```

### Tune approximate kNN for speed or accuracy [tune-approximate-knn-for-speed-accuracy]

To gather results, the kNN API first finds a `num_candidates` number of approximate neighbors per shard, computes similarity to the query vector, selects the top `k` per shard, and merges them into the global top `k` nearest neighbors.

* Increase `num_candidates` to improve recall and accuracy (at the cost of higher latency).
* Decrease `num_candidates` for faster queries (with a potential accuracy trade-off).

Choosing `num_candidates` is the primary knob for optimizing the latency/recall trade-off in {{es}} vector similarity search.

### Approximate kNN using byte vectors [approximate-knn-using-byte-vectors]

The approximate kNN search API also supports `byte` (int8) value vectors alongside `float` vectors. Use the [`knn` option](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-knn) to search a `dense_vector` field with [`element_type`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-params) set to `byte` and indexing enabled. Byte vectors reduce memory footprint and can improve cache efficiency for large-scale vector similarity search.

1. Explicitly map one or more `dense_vector` fields with [`element_type`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-params) set to `byte` and indexing enabled.

    ```console
    PUT byte-image-index
    {
      "mappings": {
        "properties": {
          "byte-image-vector": {
            "type": "dense_vector",
            "element_type": "byte",
            "dims": 2
          },
          "title": {
            "type": "text"
          }
        }
      }
    }
    ```

2. Index your data ensuring all vector values are integers within the range [-128, 127].

    ```console
    POST byte-image-index/_bulk?refresh=true
    { "index": { "_id": "1" } }
    { "byte-image-vector": [5, -20], "title": "moose family" }
    { "index": { "_id": "2" } }
    { "byte-image-vector": [8, -15], "title": "alpine lake" }
    { "index": { "_id": "3" } }
    { "byte-image-vector": [11, 23], "title": "full moon" }
    ```

3. Run the search using the [`knn` option](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-knn) ensuring the `query_vector` values are integers within the range [-128, 127].

    ```console
    POST byte-image-index/_search
    {
      "knn": {
        "field": "byte-image-vector",
        "query_vector": [-5, 9],
        "k": 10,
        "num_candidates": 100
      },
      "fields": [ "title" ]
    }
    ```


*Note*: In addition to the standard byte array, one can also provide a hex-encoded string value for the `query_vector` param. As an example, the search request above can also be expressed as follows, which would yield the same results

```console
POST byte-image-index/_search
{
  "knn": {
    "field": "byte-image-vector",
    "query_vector": "fb09",
    "k": 10,
    "num_candidates": 100
  },
  "fields": [ "title" ]
}
```

### Byte quantized kNN search [knn-search-quantized-example]

If you want to provide `float` vectors but still get the memory savings of `byte` vectors, use the [quantization](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization) feature. Quantization allows you to provide `float` vectors, but internally they are indexed as `byte` vectors. Additionally, the original `float` vectors are still retained in the index.

::::{note}
The default index type for `dense_vector` is either `bbq_hnsw` or `int8_hnsw`, depending on your product version. Refer to [Dense vector field type](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md).
::::

You can use the default quantization strategy or specify an index option.
For example, use `int8_hnsw`:

```console
PUT quantized-image-index
{
  "mappings": {
    "properties": {
      "image-vector": {
        "type": "dense_vector",
        "element_type": "float",
        "dims": 2,
        "index": true,
        "index_options": {
          "type": "int8_hnsw"
        }
      },
      "title": {
        "type": "text"
      }
    }
  }
}
```

1. Index your `float` vectors.

    ```console
    POST quantized-image-index/_bulk?refresh=true
    { "index": { "_id": "1" } }
    { "image-vector": [0.1, -2], "title": "moose family" }
    { "index": { "_id": "2" } }
    { "image-vector": [0.75, -1], "title": "alpine lake" }
    { "index": { "_id": "3" } }
    { "image-vector": [1.2, 0.1], "title": "full moon" }
    ```

2. Run the search using the [`knn` option](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-knn). When searching, the `float` vector is automatically quantized to a `byte` vector.

    ```console
    POST quantized-image-index/_search
    {
      "knn": {
        "field": "image-vector",
        "query_vector": [0.1, -2],
        "k": 10,
        "num_candidates": 100
      },
      "fields": [ "title" ]
    }
    ```

Because the original `float` vectors are retained alongside the quantized index, you can use them for re-scoring: retrieve candidates quickly via the `int8_hnsw` index, then rescore the top `k` hits using the original `float` vectors. This provides the best of both worlds, fast search and accurate scoring.

```console
POST quantized-image-index/_search
{
  "knn": {
    "field": "image-vector",
    "query_vector": [0.1, -2],
    "k": 15,
    "num_candidates": 100
  },
  "fields": [ "title" ],
  "rescore": {
    "window_size": 10,
    "query": {
      "rescore_query": {
        "script_score": {
          "query": {
            "match_all": {}
          },
          "script": {
            "source": "cosineSimilarity(params.query_vector, 'image-vector') + 1.0",
            "params": {
              "query_vector": [0.1, -2]
            }
          }
        }
      }
    }
  }
}
```

### BFloat16 vector encoding [knn-search-bfloat16]
```{applies_to}
stack: ga 9.3
```
Instead of storing raw vectors as 4-byte values, you can use `element_type: bfloat16` to store each dimension as a 2-byte value. This can be useful if your indexed vectors are at bfloat16 precision already, or if you want to reduce the disk space required to store vector data. When this element type is used, {{es}} automatically rounds 4-byte float values to 2-byte bfloat16 values when indexing vectors.

Due to the reduced precision of bfloat16, any vectors retrieved from the index might have slightly different values to those originally indexed.

### Filtered kNN search [knn-search-filter-example]

The kNN search API supports restricting vector similarity search with a filter. The request returns the top `k` nearest neighbors that also satisfy the filter query, enabling targeted, pre-filtered approximate kNN in {{es}}.

The following request performs an approximate kNN search filtered by the `file-type` field:

```console
POST image-index/_search
{
  "knn": {
    "field": "image-vector",
    "query_vector": [54, 10, -2],
    "k": 5,
    "num_candidates": 50,
    "filter": {
      "term": {
        "file-type": "png"
      }
    }
  },
  "fields": ["title"],
  "_source": false
}
```

::::{note}
The filter is applied **during** approximate kNN search to ensure that `k` matching documents are returned. In contrast, post-filtering applies the filter **after** the approximate kNN step and can return fewer than `k` results; even when enough relevant documents exist.
::::

### Approximate kNN search and filtering [approximate-knn-search-and-filtering]

In approximate kNN search with an HNSW index, applying filters can decrease performance as the engine must explore more of the graph to gather enough candidates that satisfy the filter and reach `num_candidates`. This contrasts with conventional query filtering, where stricter filters often speed up queries.

To avoid significant performance drawbacks, Lucene implements the following strategies per segment:

* If the filtered document count is less than or equal to num_candidates, the search bypasses the HNSW graph and uses a brute force search on the filtered documents.
* While exploring the HNSW graph, if the number of nodes explored exceeds the number of documents that satisfy the filter, the search will stop exploring the graph and switch to a brute force search over the filtered documents.

### Combine approximate kNN with other features [_combine_approximate_knn_with_other_features]

You can perform **hybrid retrieval** by combining the [`knn` option](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-knn) with a standard [`query`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-query). This blends vector similarity with lexical relevance, filters, and aggregations.

```console
POST image-index/_search
{
  "query": {
    "match": {
      "title": {
        "query": "mountain lake",
        "boost": 0.9
      }
    }
  },
  "knn": {
    "field": "image-vector",
    "query_vector": [54, 10, -2],
    "k": 5,
    "num_candidates": 50,
    "boost": 0.1
  },
  "size": 10
}
```

This search finds the global top `k = 5` vector matches, combines them with the matches from the `match` query, and finally returns the 10 top-scoring results. The `knn` and `query` matches are combined through a disjunction, as if you took a boolean *or* between them. The top `k` vector results represent the global nearest neighbors across all index shards.

The score of each hit is the sum of the `knn` and `query` scores. You can specify a `boost` value to give a weight to each score in the sum. In the example above, the scores will be calculated as

```
score = 0.9 * match_score + 0.1 * knn_score
```

The `knn` option can also be used with [`aggregations`](../../../explore-analyze/query-filter/aggregations.md). In general, {{es}} computes aggregations over all documents that match the search. So for approximate kNN search, aggregations are calculated on the top `k` nearest documents. If the search also includes a `query`, then aggregations are calculated on the combined set of `knn` and `query` matches.

### Perform semantic search [knn-semantic-search]

:::{tip}
Looking for a minimal configuration approach? The `semantic_text` field type abstracts these vector search implementations with sensible defaults and automatic model management. It's the recommended approach for most users. [Learn more about semantic_text](../semantic-search/semantic-search-semantic-text.md).
:::

kNN search enables you to perform semantic search by using a previously deployed [text embedding model](../../../explore-analyze/machine-learning/nlp/ml-nlp-search-compare.md#ml-nlp-text-embedding). Instead of literal matching on search terms, semantic search retrieves results based on the intent and the contextual meaning of a search query.

Under the hood, the text embedding NLP model converts your input query string (provided as `model_text`) into a dense vector. The query vector is compared against an index containing dense vectors created with the same text embedding {{ml}} model. The search results are semantically similar as learned by the model.

::::{important}
To perform semantic search:

* You need an index that contains dense vector representations of the input data to search against.
* You must use the same text embedding model for search that you used to create the document vectors.
* The text embedding NLP model deployment must be started.
::::

Reference the deployed text embedding model or the model deployment in the `query_vector_builder` object, and provide the search string as `model_text`:

```js
(...)
{
  "knn": {
    "field": "dense-vector-field",
    "k": 10,
    "num_candidates": 100,
    "query_vector_builder": {
      "text_embedding": { <1>
        "model_id": "my-text-embedding-model", <2>
        "model_text": "The opposite of blue" <3>
      }
    }
  }
}
(...)
```

1. The {{nlp}} task to perform. It must be `text_embedding`.
2. The ID of the text embedding model used to generate the query’s dense vector. Use the same model that produced the document embeddings in the target index. You can also provide the `deployment_id` as the `model_id` value.
3. The query string from which the model generates the dense vector representation.

For more information on how to deploy a trained model and use it to create text embeddings, refer to this [end-to-end example](../../../explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md).

### Search multiple kNN fields [_search_multiple_knn_fields]

In addition to *hybrid retrieval*, you can search more than one kNN vector field in a single request:

```console
POST image-index/_search
{
  "query": {
    "match": {
      "title": {
        "query": "mountain lake",
        "boost": 0.9
      }
    }
  },
  "knn": [ {
    "field": "image-vector",
    "query_vector": [54, 10, -2],
    "k": 5,
    "num_candidates": 50,
    "boost": 0.1
  },
  {
    "field": "title-vector",
    "query_vector": [1, 20, -52, 23, 10],
    "k": 10,
    "num_candidates": 10,
    "boost": 0.5
  }],
  "size": 10
}
```

This search retrieves the global top `k = 5` neighbors for `image-vector` and the global top `k = 10` for `title-vector`. These vector result sets are combined with the matches from the `match` query, and the top 10 overall documents are returned. Multiple `knn` clauses and the `query` clause are combined via a disjunction (boolean *OR*). The top `k` vector results represent the global nearest neighbors across all index shards.

The scoring for a document with the above configured boosts would be:

```
score = 0.9 * match_score + 0.1 * knn_score_image-vector + 0.5 * knn_score_title-vector
```

### Search kNN with expected similarity [knn-similarity-search]

While kNN is a powerful tool, it always tries to return `k` nearest neighbors. Consequently, when using `knn` with a `filter`, you could filter out all relevant documents and only have irrelevant ones left to search. In that situation, `knn` will still do its best to return `k` nearest neighbors, even though those neighbors could be far away in the vector space.

To control this, use the `similarity` parameter in the `knn` clause. This sets a minimum similarity threshold a vector must meet to be considered a match. The `knn` search flow with this parameter is:

* Apply any user-provided `filter` queries.
* Explore the vector space to gather `k` candidates.
* Exclude any vectors with similarity below the configured `similarity` threshold.

::::{note}
`similarity` is the true [similarity](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-similarity) value **before** it is transformed into `_score` and before any boosts are applied.
::::

For each configured [similarity](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-similarity), the following shows how to invert `_score` back to the underlying similarity. Use these when you want to filter based on `_score`:

* `l2_norm`: `sqrt((1 / _score) - 1)`
* `cosine`: `(2 * _score) - 1`
* `dot_product`: `(2 * _score) - 1`
* `max_inner_product`:
  * `_score < 1`: `1 - (1 / _score)`
  * `_score >= 1`: `_score - 1`

Example: the query searches for the given `query_vector`, with a `filter` applied, and requires that matches meet or exceed the specified `similarity` threshold. Results below the threshold are not returned, even if fewer than `k` neighbors remain.

```console
POST image-index/_search
{
  "knn": {
    "field": "image-vector",
    "query_vector": [1, 5, -20],
    "k": 5,
    "num_candidates": 50,
    "similarity": 36,
    "filter": {
      "term": {
        "file-type": "png"
      }
    }
  },
  "fields": ["title"],
  "_source": false
}
```

In this data set, the only document with `file-type = png` has the vector `[42, 8, -15]`. The `l2_norm` distance between `[42, 8, -15]` and `[1, 5, -20]` is `41.412`, which exceeds the configured `similarity` threshold of `36`. As a result, this search returns no hits.

### Nested kNN search [nested-knn-search]

When text exceeds a model’s token limit, chunking must be performed before generating embeddings for each chunk. By combining [`nested`](elasticsearch://reference/elasticsearch/mapping-reference/nested.md) fields with [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md), you can perform nearest passage retrieval without copying top-level document metadata.  
Note that nested kNN queries only support [score_mode](elasticsearch://reference/query-languages/query-dsl/query-dsl-nested-query.md#nested-top-level-params)=`max`.

Here is a simple passage vectors index that stores vectors and some top-level metadata for filtering.

```console
PUT passage_vectors
{
    "mappings": {
        "properties": {
            "full_text": {
                "type": "text"
            },
            "creation_time": {
                "type": "date"
            },
            "paragraph": {
                "type": "nested",
                "properties": {
                    "vector": {
                        "type": "dense_vector",
                        "dims": 2,
                        "index_options": {
                            "type": "hnsw"
                        }
                    },
                    "text": {
                        "type": "text",
                        "index": false
                    },
                    "language": {
                        "type": "keyword"
                    }
                }
            },
            "metadata": {
                "type": "nested",
                "properties": {
                    "key": {
                        "type": "keyword"
                    },
                    "value": {
                        "type": "text"
                    }
                }
            }
        }
    }
}
```

With the above mapping, we can index multiple passage vectors along with storing the individual passage text.

```console
POST passage_vectors/_bulk?refresh=true
{ "index": { "_id": "1" } }
{ "full_text": "first paragraph another paragraph", "creation_time": "2019-05-04", "paragraph": [ { "vector": [ 0.45, 45 ], "text": "first paragraph", "paragraph_id": "1", "language": "EN" }, { "vector": [ 0.8, 0.6 ], "text": "another paragraph", "paragraph_id": "2", "language": "FR" } ], "metadata": [ { "key": "author", "value": "Jane Doe" }, { "key": "source", "value": "Internal Memo" } ] }
{ "index": { "_id": "2" } }
{ "full_text": "number one paragraph number two paragraph", "creation_time": "2020-05-04", "paragraph": [ { "vector": [ 1.2, 4.5 ], "text": "number one paragraph", "paragraph_id": "1", "language": "EN" }, { "vector": [ -1, 42 ], "text": "number two paragraph", "paragraph_id": "2", "language": "EN" }] , "metadata": [ { "key": "author", "value": "Jane Austen" }, { "key": "source", "value": "Financial" } ] }
```

The query will seem very similar to a typical kNN search:

```console
POST passage_vectors/_search
{
    "fields": ["full_text", "creation_time"],
    "_source": false,
    "knn": {
        "query_vector": [
            0.45,
            45
        ],
        "field": "paragraph.vector",
        "k": 2
    }
}
```

Note that even with 4 total nested vectors, the response still returns two documents. kNN search over nested dense vectors will always diversify the top results over the top-level document; `"k"` top-level documents will be returned, scored by their nearest passage vector (for example, `"paragraph.vector"`).

```console-result
{
    "took": 4,
    "timed_out": false,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 2,
            "relation": "eq"
        },
        "max_score": 1.0,
        "hits": [
            {
                "_index": "passage_vectors",
                "_id": "1",
                "_score": 1.0,
                "fields": {
                    "creation_time": [
                        "2019-05-04T00:00:00.000Z"
                    ],
                    "full_text": [
                        "first paragraph another paragraph"
                    ]
                }
            },
            {
                "_index": "passage_vectors",
                "_id": "2",
                "_score": 0.9997144,
                "fields": {
                    "creation_time": [
                        "2020-05-04T00:00:00.000Z"
                    ],
                    "full_text": [
                        "number one paragraph number two paragraph"
                    ]
                }
            }
        ]
    }
}
```

#### Filtering in nested KNN search [nested-knn-search-filtering]

Want to filter by metadata in a nested kNN search? Add a `filter` to your `knn` clause.

To ensure correct results, each individual filter must target either:

* Top-level metadata 
* `nested` metadata {applies_to}`stack: ga 9.2`
  :::{note}
  A single `knn` search can include multiple filters: some over top-level metadata and others over nested metadata.
  :::

```console
POST passage_vectors/_search
{
    "fields": [
        "creation_time",
        "full_text"
    ],
    "_source": false,
    "knn": {
        "query_vector": [0.45, 45],
        "field": "paragraph.vector",
        "k": 2,
        "filter": {
            "range": {
                "creation_time": {
                    "gte": "2019-05-01",
                    "lte": "2019-05-05"
                }
            }
        }
    }
}
```

With the top-level `creation_time` filter applied, only one document falls within the specified range.

```console-result
{
    "took": 4,
    "timed_out": false,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 1,
            "relation": "eq"
        },
        "max_score": 1.0,
        "hits": [
            {
                "_index": "passage_vectors",
                "_id": "1",
                "_score": 1.0,
                "fields": {
                    "creation_time": [
                        "2019-05-04T00:00:00.000Z"
                    ],
                    "full_text": [
                        "first paragraph another paragraph"
                    ]
                }
            }
        ]
    }
}
```

##### Filtering on nested metadata [nested-knn-search-filtering-nested-metatadata]
```{applies_to}
stack: ga 9.2
```

The following query applies a nested metadata filter. When scoring parent documents, it only considers nested vectors whose "paragraph.language" is "EN".

```console
POST passage_vectors/_search
{
    "fields": [
        "full_text"
    ],
    "_source": false,
    "knn": {
        "query_vector": [0.45, 45],
        "field": "paragraph.vector",
        "k": 2,
        "filter": {
            "match": {
                "paragraph.language": "EN"
            }
        }
    }
}
```

The next example combines two filters: one on nested metadata and one on top-level metadata. Parent documents are scored only by vectors with "paragraph.language": "EN" and whose parent documents fall within the specified time range.

```console
POST passage_vectors/_search
{
    "fields": [
        "full_text"
    ],
    "_source": false,
    "knn": {
        "query_vector": [0.45,45],
        "field": "paragraph.vector",
        "k": 2,
        "filter": [
            {"match": {"paragraph.language": "EN"}},
            {"range": { "creation_time": { "gte": "2019-05-01", "lte": "2019-05-05"}}}
        ]
    }
}
```

#### Filtering by sibling nested fields in nested KNN search [nested-knn-search-filtering-sibling]
```{applies_to}
stack: ga 9.2
```

Nested knn search also allows pre-filtering on sibling nested fields.
For example, given "paragraphs" and "metadata" as nested fields, we can search "paragraphs.vector" and filter by "metadata.key" and "metadata.value".

```console
POST passage_vectors/_search
{
    "fields": [
        "full_text"
    ],
    "_source": false,
    "knn": {
        "query_vector": [0.45, 45],
        "field": "paragraph.vector",
        "k": 2,
        "filter": {
            "nested": {
                "path": "metadata",
                "query": {
                    "bool": {
                        "must": [
                            { "match": { "metadata.key": "author" } },
                            { "match": { "metadata.value": "Doe" } }
                        ]
                    }
                }
            }
        }
    }
}
```

:::{note}
Retrieving "inner_hits" when filtering on sibling nested fields is not supported.
:::

### Nested kNN Search with Inner hits [nested-knn-search-inner-hits]

To extract the nearest passage for each matched parent document, add [inner_hits](elasticsearch://reference/elasticsearch/rest-apis/retrieve-inner-hits.md) to the `knn` clause.

::::{note}
When using `inner_hits` with multiple `knn` clauses, set a unique [`inner_hits.name`](elasticsearch://reference/elasticsearch/rest-apis/retrieve-inner-hits.md#inner-hits-options) for each clause to avoid naming collisions that would fail the search request.
::::

```console
POST passage_vectors/_search
{
    "fields": [
        "creation_time",
        "full_text"
    ],
    "_source": false,
    "knn": {
        "query_vector": [
            0.45,
            45
        ],
        "field": "paragraph.vector",
        "k": 2,
        "num_candidates": 2,
        "inner_hits": {
            "_source": false,
            "fields": [
                "paragraph.text"
            ],
            "size": 1
        }
    }
}
```

Now the result will contain the nearest found paragraph when searching.

```console-result
{
    "took": 4,
    "timed_out": false,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 2,
            "relation": "eq"
        },
        "max_score": 1.0,
        "hits": [
            {
                "_index": "passage_vectors",
                "_id": "1",
                "_score": 1.0,
                "fields": {
                    "creation_time": [
                        "2019-05-04T00:00:00.000Z"
                    ],
                    "full_text": [
                        "first paragraph another paragraph"
                    ]
                },
                "inner_hits": {
                    "paragraph": {
                        "hits": {
                            "total": {
                                "value": 2,
                                "relation": "eq"
                            },
                            "max_score": 1.0,
                            "hits": [
                                {
                                    "_index": "passage_vectors",
                                    "_id": "1",
                                    "_nested": {
                                        "field": "paragraph",
                                        "offset": 0
                                    },
                                    "_score": 1.0,
                                    "fields": {
                                        "paragraph": [
                                            {
                                                "text": [
                                                    "first paragraph"
                                                ]
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                }
            },
            {
                "_index": "passage_vectors",
                "_id": "2",
                "_score": 0.9997144,
                "fields": {
                    "creation_time": [
                        "2020-05-04T00:00:00.000Z"
                    ],
                    "full_text": [
                        "number one paragraph number two paragraph"
                    ]
                },
                "inner_hits": {
                    "paragraph": {
                        "hits": {
                            "total": {
                                "value": 2,
                                "relation": "eq"
                            },
                            "max_score": 0.9997144,
                            "hits": [
                                {
                                    "_index": "passage_vectors",
                                    "_id": "2",
                                    "_nested": {
                                        "field": "paragraph",
                                        "offset": 1
                                    },
                                    "_score": 0.9997144,
                                    "fields": {
                                        "paragraph": [
                                            {
                                                "text": [
                                                    "number two paragraph"
                                                ]
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        ]
    }
}
```

### Search with nested vectors for chunked content [nested-knn-search-chunked-content]

Use nested kNN search with `dense_vector` fields and `inner_hits` in {{es}} to retrieve the most relevant passages from structured, chunked documents.

This approach is ideal when you:

* Chunk your content into paragraphs, sections, or other nested structures.
* Want to retrieve only the most relevant nested section of each matching document.
* Generate your own vectors with a custom model instead of relying on the [`semantic_text`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-text) field provided by Elastic's semantic search capability.

#### Create the index mapping

This example creates an index that stores a vector at the top level for the document title and multiple vectors inside a nested field for individual paragraphs.


```console
PUT nested_vector_index
{
  "mappings": {
    "properties": {
      "paragraphs": {
        "type": "nested",
        "properties": {
          "text": {
            "type": "text"
          },
          "vector": {
            "type": "dense_vector",
            "dims": 2,
            "index_options": {
              "type": "hnsw"
            }
          }
        }
      }
    }
  }
}
```

#### Index the documents

Add example documents with vectors for each paragraph.

```console
POST _bulk
{ "index": { "_index": "nested_vector_index", "_id": "1" } }
{ "paragraphs": [ { "text": "First paragraph", "vector": [0.5, 0.4] }, { "text": "Second paragraph", "vector": [0.3, 0.8] } ] }
{ "index": { "_index": "nested_vector_index", "_id": "2" } }
{ "paragraphs": [ { "text": "Another one", "vector": [0.1, 0.9] } ] }
```

#### Run the search query

This example searches for documents with relevant paragraph vectors.

```console
POST nested_vector_index/_search
{
  "_source": false,
  "knn": {
    "field": "paragraphs.vector",
    "query_vector": [0.5, 0.4],
    "k": 2,
    "num_candidates": 10,
    "inner_hits": {
      "size": 2,
      "name": "top_passages",
      "_source": false,
      "fields": ["paragraphs.text"]
    }
  }
}
```

The `inner_hits` block returns the most relevant paragraphs within each top-level document. Use the `size` parameter to control how many matches are returned. If your query includes multiple kNN clauses, set a unique `name` for each clause to avoid naming conflicts in the response.

```json
{
  "took": 4,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": { 
    "total": { 
      "value": 2, <1>
      "relation": "eq"
    }, 
    "max_score": 1,
    "hits": [ 
      {
        "_index": "nested_vector_index",
        "_id": "1",
        "_score": 1, <2>
        "inner_hits": { <3>
          "top_passages": {
            "hits": {
              "total": {
                "value": 2,
                "relation": "eq"
              },
              "max_score": 1,
              "hits": [
                {
                  "_index": "nested_vector_index",
                  "_id": "1",
                  "_nested": {
                    "field": "paragraphs",
                    "offset": 0
                  },
                  "_score": 1,
                  "fields": {
                    "paragraphs": [
                      {
                        "text": [
                          "First paragraph" <4>
                        ]
                      }
                    ]
                  }
                },
                {
                  "_index": "nested_vector_index",
                  "_id": "1",
                  "_nested": {
                    "field": "paragraphs",
                    "offset": 1
                  },
                  "_score": 0.92955077,
                  "fields": {
                    "paragraphs": [
                      {
                        "text": [
                          "Second paragraph"
                        ]
                      }
                    ]
                  }
                }
              ]
            }
          }
        }
      },
      {
        "_index": "nested_vector_index",
        "_id": "2",
        "_score": 0.8535534,
        "inner_hits": {
          "top_passages": {
            "hits": {
              "total": {
                "value": 1,
                "relation": "eq"
              },
              "max_score": 0.8535534,
              "hits": [
                {
                  "_index": "nested_vector_index",
                  "_id": "2",
                  "_nested": {
                    "field": "paragraphs",
                    "offset": 0
                  },
                  "_score": 0.8535534,
                  "fields": {
                    "paragraphs": [
                      {
                        "text": [
                          "Another one"
                        ]
                      }
                    ]
                  }
                }
              ]
            }
          }
        }
      }
    ]
  }
}
```

1. Two documents matched the query.
2. Document score, based on its most relevant paragraph.
3. Matching paragraphs appear in the `inner_hits` section.
4. Actual paragraph text that matched the query.

### Limitations for approximate kNN search [approximate-knn-limitations]

* When using kNN search in [{{ccs}}](../../../solutions/search/cross-cluster-search.md), the [`ccs_minimize_roundtrips`](../../../solutions/search/cross-cluster-search.md#ccs-min-roundtrips) option is not supported.
* {{es}} uses the [HNSW algorithm](https://arxiv.org/abs/1603.09320) for efficient kNN. Like most approximate methods, HNSW trades perfect accuracy for speed, so results aren’t always the true *k* closest neighbors.

::::{note}
Approximate kNN always uses the [`dfs_query_then_fetch`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) search type to gather the global top `k` matches across shards. You can’t set `search_type` explicitly for kNN search.
::::

### Oversampling and rescoring for quantized vectors [dense-vector-knn-search-rescoring]

When using [quantized vectors](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization) for kNN search, can optionally rescore results to balance performance and accuracy, by doing:

* **Oversampling** — retrieving more candidates per shard.
* **Rescoring** — recalculating scores on those oversampled candidates using the original (non-quantized) vectors.

Because final scores are computed with the original `float` vectors, rescoring combines:

* The performance and memory benefits of approximate retrieval with quantized vectors.
* The accuracy of using the original vectors for rescoring the top candidates.

All quantization introduces some accuracy loss, and higher compression generally increases that loss. In practice:

* `int8` typically needs little to no rescoring.
* `int4` often benefits from rescoring for higher accuracy or recall; 1.5×–2× oversampling usually recovers most loss.
* `bbq` commonly requires rescoring except on very large indices or models specifically designed for quantization; 3×–5× oversampling is generally sufficient, but higher may be needed for low-dimension vectors or embeddings that quantize poorly.

#### The `rescore_vector` option
```{applies_to}
stack: preview 9.0, ga 9.1
```

Use `rescore_vector` to automatically perform reranking. When you specify an `oversample` value, approximate kNN will:

* Retrieve `num_candidates` candidates per shard.
* Rescore the top `k * oversample` candidates per shard using the original vectors.
* Return the top `k` rescored candidates.

Here is an example of using the `rescore_vector` option with the `oversample` parameter:

```console
POST image-index/_search
{
  "knn": {
    "field": "image-vector",
    "query_vector": [-5, 9, -12],
    "k": 10,
    "num_candidates": 100,
    "rescore_vector": {
      "oversample": 2.0
    }
  },
  "fields": [ "title", "file-type" ]
}
```

This example will:

* Search using approximate kNN for the top 100 candidates.
* Rescore the top 20 candidates (`oversample * k`) per shard using the original, non quantized vectors.
* Return the top 10 (`k`) rescored candidates.
* Merge the rescored candidates from all shards, and return the top 10 (`k`) results.

#### The `on_disk_rescore` option
```{applies_to}
stack: preview 9.3
serverless: unavailable
```

By default, {{es}} reads raw vector data into memory to perform rescoring. This can have an effect on performance if the vector data is too large to all fit in off-heap memory at once. When the `on_disk_rescore: true` index setting is set, {{es}} reads vector data directly from disk during rescoring.

This setting only applies to newly indexed vectors. To apply the option to all vectors in the index, the vectors must be re-indexed or force-merged after changing the setting.

#### Additional rescoring techniques [dense-vector-knn-search-rescoring-rescore-additional]

The following sections provide additional ways of rescoring:

##### Use the `rescore` section for top-level kNN search [dense-vector-knn-search-rescoring-rescore-section]

You can use this option when you don’t want to rescore on each shard, but on the top results from all shards.

Use the [rescore section](elasticsearch://reference/elasticsearch/rest-apis/filter-search-results.md#rescore) in the `_search` request to rescore the top results from a kNN search.

Here is an example using the top level `knn` search with oversampling and using `rescore` to rerank the results:

```console
POST /my-index/_search
{
  "size": 10, <1>
  "knn": {
    "query_vector": [0.04283529, 0.85670587, -0.51402352, 0],
    "field": "my_int4_vector",
    "k": 20, <2>
    "num_candidates": 50
  },
  "rescore": {
    "window_size": 20, <3>
    "query": {
      "rescore_query": {
        "script_score": {
          "query": {
            "match_all": {}
          },
          "script": {
            "source": "(dotProduct(params.queryVector, 'my_int4_vector') + 1.0)", <4>
            "params": {
              "queryVector": [0.04283529, 0.85670587, -0.51402352, 0]
            }
          }
        }
      },
      "query_weight": 0, <5>
      "rescore_query_weight": 1 <6>
    }
  }
}
```

1. The number of results to return, note its only 10 and we will oversample by 2x, gathering 20 nearest neighbors.
2. The number of results to return from the KNN search. This will do an approximate KNN search with 50 candidates per HNSW graph and use the quantized vectors, returning the 20 most similar vectors according to the quantized score. Additionally, since this is the top-level `knn` object, the global top 20 results will from all shards will be gathered before rescoring. Combining with `rescore`, this is oversampling by `2x`, meaning gathering 20 nearest neighbors according to quantized scoring and rescoring with higher fidelity float vectors.
3. The number of results to rescore, if you want to rescore all results, set this to the same value as `k`
4. The script to rescore the results. Script score will interact directly with the originally provided float32 vector.
5. The weight of the original query, here we simply throw away the original score
6. The weight of the rescore query, here we only use the rescore query

##### Use a `script_score` query to rescore per shard [dense-vector-knn-search-rescoring-script-score]

You can use this option when you want to rescore on each shard and want more fine-grained control on the rescoring than the `rescore_vector` option provides.

Use rescore per shard with the [knn query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md) and [script_score query ](elasticsearch://reference/query-languages/query-dsl/query-dsl-script-score-query.md). Generally, this means that there will be more rescoring per shard, but this can increase overall recall at the cost of compute.

```console
POST /my-index/_search
{
  "size": 10, <1>
  "query": {
    "script_score": {
      "query": {
        "knn": { <2>
          "query_vector": [0.04283529, 0.85670587, -0.51402352, 0],
          "field": "my_int4_vector",
          "num_candidates": 20 <3>
        }
      },
      "script": {
        "source": "(dotProduct(params.queryVector, 'my_int4_vector') + 1.0)", <4>
        "params": {
          "queryVector": [0.04283529, 0.85670587, -0.51402352, 0]
        }
      }
    }
  }
}
```

1. The number of results to return
2. The `knn` query to perform the initial search, this is executed per-shard
3. The number of candidates to use for the initial approximate `knn` search. This will search using the quantized vectors and return the top 20 candidates per shard to then be scored
4. The script to score the results. Script score will interact directly with the originally provided float32 vector.

## Exact kNN search [exact-knn]

To run an exact kNN search, use a `script_score` query with a vector function.

1. Explicitly map one or more `dense_vector` fields. If you don’t intend to use the field for approximate kNN, set the `index` mapping option to `false`. This can significantly improve indexing speed.

    ```console
    PUT product-index
    {
      "mappings": {
        "properties": {
          "product-vector": {
            "type": "dense_vector",
            "dims": 5,
            "index": false
          },
          "price": {
            "type": "long"
          }
        }
      }
    }
    ```

2. Index your data.

    ```console
    POST product-index/_bulk?refresh=true
    { "index": { "_id": "1" } }
    { "product-vector": [230.0, 300.33, -34.8988, 15.555, -200.0], "price": 1599 }
    { "index": { "_id": "2" } }
    { "product-vector": [-0.5, 100.0, -13.0, 14.8, -156.0], "price": 799 }
    { "index": { "_id": "3" } }
    { "product-vector": [0.5, 111.3, -13.0, 14.8, -156.0], "price": 1099 }
    ...
    ```

3. Use the [search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) to run a `script_score` query containing a [vector function](elasticsearch://reference/query-languages/query-dsl/query-dsl-script-score-query.md#vector-functions).

    ::::{tip}
    To limit the number of matched documents passed to the vector function, we recommend you specify a filter query in the `script_score.query` parameter. If needed, you can use a [`match_all` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-all-query.md) in this parameter to match all documents. However, matching all documents can significantly increase search latency.
    ::::

    ```console
    POST product-index/_search
    {
      "query": {
        "script_score": {
          "query" : {
            "bool" : {
              "filter" : {
                "range" : {
                  "price" : {
                    "gte": 1000
                  }
                }
              }
            }
          },
          "script": {
            "source": "cosineSimilarity(params.queryVector, 'product-vector') + 1.0",
            "params": {
              "queryVector": [-0.5, 90.0, -10, 14.8, -156.0]
            }
          }
        }
      }
    }
    ```

A *k-nearest neighbor* (kNN) search finds the *k* nearest vectors to a query vector, as measured by a similarity metric.

Common use cases for kNN include:

* Relevance ranking based on natural language processing (NLP) algorithms
* Product recommendations and recommendation engines
* Similarity search for images or videos

::::{tip}
Check out our [hands-on tutorial](bring-own-vectors.md) to learn how to ingest dense vector embeddings into Elasticsearch.
::::
