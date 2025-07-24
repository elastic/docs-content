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
---

# Get started with {{es}}

New to {{es}}? Start building a search experience by setting up your first deployment, refining your search goals, and adding data.

:::{note}
If you're looking for an introduction to the {{stack}} or the {{es}} product, go to [](/get-started/index.md) or [](/manage-data/data-store.md).
:::

:::::{stepper}
::::{step} Choose your deployment type

Elastic provides several self-managed or Elastic-managed options.
For simplicity and speed, try out [{{es-serverless}}](/solutions/search/serverless-elasticsearch-get-started.md) or [run {{es}} locally](/solutions/search/run-elasticsearch-locally.md).
Check out the full list of [deployment types](/deploy-manage/deploy.md#choosing-your-deployment-type) to learn more.
::::

::::{step} Identify your search goals

You can choose multiple [search approaches](search-approaches.md) (for example, full-text and semantic search) depending on your use case.
Each approach affects your options for storing and querying your data.

:::{tip}
If you want to ingest your data first and transform or reindex it as needed later, you can skip to the next step.
:::
::::
::::{{step}} Ingest your data

To learn about adding data, go to [](/solutions/search/ingest-for-search.md).
For a broader overview of ingestion options, go to [](/manage-data/ingest.md).

If you're planning to perform vector or semantic AI-powered search, the approach that requires the least configuration involves adding `semantic_text` fields when you ingest your data.
Try it out with [](/solutions/search/get-started/semantic-search.md).

:::{tip}
If you're not ready to add your own data, you can use [sample data](/manage-data/ingest/sample-data.md) or create small data sets when you follow the [quickstarts](/solutions/search/get-started/quickstarts.md).
:::
::::

::::{{step}} Get started with your use case

Not sure where to start exploring or which features may be relevant for you?
View our [quickstarts](/solutions/search/get-started/quickstarts.md), which help you complete a core task so you can get up and running.
For example, to learn about using clients to integrate with {{es}} in your application, check out [](/solutions/search/get-started/keyword-search-python.md).
::::
:::::
