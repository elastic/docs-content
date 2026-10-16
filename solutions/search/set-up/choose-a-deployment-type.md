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

Select a deployment type below to get {{es}} running.

**Quick start options**

* **[{{ecloud}}](/deploy-manage/deploy/elastic-cloud.md)**: Includes {{serverless-full}} and {{ech}}. Both run on {{ecloud}}, in the cloud provider and region of your choice.
  * **[{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md)**: Includes the {{es}} {{vectordb}} project and the {{es}} project. Elastic scales and upgrades the project, so you can focus on your data:
    * **[{{es}} {{vectordb}} project](/solutions/vector-database/get-started.md)**: For most search workloads, this is the recommended option. It is optimized for vector workloads and uses a vector-tuned default configuration, with a hardware profile suited to embeddings. Sign up for a [14-day free trial](https://cloud.elastic.co/registration?onboarding_token=vector).
    * **[{{es}} project](/solutions/elasticsearch-solution-project/get-started.md)**: If you have logs, events, time series, or telemetry data, this is the recommended option. Use it for data that is written continuously and queried by time range, such as telemetry data, application logs, or metrics. Sign up for a [14-day free trial](https://cloud.elastic.co/serverless-registration).
  * **[{{ech}}](/deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md)**: You size, scale, and upgrade the cluster yourself, and you select the hardware profile it runs on. Sign up for a [14-day free trial](https://cloud.elastic.co/registration).
* **[Local development](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md)**: Get started quickly with {{es}} and {{kib}} in Docker for local development and testing. Refer to [](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md).

**Advanced options**

* **[Self-managed](/deploy-manage/deploy/self-managed.md)**: Install, configure, and run Elastic on your own premises.
* **[{{ece}}](/deploy-manage/deploy/cloud-enterprise/create-deployment.md)**: Deploy {{ecloud}} on public or private clouds, virtual machines, or your own premises.
* **[{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md#eck-quickstart)**: Deploy {{ecloud}} on Kubernetes.

For a detailed comparison of all available deployment types, refer to the [deployment comparison](/deploy-manage/deploy/deployment-comparison.md).

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
