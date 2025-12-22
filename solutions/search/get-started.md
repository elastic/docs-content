---
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
navigation_title: Get started
description: Get started with the search use case using the core Elasticsearch search features available on any deployment type.
---

# Get started with search

New to search with {{es}}? Start building a search experience by setting up your first deployment, refining your search goals, and adding data. These core search capabilities are available to you regardless of your deployment type, solution, or project type.

:::{note}
If you're looking for an introduction to the {{stack}} or the {{es}} product, go to [](/get-started/index.md) or [](/manage-data/data-store.md).
:::

::::::{stepper}
:::::{step} Choose your deployment type

Elastic provides several self-managed and Elastic-managed options.
For simplicity and speed, try out {{serverless-full}}:

::::{dropdown} Create a serverless project
:::{include} /deploy-manage/deploy/_snippets/create-serverless-project-intro.md
:::

If you're not sure which project type to choose, select the **{{es}}** project type. This project type provides core {{es}} search capabilities along with additional UI tools to help you build search applications faster.

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

::::::


## Related resources

Use these resources to learn more about {{es}} or get started in a different way:

- Evaluate the [{{es}} solution](/solutions/elasticsearch-solution-project.md).
- [](/deploy-manage/deploy/deployment-comparison.md)
- [Get started with Query DSL search and filters](elasticsearch://reference/query-languages/query-dsl/full-text-filter-tutorial.md)
- [Get started with ES|QL queries](elasticsearch://reference/query-languages/esql/esql-getting-started.md)
- [Analyze eCommerce data with aggregations using Query DSL](/explore-analyze/query-filter/aggregations/tutorial-analyze-ecommerce-data-with-aggregations-using-query-dsl.md)


