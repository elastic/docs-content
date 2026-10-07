---
applies_to:
  stack:
  serverless:
navigation_title: Choose a deployment type
description: Select an Elasticsearch hosting model for search, compare Serverless project types, and start a deployment.
type: overview
---

# Choose a deployment type [choose-a-deployment-type]

{{es}} runs on several deployment types, and each type fits different operational needs.

The type you select sets who operates the cluster, how usage is billed, and which {{kib}} search tools you can use. This page helps you select the deployment type that fits your needs. 

:::{note}
For most search workloads using vectors, the recommended option is an [{{es}} {{vectordb}} project](/solutions/vector-database.md). Click here to get started with the {{vectordb}}. For a detailed comparison, use the resources in [Select a hosting model](#select-a-hosting-model).
:::

## Select a hosting model [select-a-hosting-model]

{{es}} supports these deployment types for search: [{{serverless-short}}](/deploy-manage/deploy/elastic-cloud/serverless.md) (an [{{es}} {{vectordb}} project](/solutions/vector-database.md) or an [{{es}} project](/solutions/elasticsearch-solution-project.md)), [{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md), and [self-managed](/deploy-manage/deploy/self-managed.md). Each hosting model affects who manages the cluster and how it is billed.

Use the following resources to compare hosting models:

1. Compare deployment options, including self-managed, {{ech}}, and {{serverless-short}}. Refer to [](/deploy-manage/deploy/deployment-comparison.md).
2. Compare {{es-serverless}} and {{es}} {{vectordb}}:

  :::{include} _snippets/serverless-project-type-comparison.md
  :::

## Start a deployment [start-a-deployment]

After you have selected a deployment type, start with one of these guides:

* {{es}} {{vectordb}} project: [](/solutions/vector-database/get-started.md)
* {{es}} project ({{serverless-short}}): [](/solutions/elasticsearch-solution-project/get-started.md)
* {{ech}}: [](/deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md)
* Self-managed: [](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md)

## Next step [choose-a-deployment-type-next]

After you have selected and started a deployment, get connected: find your endpoint and create an API key in [](/solutions/search/set-up/api-key-and-endpoints.md).
