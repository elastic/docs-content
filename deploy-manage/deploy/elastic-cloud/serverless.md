---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/index.html
  - https://www.elastic.co/guide/en/serverless/current/intro.html
  - https://www.elastic.co/guide/en/serverless/current/general-serverless-status.html
applies_to:
  serverless:
products:
  - id: cloud-serverless
type: overview
---

# {{serverless-full}}

{{serverless-full}} lets you run Elastic without managing clusters, nodes, or scaling. You create serverless projects and Elastic provisions, upgrades, and autoscales them so you can focus on your data.

## Serverless overview

{{serverless-full}} automatically provisions, manages, and scales your {{es}} resources based on your actual usage. Unlike traditional deployments where you need to predict and provision resources in advance, serverless adapts to your workload in real-time, ensuring optimal performance while eliminating the need for manual capacity planning.

Serverless projects use the core components of the {{stack}}, such as {{es}} and {{kib}}, and are based on an architecture that decouples compute and storage. Search and indexing operations are separated, which offers high flexibility for scaling your workloads while ensuring a high level of performance.

:::{note}
There are differences between {{es-serverless}} and {{ech}}. Learn more in [Compare {{ech}} and {{es-serverless}}](../elastic-cloud.md#general-what-is-serverless-elastic-differences-between-serverless-projects-and-hosted-deployments-on-ecloud).
:::


## Benefits of serverless projects [_benefits_of_serverless_projects]

**Management free:** Elastic manages the underlying Elastic cluster, so you can focus on your data. With serverless projects, Elastic is responsible for automatic upgrades, data backups, and business continuity.

**Autoscaled:** To meet your performance requirements, the system automatically adjusts to your workloads. For example, when you have a short-term spike on the data you ingest, more resources are allocated for that period of time. When the spike is over, the system uses less resources, without any action on your end. Some project-level limits apply to ensure performance and stability, including a [limit on the number of indices per project](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-index-size) that can be adjusted by request.

**Optimized data storage:** Your data is stored in cost-efficient, general storage. A cache layer is available on top of the general storage for recent and frequently queried data that provides faster search speed. The size of the cache layer and the volume of data it holds depend on [settings](../../../deploy-manage/deploy/elastic-cloud/project-settings.md) that you can configure for each project.

**Dedicated experiences:** All serverless solutions are built on the Elastic Search Platform and include the core capabilities of the {{stack}}. They also each offer a distinct experience and specific capabilities that help you focus on your data, goals, and use cases.

**Pay per usage:** Each serverless project type includes product-specific and usage-based pricing.

**Data and performance control**. Control your project data and query performance against your project data.
  * **Data:** Choose the data you want to ingest and the method to ingest it. By default, data is stored indefinitely in your project, and you define the retention settings for your data streams.
  * **Performance:** For granular control over costs and query performance against your project data, serverless projects come with a set of predefined settings you can edit.

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::

## Get started [get-started]

Elastic provides four serverless project types on {{ecloud}}. {{es}}, Observability, and Security projects correspond to the same [solutions](/solutions/index.md) available on stateful deployments; {{es}} {{vectordb}} is an additional {{serverless-short}}-only project type.

Choose a type that matches your use case, then [create a serverless project](create-serverless-project.md).

### Explore the solution docs

If you're deciding which project type to create, these guides describe the capabilities and use cases for each one.

![elasticsearch](../../images/64x64_Color_elasticsearch-logo-color-64px.png "elasticsearch =30") **[{{es-serverless}}](/solutions/elasticsearch-solution-project.md)**  
Build powerful, scalable search and analytics applications across structured data, logs, metrics, documents, and vectors as part of a broader {{stack}}.

![vectordatabase](../../images/64x64_Color_vectordb-logo-color-64px.png "vectordatabase =30") **[{{es}} {{vectordb}}](/solutions/vector-database.md)**  
Build embedding-driven workloads such as semantic search, RAG, and AI-powered retrieval. Built-in models and vector-optimized defaults mean less configuration and faster time to production.

![observability](../../images/64x64_Color_observability-logo-color-64px.png "observability =30") **[{{obs-serverless}}](/solutions/observability.md)**  
Monitor your own platforms and services using powerful machine learning and analytics tools with your logs, metrics, traces, and APM data.

![security](../../images/64x64_Color_security-logo-color-64px.png "security =30") **[{{sec-serverless}}](/solutions/security.md)**  
Detect, investigate, and respond to threats with SIEM, endpoint protection, and AI-powered analytics capabilities.

## Next steps

* [Create a {{serverless-short}} project](create-serverless-project.md): After you decide on a project type, create a project in the {{ecloud}} console.

## Set up your environment

* [Create a project API key](../../api-keys/serverless-project-api-keys.md): Give applications and automations a key they can use to call your project's APIs.
* [Learn about your Cloud organization](../../cloud-organization.md): Understand how your projects, members, and account settings are grouped under one {{ecloud}} organization.
* [Understand serverless billing](../../cloud-organization/billing/serverless-project-billing-dimensions.md): See what you're charged for so you can estimate cost and control usage.
* [Learn how user access works](../../users-roles/cloud-organization.md): Invitations, roles, and SSO for your organization.
* [Review the {{serverless-full}} FAQ](serverless-faq.md): Review answers on pricing, regions, backups, and converting between project types.
* [Read the {{serverless-full}} blog](https://www.elastic.co/blog/elastic-cloud-serverless): More background on the product and architecture.
* [Check service status](../../cloud-organization/service-status.md): Current availability and updates when a cloud region is affected.
