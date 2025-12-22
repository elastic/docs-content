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

# {{es}} solution overview

The {{es}} solution and serverless project type provide specialized UI tools that help you build search applications faster. The solution is an optional complement to the core {{es}} [search capabilities](/solutions/search.md) which are available through APIs across all deployment types, solutions, and project types.[^api-note]

These UI affordances are exclusive to the {{es}} solution (on non-serverless deployments) and the {{es}} serverless project type.

::::{tip}
Not sure which deployment type is right for you? Use the following resources to help you decide:

- Read the Elastic [deployment types overview](/deploy-manage/deploy.md)
- Compare [serverless and {{ech}}](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md)
  - Compare pricing models between [Elastic Cloud](/deploy-manage/cloud-organization/billing/cloud-hosted-deployment-billing-dimensions.md) and [Serverless](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md)
::::


## Features and tools

The {{es}} solution provides the following specialized UI tools and features to help you build search applications faster:

### Agent Builder

[Agent Builder](/solutions/search/elastic-agent-builder.md) enables you to create AI agents that can interact with your {{es}} data, execute queries, and provide intelligent responses. It provides a complete framework for building conversational AI experiences on top of your search infrastructure.

### Playground

[Playground](/solutions/elasticsearch-solution-project/playground.md) lets you use large language models (LLMs) to understand, explore, and analyze your {{es}} data using retrieval augmented generation (RAG), via a chat interface. Playground is also useful for testing and debugging your {{es}} queries using the [retrievers](/solutions/search/retrievers-overview.md) syntax.

### Synonyms UI

The [synonyms UI](/solutions/search/full-text/search-with-synonyms.md#method-1-kib-ui) enables managing synonym sets directly within {{kib}}. This makes it easier to improve search relevance without editing configuration files.

### Query Rules UI

The [Query Rules UI](/solutions/elasticsearch-solution-project/query-rules-ui.md) enables you to create and manage query rules that modify search behavior based on specific conditions, helping you deliver more relevant results for common queries.

## Get started

Ready to start using the {{es}} solution? Refer to [Get started](/solutions/elasticsearch-solution-project/get-started.md) for setup instructions and quickstart guides.

For a deeper understanding of search concepts and techniques, refer to the [Search use case](/solutions/search.md) documentation.

## Related reference

* [Search use case documentation](/solutions/search.md)
* [{{es}} reference documentation](elasticsearch://reference/elasticsearch/index.md)
* [{{es}} API documentation]({{es-apis}})

[^api-note]: Certain APIs are not available on serverless deployments because they are fully managed by Elastic. Refer to [Available Elasticsearch APIs](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-apis-availability) for details.
