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

# The Elasticsearch solution

The {{es}} solution and serverless project type position {{es}} as a comprehensive platform: a scalable data store, a powerful search engine, and a vector database in one. At its core, {{es}} is a distributed datastore that can ingest, index, and manage various types of data in near real-time, making them both searchable and analyzable. With specialized user interfaces and tools, it provides the flexibility to create, deploy, and run a wide range of applications, from search to analytics to AI-driven solutions.

## What the {{es}} solution provides

The {{es}} solution and serverless project type include specialized user interfaces and tools that simplify working with {{es}}:

* **Ingestion tools**: Content connectors, crawlers, file upload capabilities, and indexing APIs for ingesting and storing data
* **Data management and discovery**: Discover and Dashboards for exploring data, building visualizations, and creating interactive experiences
* **Management interfaces**: Index Management and other tools for configuring and optimizing your stored data and implementation
* **Search relevance tools**: Purpose-built UIs for managing synonyms, query rules, and other relevance-enhancing features
* **AI toolkit**: RAG Playground and inference endpoints management for building AI-enhanced applications
* **Complete {{es}} REST API**: Full access to {{es}}'s comprehensive APIs for indexing, searching, and managing data
* **Deployment flexibility**: Run in Elastic Cloud, Elastic Serverless, or self-managed environments with consistent interfaces

## Core capabilities and use cases

You can think of {{es}} in two complementary ways:

1. **As a datastore and vector database**: use {{es}} directly to ingest, store, and manage many types of data in a scalable, cost-efficient way, without the need to add anything else.
2. **As a foundation for custom applications**: use {{es}}'s building blocks to design and build applications including search and discovery tools.  

### Datastore

You can index many types of data, keep them stored efficiently, searchable, and analyzable. If all you need is a reliable and scalable datastore, you can use {{es}} that way without adding anything else. All of {{es}}’s advanced capabilities start with its role as a [data store](/manage-data/data-store.md). Examples include, but are not limited to:

* **Textual data**: documents, logs, articles, and transcripts
* **Numerical data**: metrics, performance data, sensor readings
* **Time series data**: events, traces, and system metrics collected over time
* **Geospatial data**: coordinates, maps, and location-based signals
* **Vector data**: embeddings from {{ml}} models for semantic or hybrid search

By bringing these capabilities together, {{es}} acts as a powerful data store, time series database, geospatial engine, and vector database, all within a single platform. Whether you use it as a datastore or as the backbone for advanced search and analytics, this unified foundation enables you to work seamlessly with diverse data types and power your own applications.

### Search and discovery applications

Search is one of the common use cases built on {{es}}. {{es}} gives you the tools to store, search, and analyze your own data, including text, logs, metrics, events, vectors, and geospatial information. Using these building blocks, you can design search and discovery experiences, from internal knowledge bases to product catalogs, chat interfaces, or geospatial applications.

{{es}} gives you the core platform to build the experiences that best match your requirements.

| Use case                             | Business goals                                                     | Technical requirements                                        |
| ------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------- |
| **Vector search/hybrid search**      | Run nearest neighbour search, combine with text for hybrid results | Dense embeddings, sparse embeddings, combined with text/BM25  |
| **Ecommerce/product catalog search** | Provide fast, relevant, and up-to-date results, faceted navigation | Inventory sync, user behavior tracking, results caching       |
| **Workplace/knowledge base search**  | Search across range of data sources, enforcing permissions         | Third-party connectors, document-level security, role mapping |
| **Website search**                   | Deliver relevant, up-to-date results                               | Web crawling, incremental indexing, query caching             |
| **Customer support search**          | Surface relevant solutions, manage access controls, track metrics  | Knowledge graph, role-based access, analytics                 |
| **Chatbots/RAG**                     | Enable natural conversations, provide context, maintain knowledge  | Vector search, ML models, knowledge base integration          |
| **Geospatial search**                | Process location queries, sort by proximity, filter by area        | Geo-mapping, spatial indexing, distance calculations          |

## Further reading

* [{{es}} reference documentation](elasticsearch::docs/reference/elasticsearch/index.md)
* [The {{es}} data store](/manage-data/data-store.md)
* [Content connectors](elasticsearch::docs/reference/search-connectors/index.md)
* [{{es}} API documentation](https://www.elastic.co/docs/api/doc/elasticsearch/v9/)

::::{tip}
Considering whether {{es}} on {{serverless-full}} is the right deployment option for your needs?

These resources can help you compare and decide:

* [What’s different?](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md): Understand the differences between {{serverless-full}} and other deployment types.
* [Billing](/deploy-manage/cloud-organization/billing/elasticsearch-billing-dimensions.md): Learn about the billing model for {{es}} on {{serverless-full}}.
::::
