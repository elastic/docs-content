---
mapped_urls:
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-dev-tools.html
  - https://www.elastic.co/guide/en/enterprise-search/current/search-ui.html
applies_to:
  stack:
  serverless:
---

# APIs and tools

This page is handy list of the most important APIs and tools you need to build, test, and manage your search app built with {{es}}.

## API endpoints

### Query & search APIs

| Endpoint | Function |
|----------|----------|
| [`_search`](https://www.elastic.co/docs/api/doc/elasticsearch/v8/group/endpoint-search) | Searches and aggregations written in [Query DSL](/explore-analyze/query-filter/languages/querydsl.md) and [retrievers](retrievers-overview.md) syntax |
| [`_query`](https://www.elastic.co/docs/api/doc/elasticsearch/v8/group/endpoint-esql)| Endpoint for [{{esql}}](/explore-analyze/query-filter/languages/esql.md) queries |
| [`_explain`](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-explain) | Provides detailed explanation of how a specific document matches a query with scoring breakdown |
| [`_count`](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-count) | Returns count of documents matching a query without retrieving results |
| [`_validate/query`](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-indices-validate-query) | Validates query syntax without executing the search |
| [`_analyze`](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-analyze.html) | Performs analysis for [full-text search](./full-text.md) on a text string and returns the resulting tokens. |

### Ingestion & mapping APIs

| Endpoint | Function |
|----------|----------|
| [`_mapping`](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-indices-get-field-mapping) | Retrieves or updates field mappings with options for specific field inspection |
| [`_reindex`](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-reindex) | Copies documents from one index to another, useful for mapping changes |
| [`_update_by_query`](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-update-by-query) | Updates documents matching a query without reindexing |
| [`_bulk`](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-bulk-1) | Performs multiple index/update/delete operations in a single request |
| [`_refresh`](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-indices-refresh-3) | Forces a refresh to make recent operations searchable |
| [`_ingest/pipeline`](https://www.elastic.co/docs/api/doc/elasticsearch/v8/group/endpoint-ingest) | Creates and manages document processing pipelines before indexing |

### Search optimization APIs

| Endpoint | Function |
|----------|----------|
| [`_rank_eval`](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-rank-eval)| Evaluates search quality against known relevant documents |
| [`_settings`](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-indices-get-settings-1) | Configures settings including slow logs, refresh intervals, and replicas (only index-level settings available in serverless) |
| [`_scripts`](https://www.elastic.co/docs/api/doc/elasticsearch/v8/group/endpoint-script) | Creates or updates stored scripts for reuse in queries and aggregations |


## UI tools [elasticsearch-dev-tools]

### Dev tools

Access these specialized tools in Kibana and the Serverless UI to develop, debug, and refine your search queries while monitoring their performance and efficiency.

These tools are documented in the **Explore & Analyze** section:

| Tool | Function |
|------|----------|
| [Saved queries](/explore-analyze/query-filter/tools/saved-queries.md) | Save your searches and queries to reuse them later. |
| [Console](/explore-analyze/query-filter/tools/console.md) | Interact with the REST APIs of {{es}} and {{kib}}, including sending requests and viewing API documentation. |
| [{{searchprofiler}}](/explore-analyze/query-filter/tools/search-profiler.md) | Inspect and analyze your search queries. |
| [Grok Debugger](/explore-analyze/query-filter/tools/grok-debugger.md) | Build and debug grok patterns before you use them in your data processing pipelines. |
| [Painless Lab](/explore-analyze/scripting/painless-lab.md) | Test and debug Painless scripts in real-time. |

### Playground

Use [Playground](rag/playground.md) to combine your {{es}} data with the power of large language models (LLMs) for retrieval augmented generation (RAG), using a chat interface. Playground is also very useful for testing and debugging your {{es}} queries, using the [retrievers](retrievers-overview.md) syntax with the `_search` endpoint.

### Search UI

[Elastic Search UI](./site-or-app/search-ui.md) is a library of JavaScript and React tools for building search experiences, optimized for use with {{es}}.

:::{tip}
Check out the Elasticsearch Labs [blog](https://www.elastic.co/search-labs) to learn how to use Elastic to build advanced search experiences including generative AI, embedding models, reranking capabilities and more.

The accompanying [GitHub repository](https://www.github.com/elastic/elasticsearch-labs) contains hands-on Python notebooks and sample apps to help you get started with these advanced search features.
:::