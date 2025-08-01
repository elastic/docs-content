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

We clearly mark content added or changed in a specific version using availability badges. The availability badges appear in page and section headers. 

#### Elastic Stack example

```yaml {applies_to}
stack: ga 9.1
```

This means the feature is:
* Available on Elastic Stack
* Generally Available (GA)
* Introduced in version 9.1.0

#### Serverless example

```yaml {applies_to}
serverless:
  security: beta
  elasticsearch: ga
```
* Applies to {{serverless-full}} 
* Generally Available for {{es}} projects
* Beta for {{elastic-sec}} projects

#### Elastic Cloud Enterprise example

```yaml {applies_to}
deployment:
  ece: deprecated 4.1.0
```
* Applies to {{ece}}
* Deprecated starting in {{ece}} version 4.1.0

:::{tip}
Want to learn more about how availability badges are used? Check the [Elastic Docs syntax guide](https://elastic.github.io/docs-builder/syntax/applies/).
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

% ### How do I know what the current {{stack}} version is?

% To make sure you're always viewing the most up-to-date and relevant documentation, the version dropdown at the % top of each page shows the most recent 9.x release. For example, Elastic Stack 9.0+ (latest: 9.1.0).

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
| **Deployment type** | The environment where the feature is available, for example, {{stack}}, {{serverless-full}}, {{ece}} (ECE), {{eck}} (ECK) |
| **Lifecycle state** | The development or support status of the feature, for example, GA and Beta |
| **Version** | The specific version the lifecycle state applies to |

### Lifecycle states

| Lifecycle state | Description |
|-------|-------------|
| **Generally Available (GA)** | Production-ready feature. When unspecified, GA is the default |
| **Beta** | Feature is nearing general availability but not yet production-ready |
| **Technical preview** | Feature is in early development stage |
| **Unavailable** | Feature is not supported in this deployment type or version |

### Examples of where availability can vary

| Category | Example |
|-------|-------------|
| **Elastic Stack versions** | [Elastic Stack](the-stack.md) version 9.0.0 and later, including 9.1.0 |
| **Deployment types** | [Elastic Cloud Serverless](/deploy-manage/deploy/elastic-cloud/serverless.md), [Elastic Cloud Hosted](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md), [Elastic Cloud Enterprise (ECE)](/deploy-manage/deploy/cloud-enterprise.md), [Elastic Cloud on Kubernetes (ECK)](/deploy-manage/deploy/cloud-on-k8s.md), and [Self-managed deployments](/deploy-manage/deploy/self-managed.md) |
| **Deployment versions** | [Elastic Cloud Enterprise (ECE)](/deploy-manage/deploy/cloud-enterprise.md) 4.0.0 and later, [Elastic Cloud on Kubernetes (ECK)](/deploy-manage/deploy/cloud-on-k8s.md) 3.0.0 and later |
| **Serverless project types** | {{es}}, {{observability}}, and {{elastic-sec}}

## Find docs for your product version

Find the documentation for your Elastic product versions or releases.

### Elastic Stack product versions

| Product | Version |
| --- | --- |
| [Elasticsearch](/release-notes/elasticsearch.md) | 9.0.0 and later |
| [Kibana](/release-notes/kibana.md) | 9.0.0 and later |
| [Fleet and Elastic Agent](/release-notes/fleet.md) | 9.0.0 and later |
| [Logstash](/release-notes/logstash.md) | 9.0.0 and later |
| [Beats](/release-notes/beats.md) | 9.0.0 and later |
| [Elastic Observability](/release-notes/observability.md) | 9.0.0 and later |
| [Elastic APM](/release-notes/apm.md) | 9.0.0 and later |
| [Elastic Security](/release-notes/security.md) | 9.0.0 and later |

### Deployment type versions or releases

| Product | Version or release |

| All [Elastic Cloud Serverless](/release-notes/cloud-serverless.md) project types | All releases |
| [Elastic Cloud Hosted](/release-notes/cloud-hosted.md) | All releases for January 2025 and later  |
| [Elastic Cloud Enterprise](/release-notes/cloud-enterprise.md) | 4.0.0 and later |
| [Elastic Cloud on Kubernetes](/release-notes/cloud-on-k8s.md) | 3.0.0 and later |

### Schema, library, and tool versions

| Product | Version or release
| --- | --- |
| [Elasticsearch Java Client](/release-notes/elasticsearch/clients/java.md) | 9.0.0 and later |
| [Elasticsearch JavaScript Client](/release-notes/elasticsearch/clients/javascript.md) | 9.0.0 and later |
| [Elasticsearch .NET Client](/release-notes/elasticsearch/clients/dotnet.md) | 9.0.0 and later |
| [Elasticsearch PHP Client](/release-notes/elasticsearch/clients/php.md) | 9.0.0 and later |
| [Elasticsearch Python Client](/release-notes/elasticsearch/clients/python.md) | 9.0.0 and later |
| [Elasticsearch Ruby Client](/release-notes/elasticsearch/clients/ruby.md) | 9.0.0 and later |
| [Elastic Common Schema (ECS)](/release-notes/ecs.md) | 9.0.0 and later |
| [ECS Logging .NET library](/reference/ecs/logging/dotnet.md) | 8.18.1 and later |
| [ECS Logging Go (Logrus) library](/reference/ecs/logging/go-logrus.md) | 1.0.0 and later |
| [ECS Logging Go (Zap) library](/reference/ecs/logging/go-zap.md) | 1.0.3 and later |
| [ECS Logging Go (Zerolog) library](/reference/ecs/logging/go-zerolog.md) | 0.2.0 and later |
| [ECS Logging Java library](/reference/ecs/logging/java.md) | 1.x and later |
| [ECS Logging Node.js library](/reference/ecs/logging/nodejs.md) | 1.5.3 and later |
| [ECS Logging PHP library](/reference/ecs/logging/php.md) | 2.0.0 and later |
| [ECS Logging Python library](/reference/ecs/logging/python.md) | 2.2.0 and later |
| [ECS Logging Ruby library](/reference/ecs/logging/ruby.md) | 1.0.0 and later |
| [Elasticsearch for Apache Hadoop]((/release-notes/elasticsearch-hadoop.md)) | 9.0.0 and later |
| [Elasticsearch Curator](/reference/elasticsearch/curator.md) | 8.0.0 and later |
| [Elastic Cloud Control (ECCTL)](/release-notes/ecctl.md) | 1.14.0 and later |
| [Elastic Serverless Forwarder for AWS](/reference/aws-forwarder.md) | 1.20.1 and later |
| [Elastic integrations](/reference/integrations/all_integrations.md) | All versions |
| [Search UI JavaScript library](/reference/search-ui.md) | 1.24.0 and later |

### APM agent and tool versions

| Product | Version |
| --- | --- |
| [Elastic Distribution of OpenTelemetry Android](/release-notes/edot/sdks/android.md) | 0.1.0 and later |
| [Elastic Distribution of OpenTelemetry iOS](/release-notes/edot/sdks/ios.md) | 1.0.0 and later |
| [Elastic Distribution of OpenTelemetry Java](/release-notes/edot/sdks/java.md) | 1.0.0 and later |
| [Elastic Distribution of OpenTelemetry .NET](/release-notes/edot/sdks/dotnet.md) | 1.0.0 and later |
| [Elastic Distribution of OpenTelemetry Node.js](/release-notes/edot/sdks/node.md) | 0.1.0 and later |
| [Elastic Distribution of OpenTelemetry Python](/release-notes/edot/sdks/python.md) | 0.1.0 and later |
| [Elastic Distribution of OpenTelemetry PHP](/release-notes/edot/sdks/php.md) | 0.1.0 and later |
| [Elastic APM .NET Agent](/release-notes/apm/agents/dotnet.md) | 1.0.0 and later |
| [Elastic APM Go Agent](/release-notes/apm/agents/go.md) | 2.0.0 and later |
| [Elastic APM Java Agent](/release-notes/apm/agents/java.md) | 1.0.0 and later |
| [Elastic APM Node.js Agent](/release-notes/apm/agents/nodejs.md) | 4.0.0 and later |
| [Elastic APM PHP Agent](/release-notes/apm/agents/php.md) | 1.0.0 and later |
| [Elastic APM Python Agent](/release-notes/apm/agents/python.md) | 6.0.0 and later |
| [Elastic APM Ruby Agent](/release-notes/apm/agents/ruby.md) | 4.0.0 and later |
| [Elastic APM Real User Monitoring JavaScript Agent](/release-notes/apm/agents/rum-js.md) | 5.0.0 and later |
| [Elastic APM AWS Lambda extension](/release-notes/release-notes/apm/aws-lambda/release-notes.md) | 1.0.0 and later |
| [Elastic APM Attacher for Kubernetes](/reference/apm/k8s-attacher.md) | 1.1.3 |








