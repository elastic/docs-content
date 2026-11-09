---
navigation_title: Approximate kNN query examples
description: Examples of using approximate kNN in Elasticsearch search queries for similarity thresholds, hybrid search, multiple vector fields, and aggregations.
applies_to:
  stack:
  serverless:
---

# Approximate kNN query examples [build-approximate-knn-queries]

This page collects query patterns specific to approximate kNN: requiring a minimum similarity, combining approximate kNN with other retrieval methods, searching several vector fields at once, and aggregating over the nearest neighbors.

Except where a text embedding model is required, the examples run against the `image-index` mapping and sample data from [Approximate kNN search](approximate-knn.md#approximate-knn-example). That index stores an `image-vector` field with `l2_norm` similarity, a `title` text field, and a `file-type` keyword field.

The examples use whichever of the three kNN forms suits the pattern: the top-level `knn` option, the [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md), or the [`knn` retriever](elasticsearch://reference/elasticsearch/rest-apis/retrievers/knn-retriever.md). Refer to [Approximate kNN search methods](approximate-knn.md#approximate-knn-methods) to choose between them for your own searches. For query vector examples shared by exact and approximate kNN, refer to [kNN search examples](../knn.md#knn-search-examples). For filtered approximate kNN search, refer to [Filter approximate kNN results](filtered-knn-search.md). For vectors stored in `nested` fields, refer to [Nested approximate kNN search](nested-knn-search.md).

## Set a similarity threshold for approximate kNN [knn-similarity-search]

Approximate kNN always tries to return `k` nearest neighbors, even when none of them are close. Combined with a `filter`, this means you can filter away every relevant document and still receive `k` hits, drawn from whatever distant vectors remain.

Use the `similarity` parameter to set a threshold that a vector must meet to be considered a match. The `knn` search flow with this parameter is:

* Apply any user-provided `filter` queries.
* Explore the vector space to gather `k` candidates.
* Discard candidates that don't meet the `similarity` threshold.

Because the threshold is applied last, a search can return fewer than `k` hits, which is the point of the parameter.

### Understand threshold values by similarity metric [knn-threshold-by-similarity]

What the threshold means depends on the [similarity](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-similarity) configured on the field:

* `l2_norm`: a **maximum distance**. Matches are the vectors that fall within a `dims`-dimensional hypersphere of radius `similarity`, centered on `query_vector`. Lower values are stricter.
* `cosine`, `dot_product`, and `max_inner_product`: a **minimum similarity**. Higher values are stricter.

::::{note}
`similarity` is the true similarity value **before** it is transformed into `_score` and before any boosts are applied.
::::

### Derive a threshold from an observed score [knn-threshold-from-score]

To derive a threshold from a `_score` you've already observed, invert the score. For `float` and `bfloat16` vectors:

* `l2_norm`: `sqrt((1 / _score) - 1)`
* `cosine`: `(2 * _score) - 1`
* `dot_product`: `(2 * _score) - 1`
* `max_inner_product`:
  * `_score < 1`: `1 - (1 / _score)`
  * `_score >= 1`: `_score - 1`

`byte` and `bit` vectors use different score formulas, so these inversions don't apply to them.

The following query searches for the given `query_vector`, restricts results to PNG files, and requires that matches fall within an `l2_norm` distance of `36`:

```console
POST image-index/_search
{
  "knn": {
    "field": "image-vector",
    "query_vector": [1, 5, -20],
    "k": 5,
    "num_candidates": 50,
    "similarity": 36,
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

In this data set, the only document with `file-type = png` has the vector `[42, 8, -15]`. Its `l2_norm` distance from `[1, 5, -20]` is `41.412`, which is farther than the threshold of `36` allows. The filter leaves one candidate and the threshold rejects it, so this search returns no hits.

## Use approximate kNN in hybrid search [combine_approximate_knn_with_other_features]

Combine approximate kNN with other retrieval methods when you want one ranked result list that reflects both how similar documents are to your query vector and how well they match specific words or phrases. For example, you might find images that look similar to a reference photo while also matching a title keyword like "mountain lake".

The difficulty is that BM25 scores and vector similarity scores live on unrelated scales, and those scales shift with the query. Combining them by rank, or by normalizing them first, is more robust than adding raw scores together.

### Combine results with an `rrf` retriever [knn-hybrid-rrf]

[Reciprocal rank fusion](elasticsearch://reference/elasticsearch/rest-apis/reciprocal-rank-fusion.md) (RRF) merges result sets by the rank a document holds in each one, ignoring the raw scores entirely. This is the recommended starting point for hybrid search, because it needs no score tuning.

Pass a `standard` retriever for the keyword query and a `knn` retriever for the vector search to an [`rrf` retriever](elasticsearch://reference/elasticsearch/rest-apis/retrievers/rrf-retriever.md):

```console
POST image-index/_search
{
  "retriever": {
    "rrf": {
      "retrievers": [
        {
          "standard": {
            "query": {
              "match": {
                "title": "mountain lake"
              }
            }
          }
        },
        {
          "knn": {
            "field": "image-vector",
            "query_vector": [54, 10, -2],
            "k": 50,
            "num_candidates": 100
          }
        }
      ],
      "rank_window_size": 50 <1>
    }
  },
  "size": 10
}
```

1. How many results to pull from each retriever before merging. Raising it improves relevance at the cost of performance. It must be at least as large as `size`, and defaults to `10`. Set the `knn` retriever's `k` to at least this value, or the vector result set won't fill the window.

### Weight the two result sets with a `linear` retriever [knn-hybrid-linear]

When you do want explicit control over how much each signal contributes, use a [`linear` retriever](elasticsearch://reference/elasticsearch/rest-apis/retrievers/linear-retriever.md). It normalizes each retriever's scores, then combines them as a weighted sum. Normalizing first is what makes the weights meaningful, because it puts both result sets on the same 0-to-1 scale before the weights apply.

```console
POST image-index/_search
{
  "retriever": {
    "linear": {
      "retrievers": [
        {
          "retriever": {
            "standard": {
              "query": {
                "match": {
                  "title": "mountain lake"
                }
              }
            }
          },
          "weight": 0.9, <1>
          "normalizer": "minmax" <2>
        },
        {
          "retriever": {
            "knn": {
              "field": "image-vector",
              "query_vector": [54, 10, -2],
              "k": 50,
              "num_candidates": 100
            }
          },
          "weight": 0.1,
          "normalizer": "minmax"
        }
      ],
      "rank_window_size": 50
    }
  },
  "size": 10
}
```

1. The multiplier applied to this retriever's normalized scores. Defaults to `1.0`.
2. How to normalize this retriever's scores before weighting. `minmax` rescales each result set to a range of 0 to 1.

### Combine the `knn` option with a `query` [knn-hybrid-score-sum]

You can also perform hybrid retrieval without retrievers, by combining the [`knn` option]({{es-apis}}operation/operation-search#operation-search-body-application-json-knn) with a standard [`query`]({{es-apis}}operation/operation-search#operation-search-query) in the same request. This is the most direct form, but it adds the two raw scores together, so you have to tune the boosts by hand for your data and query mix.

```console
POST image-index/_search
{
  "query": {
    "match": {
      "title": {
        "query": "mountain lake",
        "boost": 0.9
      }
    }
  },
  "knn": {
    "field": "image-vector",
    "query_vector": [54, 10, -2],
    "k": 5,
    "num_candidates": 50,
    "boost": 0.1
  },
  "size": 10
}
```

This search finds the global top `k = 5` vector matches, combines them with the matches from the `match` query, and returns the 10 top-scoring results. The `knn` and `query` matches are combined through a disjunction, as if you took a boolean *OR* between them. The top `k` vector results represent the global nearest neighbors across all index shards.

The score of each result is the sum of the `knn` and `query` scores, and the `boost` values weight each score in that sum. In the preceding example, the scores are calculated as follows:

```
score = 0.9 * match_score + 0.1 * knn_score
```

For more on hybrid search, including approaches that use `semantic_text` fields and {{esql}}, refer to [Hybrid search](../../hybrid-search.md).

## Search multiple vector fields with approximate kNN [_search_multiple_knn_fields]

Search multiple vector fields with approximate kNN when your documents store more than one vector representation and you want to rank results by similarity across all of them in a single request. For example, you might search an image embedding and a title embedding together to surface documents that are both visually and semantically relevant.

These examples add a second vector field, `title-vector`, to the `image-index` mapping created in [Approximate kNN search](approximate-knn.md#approximate-knn-example):

```console
PUT image-index/_mapping
{
  "properties": {
    "title-vector": {
      "type": "dense_vector",
      "similarity": "l2_norm"
    }
  }
}
```

Pass an array to the `knn` option to search both fields, optionally alongside a `query`:

```console
POST image-index/_search
{
  "query": {
    "match": {
      "title": {
        "query": "mountain lake",
        "boost": 0.9
      }
    }
  },
  "knn": [ {
    "field": "image-vector",
    "query_vector": [54, 10, -2],
    "k": 5,
    "num_candidates": 50,
    "boost": 0.1
  },
  {
    "field": "title-vector",
    "query_vector": [1, 20, -52, 23, 10],
    "k": 10,
    "num_candidates": 100,
    "boost": 0.5
  }],
  "size": 10
}
```

This search retrieves the global top `k = 5` neighbors for `image-vector` and the global top `k = 10` for `title-vector`. These vector result sets are combined with the matches from the `match` query, and the top 10 overall documents are returned. Multiple `knn` clauses and the `query` clause are combined via a disjunction (boolean *OR*). The top `k` vector results represent the global nearest neighbors across all index shards.

With the boosts configured above, a document is scored as:

```
score = 0.9 * match_score + 0.1 * knn_score_image-vector + 0.5 * knn_score_title-vector
```

As with hybrid retrieval, you can instead pass one `knn` retriever per field to an `rrf` or `linear` retriever, which spares you from balancing raw scores across fields. Refer to [](#combine_approximate_knn_with_other_features).

## Aggregate over approximate kNN results [knn-aggregations]

You can use [aggregations](/explore-analyze/query-filter/aggregations.md) with the `knn` option, but the buckets cover a different document set than you might expect. {{es}} computes aggregations over the documents that match the search, and for approximate kNN that means the top `k` nearest documents rather than everything in the index. If the request also includes a `query`, aggregations cover the combined set of `knn` and `query` matches.

The following request buckets the five nearest images by file type:

```console
POST image-index/_search
{
  "knn": {
    "field": "image-vector",
    "query_vector": [-5, 9, -12],
    "k": 5,
    "num_candidates": 50
  },
  "aggs": {
    "file-types": {
      "terms": {
        "field": "file-type"
      }
    }
  }
}
```

The `file-types` buckets describe the five nearest neighbors only, so treat the counts as a summary of the result set rather than of the index. To aggregate across all documents that match a filter, run a separate request without a `knn` clause.

## Resources

Use these resources to explore related search approaches and API details:

- [Tune approximate kNN search](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md): Production guidance for vector memory, node sizing, indexing, filesystem cache, and on-disk rescoring.
- [Profile kNN search](elasticsearch://reference/elasticsearch/rest-apis/search-profile.md#profiling-knn-search): Inspect query timing and vector operation counts to diagnose slow kNN searches.
- [`dense_vector` field type](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md): API reference for vector field mapping, including `index`, `similarity`, `index_options`, and quantization parameters.
- [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md): API reference for the `knn` query, including parameters, `query_vector_builder` options, and usage with `dense_vector` and `semantic_text` fields.
