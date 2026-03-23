---
navigation_title: Choose a strategy
description: Compare full-text search, semantic search, hybrid search, and reranking to decide which approach fits your use case.
applies_to:
  stack: ga
  serverless:
    elasticsearch: ga
---

# Choose a retrieval strategy

Elasticsearch supports several retrieval strategies. This page helps you understand the differences and choose the right approach for your use case.

The main approaches are:

- **Full-text search**: keyword and lexical matching using BM25
- **Semantic search**: meaning-based matching using vector embeddings
- **Hybrid search**: BM25 and semantic search combined
- **Reranking**: a second-pass scoring step applied on top of retrieval results

## Full-text search [full-text]

Full-text search uses BM25 to match documents based on the terms in the query.

Use full-text search when:

- Queries use specific terms, product names, identifiers, or codes that should match exactly
- Your corpus is structured or semi-structured, such as documentation, product catalogs, or support tickets
- You need predictable, explainable relevance scores

Full-text search might not perform well when users express the same idea in many different ways, or when queries are conversational and meaning matters more than term overlap.

For more information, refer to [Full-text search](/solutions/search/full-text.md).

## Semantic search [semantic]

Semantic search uses vector embeddings to match documents based on meaning rather than exact terms. Documents and queries are converted to vectors, and retrieval finds the nearest vectors in that space.

Use semantic search when:

- Queries are conversational or use natural language phrasing
- Your corpus covers the same topics using varied vocabulary
- You want to match across languages without a translation layer
- You are building a RAG pipeline that needs conceptually relevant context

Semantic search requires generating embeddings at index time and query time, which adds memory and inference costs compared to full-text search. It can also perform poorly for queries that depend on exact-match precision, such as specific product codes or usernames.

For more information, refer to [Semantic search](/solutions/search/semantic-search.md).

## Hybrid search [hybrid]

Hybrid search runs BM25 and semantic retrieval in parallel and combines their results. The most common combination method is Reciprocal Rank Fusion (RRF), which merges ranked results from both retrievers without requiring score normalization.

Use hybrid search when:

- Your query mix includes both keyword-heavy and conversational queries
- You want the precision of BM25 alongside the recall of semantic search
- Either approach alone is missing relevant results for some queries

Hybrid search runs two retrievers per query. For high-throughput applications, test the combined query latency against your requirements before adopting it.

For more information, refer to [Hybrid search](/solutions/search/hybrid-search.md).

## Reranking [reranking]

Reranking is a second-pass step applied after initial retrieval. A cross-encoder model scores each retrieved document against the query, producing more precise relevance scores than the initial retrieval step. Reranking is always combined with an upstream retriever.

Use reranking when:

- You retrieve a larger candidate set and want to return only the most relevant top-k results
- You need higher relevance precision than retrieval alone provides
- You are building a RAG pipeline and the quality of the context window matters

Reranking adds per-query inference latency on top of the retrieval step.

For more information, refer to [Semantic reranking](/solutions/search/ranking/semantic-reranking.md).

## Comparison [comparison]

| Situation | Recommended approach |
|---|---|
| Queries use specific terms, identifiers, or codes | Full-text |
| Queries are conversational or use natural language | Semantic |
| Mixed query types in the same application | Hybrid |
| You need both exact-match precision and semantic recall | Hybrid |
| You want higher precision over a retrieved candidate set | Add reranking |
| Multilingual corpus, no translation layer | Semantic |

## Resource considerations [resources]

The approaches have different infrastructure requirements.

**Full-text search** runs on CPU with no embedding model or per-query inference overhead.

**Semantic search** requires generating embeddings at index time and query time. Dense vector fields consume memory proportional to the number of documents and vector dimensions.

**Hybrid search** runs both retrievers per query. Latency is roughly the maximum of the two retrievers, since they run in parallel.

**Reranking** adds a cross-encoder inference step on top of retrieval and increases per-query latency.

:::{tip}
If you are unsure which approach to use, start with full-text search or the `semantic_text` workflow. You can add hybrid search or reranking incrementally once you have measured where the simpler approach falls short.
:::

## Next steps [next-steps]

- [Semantic search overview](/solutions/search/semantic-search.md)
- [Hybrid search](/solutions/search/hybrid-search.md)
- [Semantic reranking](/solutions/search/ranking/semantic-reranking.md)
- [Retrievers overview](/solutions/search/retrievers-overview.md)
