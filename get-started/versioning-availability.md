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

% will replace this with a ref link. 
% ## Find docs for your product version

