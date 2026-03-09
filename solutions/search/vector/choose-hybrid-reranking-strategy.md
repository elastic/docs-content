---
navigation_title: Hybrid and reranking
description: Understand when to use hybrid search, how to choose between RRF and linear combination, and when to add semantic reranking or Learning to Rank on top of your retrieval pipeline.
applies_to:
  stack: ga
  serverless:
    elasticsearch: ga
---

# Choose a hybrid and reranking strategy

Elasticsearch supports several ways to combine and improve retrieval results. This page describes when to use each option and how they fit together in a retrieval pipeline.

The main options are:

- **Hybrid search**: combine BM25 and semantic retrieval results using RRF or linear combination
- **Semantic reranking**: reorder retrieved candidates using a cross-encoder model
- **Learning to Rank (LTR)**: reorder results using a trained ranking model

## When semantic search alone is sufficient [semantic-only]

If your queries are consistently conversational or natural language, and you are not seeing gaps in retrieval quality, semantic search alone may be sufficient. Adding hybrid or reranking steps increases query complexity and latency. Measure whether either approach improves results for your data before adding them.

## Hybrid search [hybrid]

Hybrid search combines BM25 (lexical) and semantic retrieval in parallel and merges the results. Use hybrid search when your query set includes both keyword-heavy queries and natural language queries, or when either retrieval method alone is missing relevant results.

### RRF vs. linear combination [rrf-vs-linear]

Elasticsearch supports two methods for combining results from multiple retrievers.

**Reciprocal Rank Fusion (RRF)** merges results based on rank position rather than score. It does not require score normalization across retrievers and works well without tuning. RRF is the recommended starting point for most hybrid search implementations.

**Linear combination** merges results using a weighted sum of the scores from each retriever. Scores from each retriever are normalized before combining. Use linear combination when you want explicit control over the relative weight of each retriever — for example, to give more weight to semantic results for some query types, or when you have data to support specific weight values.

If you are not sure which to use, start with RRF. The `rrf` retriever is available in the [Retrievers API](/solutions/search/retrievers-overview.md) and requires no per-query tuning.

For more information, refer to [Hybrid search](/solutions/search/hybrid-search.md).

## Semantic reranking [semantic-reranking]

Semantic reranking applies a cross-encoder model as a second pass over the top-k candidates returned by your retriever. The cross-encoder scores each document against the full query text, producing more precise relevance scores than the initial retrieval step.

Use semantic reranking when:

- Your retrieval step returns a good set of candidates but the ranking order needs improvement
- You are building a RAG pipeline and the quality of the top results passed to the LLM matters
- You want to add semantic relevance to an existing BM25 index without reindexing

Semantic reranking works with any upstream retriever — full-text, semantic, or hybrid. Because the cross-encoder only runs over a small top-k set, the additional latency is manageable at moderate query volumes.

In Elasticsearch, semantic reranking is implemented using the `text_similarity_reranker` retriever. This retriever wraps an upstream retriever and applies reranking to its results.

For more information, refer to [Semantic reranking](/solutions/search/ranking/semantic-reranking.md).

### Two-stage pipeline example [two-stage]

A typical two-stage pipeline looks like this:

1. **First stage**: an `rrf` retriever combines BM25 and semantic retrieval and returns the top-k candidates
2. **Second stage**: a `text_similarity_reranker` retriever reranks those candidates using a cross-encoder model

This pattern is available entirely through the retriever syntax in a single `_search` API call.

## Learning to Rank [ltr]

Learning to Rank (LTR) trains a ranking model on labeled query-document pairs and uses it to reorder results at query time. It supports a wider range of input features than semantic reranking, including custom signals such as recency, popularity, or business rules.

Use LTR when:

- You have a labeled dataset of query-document relevance judgments to train on
- You want to incorporate signals beyond semantic similarity — for example, click data, document age, or explicit relevance labels
- You have the infrastructure to maintain and retrain the model as your data or queries change

LTR requires more setup than semantic reranking. It is best suited for high-traffic search applications where relevance is critical and you have the data to support a training pipeline.

For more information, refer to [Learning to Rank](/solutions/search/ranking/learning-to-rank-ltr.md).

## The linear retriever [linear-retriever]

The `linear` retriever is a compound retriever that combines scores from multiple sub-retrievers using a weighted sum, with built-in score normalization. It is an alternative to RRF when you want score-based combination rather than rank-based combination.

The linear retriever is the recommended implementation approach when you choose linear combination over RRF.

For more information, refer to [Retrievers](/solutions/search/retrievers-overview.md).

## Comparison [comparison]

| Situation | Recommended approach |
|---|---|
| Queries are consistently conversational | Semantic search only |
| Mixed keyword and natural language queries | Hybrid with RRF |
| You want explicit control over retriever weights | Hybrid with linear combination |
| Retrieved candidates are good but ranking needs improvement | Add semantic reranking |
| You have labeled training data and custom ranking signals | Learning to Rank |
| You are building a RAG pipeline | Hybrid + semantic reranking |

## Next steps [next-steps]

- [Hybrid search](/solutions/search/hybrid-search.md)
- [Hybrid search with `semantic_text`](/solutions/search/hybrid-semantic-text.md)
- [Semantic reranking](/solutions/search/ranking/semantic-reranking.md)
- [Learning to Rank](/solutions/search/ranking/learning-to-rank-ltr.md)
- [Retrievers overview](/solutions/search/retrievers-overview.md)
