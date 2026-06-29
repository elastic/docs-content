---
navigation_title: Approximate kNN search
description: Run fast, scalable approximate k-nearest neighbor (kNN) vector search in Elasticsearch using dense_vector fields and HNSW indexing.
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-knn-search.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Approximate kNN search [approximate-knn]

Approximate kNN search uses graph-based or clustered index structures to find similar vectors quickly at scale. Use it for most production workloads where low latency matters more than perfect recall. For tuning trade-offs among speed, accuracy, storage, and quantization, refer to [Optimize performance and accuracy](optimize-performance-accuracy.md). For query patterns such as filtering, hybrid retrieval, and nested vectors, refer to [Build search queries](build-search-queries.md).


::::{warning}
Approximate kNN search has specific resource requirements. For instance, for HNSW, all vector data must fit in the node’s page cache for efficient performance. Refer to the [approximate kNN tuning guide](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md) for configuration tips.
::::

To run an approximate kNN search:

1. Map one or more `dense_vector` fields. Approximate kNN search requires the following mapping options:  

    * A `similarity` value. This value determines the similarity metric used to score documents based on similarity between the query and document vector. For a list of available metrics, see the [`similarity`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-similarity) parameter documentation. The `similarity` setting defaults to `cosine`.

    ```console
    PUT image-index
    {
      "mappings": {
        "properties": {
          "image-vector": {
            "type": "dense_vector",
            "dims": 3,
            "similarity": "l2_norm"
          },
          "title-vector": {
            "type": "dense_vector",
            "dims": 5,
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

2. Index your data with embeddings.  

    ```console
    POST image-index/_bulk?refresh=true
    { "index": { "_id": "1" } }
    { "image-vector": [1, 5, -20], "title-vector": [12, 50, -10, 0, 1], "title": "moose family", "file-type": "jpg" }
    { "index": { "_id": "2" } }
    { "image-vector": [42, 8, -15], "title-vector": [25, 1, 4, -12, 2], "title": "alpine lake", "file-type": "png" }
    { "index": { "_id": "3" } }
    { "image-vector": [15, 11, 23], "title-vector": [1, 5, 25, 50, 20], "title": "full moon", "file-type": "jpg" }
    ...
    ```

3. Query using the [`knn` option]({{es-apis}}operation/operation-search#operation-search-body-application-json-knn) or a [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md).

    ```console
    POST image-index/_search
    {
      "knn": {
        "field": "image-vector",
        "query_vector": [-5, 9, -12],
        "k": 10,
        "num_candidates": 100
      },
      "fields": [ "title", "file-type" ]
    }
    ```

The document `_score` is a positive 32-bit floating-point number that ranks result relevance. In {{es}} kNN search, `_score` is derived from the chosen vector similarity metric between the query and document vectors. Refer to [`similarity`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-similarity) for details on how kNN scores are computed.

::::{note}
Support for approximate kNN search was added in version 8.0. Before 8.0, `dense_vector` fields did not support enabling `index` in the mapping. If you created an index before 8.0 with `dense_vector` fields, reindex using a new mapping with `index: true` (which is the default value) to use approximate kNN.
::::

## Indexing considerations for approximate kNN search [knn-indexing-considerations]


For approximate kNN, {{es}} stores dense vector values per segment as an [HNSW graph](https://arxiv.org/abs/1603.09320) or per segment as clusters using [DiskBBQ](https://www.elastic.co/search-labs/blog/diskbbq-elasticsearch-introduction). Building these approximate kNN structures is compute-intensive, which means indexing vectors can be time-consuming. As a result, you might need to increase client request timeouts for index and bulk operations. The [approximate kNN tuning guide](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md) covers indexing performance, sizing, and configuration trade-offs that affect search performance.

{applies_to}`stack: ga 9.2` In addition to search-time parameters, HNSW and DiskBBQ expose index-time settings that balance graph build cost, search speed, and accuracy. When defining your `dense_vector` mapping, use [`index_options`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-index-options) to set these parameters:

::::{tip}
When using the [`semantic_text` field type](../../semantic-search/semantic-search-semantic-text.md) with dense vector embeddings, you can also configure `index_options` directly on the field. Refer to [Optimizing vector storage with `index_options`](../vector-storage-for-semantic-search.md) for examples.
::::

```console
PUT image-index
{
  "mappings": {
    "properties": {
      "image-vector": {
        "type": "dense_vector",
        "dims": 3,
        "similarity": "l2_norm",
        "index_options": {
          "type": "hnsw",
          "m": 32,
          "ef_construction": 100
        }
      }
    }
  }
}
```

## Limitations for approximate kNN search [approximate-knn-limitations]

* When using kNN search in [{{ccs}}](../../../../explore-analyze/cross-cluster-search.md), the [`ccs_minimize_roundtrips`](../../../../explore-analyze/cross-cluster-search.md#ccs-min-roundtrips) option is not supported.
* {{es}} uses the [HNSW algorithm](https://arxiv.org/abs/1603.09320) for efficient kNN. Like most approximate methods, HNSW trades perfect accuracy for speed, so results aren’t always the true *k* closest neighbors.

::::{note}
Approximate kNN always uses the [`dfs_query_then_fetch`]({{es-apis}}operation/operation-search) search type to gather the global top `k` matches across shards. You can’t set `search_type` explicitly for kNN search.
::::

