---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/what-is-elasticsearch-serverless.html
  - https://www.elastic.co/guide/en/kibana/current/search-space.html
applies_to:
  stack:
  serverless: 
    elasticsearch: ga
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: kibana
navigation_title: Elasticsearch solution
description: >-
  Use the Elasticsearch solution to build search applications and to run
  search, analytics, and time series data together. It includes Kibana tools
  such as Agent Builder, Synonyms, and Query Rules.
type: overview
---

# {{es}} solution overview

The {{es}} solution is for building search applications, and for keeping search, analytics, and time series data together. On {{serverless-full}}, you create it as a project. On {{ech}}, {{ece}}, {{eck}}, and self-managed clusters, it is a solution view in {{kib}}.

This solution includes the tools and applications you need to implement [search use cases](/solutions/search.md), plus {{kib}} applications for data exploration and analytics.

::::{tip}
Not sure which deployment type is right for you? Use the following resources to help you decide:

- Read the Elastic [deployment types overview](/deploy-manage/deploy.md)
- Compare [serverless and {{ech}}](/deploy-manage/deploy/deployment-comparison.md)
  - Compare pricing models between [{{ech}}](/deploy-manage/cloud-organization/billing/cloud-hosted-deployment-billing-dimensions.md) and [Serverless](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md)
::::

## When to use this solution

Use this solution when you need search together with analytics or time series data, or tools such as Agent Builder, Synonyms, and Query Rules.

If you're building [RAG](/solutions/search/rag.md), or most of your queries are similarity or hybrid search on embeddings, use the [{{es}} {{vectordb}} project type](/solutions/vector-database.md#when-to-use-this-project-type) instead. {{vectordb}} is available on {{serverless-short}} only. Both use the same {{es}} engine and query APIs.

## Features and tools

The {{es}} solution includes these {{kib}} applications:

### Agent Builder

[Agent Builder](/explore-analyze/ai-features/elastic-agent-builder.md) enables you to create AI agents that can interact with your {{es}} data, run queries, and provide intelligent responses. It provides a complete framework for building conversational AI experiences on top of your search infrastructure.

### Synonyms UI

The [synonyms UI](/solutions/search/full-text/search-with-synonyms.md#synonyms-store-synonyms-kibana) enables managing synonym sets directly within {{kib}}. This makes it easier to improve search relevance without editing configuration files.

### Query Rules UI

The [Query Rules UI](/solutions/elasticsearch-solution-project/query-rules-ui.md) enables you to create and manage query rules that modify search behavior based on specific conditions, helping you deliver more relevant results for common queries.

## Get started

Ready to start using the {{es}} solution? Refer to [Get started](/solutions/elasticsearch-solution-project/get-started.md) for setup instructions and quickstart guides.

For a deeper understanding of search concepts and techniques, refer to the [Search use case](/solutions/search.md) documentation.

## Related pages

* [{{es}} {{vectordb}} project overview](/solutions/vector-database.md)
* [Search use case documentation](/solutions/search.md)
* [{{es}} reference documentation](elasticsearch://reference/elasticsearch/index.md)
* [{{es}} API documentation]({{es-apis}})
