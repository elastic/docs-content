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

Elastic products and features have different availability states across deployment types:

- **Generally Available**: Feature is production-ready (default if not specified)
- **Beta**: Feature is nearing general availability but is not yet ready for production usage
- **Technical preview**: Feature is in early development
- **Coming**: Feature is announced for a future release
- **Discontinued**: Feature is being phased out
- **Unavailable**: Feature is not supported in this deployment type or version

Features may have different availability states between:

- Elastic Stack versions (for example, 9.0, 9.1)
- Serverless projects (Security, {{es}}, Observability)
- Deployment types (and versions)
  - [Elastic Cloud Hosted](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md)
  - [Elastic Cloud Serverless](/deploy-manage/deploy/elastic-cloud/serverless.md)
  - [Self-managed deployments](/deploy-manage/deploy/self-managed.md)
  - [Elastic Cloud Enterprise (ECE)](/deploy-manage/deploy/cloud-enterprise.md)
    - ECE deployment versions (for example, 4.0.0)
  - [Elastic Cloud on Kubernetes (ECK)](/deploy-manage/deploy/cloud-on-k8s.md)
    - ECK deployment versions (for example, 3.0.0)

When reading the Elastic documentation be sure to:

- Check feature availability for your deployment type and version
- Note stack version requirements
- Be aware that Serverless features may vary by project type