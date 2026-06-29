---
navigation_title: Optimize performance and accuracy
description: Tune approximate kNN search in Elasticsearch for speed, recall, vector storage, quantization, and rescoring trade-offs.
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Optimize performance and accuracy [optimize-knn-performance-accuracy]

This page covers trade-offs among search speed, recall, indexing cost, vector storage, quantization, and rescoring for approximate kNN search.

## Tune approximate kNN for speed or accuracy [tune-approximate-knn-for-speed-accuracy]

To gather results, the kNN API first finds a `num_candidates` number of approximate neighbors per shard, computes similarity to the query vector, selects the top `k` per shard, and merges them into the global top `k` nearest neighbors.

For HNSW indices, `num_candidates` is the main search-time speed/accuracy control:

* Increase `num_candidates` to improve recall and accuracy (at the cost of higher latency).
* Decrease `num_candidates` for faster queries (with a potential accuracy trade-off).

For DiskBBQ (`bbq_disk`) indices, you can also use `visit_percentage` to control the total percentage of vectors visited during search. `visit_percentage` accepts values from `0` to `100`, including decimal values such as `0.5` (half a percent):

* A good starting value is `3` (3%).
* Increase `visit_percentage` to improve recall and accuracy (at the cost of higher latency).
* Decrease `visit_percentage` for faster queries (with a potential accuracy trade-off).

When a search targets both HNSW and DiskBBQ indices, use `visit_percentage` with `num_candidates` to tune performance and recall across both index types.

When [quantization](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization) is involved, `rescore_vector` is an additional speed/accuracy tuning tool. It reranks a larger candidate set using original vectors after approximate retrieval.

