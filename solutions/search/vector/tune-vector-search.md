---
navigation_title: Tune performance
description: Control quantization, index type, num_candidates, and rescoring to balance recall accuracy, query latency, and memory footprint for dense vector search in Elasticsearch.
applies_to:
  stack: ga
  serverless:
    elasticsearch: ga
---

# Tune vector search performance and relevance

This page describes how to tune a dense vector index once you have decided to use vector search. For guidance on choosing between retrieval approaches, refer to [Choose a retrieval strategy](/solutions/search/choose-retrieval-strategy.md). For guidance on which implementation path to use, refer to [Choose a semantic search implementation](/solutions/search/semantic-search/choose-semantic-implementation.md).

The main tuning levers are:

- **Quantization and index type**: controls memory footprint and index-time cost
- **Rescoring**: recovers accuracy lost through quantization
- **`num_candidates`**: controls the recall/latency tradeoff at query time
- **Similarity function**: must match the function used to train your embedding model

## Quantization and index type [quantization]

When you define a `dense_vector` field with indexing enabled, Elasticsearch automatically selects a quantization strategy based on vector dimensions. You can override this by setting `index_options.type` on the field mapping.

The available index types are:

| Index type | Compression | Memory reduction | Accuracy impact | Default for |
|---|---|---|---|---|
| `int8_hnsw` | 4× (float → int8) | ~75% | Low | Vectors < 384 dims |
| `int4_hnsw` | 8× (float → int4) | ~87.5% | Moderate | — |
| `bbq_hnsw` | ~32× (binary) | ~97% | Higher; rescoring recommended | Vectors ≥ 384 dims |
| `bbq_disk` | ~32× (disk-based binary) | Minimizes RAM use | Higher; rescoring required | Very large corpora |
| `hnsw` | None (float32) | — | None | Not recommended at scale |

All quantization strategies retain the original float vectors on disk for use during rescoring. Disk usage increases slightly as a result.

### When to override the default [override-default]

The automatic default (`int8_hnsw` for vectors under 384 dimensions, `bbq_hnsw` for 384 and above) is suitable for most use cases. Override the default when:

- You need maximum recall accuracy and can afford the memory cost: use `hnsw` (no quantization)
- You need to minimize memory at the cost of accuracy: use `int4_hnsw` or `bbq_hnsw` with rescoring
- Your corpus is very large (hundreds of millions of vectors) and RAM is the primary constraint: use `bbq_disk`

:::{important}
`bbq_disk` (DiskBBQ) stores the vector index on disk rather than in RAM. Search latency is highly sensitive to the amount of off-heap RAM available for the OS page cache. If the vector data does not fit in the page cache, query latency can degrade significantly. Size your heap and off-heap RAM accordingly before using `bbq_disk` in production.
:::

### Setting the index type [set-index-type]

Set `index_options.type` on the `dense_vector` field at index creation time:

```json
PUT my-vector-index
{
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "dense_vector",
        "dims": 768,
        "index": true,
        "similarity": "cosine",
        "index_options": {
          "type": "bbq_hnsw"
        }
      }
    }
  }
}
```

Index type cannot be changed after indexing. To change quantization, create a new index and reindex.

For full `dense_vector` field mapping options, refer to the Elasticsearch reference documentation.

## Rescoring quantized vectors [rescoring]

Quantization reduces accuracy because approximate retrieval uses compressed vectors. You can recover most of this accuracy by rescoring: retrieving a larger candidate set using the quantized index, then re-ranking those candidates using the original float vectors.

Use `rescore_vector.oversample` in the `knn` retriever to enable this:

```json
GET my-vector-index/_search
{
  "retriever": {
    "knn": {
      "field": "my_vector",
      "query_vector": [...],
      "k": 10,
      "num_candidates": 100,
      "rescore_vector": {
        "oversample": 2.0
      }
    }
  }
}
```

With `oversample: 2.0` and `k: 10`, Elasticsearch retrieves 20 candidates per shard using the quantized index, then rescores them with the original float vectors and returns the top 10.

**Recommended oversample values by index type:**

- `int8_hnsw`: rescoring is optional; the accuracy loss is low without it
- `int4_hnsw`: use 1.5×–2× oversample to recover most accuracy loss
- `bbq_hnsw` / `bbq_disk`: use 3×–5× oversample; higher may be needed for low-dimension vectors or models that quantize poorly

Rescoring increases latency proportionally to the oversample factor. Set the oversample value based on measured recall on a representative query set, not on defaults alone.

For detailed behavior, refer to [kNN search in Elasticsearch](/solutions/search/vector/knn.md).

## `num_candidates` [num-candidates]

`num_candidates` controls how many candidate vectors are considered per shard during approximate kNN search. A higher value improves recall at the cost of higher query latency. When not set explicitly, Elasticsearch uses an internal default. Set it explicitly when:

- You are seeing recall gaps and want to improve result quality without rescoring
- You are tuning the latency/recall tradeoff for a specific workload

There is no single correct value. Test `num_candidates` against a labeled evaluation set for your index and query distribution.

## Approximate vs exact kNN [approx-vs-exact]

Elasticsearch supports two kNN search modes:

**Approximate kNN** uses the HNSW index for fast similarity search. It is the correct choice for any production workload. Use this when your index has indexed vectors (`"index": true` on the field mapping).

**Exact kNN** uses a `script_score` query to compute similarity against every matching document. It guarantees finding the true k nearest neighbors but does not scale beyond small corpora. Use exact kNN only for prototyping, very small datasets, or when you need to filter heavily before scoring.

## Similarity function [similarity]

The `similarity` parameter on a `dense_vector` field defines how the query vector is compared to document vectors. The available options are `cosine` (default), `dot_product`, and `l2_norm`.

The similarity function must match the function the embedding model was trained or normalized for:

- Use `dot_product` when your model outputs unit-normalized vectors (many dense retrieval models do). It is faster than `cosine` and produces equivalent results for normalized vectors.
- Use `cosine` when vectors are not normalized, or when you are unsure. It is the safe default.
- Use `l2_norm` (Euclidean distance) when your model explicitly targets L2 similarity — this is uncommon for text embedding models.

The similarity function cannot be changed after indexing. If you change your embedding model to one that uses a different normalization or similarity function, create a new index.

## Next steps [next-steps]

- [kNN search in Elasticsearch](/solutions/search/vector/knn.md)
- [Choose a hybrid and reranking strategy](/solutions/search/vector/choose-hybrid-reranking-strategy.md)
