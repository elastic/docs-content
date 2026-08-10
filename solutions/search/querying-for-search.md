---
navigation_title: Build search queries
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/8.18/search-with-elasticsearch.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-your-data.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-search-your-data.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-search-your-data-the-search-api.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Build your search queries

::::{tip}
This page is focused on the search use case. For an overview of Elastic query languages for every use case, refer to the [complete overview](/explore-analyze/query-filter/languages.md).
::::

Once you know which [search approaches](search-approaches.md) you need to use, you can start building and testing your search queries. {{es}} provides several query interfaces to help you express your search logic.

| Interface | Endpoint | Description |
|-----------|----------|-------------|
| [**Query DSL**](/explore-analyze/query-filter/languages/querydsl.md) | [`_search`](the-search-api.md) | Original, JSON-based query language native to {{es}}. Expressive and well-supported across all client libraries. |
| [**Retrievers**](retrievers-overview.md) | [`_search`](the-search-api.md) | Composable `_search` API syntax for building multi-stage retrieval pipelines in a single request. Built on top of Query DSL. |
| [**ES\|QL**](esql-for-search.md) | `_query` | Piped query language with SQL-like syntax, built on a new compute architecture. Supports full-text search, semantic search, hybrid search, reranking, and text generation. |

These query interfaces are complementary, not mutually exclusive. You can use different interfaces for different parts of your application, based on your specific needs. This flexibility allows you to gradually adopt newer interfaces as your requirements evolve.

## Choosing the right interface

Use the following guidance to decide which interface best fits your use case.

### Query DSL

Choose [Query DSL](/explore-analyze/query-filter/languages/querydsl.md) when you need:

- Fine-grained control over individual query clauses, scoring, and boosting
- The widest ecosystem support: all {{es}} clients, tools, and integrations work with Query DSL
- A single-stage query like a `match`, `bool`, or `term` query without multi-stage retrieval

Query DSL is the foundational query language and remains the right choice for straightforward search queries, especially when you're using a single retrieval strategy.

### Retrievers

Choose [retrievers](retrievers-overview.md) when you need to:

- Compose multi-stage retrieval pipelines in a single `_search` call (for example, retrieve, rerank, diversify)
- Combine multiple retrieval strategies using RRF or linear combination
- Apply semantic reranking with the `text_similarity_reranker` retriever
- Use the [multi-field query format](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md#multi-field-query-format) for simple hybrid search across lexical and semantic fields with automatic score normalization

Retrievers wrap Query DSL and add composability. If your search involves multiple retrieval stages, such as combining BM25 with vector search or adding a reranking step, retrievers let you express the entire pipeline declaratively.

### ES|QL

Choose [ES|QL](esql-for-search.md) when you need to:

- Build end-to-end search queries using piped syntax, including hybrid search with `FORK`/`FUSE`, reranking with `RERANK`, and text generation with `COMPLETION`
- Combine search with aggregations, stats, or other data transformations in a single query
- Explore data interactively using a familiar SQL-like syntax in Kibana or the API

ES|QL is a good fit when your workflow extends beyond retrieval. For example, you can search, rerank, and summarize results in a single piped query.

### Feature comparison

The following table summarizes which capabilities are available in each interface.

| Capability | Query DSL | Retrievers | ES\|QL |
|------------|:---------:|:----------:|:------:|
| Full-text search (BM25) | Yes | Yes | Yes |
| Semantic / vector search | Yes | Yes | Yes |
| Hybrid search (score combination) | - | Yes (RRF, linear) | Yes (FORK/FUSE) |
| Semantic reranking | - | Yes (`text_similarity_reranker`) | Yes (`RERANK`) |
| Result diversification (MMR) | - | Yes (`diversify`) | Yes (`MMR`) |
| Multi-field query format | - | Yes | - |
| Aggregations | Yes | Yes | Yes |
| Text generation (LLM) | - | - | Yes (`COMPLETION`) |
| Piped transformations | - | - | Yes |

::::{note}
You can use the [{{es}} REST APIs]({{es-apis}}) to search your data using any HTTP client, including the [{{es}} client libraries](site-or-app/clients.md), or directly in [Console](/explore-analyze/query-filter/tools/console.md). You can also run searches using [Discover](/explore-analyze/discover.md) in the UI.
::::

::::{tip}
Try our hands-on [quickstart guides](/solutions/search/get-started/quickstarts.md) to get started, or check out our [Python notebooks](https://github.com/elastic/elasticsearch-labs/tree/main/notebooks#readme).
::::
