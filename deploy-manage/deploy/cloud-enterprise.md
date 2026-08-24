---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/index.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/Elastic-Cloud-Enterprise-overview.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# {{ece}} [Elastic-Cloud-Enterprise-overview]

{{ece}} (ECE) is an Elastic self-managed solution for deploying, orchestrating, and managing {{es}} clusters at scale. It provides a centralized platform that allows organizations to run {{es}}, {{kib}}, and other {{stack}} components across multiple machines.

ECE evolves from the [{{ech}}](./elastic-cloud.md) offering into a standalone product. You can deploy ECE on public or private clouds, virtual machines, or your own premises.

With {{ece}}, you can:

* Host your regulated or sensitive data on your internal network.
* Reuse your existing investment in on-premise infrastructure and reduce total cost.
* Maximize the hardware utilization for the various clusters.
* Centralize the management of multiple Elastic deployments across teams or geographies.

Refer to [](./cloud-enterprise/ece-architecture.md) for details about the ECE platform architecture and the technologies used.

:::{admonition} Use cloud services in your ECE environment with Cloud Connect
With [Cloud Connect](/deploy-manage/cloud-connect.md), you can use Elastic-managed cloud services in your ECE environment without having to install and manage their infrastructure yourself. In this way, you can get faster access to new features without adding to your operational overhead.
::::

## ECE features

- **Automated scaling & orchestration**: Handles cluster provisioning, scaling, and upgrades automatically.
- **High availability & resilience**: Ensures uptime through multiple Availability Zones, data replication, and automated restore and snapshot.
- **Centralized monitoring & logging**: Provides insights into cluster performance, resource usage, and logs.
- **Single Sign-On (SSO) & role-based access control (RBAC)**: Allows organizations to manage access and security policies.
- **API & UI management**: Offers a web interface and API to create and manage clusters easily.
- **Air-gapped installations**: Support for off-line installations.
- **Microservices architecture**: All services are containerized through Docker.

Check the [glossary](/reference/glossary/index.md) to get familiar with the terminology for ECE as well as other Elastic products and solutions.

## Section overview

This section focuses on deploying the ECE platform, as well as orchestrating and configuring {{es}} clusters, referred to as deployments.

In ECE, a deployment is a managed {{stack}} environment that provides users with an {{es}} cluster along with supporting components such as {{kib}} and other optional services like APM and {{fleet}}.

The section covers the following tasks:

* [Deploy an ECE orchestrator](./cloud-enterprise/deploy-an-orchestrator.md)
    - [Prepare the environment](./cloud-enterprise/prepare-environment.md)
    - [Install ECE](./cloud-enterprise/install.md)
    - [Air gapped installations](./cloud-enterprise/air-gapped-install.md)
    - [Configure ECE](./cloud-enterprise/configure.md)

* [Work with deployments](./cloud-enterprise/working-with-deployments.md)
  - Use [](./cloud-enterprise/deployment-templates.md) to [](./cloud-enterprise/create-deployment.md)
  - [](./cloud-enterprise/customize-deployment.md)
  - [Connect your applications to {{es}}](./cloud-enterprise/connect-elasticsearch.md)

* Learn about [](./cloud-enterprise/tools-apis.md) that you can use with ECE

Other sections of the documentation provide guidance on additional important tasks related to ECE:

* Platform security and management:
  * [Secure your ECE installation](../security/secure-your-elastic-cloud-enterprise-installation.md)
  * [Users and roles](../users-roles/cloud-enterprise-orchestrator.md)
  * [ECE platform maintenance operations](../maintenance/ece.md)
  * [Manage licenses](../license/manage-your-license-in-ece.md)

* Deployments security and management:
  * [Secure your deployments](../security/secure-your-cluster-deployment.md)
  * [Manage snapshot repositories](../tools/snapshot-and-restore.md)

To learn about other deployment options, refer to [](../deploy.md).

## Supported versions [ece-supported-versions]

Refer to the [Elastic Support Matrix](https://www.elastic.co/support/matrix#elastic-cloud-enterprise) for more information about supported Operating Systems, Docker, and Podman versions.
