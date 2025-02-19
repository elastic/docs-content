---
applies:
  ece: all
---

# Elastic Cloud Enterprise [Elastic-Cloud-Enterprise-overview]

{{ece}} (ECE) is an Elastic self-managed solution for deploying, orchestrating, and managing {{es}} clusters at scale. It provides a centralized platform that allows organizations to run {{es}}, {{kib}}, and other {{stack}} components across multiple machines.

Refer to [](./cloud-enterprise/ece-overview.md) for a detailed introduction to ECE, including its features, use cases, and architecture.

::::{tip}
If you are looking for a solution to orchestrate and manage {{es}} clusters natively on Kubernetes, consider using [Elastic Cloud on Kubernetes (ECK)](./cloud-on-k8s.md) instead of ECE. ECK enables you to orchestrate Elastic Stack applications seamlessly on Kubernetes, leveraging it as the underlying platform for deployment, scaling, and lifecycle management.
::::

% should we use a L2 heading here or just continue?
## Section overview

This section focuses on deploying ECE and the orchestrating and configuring {{es}} clusters, also referred to as `deployments`.

In ECE, a deployment is a managed {{stack}} environment that provides users with an {{es}} cluster along with supporting components such as {{kib}} and other optional services like APM and Fleet.

This section covers the following tasks:

* [Deploy ECE](./cloud-enterprise/deploy-an-orchestrator.md)
    - [Prepare the environment](./cloud-enterprise/prepare-environment.md)
    - [Install ECE](./cloud-enterprise/install.md)
    - [Air gapped installations](./cloud-enterprise/air-gapped-install.md)
    - [Configure ECE](./cloud-enterprise/configure.md)

* [Work with deployments](./cloud-enterprise/working-with-deployments.md)
  - Use [](./cloud-enterprise/deployment-templates.md) to [](./cloud-enterprise/create-deployment.md)
  - [](./cloud-enterprise/customize-deployment.md)
  - Use the deployment [Cloud ID](./cloud-enterprise/find-cloud-id.md) and [Endpoint URLs](./cloud-enterprise/find-endpoint-url.md) for clients connection

* Learn how to use the multiple [](./cloud-enterprise/tools-apis.md) available

Other sections of the documentation also include important tasks related with ECE:

* [Secure your ECE installation](../security/secure-your-elastic-cloud-enterprise-installation.md)
* [Users and roles](../users-roles/cloud-enterprise-orchestrator.md)
* [Manage snapshot repositories](../tools/snapshot-and-restore.md)
* [Manage licenses](../license/manage-your-license-in-ece.md)
* [ECE platform maintenance operations](../maintenance/ece.md)

## How ECE differs from Elastic Cloud and other orchestrators

For information about other deployment options, refer to [](../deploy.md).

% - **Elastic Cloud** (hosted by Elastic) is fully managed and runs on AWS, GCP, and Azure.
% - **ECE** is for organizations that **want to self-host and manage their own Elastic Stack** deployments across their infrastructure.
% - **ECK** is for organizations that want to run on Kubernetes.

## Supported versions [ece-supported-versions]

Refer to [Elastic Support Matrix](https://www.elastic.co/support/matrix#elastic-cloud-enterprise) for more information about supported Operating Systems, Docker, and Podman versions.