---
navigation_title: Nested kNN search
description: Run approximate kNN search on nested dense_vector fields for passage retrieval, filtering, inner hits, and chunked content in Elasticsearch.
applies_to:
  stack:
  serverless:
---

# Nested kNN search [nested-knn-search]

Nested kNN search lets you find the most relevant passage or chunk inside long documents by storing a separate vector for each nested section and returning parent documents ranked by their best match. This approach is useful when a single document is too long to embed as one vector, such as when a support portal needs to surface the most relevant paragraph from a long troubleshooting guide in response to a user question.

This page covers a basic mapping and query example, filtering, inner hits, and chunked content retrieval. For other approximate kNN query examples, refer to [Examples of using approximate kNN in search queries](build-search-queries.md).

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

The query uses the same structure as a typical kNN search:

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


## Filtering in nested kNN search [nested-knn-search-filtering]

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

With the top-level `creation_time` filter applied, only document `1` falls within the specified range, so the response contains a single hit.

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

## Filtering by sibling nested fields [nested-knn-search-filtering-sibling]
```{applies_to}
stack: ga 9.2
```

Filter by sibling nested fields when passage vectors and the metadata you want to filter on live in separate nested structures within the same document. For example, you might search `paragraph.vector` for similar passages but only in documents whose `metadata` nested field lists a specific author or source.

Use a `nested` query in the `filter` clause to target the sibling nested field, such as `metadata.key` and `metadata.value`.

:::{important}
Sibling nested field filtering is only supported with the **top-level `knn` section** shown in the examples on this page. It does not work when using a [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md) inside a `nested` query. Retrieving `inner_hits` when filtering on sibling nested fields is also not supported.
:::

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

The response now includes an `inner_hits` section with the nearest matching passage for each parent document.

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

## Chunked content retrieval [nested-knn-search-chunked-content]

The patterns on this page apply directly to chunked content retrieval. Whether you chunk documents into paragraphs, sections, or other structures, the approach is the same: store each chunk's vector in a `nested` field and use `inner_hits` to return the most relevant chunk per document. If you use [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) fields, chunking and embedding are handled automatically. Use nested `dense_vector` fields when you need control over the chunking strategy, the embedding model, or chunk-level metadata filtering. For custom models, use the [basic nested kNN example](#nested-knn-basic-example) and [inner hits](#nested-knn-search-inner-hits) patterns on this page.

## Resources

- [Approximate kNN search](approximate-knn.md): Learn how to map, index, and run a basic approximate kNN search, including indexing considerations.
- [Optimize performance and accuracy](optimize-performance-accuracy.md): Tune search speed, recall, vector storage, quantization, and rescoring for approximate kNN search.
- [Exact kNN search](exact-knn.md): Run exact brute-force kNN search for small datasets or precise scoring.
- [Retrieval augmented generation (RAG)](../../rag.md): Retrieve relevant passages and combine them with generative AI models.
- [Semantic search with `semantic_text`](../../semantic-search/semantic-search-semantic-text.md): Use managed semantic search when you do not need to store passage vectors in nested fields yourself.
