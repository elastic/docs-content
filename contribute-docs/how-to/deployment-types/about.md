---
navigation_title: Deployment types reference
description: "Reference for docs contributors on Elastic's deployment types: what they are, the stack components and flavors available on each, and where user-facing tasks differ across them."
---

# Deployment types reference for docs contributors

This page covers what deployment types are, how they relate to {{stack}} components and flavors, and where the same task can require different steps on different deployment types.

## What deployment types are

Deployment types define the supported ways to provision and run the {{stack}} across different infrastructures and platforms: where and how to deploy.

- Deployment types are independent of [Elastic Solutions](/solutions/index.md) (Search, Security, {{observability}}). Solutions focus on use cases and functionality. Deployment types focus on infrastructure, lifecycle, and operational model.
- Some deployment types automate parts of the platform and {{stack}} lifecycle.
- Not all deployment types allow deploying every stack component.

## The deployment types

| Where and how to deploy | Deployment type |
|---|---|
| On your own premises, hardware, VMs, or cloud VMs with no orchestration | Self-managed |
| On {{ecloud}} (SaaS, platform handled by Elastic) | {{ech}} (ECH) |
| On {{ecloud}}, fully managed (platform and stack lifecycle handled by Elastic) | {{serverless-full}} |
| Self-managed orchestrator similar to ECH, but owned by you | {{ece}} (ECE) |
| On {{k8s}} | {{eck}} (ECK) |

For a user-facing overview, refer to [](/get-started/deployment-options.md). For the full user-facing deployment documentation, refer to [](/deploy-manage/index.md).

## Stack flavors

The {{stack}} has two flavors:

- **Versioned stack**: {{stack}} products released on a single cadence with a shared versioning pattern, designed to work tightly together based on a compatibility matrix. Often referred to as just "stack."
- **Serverless**: managed, unversioned, continuously delivered equivalents of some {{stack}} products, hosted by Elastic. Only {{es}}, {{kib}}, and {{fleet-server}} have a {{serverless-short}} equivalent today.

Some versioned and {{serverless-short}} products work together. For example, versioned {{ls}} or {{agent}} can send data to {{serverless-short}} {{es}}.

| Deployment type | Stack components available | Stack flavor |
|---|---|---|
| Self-managed | All components | Versioned stack |
| ECH | {{es}}, {{kib}}, {{integrations-server}} ({{fleet-server}} + {{apm-server}}), agentless integrations | Versioned stack |
| ECE | Same as ECH | Versioned stack |
| ECK | All components | Versioned stack |
| {{serverless-full}} | {{es}}, {{kib}}, {{fleet-server}} ({{serverless-short}} versions) | {{serverless-short}} |

### How flavors and deployment types map to `applies_to`

:::{include} /contribute-docs/_snippets/applies_to-stack-serverless.md
:::

For full context on `applies_to` dimensions, refer to [Dimensions](/contribute-docs/how-to/cumulative-docs/guidelines.md#dimensions).

## Components by deployment type

Not every stack component is available on every deployment type.

| Stack component | Deployment types |
|---|---|
| {{es}} | ECH, ECE, ECK, self-managed, {{serverless-short}} |
| {{kib}} | ECH, ECE, ECK, self-managed, {{serverless-short}} |
| {{ls}}, {{beats}}, {{agent}} | Self-managed, ECK (agentless integrations are now available on ECH) |
| {{fleet-server}} | ECH, ECE, ECK, self-managed, {{serverless-short}} |
| {{apm-server}} (or {{agent}} with {{product.apm}} integration) | ECH, ECE, ECK, self-managed |
| Client libraries | All deployment types |
| Maps server, {{package-registry}} | Self-managed, ECK |

## About each deployment type

### Self-managed

Users own the platform and the {{stack}}, with no orchestration or automation. Installation, configuration, and upgrades are all manual. The term "cluster" is used more often than "deployment."

:::{warning}
Some people refer to everything not hosted on {{ecloud}} as "self-managed" (grouping ECK, ECE, and self-managed together). **Don't use this grouping in published documentation.** ECK, ECE, and self-managed differ in meaningful ways that the grouping obscures. Always name the specific deployment type.
:::

### {{ech}} (ECH)

Elastic's SaaS offering: Elastic operates the platform, users own their deployments. Deployments ({{es}} + {{kib}} + {{integrations-server}}) are provisioned through the {{ecloud}} Console or API, using hardware profiles and {{es}} architectures offered by Elastic.

- **Configuration**: Partly automated (for example, communication between components). Some settings aren't user-configurable. Keystore settings, user settings, bundles, and plugins use higher-level abstractions.
- **Platform features**: Automatic snapshots, one-click upgrades, autoscaling, and private connectivity.

ECH is not a fully managed service. Users retain significant responsibility for their deployment.

### {{ece}} (ECE)

The self-managed version of the ECH platform, built on the same software. ECE lets organizations offer an ECH-like experience on their own infrastructure.

Not all ECH features are available in ECE: plugins, bundles, private links, and agentless integrations differ or are ECH-only. Unlike ECH, where the platform layer is Elastic SRE's responsibility and isn't documented, ECE platform administration is the customer's responsibility and is fully documented.

### {{eck}} (ECK)

A self-managed orchestrator that deploys {{stack}} components on {{k8s}}, with no platform UI similar to ECH or ECE. There are almost no restrictions on configuration flexibility, though mechanisms are adapted to {{k8s}}: files are added through volumes and volume mounts; plugins are added through init containers.

Connectivity, authentication, and authorization between components are applied automatically by the operator.

### {{serverless-full}}

Evolution of ECH on the same platform, aimed at being a fully managed version of {{es}} and {{kib}}. Users interact with {{serverless-full}} through "projects" rather than deployments.

Compared to ECH orchestration:

- **Automated or managed**: scaling, server security.
- **Opinionated**: cross-project user management only.
- **Limited**: no custom plugins or bundles.
- **Not yet available but planned**: user-controlled snapshot and restore, BYOK.

## Configuration tasks across deployment types

Even when a task is conceptually the same, the steps often differ across deployment types. In general, feature usage is usually the same across deployment types, while admin tasks are usually different.

| Task | Same or different? |
|---|---|
| Configure an `elasticsearch.yml` setting | Different. Steps depend on deployment type, because the configuration file isn't directly available in orchestrated deployments. |
| Configure something in the {{kib}} UI | Same across deployment types (exceptions for {{serverless-short}}). |
| Configure an {{es}} cluster-level or dynamic setting | Same across deployment types, because it's done through the {{es}} API (exceptions for {{serverless-short}}). |
| Add a config file to your {{es}} instance | Different. Steps depend on deployment type. |
| Install an {{agent}} to send data to {{es}} | Same across deployment types. Action is performed on clients. |
| Integrate a custom application using client libraries | Same across deployment types. Action is performed in client code. |
| Configure {{ilm-init}} policies | Same across deployment types; unavailable in {{serverless-short}}. |
