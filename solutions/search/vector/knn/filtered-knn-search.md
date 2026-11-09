---
navigation_title: Filter approximate kNN results
description: Filter approximate kNN search results and understand pre-filtering, post-filtering, and HNSW filtering performance in Elasticsearch.
applies_to:
  stack:
  serverless:
---

# Filter approximate kNN results [knn-search-filter-example]

Use a filter with approximate kNN when you want the most similar results, but only from a specific subset of your data. For example, you might search for similar products in one category, documents from a certain time period, or images with a particular file type.

The examples run against the `image-index` mapping and sample data from [Approximate kNN search](approximate-knn.md#approximate-knn-example).

Add a `filter` to the `knn` clause. {{es}} returns the top `k` nearest neighbors that also satisfy the filter query:

```console
POST image-index/_search
{
  "knn": {
    "field": "image-vector",
    "query_vector": [54, 10, -2],
    "k": 5,
    "num_candidates": 50,
    "filter": {
      "term": {
        "file-type": "png"
      }
    }
  },
  "fields": ["title"],
  "_source": false
}
```

::::{note}
The filter is applied **during** approximate kNN search to ensure that `k` matching documents are returned. In contrast, post-filtering applies the filter **after** the approximate kNN step and can return fewer than `k` results, even when enough relevant documents exist.
::::

## Pre-filtering and post-filtering [knn-prefilter-vs-postfilter]

Pre-filtering only happens when the filter is part of the kNN clause itself. The `filter` parameter of the `knn` option, the `knn` query, and the `knn` retriever all pre-filter. A filter placed outside the kNN clause does not.

This distinction matters most when you translate a filtered search into the [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md) form. In the following request, the `filter` clause of the `bool` query is a sibling of the `knn` query, so it's applied **after** the vector search:

```console
POST image-index/_search
{
  "query": {
    "bool": {
      "must": {
        "knn": {
          "field": "image-vector",
          "query_vector": [54, 10, -2],
          "k": 5,
          "num_candidates": 50
        }
      },
      "filter": {
        "term": {
          "file-type": "png"
        }
      }
    }
  }
}
```

The kNN search runs without any knowledge of the filter and returns the five nearest images regardless of file type. Only then does the `bool` query discard the ones that aren't PNGs, so the response can contain far fewer than five hits, or none at all, even when the index holds plenty of similar PNGs.

To pre-filter instead, move the filter inside the `knn` query:

```console
POST image-index/_search
{
  "query": {
    "knn": {
      "field": "image-vector",
      "query_vector": [54, 10, -2],
      "k": 5,
      "num_candidates": 50,
      "filter": {
        "term": {
          "file-type": "png"
        }
      }
    }
  }
}
```

Post-filtering isn't always wrong. It's a reasonable choice when the filter matches most of your documents and you'd rather not pay the cost of filtered graph traversal. But when the filter is selective, pre-filter.

## Filtering behavior and performance [filtering-behavior-and-performance]

In approximate kNN search with an HNSW index, filters can make a search slower rather than faster, because the search has to explore more of the graph to collect enough candidates that satisfy the filter. This is the opposite of conventional query filtering, where a stricter filter usually speeds up a query.

To limit the impact, Lucene falls back to brute force per segment in two cases:

* If the number of documents matching the filter in a segment is no greater than the number of candidates the search would examine there, the search skips the HNSW graph and scores the filtered documents directly.
* While exploring the graph, if the search visits more nodes than there are documents matching the filter, it stops traversing and scores the filtered documents directly.

:::{note}
:applies_to: stack: preview 9.1
For indices created in 9.1 or later, {{es}} also applies the `acorn` filter heuristic by default, which traverses only vectors that match the filter instead of comparing every vector it visits. This is generally faster at comparable recall, although you might need to raise `num_candidates` to hit exceptionally high recall targets. To change the heuristic, use [`index.dense_vector.hnsw_filter_heuristic`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-dense-vector-hnsw-filter-heuristic).
:::

For more ways to trade approximate search speed against accuracy, refer to [Optimize approximate kNN performance and accuracy](optimize-performance-accuracy.md).
