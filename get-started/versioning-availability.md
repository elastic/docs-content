---
navigation_title: Versioning and availability
mapped_pages:
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/introducing-elastic-documentation.html
products:
  - id: elastic-stack
description: Learn how Elastic handles versioning and feature availability in the docs. Find the product versions that are supported, how to read availability badges, and...
---

# Versioning and availability in Elastic Docs

Learn how Elastic Docs handles versioning, feature availability, and how to find the right documentation for your deployment type and product version. Find answers to common questions about the Elastic Stack versioning and to help you confidently navigate our continuously updated documentation.

## Frequently asked questions

### Where can I find documentation for the latest version of the {{stack}}?

You’re in the right place! All documentation for Elastic Stack 9.0.0 and later is available at [elastic.co/docs](https://www.elastic.co/docs), including the latest 9.1.0 version and any future versions in the 9.x series.

Need docs for an earlier version? Go to [elastic.co/guide](https://www.elastic.co/guide).

### Why doesn't Elastic have separate documentation for each version?

Starting with {{stack}} 9.0.0, Elastic no longer publishes separate documentation sets for each minor release. Instead, all changes in the 9.x series are included in a single, continuously updated documentation set.

This approach helps:
* Reduce duplicate pages
* Show the full history and context of a feature
* Simplify search and navigation

### How do I know content was added in a specific version?

We clearly mark content added or changed in a specific version using availability badges.

For example:

```yaml {applies_to}
stack: ga 9.1
```

This means the feature is:
* Available on Elastic Stack
* Generally Available (GA)
* Introduced in version 9.1.0

Other examples:

```yaml {applies_to}
serverless:
  security: beta
  elasticsearch: ga
```
* Applies to {{serverless-full}}
* Beta for {{elastic-sec}} projects
* Generally Available for {{es}} projects

```yaml {applies_to}
deployment:
  ece: deprecated 4.1.0
```
* Applies to {{ece}}
* Deprecated starting in {{ece}} version 4.1.0

Look for the availability badges in page and section headers. 

:::{tip}
Want to learn more about how availability badges are used? Check the [Elastic docs syntax guide](https://elastic.github.io/docs-builder/syntax/applies/).
:::

### What if I'm using a version earlier than {{stack}} 9.0.0?

Documentation for {{stack}} 8.19.0 and earlier is available at [elastic.co/guide](https://www.elastic.co/guide).

If a previous version for a specific page exists, you can select the version from the dropdown in the page sidebar. 

### How often is the documentation updated?

We frequently update Elastic Docs to reflect the following:
* Minor versions, such as {{stack}} 9.1.0 
* Patch-level updates, such as {{stack}} 9.1.1
* Ongoing improvements to clarify and expand guidance

To learn what's changed, check the [release notes](/release-notes/index.md) for each Elastic product.

### How do I know what the current {{stack}} version is?

To make sure you're always viewing the most up-to-date and relevant documentation, the version dropdown at the top of each page shows the most recent 9.x release. For example, Elastic Stack 9.0+ (latest: 9.1.0).

## Understanding {{stack}} versioning

{{stack}} uses semantic versioning in the `X.Y.Z` format, such as `9.0.0`.

| Version | Description |
|-------|-------------|
| **Major (X)** | Indicates significant changes, such as new features, breaking changes, and major enhancements. Upgrading to a new major version may require changes to your existing setup and configurations. |
| **Minor (Y)** | Introduces new features and improvements, while maintaining backward compatibility with the previous minor versions within the same major version. Upgrading to a new minor version should not require any changes to your existing setup. |
| **Patch (Z)** | Contains bug fixes and security updates, without introducing new features or breaking changes. Upgrading to a new patch version should be seamless and not require any changes to your existing setup. |

Understanding {{stack}} versioning is essential for [upgrade planning](/deploy-manage/upgrade.md) and ensuring compatibility.

## Availability of features

The features available to you can differ based on deployment type, product lifecycle stage, and specific version.

### Feature availability factors

| Factor | Description |
|-------|-------------|
| **Deployment type** | The environment where the feature is available (Stack, Serverless, ECE, ECK, etc.) |
| **Lifecycle state** | The development or support status of the feature (GA, Beta, etc.) |
| **Version** | The specific version the lifecycle state applies to |

### Lifecycle states

| Lifecycle state | Description |
|-------|-------------|
| **Generally Available (GA)** | Production-ready feature (default if not specified) |
| **Beta** | Feature is nearing general availability but not yet production-ready |
| **Technical preview** | Feature is in early development stage |
| **Unavailable** | Feature is not supported in this deployment type or version |

### Examples of where availability can vary

- **[Elastic Stack](the-stack.md)** versions (for example, 9.0, 9.1)
- **Deployment types and versions** 
  - [Elastic Cloud Hosted](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md)
  - [Elastic Cloud Serverless](/deploy-manage/deploy/elastic-cloud/serverless.md)
  - [Self-managed deployments](/deploy-manage/deploy/self-managed.md)
  - [Elastic Cloud Enterprise (ECE)](/deploy-manage/deploy/cloud-enterprise.md)
    - ECE deployment versions (for example, 4.0.0)
  - [Elastic Cloud on Kubernetes (ECK)](/deploy-manage/deploy/cloud-on-k8s.md)
    - ECK deployment versions (for example, 3.0.0)
- **Serverless project types**
  - {{es}}
  - {{observability}}
  - {{elastic-sec}}

## Find docs for your product version

Find the documentation for your Elastic product versions.

### Core products and deployments

| Product | Version |
| --- | --- |
| {{stack}}<br><br>Includes {{es}}, {{kib}}, {{ls}}, {{fleet}}, <br>{{agent}}, Beats, APM, and query languages | 9.0.0+ |
| {{observability}} | 9.0.0+ |
| {{elastic-sec}} | 9.0.0+ |
| {{serverless-full}} (all project types) | All |
| {{ech}} | All*  |
| {{ece}} | 4.0.0+ |
| {{eck}} | 3.0.0+ |

\* Excludes release notes before January 2025

### Schemas, libraries, and tools

| Product | Version |
| --- | --- |
| Elastic Common Schema | 9.0.0+ |
| ECS logging Java library | 1.x+ |
| Other ECS logging libraries | All |
| {{es}} API clients | 9.0.0+ |
| {{es}} for Apache Hadoop | 9.0.0+ |
| Curator | 8.0+ |
| Elastic Cloud Control (ECCTL) | 1.14+ |
| Elastic Serverless Forwarder | All |
| Elastic integrations | All |
| Elastic Search UI library | All |

### APM agents and tools

| Product | Version |
| --- | --- |
| APM Android agent | 1.x+ |
| APM .NET agent | 1.x+ |
| APM Go agent | 2.x+ |
| APM iOS agent | 1.x+ |
| APM Java agent | 1.x+ |
| APM Node.js agent | 4.x+ |
| APM PHP agent | All |
| APM Python agent | 6.x+ |
| APM Ruby agent | 4.x+ |
| APM Real User Monitoring JavaScript agent | 5.x+ |
| APM attacher for Kubernetes | All |



