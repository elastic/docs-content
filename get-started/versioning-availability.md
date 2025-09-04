---
navigation_title: Versioning and availability
mapped_pages:
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/introducing-elastic-documentation.html
products:
  - id: elastic-stack
description: Learn how Elastic handles versioning and feature availability in the docs. Find the product versions that are supported, how to read availability badges, and...
---

# Versioning and availability

Learn how Elastic products are versioned, the lifecycle of features, and how to find the right documentation for your deployment type and product version. Find answers to common questions about the versioning and confidently navigate our continuously updated documentation.

## Understanding versioning

Most Elastic products, like {{es}} or {{kib}}, share the same versioning pattern, based on the {{stack}}. Orchestrators such as {{ece}} and {{eck}}, and other tools such as code clients and SDKs, are versioned independently of the Elastic Stack. The {{ecloud}} console and {{serverless-short}} projects are always automatically updated with the latest changes.

The Elastic Stack products use semantic versioning in the `X.Y.Z` format, such as `9.0.0`.

| Version | Description |
| ----- | ----- |
| Major (X) | Indicates significant changes, such as new features, breaking changes, and major enhancements. Upgrading to a new major version may require changes to your existing setup and configurations. |
| Minor (Y) | Introduces new features and improvements, while maintaining backward compatibility with the previous minor versions within the same major version. Upgrading to a new minor version should not require any changes to your existing setup. |
| Patch (Z) | Contains bug fixes and security updates, without introducing new features or breaking changes. Upgrading to a new patch version should be seamless and not require any changes to your existing setup. |

Understanding Elastic Stack versioning is essential for [upgrade planning](/deploy-manage/upgrade.md) and ensuring compatibility.

## Availability of features

Features available to you can differ based on deployment type, product lifecycle stage, and specific version.

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
| Beta | Feature is nearing general availability but not yet production-ready |
| Generally Available (GA) | Production-ready feature. When unspecified, GA is the default |
| Deprecated | Feature is still usable but is set to be removed or replaced in a future update |
| Removed | Feature can no longer be used |
| Unavailable | Feature is not supported in this deployment type or version |

### Examples of where availability can vary

| Category | Example |
| ----- | ----- |
| Elastic Stack versions | [{{stack}}](/get-started/the-stack.md) version 9.0.0 and later, including 9.1.0 |
| Deployment types | [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md), [{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md), [{{ece}}](/deploy-manage/deploy/cloud-enterprise.md), [{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md), and [Self-managed deployments](/deploy-manage/deploy/self-managed.md) |
| Orchestrator versions | [{{ece}}](/deploy-manage/deploy/cloud-enterprise.md) 4.0.0 and later, [{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md) 3.0.0 and later |
| Serverless project types | {{es}}, Elastic {{observability}}, and {{elastic-sec}} |




