---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-getting-started.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: kibana
---

# Get started with the {{es}} solution

This guide helps you get started with the {{es}} solution and serverless project type, including the specialized UI tools and interfaces available exclusively in this environment.

::::{tip}
New to {{es}} search capabilities? Start with the [Search use case documentation](/solutions/search.md) to learn about universal {{es}} search primitives like full-text search, vector search, and hybrid search that work across all deployment types.
::::

## Before you begin

To use the {{es}} solution, you'll need:

- An {{es}} solution deployment on {{ech}} or an {{es}} serverless project
- Access to {{kib}} for using the UI tools
- Connection details for your cluster. Refer to [Connection details](/solutions/elasticsearch-solution-project/search-connection-details.md) for more information.

## Quickstarts

Get hands-on experience with {{es}} using these guided tutorials:

- [**Index basics**](/solutions/elasticsearch-solution-project/get-started/index-basics.md): Learn how to create indices, add documents, and perform searches.
- [**Keyword search with Python**](/solutions/elasticsearch-solution-project/get-started/keyword-search-python.md): Build a keyword search application.
- [**Semantic search**](/solutions/elasticsearch-solution-project/get-started/semantic-search.md): Implement semantic search using embeddings.

## Explore {{es}} solution features

The {{es}} solution provides specialized UI tools to enhance your search experience:

### Agent Builder

Create AI agents that interact with your {{es}} data. Refer to [Agent Builder](/solutions/elasticsearch-solution-project/elastic-agent-builder.md) to get started.

### Playground

Test and explore RAG (Retrieval Augmented Generation) workflows using the interactive Playground interface. Refer to [Playground](/solutions/elasticsearch-solution-project/playground.md) to learn more.

### Search Applications

Manage and deploy search-powered applications with pre-built templates. Refer to [Search Applications](/solutions/elasticsearch-solution-project/search-applications.md) for details.

### UI tools for search optimization

- [**Search with synonyms**](/solutions/elasticsearch-solution-project/full-text/search-with-synonyms.md): Manage synonym sets through the UI
- [**Query Rules UI**](/solutions/elasticsearch-solution-project/query-rules-ui.md): Create rules to modify search behavior
- [**AI Assistant**](/solutions/elasticsearch-solution-project/ai-assistant.md): Get intelligent assistance across the platform

## Next steps

- Learn about [search techniques and approaches](/solutions/search/search-approaches.md) in the Search use case documentation
- Explore [RAG concepts](/solutions/search/rag.md) to understand how Playground leverages retrieval augmented generation
- Discover [ingestion methods](/solutions/search/ingest-for-search.md) for preparing your data
- Understand [ranking strategies](/solutions/search/ranking.md) to improve search relevance

## Related resources

- [{{es}} solution overview](/solutions/elasticsearch-solution-project.md)
- [Search use case documentation](/solutions/search.md)
- [{{es}} API documentation]({{es-apis}})
- [{{es}} reference documentation](elasticsearch://reference/elasticsearch/index.md)
