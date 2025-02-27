---
mapped_urls:
  - https://www.elastic.co/guide/en/serverless/current/intro.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-deploy.html
---

% What needs to be done: Write from scratch

% GitHub issue: https://github.com/elastic/docs-projects/issues/334

% Scope notes: does plan for production content go here?  With orchestrator layer - explain relationship between orchestrator and clusters  how to help people to be aware of the other products that might need to be deployed? "these are the core products, you might add others on"  describe relationship between orchestrators and ES  Explain that when using orchestrators a lot of the reference configuration of the orchestrated applications is still applicable. The user needs to learn how to configure the applications when using an orchestrator, then afterwards, the documentation of the application will be valid and applicable to their use case. When a certain feature or configuration is not applicable in some deployment types, the document will specify it.

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/docs-content/serverless/intro.md
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/elasticsearch-intro-deploy.md

# Deploy

Whether you're planning to use Elastic's pre-built solutions or Serverless projects, build your own applications with {{es}}, or analyze your data using {{kib}} tools, you'll need to deploy Elastic first.

This page will help you understand your deployment options and choose the approach that best fits your needs.

## Core components

Every Elastic deployment requires {{es}} as its core data store and search/analytics engine.
Additionally, {{kib}} provides the user interface for all Elastic solutions and Serverless projects. It is required for most use cases, from data exploration to monitoring and security analysis.

Your choice of deployment type determines how you'll set up and manage these core components, plus any additional components you need.

:::{tip}
Learn more about the [{{stack}}](/get-started/the-stack.md) to understand the core and optional components of an Elastic deployment.
:::

## Choosing your deployment type

:::{include} _snippets/deployment-options-overview.md
:::

### Who manages the infrastructure?

#### Managed by Elastic

If you want to focus on using Elastic products rather than managing infrastructure, choose:

- **Serverless**: Zero operational overhead, automatic scaling and updates, latest features
- **Cloud hosted**: Balance of control and managed operations, choice of resources and regions

#### Self-hosted options

If you need to run Elastic on your infrastructure, choose between a fully self-managed deployment or using an orchestrator:

- **Fully self-managed**: Complete control and responsibility for your Elastic deployment
- **With orchestration**:
  - **Elastic Cloud on Kubernetes (ECK)**: If you need Kubernetes-native orchestration
  - **Elastic Cloud Enterprise (ECE)**: If you need a multi-tenant orchestration platform

:::::{note}
:::{dropdown} About orchestration

An orchestrator automates the deployment and management of multiple Elastic clusters, handling tasks like scaling, upgrades, and monitoring.

Consider orchestration if you:
- Need to manage multiple Elastic clusters
- Want automated operations at scale
- Have a Kubernetes environment (ECK)
- Need to build a multi-tenant platform (ECE)

Orchestrators manage the lifecycle of your Elastic deployments but don't change how the core products work. When using ECK or ECE:
- You'll still use the same Elasticsearch and Kibana features and configurations
- Most product documentation remains applicable
- You can add other Elastic products as needed
- The orchestrator handles operational tasks while you focus on using and configuring the products

::::{tip}
Documentation will specify when certain features or configurations are not applicable to specific deployment types.
::::
:::
:::::

### Versioning and compatibility 

In {{serverless-full}}, you automatically get access to the latest versions of Elastic features and you don't need to manage version compatibility.

With other deployment types ({{ecloud}} Hosted, ECE, and ECK), you control which {{stack}} versions you deploy and when you upgrade. The ECE and ECK orchestrators themselves also receive regular version updates, independent of the {{stack}} versions they manage.

Consider this when choosing your deployment type:

- Choose Serverless if you want automatic access to the latest features and don't want to manage version compatibility
- Choose other deployment types if you need more control over version management

:::{tip}
Learn more about [versioning and availability](/get-started/versioning-availability.md). 
:::

### Cost considerations

- **Serverless**: Pay for what you use
- **Cloud hosted**: Subscription-based with resource allocation
- **Self-hosted options**: Infrastructure costs plus operational overhead mean a higher total cost of ownership (TCO)

:::::{tip}
For a detailed comparison of features and capabilities across deployment types, see the [Deployment comparison reference](./deploy/deployment-comparison.md).
:::::
