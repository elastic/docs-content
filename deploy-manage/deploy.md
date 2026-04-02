---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/intro.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-deploy.html
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/get-elastic.html
products:
  - id: cloud-serverless
  - id: elasticsearch
  - id: elastic-stack
---

# Deploy

Whether you're planning to use Elastic's pre-built solutions or Serverless projects, build your own applications with {{es}}, or analyze your data using {{kib}} tools, you need to deploy Elastic first.

This page will help you understand your deployment options and choose the approach that best fits your needs.

## Core components

All deployments include **{{es}}**. {{es}} is the distributed search and analytics engine, scalable data store, and vector database at the heart of all Elastic solutions.

In most cases, you also need to deploy **{{kib}}**. {{kib}} provides the user interface for all Elastic solutions and Serverless projects. It’s a powerful tool for visualizing and analyzing your data, and for managing and monitoring the {{stack}}. Although {{kib}} is not required to use {{es}}, it's required for most use cases, and is included by default when you deploy using certain deployment methods.

Your choice of deployment type determines how you'll set up and manage these core components, as well as any additional components you need.

:::{admonition} Other {{stack}} components
This section focuses on deploying and managing {{es}} and {{kib}}, as well as supporting orchestration technologies. However, depending on your use case, you might need to deploy [other {{stack}} components](/get-started/the-stack.md). For example, you might need to add components to ingest logs or metrics.

To learn how to deploy optional {{stack}} components, refer to the following sections:
* [Fleet and Elastic Agent](/reference/fleet/index.md)
* [APM](/solutions/observability/apm/index.md)
* [Beats](beats://reference/index.md)
* [Logstash](logstash://reference/index.md)
:::

## Choosing your deployment type

:::{include} _snippets/deployment-options-overview.md
:::

::::{tip}
Documentation will specify when certain features or configurations are not applicable to specific deployment types.
::::

### Who manages the infrastructure?

#### Managed by Elastic

If you want to focus on using Elastic products rather than managing infrastructure, choose one of the following options:

- **{{serverless-full}}**: Zero operational overhead, automatic scaling and updates, latest features
- **{{ech}}**: Balance of control and managed operations, choice of resources and regions

Both of these options use [{{ecloud}}](/deploy-manage/deploy/elastic-cloud.md) as the orchestration platform.

#### Self-hosted options

If you need to run Elastic on your infrastructure, choose between a fully self-managed deployment or using an orchestrator:

- **Fully self-managed**: Complete control and responsibility for your Elastic deployment
- **With orchestration**:
  - **{{eck}} (ECK)**: If you need Kubernetes-native orchestration
  - **{{ece}} (ECE)**: If you need a multi-tenant orchestration platform

:::{admonition} Use cloud services in your self-hosted environment with Cloud Connect
With [Cloud Connect](/deploy-manage/cloud-connect.md), you can use Elastic-managed cloud services in your self-managed, ECE, or ECK environment without having to install and manage their infrastructure yourself. In this way, you can get faster access to new features without adding to your operational overhead.
::::

### About orchestration

An orchestrator automates the deployment and management of multiple Elastic clusters, handling tasks like scaling, upgrades, and monitoring.

Consider orchestration in the following cases:
- You need to manage multiple Elastic clusters
- You want automated operations at scale
- You have a Kubernetes environment (ECK)
- You need to build a multi-tenant platform (ECE)

Orchestrators manage the lifecycle of your Elastic deployments but don't change how the core products work. When using an orchestrated deployment:
- You'll still use the same {{es}} and {{kib}} features and configurations
- Most product documentation remains applicable
- You can add other Elastic products as needed
- The orchestrator handles operational tasks while you focus on using and configuring the products

### Versioning and compatibility

In {{serverless-full}}, you automatically get access to the latest versions of Elastic features and you don't need to manage version compatibility.

With other deployment types (fully self-managed, ECH, ECE, and ECK), you control which {{stack}} versions you deploy and when you upgrade. The ECE and ECK orchestrators themselves also receive regular version updates, independent of the {{stack}} versions they manage.

Consider this when choosing your deployment type:

- Choose {{serverless-full}} if you want automatic access to the latest features and don't want to manage version compatibility
- Choose other deployment types if you need more control over version management

:::{tip}
Learn more about [versioning and availability](/get-started/versioning-availability.md).
:::

### Cost considerations

- **{{serverless-full}}**: Pay for what you use
- **{{ech}}**: Subscription-based with resource allocation
- **Self-hosted options**, **including fully self-managed, ECE, and ECK**: Infrastructure costs plus operational overhead mean a higher total cost of ownership (TCO)

:::::{tip}
For a detailed comparison of features and capabilities across deployment types, see the [](./deploy/deployment-comparison.md).
:::::
