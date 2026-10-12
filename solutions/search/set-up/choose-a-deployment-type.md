---
applies_to:
  stack:
  serverless:
navigation_title: Choose a deployment type
description: Select an Elasticsearch deployment model for search, get it running, and try a search quickstart.
type: overview
---

# Choose a deployment type [choose-a-deployment-type]

{{es}} is at the core of every Elastic deployment type. The deployment type you choose determines who manages the infrastructure, how usage is billed, and which {{kib}} search tools are available. Use this page to compare the options and find the best fit for your operational needs.

:::::{stepper}

::::{step} Choose a deployment and get {{es}} running

You can choose from several deployment options for your search use cases with Elastic, including self-managed deployments, {{ech}}, and {{serverless-short}} projects.

1. Use the [](/deploy-manage/deploy/deployment-comparison.md) to learn how security, cluster management, monitoring, and data lifecycle differ. Choose the one that best fits your needs.

2. If you go with {{serverless-short}}, compare {{es-serverless}} and {{es}} {{vectordb}} by use case:

:::{include} _snippets/serverless-project-type-comparison.md
:::

:::{tip}
For most search workloads using vectors, the recommended option is a {{serverless-short}} {{es}} {{vectordb}} project. [Sign up for a free trial](https://cloud.elastic.co/registration?onboarding_token=vector).
:::

After you select a type, use the matching guide to get {{es}} running:

* {{serverless-short}}:
  * [{{es}} {{vectordb}}](/solutions/vector-database/get-started.md)
  * [{{es}} project](/solutions/elasticsearch-solution-project/get-started.md)
* [Self-managed](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md)
* [{{ece}}](/deploy-manage/deploy/cloud-enterprise/create-deployment.md)
* [{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md#eck-quickstart)
* [{{ech}}](/deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md)

::::

::::{step} Try a quickstart

These quickstarts show how to use {{es}} for search. They work on any deployment type:

* [](/solutions/search/get-started/index-basics.md): create an index, add documents, and run a search
* [](/solutions/search/get-started/keyword-search-python.md): build a search query with Python
* [](/solutions/search/get-started/semantic-search.md): run a semantic search with the `semantic_text` field type

::::

::::{step} Next step

After you have selected and started a deployment, get connected: find your endpoint and create an API key in [](/solutions/search/set-up/api-key-and-endpoints.md).

::::

:::::
