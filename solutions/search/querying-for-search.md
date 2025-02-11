---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-your-data.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-search-your-data.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-search-your-data-the-search-api.html
navigation_title: Build search queries
---

# Build your search queries

::::{tip} 
This page is focused on the search use case. For an overview of Elastic query languages for every use case, refer to the [complete overview](/explore-analyze/query-filter/languages.md).
::::

Once you know which [search approaches](search-approaches.md) you need to use, you can start building and testing your search queries. {{es}} provides several query languages to help you express your search logic.

| Interface | Endpoint | Description | Best for |
|-----------|----------|-------------|----------|
| [**Query DSL**](/explore-analyze/query-filter/languages/querydsl.md) | [`_search`](the-search-api.md) | Original, JSON-based query language native to Elasticsearch. Powerful but complex syntax. | Full-text and semantic search queries |
| [**ESQL**](/explore-analyze/query-filter/languages/esql.md) | `_query` | Fast, SQL-like language with piped syntax, built on new compute architecture. | Filtering, analysis, aggregations |
| [**Retrievers**](retrievers-overview.md) | `_search` | Modern `_search` API syntax focused on composability. | Building complex search pipelines, especially those using semantic search. Required for [semantic reranking](ranking/semantic-reranking.md). |

These query languages are complementary, not mutually exclusive. You can use different query languages for different parts of your application, based on your specific needs. This flexibility allows you to gradually adopt newer interfaces as your requirements evolve.

::::{note} 
You can use the [{{es}} REST APIs](https://www.elastic.co/docs/api/doc/elasticsearch) to search your data using any HTTP client, including the [{{es}} client libraries](site-or-app/clients.md), or directly in [Console](https://www.elastic.co/guide/en/serverless/current/devtools-run-api-requests-in-the-console.html). You can also run searches using [Discover](/explore-analyze/discover.md) in the UI.
::::


::::{tip} 
Try our hands-on [quick start tutorials](api-quickstarts.md) in the core {{es}} documentation to get started, or check out our [Python notebooks](https://github.com/elastic/elasticsearch-labs/tree/main/notebooks#readme).
::::