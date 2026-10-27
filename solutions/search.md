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

# Search with {{es}}

This section documents core {{es}} search capabilities. These capabilities are available across all Elastic deployments, solutions, and project types. Use this section to set up {{es}} and understand search techniques, ranking strategies, and data ingestion for search-powered applications.

:::{agent-skill}
:url: https://github.com/elastic/agent-skills@elasticsearch-onboarding
This skill guides users through search concepts and helps create a working search use case.
:::

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

## Learn about concepts

- If you want an introduction to the {{stack}} or the {{es}} product, start with [](/get-started/index.md) or [](/manage-data/data-store.md).
- To dive more deeply into the building blocks of {{es}} clusters, including nodes, shards, primaries, and replicas, refer to [](/deploy-manage/distributed-architecture.md).
- You can learn how {{es}} stores embeddings and retrieves similar results in [{{es}} as a vector database](/solutions/search/vector.md#es-as-vector-database).

## Build a search experience

These steps take you from a running {{es}} deployment to search queries.

::::::{stepper}
:::::{step} Set up {{es}}

Choose where {{es}} runs, start it, and connect a client. Once {{es}} is running, try a [quickstart](/solutions/search/get-started/quickstarts.md).
:::::
:::::{step} Identify your search goals
Depending on your use case, you can choose multiple [search approaches](/solutions/search/search-approaches.md), for example full-text and semantic search.
Each approach affects your options for storing and querying your data.

If you're unsure which approaches match your goals, you can try them out with sample data. For example, [](/solutions/search/get-started/semantic-search.md).

If you prefer to ingest your data first and transform or reindex it as needed later, skip to the next step.
:::::
:::::{step} Ingest your data

If your goals include vector or semantic AI-powered search, create vectorized data with built-in and third-party natural language processing (NLP) models and store it in an {{es}} vector database.
The approach that requires the least configuration involves adding `semantic_text` fields when ingesting your data.
This method is described in [](/solutions/search/semantic-search/semantic-search-semantic-text.md).

To learn about adding data for other search goals, go to [](/solutions/search/ingest-for-search.md).
For a broader overview of ingestion options, go to [](/manage-data/ingest.md).

If you're not ready to add your own data, you can use [sample data](/manage-data/ingest/sample-data.md) or create small data sets when you follow the instructions in the [quickstarts](/solutions/search/get-started/quickstarts.md).

The {{es}} home page in the UI also provides workflow guides for creating indices and ready-to-use code examples for ingesting data by using REST APIs.
:::::
:::::{step} Build your search queries

Your next steps will be to choose a method to write queries and interact with {{es}}.
You can pick a programming language [client](/reference/elasticsearch-clients/index.md) that matches your application and choose which [query languages](/solutions/search/querying-for-search.md) you will use to express your search logic.
Each decision builds on the previous ones, offering flexibility to mix and match approaches based on your needs.
:::::

::::::

## Resources

- [{{es}} solution documentation](/solutions/elasticsearch-solution-project.md): Additional UI tools included with the {{es}} solution and serverless project type.
- [{{es}} reference documentation](elasticsearch://reference/elasticsearch/index.md): Reference for setup, working with data, search, and analytics.
- [{{es}} API documentation]({{es-apis}}): REST API reference for indexing, searching, and managing {{es}}.

