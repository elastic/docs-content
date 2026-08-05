---
navigation_title: Deployment types reference
description: "Reference for docs contributors on Elastic's deployment types: what they are, the stack components and flavors available on each, and where user-facing tasks differ across them."
---

# Deployment types reference for docs contributors

Deployment types define the supported ways to provision and run the {{stack}} across different infrastructures and platforms: where and how to deploy.

- Deployment types are independent of [Elastic Solutions](/solutions/index.md) (Search, Security, {{observability}}). Solutions focus on use cases and functionality. Deployment types focus on infrastructure, lifecycle, and operational model.
- Some deployment types automate parts of the platform and {{stack}} lifecycle.
- Not all deployment types allow deploying every stack component.

This page provides an overview of the available deployment types, how they relate to {{stack}} components and flavors, and a primer on where the same task can require different steps on different deployment types.

## Deployment types

The supported deployment types differ by where the {{stack}} runs and how much of the platform Elastic operates.

| Deployment type | Where and how to deploy |
|---|---|
| Self-managed | On your own premises, hardware, VMs, or cloud VMs with no orchestration |
| {{ech}} (ECH) | On {{ecloud}} (SaaS, platform handled by Elastic) |
| {{ece}} (ECE) | Self-managed orchestrator similar to ECH, but owned by you |
| {{eck}} (ECK) | On {{k8s}} |
| {{serverless-full}} | On {{ecloud}}, fully managed (platform and stack lifecycle handled by Elastic) |

For a user-facing overview, refer to [](/get-started/deployment-options.md). For the full user-facing deployment documentation, refer to [](/deploy-manage/index.md).

### Deployments in detail

Review the following sections to learn the basics of each deployment type, and what's distinctive about it.

:::{dropdown} Self-managed
Users own the platform and the {{stack}}, with no orchestration or automation. Installation, configuration, and upgrades are all manual. In this context, the term "cluster" is used more often than "deployment", even though components other than {{es}} are not part of a cluster directly.
:::

:::{dropdown} {{ech}} (ECH)
Elastic's SaaS offering: Elastic operates the platform, users own their deployments. Deployments are discrete instances of the {{stack}} (such as an {{es}} cluster + {{kib}} + {{integrations-server}}) that are provisioned through the {{ecloud}} Console or API, using hardware profiles and {{es}} architectures offered by Elastic.

- **Configuration**: Partly automated (for example, communication between components). Some settings aren't user-configurable. Keystore settings, user settings, bundles, and plugins use higher-level abstractions.
- **Platform features**: Automatic snapshots, one-click upgrades, autoscaling, and private connectivity.

ECH is not a fully managed service. Users retain significant responsibility for their deployment.

ECH is hosted on {{ecloud}}, which is a common platform that it shares with {{serverless-short}} and certain services offered through [Cloud Connect](/deploy-manage/cloud-connect.md). This means that some configurations can be managed centrally, and then shared across ECH deployments and {{serverless-short}} projects. Common areas include, but are not limited to, user management, network security, and billing.
:::

:::{dropdown} {{ece}} (ECE)
The self-managed version of the ECH platform, built on the same software. ECE lets organizations offer an ECH-like experience on their own infrastructure.

Not all ECH features are available in ECE: plugins, bundles, private links, and agentless integrations differ or are ECH-only. Unlike ECH, where the platform layer is Elastic SREs' responsibility and isn't documented, ECE platform administration is the customer's responsibility and is fully documented.
:::

:::{dropdown} {{eck}} (ECK)
A self-managed orchestrator that deploys {{stack}} components on {{k8s}}, with no platform UI (like the ones provided by ECH or ECE). There are almost no restrictions on configuration flexibility, though mechanisms are adapted to {{k8s}}: files are added through volumes and volume mounts; plugins are added through init containers.

Connectivity, authentication, and authorization between components are applied automatically by the operator but can be customized.
:::

:::{dropdown} {{serverless-full}}
An evolution of ECH on the same platform, aimed at being a fully managed version of {{es}} and {{kib}}. Users interact with {{serverless-full}} through "projects" rather than deployments.

