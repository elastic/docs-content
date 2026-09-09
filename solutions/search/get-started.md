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

New to search with {{es}}? Start building a search experience by setting up your first deployment, refining your search goals, and adding data. **These core search capabilities are available to you regardless of your deployment type, solution, or project type.**

:::{note}
If you're looking for an introduction to the {{stack}} or the {{es}} product, go to [](/get-started/index.md) or [](/manage-data/data-store.md).
:::

:::{agent-skill}
:url: https://github.com/elastic/agent-skills@elasticsearch-onboarding
This skill guides users through search concepts and helps create a working search use case.
:::

::::::{stepper}
:::::{step} Choose your deployment type

Elastic provides several self-managed and Elastic-managed options.

To get started, choose one of these options:

- [Create a {{serverless-short}} project](#create-serverless-project).
- [Create a local development installation](#create-local-development-installation).

Check out the full list of [deployment types](/deploy-manage/deploy.md#choosing-your-deployment-type) to learn more.

### Create a {{serverless-short}} project [create-serverless-project]

```{applies_to}
serverless:
```

For simplicity and speed, use {{serverless-full}}.

::::{dropdown} Create a serverless project
$$$serverless-project-configuration$$$
#### Choose a {{serverless-short}} project configuration

Both [{{es}} projects](/solutions/elasticsearch-solution-project.md) and [{{es}} Vector Database projects](/solutions/vector-database.md) support vector search and use the same query APIs.

| Project type | When to choose |
| --- | --- |
| [{{es}} project](/solutions/elasticsearch-solution-project.md) | For general-purpose data storage and search, including mixed lexical, time series, and analytics workloads, or when you need to run custom models on {{ml}} nodes |
| [{{es}} Vector Database project](/solutions/vector-database.md) | When embeddings and similarity search are central to your workload, such as RAG, recommendations, semantic search, hybrid search, or multimodal search |

There are two options to create a serverless project:

* If you're a new user, [sign up for a free 14-day trial](https://cloud.elastic.co/serverless-registration) to create a serverless project. For more information about {{ecloud}} trials, refer to [Trial features](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#general-sign-up-trial-what-is-included-in-my-trial).
* If you're an existing customer, [log in to {{ecloud}}](https://cloud.elastic.co/login). On the home page, you can create a serverless project. You need the `admin` predefined role or an equivalent custom role to create projects. Refer to [](/deploy-manage/users-roles/cloud-organization/user-roles.md).
::::

### Create a local development installation [create-local-development-installation]

Create a [local development installation](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md) in Docker:

```sh
curl -fsSL https://elastic.co/start-local | sh
```

:::::

:::::{step} (Optional) Try out a quickstart

Get hands-on experience with {{es}} using guided tutorials that walk you through common search scenarios:

- [**Index and search basics**](/solutions/search/get-started/index-basics.md): Learn how to create indices, add documents, and perform searches
- [**Keyword search with Python**](/solutions/search/get-started/keyword-search-python.md): Build your first search query with Python
- [**Semantic search**](/solutions/search/get-started/semantic-search.md): Implement semantic search with vector embeddings using the `semantic_text` workflow
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

- Evaluate the [{{es}} solution](/solutions/elasticsearch-solution-project.md)
- [](/deploy-manage/deploy/deployment-comparison.md)
- [Get started with Query DSL search and filters](elasticsearch://reference/query-languages/query-dsl/full-text-filter-tutorial.md)
- [Get started with ES|QL queries](elasticsearch://reference/query-languages/esql/esql-getting-started.md)
- [Analyze eCommerce data with aggregations using Query DSL](/explore-analyze/query-filter/aggregations/tutorial-analyze-ecommerce-data-with-aggregations-using-query-dsl.md)


