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
---

# {{es}} solution overview

The {{es}} solution and serverless project type provide specialized UI tools that help you build search-powered applications faster. These tools build on top of core {{es}} [search capabilities](/solutions/search.md) that are available across all deployment types, solutions, and project types.

These UI affordances are exclusive to the {{es}} solution and serverless project type.

::::{tip}
Not sure which deployment type is right for you? Use the following resources to help you decide:

- Read the Elastic [deployment types overview](/deploy-manage/deploy.md)
- Compare [serverless and {{ech}}](/deploy-manage/deploy/deployment-comparison.md)
  - Compare pricing models between [{{ech}}](/deploy-manage/cloud-organization/billing/cloud-hosted-deployment-billing-dimensions.md) and [Serverless](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md)
::::

::::{admonition} About the term {{es}}
:::{include} /solutions/_snippets/elasticsearch-disambiguation.md
:::

This page describes the {{es}} solution and serverless project type. To learn the basics of Elastic and {{es}}, including the {{stack}}, deployment options, and solutions, go to [Elastic fundamentals](/get-started/index.md). To learn about search techniques that work in every deployment type, go to the [Search use case](/solutions/search.md). To set up, secure, and configure {{es}}, go to the [{{es}} reference](elasticsearch://reference/elasticsearch/index.md). To call {{es}} from your code, go to the [{{es}} API documentation]({{es-apis}}).
::::


## Features and tools

The {{es}} solution provides the following specialized UI tools and features to help you build search-powered applications faster:

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

* [Search use case documentation](/solutions/search.md)
* [{{es}} reference documentation](elasticsearch://reference/elasticsearch/index.md)
* [{{es}} API documentation]({{es-apis}})
