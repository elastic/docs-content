---
applies:
  ece: all
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/Elastic-Cloud-Enterprise-overview.html
---

% we still need to determine what to do with /raw-migrated-files/cloud/cloud-enterprise/ece-administering-ece.md

# Elastic Cloud Enterprise [Elastic-Cloud-Enterprise-overview]

This page provides a high-level introduction to {{ece}} (ECE).

::::{note}
Try one of the [getting started guides](https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/getting-started-guides.html) to discover the core concepts of the Elastic Stack and understand how Elastic can help you.
::::

## ECE Overview

Elastic Cloud Enterprise (ECE) is an on-premises and self-managed solution for deploying, orchestrating, and managing {{es}} clusters at scale. It provides a centralized platform that allows organizations to run {{es}}, {{kib}}, and other {{stack}} components across multiple machines.

ECE evolves from the Elastic hosted Cloud SaaS offering into a standalone product. You can deploy ECE on public or private clouds, virtual machines, or on-premises.

For an overview of ECE architecture refer to [](./cloud-enterprise/ece-architecture.md).

::::{tip}
If you are looking for a solution to orchestrate and manage {{es}} clusters natively on Kubernetes, consider using [Elastic Cloud on Kubernetes (ECK)](./cloud-on-k8s.md) instead of ECE. ECK enables you to orchestrate Elastic Stack applications seamlessly on Kubernetes, leveraging it as the underlying platform for deployment, scaling, and lifecycle management.
::::

### Why ECE?

* Host your regulated or sensitive data on your internal network.
* Reuse your existing investment in on-premise infrastructure and reduce total cost.
* Maximize the hardware utilization for the various clusters.
* Centralize the management of multiple Elastic deployments across teams or geographies.

### ECE features

- **Automated Scaling & Orchestration** – Handles cluster provisioning, scaling, and upgrades automatically.
- **High Availability & Resilience** – Ensures uptime through multiple Availability Zones, data replication, and automated restore and snapshot.
- **Centralized Monitoring & Logging** – Provides insights into cluster performance, resource usage, and logs.
- **Single Sign-On (SSO) & Role-Based Access Control (RBAC)** – Allows organizations to manage access and security policies.
- **API & UI Management** – Offers a web interface and API to create and manage clusters easily.
- **Air gapped installations** - Support for off-line installations.
- **Microservices** - All services are containerized through Docker. See [](./cloud-enterprise/ece-containerization.md) for more details.

Check the [glossary](https://www.elastic.co/guide/en/elastic-stack-glossary/current/terms.html) to get familiar with the terminology for ECE as well as other Elastic products and solutions.

### Use cases

- Organizations that need **full control over their Elastic Stack** while benefiting from cloud-like automation.
- Enterprises managing **multiple Elasticsearch clusters** across different teams or environments.
- Businesses looking for **a self-hosted alternative to Elastic Cloud** with centralized administration.

## How it differs from Elastic Cloud and other orchestrators

For information about other deployment options, refer to [](../deploy.md).

% - **Elastic Cloud** (hosted by Elastic) is fully managed and runs on AWS, GCP, and Azure.
% - **ECE** is for organizations that **want to self-host and manage their own Elastic Stack** deployments across their infrastructure.
% - **ECK** is for organizations that want to run on Kubernetes.

## Supported versions [ece-supported-versions]

Refer to [Elastic Support Matrix](https://www.elastic.co/support/matrix#elastic-cloud-enterprise) for more information about supported Operating Systems, Docker, and Podman versions.
