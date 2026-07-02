---
navigation_title: Build search queries
description: Construct approximate kNN queries in Elasticsearch for filtering, hybrid retrieval, semantic search, multiple vector fields, similarity thresholds, and nested chunked content.
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Build search queries [build-approximate-knn-queries]

This page shows how to construct approximate kNN queries for common retrieval patterns, including filtering, hybrid retrieval, semantic search, multiple vector fields, similarity thresholds, and nested or chunked content.

## Filtered kNN search [knn-search-filter-example]

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

## Approximate kNN search and filtering [approximate-knn-search-and-filtering]

In approximate kNN search with an HNSW index, applying filters can decrease performance as the engine must explore more of the graph to gather enough candidates that satisfy the filter and reach `num_candidates`. This contrasts with conventional query filtering, where stricter filters often speed up queries.

To avoid significant performance drawbacks, Lucene implements the following strategies per segment:

* If the filtered document count is less than or equal to num_candidates, the search bypasses the HNSW graph and uses a brute force search on the filtered documents.
* While exploring the HNSW graph, if the number of nodes explored exceeds the number of documents that satisfy the filter, the search will stop exploring the graph and switch to a brute force search over the filtered documents.

## Combine approximate kNN with other features [_combine_approximate_knn_with_other_features]

You can perform **hybrid retrieval** by combining the [`knn` option]({{es-apis}}operation/operation-search#operation-search-body-application-json-knn) with a standard [`query`]({{es-apis}}operation/operation-search#operation-search-query). This blends vector similarity with lexical relevance, filters, and aggregations.

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

The score of each result is the sum of the `knn` and `query` scores. You can specify a `boost` value to give a weight to each score in the sum. In the preceding example, the scores will be calculated as

```
score = 0.9 * match_score + 0.1 * knn_score
```

The `knn` option can also be used with [`aggregations`](../../../../explore-analyze/query-filter/aggregations.md). In general, {{es}} computes aggregations over all documents that match the search. So for approximate kNN search, aggregations are calculated on the top `k` nearest documents. If the search also includes a `query`, then aggregations are calculated on the combined set of `knn` and `query` matches.

## Perform semantic search [knn-semantic-search]

:::{tip}
Looking for a minimal configuration approach? The `semantic_text` field type abstracts these vector search implementations with sensible defaults and automatic model management. It's the recommended approach for most users. [Learn more about semantic_text](../../semantic-search/semantic-search-semantic-text.md).
:::

kNN search enables you to perform semantic search by using a previously deployed [text embedding model](../../../../explore-analyze/machine-learning/nlp/ml-nlp-search-compare.md#ml-nlp-text-embedding). Instead of literal matching on search terms, semantic search retrieves results based on the intent and the contextual meaning of a search query.

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

1. The task to perform. In this case, it is `text_embedding`.
2. The ID of the text embedding model used to generate the query’s dense vector. Use the same model that produced the document embeddings in the target index. You can also provide the `deployment_id` as the `model_id` value.
3. The query string from which the model generates the dense vector representation.

:::{tip}
For an overview of `query_vector_builder` options (`text_embedding`, `embedding`, and `lookup`), refer to [Build query vectors for knn search](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md#build-query-vectors-for-knn-search).
:::


For more information on how to deploy a trained model and use it to create text embeddings, refer to this [end-to-end example](../../../../explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md).

## Search multiple kNN fields [_search_multiple_knn_fields]

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

## Search kNN with expected similarity [knn-similarity-search]

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

## Nested kNN search [nested-knn-search]

When text exceeds a model’s token limit, chunking must be performed before generating embeddings for each chunk. By combining [`nested`](elasticsearch://reference/elasticsearch/mapping-reference/nested.md) fields with [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md), you can perform nearest passage retrieval without copying top-level document metadata.  
Note that nested kNN queries only support [score_mode](elasticsearch://reference/query-languages/query-dsl/query-dsl-nested-query.md#nested-top-level-params)=`max`.

Here is a basic passage vectors index that stores vectors and some top-level metadata for filtering.

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

Note that even with 4 total nested vectors, the response still returns two documents. kNN search over nested dense vectors will always diversify the top results over the top-level document. `"k"` top-level documents will be returned, scored by their nearest passage vector (for example, `"paragraph.vector"`).

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

### Filtering in nested KNN search [nested-knn-search-filtering]

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

#### Filtering on nested metadata [nested-knn-search-filtering-nested-metatadata]
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

### Filtering by sibling nested fields in nested KNN search [nested-knn-search-filtering-sibling]
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

## Nested kNN Search with Inner hits [nested-knn-search-inner-hits]

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

## Search with nested vectors for chunked content [nested-knn-search-chunked-content]

Use nested kNN search with `dense_vector` fields and `inner_hits` in {{es}} to retrieve the most relevant passages from structured, chunked documents.

This approach is ideal when you:

* Chunk your content into paragraphs, sections, or other nested structures.
* Want to retrieve only the most relevant nested section of each matching document.
* Generate your own vectors with a custom model instead of relying on the [`semantic_text`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-text) field provided by Elastic's semantic search capability.

### Create the index mapping

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

### Index the documents

Add example documents with vectors for each paragraph.

```console
POST _bulk
{ "index": { "_index": "nested_vector_index", "_id": "1" } }
{ "paragraphs": [ { "text": "First paragraph", "vector": [0.5, 0.4] }, { "text": "Second paragraph", "vector": [0.3, 0.8] } ] }
{ "index": { "_index": "nested_vector_index", "_id": "2" } }
{ "paragraphs": [ { "text": "Another one", "vector": [0.1, 0.9] } ] }
```

### Run the search query

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

