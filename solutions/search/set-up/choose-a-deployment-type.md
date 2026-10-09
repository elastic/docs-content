---
applies_to:
  stack:
  serverless:
navigation_title: Choose a deployment type
description: Select an Elasticsearch deployment model for search, compare Serverless project types, and start a deployment.
type: overview
---

# Choose a deployment type [choose-a-deployment-type]

{{es}} runs on several deployment types, and each type fits different operational needs. The type you select sets who operates the cluster, how usage is billed, and which {{kib}} search tools you can use. This page helps you select the deployment type that fits your needs.

:::::{stepper}

::::{step} Select a deployment model

Elastic supports the following deployment types for search: self-managed, {{ece}} (ECE), {{eck}} (ECK), {{ech}} (ECH), and {{serverless-short}} (an {{es}} {{vectordb}} project or an {{es}} project).

1. Use the [](/deploy-manage/deploy/deployment-comparison.md) to learn how security, cluster management, monitoring, and data lifecycle differ. Choose the one that best fits your needs.

2. If you go with {{serverless-short}}, compare {{es-serverless}} and {{es}} {{vectordb}}:

:::{include} _snippets/serverless-project-type-comparison.md
:::

:::{tip}
For most search workloads using vectors, the recommended option is a {{serverless-short}} {{es}} {{vectordb}} project. [Start your {{es}} {{vectordb}} project](https://cloud.elastic.co/registration?onboarding_token=vector).
:::

::::

::::{step} Start a deployment

After you have selected a deployment type, use the following guides to start a deployment:

* [](/solutions/vector-database/get-started.md)
* [](/solutions/elasticsearch-solution-project/get-started.md)
* [](/deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md)
* [](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md)

::::

::::{step} Next step

After you have selected and started a deployment, get connected: find your endpoint and create an API key in [](/solutions/search/set-up/api-key-and-endpoints.md).

::::

:::::
