---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-with-elasticsearch.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
navigation_title: Search use case
---

# Search use case

Build powerful search experiences using {{es}}'s universal search capabilities. Whether you're running a self-managed cluster, {{ech}}, or an {{es}} serverless project, these search primitives are available across all deployment types.

{{es}} is a distributed datastore that can ingest, index, and manage various types of data in near real-time, making them both searchable and analyzable. This documentation covers the core search capabilities and techniques that work universally across all {{es}} deployments.

::::{tip}
Using the {{es}} solution or serverless project type? Check out the [{{es}} solution documentation](/solutions/elasticsearch-solution-project.md) for exclusive UI tools like Agent Builder, Playground, and Search Applications that complement these universal search capabilities.
::::

## Use cases

Here are a few common real-world applications:

| Use case                             | Business goals                                                     | Technical requirements                                        |
| ------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------- |
| **Vector search/hybrid search** | Run nearest neighbour search, combine with text for hybrid results | Dense embeddings, sparse embeddings, combined with text/BM25       |
| **Ecommerce/product catalog search** | Provide fast, relevant, and up-to-date results, faceted navigation | Inventory sync, user behavior tracking, results caching       |
| **Workplace/knowledge base search**  | Search across range of data sources, enforcing permissions         | Third-party connectors, document-level security, role mapping |
| **Website search**                   | Deliver relevant, up-to-date results                               | Web crawling, incremental indexing, query caching             |
| **Customer support search**          | Surface relevant solutions, manage access controls, track metrics  | Knowledge graph, role-based access, analytics                 |
| **Chatbots/RAG**                     | Enable natural conversations, provide context, maintain knowledge  | Vector search, ML models, knowledge base integration          |
| **Geospatial search**                | Process location queries, sort by proximity, filter by area        | Geo-mapping, spatial indexing, distance calculations          |

If you're new to {{es}} and want to try out some simple search use cases, refer to [Get started with search](/solutions/search/get-started.md).

## Core concepts [search-concepts]

For an introduction to core {{es}} concepts such as indices, documents, and mappings, refer to [](/manage-data/data-store.md).

To dive more deeply into the building blocks of {{es}} clusters, including nodes, shards, primaries, and replicas, refer to [](/deploy-manage/distributed-architecture.md).

## Related reference

* [{{es}} reference documentation](elasticsearch://reference/elasticsearch/index.md)
* [Content connectors](elasticsearch://reference/search-connectors/index.md)
* [{{es}} API documentation]({{es-apis}})

::::{tip}
Not sure whether {{es}} on {{serverless-full}} is the right deployment choice for you?

Check out the following resources to help you decide:

- [What’s different?](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md): Understand the differences between {{serverless-full}} and other deployment types.
- [Billing](/deploy-manage/cloud-organization/billing/elasticsearch-billing-dimensions.md): Learn about the billing model for {{es}} on {{serverless-full}}.
::::
