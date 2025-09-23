---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-with-elasticsearch.html
  - https://www.elastic.co/guide/en/serverless/current/what-is-elasticsearch-serverless.html
  - https://www.elastic.co/guide/en/kibana/current/search-space.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: kibana
---

# Elasticsearch

{{es}} enables you to build powerful search experiences for websites, applications, and enterprise data using Elastic's unified platform.

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

## {{es-serverless}} [elasticsearch-serverless]
```{applies_to}
serverless:
  elasticsearch: ga
```

{{es-serverless}} is one of the three available project types on [{{serverless-full}}](/deploy-manage/deploy.md).

This project type enables you to use the core functionality of {{es}}: searching, indexing, storing, and analyzing data of all shapes and sizes.

When using {{es}} on {{serverless-full}} you don’t need to worry about managing the infrastructure that keeps {{es}} distributed and available: nodes, shards, and replicas. These resources are completely automated on the serverless platform, which is designed to scale up and down with your workload.
This automation allows you to focus on building your search applications and solutions.

::::{tip}
Not sure whether {{es}} on {{serverless-full}} is the right deployment choice for you?

Check out the following resources to help you decide:
- [What’s different?](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md): Understand the differences between {{serverless-full}} and other deployment types.
- [Billing](/deploy-manage/cloud-organization/billing/elasticsearch-billing-dimensions.md): Learn about the billing model for {{es}} on {{serverless-full}}.
::::