* Increase `rescore_vector.oversample` to improve accuracy (at the cost of higher latency).
* Decrease `rescore_vector.oversample` for faster queries (with a potential accuracy trade-off).
* For detailed behavior and usage guidance, see [Oversampling and rescoring for quantized vectors](#dense-vector-knn-search-rescoring).

## Approximate kNN using byte vectors [approximate-knn-using-byte-vectors]

The approximate kNN search API also supports `byte` (int8) value vectors alongside `float` vectors. Use the [`knn` option]({{es-apis}}operation/operation-search#operation-search-body-application-json-knn) to search a `dense_vector` field with [`element_type`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-params) set to `byte` and indexing enabled. Byte vectors reduce memory footprint and can improve cache efficiency for large-scale vector similarity search.

1. Explicitly map one or more `dense_vector` fields with [`element_type`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-params) set to `byte` and indexing enabled.

    ```console
    PUT byte-image-index
    {
      "mappings": {
        "properties": {
          "byte-image-vector": {
            "type": "dense_vector",
            "element_type": "byte",
            "dims": 2
          },
          "title": {
            "type": "text"
          }
        }
      }
    }
    ```

2. Index your data ensuring all vector values are integers within the range [-128, 127].

    ```console
    POST byte-image-index/_bulk?refresh=true
    { "index": { "_id": "1" } }
    { "byte-image-vector": [5, -20], "title": "moose family" }
    { "index": { "_id": "2" } }
    { "byte-image-vector": [8, -15], "title": "alpine lake" }
    { "index": { "_id": "3" } }
    { "byte-image-vector": [11, 23], "title": "full moon" }
    ```

3. Run the search using the [`knn` option]({{es-apis}}operation/operation-search#operation-search-body-application-json-knn) ensuring the `query_vector` values are integers within the range [-128, 127].

    ```console
    POST byte-image-index/_search
    {
      "knn": {
        "field": "byte-image-vector",
        "query_vector": [-5, 9],
        "k": 10,
        "num_candidates": 100
      },
      "fields": [ "title" ]
    }
    ```


*Note*: In addition to the standard byte array, one can also provide a hex-encoded string value for the `query_vector` param. As an example, the search request above can also be expressed as follows, which would yield the same results

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

## Byte quantized kNN search [knn-search-quantized-example]

If you want to provide `float` vectors but still get the memory savings of `byte` vectors, use the [quantization](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization) feature. Quantization allows you to provide `float` vectors, but internally they are indexed as `byte` vectors. Additionally, the original `float` vectors are still retained in the index.

::::{note}
The default index type for `float` vectors is either `bbq_hnsw` or `int8_hnsw`, depending on your product version and vector dimensions. Other element types, such as `byte`, default to plain `hnsw` with no quantization. Refer to [Dense vector field type](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md).
::::

You can use the default quantization strategy or specify an index option.
For example, use `int8_hnsw`:

```console
PUT quantized-image-index
{
  "mappings": {
    "properties": {
      "image-vector": {
        "type": "dense_vector",
        "element_type": "float",
        "dims": 2,
        "index": true,
        "index_options": {
          "type": "int8_hnsw"
        }
      },
      "title": {
        "type": "text"
      }
    }
  }
}
```

1. Index your `float` vectors.

    ```console
    POST quantized-image-index/_bulk?refresh=true
    { "index": { "_id": "1" } }
    { "image-vector": [0.1, -2], "title": "moose family" }
    { "index": { "_id": "2" } }
    { "image-vector": [0.75, -1], "title": "alpine lake" }
    { "index": { "_id": "3" } }
    { "image-vector": [1.2, 0.1], "title": "full moon" }
    ```

2. Run the search using the [`knn` option]({{es-apis}}operation/operation-search#operation-search-body-application-json-knn). When searching, the `float` vector is automatically quantized to a `byte` vector.

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

Because the original `float` vectors are retained alongside the quantized index, you can use them for re-scoring: retrieve candidates quickly via the `int8_hnsw` index, then rescore the top `k` hits using the original `float` vectors. This provides the best of both worlds, fast search and accurate scoring.

```console
POST quantized-image-index/_search
{
  "knn": {
    "field": "image-vector",
    "query_vector": [0.1, -2],
    "k": 15,
    "num_candidates": 100
  },
  "fields": [ "title" ],
  "rescore": {
    "window_size": 10,
    "query": {
      "rescore_query": {
        "script_score": {
          "query": {
            "match_all": {}
          },
          "script": {
            "source": "cosineSimilarity(params.query_vector, 'image-vector') + 1.0",
            "params": {
              "query_vector": [0.1, -2]
            }
          }
        }
      }
    }
  }
}
```

## BFloat16 vector encoding [knn-search-bfloat16]
```{applies_to}
stack: ga 9.3
```
Instead of storing raw vectors as 4-byte values, you can use `element_type: bfloat16` to store each dimension as a 2-byte value. This can be useful if your indexed vectors are at bfloat16 precision already, or if you want to reduce the disk space required to store vector data. When this element type is used, {{es}} automatically rounds 4-byte float values to 2-byte bfloat16 values when indexing vectors.

Due to the reduced precision of bfloat16, any vectors retrieved from the index might have slightly different values to those originally indexed.

## Oversampling and rescoring for quantized vectors [dense-vector-knn-search-rescoring]

When using [quantized vectors](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization) for kNN search, can optionally rescore results to balance performance and accuracy, by doing:

* **Oversampling** — retrieving more candidates per shard.
* **Rescoring** — recalculating scores on those oversampled candidates using the original (non-quantized) vectors.

Because final scores are computed with the original `float` vectors, rescoring combines:

* The performance and memory benefits of approximate retrieval with quantized vectors.
* The accuracy of using the original vectors for rescoring the top candidates.

All quantization introduces some accuracy loss, and higher compression generally increases that loss. In practice:

* `int8` typically needs little to no rescoring.
* `int4` often benefits from rescoring for higher accuracy or recall; 1.5×–2× oversampling usually recovers most loss.
* `bbq` commonly requires rescoring except on very large indices or models specifically designed for quantization; 3×–5× oversampling is generally sufficient, but higher might be needed for low-dimension vectors or embeddings that quantize poorly.

### The `rescore_vector` option
```{applies_to}
stack: preview =9.0, ga 9.1+
```

Use `rescore_vector` to automatically perform reranking. When you specify an `oversample` value, approximate kNN will:

* Retrieve `num_candidates` candidates per shard.
* Rescore the top `k * oversample` candidates per shard using the original vectors.
* Return the top `k` rescored candidates.

Here is an example of using the `rescore_vector` option with the `oversample` parameter:

```console
POST image-index/_search
{
  "knn": {
    "field": "image-vector",
    "query_vector": [-5, 9, -12],
    "k": 10,
    "num_candidates": 100,
    "rescore_vector": {
      "oversample": 2.0
    }
  },
  "fields": [ "title", "file-type" ]
}
```

This example will:

* Search using approximate kNN for the top 100 candidates.
* Rescore the top 20 candidates (`oversample * k`) per shard using the original, non quantized vectors.
* Return the top 10 (`k`) rescored candidates.
* Merge the rescored candidates from all shards, and return the top 10 (`k`) results.

### The `on_disk_rescore` option
```{applies_to}
stack: preview 9.3
serverless: unavailable
```

By default, {{es}} reads raw vector data into memory to perform rescoring. This can have an effect on performance if the vector data is too large to all fit in off-heap memory at once. When the `on_disk_rescore: true` index setting is set, {{es}} reads vector data directly from disk during rescoring.

This setting only applies to newly indexed vectors. To apply the option to all vectors in the index, the vectors must be re-indexed or force-merged after changing the setting.

### Additional rescoring techniques [dense-vector-knn-search-rescoring-rescore-additional]

The following sections provide additional ways of rescoring:

#### Use the `rescore` section for top-level kNN search [dense-vector-knn-search-rescoring-rescore-section]

You can use this option when you don’t want to rescore on each shard, but on the top results from all shards.

Use the [rescore section](elasticsearch://reference/elasticsearch/rest-apis/filter-search-results.md#rescore) in the `_search` request to rescore the top results from a kNN search.

Here is an example using the top level `knn` search with oversampling and using `rescore` to rerank the results:

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

1. The number of results to return, note its only 10 and we will oversample by 2x, gathering 20 nearest neighbors.
2. The number of results to return from the KNN search. This will do an approximate KNN search with 50 candidates per HNSW graph and use the quantized vectors, returning the 20 most similar vectors according to the quantized score. Additionally, because this is the top-level `knn` object, the global top 20 results from all shards will be gathered before rescoring. Combining with `rescore`, this is oversampling by `2x`, meaning gathering 20 nearest neighbors according to quantized scoring and rescoring with higher fidelity float vectors.
3. The number of results to rescore, if you want to rescore all results, set this to the same value as `k`
4. The script to rescore the results. Script score will interact directly with the originally provided float32 vector.
5. The weight of the original query, here we throw away the original score
6. The weight of the rescore query, here we only use the rescore query

#### Use a `script_score` query to rescore per shard [dense-vector-knn-search-rescoring-script-score]

You can use this option when you want to rescore on each shard and want more fine-grained control on the rescoring than the `rescore_vector` option provides.

Use rescore per shard with the [knn query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md) and [script_score query ](elasticsearch://reference/query-languages/query-dsl/query-dsl-script-score-query.md). Generally, this means that there will be more rescoring per shard, but this can increase overall recall at the cost of compute.

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
          "num_candidates": 20 <3>
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

1. The number of results to return
2. The `knn` query to perform the initial search, this is executed per-shard
3. The number of candidates to use for the initial approximate `knn` search. This will search using the quantized vectors and return the top 20 candidates per shard to then be scored
4. The script to score the results. Script score will interact directly with the originally provided float32 vector.

