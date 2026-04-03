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

# Optimize vector storage for semantic search [semantic-text-index-options]

When scaling semantic search, the memory footprint of dense vector embeddings can become a primary concern. You can optimize storage and search performance for your `semantic_text` indexes by configuring the `index_options` parameter on the underlying `dense_vector` field. The `index_options` parameter controls how vectors are indexed and stored. You can specify [quantization strategies](https://www.elastic.co/blog/vector-search-elasticsearch-rationale) like [Better Binary Quantization (BBQ)](elasticsearch://reference/elasticsearch/mapping-reference/bbq.md) that compress high-dimensional vectors into more efficient representations, achieving up to 32x memory reduction while maintaining search quality.

## Before you begin

- You need a `semantic_text` field that uses an {{infer}} endpoint producing **dense vector embeddings** (such as E5, OpenAI embeddings, or Cohere).
- If you use a custom model, create the {{infer}} endpoint first using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put).

::::{note}
These `index_options` do not apply to sparse vector models like ELSER, which use a different internal representation. For details on all available options and their trade-offs, refer to the [`dense_vector` `index_options` documentation](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-index-options).
::::

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
2. Better Binary Quantization with HNSW indexing for optimal memory efficiency. This setting applies to the underlying `dense_vector` field that stores the embeddings.

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
        "inference_id": ".multilingual-e5-small-elasticsearch",
        "index_options": {
          "dense_vector": {
            "type": "bbq_flat" <1>
          }
        }
      }
    }
  }
}
```

1. BBQ without HNSW for smaller datasets. Uses brute-force search, which requires fewer resources during indexing but more during querying.

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
        "inference_id": ".multilingual-e5-small-elasticsearch",
        "index_options": {
          "dense_vector": {
            "type": "bbq_disk" <1>
          }
        }
      }
    }
  }
}
```

1. Use DiskBBQ when RAM is limited. This option keeps vectors in compressed form on disk and only loads/decompresses small portions on-demand during queries. Unlike standard HNSW indexes (which rely on filesystem cache to load vectors into memory for fast search), DiskBBQ dramatically reduces RAM requirements by avoiding the need to cache vectors in memory. This enables vector search on much larger datasets with minimal memory, though queries are slower compared to in-memory approaches.

::::::::

::::::::{tab-item} Integer quantization

```console
PUT semantic-embeddings-int8
{
  "mappings": {
    "properties": {
      "content": {
        "type": "semantic_text",
        "inference_id": ".multilingual-e5-small-elasticsearch",
        "index_options": {
          "dense_vector": {
            "type": "int8_hnsw" <1>
          }
        }
      }
    }
  }
}
```

1. 8-bit integer quantization for 4x memory reduction with high accuracy retention. For 4-bit quantization, use `"type": "int4_hnsw"` instead (up to 8x memory reduction). For the full list of other available quantization options (including `int4_flat` and others), refer to the [`dense_vector` `index_options` documentation](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-index-options).

::::::::

:::::::::

## Verify your configuration

Confirm that the `index_options` are applied to your index:

```console
GET semantic-embeddings-optimized/_mapping
```

The response includes the `index_options` you configured under the `content` field's mapping. If the `index_options` block is missing, check that you specified it correctly in the `PUT` request.

## (Optional) Tune HNSW parameters

For HNSW-specific tuning parameters like `m` and `ef_construction`, you can include them in the `index_options`:

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

1. Number of neighbors each node connects to in the HNSW graph. Higher values improve recall but increase memory usage. Default: `16`.
2. Number of candidates considered during graph construction. Higher values improve index quality but slow down indexing. Default: `100`.

## Next steps

- Follow the [Semantic search with `semantic_text`](semantic-search-semantic-text.md) tutorial to set up an end-to-end semantic search workflow.
- Combine semantic search with keyword search using [hybrid search](../hybrid-semantic-text.md).

## Related pages

- [`dense_vector` `index_options` reference](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-index-options)
- [Better Binary Quantization (BBQ)](elasticsearch://reference/elasticsearch/mapping-reference/bbq.md)
- [Dense vector search](../vector/dense-vector.md)
- [Trained model autoscaling](../../../deploy-manage/autoscaling/trained-model-autoscaling.md)
