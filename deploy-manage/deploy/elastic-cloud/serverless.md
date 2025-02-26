---
mapped_urls:
  - https://www.elastic.co/guide/en/serverless/current/index.html
  - https://www.elastic.co/guide/en/serverless/current/intro.html
  - https://www.elastic.co/guide/en/serverless/current/general-serverless-status.html
applies_to:
  serverless:
---

# {{serverless-full}}

{{serverless-full}} is a fully managed solution that allows you to deploy and use Elastic for your use cases without managing the underlying infrastructure. It represents a shift in how you interact with {{es}} - instead of managing clusters, nodes, data tiers, and scaling, you create **serverless projects** that are fully managed and automatically scaled by Elastic. This abstraction of infrastructure decisions allows you to focus solely on gaining value and insight from your data.

## Serverless overview

{{serverless-full}} automatically provisions, manages, and scales your {{es}} resources based on your actual usage. Unlike traditional deployments where you need to predict and provision resources in advance, serverless adapts to your workload in real-time, ensuring optimal performance while eliminating the need for manual capacity planning.

Serverless projects use the core components of the {{stack}}, such as {{es}} and {{kib}}, and are based on an architecture that decouples compute and storage. Search and indexing operations are separated, which offers high flexibility for scaling your workloads while ensuring a high level of performance.

:::{note}
There are differences between {{es-serverless}} and {{ech}}, for a list of differences between them, see [differences between {{ech}} and {{es-serverless}}](../elastic-cloud.md#general-what-is-serverless-elastic-differences-between-serverless-projects-and-hosted-deployments-on-ecloud).
:::

## Get started

Elastic provides three serverless solutions available on {{ecloud}}. Follow these guides to get started with your serverless project:

* **[{{es-serverless}}](../../../solutions/search/serverless-elasticsearch-get-started.md)**: Build powerful applications and search experiences using a rich ecosystem of vector search capabilities, APIs, and libraries.
* **[{{obs-serverless}}](../../../solutions/observability/get-started/create-an-observability-project.md)**: Monitor your own platforms and services using powerful machine learning and analytics tools with your logs, metrics, traces, and APM data.
* **[{{sec-serverless}}](../../../solutions/security/get-started/create-security-project.md)**: Detect, investigate, and respond to threats with SIEM, endpoint protection, and AI-powered analytics capabilities.

Afterwards, you can:

* Learn about the [cloud organization](../../cloud-organization.md) that is the umbrella for all of your Elastic Cloud resources, users, and account settings.
* Learn about how {{es-serverless}} is [billed](../../cloud-organization/billing/serverless-project-billing-dimensions.md).
* Learn how to [create an API key](../../api-keys/serverless-project-api-keys.md). This key provides access to the API that enables you to manage your deployments.
* Learn how manage [users and roles](../../users-roles/cloud-organization.md) in your {{es-serverless}} deployment.
* Learn more about {{serverless-full}} in [our blog](https://www.elastic.co/blog/elastic-cloud-serverless).

## Benefits of serverless projects [_benefits_of_serverless_projects]

**Management free:** Elastic manages the underlying Elastic cluster, so you can focus on your data. With serverless projects, Elastic is responsible for automatic upgrades, data backups, and business continuity.

**Autoscaled:** To meet your performance requirements, the system automatically adjusts to your workloads. For example, when you have a short time spike on the data you ingest, more resources are allocated for that period of time. When the spike is over, the system uses less resources, without any action on your end.

**Optimized data storage:** Your data is stored in cost-efficient, general storage. A cache layer is available on top of the general storage for recent and frequently queried data that provides faster search speed. The size of the cache layer and the volume of data it holds depend on [settings](../../../deploy-manage/deploy/elastic-cloud/project-settings.md) that you can configure for each project.

**Dedicated experiences:** All serverless solutions are built on the Elastic Search Platform and include the core capabilities of the Elastic Stack. They also each offer a distinct experience and specific capabilities that help you focus on your data, goals, and use cases.

**Pay per usage:** Each serverless project type includes product-specific and usage-based pricing.

**Data and performance control**. Control your project data and query performance against your project data. 
  * **Data:** Choose the data you want to ingest and the method to ingest it. By default, data is stored indefinitely in your project, and you define the retention settings for your data streams. 
  * **Performance:** For granular control over costs and query performance against your project data, serverless projects come with a set of predefined settings you can edit.

## Monitor serverless status [general-serverless-status]

Serverless projects run on cloud platforms, which may undergo changes in availability. When availability changes, Elastic makes sure to provide you with a current service status.

To learn more about serverless status, see [Service status](../../cloud-organization/service-status.md).

## Answers to common serverless questions [general-what-is-serverless-elastic-answers-to-common-serverless-questions]

**Is there migration support between hosted deployments and serverless projects?**

Migration paths between hosted deployments and serverless projects are currently unsupported.

**How can I move data to or from serverless projects?**

We are working on data migration tools! In the interim, [use Logstash](https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-logstash.html) with Elasticsearch input and output plugins to move data to and from serverless projects.

**How does serverless ensure compatibility between software versions?**

Connections and configurations are unaffected by upgrades. To ensure compatibility between software versions, quality testing and API versioning are used.

**Can I convert a serverless project into a hosted deployment, or a hosted deployment into a serverless project?**

Projects and deployments are based on different architectures, and you are unable to convert.

**Can I convert a serverless project into a project of a different type?**

You are unable to convert projects into different project types, but you can create as many projects as you’d like. You will be charged only for your usage.

**How can I create serverless service accounts?**

Create API keys for service accounts in your serverless projects. Options to automate the creation of API keys with tools such as Terraform will be available in the future.

To raise a Support case with Elastic, raise a case for your subscription the same way you do today. In the body of the case, make sure to mention you are working in serverless to ensure we can provide the appropriate support.

**Where can I learn about pricing for serverless?**

See serverless pricing information for [Search](https://www.elastic.co/pricing/serverless-search), [Observability](https://www.elastic.co/pricing/serverless-observability), and [Security](https://www.elastic.co/pricing/serverless-security).

**Can I request backups or restores for my projects?**

It is not currently possible to request backups or restores for projects, but we are working on data migration tools to better support this.
