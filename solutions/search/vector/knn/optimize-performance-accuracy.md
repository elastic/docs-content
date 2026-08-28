---
navigation_title: Optimize performance and accuracy
description: Tune approximate kNN search in Elasticsearch for speed, recall, vector storage, quantization, and rescoring trade-offs.
applies_to:
  stack:
  serverless:
---

# Optimize approximate kNN search performance and accuracy [optimize-knn-performance-accuracy]

After you have approximate kNN search working, use this page to balance latency, recall, and storage. You can change how much of the index each query explores, how vectors are stored, and whether results are rescored with the original vectors.

This page covers those query-time and encoding trade-offs. For mapping, indexing, and a basic search example, refer to [Approximate kNN search](approximate-knn.md). For cluster sizing, memory, segment merging, and filesystem cache guidance, refer to [Tune approximate kNN search](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md).

| If you want to... | Start here |
|---|---|
| Search faster, or improve recall, without reindexing | [Tune search-time speed versus accuracy](#tune-approximate-knn-for-speed-accuracy) |
| Use less memory or disk | [Reduce vector storage](#reduce-knn-vector-storage) |
| Recover recall after quantization | [Oversampling and rescoring for quantized vectors](#dense-vector-knn-search-rescoring) |

## Tune search-time speed versus accuracy [tune-approximate-knn-for-speed-accuracy]

Approximate kNN does not score every vector. Each query explores a candidate set, keeps the best `k` hits on the shard, then merges shard results into the global top `k`. How you size that candidate set is the main search-time trade-off between latency and recall.

Which parameter you set depends on the index type:

* For HNSW indices, set `num_candidates`.
* For DiskBBQ (`bbq_disk`) indices, set `visit_percentage`.

If the field is [quantized](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization), you can also recover recall after retrieval with `rescore_vector`. Refer to [Oversampling and rescoring for quantized vectors](#dense-vector-knn-search-rescoring).

### HNSW: `num_candidates` [tune-knn-num-candidates]

For each segment, {{es}} explores a `num_candidates` set of approximate neighbors. It then keeps the top `k` on the shard and merges those shard results into the global top `k`.

`num_candidates` must be greater than or equal to `k` and cannot exceed `10,000`. If you omit it, it defaults to `1.5 * k` when `k` is set, or `1.5 * size` when `k` is omitted, capped at `10,000`.

* Increase `num_candidates` to improve recall, at the cost of higher latency.
* Decrease `num_candidates` for faster queries, with a potential recall trade-off.

Because {{es}} searches each segment's HNSW graph separately, more segments means more candidate exploration. For guidance on reducing segment count, refer to [Tune approximate kNN search](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md).

```console
POST image-index/_search
{
  "knn": {
    "field": "image-vector",
    "query_vector": [-5, 9, -12],
    "k": 10, <1>
    "num_candidates": 100 <2>
  }
}
```

1. The number of nearest neighbors to return.
2. The candidate set explored per segment. Larger values improve recall and increase latency.

### DiskBBQ: `visit_percentage` [tune-knn-visit-percentage]
```{applies_to}
stack: ga 9.2+
serverless: ga
```

For DiskBBQ (`bbq_disk`) indices, `visit_percentage` controls the percentage of vectors explored during search. It accepts values from `0` to `100`, including decimals such as `0.5` (half a percent). On {{stack}}, `bbq_disk` requires an [Enterprise subscription](https://www.elastic.co/subscriptions).

* If you omit `visit_percentage`, or set it to `0`, {{es}} picks the visit budget from `num_candidates` and segment size.
* If you set a non-zero `visit_percentage`, DiskBBQ uses that value to size the visit budget and does not use `num_candidates` for that budget.
* Increase `visit_percentage` to improve recall, at the cost of higher latency.
* Decrease `visit_percentage` for faster queries, with a potential recall trade-off.

Create a `bbq_disk` index, then set `visit_percentage` at search time:

```console
PUT diskbbq-image-index
{
  "mappings": {
    "properties": {
      "image-vector": {
        "type": "dense_vector",
        "dims": 3,
        "index_options": {
          "type": "bbq_disk"
        }
      }
    }
  }
}
```

```console
POST diskbbq-image-index/_search
{
  "knn": {
    "field": "image-vector",
    "query_vector": [-5, 9, -12],
    "k": 10, <1>
    "visit_percentage": 3 <2>
  }
}
```

1. The number of nearest neighbors to return.
2. The percentage of vectors to explore. `3` visits 3% of the vectors. Larger values improve recall and increase latency.

When a search targets both HNSW and DiskBBQ indices, set both `num_candidates` and `visit_percentage`. HNSW uses `num_candidates`. DiskBBQ uses `visit_percentage` when that value is non-zero.

## Reduce vector storage [reduce-knn-vector-storage]

How you encode vectors is the main mapping-time trade-off between memory, disk, and recall. Start from how your embeddings are produced:

| If your embeddings are... | Use | Effect |
|---|---|---|
| `float` (the usual case) | [Quantization](#knn-search-quantized-example) | Much less RAM for search. Disk use increases because original vectors stay on disk. Some recall loss, which you can recover by [rescoring](#dense-vector-knn-search-rescoring). |
| Already 8-bit integers | [`element_type: byte`](#approximate-knn-using-byte-vectors) | Smaller memory footprint than `float`, without a separate quantization step. Query vectors must also be bytes. |
| Already bfloat16, or you need cheaper raw-vector storage {applies_to}`{ stack: ga 9.3+, serverless: ga }` | [`element_type: bfloat16`](#knn-search-bfloat16) | Halves raw vector storage compared with `float`. {{es}} can still quantize these fields. |

Do not convert `float` embeddings to `byte` yourself to save memory. Use quantization instead.

### Quantized float vectors [knn-search-quantized-example]

To index `float` or `bfloat16` vectors with a smaller memory footprint, use [quantization](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization). {{es}} stores a quantized representation for approximate retrieval and keeps the original vectors on disk for rescoring, reindexing, and later quantization improvements. That extra copy means disk use goes up even as RAM for search goes down.

Unless you set `index_options.type`, {{es}} quantizes `float` and `bfloat16` fields automatically:

::::{applies-switch}

:::{applies-item} stack: ga 9.0
`int8_hnsw`
:::

:::{applies-item} stack: ga 9.1-9.3
`bbq_hnsw` for 384 or more dimensions, otherwise `int8_hnsw`
:::

:::{applies-item} { "stack": "ga 9.4+", "serverless": "ga" }
`bbq_disk` when available under the current license. On {{stack}}, this requires an [Enterprise subscription](https://www.elastic.co/subscriptions). For fewer than 384 dimensions, that default uses 4-bit quantization (`bits: 4`).
:::

::::

`byte` and `bit` fields are not quantized. They default to `hnsw`.

Higher compression uses less RAM and usually costs more recall:

| Type | RAM versus unquantized `float` | Recall |
|---|---|---|
| `int8_hnsw` | About 4x less | Smallest extra loss. Often needs little or no rescoring. |
| `int4_hnsw` | About 8x less | Larger loss. Often benefits from rescoring. |
| BBQ (`bbq_hnsw`, `bbq_disk` {applies_to}`{ stack: ga 9.2+, serverless: ga }`) | About 32x less | Larger loss. BBQ defaults to 3x oversampling to recover recall. |

`bbq_disk` is the BBQ variant that can run with less of the index in RAM. For RAM formulas and node sizing, refer to [Tune approximate kNN search](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md). For the full parameter list, refer to [`index_options`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-index-options).

To override the default, set `index_options.type`:

```console
PUT quantized-image-index
{
  "mappings": {
    "properties": {
      "image-vector": {
        "type": "dense_vector",
        "element_type": "float",
        "dims": 2,
        "index_options": {
          "type": "int8_hnsw" <1>
        }
      },
      "title": {
        "type": "text"
      }
    }
  }
}
```

1. Overrides the default quantization.

Index `float` vectors as usual. {{es}} quantizes them for approximate retrieval and keeps the original values on disk:

```console
POST quantized-image-index/_bulk?refresh=true
{ "index": { "_id": "1" } }
{ "image-vector": [0.1, -2], "title": "moose family" }
{ "index": { "_id": "2" } }
{ "image-vector": [0.75, -1], "title": "alpine lake" }
{ "index": { "_id": "3" } }
{ "image-vector": [1.2, 0.1], "title": "full moon" }
```

At search time, {{es}} quantizes the query vector to match the index:

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

To recover recall, rescore the top candidates with the original vectors. Refer to [Oversampling and rescoring for quantized vectors](#dense-vector-knn-search-rescoring).

### Byte vectors [approximate-knn-using-byte-vectors]

Use `element_type: byte` when your embeddings are already 8-bit integers. Indexed values and `query_vector` values must be integers in the range [-128, 127].

```console
PUT byte-image-index
{
  "mappings": {
    "properties": {
      "byte-image-vector": {
        "type": "dense_vector",
        "element_type": "byte", <1>
        "dims": 2
      },
      "title": {
        "type": "text"
      }
    }
  }
}
```

1. Required when your embeddings are already 8-bit integers.

```console
POST byte-image-index/_bulk?refresh=true
{ "index": { "_id": "1" } }
{ "byte-image-vector": [5, -20], "title": "moose family" }
{ "index": { "_id": "2" } }
{ "byte-image-vector": [8, -15], "title": "alpine lake" }
{ "index": { "_id": "3" } }
{ "byte-image-vector": [11, 23], "title": "full moon" }
```

```console
POST byte-image-index/_search
{
  "knn": {
    "field": "byte-image-vector",
    "query_vector": [-5, 9], <1>
    "k": 10,
    "num_candidates": 100
  },
  "fields": [ "title" ]
}
```

1. Query values must also be integers in the range [-128, 127].

You can also pass `query_vector` as an encoded string.

{applies_to}`stack: ga 9.0-9.3` This request is equivalent to the previous search. `[-5, 9]` encoded as a hex byte string is `fb09`:

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

{applies_to}`{ stack: ga 9.4+, serverless: ga }` You can also pass a [base64-encoded query vector](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md). Base64 supports `float`, `bfloat16`, `byte`, and `bit` encodings depending on the field type.

### BFloat16 vector encoding [knn-search-bfloat16]
```{applies_to}
stack: ga 9.3+
serverless: ga
```

Set `element_type` to `bfloat16` to store each dimension as a 2-byte value instead of a 4-byte `float`. Use this when your indexed vectors are already at bfloat16 precision, or when you want to reduce the disk space required to store raw vector data. {{es}} rounds 4-byte float values to bfloat16 when indexing.

Retrieved vectors might differ slightly from the values originally indexed, because bfloat16 stores each dimension in 2 bytes.

## Oversampling and rescoring for quantized vectors [dense-vector-knn-search-rescoring]

Quantization reduces RAM for search and costs some recall. Rescoring recovers recall for the top candidates by scoring them again with the original vectors.

* **Oversampling** retrieves more candidates per shard than `k`.
* **Rescoring** recomputes scores for those candidates using the original (non-quantized) vectors.

Higher compression generally needs more oversampling to recover recall. There is no single `oversample` value that fits every model and dataset: measure recall and latency on your data.

BBQ (`bbq_hnsw` and `bbq_disk`) fields already apply a mapping-level `rescore_vector.oversample` of `3.0` unless you override it. `int8_hnsw` does not. Set `rescore_vector` at query time to change the factor.

Prefer the `rescore_vector` option for this workflow. For DiskBBQ (`bbq_disk`) indices, you can also let {{es}} pick oversampling per segment with [auto-calibration](#bbq-disk-auto-calibrate).

The [additional rescoring techniques](#dense-vector-knn-search-rescoring-rescore-additional) cover rescoring after the merge step, or custom per-shard scoring.

### The `rescore_vector` option [the-rescore_vector-option]
```{applies_to}
stack: preview =9.0, ga 9.1+
serverless: ga
```

Use `rescore_vector` to oversample and rerank quantized results. When you specify an `oversample` value, approximate kNN:

* Retrieves `num_candidates` candidates per segment. If needed, {{es}} raises `num_candidates` to `k * oversample`.
* Rescores the top `k * oversample` candidates per shard using the original vectors.
* Merges those candidates after rescoring and returns the global top `k`.

`oversample` must be `1` or greater.

{applies_to}`{ stack: ga 9.1+, serverless: ga }` Set `oversample` to `0` to skip oversampling and rescoring.

`rescore_vector` applies only to quantized `dense_vector` fields. {{es}} ignores it for non-quantized fields, because those fields already score with the original vectors.

A query-time `rescore_vector` overrides any mapping-level `rescore_vector.oversample` on the field.

This example uses `rescore_vector` with an `oversample` of `2.0`:

```console
POST quantized-image-index/_search
{
  "knn": {
    "field": "image-vector",
    "query_vector": [0.1, -2],
    "k": 10, <1>
    "num_candidates": 100, <2>
    "rescore_vector": {
      "oversample": 2.0 <3>
    }
  },
  "fields": [ "title" ]
}
```

1. The number of nearest neighbors to return (`k`).
2. Candidates gathered per segment for approximate retrieval. If this is lower than `k * oversample`, {{es}} raises it.
3. Rescore the top `k * oversample` (20) candidates per shard using the original vectors, then merge shards and return the top 10 (`k`).

### Auto-calibrate DiskBBQ oversampling [bbq-disk-auto-calibrate]
```{applies_to}
stack: ga 9.5+
```

For `bbq_disk` fields, set `auto_calibrate: true` in `index_options` to let {{es}} select quantization, oversampling, and preconditioning for each merged segment from the data in that segment.

A query-time `rescore_vector.oversample` still wins: it applies to every segment and overrides the calibrated values. If you do not set a query-time oversample, calibrated segments use their per-segment factors.

```console
PUT my-auto-calibrated-index
{
  "mappings": {
    "properties": {
      "image-vector": {
        "type": "dense_vector",
        "index_options": {
          "type": "bbq_disk",
          "auto_calibrate": true <1>
        }
      }
    }
  }
}
```

1. Lets {{es}} pick quantization, oversampling, and preconditioning per merged segment. A query-time `rescore_vector.oversample` overrides these calibrated values.

For how calibration runs, which segments it skips, and how it interacts with `bits` and `precondition`, refer to [Auto-calibration for `bbq_disk`](elasticsearch://reference/elasticsearch/mapping-reference/bbq.md#bbq-auto-calibration).

### The `on_disk_rescore` option [the-on_disk_rescore-option]
```{applies_to}
stack: preview 9.3+
serverless: unavailable
```

By default, {{es}} reads raw vector data into memory to perform rescoring. This can slow search if the vector data is too large to fit in off-heap memory at once. When you set `on_disk_rescore: true` in the field's [`index_options`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-index-options), {{es}} reads vector data directly from disk during rescoring.

This option applies only to newly indexed vectors. To apply it to all vectors in the index, reindex or force-merge after you change it.

For guidance on when on-disk rescoring helps, refer to [Use on-disk rescoring when the vector data does not fit in RAM](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md).

### Additional rescoring techniques [dense-vector-knn-search-rescoring-rescore-additional]

Use these approaches when you need to rescore without `rescore_vector`: after the merge step across shards, or with a custom score.

The examples in this section use an `int4_hnsw` field:

```console
PUT my-index
{
  "mappings": {
    "properties": {
      "my_int4_vector": {
        "type": "dense_vector",
        "dims": 4,
        "index_options": {
          "type": "int4_hnsw"
        }
      }
    }
  }
}
```

#### Use the `rescore` section for top-level kNN search [dense-vector-knn-search-rescoring-rescore-section]

Use this option to rescore the top results from all shards, rather than rescoring on each shard.

This example oversamples with the top-level `knn` search, then uses the [rescore](elasticsearch://reference/elasticsearch/rest-apis/filter-search-results.md#rescore) section to rerank the merged results:

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

1. The number of hits to return. This request returns 10 results and gathers 20 nearest neighbors for rescoring.
2. Neighbors returned by approximate kNN, using quantized scores. Because this is the top-level `knn` object, {{es}} gathers the global top 20 from all shards before rescoring. Combined with `rescore`, this oversamples by 2x.
3. The number of results to rescore. To rescore all kNN results, set this to the same value as `k`.
4. The script that rescores with the original `float` vector.
5. Weight of the original query. `0` discards the quantized score.
6. Weight of the rescore query. This example uses only the rescore query score.

#### Use a `script_score` query to rescore per shard [dense-vector-knn-search-rescoring-script-score]

Use this option to rescore on each shard when you need more control than `rescore_vector` provides.

Combine the [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md) with a [`script_score` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-script-score-query.md). This rescores more candidates per shard, which can increase recall at the cost of compute.

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
          "k": 20, <3>
          "num_candidates": 50
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

1. The number of results to return.
2. The `knn` query that runs the initial search. This runs per shard.
3. Neighbors returned per shard from the quantized search. `script_score` then rescores these hits with the original vectors. `num_candidates` is the per-segment candidate set and must be at least `k`.
4. The script that scores with the original `float` vector.

## Resources [knn-optimize-resources]

- [Approximate kNN search](approximate-knn.md): Map, index, and run a basic approximate kNN search, including indexing considerations.
- [Tune approximate kNN search](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md): Production sizing, memory, indexing, and cluster configuration for approximate kNN search.
- [kNN search on {{es}}](../knn.md): Common use cases, prerequisites, and a comparison of approximate and exact kNN methods.
- [`dense_vector` field type](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md): Vector mapping options, including `index_options` and quantization settings.
- [Auto-calibration for `bbq_disk`](elasticsearch://reference/elasticsearch/mapping-reference/bbq.md#bbq-auto-calibration): How DiskBBQ selects quantization and oversampling per merged segment.
- [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md): Parameters, `query_vector_builder` options, and usage with `dense_vector` and `semantic_text` fields.
