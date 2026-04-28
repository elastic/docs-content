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

Use this section to understand search techniques, query methods, ranking strategies, and data ingestion for search-powered applications.

::::{tip}
Using the {{es}} solution or serverless project type? The [{{es}} solution documentation](/solutions/elasticsearch-solution-project.md) covers additional UI tools included with these options.
::::

## What you can build

Use {{es}} search capabilities for use cases such as:

- Website and documentation search
- Ecommerce product catalogs
- Content recommendation systems
- RAG (Retrieval Augmented Generation) systems
- Geospatial search applications
- Question answering systems
- Analytics dashboards and data exploration
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

## Search concepts [search-concepts]

For an introduction to core {{es}} concepts such as indices, documents, and mappings, refer to [](/manage-data/data-store.md).

To dive more deeply into the building blocks of {{es}} clusters, including nodes, shards, primaries, and replicas, refer to [](/deploy-manage/distributed-architecture.md).

## {{es}} as a vector database [es-as-vector-database]

{{es}} functions as a vector database by storing vector embeddings and retrieving the most similar results to a query vector. Vector embeddings are numerical representations of data, such as text, images, or audio, created by {{ml}} models. Because similar items are positioned closer together in vector space, {{es}} can use these embeddings to perform semantic similarity search and return results based on meaning rather than exact keyword matches.

This capability is the foundation for vector search and related use cases in {{es}}. It enables you to work with semantic retrieval on the same data and infrastructure that you already use for full-text search, structured filters, and aggregations. {{es}} supports this by storing embeddings in vector field types such as `dense_vector` and `sparse_vector`, alongside your other indexed data.

To use {{es}} as a vector database, you can use the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type. When you index content into a `semantic_text` field, {{es}} automatically generates vector embeddings using a configured {{ml}} model and stores them in the underlying vector field. These embeddings are indexed for efficient [k-nearest neighbor (kNN) search](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md), enabling fast similarity-based retrieval at query time.

For a high-level understanding of vector search concepts and capabilities in {{es}}, refer to Vector search. For an overview of use cases and guidance on how to implement them, refer to Vector search use cases.

<!--
TODO: Once https://github.com/elastic/docs-content/pull/5567 is merged:
- Place link to definition list items on the new Vector search landing page for the following terms: vector database, vector embeddings, dense_vector, sparse_vector
- Place links to Vector search and Vector search use cases
-->

## Related reference

* [{{es}} reference documentation](elasticsearch://reference/elasticsearch/index.md)
* [{{es}} API documentation]({{es-apis}})

