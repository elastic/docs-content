---
applies_to:
  stack:
  serverless:
navigation_title: Get {{es}} running
description: Select an {{es}} deployment model for search, get it running, and try a search quickstart.
type: overview
---

# Get {{es}} running for search [get-elasticsearch-running-for-search]

{{es}} is at the core of every Elastic deployment type. The deployment type you choose determines who manages the infrastructure, scaling, and upgrades, and how usage is billed. This page briefly introduces the deployment types you can use to get {{es}} running quickly, and points you to resources that compare them in detail.

:::::{stepper}

::::{step} Choose a deployment and get {{es}} running

Get {{es}} running in a few minutes.

### Try for free on {{ecloud}}

* **{{serverless-full}}**: Elastic automatically scales and upgrades the project. Projects are versionless, so you always get the latest features.
  
  Serverless has two project types optimized for different search workloads. Choose the one that matches your data and use case:
  
  * **[{{es}} {{vectordb}} project](/solutions/vector-database/get-started.md)**: For most search workloads, this is the recommended option. It is optimized for vector workloads, such as [RAG](/solutions/search/rag.md), recommendations, and [multimodal search](/solutions/search/multimodal-search.md). Sign up for a [14-day free trial](https://cloud.elastic.co/registration?onboarding_token=vector).
  * **[{{es}} project](/solutions/elasticsearch-solution-project/get-started.md)**: If you have logs, events, time series, or telemetry data, choose this project type. Sign up for a [14-day free trial](https://cloud.elastic.co/serverless-registration).
* **[{{ech}}](/deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md)**: You size, scale, and upgrade the cluster yourself, and you select the hardware profile it runs on. The cluster runs a specific {{stack}} version. Sign up for a [14-day free trial](https://cloud.elastic.co/registration).

### Run locally

* **[Local development](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md)**: Get started quickly with {{es}} and {{kib}} in Docker for local development and testing.

:::{tip}
These are the fastest ways to get {{es}} running for search. Elastic offers additional deployment types for production workloads on your own infrastructure. 

For more detail on the options listed here, and to compare all deployment types across factors like data residency, compliance, feature availability, and infrastructure control, refer to the [full list of deployment options](/deploy-manage/deploy.md) and the [detailed feature comparison](/deploy-manage/deploy/deployment-comparison.md).
:::

::::

::::{step} Try a quickstart

Once you have {{es}} running, try a quickstart tutorial:

* [](/solutions/vector-database/vector-full-text-search.md): Connect a client and run full-text, semantic, and hybrid search. You can follow the examples in Python, TypeScript, PHP, Ruby, C#/.NET, Java, or Go.
* [](/solutions/search/get-started/index-basics.md): Create an index, add documents, and run a search. This tutorial goes further into indices, including dynamic and explicit mappings.
* [](/solutions/search/get-started/keyword-search-python.md): Build a keyword search query with Python.

::::

::::{step} Next step

After you have selected and started a deployment, get connected: find your endpoint and create an API key in [](/solutions/search/set-up/api-key-and-endpoints.md).

::::

:::::
