---
navigation_title: kNN search in Elasticsearch
description: Find semantically similar documents using k-nearest neighbor (kNN) vector search in Elasticsearch.
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-knn-search.html
applies_to:
  stack:
  serverless:
---

# kNN search in {{es}} [knn-search]

A *k-nearest neighbor* (kNN) search finds the *k* nearest vectors to a query vector using a similarity metric such as cosine or L2 norm. In {{es}}, kNN is the primary way to query [`dense_vector`](dense-vector.md) fields after you store embeddings.



## Common use cases for kNN vector similarity search

kNN vector similarity search supports use cases across search, recommendations, and analysis:

- **Search**
  - [Semantic text search](../semantic-search.md): Find documents that match the meaning of a query, even when the wording differs.
  - [Image and video similarity](vector-search-use-cases.md#multimodal-search): Search across text, images, audio, or video to find visually or semantically similar content.

- **Recommendations**
  - [Product recommendations](vector-search-use-cases.md#discovery-and-recommendations): Surface items similar to what a user is viewing or has interacted with.
  - [Collaborative filtering](vector-search-use-cases.md#discovery-and-recommendations): Match users or items based on shared behavior or preference patterns in vector space.
  - [Personalized content discovery](vector-search-use-cases.md#discovery-and-recommendations): Suggest articles, media, or other content tailored to individual user interests.

- **Analysis**
  - [{{anomaly-detect-cap}}](vector-search-use-cases.md#duplicate-detection-fraud-and-anomaly-detection): Flag records whose vectors sit unusually far from their nearest neighbors.
  - [Pattern matching](vector-search-use-cases.md#duplicate-detection-fraud-and-anomaly-detection): Find near-duplicates, suspicious matches, or other patterns that exact matching would miss.

## Prerequisites for kNN search [knn-prereqs]

To run a kNN search in {{es}}:

- Your data must be vectorized. You can:
  - Use [`semantic_text`](/solutions/search/semantic-search/semantic-search-semantic-text.md) to have Elastic generate embeddings automatically.
  - Use the [Elastic {{infer-cap}} Service](/explore-analyze/elastic-inference/eis.md) for managed {{infer}}.
  - [Deploy an NLP model](/explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md) on an ML node.
  - Generate vectors outside of your Elastic deployment. Learn how to [Bring your own dense vectors](bring-own-vectors.md).

:::{tip}
Query vectors must have the same dimension and be created with the same model as the document vectors.

After you index vectors, [confirm that they are searchable](#verify-embeddings).
:::

- Required [index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices):
  - `create_index` or `manage` to create an index with a `dense_vector` field
  - `create`, `index`, or `write` to add data
  - `read` to search the index

If you're using {{serverless-full}}, [compare {{es}} and {{vectordb}} projects](/solutions/vector-database.md#when-to-use-this-project-type) before implementing kNN search.

## Confirm that your vectors are searchable [verify-embeddings]

After you index documents, {{es}} can return a successful response even when those documents have no vector that a kNN search can use. This can happen when the ingest pipeline that contains the {{infer}} processor isn't applied to the indexing request, or when the {{infer}} processor is configured to ignore processor failures or missing input fields.

Before you run a kNN search, use this checklist to confirm that your vectors are searchable:

- [Check that the document has embeddings](#verify-embeddings-stored).
- [Check that the field mapping supports kNN search](#verify-embeddings-mapping).
- [Check that indexing and search use the same model](#verify-embeddings-endpoint).
- [Check that search returns the expected document](#verify-embeddings-query).

### Check that the document has embeddings [verify-embeddings-stored]

Confirm that the document contains embeddings in the expected field.

Use the example for your field type. For a `semantic_text` field, select your deployment type or the {{stack}} version in which the index was created. Upgrading {{stack}} doesn't change this behavior for existing indices.

:::::::{tab-set}
::::::{tab-item} `dense_vector`
Retrieve the document by ID and include only the `dense_vector` field. Replace `my-index`, `1`, and `dense-vector-field` with the values for your document:

```console
GET my-index/_doc/1?_source_includes=dense-vector-field
```

A stored vector appears in `_source` as an array of numbers.

:::{dropdown} Example response
:open:
```console-result
{
  "_index": "my-index",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "dense-vector-field": [ <1>
      1,
      0,
      0
    ]
  }
}
```

1. The stored vector values. The presence of this array confirms that the document has a vector in the requested field.
:::
::::::

::::::{tab-item} `semantic_text`
:::::{applies-switch}
::::{applies-item} { stack: ga 9.2+, serverless: ga }
Include the embeddings in `_source`:

```console
POST my-index/_search
{
  "_source": {
    "exclude_vectors": false <1>
  },
  "query": {
    "ids": {
      "values": ["1"] <2>
    }
  }
}
```

1. Includes the stored embeddings in `_source`. Vector data is excluded by default.
2. Identifies the document to check. Replace `1` with the ID of a document you indexed.

Stored embeddings appear under `_inference_fields` in `_source`.

:::{dropdown} Example response
:open:
```console-result
{
  "took": 35,
  "timed_out": false,
  "_shards": {
    "total": 6,
    "successful": 6,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "my-index",
        "_id": "1",
        "_score": 1,
        "_source": {
          "content": "Paris is the capital of France.",
          "_inference_fields": {
            "content": {
              "inference": {
                "inference_id": ".jina-embeddings-v5-text-small",
                "model_settings": {
                  "service": "elastic",
                  "task_type": "text_embedding",
                  "dimensions": 1024,
                  "similarity": "cosine",
                  "element_type": "float"
                },
                "chunks": {
                  "content": [
                    {
                      "start_offset": 0,
                      "end_offset": 31,
                      "embeddings": [ <1>
                        -0.026611328,
                        0.045166016,
                        -0.006439209,
                        ...
                        -0.036621094
                      ]
                    }
                  ]
                }
              }
            }
          }
        }
      }
    ]
  }
}
```

1. The stored embedding for this text chunk. The example omits most values from the 1024-dimension vector.
:::
::::

::::{applies-item} stack: ga 9.0-9.1
Request the internal inference fields:

```console
POST my-index/_search
{
  "query": {
    "ids": {
      "values": ["1"] <1>
    }
  },
  "fields": ["_inference_fields"] <2>
}
```

1. Identifies the document to check. Replace `1` with the ID of a document you indexed.
2. Requests the internal inference data, including the stored embeddings.

Stored embeddings appear under `_inference_fields` in `_source`.

:::{dropdown} Example response
:open:
```console-result
{
  "took": 3,
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
    "max_score": 1,
    "hits": [
      {
        "_index": "my-index",
        "_id": "1",
        "_score": 1,
        "_source": {
          "content": "Paris is the capital of France.",
          "_inference_fields": {
            "content": {
              "inference": {
                "inference_id": ".multilingual-e5-small-elasticsearch",
                "model_settings": {
                  "service": "elasticsearch",
                  "task_type": "text_embedding",
                  "dimensions": 384,
                  "similarity": "cosine",
                  "element_type": "float"
                },
                "chunks": {
                  "content": [
                    {
                      "start_offset": 0,
                      "end_offset": 31,
                      "embeddings": [ <1>
                        0.007674215,
                        -0.0059343106,
                        0.023091488,
                        ...
                        0.07972942
                      ]
                    }
                  ]
                }
              }
            }
          }
        }
      }
    ]
  }
}
```

1. The stored 384-dimension embedding. The example omits most values.
:::
::::
:::::
::::::
:::::::

If the expected field is missing, the ingest pipeline might not have run, or the {{infer}} processor might have failed. Learn more about how {{es}} handles processor failures in [Handling pipeline failures](/manage-data/ingest/transform-enrich/ingest-pipelines.md#handling-pipeline-failures).

### Check that the field mapping supports kNN search [verify-embeddings-mapping]

Confirm that the field mapping supports kNN search.

The field mapping controls how {{es}} stores and searches embeddings. A kNN search can search:

- A `dense_vector` field with `index: true`.
- A `semantic_text` field that uses a dense embedding model.

It can't search a `sparse_vector` field or a `semantic_text` field that uses a sparse embedding model such as ELSER. Use a [`sparse_vector` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-sparse-vector-query.md) or a `match` query on the `semantic_text` field instead.

Use the example for your field type:

:::::{tab-set}
::::{tab-item} `dense_vector`
Retrieve the index mapping and locate the `dense_vector` field under `mappings.properties`:

```console
GET my-index/_mapping
```

Confirm the following:

- `type` is `dense_vector`.
- `index` is `true`. A kNN search can't run on a field with `index: false`.
- `dims` matches the number of dimensions in the query vectors.

:::{dropdown} Example response
:open:
```console-result
{
  "my-index": {
    "mappings": {
      "properties": {
        "embedding": {
          "type": "dense_vector", <1>
          "dims": 3, <2>
          "index": true, <3>
          "similarity": "cosine",
          "index_options": {
            "type": "bbq_disk",
            "cluster_size": 384,
            "flat_index_threshold": -1,
            "default_visit_percentage": 0,
            "rescore_vector": {
              "oversample": 3
            },
            "bits": 4
          }
        },
        "title": {
          "type": "keyword"
        }
      }
    }
  }
}
```

1. Confirms that the field stores dense vectors.
2. The number of dimensions in each stored vector. Query vectors must have the same number of dimensions.
3. Confirms that the field is indexed and supports kNN search.
:::
::::
::::{tab-item} `semantic_text`
Retrieve the index mapping and locate the `semantic_text` field under `mappings.properties`:

```console
GET my-index/_mapping
```

Confirm the following:

- `type` is `semantic_text`.
- `model_settings.task_type` isn't `sparse_embedding`, which isn't compatible with kNN search.

:::{dropdown} Example response
:open:
```console-result
{
  "my-index": {
    "mappings": {
      "properties": {
        "content": {
          "type": "semantic_text", <1>
          "inference_id": ".jina-embeddings-v5-text-small",
          "model_settings": {
            "service": "elastic",
            "task_type": "text_embedding", <2>
            "dimensions": 1024,
            "similarity": "cosine",
            "element_type": "float"
          }
        }
      }
    }
  }
}
```

1. Confirms that the field is a `semantic_text` field.
2. Confirms that the field uses a dense text embedding model that supports kNN search.
:::
::::
:::::

### Check that indexing and search use the same model [verify-embeddings-endpoint]

Before you search, confirm which model generated the indexed vectors. The query vectors must come from the same model because vectors from different models aren't comparable, even when they have the same number of dimensions.

Use the example for your field type:

:::::::{tab-set}
::::::{tab-item} `dense_vector`
A `dense_vector` field doesn't record which model generated its vectors. If an {{infer}} processor generated the document embeddings, retrieve the ingest pipeline that processed the document:

```console
GET _ingest/pipeline/my-pipeline
```

:::{dropdown} Example response
:open:
```console-result
{
  "my-pipeline": {
    "created_date_millis": 1793790532176,
    "processors": [
      {
        "inference": {
          "input_output": {
            "input_field": "content",
            "output_field": "embedding"
          },
          "model_id": ".jina-embeddings-v5-text-small" <1>
        }
      }
    ],
    "modified_date_millis": 1793790532176
  }
}
```

1. The {{infer}} endpoint that generated the document embeddings.
:::

Check that the {{infer}} endpoint is still available. Use the `model_id` from the pipeline, for example:

```console
GET _inference/.jina-embeddings-v5-text-small
```

If `model_id` refers to a trained model instead of an {{infer}} endpoint, check the model deployment:

```console
GET _ml/trained_models/my-model/_stats
```

Use the same model to generate the query vector.

If you generated the vectors outside {{es}}, check the configuration of the application that generated them. {{es}} can't determine the model from the stored vectors.
::::::

::::::{tab-item} `semantic_text`
Select your deployment type or the {{stack}} version in which the index was created:

:::::{applies-switch}
::::{applies-item} { stack: ga 9.2+, serverless: ga }
Retrieve a document and include its stored embeddings. Replace `my-index` with your index name and `1` with the document ID:

```console
POST my-index/_search
{
  "_source": {
    "exclude_vectors": false
  },
  "query": {
    "ids": {
      "values": ["1"]
    }
  }
}
```

:::{dropdown} Example response
:open:
```console-result
{
  "took": 35,
  "timed_out": false,
  "_shards": {
    "total": 6,
    "successful": 6,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "my-index",
        "_id": "1",
        "_score": 1,
        "_source": {
          "content": "Paris is the capital of France.",
          "_inference_fields": {
            "content": {
              "inference": {
                "inference_id": ".jina-embeddings-v5-text-small", <1>
                "model_settings": {
                  "service": "elastic",
                  "task_type": "text_embedding",
                  "dimensions": 1024,
                  "similarity": "cosine",
                  "element_type": "float"
                },
                "chunks": {
                  "content": [
                    {
                      "start_offset": 0,
                      "end_offset": 31,
                      "embeddings": [
                        -0.026611328,
                        0.045166016,
                        -0.006439209,
                        ...
                        -0.036621094
                      ]
                    }
                  ]
                }
              }
            }
          }
        }
      }
    ]
  }
}
```

1. The {{infer}} endpoint that generated the stored embedding.
:::

Check that the {{infer}} endpoint is still available. Use the `inference_id` from the document, for example:

```console
GET _inference/.jina-embeddings-v5-text-small
```

Use the same model to generate the query vector.
::::

::::{applies-item} stack: ga 9.0-9.1
Request the internal inference fields for a document. Replace `my-index` with your index name and `1` with the document ID:

```console
POST my-index/_search
{
  "query": {
    "ids": {
      "values": ["1"]
    }
  },
  "fields": ["_inference_fields"]
}
```

:::{dropdown} Example response
:open:
```console-result
{
  "took": 3,
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
    "max_score": 1,
    "hits": [
      {
        "_index": "my-index",
        "_id": "1",
        "_score": 1,
        "_source": {
          "content": "Paris is the capital of France.",
          "_inference_fields": {
            "content": {
              "inference": {
                "inference_id": ".multilingual-e5-small-elasticsearch", <1>
                "model_settings": {
                  "service": "elasticsearch",
                  "task_type": "text_embedding",
                  "dimensions": 384,
                  "similarity": "cosine",
                  "element_type": "float"
                },
                "chunks": {
                  "content": [
                    {
                      "start_offset": 0,
                      "end_offset": 31,
                      "embeddings": [
                        0.007674215,
                        -0.0059343106,
                        0.023091488,
                        ...
                        0.07972942
                      ]
                    }
                  ]
                }
              }
            }
          }
        }
      }
    ]
  }
}
```

1. The {{infer}} endpoint that generated the stored embedding.
:::

Check that the {{infer}} endpoint is still available. Use the `inference_id` from the document, for example:

```console
GET _inference/.multilingual-e5-small-elasticsearch
```

Use the same model to generate the query vector.
::::
:::::
::::::
:::::::

### Check that search returns the expected document [verify-embeddings-query]

Search with text that you know is in the index, and confirm that the document containing that text comes back first.

Use the example for your field type:

:::::{tab-set}
::::{tab-item} `dense_vector`
```console
POST my-index/_search
{
  "knn": {
    "field": "embedding",
    "k": 5,
    "num_candidates": 50,
    "query_vector_builder": {
      "text_embedding": {
        "model_id": ".jina-embeddings-v5-text-small",
        "model_text": "Paris is the capital of France." <1>
      }
    }
  }
}
```

1. Text that you know appears verbatim in a document you indexed.

:::{dropdown} Example response
:open:
```console-result
{
  "took": 292,
  "timed_out": false,
  "_shards": {
    "total": 6,
    "successful": 6,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.89348686,
    "hits": [
      {
        "_index": "my-index",
        "_id": "1",
        "_score": 0.89348686, <1>
        "_source": {
          "content": "Paris is the capital of France." <2>
        }
      }
    ]
  }
}
```

1. The high `_score` indicates a strong match.
2. The expected document is the top result.
:::
::::

::::{tab-item} `semantic_text`
```console
POST my-index/_search
{
  "query": {
    "knn": {
      "field": "content",
      "k": 1,
      "num_candidates": 10,
      "query_vector_builder": {
        "text_embedding": {
          "model_text": "Paris is the capital of France." <1>
        }
      }
    }
  }
}
```

1. Text that you know appears verbatim in a document you indexed.

:::{dropdown} Example response
:open:
```console-result
{
  "took": 113,
  "timed_out": false,
  "_shards": {
    "total": 6,
    "successful": 6,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.8935028,
    "hits": [
      {
        "_index": "my-index",
        "_id": "1",
        "_score": 0.8935028, <1>
        "_source": {
          "content": "Paris is the capital of France." <2>
        }
      }
    ]
  }
}
```

1. The high `_score` indicates a strong match.
2. The expected document is the top result.
:::
::::
:::::

## kNN search methods [knn-methods]

{{es}} provides two ways to perform kNN search. Select a method based on your dataset size, latency requirements, and whether you need exact scoring.

[**Approximate kNN**](knn/approximate-knn.md) is best for most production workloads where low latency and scale matter more than perfect recall. It narrows the search to likely matches instead of scoring every document, reducing latency on large datasets.

[**Exact, brute-force kNN**](knn/exact-knn.md) is best for small datasets, pre-filtered subsets, or when you need precise scoring without approximate indexing. It scores every matching document, which guarantees accurate results but does not scale well for large datasets. You can improve latency by filtering your data to a small subset of documents.

## kNN search examples [knn-search-examples]

Every kNN search needs a query vector. You can provide it directly or have {{es}} generate or retrieve it at search time with `query_vector_builder`. The exact `dense_vector` query and the approximate kNN methods support query vector builders.

For examples that provide a query vector directly, refer to:

- [Approximate kNN search](knn/approximate-knn.md#approximate-knn-example)
- [Exact kNN with the `dense_vector` query](knn/exact-knn.md#exact-knn-dense-vector-query)
- [Exact kNN with a `script_score` query](knn/exact-knn.md#exact-knn-script-score-query)

### Generate or retrieve a query vector at search time [knn-build-query-vector]

The following examples use `query_vector_builder` with the top-level `knn` option. You can use the same builders with the exact `dense_vector` query. For all available builders and their parameters, refer to [Query vector builders](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md#query-vector-builders-overview).

#### Use the `text_embedding` query vector builder [knn-semantic-search]

Use the `text_embedding` query vector builder to generate a query vector from text. Specify the same model that generated the document vectors.

Reference the deployed model or its deployment in the `query_vector_builder` object, and pass the search string as `model_text`:

```console
POST my-index/_search
{
  "knn": {
    "field": "dense-vector-field",
    "k": 10,
    "num_candidates": 100,
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "my-text-embedding-model", <1>
        "model_text": "The opposite of blue" <2>
      }
    }
  }
}
```

1. The ID of the text embedding model that generates the query vector. Use the same model that produced the document embeddings in the target index. You can also provide a `deployment_id` as the `model_id` value.
2. The query string from which the model generates the dense vector representation.

For a walkthrough that covers deploying a model, generating document embeddings, and querying them, refer to this [end-to-end example](../../../explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md).

#### Use the `lookup` query vector builder [knn-lookup-similar-documents]
```{applies_to}
stack: ga 9.4
```

Use the [`lookup` query vector builder](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md#knn-query-builder-lookup) when the vector you want to search with is already stored in a document. This is the pattern behind "more like this" and recommendation features: instead of embedding new input, you take the vector from an item the user is viewing and find its nearest neighbors.

The following request finds the images most similar to document `2`:

```console
POST image-index/_search
{
  "knn": {
    "field": "image-vector",
    "k": 10,
    "query_vector_builder": {
      "lookup": {
        "index": "image-index", <1>
        "id": "2", <2>
        "path": "image-vector" <3>
      }
    }
  }
}
```

1. The index that holds the document to look up. It doesn't have to be the index you're searching.
2. The ID of the document to look up. The request fails with a `404` if the document doesn't exist or has no value for `path`.
3. The vector field to read the query vector from. Its dimensions must match the field you're searching.

{{es}} reads the vector from the indexed field rather than from `_source`, so the lookup works even when vector values are excluded from `_source`.

The looked-up document is its own nearest neighbor, so it comes back as the top hit. Exclude it with a filter when you only want other documents:

```console
POST image-index/_search
{
  "knn": {
    "field": "image-vector",
    "k": 10,
    "query_vector_builder": {
      "lookup": {
        "index": "image-index",
        "id": "2",
        "path": "image-vector"
      }
    },
    "filter": {
      "bool": {
        "must_not": {
          "ids": {
            "values": ["2"]
          }
        }
      }
    }
  }
}
```

### Find more examples by method

For approximate kNN similarity thresholds, hybrid search, multiple vector fields, and aggregations, refer to [Approximate kNN query examples](knn/approximate-knn-query-examples.md). For filtering, refer to [Filter approximate kNN results](knn/filtered-knn-search.md).

For exact kNN filtering and scoring examples, refer to [Exact kNN search](knn/exact-knn.md).

## Next steps

Continue with the guide for the kNN search method that fits your use case:

- [Approximate kNN search](knn/approximate-knn.md): Learn how to map, index, and query `dense_vector` fields for fast, scalable approximate kNN search.
- [Exact kNN search](knn/exact-knn.md): Learn how to run exact brute-force kNN search for small datasets or precise scoring.
