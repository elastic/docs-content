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

{{serverless-full}} lets you run {{es}}, {{vectordb}}, {{observability}}, and Security as fully managed serverless projects - no cluster management, no capacity planning, no upgrades. Elastic manages the infrastructure so you can focus on your data.


## How {{serverless-short}} works

In {{serverless-short}}, the resource you work with is a _project_, and each project is dedicated to a single use case. Projects belong to an {{ecloud}} organization, where users, roles, and billing are managed.

Serverless projects use the core components of the {{stack}}, such as {{es}} and {{kib}}, and are based on an architecture that decouples compute and storage. Search and indexing operations are separated, which offers high flexibility for scaling your workloads while ensuring a high level of performance.

Rather than scaling to the capacity you provision in advance, {{serverless-short}} scales to your actual usage in real time, so you don't size or tune resources for peak load.

{{serverless-short}} projects are versionless and continuously updated by Elastic, so you never select a {{stack}} version or plan an upgrade. Your connections and configurations are unaffected by updates, and API versioning and quality testing keep your clients compatible. Although the `GET /` root API returns a version number, it is used as a [client compatibility version](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-version-reporting).

Setup is brief. You sign up for a trial or log in to an existing organization, then create a project in the {{ecloud}} console. There is nothing to install or size, and your project is ready in minutes. 

:::{admonition} Not sure which deployment type fits your needs?
Compared to {{ech}}, {{ece}}, {{eck}}, and self-managed clusters, {{serverless-short}} takes the infrastructure decisions away: you no longer select node counts, hardware profiles, or {{stack}} versions, and you no longer perform upgrades or snapshots. In exchange, some cluster-level capabilities are unavailable in {{serverless-short}}, such as authentication realms, user-initiated snapshots, and custom plugins.

