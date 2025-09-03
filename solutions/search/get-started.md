---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-get-started.html
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

# Get started with {{es}}

New to {{es}}? Start building a search experience by setting up your first deployment, refining your search goals, and adding data.

:::{note}
If you're looking for an introduction to the {{stack}} or the {{es}} product, go to [](/get-started/index.md) or [](/manage-data/data-store.md).
:::

:::::{stepper}
::::{step} Choose your deployment type

Elastic provides several self-managed and Elastic-managed options.
For simplicity and speed, try out [{{es-serverless}}](/solutions/search/serverless-elasticsearch-get-started.md).

Alternatively, create a [local development installation](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md) in Docker:

```sh
curl -fsSL https://elastic.co/start-local | sh
```

Check out the full list of [deployment types](/deploy-manage/deploy.md#choosing-your-deployment-type) to learn more.
::::

::::{step} Identify your search goals
Depending on your use case, you can choose multiple [search approaches](search-approaches.md) (for example, full-text and semantic search).
Each approach affects your options for storing and querying your data.

:::{tip}
If you want to ingest your data first and transform or reindex it as needed later, you can skip to the next step.
:::
::::
::::{{step}} Ingest your data

To learn about adding data, go to [](/solutions/search/ingest-for-search.md).
For a broader overview of ingestion options, go to [](/manage-data/ingest.md).

If you're planning to perform a vector or semantic AI-powered search, the approach that requires the least configuration involves adding `semantic_text` fields when ingesting your data.
Try it out with [](/solutions/search/get-started/semantic-search.md).

:::{tip}
If you're not ready to add your own data, you can use [sample data](/manage-data/ingest/sample-data.md) or create small data sets when you follow the instructions in the [quickstarts](/solutions/search/get-started/quickstarts.md).
:::
::::

::::{{step}} Get started with your use case

Not sure where to start exploring or which features may be relevant for you?
View our [quickstarts](/solutions/search/get-started/quickstarts.md), which help you complete a core task so you can get up and running.
For example, learn about [index and search basics](/solutions/search/get-started/index-basics.md).

Your next steps will be to choose a method to write queries and interact with {{es}}.
You can pick a programming language [client](/reference/elasticsearch-clients/index.md) that matches your application and choose which [query languages](/solutions/search/querying-for-search.md) you will use to express your search logic.
Each decision builds on the previous ones, offering flexibility to mix and match approaches based on your needs.
::::
:::::

## Related resources

Use these resources to learn more about {{es}} or get started in a different way:

- [](/deploy-manage/deploy/deployment-comparison.md)
- [](/solutions/search/get-started/quickstarts.md)
- [Get started with Query DSL search and filters](elasticsearch://reference/query-languages/query-dsl/full-text-filter-tutorial.md)
- [Get started with ES|QL queries](elasticsearch://reference/query-languages/esql/esql-getting-started.md)
- [Analyze eCommerce data with aggregations using Query DSL](/explore-analyze/query-filter/aggregations/tutorial-analyze-ecommerce-data-with-aggregations-using-query-dsl.md)