Compared to ECH orchestration:

* Some things are **automated / managed**: scaling, server security
* Some things are **opinionated**: cross project user management only
* Some things are **limited**: no custom plugins or bundles
* Some things are **not yet available** (but planned): no user-controlled snapshot/restore, BYOK, etc.

{{serverless-short}} is hosted on {{ecloud}}, which is a common platform that it shares with ECH and certain services offered through [Cloud Connect](/deploy-manage/cloud-connect.md). This means that some configurations can be managed centrally, and then shared across ECH deployments and {{serverless-short}} projects. Common areas include, but are not limited to, user management, network security, and billing.
:::

:::{include} /contribute-docs/_snippets/self-managed-naming.md
:::

## Deployments and the stack

The {{stack}} has two flavors:

- **Versioned stack**: {{stack}} products released on a single cadence with a shared versioning pattern, designed to work tightly together based on a compatibility matrix. Often referred to as just "the stack."
- **Serverless**: Managed, unversioned, continuously delivered equivalents of some {{stack}} products, hosted by Elastic. Only {{es}}, {{kib}}, and {{fleet-server}} have a {{serverless-short}} equivalent today.

Some versioned and {{serverless-short}} products work together. For example, versioned {{ls}} or {{agent}} can send data to {{serverless-short}} {{es}}. 

In other cases, versioned {{stack}} components deployed on a particular orchestrator can work together with components deployed by other means. For example, you can manually deploy {{ls}}, or deploy it with {{eck}}, and have it send data to {{es}} deployed on ECE.

Highly orchestrated deployments of the versioned stack, such as ECH and ECE, and managed versions of the stack ({{serverless-full}}), concentrate on core and server-side components. Client-side components (which usually feed data to the stack) don't need to be hosted on the same platform to perform their functions.

| Deployment type | Stack components available | Stack flavor |
|---|---|---|
| Self-managed | All components (manual install) | Versioned stack |
| ECH | {{es}}, {{kib}}, {{integrations-server}} ({{fleet-server}} + {{apm-server}}), agentless integrations | Versioned stack |
| ECE | {{es}}, {{kib}}, {{integrations-server}} ({{fleet-server}} + {{apm-server}}), agentless integrations | Versioned stack |
| ECK | All components | Versioned stack |
| {{serverless-full}} | {{es}}, {{kib}}, {{fleet-server}} ({{serverless-short}} versions) | {{serverless-short}} |

::::{tip} - Where stack flavor and deployment type collide
:::{include} /contribute-docs/_snippets/applies_to-stack-serverless.md
:::

For details, refer to [Dimensions](/contribute-docs/how-to/cumulative-docs/guidelines.md#dimensions).
::::

## Configuration tasks across deployment types

Even when a task is conceptually the same, the steps often differ across deployment types. 

*In general*, **feature usage** is usually the **same** across deployment types (with some exceptions for {{serverless-short}}), while **admin tasks** are usually **different** or have exceptions.

| Task | Same or different? |
|---|---|
| Configure an `elasticsearch.yml` setting | **Different.** Steps depend on deployment type, because the configuration file isn't directly available in orchestrated deployments. |
| Configure something in the {{kib}} UI | **Same** across deployment types (exceptions for {{serverless-short}}). |
| Configure an {{es}} cluster-level or dynamic setting | **Same** across deployment types, because it's done through the {{es}} API (exceptions for {{serverless-short}}). |
| Add a config file to your {{es}} instance | **Different.** Steps depend on deployment type. |
| Install an {{agent}} to send data to {{es}} | **Same** across deployment types. Action is performed on clients. |
| Integrate a custom application using client libraries | **Same** across deployment types. Action is performed in client code. |
| Configure {{ilm-init}} policies | **Same** across deployment types; unavailable in {{serverless-short}}. |


## Next steps

Now that you know the basics of each deployment type, you can learn more about [how to document features that vary by deployment type](/contribute-docs/how-to/deployment-types/strategies.md).
