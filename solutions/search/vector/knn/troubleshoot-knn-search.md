---
navigation_title: Troubleshoot kNN search results
description: Resolve kNN searches that fail, return no results, or do not return the expected document in Elasticsearch.
type: troubleshooting
products:
  - id: elasticsearch
applies_to:
  stack:
  serverless:
---

# Resolve missing or unexpected kNN search results

This page provides a checklist for diagnosing kNN searches that fail, return no results, or do not return the document you expect. The checks cover stored embeddings, field mappings, model compatibility, and a test query to help you identify the cause of the issue.

## Symptoms

- A kNN search fails.
- A kNN search returns no results.
- A kNN search does not return the expected document.

## Resolution

{{es}} can return a successful indexing response even when documents have no vector that a kNN search can use. This can happen when the ingest pipeline that contains the {{infer}} processor isn't applied to the indexing request, or when the {{infer}} processor is configured to ignore processor failures or missing input fields.

Use this checklist to diagnose the problem:

- [Check that the document has embeddings](#verify-embeddings-stored).
- [Check that the field mapping supports kNN search](#verify-embeddings-mapping).
- [Check that indexing and search use the same model](#verify-embeddings-endpoint).
- [Check that search returns the expected document](#verify-embeddings-query).

## Check that the document has embeddings [verify-embeddings-stored]

Confirm that the document contains embeddings in the expected field.

Use the example for your field type. For a `semantic_text` field, select your deployment type or the {{stack}} version in which the index was created. Upgrading {{stack}} doesn't change this behavior for existing indices.

:::::::{tab-set}
::::::{tab-item} `dense_vector`
Retrieve the document by ID and include only the `embedding` field. Replace `my-index` and `1` with the values for your document:

```console
GET my-index/_doc/1?_source_includes=embedding
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
    "embedding": [ <1>
      -0.026611328,
      0.045166016,
      -0.006439209,
      ...
      -0.036621094
    ]
  }
}
```

1. The stored 1024-dimension vector. The example omits most values.
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

## Check that the field mapping supports kNN search [verify-embeddings-mapping]

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
          "dims": 1024, <2>
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
        "content": {
          "type": "text"
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

## Check that indexing and search use the same model [verify-embeddings-endpoint]

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

## Check that search returns the expected document [verify-embeddings-query]

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
