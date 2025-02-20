---
mapped_urls:
  - https://www.elastic.co/guide/en/serverless/current/intro.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-deploy.html
---

# Deploy

% What needs to be done: Write from scratch

% GitHub issue: https://github.com/elastic/docs-projects/issues/334

% Scope notes: does plan for production content go here?  With orchestrator layer - explain relationship between orchestrator and clusters  how to help people to be aware of the other products that might need to be deployed? "these are the core products, you might add others on"  describe relationship between orchestrators and ES  Explain that when using orchestrators a lot of the reference configuration of the orchestrated applications is still applicable. The user needs to learn how to configure the applications when using an orchestrator, then afterwards, the documentation of the application will be valid and applicable to their use case. When a certain feature or configuration is not applicable in some deployment types, the document will specify it.

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/docs-content/serverless/intro.md
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/elasticsearch-intro-deploy.md

Whether you're planning to use Elastic's pre-built solutions or Serverless projects, build your own applications with {{es}}, or analyze your data using {{kib}} tools, you'll need to deploy Elastic first.

This page will help you understand your deployment options and choose the approach that best fits your needs.

## Core components

Every Elastic deployment requires Elasticsearch as its core data store and search/analytics engine.
Additionally, Kibana provides the user interface for all Elastic solutions and Serverless projects. It is required for most use cases, from data exploration to monitoring and security analysis.

Your choice of deployment type determines how you'll set up and manage these core components, plus any additional components you need.

Elastic offers deployment options ranging from fully automated to fully self-managed.

:::{tip}
Learn more about the [{{stack}}](/get-started/the-stack.md) to understand the core and optional components of an Elastic deployment.
::: 

## Deployment types overview

:::{include} _snippets/deployment-options-overview.md
:::

## Versioning and compatability 

In {{serverless-full}}, you automatically get access to the latest versions of Elastic features and you don't need to manage version compatibility.

All other deployment types use stack versioning, where components are tested and versioned together to ensure compatibility. ECE and ECK have their own deployment versions, in addition to stack versioning.

Consider this when choosing your deployment type:

- Choose Serverless if you want automatic access to the latest features and don't want to manage version compatibility
- Choose other deployment types if you need more control over version management

:::{tip}
Learn more about [versioning and availability](/get-started/versioning-availability.md). 
:::

## Choose your deployment path

Your deployment choice determines how you'll set up and manage these components.

### Step 1: Who manages the infrastructure?

#### Managed by Elastic

If you want to focus on using Elastic products rather than managing infrastructure, choose:

- **Serverless**: Zero operational overhead, automatic scaling and updates, latest features
- **Cloud hosted**: Balance of control and managed operations, choice of resources and regions

#### Self-managed with your infrastructure

If you need to run Elastic on your infrastructure, you have three options:

- **Basic self-managed**: Direct control over all aspects of deployment
- **Elastic Cloud on Kubernetes (ECK)**: Kubernetes-native orchestration
- **Elastic Cloud Enterprise (ECE)**: Multi-tenant orchestration platform

### Step 2: For self-managed - do you need orchestration?

If you chose self-managed, consider whether you need orchestration:

- **No orchestration needed**:
  Choose basic self-managed deployment for full control and direct management

- **Kubernetes environment**:
  Use ECK for native Kubernetes orchestration and automated operations

- **Multi-tenant platform**:
  Use ECE to deploy {{ecloud}} on your own infrastructure

## Cost considerations

- **Serverless**: Pay for what you use
- **Cloud hosted**: Subscription-based with resource allocation
- **Self-managed options**: Infrastructure costs plus operational overhead mean a higher total cost of ownership (TCO)
