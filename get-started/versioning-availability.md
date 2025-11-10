---
navigation_title: Versioning and availability
mapped_pages:
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/introducing-elastic-documentation.html
applies_to:
  serverless:
  stack:
products:
  - id: elastic-stack
description: Learn how Elastic handles versioning and feature availability in the docs. Find the product versions that are supported, how to read availability badges, and...
---

# Versioning and availability

Learn how Elastic products are versioned, the lifecycle of features, and how to find the relevant documentation for your deployment type and product version. Find answers to common questions about the versioning and confidently navigate our continuously updated documentation.

## Understanding versioning

Many components of the [{{stack}}](/get-started/the-stack.md) (such as {{es}} and {{kib}}) share the same versioning pattern.
In Elastic documentation, this group of components is typically referred to as the {{stack}}.

Orchestrators such as {{ece}} and {{eck}}, and other tools such as code clients and SDKs, are versioned independently of the {{stack}}. The {{ecloud}} console and {{serverless-short}} projects are always automatically updated with the latest changes.

Need docs for an earlier version? Go to [elastic.co/guide](https://www.elastic.co/guide).

### Why doesn't Elastic have separate documentation for each version?

Starting with {{stack}} 9.0.0, Elastic no longer publishes separate documentation sets for each minor release. Instead, all changes in the 9.x series are included in a single, continuously updated documentation set.

This approach helps:
* Reduce duplicate pages
* Show a feature's full history and context
* Simplify search and navigation

### How do I know content was added in a specific version?

We clearly mark content added or changed in a specific version using availability badges. The availability badges appear in page headers, section headers, and inline.

#### Elastic Stack example

```{applies_to}
stack: ga 9.1
```

This means the feature is:
* Available on {{stack}}
* Generally Available (GA)
* Introduced in version 9.1.0

#### Serverless example

```{applies_to}
serverless:
  security: beta
  elasticsearch: ga
```

This means the feature is:
* Generally Available for {{es-serverless}} projects
* Beta for {{sec-serverless}} projects

#### Elastic Cloud Enterprise example

```{applies_to}
deployment:
  ece: deprecated 4.1.0
```

This means the feature is:
* Available on {{ece}}
* Deprecated starting in version 4.1.0

:::{tip}
Want to learn more about how we use availability badges? Check out the [Elastic Docs syntax guide](https://elastic.github.io/docs-builder/syntax/applies/).
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

To ensure you're always viewing the most up-to-date and relevant documentation, the version dropdown at the top of each page shows the most recent 9.x release. For example, 9.0+.

## Understanding {{stack}} versioning

The components of the {{stack}} typically use semantic versioning in the `X.Y.Z` format, such as `9.0.0`.

| Version | Description |
| ----- | ----- |
| Major (X) | Indicates significant changes, such as new features, breaking changes, and major enhancements. Upgrading to a new major version may require changes to your existing setup and configurations. |
| Minor (Y) | Introduces new features and improvements, while maintaining backward compatibility with the previous minor versions within the same major version. Upgrading to a new minor version should not require any changes to your existing setup. |
| Patch (Z) | Contains bug fixes and security updates, without introducing new features or breaking changes. Upgrading to a new patch version should be seamless and not require any changes to your existing setup. |

Understanding versioning is essential for [upgrade planning](/deploy-manage/upgrade.md) and ensuring compatibility, particularly for the self-managed [deployment option](/get-started/deployment-options.md).

## Availability of features

Available features can differ based on deployment type, product lifecycle stage, and specific version.

### Feature availability factors

| Factor | Description |
| ----- | ----- |
| Deployment type | The environment where the feature is available, for example, self-managed, {{serverless-full}}, {{ece}}, {{eck}} |
| Lifecycle state | The development or support status of the feature, for example, GA, Technical preview, Beta |
| Version | The specific version the lifecycle state applies to |

### Lifecycle states

| Lifecycle state | Description |
| ----- | ----- |
| Technical preview | Feature is in early development stage |
| Beta | Feature is nearing general availability, but not yet production ready |
| Generally Available (GA) | Production-ready feature. When unspecified, GA is the default |
| Deprecated | Feature is still usable, but is planned to be removed or replaced in a future update |
| Removed | Feature can no longer be used |
| Unavailable | Feature is unsupported in this deployment type or version |

### Examples of where availability can vary

| Category | Example |
| ----- | ----- |
| {{stack}} versions | [{{stack}}](/get-started/the-stack.md) version 9.0.0 and later, including 9.1.0 |
| Deployment types | [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md), [{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md), [{{ece}}](/deploy-manage/deploy/cloud-enterprise.md), [{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md), and [Self-managed deployments](/deploy-manage/deploy/self-managed.md) |
| Orchestrator versions | [{{ece}}](/deploy-manage/deploy/cloud-enterprise.md) 4.0.0 and later, [{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md) 3.0.0 and later |
| Serverless project types | {{es}}, Elastic {{observability}}, and {{elastic-sec}} |

## Find docs for your product version

Find the documentation for your Elastic product versions or releases.

### Elastic Stack product versions

| Product | Version |
| ----- | ----- |
| [Elasticsearch](https://www.elastic.co/docs/release-notes/elasticsearch) | 9.0.0 and later |
| [Kibana](https://www.elastic.co/docs/release-notes/kibana) | 9.0.0 and later |
| [Fleet and Elastic Agent](https://www.elastic.co/docs/release-notes/fleet) | 9.0.0 and later |
| [Logstash](https://www.elastic.co/docs/release-notes/logstash) | 9.0.0 and later |
| [Beats](https://www.elastic.co/docs/release-notes/beats) | 9.0.0 and later |
| [Elastic Observability](https://www.elastic.co/docs/release-notes/observability) | 9.0.0 and later |
| [Elastic APM](https://www.elastic.co/docs/release-notes/apm) | 9.0.0 and later |
| [Elastic Security](https://www.elastic.co/docs/release-notes/security) | 9.0.0 and later |

### Deployment type versions or releases

| Product | Version or release |
| ----- | ----- |
| All [Elastic Cloud Serverless](https://www.elastic.co/docs/release-notes/cloud-serverless) project types | All releases |
| [Elastic Cloud Hosted](https://www.elastic.co/docs/release-notes/cloud-hosted) | All releases for January 2025 and later |
| [Elastic Cloud Enterprise](https://www.elastic.co/docs/release-notes/cloud-enterprise) | 4.0.0 and later |
| [Elastic Cloud on Kubernetes](https://www.elastic.co/docs/release-notes/cloud-on-k8s) | 3.0.0 and later |

### Schema, library, and tool versions

| Product | Version or release |
| ----- | ----- |
| [Elasticsearch Java Client](https://www.elastic.co/docs/release-notes/elasticsearch/clients/java) | 9.0.0 and later |
| [Elasticsearch JavaScript Client](https://www.elastic.co/docs/release-notes/elasticsearch/clients/javascript) | 9.0.0 and later |
| [Elasticsearch .NET Client](https://www.elastic.co/docs/release-notes/elasticsearch/clients/dotnet) | 9.0.0 and later |
| [Elasticsearch PHP Client](https://www.elastic.co/docs/release-notes/elasticsearch/clients/php) | 9.0.0 and later |
| [Elasticsearch Python Client](https://www.elastic.co/docs/release-notes/elasticsearch/clients/python) | 9.0.0 and later |
| [Elasticsearch Ruby Client](https://www.elastic.co/docs/release-notes/elasticsearch/clients/ruby) | 9.0.0 and later |
| [Elastic Common Schema (ECS)](https://www.elastic.co/docs/release-notes/ecs) | 9.0.0 and later |
| [ECS Logging .NET library](https://www.elastic.co/docs/reference/ecs/logging/dotnet) | 8.18.1 and later |
| [ECS Logging Go (Logrus) library](https://www.elastic.co/docs/reference/ecs/logging/go-logrus) | 1.0.0 and later |
| [ECS Logging Go (Zap) library](https://www.elastic.co/docs/reference/ecs/logging/go-zap) | 1.0.3 and later |
| [ECS Logging Go (Zerolog) library](https://www.elastic.co/docs/reference/ecs/logging/go-zerolog) | 0.2.0 and later |
| [ECS Logging Java library](https://www.elastic.co/docs/reference/ecs/logging/java) | 1.x and later |
| [ECS Logging Node.js library](https://www.elastic.co/docs/reference/ecs/logging/nodejs) | 1.5.3 and later |
| [ECS Logging PHP library](https://www.elastic.co/docs/reference/ecs/logging/php) | 2.0.0 and later |
| [ECS Logging Python library](https://www.elastic.co/docs/reference/ecs/logging/python) | 2.2.0 and later |
| [ECS Logging Ruby library](https://www.elastic.co/docs/reference/ecs/logging/ruby) | 1.0.0 and later |
| [Elasticsearch for Apache Hadoop](https://www.elastic.co/docs/release-notes/elasticsearch-hadoop) | 9.0.0 and later |
| [Elasticsearch Curator](https://www.elastic.co/docs/reference/elasticsearch/curator) | 8.0.0 and later |
| [Elastic Cloud Control (ECCTL)](https://www.elastic.co/docs/release-notes/ecctl) | 1.14.0 and later |
| [Elastic Serverless Forwarder for AWS](https://www.elastic.co/docs/reference/aws-forwarder) | 1.20.1 and later |
| [Elastic integrations](https://www.elastic.co/docs/reference/integrations/all_integrations) | All versions |
| [Search UI JavaScript library](https://www.elastic.co/docs/reference/search-ui) | 1.24.0 and later |

### APM agent and tool versions

| Product | Version |
| ----- | ----- |
| [Elastic Distribution of OpenTelemetry Android](https://www.elastic.co/docs/release-notes/edot/sdks/android) | 0.1.0 and later |
| [Elastic Distribution of OpenTelemetry iOS](https://www.elastic.co/docs/release-notes/edot/sdks/ios) | 1.0.0 and later |
| [Elastic Distribution of OpenTelemetry Java](https://www.elastic.co/docs/release-notes/edot/sdks/java) | 1.0.0 and later |
| [Elastic Distribution of OpenTelemetry .NET](https://www.elastic.co/docs/release-notes/edot/sdks/dotnet) | 1.0.0 and later |
| [Elastic Distribution of OpenTelemetry Node.js](https://www.elastic.co/docs/release-notes/edot/sdks/node) | 0.1.0 and later |
| [Elastic Distribution of OpenTelemetry Python](https://www.elastic.co/docs/release-notes/edot/sdks/python) | 0.1.0 and later |
| [Elastic Distribution of OpenTelemetry PHP](https://www.elastic.co/docs/release-notes/edot/sdks/php) | 0.1.0 and later |
| [Elastic APM .NET Agent](https://www.elastic.co/docs/release-notes/apm/agents/dotnet) | 1.0.0 and later |
| [Elastic APM Go Agent](https://www.elastic.co/docs/release-notes/apm/agents/go) | 2.0.0 and later |
| [Elastic APM Java Agent](https://www.elastic.co/docs/release-notes/apm/agents/java) | 1.0.0 and later |
| [Elastic APM Node.js Agent](https://www.elastic.co/docs/release-notes/apm/agents/nodejs) | 4.0.0 and later |
| [Elastic APM PHP Agent](https://www.elastic.co/docs/release-notes/apm/agents/php) | 1.0.0 and later |
| [Elastic APM Python Agent](https://www.elastic.co/docs/release-notes/apm/agents/python) | 6.0.0 and later |
| [Elastic APM Ruby Agent](https://www.elastic.co/docs/release-notes/apm/agents/ruby) | 4.0.0 and later |
| [Elastic APM Real User Monitoring JavaScript Agent](https://www.elastic.co/docs/release-notes/apm/agents/rum-js) | 5.0.0 and later |
| [Elastic APM AWS Lambda extension](https://www.elastic.co/docs/release-notes/apm/aws-lambda/release-notes) | 1.0.0 and later |
| [Elastic APM Attacher for Kubernetes](https://www.elastic.co/docs/reference/apm/k8s-attacher) | 1.1.3 |

