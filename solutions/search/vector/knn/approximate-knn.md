---
navigation_title: Approximate kNN search
description: Run fast, scalable approximate k-nearest neighbor (kNN) vector search in Elasticsearch, including search methods and indexing considerations.
applies_to:
  stack:
  serverless:
---

# Approximate kNN search

Approximate kNN search uses graph-based or clustered index structures to find similar vectors quickly at scale. Use it for most production workloads where low latency matters more than perfect recall. This page covers approximate kNN search methods, a basic example, mapping defaults, indexing considerations, and vector index mode.

::::{tip}
If you use `semantic_text` fields, query them with a [`match` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md) for the simplest approach, or use the [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md#knn-query-with-semantic-text) when you need more control over the search.
::::


::::{warning}
Approximate kNN search has specific resource requirements. For instance, for HNSW, all vector data must fit in the node’s page cache for efficient performance. Refer to the [approximate kNN tuning guide](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md) for configuration tips.
::::

## Approximate kNN search methods [approximate-knn-methods]

{{es}} provides three ways to run approximate kNN search, with different field type support:

| Method | Supported field types | Use case |
|---|---|---|
| [Top-level `knn` option](#approximate-knn-example) | [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) | Standalone kNN search or hybrid search with score fusion |
| [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md) | [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md), [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) | Composable with other queries in a `bool` clause. Required for `semantic_text` fields |
| [`knn` retriever](elasticsearch://reference/elasticsearch/rest-apis/retrievers/knn-retriever.md) | [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) | Use within a retriever pipeline for ranking and result merging |

## Basic example [approximate-knn-example]

Follow these steps to map `dense_vector` fields, index embeddings, and run a basic approximate kNN query.

1. Map one or more `dense_vector` fields. Approximate kNN search is enabled by default, so no extra mapping options are required.

    Optionally, you can configure additional parameters, including the similarity metric, index options, and quantization. Refer to [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-params) for the full list of parameters.

    ```console
    PUT image-index
    {
      "mappings": {
        "properties": {
          "image-vector": {
            "type": "dense_vector",
            "similarity": "l2_norm"
          },
          "title": {
            "type": "text"
          },
          "file-type": {
            "type": "keyword"
          }
        }
      }
    }
    ```

2. Index your data with embeddings. If you don't have vectors yet, refer to [Bring your own dense vectors](../bring-own-vectors.md) for options on generating or sourcing them.

    ```console
    POST image-index/_bulk?refresh=true
    { "index": { "_id": "1" } }
    { "image-vector": [1, 5, -20], "title": "moose family", "file-type": "jpg" }
    { "index": { "_id": "2" } }
    { "image-vector": [42, 8, -15], "title": "alpine lake", "file-type": "png" }
    { "index": { "_id": "3" } }
    { "image-vector": [15, 11, 23], "title": "full moon", "file-type": "jpg" }
    ...
    ```

3. Query using the [`knn` option]({{es-apis}}operation/operation-search#operation-search-body-application-json-knn):

    ```console
    POST image-index/_search
    {
      "knn": {
        "field": "image-vector",
        "query_vector": [-5, 9, -12],
        "k": 10
      }
    }
    ```

    Alternatively, use a [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md), which you can combine with other queries in a `bool` clause:

    ```console
    POST image-index/_search
    {
      "query": {
        "knn": {
          "field": "image-vector",
          "query_vector": [-5, 9, -12],
          "k": 10
        }
      }
    }
    ```

The document `_score` is a positive float calculated based on the chosen vector similarity metric. Refer to [`similarity`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-similarity) for details on how kNN scores are computed.

## Mapping defaults [approximate-knn-defaults]

Approximate kNN works without any explicit mapping options. Unless you set them, {{es}} applies these defaults:

| Parameter | Default |
|---|---|
| `index` | `true`, so the field is searchable with approximate kNN |
| `element_type` | `float` |
| `dims` | Inferred from the first vector indexed into the field |
| `similarity` | `cosine`, except for `bit` vectors, which use `l2_norm` |
| `index_options.type` | `float` and `bfloat16` vectors are quantized automatically, using BBQ where available and `int8_hnsw` for low-dimensional vectors. `byte` and `bit` vectors are not quantized. |

The last one matters most: by default your `float` vectors are quantized, which is what keeps memory use manageable at scale. Refer to [Default quantization types](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization) for how the default is chosen, and to [Optimize performance and accuracy](optimize-performance-accuracy.md) if you need to override it.

## Indexing considerations for approximate kNN search [knn-indexing-considerations]


For approximate kNN, {{es}} indexes dense vector values as an [HNSW graph](https://arxiv.org/abs/1603.09320) or as clusters using [DiskBBQ](https://www.elastic.co/search-labs/blog/diskbbq-elasticsearch-introduction). Building these structures is compute-intensive. [GPU-accelerated vector indexing](elasticsearch://reference/elasticsearch/mapping-reference/gpu-vector-indexing.md) is also supported. To reduce memory use and speed up vector distance calculations, {{es}} also [quantizes](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization) vectors. Quantization comes at the expense of recall, which you can compensate for by [oversampling and rescoring](optimize-performance-accuracy.md#dense-vector-knn-search-rescoring) more vectors. The `hnsw` and `bbq_disk` types each come with their own settings to balance recall, indexing speed, and vector search speed. For guidance on choosing and tuning these settings, refer to the [approximate kNN tuning guide](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md). When defining your `dense_vector` mapping, use [`index_options`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-index-options) to set these parameters.

## Vector index mode [approximate-knn-vector-index-mode]

If an index is used primarily for vector search, create it with the `vectordb_document` [index mode](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-mode-setting) to get defaults tuned for vector workloads:

```console
PUT my-vector-index
{
  "settings": {
    "index": {
      "mode": "vectordb_document"
    }
  }
}
```

In this mode, {{es}} encodes vectors as `bfloat16` to halve raw vector storage, excludes vector values from `_source`, preloads vector index files into the filesystem cache, and tunes merging for vector data. Approximate kNN search also defaults to `near_real_time: false`, so newly indexed vectors become searchable only after background optimization finishes.

Refer to [Index modes for vector search](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-index-modes) for the full list of applied settings, and to [Near-real-time kNN](optimize-performance-accuracy.md#near-real-time-knn) to override the search freshness default.

## Resources

- [kNN search on {{es}}](../knn.md): Explore common use cases, prerequisites for kNN search, and a comparison of approximate and exact kNN methods.
- [Examples of using approximate kNN in search queries](build-search-queries.md): See examples of using approximate kNN for filtering, hybrid retrieval, semantic search, multiple vector fields, and similarity thresholds.
- [Nested kNN search](nested-knn-search.md): Learn how to run approximate kNN search on nested vectors for passage retrieval, filtering, inner hits, and chunked content.
- [Optimize performance and accuracy](optimize-performance-accuracy.md): Learn how to tune search speed, recall, vector storage, quantization, and rescoring for approximate kNN search.
- [Tune approximate kNN search](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md): Production guidance on vector memory footprint, node sizing, filesystem cache warm-up, GPU-accelerated indexing, and on-disk rescoring.
- [`dense_vector` field type](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md): API reference for vector field mapping, including `similarity`, `index_options`, and quantization parameters.
- [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md): API reference for the `knn` query, including parameters, `query_vector_builder` options, and usage with `dense_vector` and `semantic_text` fields.
