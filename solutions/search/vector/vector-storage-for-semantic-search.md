---
navigation_title: Optimize vector storage for semantic search
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
type: how-to
description: Reduce the memory footprint of dense vector embeddings in semantic search by configuring quantization strategies on semantic_text fields.
---

# Optimize dense vector storage for semantic search [semantic-text-index-options]

When scaling semantic search, the memory footprint of dense vector embeddings is a primary concern. You can reduce storage requirements by configuring a [quantization strategy](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization) on your `semantic_text` fields using the `index_options` parameter.

This guide walks you through choosing a strategy and applying it to a `semantic_text` field mapping. For full details on all available quantization options and their parameters, refer to the [`dense_vector` field type reference](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-index-options).

## Requirements

- You need a `semantic_text` field that uses an {{infer}} endpoint producing **dense vector embeddings** (such as E5, OpenAI embeddings, or Cohere).
- If you use a custom model, create the {{infer}} endpoint first using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put).

::::{note}
These `index_options` do not apply to sparse vector models like ELSER, which use a different internal representation.
::::

:::{tip}
To run the `curl` examples on this page, set the following environment variables:
```bash
export ELASTICSEARCH_URL="your-elasticsearch-url"
export API_KEY="your-api-key"
```
To generate API keys, search for `API keys` in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md). [Learn more about finding your endpoint and credentials](/solutions/elasticsearch-solution-project/search-connection-details.md).
:::

## Choose a quantization strategy

Select a quantization strategy based on your dataset size and performance requirements:

| Strategy | Memory reduction | Best for | Trade-offs |
|----------|-----------------|----------|------------|
| `bbq_hnsw` | Up to 32x | Most production use cases (default for 384+ dimensions) | Minimal accuracy loss |
| `bbq_flat` | Up to 32x | Smaller datasets needing maximum accuracy | Slower queries (brute-force search) |
| `bbq_disk` {applies_to}`stack: ga 9.2` | Up to 32x | Large datasets with constrained RAM | Slower queries (disk-based) |
| `int8_hnsw` | 4x | High accuracy retention | Lower compression than BBQ |
| `int4_hnsw` | 8x | Balance between compression and accuracy | Some accuracy loss |

For most use cases with dense vector embeddings from text models, we recommend [Better Binary Quantization (BBQ)](elasticsearch://reference/elasticsearch/mapping-reference/bbq.md). BBQ requires a minimum of 64 dimensions and works best with text embeddings.

## Configure your index mapping

Create an index with a `semantic_text` field and set the `index_options` to your chosen quantization strategy.

:::::::::{tab-set}

::::::::{tab-item} BBQ with HNSW

```console
PUT semantic-embeddings-optimized
{
  "mappings": {
    "properties": {
      "content": {
        "type": "semantic_text",
        "inference_id": ".multilingual-e5-small-elasticsearch", <1>
        "index_options": {
          "dense_vector": {
            "type": "bbq_hnsw" <2>
          }
        }
      }
    }
  }
}
```

1. Reference to a text embedding {{infer}} endpoint. This example uses the built-in E5 endpoint, which is automatically available. For custom models, you must create the endpoint first using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put).
2. Uses [BBQ](elasticsearch://reference/elasticsearch/mapping-reference/bbq.md) with HNSW indexing for up to 32x memory reduction.

:::{dropdown} Equivalent `curl` command
:open:

```bash
curl -X PUT "${ELASTICSEARCH_URL}/semantic-embeddings-optimized" \
     -H "Content-Type: application/json" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -d '{
       "mappings": {
         "properties": {
           "content": {
             "type": "semantic_text",
             "inference_id": ".multilingual-e5-small-elasticsearch",
             "index_options": {
               "dense_vector": {
                 "type": "bbq_hnsw"
               }
             }
           }
         }
       }
     }'
```

:::

::::::::

::::::::{tab-item} BBQ flat

Use `bbq_flat` for smaller datasets where you need maximum accuracy at the expense of speed:

```console
PUT semantic-embeddings-flat
{
  "mappings": {
    "properties": {
      "content": {
        "type": "semantic_text",
        "inference_id": ".multilingual-e5-small-elasticsearch", <1>
        "index_options": {
          "dense_vector": {
            "type": "bbq_flat" <2>
          }
        }
      }
    }
  }
}
```
1. Reference to a text embedding {{infer}} endpoint. This example uses the built-in E5 endpoint, which is automatically available. For custom models, you must create the endpoint first using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put).
2. BBQ without HNSW for smaller datasets. Uses brute-force search, so queries are slower but indexing is lighter.

:::{dropdown} Equivalent `curl` command
:open:

```bash
curl -X PUT "${ELASTICSEARCH_URL}/semantic-embeddings-flat" \
     -H "Content-Type: application/json" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -d '{
       "mappings": {
         "properties": {
           "content": {
             "type": "semantic_text",
             "inference_id": ".multilingual-e5-small-elasticsearch",
             "index_options": {
               "dense_vector": {
                 "type": "bbq_flat"
               }
             }
           }
         }
       }
     }'
```

:::



::::::::

::::::::{tab-item} DiskBBQ

```{applies_to}
stack: ga 9.2
serverless: unavailable
```

For large datasets where RAM is constrained, use `bbq_disk` (DiskBBQ) to minimize memory usage:

