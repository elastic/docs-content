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

# The Elasticsearch solution and search use case

The {es} solution and serverless project type combines the core {es} data store, search engine, and vector database technologies with specialized user interfaces and tools, giving you the building blocks to create, deploy, and run your own search applications.

## The {es} solution

The Elasticsearch solution and serverless project type provides specialized user interfaces and tools designed to simplify the implementation of search applications:

* **Search and discovery interfaces**: Discover and Dashboards for exploring data, building visualizations, and creating search experiences.
* **Management interfaces**: Index Management and other tools for configuring and optimizing your search implementation.
* **Search relevance tools**: Purpose-built UIs for managing synonyms, query rules, and other relevance-enhancing features.
* **AI toolkit**: RAG Playground and inference endpoints management for building AI-enhanced search experiences.
* **Complete Elasticsearch REST API**: Full access to Elasticsearch's comprehensive APIs for indexing, searching, and managing data.
* **Deployment flexibility**: Run in Elastic Cloud, Elastic Serverless, or self-managed environments with consistent interfaces.

## Use cases

You can approach {{es}} use cases from two complementary angles: first, as a data store and vector database where you bring in and manage different types of data, and second, as a search solution where you use those core capabilities as building blocks to create tailored search applications.

### Data store and vector database use case

All of the search capabilities you find on this page are possible because {{es}} is not just a search engine, but it’s also a scalable, cost-efficient [data store](/manage-data/data-store.md).
You can bring in many types of data, index them in near real time, and keep them stored in a way that makes them both searchable and analyzable. Common examples include, but are not limited to:

* **Textual data**: documents, logs, articles, or transcripts.
* **Numerical data**: metrics, performance data, sensor readings.
* **Geospatial data**: coordinates, maps, and location-based signals.
* **Vector data**: embeddings from {{ml}} models for semantic or hybrid search.

By bringing all these capabilities together, Elasticsearch serves as a powerful data store, a geospatial search engine, a vector database, and more,  all within a single technology. It forms the foundation of Elastic's unified data and search platform, enabling you to work with different data types seamlessly. To learn more, refer to the [{{es}} data store overview](/manage-data/data-store.md).

### Search use case

Think of {{es}} as a set of powerful building blocks. You bring in your own data, text, logs, metrics, events, vectors, or geospatial information, and {{es}} gives you the tools to store, search, and analyze it. By combining these capabilities, you can design and build the search and discovery experiences that fit your needs, from product catalogs to knowledge bases, chatbots, or geospatial applications.

| Use case                             | Business goals                                                     | Technical requirements                                        |
| ------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------- |
| **Vector search/hybrid search**      | Run nearest neighbour search, combine with text for hybrid results | Dense embeddings, sparse embeddings, combined with text/BM25  |
| **Ecommerce/product catalog search** | Provide fast, relevant, and up-to-date results, faceted navigation | Inventory sync, user behavior tracking, results caching       |
| **Workplace/knowledge base search**  | Search across range of data sources, enforcing permissions         | Third-party connectors, document-level security, role mapping |
| **Website search**                   | Deliver relevant, up-to-date results                               | Web crawling, incremental indexing, query caching             |
| **Customer support search**          | Surface relevant solutions, manage access controls, track metrics  | Knowledge graph, role-based access, analytics                 |
| **Chatbots/RAG**                     | Enable natural conversations, provide context, maintain knowledge  | Vector search, ML models, knowledge base integration          |
| **Geospatial search**                | Process location queries, sort by proximity, filter by area        | Geo-mapping, spatial indexing, distance calculations          |
