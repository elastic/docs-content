---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-knn-search.html
applies_to:
  stack:
  serverless:
---

# kNN search [knn-search]


A *k-nearest neighbor* (kNN) search finds the *k* nearest vectors to a query vector, as measured by a similarity metric.

Common use cases for kNN include:

* Search
  * Semantic text search
  * Image/video similarity

* Recommendations
  * Product suggestions
  * Collaborative filtering
  * Content discovery

* Analysis
  * Anomaly detection
  * Pattern matching

## Prerequisites [knn-prereqs]

* To run a kNN search, your data must be transformed into vectors. You can [use an NLP model in {{es}}](../../../explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md), or generate them outside {{es}}.
  - Dense vectors need to use the [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) field type.
  - Queries are represented as vectors with the same dimension. You should use the same model to generate the query vector as you used to generate the document vectors.
  - If you already have vectors, refer to the [Bring your own dense vectors](bring-own-vectors.md) guide.

* To complete the steps in this guide, you must have the following [index privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices):

    * `create_index` or `manage` to create an index with a `dense_vector` field
    * `create`, `index`, or `write` to add data to the index you created
    * `read` to search the index

## kNN methods [knn-methods]

{{es}} supports two methods for kNN search:

* [Approximate kNN](#approximate-knn) using the `knn` search option, `knn` query or a `knn` [retriever](../retrievers-overview.md)
* [Exact, brute-force kNN](#exact-knn) using a `script_score` query with a vector function

In most cases, you’ll want to use approximate kNN. Approximate kNN offers lower latency at the cost of slower indexing and imperfect accuracy.

Exact, brute-force kNN guarantees accurate results but doesn’t scale well with large datasets. With this approach, a `script_score` query must scan each matching document to compute the vector function, which can result in slow search speeds. However, you can improve latency by using a [query](../../../explore-analyze/query-filter/languages/querydsl.md) to limit the number of matching documents passed to the function. If you filter your data to a small subset of documents, you can get good search performance using this approach.


## Approximate kNN [approximate-knn]

::::{warning}
Compared to other types of search, approximate kNN search has specific resource requirements. In particular, all vector data must fit in the node’s page cache for it to be efficient. Please consult the [approximate kNN search tuning guide](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md) for important notes on configuration and sizing.
::::

To run an approximate kNN search, use the [`knn` option](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-knn) to search one or more `dense_vector` fields with indexing enabled.

1. Explicitly map one or more `dense_vector` fields. Approximate kNN search requires the following mapping options:

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

2. Index your data.

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

3. Run the search using the [`knn` option](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-knn) or the [`knn` query](elasticsearch://reference/query-languages/query-dsl-knn-query.md) (expert case).

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


The document `_score` is a positive 32-bit floating point number used to score the relevance of the returned document, determined by the similarity between the query and document vector. See [`similarity`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-similarity) for more information on how kNN search scores are computed.

::::{note}
Support for approximate kNN search was added in version 8.0. Before this, `dense_vector` fields did not support enabling `index` in the mapping. If you created an index prior to 8.0 containing `dense_vector` fields, then to support approximate kNN search the data must be reindexed using a new field mapping that sets `index: true` which is the default option.
::::

### Indexing considerations [knn-indexing-considerations]

For approximate kNN search, {{es}} stores the dense vector values of each segment as an [HNSW graph](https://arxiv.org/abs/1603.09320). Indexing vectors for approximate kNN search can take substantial time because of how expensive it is to build these graphs. You may need to increase the client request timeout for index and bulk requests. The [approximate kNN tuning guide](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md) contains important guidance around indexing performance, and how the index configuration can affect search performance.

In addition to its search-time tuning parameters, the HNSW algorithm has index-time parameters that trade off between the cost of building the graph, search speed, and accuracy. When setting up the `dense_vector` mapping, you can use the [`index_options`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-index-options) argument to adjust these parameters:

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

To gather results, the kNN search API finds a `num_candidates` number of approximate nearest neighbor candidates on each shard. The search computes the similarity of these candidate vectors to the query vector, selecting the `k` most similar results from each shard. The search then merges the results from each shard to return the global top `k` nearest neighbors.

You can increase `num_candidates` for more accurate results at the cost of slower search speeds. A search with a high value for `num_candidates` considers more candidates from each shard. This takes more time, but the search has a higher probability of finding the true `k` top nearest neighbors.

Similarly, you can decrease `num_candidates` for faster searches with potentially less accurate results.


### Approximate kNN using byte vectors [approximate-knn-using-byte-vectors]

The approximate kNN search API supports `byte` value vectors in addition to `float` value vectors. Use the [`knn` option](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-knn) to search a `dense_vector` field with [`element_type`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-params) set to `byte` and indexing enabled.

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
%  TEST[continued]
%  TEST[s/"k": 10/"k": 3/]
%  TEST[s/"num_candidates": 100/"num_candidates": 3/]


### Byte quantized kNN search [knn-search-quantized-example]

If you want to provide `float` vectors, but want the memory savings of `byte` vectors, you can use the [quantization](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization) feature. Quantization allows you to provide `float` vectors, but internally they are indexed as `byte` vectors. Additionally, the original `float` vectors are still retained in the index.

::::{note}
The default index type for `dense_vector` is `int8_hnsw`.
::::


To use quantization, you can use the index type `int8_hnsw` or `int4_hnsw` object in the `dense_vector` mapping.

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
%  TEST[continued]

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


Since the original `float` vectors are still retained in the index, you can optionally use them for re-scoring. Meaning, you can search over all the vectors quickly using the `int8_hnsw` index and then rescore only the top `k` results. This provides the best of both worlds, fast search and accurate scoring.

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
%  TEST[continued]
%  TEST[s/"k": 15/"k": 3/]
%  TEST[s/"num_candidates": 100/"num_candidates": 3/]


### Filtered kNN search [knn-search-filter-example]

The kNN search API supports restricting the search using a filter. The search will return the top `k` documents that also match the filter query.

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
%  TEST[continued]

::::{note}
The filter is applied **during** the approximate kNN search to ensure that `k` matching documents are returned. This contrasts with a post-filtering approach, where the filter is applied **after** the approximate kNN search completes. Post-filtering has the downside that it sometimes returns fewer than k results, even when there are enough matching documents.
::::



### Approximate kNN search and filtering [approximate-knn-search-and-filtering]

Unlike conventional query filtering, where more restrictive filters typically lead to faster queries, applying filters in an approximate kNN search with an HNSW index can decrease performance. This is because searching the HNSW graph requires additional exploration to obtain the `num_candidates` that meet the filter criteria.

To avoid significant performance drawbacks, Lucene implements the following strategies per segment:

* If the filtered document count is less than or equal to num_candidates, the search bypasses the HNSW graph and uses a brute force search on the filtered documents.
* While exploring the HNSW graph, if the number of nodes explored exceeds the number of documents that satisfy the filter, the search will stop exploring the graph and switch to a brute force search over the filtered documents.


### Combine approximate kNN with other features [_combine_approximate_knn_with_other_features]

You can perform *hybrid retrieval* by providing both the [`knn` option](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-knn) and a [`query`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-query):

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
%  TEST[continued]

This search finds the global top `k = 5` vector matches, combines them with the matches from the `match` query, and finally returns the 10 top-scoring results. The `knn` and `query` matches are combined through a disjunction, as if you took a boolean *or* between them. The top `k` vector results represent the global nearest neighbors across all index shards.

The score of each hit is the sum of the `knn` and `query` scores. You can specify a `boost` value to give a weight to each score in the sum. In the example above, the scores will be calculated as

```
score = 0.9 * match_score + 0.1 * knn_score
```

The `knn` option can also be used with [`aggregations`](../../../explore-analyze/query-filter/aggregations.md). In general, {{es}} computes aggregations over all documents that match the search. So for approximate kNN search, aggregations are calculated on the top `k` nearest documents. If the search also includes a `query`, then aggregations are calculated on the combined set of `knn` and `query` matches.


### Perform semantic search [knn-semantic-search]

:::{tip}
Looking for a minimal configuration approach? The `semantic_text` field type provides an abstraction over these vector search implementations with sensible defaults and automatic model management. It's the recommended approach for most users. [Learn more about semantic_text](../semantic-search/semantic-search-semantic-text.md).
:::

kNN search enables you to perform semantic search by using a previously deployed [text embedding model](../../../explore-analyze/machine-learning/nlp/ml-nlp-search-compare.md#ml-nlp-text-embedding). Instead of literal matching on search terms, semantic search retrieves results based on the intent and the contextual meaning of a search query.

Under the hood, the text embedding NLP model generates a dense vector from the input query string called `model_text` you provide. Then, it is searched against an index containing dense vectors created with the same text embedding {{ml}} model. The search results are semantically similar as learned by the model.

::::{important}
To perform semantic search:

* you need an index that contains the dense vector representation of the input data to search against,
* you must use the same text embedding model for search that you used to create the dense vectors from the input data,
* the text embedding NLP model deployment must be started.

::::


Reference the deployed text embedding model or the model deployment in the `query_vector_builder` object and provide the search query as `model_text`:

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
2. The ID of the text embedding model to use to generate the dense vectors from the query string. Use the same model that generated the embeddings from the input text in the index you search against. You can use the value of the `deployment_id` instead in the `model_id` argument.
3. The query string from which the model generates the dense vector representation.
%  NOTCONSOLE

For more information on how to deploy a trained model and use it to create text embeddings, refer to this [end-to-end example](../../../explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md).


### Search multiple kNN fields [_search_multiple_knn_fields]

In addition to *hybrid retrieval*, you can search more than one kNN vector field at a time:

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
%  TEST[continued]

This search finds the global top `k = 5` vector matches for `image-vector` and the global `k = 10` for the `title-vector`. These top values are then combined with the matches from the `match` query and the top-10 documents are returned. The multiple `knn` entries and the `query` matches are combined through a disjunction, as if you took a boolean *or* between them. The top `k` vector results represent the global nearest neighbors across all index shards.

The scoring for a doc with the above configured boosts would be:

```
score = 0.9 * match_score + 0.1 * knn_score_image-vector + 0.5 * knn_score_title-vector
```

### Search kNN with expected similarity [knn-similarity-search]

While kNN is a powerful tool, it always tries to return `k` nearest neighbors. Consequently, when using `knn` with a `filter`, you could filter out all relevant documents and only have irrelevant ones left to search. In that situation, `knn` will still do its best to return `k` nearest neighbors, even though those neighbors could be far away in the vector space.

To alleviate this worry, there is a `similarity` parameter available in the `knn` clause. This value is the required minimum similarity for a vector to be considered a match. The `knn` search flow with this parameter is as follows:

* Apply any user provided `filter` queries
* Explore the vector space to get `k` vectors
* Do not return any vectors that are further away than the configured `similarity`

::::{note}
`similarity` is the true [similarity](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-similarity) before it has been transformed into `_score` and boost applied.
::::


For each configured [similarity](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-similarity), here is the corresponding inverted `_score` function. This is so if you are wanting to filter from a `_score` perspective, you can do this minor transformation to correctly reject irrelevant results.

* `l2_norm`: `sqrt((1 / _score) - 1)`
* `cosine`: `(2 * _score) - 1`
* `dot_product`: `(2 * _score) - 1`
* `max_inner_product`:

    * `_score < 1`: `1 - (1 / _score)`
    * `_score >= 1`: `_score - 1`


Here is an example. In this example we search for the given `query_vector` for `k` nearest neighbors. However, with `filter` applied and requiring that the found vectors have at least the provided `similarity` between them.

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
%  TEST[continued]

In our data set, the only document with the file type of `png` has a vector of `[42, 8, -15]`. The `l2_norm` distance between `[42, 8, -15]` and `[1, 5, -20]` is `41.412`, which is greater than the configured similarity of `36`. Meaning, this search will return no hits.


### Nested kNN Search [nested-knn-search]

It is common for text to exceed a particular model’s token limit and requires chunking before building the embeddings for individual chunks. When using [`nested`](elasticsearch://reference/elasticsearch/mapping-reference/nested.md) with [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md), you can achieve nearest passage retrieval without copying top-level document metadata.

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
                    }
                }
            }
        }
    }
}
```
% TEST[continued]

With the above mapping, we can index multiple passage vectors along with storing the individual passage text.

```console
POST passage_vectors/_bulk?refresh=true
{ "index": { "_id": "1" } }
{ "full_text": "first paragraph another paragraph", "creation_time": "2019-05-04", "paragraph": [ { "vector": [ 0.45, 45 ], "text": "first paragraph", "paragraph_id": "1" }, { "vector": [ 0.8, 0.6 ], "text": "another paragraph", "paragraph_id": "2" } ] }
{ "index": { "_id": "2" } }
{ "full_text": "number one paragraph number two paragraph", "creation_time": "2020-05-04", "paragraph": [ { "vector": [ 1.2, 4.5 ], "text": "number one paragraph", "paragraph_id": "1" }, { "vector": [ -1, 42 ], "text": "number two paragraph", "paragraph_id": "2" } ] }
```
% TEST[continued]
% TEST[s/...//]

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
        "k": 2,
        "num_candidates": 2
    }
}
```
% TEST[continued]

