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
navigation_title: Elasticsearch solution
---

# {{es}} solution & project type overview

::::{tip}
Not sure which deployment type is right for you? Use the following resources to help you decide:

- Read the Elastic [deployment types overview](/deploy-manage/deploy.md)
- Compare [serverless and {{ech}}](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md)
  - Compare pricing models between [Elastic Cloud](/deploy-manage/cloud-organization/billing/cloud-hosted-deployment-billing-dimensions.md) and [Serverless](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md)
::::


The {{es}} solution and serverless project type provide specialized UI tools and interfaces that help you build search applications on top of the {{es}} platform.

These UI affordances are exclusive to the {{es}} **solution** (on non-serverless deployments) and the {{es}} serverless **project type**. They complement the core [search primitives](/solutions/search.md) available across all Elastic deployments.

## Features and tools

The {{es}} solution provides the following specialized UI tools:

### Agent Builder

[Agent Builder](/solutions/elasticsearch-solution-project/elastic-agent-builder.md) enables you to create AI agents that can interact with your {{es}} data, execute queries, and provide intelligent responses. It provides a complete framework for building conversational AI experiences on top of your search infrastructure.

### Playground

[Playground](/solutions/elasticsearch-solution-project/playground.md) lets you use large language models (LLMs) to understand, explore, and analyze your {{es}} data using retrieval augmented generation (RAG), via a chat interface. Playground is also useful for testing and debugging your {{es}} queries using the [retrievers](/solutions/search/retrievers-overview.md) syntax.

### Search Applications

[Search Applications](/solutions/elasticsearch-solution-project/search-applications.md) provide a simplified way to manage and access your search use cases through a unified interface. They enable you to create, configure, and manage search-powered applications with built-in templates and best practices.

### Synonyms UI

The [Search with synonyms](/solutions/search/full-text/search-with-synonyms.md) interface provides a dedicated UI for managing synonym sets directly within {{kib}}, making it easier to improve search relevance without editing configuration files.

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