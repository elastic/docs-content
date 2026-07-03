---
navigation_title: Nested kNN search
description: Run approximate kNN search on nested dense_vector fields for passage retrieval, filtering, inner hits, and chunked content in Elasticsearch.
applies_to:
  stack:
  serverless:
---

# Nested kNN search [nested-knn-search]

Nested kNN search lets you find the most relevant passage or chunk inside long documents by storing a separate vector for each nested section and returning parent documents ranked by their best match. This approach is useful when a single document is too long to embed as one vector, such as when a support portal needs to surface the most relevant paragraph from a long troubleshooting guide in response to a user question.

This page covers when to use nested kNN search, a basic mapping and query example, filtering, inner hits, and chunked content retrieval. For other approximate kNN query patterns, refer to [Build search queries](build-search-queries.md).

## Run a basic nested kNN search [nested-knn-basic-example]

When text exceeds a model’s token limit, chunking must be performed before generating embeddings for each chunk. By combining [`nested`](elasticsearch://reference/elasticsearch/mapping-reference/nested.md) fields with [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md), you can perform nearest passage retrieval without copying top-level document metadata.

:::{note}
Nested kNN queries only support [score_mode](elasticsearch://reference/query-languages/query-dsl/query-dsl-nested-query.md#nested-top-level-params)=`max`.
:::

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

With the above mapping, you can index multiple passage vectors along with storing the individual passage text.

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


## Filtering in nested KNN search [nested-knn-search-filtering]

Use filters in nested kNN search when you want the most similar passages, but only from documents or chunks that match specific criteria. For example, you might search for relevant paragraphs in documents created in a date range, written in a particular language, or authored by a specific person.

Add a `filter` to your `knn` clause to apply these restrictions during the search.

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

## Filtering on nested metadata [nested-knn-search-filtering-nested-metatadata]
```{applies_to}
stack: ga 9.2
```

Filter on nested metadata when your criteria apply to individual passages or chunks, not the whole document. For example, you might search for similar paragraphs but only among sections in a specific language or tagged with a particular category.

The following query filters on `paragraph.language` so parent documents are scored only from nested vectors where the language is `EN`.

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

## Filtering by sibling nested fields in nested KNN search [nested-knn-search-filtering-sibling]
```{applies_to}
stack: ga 9.2
```

Filter by sibling nested fields when passage vectors and the metadata you want to filter on live in separate nested structures within the same document. For example, you might search `paragraph.vector` for similar passages but only in documents whose `metadata` nested field lists a specific author or source.

Use a `nested` query in the `filter` clause to target the sibling nested field, such as `metadata.key` and `metadata.value`.

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

## Nested kNN search with inner hits [nested-knn-search-inner-hits]

Use `inner_hits` when nested kNN search should return both the matching parent document and the specific passage that produced the score.

Add [inner_hits](elasticsearch://reference/elasticsearch/rest-apis/retrieve-inner-hits.md) to the `knn` clause to include the nearest matching nested passage in the response.

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
* Generate your own vectors with a custom model instead of relying on the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field provided by Elastic's semantic search capability.

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

## Resources

- [Approximate kNN search](approximate-knn.md): Learn how to map, index, and run a basic approximate kNN search, including indexing considerations and limitations.
- [Build search queries](build-search-queries.md): Learn how to construct approximate kNN queries for filtering, hybrid retrieval, semantic search, multiple vector fields, and similarity thresholds.
- [Optimize performance and accuracy](optimize-performance-accuracy.md): Learn how to tune search speed, recall, vector storage, quantization, and rescoring for approximate kNN search.
- [kNN search on {{es}}](../knn.md): Explore common use cases, prerequisites for kNN search, and a comparison of approximate and exact kNN methods.
- [Exact kNN search](exact-knn.md): Learn how to run exact brute-force kNN search with `script_score` queries for small datasets or precise scoring.
- [Retrieval augmented generation (RAG)](../../rag.md): Learn how to retrieve relevant passages and combine them with generative AI models.
- [Semantic search with `semantic_text`](../../semantic-search/semantic-search-semantic-text.md): Use managed semantic search when you do not need to store passage vectors in nested fields yourself.
- [Vector search in {{es}}](../../vector.md): Learn the core concepts and terminology for vector search in {{es}}, including embeddings, field types, and how vector retrieval fits with other search strategies.
- [Retrieve inner hits](elasticsearch://reference/elasticsearch/rest-apis/retrieve-inner-hits.md): API reference for `inner_hits` options used to return matching nested passages.
- [Knn query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md): API reference for the `knn` query, including parameters, `query_vector_builder` options, and usage with `dense_vector` and `semantic_text` fields.
