---
navigation_title: Versioning and availability
mapped_pages:
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/introducing-elastic-documentation.html
products:
  - id: elastic-stack
description: Learn how Elastic handles versioning and feature availability in the docs. Find the product versions that are supported, how to read availability badges, and...
---

# Versioning and availability in Elastic Docs

Learn how Elastic Docs handles versioning, feature availability, and how to find the right documentation for your deployment type and product version. Find answers to common questions about the Elastic Stack versioning and confidently navigate our continuously updated documentation.

## Frequently asked questions

### Where can I find documentation for the latest version of the {{stack}}?

You’re in the right place! All documentation for Elastic Stack 9.0.0 and later is available at [elastic.co/docs](https://www.elastic.co/docs), including the latest {{version.stack| M.M}} version and any future versions in the 9.x series.

Need docs for an earlier version? Go to [elastic.co/guide](https://www.elastic.co/guide).

### Why doesn't Elastic have separate documentation for each version?

Starting with {{stack}} 9.0.0, Elastic no longer publishes separate documentation sets for each minor release. Instead, all changes in the 9.x series are included in a single, continuously updated documentation set.

This approach helps:
* Reduce duplicate pages
* Show the full history and context of a feature
* Simplify search and navigation

### How do I know content was added in a specific version?

We clearly mark content added or changed in a specific version using availability badges. The availability badges appear in page headers, section headers, and inline.

#### Elastic Stack example

```{applies_to}
stack: ga 9.1
```

This means the feature is:
* Available on Elastic Stack
* Generally Available (GA)
* Introduced in version 9.1.0

#### Serverless example

```{applies_to}
serverless:
  security: beta
  elasticsearch: ga
```

This means the feature is:
* Generally Available for {{es}} Serverless projects
* Beta for {{elastic-sec}} Serverless projects

#### Elastic Cloud Enterprise example

```{applies_to}
deployment:
  ece: deprecated 4.1.0
```

This means the feature is:
* Available on {{ece}}
* Deprecated starting in version 4.1.0

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

### How do I know what the current {{stack}} version is?

To make sure you're always viewing the most up-to-date and relevant documentation, the version dropdown at the top of each page shows the most recent 9.x release. For example, 9.0+.

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
| [Elasticsearch](elasticsearch://release-notes/index.md) | 9.0.0 and later |
| [Kibana](kibana://release-notes/index.md) | 9.0.0 and later |
| [Elastic Agent](elastic-agent://release-notes/index.md) | 9.0.0 and later |
| [Fleet](fleet-server://release-notes/index.md) 9.0.0 and later |
| [Logstash](logstash://release-notes/index.md) | 9.0.0 and later |
| [Beats](beats://release-notes/index.md) | 9.0.0 and later |
| [Elastic Observability](/release-notes/elastic-observability/index.md) | 9.0.0 and later |
| [Elastic APM](apm-server://release-notes/index.md) | 9.0.0 and later |
| [Elastic Security](/release-notes/elastic-security/index.md) | 9.0.0 and later |

### Deployment type versions or releases

| Product | Version or release |
| --- | --- |
| All [Elastic Cloud Serverless](/release-notes/elastic-cloud-serverless/index.md) project types | All releases |
| [Elastic Cloud Hosted](cloud://release-notes/cloud-hosted/index.md) | All releases for January 2025 and later  |
| [Elastic Cloud Enterprise](cloud://release-notes/cloud-enterprise/index.md) | 4.0.0 and later |
| [Elastic Cloud on Kubernetes](cloud-on-k8s://release-notes/index.md) | 3.0.0 and later |

### Schema, library, and tool versions

| Product | Version or release
| --- | --- |
| [Elasticsearch Java Client](elasticsearch-java://release-notes/index.md) | 9.0.0 and later |
| [Elasticsearch JavaScript Client](elasticsearch-js://release-notes/index.md) | 9.0.0 and later |
| [Elasticsearch .NET Client](elasticsearch-net://release-notes/index.md) | 9.0.0 and later |
| [Elasticsearch PHP Client](elasticsearch-php://release-notes/index.md) | 9.0.0 and later |
| [Elasticsearch Python Client](elasticsearch-py://release-notes/index.md)  | 9.0.0 and later |
| [Elasticsearch Ruby Client](elasticsearch-ruby://release-notes/index.md)  | 9.0.0 and later |
| [Elastic Common Schema (ECS)](ecs://release-notes/index.md)  | 9.0.0 and later |
| [ECS Logging .NET library](ecs-dotnet://reference/index.md) | 8.18.1 and later |
| [ECS Logging Go (Logrus) library](ecs-logging-go-logrus://reference/index.md) | 1.0.0 and later |
| [ECS Logging Go (Zap) library](ecs-logging-go-zap://reference/index.md) | 1.0.3 and later |
| [ECS Logging Go (Zerolog) library](ecs-logging-go-zerolog://reference/index.md) | 0.2.0 and later |
| [ECS Logging Java library](ecs-logging-java://reference/index.md) | 1.x and later |
| [ECS Logging Node.js library](ecs-logging-nodejs://reference/index.md) | 1.5.3 and later |
| [ECS Logging PHP library](ecs-logging-php://reference/index.md) | 2.0.0 and later |
| [ECS Logging Python library](ecs-logging-python://reference/index.md) | 2.2.0 and later |
| [ECS Logging Ruby library](ecs-logging-ruby://reference/index.md) | 1.0.0 and later |
| [Elasticsearch for Apache Hadoop](elasticsearch-hadoop://release-notes/index.md) | 9.0.0 and later |
| [Elasticsearch Curator](curator://reference/index.md) | 8.0.0 and later |
| [Elastic Cloud Control (ECCTL)](ecctl://release-notes/index.md) | 1.14.0 and later |
| [Elastic Serverless Forwarder for AWS](elastic-serverless-forwarder://reference/index.md) | 1.20.1 and later |
| [Elastic integrations](https://www.elastic.co/docs/reference/integrations/all_integrations) | All versions |
| [Search UI JavaScript library](search-ui://reference/index.md) | 1.24.0 and later |

### APM agent and tool versions

| Product | Version |
| --- | --- |
| [Elastic Distribution of OpenTelemetry Android](apm-agent-android://release-notes/index.md) | 0.1.0 and later |
| [Elastic Distribution of OpenTelemetry iOS](apm-agent-ios://release-notes/index.md) | 1.0.0 and later |
| [Elastic Distribution of OpenTelemetry Java](elastic-otel-java://release-notes/index.md) | 1.0.0 and later |
| [Elastic Distribution of OpenTelemetry .NET](elastic-otel-dotnet://release-notes/index.md) | 1.0.0 and later |
| [Elastic Distribution of OpenTelemetry Node.js](elastic-otel-node://release-notes/index.md) | 0.1.0 and later |
| [Elastic Distribution of OpenTelemetry Python](elastic-otel-python://release-notes/index.md) | 0.1.0 and later |
| [Elastic Distribution of OpenTelemetry PHP](elastic-otel-php://release-notes/index.md) | 0.1.0 and later |
| [Elastic APM .NET Agent](apm-agent-dotnet://release-notes/index.md) | 1.0.0 and later |
| [Elastic APM Go Agent](apm-agent-go://release-notes/index.md) | 2.0.0 and later |
| [Elastic APM Java Agent](apm-agent-java://release-notes/index.md) | 1.0.0 and later |
| [Elastic APM Node.js Agent](apm-agent-nodejs://release-notes/index.md) | 4.0.0 and later |
| [Elastic APM PHP Agent](apm-agent-php://release-notes/index.md) | 1.0.0 and later |
| [Elastic APM Python Agent](apm-agent-python://release-notes/index.md) | 6.0.0 and later |
| [Elastic APM Ruby Agent](apm-agent-ruby://release-notes/index.md) | 4.0.0 and later |
| [Elastic APM Real User Monitoring JavaScript Agent](apm-agent-rum-js://release-notes/index.md) | 5.0.0 and later |
| [Elastic APM AWS Lambda extension](apm-aws-lambda://release-notes/release-notes.md) | 1.0.0 and later |
| [Elastic APM Attacher for Kubernetes](apm-k8s-attacher://reference/index.md) | 1.1.3 |








