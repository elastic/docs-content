---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-getting-started.html
applies_to:
  stack:
  serverless:
    elasticsearch: all
products:
  - id: elasticsearch
  - id: cloud-serverless
navigation_title: Get started
description: To try out an {{es}} project or solution, pick your deployment type, search goals, and ingestion method.
---

# Get started with the {{es}} solution/project type

New to {{es}}? Start building a search experience by setting up your first deployment, refining your search goals, and adding data.

:::{note}
If you're looking for an introduction to the {{stack}} or the {{es}} product, go to [](/get-started/index.md) or [](/manage-data/data-store.md).
:::

::::::{stepper}
:::::{step} Choose your deployment type

Elastic provides several self-managed and Elastic-managed options.
For simplicity and speed, try out {{es-serverless}}:

::::{dropdown} Create an {{es-serverless}} project
:::{include} /deploy-manage/deploy/_snippets/create-serverless-project-intro.md
:::

Choose the {{es}} project type and provide a name.
You can optionally edit the project settings, such as the [region](/deploy-manage/deploy/elastic-cloud/regions.md).

When your project is created, you're ready to move on to the next step and to start creating indices, adding data, and performing searches.
::::

Alternatively, create a [local development installation](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md) in Docker:

```sh
curl -fsSL https://elastic.co/start-local | sh
```

Check out the full list of [deployment types](/deploy-manage/deploy.md#choosing-your-deployment-type) to learn more.
:::::

:::::{step} (Optional) Try out a quickstart

Get hands-on experience with {{es}} using guided tutorials that walk you through common search scenarios:

- [**Index and search basics**](/solutions/search/get-started/index-basics.md): Learn how to create indices, add documents, and perform searches
- [**Keyword search with Python**](/solutions/search/get-started/keyword-search-python.md): Build your first search query with Python
- [**Semantic search**](/solutions/search/get-started/semantic-search.md): Implement semantic search using embeddings
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

:::::{step} Explore solution features

The {{es}} solution provides additional UI tools on top of the core {{es}} capabilities, to help you build search applications:

- [**Agent Builder**](/solutions/elasticsearch-solution-project/elastic-agent-builder.md): Create AI agents that interact with your {{es}} data
- [**Query Rules UI**](/solutions/elasticsearch-solution-project/query-rules-ui.md): Create rules to modify search behavior
- [**Search with synonyms**](/solutions/search/full-text/search-with-synonyms.md): Manage synonym sets through the UI
:::::

## Related resources

Use these resources to learn more about {{es}} or get started in a different way:

- [](/deploy-manage/deploy/deployment-comparison.md)
- [Get started with Query DSL search and filters](elasticsearch://reference/query-languages/query-dsl/full-text-filter-tutorial.md)
- [Get started with ES|QL queries](elasticsearch://reference/query-languages/esql/esql-getting-started.md)
- [Analyze eCommerce data with aggregations using Query DSL](/explore-analyze/query-filter/aggregations/tutorial-analyze-ecommerce-data-with-aggregations-using-query-dsl.md)
