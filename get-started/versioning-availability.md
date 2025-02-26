---
navigation_title: Versioning and availability
---

# Understanding versioning and availability

## Elastic Stack versioning

{{es}} and the core components of the Elastic Stack use a semantic versioning scheme. This scheme consists of three numbers separated by periods in the form `X.Y.Z`, for example: `9.0.0`.

Each number represents a specific level of change:

- **Major (X)**: Indicates significant changes, such as new features, breaking changes, and major enhancements. Upgrading to a new major version may require changes to your existing setup and configurations.
- **Minor (Y)**: Introduces new features and improvements, while maintaining backward compatibility with the previous minor versions within the same major version. Upgrading to a new minor version should not require any changes to your existing setup.
- **Patch (Z)**: Contains bug fixes and security updates, without introducing new features or breaking changes. Upgrading to a new patch version should be seamless and not require any changes to your existing setup.

It's important to understand this versioning system, for compatibility and [upgrade](/deploy-manage/upgrade.md) planning.

## Availability of features

Elastic products and features have different availability states across deployment types and lifecycle stages.

Features may have different availability states between:

- **Deployment type**: The environment where the feature is available (Stack, Serverless, ECE, ECK, etc.)
- **Lifecycle state**: The development or support status of the feature (GA, Beta, etc.)
- **Version**: The specific version the lifecycle state applies to

#### Lifecycle states

| State | Description |
|-------|-------------|
| **Generally Available (GA)** | Production-ready feature (default if not specified) |
| **Beta** | Feature is nearing general availability but not yet production-ready |
| **Technical preview** | Feature is in early development stage |
| **Coming** | Feature announced for a future release |
| **Discontinued** | Feature is being phased out |
| **Unavailable** | Feature is not supported in this deployment type or version |

### Where feature availability may differ

Features may have different states between:

- **[Elastic Stack](the-stack.md)** versions (e.g., 9.0, 9.1)
- **Deployment types** (and deployment versions)
  - [Elastic Cloud Hosted](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md)
  - [Elastic Cloud Serverless](/deploy-manage/deploy/elastic-cloud/serverless.md)
  - [Self-managed deployments](/deploy-manage/deploy/self-managed.md)
  - [Elastic Cloud Enterprise (ECE)](/deploy-manage/deploy/cloud-enterprise.md)
    - ECE deployment versions (for example, 4.0.0)
  - [Elastic Cloud on Kubernetes (ECK)](/deploy-manage/deploy/cloud-on-k8s.md)
    - ECK deployment versions (for example, 3.0.0)
- **Serverless project types**
  - Security
  - Elasticsearch
  - Observability

### Important tips when reading the docs

- Always check feature lifecycle state for your specific deployment type and version
- Pay attention to Elastic Stack version requirements
- Note that Serverless features may vary by project type

### Availability badges in the docs

Our documentation uses badges to help you quickly identify where and when features are available for your specific environment.

Badges can appear in two places:
1. **Page headers**: Shows the overall availability across all deployment types
2. **Section headers**: Indicates specific availability for content in that section

### How to read the badges

Here are some examples to help you understand how to read the availability badges.

#### Example #1: Stack only feature

```yaml {applies_to}
stack: ga 9.1
```
- **Deployment type**: Elastic Stack
- **Version**: 9.1
- **Lifecycle**: Generally Available (GA) — default state

#### Example #2: Serverless-only feature with project differences

```yaml {applies_to}
serverless:
  security: beta
  elasticsearch: ga
```
- **Deployment type**: Serverless 
- **Lifecycle**: 
  - Beta for Security projects
  - Generally Available for Elasticsearch projects

#### Example #3: Discontinued feature on one deployment type

```yaml {applies_to}
deployment:
  ece: discontinued 4.1.0
```
- **Deployment type**: Elastic Cloud Enterprise
- **Lifecycle**: Discontinued
- **Version**: 4.1.0

:::{tip}
For contributors and those interested in the technical details, see the [Elastic docs syntax guide](https://elastic.github.io/docs-builder/syntax/applies/) for more information on how these badges are implemented.
:::