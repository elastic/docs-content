---
navigation_title: Examples of using approximate kNN
description: Examples of using approximate kNN in Elasticsearch search queries for query vector builders, filtering, similarity thresholds, hybrid search, multiple vector fields, and aggregations.
applies_to:
  stack:
  serverless:
---

# Examples of using approximate kNN in search queries [build-approximate-knn-queries]

This page collects the query patterns you need most often with approximate kNN: building the query vector, restricting results with filters, requiring a minimum similarity, combining kNN with keyword search, searching several vector fields at once, and aggregating over kNN results.

Except where a text embedding model is required, the examples run against the `image-index` mapping and sample data from [Approximate kNN search](approximate-knn.md#approximate-knn-example). That index stores an `image-vector` field with `l2_norm` similarity, a `title` text field, and a `file-type` keyword field.

The examples use whichever of the three kNN forms suits the pattern: the top-level `knn` option, the [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md), or the [`knn` retriever](elasticsearch://reference/elasticsearch/rest-apis/retrievers/knn-retriever.md). Refer to [Approximate kNN search methods](approximate-knn.md#approximate-knn-methods) to choose between them for your own searches. For vectors stored in `nested` fields, refer to [Nested kNN search](nested-knn-search.md).

## Build the query vector [knn-build-query-vector]

Every kNN search needs a query vector. Provide it directly as `query_vector`, as most examples on this page do, or have {{es}} produce it at search time with `query_vector_builder`. Building the vector at search time keeps embedding logic out of your application, at the cost of some search latency.

Three builders are available, and all of them work with the `knn` option, the `knn` query, and the `knn` retriever:

- `text_embedding` generates a vector from query text using a text embedding model deployed in {{es}}. Refer to [Perform semantic search](#knn-semantic-search).
- `lookup` reuses a vector already stored in a document. Refer to [Find documents similar to an existing document](#knn-lookup-similar-documents). {applies_to}`stack: ga 9.4`
- `embedding` generates a vector from text or a base64-encoded image using an {{infer}} endpoint, which makes multimodal search possible. Refer to [Multimodal search](../../multimodal-search.md) for the use case and [`embedding`](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md#knn-query-builder-embedding) for the parameters. {applies_to}`stack: preview 9.4` {applies_to}`serverless: preview`

### Perform semantic search [knn-semantic-search]

kNN search lets you perform semantic search with a previously deployed [text embedding model](../../../../explore-analyze/machine-learning/nlp/ml-nlp-search-compare.md#ml-nlp-text-embedding). Instead of matching search terms literally, semantic search retrieves results based on the intent and contextual meaning of the query.

The model converts your input string into a dense vector, which {{es}} compares against vectors created with the same model. Because the comparison happens in the model's embedding space, the results are semantically similar as learned by the model.

:::{tip}
The `semantic_text` field type handles model management, chunking, and embedding for you, and it's the recommended starting point for semantic search. Use the pattern in this section when you need to manage the model and the `dense_vector` mapping yourself. Refer to [Semantic search with `semantic_text`](../../semantic-search/semantic-search-semantic-text.md).
:::

To perform semantic search:

- Your index must contain dense vector representations of the input data.
- Use the same text embedding model for search that generated the document vectors.
- Start the text embedding model deployment before running the query.

Reference the deployed model or its deployment in the `query_vector_builder` object, and pass the search string as `model_text`:

```console
POST my-index/_search
{
  "knn": {
    "field": "dense-vector-field",
    "k": 10,
    "num_candidates": 100,
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "my-text-embedding-model", <1>
        "model_text": "The opposite of blue" <2>
      }
    }
  }
}
```

1. The ID of the text embedding model that generates the query vector. Use the same model that produced the document embeddings in the target index. You can also provide a `deployment_id` as the `model_id` value.
2. The query string from which the model generates the dense vector representation.

For a walkthrough that covers deploying a model, generating document embeddings, and querying them, refer to this [end-to-end example](../../../../explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md).

### Find documents similar to an existing document [knn-lookup-similar-documents]
```{applies_to}
stack: ga 9.4
```

Use the `lookup` query vector builder when the vector you want to search with is already stored in a document. This is the pattern behind "more like this" and recommendation features: instead of embedding new input, you take the vector from an item the user is viewing and find its nearest neighbors.

The following request finds the images most similar to document `2`:

```console
POST image-index/_search
{
  "knn": {
    "field": "image-vector",
    "k": 10,
    "query_vector_builder": {
      "lookup": {
        "index": "image-index", <1>
        "id": "2", <2>
        "path": "image-vector" <3>
      }
    }
  }
}
```

1. The index that holds the document to look up. It doesn't have to be the index you're searching.
2. The ID of the document to look up. The request fails with a `404` if the document doesn't exist or has no value for `path`.
3. The vector field to read the query vector from. Its dimensions must match the field you're searching.

{{es}} reads the vector from the indexed field rather than from `_source`, so the lookup works even when vector values are excluded from `_source`.

The looked-up document is its own nearest neighbor, so it comes back as the top hit. Exclude it with a filter when you only want other documents:

```console
POST image-index/_search
{
  "knn": {
    "field": "image-vector",
    "k": 10,
    "query_vector_builder": {
      "lookup": {
        "index": "image-index",
        "id": "2",
        "path": "image-vector"
      }
    },
    "filter": {
      "bool": {
        "must_not": {
          "ids": {
            "values": ["2"]
          }
        }
      }
    }
  }
}
```

## Filter kNN results [knn-search-filter-example]

Use a filter when you want the most similar results, but only from a specific subset of your data. For example, you might search for similar products in one category, documents from a certain time period, or images with a particular file type.

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

### Put the filter where the kNN search can see it [knn-prefilter-vs-postfilter]

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

### Filtering behavior and performance [filtering-behavior-and-performance]

In approximate kNN search with an HNSW index, filters can make a search slower rather than faster, because the search has to explore more of the graph to collect enough candidates that satisfy the filter. This is the opposite of conventional query filtering, where a stricter filter usually speeds up a query.

To limit the impact, Lucene falls back to brute force per segment in two cases:

* If the number of documents matching the filter in a segment is no greater than the number of candidates the search would examine there, the search skips the HNSW graph and scores the filtered documents directly.
* While exploring the graph, if the search visits more nodes than there are documents matching the filter, it stops traversing and scores the filtered documents directly.

{applies_to}`stack: preview 9.1` For indices created in 9.1 or later, {{es}} also applies the `acorn` filter heuristic by default, which traverses only vectors that match the filter instead of comparing every vector it visits. This is generally faster at comparable recall, although you might need to raise `num_candidates` to hit exceptionally high recall targets. To change the heuristic, use [`index.dense_vector.hnsw_filter_heuristic`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-dense-vector-hnsw-filter-heuristic).

For more ways to trade search speed against accuracy, refer to [Optimize performance and accuracy](optimize-performance-accuracy.md).

## Set a similarity threshold [knn-similarity-search]

kNN always tries to return `k` nearest neighbors, even when none of them are close. Combined with a `filter`, this means you can filter away every relevant document and still receive `k` hits, drawn from whatever distant vectors remain.

Use the `similarity` parameter to set a threshold that a vector must meet to be considered a match. The `knn` search flow with this parameter is:

* Apply any user-provided `filter` queries.
* Explore the vector space to gather `k` candidates.
* Discard candidates that don't meet the `similarity` threshold.

Because the threshold is applied last, a search can return fewer than `k` hits, which is the point of the parameter.

What the threshold means depends on the [similarity](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-similarity) configured on the field:

* `l2_norm`: a **maximum distance**. Matches are the vectors that fall within a `dims`-dimensional hypersphere of radius `similarity`, centered on `query_vector`. Lower values are stricter.
* `cosine`, `dot_product`, and `max_inner_product`: a **minimum similarity**. Higher values are stricter.

::::{note}
`similarity` is the true similarity value **before** it is transformed into `_score` and before any boosts are applied.
::::

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

## Combine approximate kNN with keyword search [combine_approximate_knn_with_other_features]

Use hybrid retrieval when you want one ranked result list that reflects both how similar documents are to your query vector and how well they match specific words or phrases. For example, you might find images that look similar to a reference photo while also matching a title keyword like "mountain lake".

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

For more on hybrid search, including approaches that use `semantic_text` fields and ES|QL, refer to [Hybrid search](../../hybrid-search.md).

## Search multiple vector fields [_search_multiple_knn_fields]

Search multiple vector fields when your documents store more than one vector representation and you want to rank results by similarity across all of them in a single request. For example, you might search an image embedding and a title embedding together to surface documents that are both visually and semantically relevant.

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

As with hybrid retrieval, you can instead pass one `knn` retriever per field to an `rrf` or `linear` retriever, which spares you from balancing raw scores across fields. Refer to [Combine approximate kNN with keyword search](#combine_approximate_knn_with_other_features).

## Aggregate over kNN results [knn-aggregations]

You can use [aggregations](../../../../explore-analyze/query-filter/aggregations.md) with the `knn` option, but the buckets cover a different document set than you might expect. {{es}} computes aggregations over the documents that match the search, and for approximate kNN that means the top `k` nearest documents rather than everything in the index. If the request also includes a `query`, aggregations cover the combined set of `knn` and `query` matches.

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

- [Approximate kNN search](approximate-knn.md): Learn how to map, index, and query `dense_vector` fields for fast, scalable approximate kNN search.
- [Nested kNN search](nested-knn-search.md): Learn how to run approximate kNN search on nested vectors for passage retrieval, filtering, inner hits, and chunked content.
- [Optimize performance and accuracy](optimize-performance-accuracy.md): Learn how to tune search speed, recall, vector storage, quantization, and rescoring for approximate kNN search.
- [Exact kNN search](exact-knn.md): Learn how to run exact brute-force kNN search for small datasets or precise scoring.
- [Hybrid search](../../hybrid-search.md): Compare the approaches for combining full-text and vector search in a single request.
- [Retrievers](../../retrievers-overview.md): Learn what retrievers are, which types exist, and how to compose them into ranking pipelines.
- [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md): API reference for the `knn` query, including parameters, `query_vector_builder` options, and usage with `dense_vector` and `semantic_text` fields.