Note below that even though we have 4 total vectors, we still return two documents. kNN search over nested dense_vectors will always diversify the top results over the top-level document. Meaning, `"k"` top-level documents will be returned, scored by their nearest passage vector (e.g. `"paragraph.vector"`).

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
%  TESTRESPONSE[s/"took": 4/"took" : "$body.took"/]

What if you wanted to filter by some top-level document metadata? You can do this by adding `filter` to your `knn` clause.

::::{note}
`filter` will always be over the top-level document metadata. This means you cannot filter based on `nested` field metadata.
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
        "filter": {
            "bool": {
                "filter": [
                    {
                        "range": {
                            "creation_time": {
                                "gte": "2019-05-01",
                                "lte": "2019-05-05"
                            }
                        }
                    }
                ]
            }
        }
    }
}
```
% TEST[continued]

Now we have filtered based on the top level `"creation_time"` and only one document falls within that range.

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
%  TESTRESPONSE[s/"took": 4/"took" : "$body.took"/]


### Nested kNN Search with Inner hits [nested-knn-search-inner-hits]

Additionally, if you wanted to extract the nearest passage for a matched document, you can supply [inner_hits](elasticsearch://reference/elasticsearch/rest-apis/retrieve-inner-hits.md) to the `knn` clause.

::::{note}
When using `inner_hits` and multiple `knn` clauses, be sure to specify the [`inner_hits.name`](elasticsearch://reference/elasticsearch/rest-apis/retrieve-inner-hits.md#inner-hits-options) field. Otherwise, a naming clash can occur and fail the search request.
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
% TEST[continued]

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
%  TESTRESPONSE[s/"took": 4/"took" : "$body.took"/]

### Limitations for approximate kNN search [approximate-knn-limitations]

* When using kNN search in [{{ccs}}](../../../solutions/search/cross-cluster-search.md), the [`ccs_minimize_roundtrips`](../../../solutions/search/cross-cluster-search.md#ccs-min-roundtrips) option is not supported.
* {{es}} uses the [HNSW algorithm](https://arxiv.org/abs/1603.09320) to support efficient kNN search. Like most kNN algorithms, HNSW is an approximate method that sacrifices result accuracy for improved search speed. This means the results returned are not always the true *k* closest neighbors.

::::{note}
Approximate kNN search always uses the [`dfs_query_then_fetch`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) search type in order to gather the global top `k` matches across shards. You cannot set the `search_type` explicitly when running kNN search.
::::



### Oversampling and rescoring for quantized vectors [dense-vector-knn-search-rescoring]

When using [quantized vectors](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization) for kNN search, you can optionally rescore results to balance performance and accuracy, by doing:

* **Oversampling**: Retrieve more candidates per shard.
* **Rescoring**: Use the original vector values for re-calculating the score on the oversampled candidates.

As the non-quantized, original vectors are used to calculate the final score on the top results, rescoring combines:

* The performance and memory gains of approximate retrieval using quantized vectors for retrieving the top candidates.
* The accuracy of using the original vectors for rescoring the top candidates.

All forms of quantization will result in some accuracy loss and as the quantization level increases the accuracy loss will also increase. Generally, we have found that:

* `int8` requires minimal if any rescoring
* `int4` requires some rescoring for higher accuracy and larger recall scenarios. Generally, oversampling by 1.5x-2x recovers most of the accuracy loss.
* `bbq` requires rescoring except on exceptionally large indices or models specifically designed for quantization. We have found that between 3x-5x oversampling is generally sufficient. But for fewer dimensions or vectors that do not quantize well, higher oversampling may be required.

You can use the `rescore_vector` [preview] option to automatically perform reranking. When a rescore `oversample` parameter is specified, the approximate kNN search will:

* Retrieve `num_candidates` candidates per shard.
* From these candidates, the top `k * oversample` candidates per shard will be rescored using the original vectors.
* The top `k` rescored candidates will be returned.

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
% TEST[continued]
%  TEST[s/"k": 10/"k": 3/]
%  TEST[s/"num_candidates": 100/"num_candidates": 3/]

This example will:

* Search using approximate kNN for the top 100 candidates.
* Rescore the top 20 candidates (`oversample * k`) per shard using the original, non quantized vectors.
* Return the top 10 (`k`) rescored candidates.
* Merge the rescored canddidates from all shards, and return the top 10 (`k`) results.


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
%  TEST[skip: setup not provided]


##### Use a `script_score` query to rescore per shard [dense-vector-knn-search-rescoring-script-score]

You can use this option when you want to rescore on each shard and want more fine-grained control on the rescoring than the `rescore_vector` option provides.

Use rescore per shard with the [knn query](elasticsearch://reference/query-languages/query-dsl-knn-query.md) and [script_score query ](elasticsearch://reference/query-languages/query-dsl-script-score-query.md). Generally, this means that there will be more rescoring per shard, but this can increase overall recall at the cost of compute.

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
%  TEST[skip: setup not provided]


## Exact kNN [exact-knn]

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

3. Use the [search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) to run a `script_score` query containing a [vector function](elasticsearch://reference/query-languages/query-dsl-script-score-query.md#vector-functions).

    ::::{tip}
    To limit the number of matched documents passed to the vector function, we recommend you specify a filter query in the `script_score.query` parameter. If needed, you can use a [`match_all` query](elasticsearch://reference/query-languages/query-dsl-match-all-query.md) in this parameter to match all documents. However, matching all documents can significantly increase search latency.
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