---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-dev-tools.html
  - https://www.elastic.co/guide/en/enterprise-search/current/search-ui.html
applies_to:
  stack:
  serverless:
products:
  - id: cloud-serverless
---

# APIs and tools

This page is handy list of the most important APIs and tools you need to build, test, and manage your search app built with {{es}}.

## API endpoints

### Query & search APIs

| Endpoint | Function |
|----------|----------|
| [`_search`]({{es-apis}}group/endpoint-search) | Searches and aggregations written in [Query DSL](/explore-analyze/query-filter/languages/querydsl.md) and [retrievers](retrievers-overview.md) syntax |
| [`_query`]({{es-apis}}group/endpoint-esql)| Endpoint for [{{esql}}](elasticsearch://reference/query-languages/esql.md) queries |
| [`_explain`]({{es-apis}}operation/operation-explain) | Provides detailed explanation of how a specific document matches a query with scoring breakdown |
| [`_count`]({{es-apis}}operation/operation-count) | Returns count of documents matching a query without retrieving results |
| [`_validate/query`]({{es-apis}}operation/operation-indices-validate-query) | Validates query syntax without executing the search |
| [`_analyze`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-analyze) | Performs analysis for [full-text search](./full-text.md) on a text string and returns the resulting tokens. |

### Ingestion & mapping APIs

| Endpoint | Function |
|----------|----------|
| [`_mapping`]({{es-apis}}operation/operation-indices-get-field-mapping) | Retrieves or updates field mappings with options for specific field inspection |
| [`_reindex`]({{es-apis}}operation/operation-reindex) | Copies documents from one index to another, useful for mapping changes |
| [`_update_by_query`]({{es-apis}}operation/operation-update-by-query) | Updates documents matching a query without reindexing |
| [`_bulk`]({{es-apis}}operation/operation-bulk) | Performs multiple index/update/delete operations in a single request |
| [`_refresh`]({{es-apis}}operation/operation-indices-refresh) | Forces a refresh to make recent operations searchable |
| [`_ingest/pipeline`]({{es-apis}}group/endpoint-ingest) | Creates and manages document processing pipelines before indexing |

### Search optimization APIs

| Endpoint | Function |
|----------|----------|
| [`_rank_eval`]({{es-apis}}operation/operation-rank-eval)| Evaluates search quality against known relevant documents |
| [`_settings`]({{es-apis}}operation/operation-indices-get-settings) | Configures settings including slow logs, refresh intervals, and replicas (only index-level settings available in serverless) |
| [`_scripts`]({{es-apis}}group/endpoint-script) | Creates or updates stored scripts for reuse in queries and aggregations |


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

### Search UI

[Elastic Search UI](./site-or-app/search-ui.md) is a library of JavaScript and React tools for building search experiences, optimized for use with {{es}}.

:::{tip}
Check out the Elasticsearch Labs [blog](https://www.elastic.co/search-labs) to learn how to use Elastic to build advanced search experiences including generative AI, embedding models, reranking capabilities and more.

The accompanying [GitHub repository](https://www.github.com/elastic/elasticsearch-labs) contains hands-on Python notebooks and sample apps to help you get started with these advanced search features.
:::

## Generative AI tools

The following generative AI tools are available as part of the {{es}} solution and serverless project type. They enable you to build AI-powered search applications on top of the core {{es}} features, including retrieval augmented generation (RAG) systems and agentic workflows.

### Agent Builder

[Agent Builder](/solutions/elasticsearch-solution-project/elastic-agent-builder.md) enables you to create AI agents that can interact with your {{es}} data, execute queries, and provide intelligent responses. It provides a complete framework for building conversational AI experiences on top of your search infrastructure.

### Playground

[Playground](/solutions/elasticsearch-solution-project/playground.md) enables you to use large language models (LLMs) to understand, explore, and analyze your {{es}} data using retrieval augmented generation (RAG), via a chat interface. Playground is also useful for testing and debugging your {{es}} queries using the [retrievers](retrievers-overview.md) syntax with the `_search` endpoint.

### Model Context Protocol (MCP)

The [Model Context Protocol (MCP)](/solutions/elasticsearch-solution-project/mcp.md) lets you connect AI agents and assistants to your {{es}} data to enable natural language interactions with your indices.

Refer to the [{{es}} solution documentation](/solutions/elasticsearch-solution-project.md) for more information about these UI tools.