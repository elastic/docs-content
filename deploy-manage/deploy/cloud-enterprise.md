---
applies_to:
  deployment:
    ece: all
---

# Elastic Cloud Enterprise [Elastic-Cloud-Enterprise-overview]

{{ece}} (ECE) is an Elastic self-managed solution for deploying, orchestrating, and managing {{es}} clusters at scale. It provides a centralized platform that allows organizations to run {{es}}, {{kib}}, and other {{stack}} components across multiple machines.

::::{tip}
If you are looking for a solution to orchestrate and manage {{es}} clusters natively on Kubernetes, consider using [Elastic Cloud on Kubernetes (ECK)](./cloud-on-k8s.md) instead of ECE. ECK enables you to orchestrate Elastic Stack applications seamlessly on Kubernetes, leveraging it as the underlying platform for deployment, scaling, and lifecycle management.
::::

ECE evolves from the Elastic hosted Cloud SaaS offering into a standalone product. You can deploy ECE on public or private clouds, virtual machines, or your own premises.

With {{ece}}, you can:

* Host your regulated or sensitive data on your internal network.
* Reuse your existing investment in on-premise infrastructure and reduce total cost.
* Maximize the hardware utilization for the various clusters.
* Centralize the management of multiple Elastic deployments across teams or geographies.

Refer to [](./cloud-enterprise/ece-architecture.md) for details about the ECE platform architecture and the technologies used.

## ECE features

- **Automated scaling & orchestration**: Handles cluster provisioning, scaling, and upgrades automatically.
- **High availability & resilience**: Ensures uptime through multiple Availability Zones, data replication, and automated restore and snapshot.
- **Centralized monitoring & logging**: Provides insights into cluster performance, resource usage, and logs.
- **Single Sign-On (SSO) & role-based access aontrol (RBAC)**: Allows organizations to manage access and security policies.
- **API & UI management**: Offers a web interface and API to create and manage clusters easily.
- **Air-gapped installations**: Support for off-line installations.
- **Microservices architecture**: All services are containerized through Docker.

Check the [glossary](https://www.elastic.co/guide/en/elastic-stack-glossary/current/terms.html) to get familiar with the terminology for ECE as well as other Elastic products and solutions.

## Section overview

This section focuses on deploying ECE and orchestrating and configuring {{es}} clusters, also referred to as `deployments`.

In ECE, a deployment is a managed {{stack}} environment that provides users with an {{es}} cluster along with supporting components such as {{kib}} and other optional services like APM and {{fleet}}.

This section covers the following tasks:

* [Deploy ECE orchestrator](./cloud-enterprise/deploy-an-orchestrator.md)
    - [Prepare the environment](./cloud-enterprise/prepare-environment.md)
    - [Install ECE](./cloud-enterprise/install.md)
    - [Air gapped installations](./cloud-enterprise/air-gapped-install.md)
    - [Configure ECE](./cloud-enterprise/configure.md)

* [Work with deployments](./cloud-enterprise/working-with-deployments.md)
  - Use [](./cloud-enterprise/deployment-templates.md) to [](./cloud-enterprise/create-deployment.md)
  - [](./cloud-enterprise/customize-deployment.md)
  - Use the deployment [Cloud ID](./cloud-enterprise/find-cloud-id.md) and [Endpoint URLs](./cloud-enterprise/find-endpoint-url.md) for clients connection

* Learn about [](./cloud-enterprise/tools-apis.md) that you can use with ECE

Other sections of the documentation also include important tasks related to ECE:

* Platform security and management:
  * [Secure your ECE installation](../security/secure-your-elastic-cloud-enterprise-installation.md)
  * [Users and roles](../users-roles/cloud-enterprise-orchestrator.md)
  * [ECE platform maintenance operations](../maintenance/ece.md)
  * [Manage licenses](../license/manage-your-license-in-ece.md)

* Deployments security and management:
  * [Secure your deployments](../security/secure-your-cluster-deployment.md)
  * [Manage snapshot repositories](../tools/snapshot-and-restore.md)

## How ECE differs from Elastic Cloud and other orchestrators

For information about other deployment options, refer to [](../deploy.md).

% - **Elastic Cloud** (hosted by Elastic) is fully managed and runs on AWS, GCP, and Azure.
% - **ECE** is for organizations that **want to self-host and manage their own Elastic Stack** deployments across their infrastructure.
% - **ECK** is for organizations that want to run on Kubernetes.

## Supported versions [ece-supported-versions]

Refer to the [Elastic Support Matrix](https://www.elastic.co/support/matrix#elastic-cloud-enterprise) for more information about supported Operating Systems, Docker, and Podman versions.