---
navigation_title: ECE Overview
applies:
  ece: all
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/Elastic-Cloud-Enterprise-overview.html
---

# Elastic Cloud Enterprise overview [Elastic-Cloud-Enterprise-overview]

This page provides a high-level introduction to {{ece}} (ECE), including its [](./ece-architecture.md) and [Containerized design](./ece-containerization.md).

::::{note}
Try one of the [getting started guides](https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/getting-started-guides.html) to discover the core concepts of the Elastic Stack and understand how Elastic can help you.
::::

### What is ECE?

ECE evolves from the Elastic hosted Cloud SaaS offering into a standalone product. You can deploy ECE on public or private clouds, virtual machines, or your own premises.

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
- **Microservices** - All services are containerized through Docker. Refer to [](./ece-containerization.md) for more details.

Check the [glossary](https://www.elastic.co/guide/en/elastic-stack-glossary/current/terms.html) to get familiar with the terminology for ECE as well as other Elastic products and solutions.

### Use cases

- Organizations that need full control over their Elastic Stack while benefiting from cloud-like automation.
- Enterprises managing multiple Elasticsearch clusters across different teams or environments.
- Businesses looking for a self-hosted alternative to Elastic Cloud with centralized administration.