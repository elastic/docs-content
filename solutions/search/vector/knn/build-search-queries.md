---
navigation_title: Build search queries
description: Construct approximate kNN queries in Elasticsearch for filtering, hybrid retrieval, semantic search, multiple vector fields, and similarity thresholds.
applies_to:
  stack:
  serverless:
---

# Build approximate kNN search queries [build-approximate-knn-queries]

This page shows how to construct approximate kNN queries for common retrieval patterns, including filtering, hybrid retrieval, semantic search, multiple vector fields, and similarity thresholds. 


## Perform semantic search [knn-semantic-search]

:::{tip}
Looking for a minimal configuration approach? The `semantic_text` field type abstracts these vector search implementations with sensible defaults and automatic model management. It's the recommended approach for most users. [Learn more about semantic_text](../../semantic-search/semantic-search-semantic-text.md).
:::

kNN search enables you to perform semantic search by using a previously deployed [text embedding model](../../../../explore-analyze/machine-learning/nlp/ml-nlp-search-compare.md#ml-nlp-text-embedding). Instead of literal matching on search terms, semantic search retrieves results based on the intent and the contextual meaning of a search query.

Under the hood, the text embedding NLP model converts your input query string (provided as `model_text`) into a dense vector. The query vector is compared against an index containing dense vectors created with the same text embedding {{ml}} model. The search results are semantically similar as learned by the model.

To perform semantic search:

- You need an index that contains dense vector representations of the input data to search against.
- You must use the same text embedding model for search that you used to create the document vectors.
- The text embedding NLP model deployment must be started.

Reference the deployed text embedding model or the model deployment in the `query_vector_builder` object, and provide the search string as `model_text`:

```js
(...)
{
  "knn": {
    "field": "dense-vector-field",
    "k": 10,
    "num_candidates": 100,
    "query_vector_builder": {
      "text_embedding": { <1>
        "model_id": "my-text-embedding-model", <2>
        "model_text": "The opposite of blue" <3>
      }
    }
  }
}
(...)
```

1. The task to perform. In this case, it is `text_embedding`.
2. The ID of the text embedding model used to generate the query’s dense vector. Use the same model that produced the document embeddings in the target index. You can also provide the `deployment_id` as the `model_id` value.
3. The query string from which the model generates the dense vector representation.

:::{tip}
For an overview of `query_vector_builder` options (`text_embedding`, `embedding`, and `lookup`), refer to [Build query vectors for knn search](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md#build-query-vectors-for-knn-search).
:::


For more information on how to deploy a trained model and use it to create text embeddings, refer to this [end-to-end example](../../../../explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md).

## Combine approximate kNN with keyword search [combine_approximate_knn_with_other_features]

Use hybrid retrieval when you want one ranked result list that reflects both how similar documents are to your query vector and how well they match specific words or phrases. For example, you might find images that look similar to a reference photo while also matching a title keyword like "mountain lake".

You can perform hybrid retrieval by combining the [`knn` option]({{es-apis}}operation/operation-search#operation-search-body-application-json-knn) with a standard [`query`]({{es-apis}}operation/operation-search#operation-search-query). This blends vector similarity with lexical relevance, filters, and aggregations.

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

This search finds the global top `k = 5` vector matches, combines them with the matches from the `match` query, and finally returns the 10 top-scoring results. The `knn` and `query` matches are combined through a disjunction, as if you took a boolean *or* between them. The top `k` vector results represent the global nearest neighbors across all index shards.

The score of each result is the sum of the `knn` and `query` scores. You can specify a `boost` value to give a weight to each score in the sum. In the preceding example, the scores will be calculated as

```
score = 0.9 * match_score + 0.1 * knn_score
```

The `knn` option can also be used with [`aggregations`](../../../../explore-analyze/query-filter/aggregations.md). In general, {{es}} computes aggregations over all documents that match the search. So for approximate kNN search, aggregations are calculated on the top `k` nearest documents. If the search also includes a `query`, then aggregations are calculated on the combined set of `knn` and `query` matches.

## Filtered kNN search [knn-search-filter-example]

Use filtered kNN search when you want the most similar results, but only from a specific subset of your data. For example, you might search for similar products in one category, documents from a certain time period, or images with a particular file type.

The kNN search API supports restricting vector similarity search with a filter. The request returns the top `k` nearest neighbors that also satisfy the filter query, enabling targeted, pre-filtered approximate kNN in {{es}}.

The following request performs an approximate kNN search filtered by the `file-type` field:

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

### Filtering behavior and performance [filtering-behavior-and-performance]

In approximate kNN search with an HNSW index, applying filters can decrease performance as the engine must explore more of the graph to gather enough candidates that satisfy the filter and reach `num_candidates`. This contrasts with conventional query filtering, where stricter filters often speed up queries.

To avoid significant performance drawbacks, Lucene implements the following strategies per segment:

* If the filtered document count is less than or equal to num_candidates, the search bypasses the HNSW graph and uses a brute force search on the filtered documents.
* While exploring the HNSW graph, if the number of nodes explored exceeds the number of documents that satisfy the filter, the search will stop exploring the graph and switch to a brute force search over the filtered documents.

## Search multiple kNN fields [_search_multiple_knn_fields]

Use multiple kNN fields when your documents store more than one vector representation and you want to rank results by similarity across all of them in a single request. For example, you might search an image embedding and a title embedding together to surface documents that are both visually and semantically relevant.

In addition to *hybrid retrieval*, you can search more than one kNN vector field in a single request:

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
    "num_candidates": 10,
    "boost": 0.5
  }],
  "size": 10
}
```

This search retrieves the global top `k = 5` neighbors for `image-vector` and the global top `k = 10` for `title-vector`. These vector result sets are combined with the matches from the `match` query, and the top 10 overall documents are returned. Multiple `knn` clauses and the `query` clause are combined via a disjunction (boolean *OR*). The top `k` vector results represent the global nearest neighbors across all index shards.

The scoring for a document with the above configured boosts would be:

```
score = 0.9 * match_score + 0.1 * knn_score_image-vector + 0.5 * knn_score_title-vector
```

## Search kNN with expected similarity [knn-similarity-search]

While kNN is a powerful tool, it always tries to return `k` nearest neighbors. Consequently, when using `knn` with a `filter`, you could filter out all relevant documents and only have irrelevant ones left to search. In that situation, `knn` will still do its best to return `k` nearest neighbors, even though those neighbors could be far away in the vector space.

To control this, use the `similarity` parameter in the `knn` clause. This sets a minimum similarity threshold a vector must meet to be considered a match. The `knn` search flow with this parameter is:

* Apply any user-provided `filter` queries.
* Explore the vector space to gather `k` candidates.
* Exclude any vectors with similarity below the configured `similarity` threshold.

::::{note}
`similarity` is the true [similarity](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-similarity) value **before** it is transformed into `_score` and before any boosts are applied.
::::

For each configured [similarity](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-similarity), the following shows how to invert `_score` back to the underlying similarity. Use these when you want to filter based on `_score`:

* `l2_norm`: `sqrt((1 / _score) - 1)`
* `cosine`: `(2 * _score) - 1`
* `dot_product`: `(2 * _score) - 1`
* `max_inner_product`:
  * `_score < 1`: `1 - (1 / _score)`
  * `_score >= 1`: `_score - 1`

Example: the query searches for the given `query_vector`, with a `filter` applied, and requires that matches meet or exceed the specified `similarity` threshold. Results below the threshold are not returned, even if fewer than `k` neighbors remain.

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

In this data set, the only document with `file-type = png` has the vector `[42, 8, -15]`. The `l2_norm` distance between `[42, 8, -15]` and `[1, 5, -20]` is `41.412`, which exceeds the configured `similarity` threshold of `36`. As a result, this search returns no hits.

## Resources

- [Approximate kNN search](approximate-knn.md): Learn how to map, index, and run a basic approximate kNN search, including indexing considerations and limitations.
- [Nested kNN search](nested-knn-search.md): Learn how to run approximate kNN search on nested vectors for passage retrieval, filtering, inner hits, and chunked content.
- [Optimize performance and accuracy](optimize-performance-accuracy.md): Learn how to tune search speed, recall, vector storage, quantization, and rescoring for approximate kNN search.
- [kNN search on {{es}}](../knn.md): Explore common use cases, prerequisites for kNN search, and a comparison of approximate and exact kNN methods.
- [Exact kNN search](exact-knn.md): Learn how to run exact brute-force kNN search with `script_score` queries for small datasets or precise scoring.
- [Hybrid search with `semantic_text`](../../hybrid-semantic-text.md): Follow a step-by-step tutorial for combining lexical and semantic search with reciprocal rank fusion.
- [Vector search in {{es}}](../../vector.md): Learn the core concepts and terminology for vector search in {{es}}, including embeddings, field types, and how vector retrieval fits with other search strategies.
- [Knn query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md): API reference for the `knn` query, including parameters, `query_vector_builder` options, and usage with `dense_vector` and `semantic_text` fields.
