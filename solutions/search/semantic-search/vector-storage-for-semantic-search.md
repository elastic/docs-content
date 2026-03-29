---
navigation_title: Optimize vector storage for semantic search
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
---

# Optimize vector storage for semantic search [semantic-text-index-options]

When scaling semantic search in Elasticsearch, the memory footprint of dense vector embeddings can become a primary concern. 

When using `semantic_text` with {{infer}} endpoints that produce dense vector embeddings (such as E5, OpenAI embeddings, or Cohere), you can optimize storage and search performance by configuring `index_options` on the underlying `dense_vector` field. 

The `index_options` parameter controls how vectors are indexed and stored. You can specify [quantization strategies](https://www.elastic.co/blog/vector-search-elasticsearch-rationale) like [Better Binary Quantization (BBQ)](elasticsearch://reference/elasticsearch/mapping-reference/bbq.md) that compress high-dimensional vectors into more efficient representations. This significantly reduces memory footprint while maintaining search quality.

::::{note}
The `index_options` parameter does not apply to sparse vector models like ELSER, which use a different internal representation. For details on all available options and their trade-offs, refer to the [`dense_vector` `index_options` documentation](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-index-options).
::::

## Choose a quantization strategy

For most production use cases using `semantic_text` with dense vector embeddings from text models, BBQ is recommended. It provides up to 32x memory reduction with minimal accuracy loss. BBQ requires a minimum of 64 dimensions and works best with text embeddings. 

Choose from:
- `bbq_hnsw` - Best for most use cases (default for 384+ dimensions)
- `bbq_flat` - BBQ without HNSW for smaller datasets
- `bbq_disk` - Disk-based storage for large datasets with minimal memory requirements {applies_to}`stack: ga 9.2`

## Use BBQ with HNSW

Here's an example using `semantic_text` with a text embedding {{infer}} endpoint and BBQ quantization:

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

1. Reference to a text embedding {{infer}} endpoint. This example uses the built-in E5 endpoint that is automatically available. For custom models, you must create the endpoint first using the [Create {{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put).
2. Use Better Binary Quantization with HNSW indexing for optimal memory efficiency. This setting applies to the underlying `dense_vector` field that stores the embeddings.

## Use BBQ without HNSW

You can also use `bbq_flat` for smaller datasets where you need maximum accuracy at the expense of speed:

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

1. Use BBQ without HNSW for smaller datasets. This uses brute-force search and requires less compute resources during indexing but more during querying.

## Use DiskBBQ for large datasets

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

1. Use DiskBBQ when RAM is limited. Available in {{es}} 9.2+, this option keeps vectors in compressed form on disk and only loads/decompresses small portions on-demand during queries. Unlike standard HNSW indexes (which rely on filesystem cache to load vectors into memory for fast search), DiskBBQ dramatically reduces RAM requirements by avoiding the need to cache vectors in memory. This enables vector search on much larger datasets with minimal memory, though queries will be slower compared to in-memory approaches.

## Use integer quantization

Other quantization options include `int8_hnsw` (8-bit integer quantization) and `int4_hnsw` (4-bit integer quantization):

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

1. Use 8-bit integer quantization for 4x memory reduction with high accuracy retention. For 4-bit quantization, use `"type": "int4_hnsw"` instead, which provides up to 8x memory reduction. For the full list of other available quantization options (including `int4_flat` and others), refer to the [`dense_vector` `index_options` documentation](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-index-options).

## Tune HNSW parameters

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

1. The number of neighbors each node will be connected to in the HNSW graph. Higher values improve recall but increase memory usage. Default is 16.
2. Number of candidates considered during graph construction. Higher values improve index quality but slow down indexing. Default is 100.