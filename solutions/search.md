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

This section documents {{es}} search primitives. These capabilities that are available across all Elastic deployments.

Use this section to understand search techniques, query methods, ranking strategies, and data ingestion for search applications.

::::{tip}
Using the {{es}} solution or serverless project type? The {{es}} solution documentation covers additional UI tools that complement these search primitives. Refer to [](/solutions/elasticsearch-solution-project.md) for more details.
::::

## What you can build

| Application type | Search technique | Key primitives | Documentation |
|-----------------|------------------|----------------|---------------|
| **Website/documentation search** | Text matching with relevance scoring | Full-text search, analyzers, scoring functions | [Full-text search](/solutions/search/full-text.md), [Ranking](/solutions/search/ranking.md) |
| **Ecommerce product catalogs** | Text + filters + facets | Hybrid search, aggregations, boosting | [Hybrid search](/solutions/search/hybrid-search.md), [Ranking](/solutions/search/ranking.md) |
| **Semantic/similarity search** | Embedding-based retrieval | Vector search, dense/sparse vectors, kNN | [Vector search](/solutions/search/vector.md), [Semantic search](/solutions/search/semantic-search.md) |
| **RAG applications** | Retrieval for LLM context | Retrievers, embedding models, ranking, query methods | [RAG](/solutions/search/rag.md), [Querying](/solutions/search/querying-for-search.md), [Retrievers](/solutions/search/retrievers-overview.md), [Semantic search](/solutions/search/semantic-search.md), [Ranking](/solutions/search/ranking.md) |
| **Geospatial applications** | Location-based queries | Geo-point, geo-shape fields, distance sorting | [Geospatial search](elasticsearch://reference/elasticsearch/mapping-reference/geo-point.md) |
| **Federated search** | Querying multiple clusters | Remote cluster connections, distributed queries | [Cross-cluster search](/solutions/search/cross-cluster-search.md) |

## Core concepts [search-concepts]

For an introduction to core {{es}} concepts such as indices, documents, and mappings, refer to [](/manage-data/data-store.md).

To dive more deeply into the building blocks of {{es}} clusters, including nodes, shards, primaries, and replicas, refer to [](/deploy-manage/distributed-architecture.md).

## Related reference

* [{{es}} reference documentation](elasticsearch://reference/elasticsearch/index.md)
* [{{es}} API documentation]({{es-apis}})