[Compare](/deploy-manage/deploy/elastic-cloud.md#general-what-is-serverless-elastic-differences-between-serverless-projects-and-hosted-deployments-on-ecloud) the core features and capabilities of {{ech}} and {{es-serverless}}, then review the [feature-level comparison](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md) to check the specific features you depend on.
:::

### Benefits of serverless projects [_benefits_of_serverless_projects]

**Management free:** Elastic manages the underlying Elastic cluster, so you can focus on your data. With serverless projects, Elastic is responsible for automatic upgrades, data backups, and business continuity.

**Autoscaled:** To meet your performance requirements, the system automatically adjusts to your workloads. For example, when you have a short-term spike on the data you ingest, more resources are allocated for that period of time. When the spike is over, the system uses less resources, without any action on your end. Some project-level limits apply to ensure performance and stability, including a [limit on the number of indices per project](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-index-size) that can be adjusted by request.

**Optimized data storage:** Your data is stored in cost-efficient, general storage. A cache layer is available on top of the general storage for recent and frequently queried data that provides faster search speed. The size of the cache layer and the volume of data it holds depend on [settings](/deploy-manage/deploy/elastic-cloud/project-settings.md) that you can configure for each project.

**Dedicated experiences:** All serverless solutions are built on the Elastic Search Platform and include the core capabilities of the {{stack}}. They also each offer a distinct experience and specific capabilities that help you focus on your data, goals, and use cases.

**Pay per usage:** Each serverless project type includes product-specific and usage-based pricing.

**Data and performance control**. Control your project data and query performance against your project data.
  * **Data:** Choose the data you want to ingest and the method to ingest it. By default, data is stored indefinitely in your project, and you define the retention settings for your data streams.
  * **Performance:** For granular control over costs and query performance against your project data, serverless projects come with a set of predefined settings you can edit.

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::


## Section overview

This section covers the tasks you perform to create, configure, and manage serverless projects. Start with the two steps that get a project running, then use the configuration pages to tune the project to your workload.

### Get started [get-started]

Setting up {{serverless-short}} takes two steps: choose the project type that matches your use case, then create the project.

::::::{stepper}

:::::{step} Choose a project type

Each {{serverless-short}} project is purpose-built for a specific use case. {{es}}, Observability, and Security projects correspond to the same [solutions](/solutions/index.md) available on stateful deployments; {{es}} {{vectordb}} is an additional {{serverless-short}}-only project type.

| Project type | Use case | What you get |
| --- | --- | --- |
| [{{es-serverless}}](/solutions/elasticsearch-solution-project.md) | You're building search-powered applications and want direct control over indices, queries, and clients | Search and analytics across structured data, logs, metrics, documents, and vectors, with UI tools such as Agent Builder and query rules |
| [{{es}} {{vectordb}}](/solutions/vector-database.md) | Your workload is embedding-driven, such as semantic search, RAG, or AI-powered retrieval | Built-in models and vector-optimized defaults, so you write less configuration to get to production |
| [{{obs-serverless}}](/solutions/observability.md) | You're monitoring the health and performance of your own applications and infrastructure | Logs, metrics, traces, and APM data with prebuilt dashboards, SLOs, and alerting |
| [{{sec-serverless}}](/solutions/security.md) | You're detecting, investigating, and responding to security threats | SIEM, endpoint protection, detection rules, and AI-powered analytics |

For [{{observability}}](/solutions/observability/observability-serverless-feature-tiers.md) and [Security](/solutions/security/security-serverless-feature-tiers.md) projects, you also select a feature tier, which determines which capabilities are available and how the project is billed. You can change the tier later in [project settings](/deploy-manage/deploy/elastic-cloud/project-settings.md#project-features-add-ons).

::::{tip}
Not sure which to choose? Start with the {{es}} solution for general-purpose search and analytics if you don't need the additional features of {{product.observability}}, {{product.security}}, or the preconfigured defaults of {{es}} {{vectordb}}.
::::

:::::

:::::{step} Create your project

[Create a serverless project](/deploy-manage/deploy/elastic-cloud/create-serverless-project.md) in the {{ecloud}} console, either as part of a free trial or in an existing organization. You select the project type and the [region](/deploy-manage/deploy/elastic-cloud/regions.md) during setup, and the project is ready in a few minutes.

A project's type is fixed after you create it, but you can create as many projects as you need and you are charged only for your usage. That means you can create one project of each type to evaluate them side by side, then delete the ones you don't keep.

:::::

::::::

### Configure and manage your project

After you create a project, review these pages to learn about the settings you can control and the tools you can use to manage projects at scale.

* [](/deploy-manage/deploy/elastic-cloud/regions.md): Review the available AWS, Azure, and GCP regions. You select a region during setup and you are unable to change it afterwards, so it affects latency and where your data resides.
* [](/deploy-manage/deploy/elastic-cloud/project-settings.md): Configure Search AI Lake settings, feature tiers, tags, and connection aliases. These settings are your main controls over data retention, query performance, and cost.
* [](/deploy-manage/deploy/elastic-cloud/manage-serverless-projects-using-api.md): Create and manage projects programmatically with the [{{serverless-full}} API]({{cloud-serverless-apis}}), for provisioning at scale or as part of your own automations. Calls are authenticated with an [{{ecloud}} API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md).
* [](/deploy-manage/deploy/elastic-cloud/serverless-faq.md): Find answers to common questions about pricing, regions, moving data, backups, authentication, converting between project types, and support.

## Other important sections

Review these other sections for critical information about billing, data movement, security, and operating serverless projects.

### Billing and pricing

Because projects are billed on usage rather than provisioned capacity, your costs follow the volume of data you ingest and retain, how much of that data you keep search-ready, and the project type and feature tier you select.

* [](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md): Learn about the usage dimensions you're charged for so you can estimate cost and control usage.
* Pricing for [{{es-serverless}}](https://www.elastic.co/pricing/serverless-search), [{{es}} {{vectordb}}](https://cloud.elastic.co/pricing/serverless?s=vectordb), [{{observability}}](https://www.elastic.co/pricing/serverless-observability), and [{{sec-serverless}}](https://www.elastic.co/pricing/serverless-security).
* [](/deploy-manage/monitor/autoops/autoops-for-serverless.md): Monitor usage patterns and billing dimensions in your project.

### Move data to and from serverless

Projects and hosted deployments are based on different architectures, so you are unable to convert a {{serverless-full}} project into an {{ech}} deployment, or the other way around. Moving between them means moving your data. To bring existing data into a project, or to move it elsewhere, use one of the following methods.

* [](/manage-data/migrate/migrate-data-using-reindex-api.md): Copy documents from a source deployment into a project using reindex from remote.
* [](/manage-data/migrate/migrate-with-logstash.md): Move data to and from {{serverless-short}} projects using {{ls}} with {{es}} input and output plugins.

Elastic backs up your projects and is responsible for business continuity, so you are unable to request project backups or take your own snapshots. If you experience data loss or corruption, you can request an emergency restore by [contacting Support](/troubleshoot/index.md#contact-us).

### Secure and control access

Learn how to control access to your organization and projects. {{serverless-short}} does not support [{{es}} authentication realms](/deploy-manage/users-roles/cluster-or-deployment-auth/authentication-realms.md). User authentication is managed at the {{ecloud}} organization level, and project-level access is handled through API keys.

* [](/deploy-manage/cloud-organization.md): Learn how your projects, members, and account settings are grouped under one {{ecloud}} organization.
* [](/deploy-manage/users-roles/cloud-organization.md): Learn how user access works in your organization, including invitations, roles, and SSO.
* [](/deploy-manage/users-roles/serverless-custom-roles.md): Create project-level roles for more tailored access.
* [](/deploy-manage/api-keys/serverless-project-api-keys.md): Authenticate applications, service accounts, and automation against a single project's APIs.
* [](/deploy-manage/api-keys/elastic-cloud-api-keys.md): Authenticate against organization-level APIs, or create one key that spans multiple projects. These keys are required for the {{serverless-full}} API and for {{cps}}.
* [](/deploy-manage/security/ip-filtering-cloud.md): Limit how your projects can be accessed by IP address.
* [](/deploy-manage/security/private-connectivity.md): Connect to your projects over your cloud provider's private network.
* [Browser access requirements](/deploy-manage/deploy/elastic-cloud.md#browser-access): Allow required domains, including `kibana.estccdn.com`. If this domain is blocked, {{kib}} might appear as a blank page.
* [Elastic Trust Center](https://www.elastic.co/trust): Compliance and privacy standards for the Elastic platform.

### Monitor and get support

Elastic operates and monitors the infrastructure behind your project, so your own monitoring focuses on project usage, performance, and service availability rather than cluster internals.

* [](/deploy-manage/monitor/autoops/autoops-for-serverless.md): View health, performance, and usage data for your project.
* [](/deploy-manage/cloud-organization/service-status.md): Check current availability and subscribe to updates when a cloud region is affected.
* [Raise a support case](/troubleshoot/index.md#contact-us): Raise a case for your subscription as you do today. In the body of the case, mention you are working with a {{serverless-short}} project.
* [](/deploy-manage/cross-project-search-config.md): Search across serverless projects in the same organization.

### Learn more

Use these resources to go deeper on how {{serverless-short}} is built, what's planned, and how projects compare to other deployment types.

* [{{serverless-full}} architecture blog](https://www.elastic.co/blog/elastic-cloud-serverless): More background on the product and architecture.
* [{{serverless-full}} roadmap](https://www.elastic.co/cloud/serverless/roadmap): Upcoming features.
* [](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md): Feature-level comparison with {{ech}}.
* [](/deploy-manage/deploy/elastic-cloud/tools-apis.md): APIs, clients, and other tools for {{ecloud}} organizations, hosted deployments, and serverless projects.
