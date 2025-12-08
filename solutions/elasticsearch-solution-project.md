---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/what-is-elasticsearch-serverless.html
  - https://www.elastic.co/guide/en/kibana/current/search-space.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: kibana
navigation_title: Elasticsearch
---

# {{es}} solution overview

The {{es}} solution and serverless project type provide specialized UI tools and interfaces that help you build search applications on top of the {{es}} platform.

These UI affordances are exclusive to the {{es}} solution (on {{ech}}) and the {{es}} serverless project type. They complement the universal search capabilities available across all {{es}} deployments.

::::{tip}
Looking for general search capabilities that work across all {{es}} deployments? Check out the [Search use case](/solutions/search.md) documentation, which covers universal {{es}} search primitives including full-text search, vector search, semantic search, and hybrid search.
::::

## Features and tools

The {{es}} solution provides the following specialized UI tools:

### Agent Builder

[Agent Builder](/solutions/elasticsearch-solution-project/elastic-agent-builder.md) enables you to create AI agents that can interact with your {{es}} data, execute queries, and provide intelligent responses. It provides a complete framework for building conversational AI experiences on top of your search infrastructure.

### Playground

[Playground](/solutions/elasticsearch-solution-project/playground.md) lets you use large language models (LLMs) to understand, explore, and analyze your {{es}} data using retrieval augmented generation (RAG), via a chat interface. Playground is also useful for testing and debugging your {{es}} queries using the [retrievers](/solutions/search/retrievers-overview.md) syntax.

### Search Applications

[Search Applications](/solutions/elasticsearch-solution-project/search-applications.md) provide a simplified way to manage and access your search use cases through a unified interface. They enable you to create, configure, and manage search-powered applications with built-in templates and best practices.

### Synonyms UI

The [Search with synonyms](/solutions/elasticsearch-solution-project/full-text/search-with-synonyms.md) interface provides a dedicated UI for managing synonym sets directly within {{kib}}, making it easier to improve search relevance without editing configuration files.

### Query Rules UI

[Query Rules UI](/solutions/elasticsearch-solution-project/query-rules-ui.md) enables you to create and manage query rules that modify search behavior based on specific conditions, helping you deliver more relevant results for common queries.

### AI Assistant

The [AI Assistant](/solutions/elasticsearch-solution-project/ai-assistant.md) provides intelligent assistance and insights across the Elastic platform, helping you understand your data and workflows more effectively.

### Model Context Protocol (MCP)

The [Model Context Protocol (MCP)](/solutions/elasticsearch-solution-project/mcp.md) lets you connect AI agents and assistants to your {{es}} data to enable natural language interactions with your indices.

## Get started

Ready to start using the {{es}} solution? Refer to [Get started](/solutions/elasticsearch-solution-project/get-started.md) for setup instructions and quickstart guides.

For a deeper understanding of search concepts and techniques, refer to the [Search use case](/solutions/search.md) documentation.

## Related reference

* [{{es}} reference documentation](elasticsearch://reference/elasticsearch/index.md)
* [Content connectors](elasticsearch://reference/search-connectors/index.md)
* [{{es}} API documentation]({{es-apis}})
* [Search use case documentation](/solutions/search.md)

::::{tip}
Not sure whether {{es}} on {{serverless-full}} is the right deployment choice for you?

Check out the following resources to help you decide:

- [What's different?](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md): Understand the differences between {{serverless-full}} and other deployment types.
- [Billing](/deploy-manage/cloud-organization/billing/elasticsearch-billing-dimensions.md): Learn about the billing model for {{es}} on {{serverless-full}}.
::::
