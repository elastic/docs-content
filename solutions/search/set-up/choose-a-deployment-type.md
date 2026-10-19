---
applies_to:
  stack:
  serverless:
navigation_title: Choose a deployment type
description: Select an Elasticsearch deployment model for search, get it running, and try a search quickstart.
type: overview
---

# Choose a deployment type [choose-a-deployment-type]

{{es}} is at the core of every Elastic deployment type. The deployment type you choose determines who manages the infrastructure, scaling, and upgrades, and how usage is billed. Use this page to compare the options and find the best fit for your operational needs.

:::::{stepper}

::::{step} Choose a deployment and get {{es}} running

Get {{es}} running in a few minutes.

**Try for free on {{ecloud}}**


* **[{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md)**: Elastic automatically scales and upgrades the project.
  * **[{{es}} {{vectordb}} project](/solutions/vector-database/get-started.md)**: For most search workloads, this is the recommended option. It is optimized for vector workloads, such as [RAG](/solutions/search/rag.md), [recommendations](/solutions/search/vector/vector-search-use-cases.md#discovery-and-recommendations), and [multimodal search](/solutions/search/multimodal-search.md). Sign up for a [14-day free trial](https://cloud.elastic.co/registration?onboarding_token=vector).
  * **[{{es}} project](/solutions/elasticsearch-solution-project/get-started.md)**: If you have logs, events, time series, or telemetry data, choose this project type. Sign up for a [14-day free trial](https://cloud.elastic.co/serverless-registration).
* **[{{ech}}](/deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md)**: You size, scale, and upgrade the cluster yourself, and you select the hardware profile it runs on. Sign up for a [14-day free trial](https://cloud.elastic.co/registration).

**Run locally**

* **[Local development](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md)**: Get started quickly with {{es}} and {{kib}} in Docker for local development and testing. Refer to [](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md).

Elastic also offers other deployment types. Refer to the [deployment comparison](/deploy-manage/deploy/deployment-comparison.md) to learn about them in detail.

If {{es}} is running, try a quickstart tutorial to index data and run a search in a few minutes.

::::

::::{step} Try a quickstart

These quickstarts show how to use {{es}} for search:

* [](/solutions/search/get-started/index-basics.md): create an index, add documents, and run a search
* [](/solutions/vector-database/vector-full-text-search.md): connect a client and run full-text, semantic, and hybrid search
* [](/solutions/search/get-started/keyword-search-python.md): build a search query with Python

::::

::::{step} Next step

After you have selected and started a deployment, get connected: find your endpoint and create an API key in [](/solutions/search/set-up/api-key-and-endpoints.md).

::::

:::::