```console
PUT semantic-embeddings-disk
{
  "mappings": {
    "properties": {
      "content": {
        "type": "semantic_text",
        "inference_id": ".multilingual-e5-small-elasticsearch", <1>
        "index_options": {
          "dense_vector": {
            "type": "bbq_disk" <2>
          }
        }
      }
    }
  }
}
```
1. Reference to a text embedding {{infer}} endpoint. This example uses the built-in E5 endpoint, which is automatically available. For custom models, you must create the endpoint first using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put).
2. DiskBBQ keeps vectors compressed on disk, dramatically reducing RAM requirements at the cost of slower queries.

:::{dropdown} Equivalent `curl` command
:open:

```bash
curl -X PUT "${ELASTICSEARCH_URL}/semantic-embeddings-disk" \
     -H "Content-Type: application/json" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -d '{
       "mappings": {
         "properties": {
           "content": {
             "type": "semantic_text",
             "inference_id": ".multilingual-e5-small-elasticsearch",
             "index_options": {
               "dense_vector": {
                 "type": "bbq_disk"
               }
             }
           }
         }
       }
     }'
```

:::

::::::::

::::::::{tab-item} Integer quantization

```console
PUT semantic-embeddings-int8
{
  "mappings": {
    "properties": {
      "content": {
        "type": "semantic_text",
        "inference_id": ".multilingual-e5-small-elasticsearch", <1>
        "index_options": {
          "dense_vector": {
            "type": "int8_hnsw" <2>
          }
        }
      }
    }
  }
}
```
1. Reference to a text embedding {{infer}} endpoint. This example uses the built-in E5 endpoint, which is automatically available. For custom models, you must create the endpoint first using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put).
2. 8-bit integer quantization for ~4x memory reduction. For higher compression, use `"type": "int4_hnsw"` (~8x reduction).

:::{dropdown} Equivalent `curl` command
:open:

```bash
curl -X PUT "${ELASTICSEARCH_URL}/semantic-embeddings-int8" \
     -H "Content-Type: application/json" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -d '{
       "mappings": {
         "properties": {
           "content": {
             "type": "semantic_text",
             "inference_id": ".multilingual-e5-small-elasticsearch",
             "index_options": {
               "dense_vector": {
                 "type": "int8_hnsw"
               }
             }
           }
         }
       }
     }'
```

:::

::::::::

:::::::::


:::{dropdown} Example response

```js
{
  "acknowledged": true, <1>
  "shards_acknowledged": true,
  "index": "semantic-embeddings-optimized"
}
```

1. `true` confirms the index was created successfully with your mapping configuration.

:::

## Verify your configuration

Confirm that the `index_options` are applied to your index:

::::{tab-set}

:::{tab-item} Console

```console
GET semantic-embeddings-optimized/_mapping
```

:::

:::{tab-item} curl

```bash
curl -X GET "${ELASTICSEARCH_URL}/semantic-embeddings-optimized/_mapping" \
     -H "Authorization: ApiKey ${API_KEY}"
```

:::

::::

The response includes the `index_options` you configured under the `content` field's mapping. If the `index_options` block is missing, check that you specified it correctly in the `PUT` request.

:::{dropdown} Example response

```js
{
  "semantic-embeddings-optimized": {
    "mappings": {
      "properties": {
        "content": {
          "type": "semantic_text",
          "inference_id": ".multilingual-e5-small-elasticsearch",
          "index_options": { <1>
            "dense_vector": {
              "type": "bbq_hnsw"
            }
          }
        }
      }
    }
  }
}
```

1. The `index_options` block confirms your quantization strategy is applied. After indexing data, the mapping may also include auto-detected `model_settings` such as dimensions and similarity metric.

:::

## (Optional) Tune HNSW parameters

For HNSW-based strategies, you can tune graph parameters like `m` and `ef_construction` in the `index_options`. Refer to the [`dense_vector` field type reference](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-index-options) for the full list of tunable parameters.

::::{tab-set}

:::{tab-item} Console

```console
PUT semantic-embeddings-custom
{
  "mappings": {
    "properties": {
      "content": {
        "type": "semantic_text",
        "inference_id": ".multilingual-e5-small-elasticsearch",
        "index_options": {
          "dense_vector": {
            "type": "bbq_hnsw",
            "m": 32, <1>
            "ef_construction": 200 <2>
          }
        }
      }
    }
  }
}
```

1. Controls graph connectivity. Higher values improve recall at the cost of memory. Default: `16`.
2. Controls index build quality. Higher values improve quality but slow indexing. Default: `100`.

:::

:::{tab-item} curl

```bash
curl -X PUT "${ELASTICSEARCH_URL}/semantic-embeddings-custom" \
     -H "Content-Type: application/json" \
     -H "Authorization: ApiKey ${API_KEY}" \
     -d '{
       "mappings": {
         "properties": {
           "content": {
             "type": "semantic_text",
             "inference_id": ".multilingual-e5-small-elasticsearch",
             "index_options": {
               "dense_vector": {
                 "type": "bbq_hnsw",
                 "m": 32,
                 "ef_construction": 200
               }
             }
           }
         }
       }
     }'
```

:::

::::

## Next steps

- Follow the [Semantic search with `semantic_text`](../semantic-search/semantic-search-semantic-text.md) tutorial to set up an end-to-end semantic search workflow.
- Combine semantic search with keyword search using [hybrid search](../hybrid-semantic-text.md).

## Related pages

- [`dense_vector` `index_options` reference](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-index-options)
- [Better Binary Quantization (BBQ)](elasticsearch://reference/elasticsearch/mapping-reference/bbq.md)
- [Dense vector search](dense-vector.md)
- [Trained model autoscaling](../../../deploy-manage/autoscaling/trained-model-autoscaling.md)
