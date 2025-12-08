---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Get started with search

This guide helps you get started with search using {{es}}, regardless of your deployment type. Whether you're using a self-managed cluster, {{ech}}, or an {{es}} serverless project, these universal search capabilities are available to you.

::::{tip}
Using the {{es}} solution or serverless project type? Check out the [{{es}} solution documentation](/solutions/elasticsearch-solution-project.md) for UI tools like Agent Builder, Playground, and Search Applications that complement these universal capabilities.
::::

## Before you begin

To follow along with this guide, you'll need:

- An {{es}} cluster or serverless project. [Create a deployment](/get-started/start-building.md) if you don't have one yet.
- Connection details for your cluster. Refer to [Connection details](/solutions/search/search-connection-details.md) for more information.

## Quickstarts

Choose a quickstart based on your use case:

- [**Index basics**](/solutions/elasticsearch-solution-project/get-started/index-basics.md): Learn how to create indices, add documents, and perform basic searches using the {{es}} APIs.
- [**Keyword search with Python**](/solutions/elasticsearch-solution-project/get-started/keyword-search-python.md): Build a keyword search application using the Python client.
- [**Semantic search**](/solutions/elasticsearch-solution-project/get-started/semantic-search.md): Implement semantic search using vector embeddings.

## Explore search approaches

Once you're comfortable with the basics, explore different search techniques:

- [**Full-text search**](/solutions/search/full-text.md): Traditional text-based search with analysis and scoring.
- [**Vector search**](/solutions/search/vector.md): Similarity search using dense or sparse vectors.
- [**Semantic search**](/solutions/search/semantic-search.md): Context-aware search using machine learning models.
- [**Hybrid search**](/solutions/search/hybrid-search.md): Combine multiple search techniques for better results.

## Next steps

- Learn about [ingestion and data preparation](/solutions/search/ingest-for-search.md)
- Explore [querying options](/solutions/search/querying-for-search.md) including Query DSL, {{esql}}, and retrievers
- Understand [ranking and relevance](/solutions/search/ranking.md) to improve search quality
- Build [RAG (Retrieval Augmented Generation)](/solutions/search/rag.md) applications

## Related resources

- [{{es}} API documentation]({{es-apis}})
- [{{es}} reference documentation](elasticsearch://reference/elasticsearch/index.md)
- [Query languages](/explore-analyze/query-filter/languages/index.md)
