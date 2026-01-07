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

This section documents core {{es}} search capabilities. These capabilities are available across all Elastic deployments, solutions, and project types.

Use this section to understand search techniques, query methods, ranking strategies, and data ingestion for search applications.

::::{tip}
Using the {{es}} solution or serverless project type? The [{{es}} solution documentation](/solutions/elasticsearch-solution-project.md) covers additional UI tools available if you are using the solution or project type.
::::

## What you can build

Use {{es}} search capabilities to build search applications including:

- Website and documentation search
- Ecommerce product catalogs
- Content recommendation systems
- RAG (Retrieval Augmented Generation) systems
- Geospatial search applications
- Question answering systems
- Custom observability or cybersecurity search tools
- Much more!

## Search use case documentation

The following subjects are covered in this section:

| Topic | Description |
|-------|-------------|
| [**Get started**](/solutions/search/get-started.md) | Create deployments, connect to {{es}}, and run your first searches |
| [**Ingest data**](/solutions/search/ingest-for-search.md) |  Learn about options for getting data into {{es}} for search use cases | 
| [**Search approaches**](/solutions/search/search-approaches.md) | Compare search techniques available in {{es}}, including full-text, vector, semantic, and hybrid search |
| [**Build your queries**](/solutions/search/querying-for-search.md) | Implement your search approaches using specific query languages |
| [**Ranking and reranking**](/solutions/search/ranking.md) | Control result ordering and relevance |
| [**RAG**](/solutions/search/rag.md) | Learn about tools for retrieval augmented generation with {{es}}|
| [**Building applications**](/solutions/search/site-or-app.md) | Integrate {{es}} into your websites or applications |

## Core concepts [search-concepts]

For an introduction to core {{es}} concepts such as indices, documents, and mappings, refer to [](/manage-data/data-store.md).

To dive more deeply into the building blocks of {{es}} clusters, including nodes, shards, primaries, and replicas, refer to [](/deploy-manage/distributed-architecture.md).

## Related reference

* [{{es}} reference documentation](elasticsearch://reference/elasticsearch/index.md)
* [{{es}} API documentation]({{es-apis}})
