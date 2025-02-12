---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/Elastic-Cloud-Enterprise-overview.html
---

# Elastic Cloud Enterprise [Elastic-Cloud-Enterprise-overview]

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/339

% Scope notes: Ensure the landing page makes sense and its aligned with the section overview and the overview about orchestators. What content should be in deployment types overview or in the main overview and what in the ECE landing page...

% Use migrated content from existing pages that map to this page:

% already deleted
% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/Elastic-Cloud-Enterprise-overview.md
%      Notes: 2 child docs
% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/ece-administering-ece.md
%      Notes: redirect only

This page provides a high-level overview of Elastic Cloud Enterprise (ECE).

::::{note}
Try one of the [getting started guides](https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/getting-started-guides.html) to discover the core concepts of the Elastic Stack and understand how Elastic can help you.
::::

**What is ECE?**

ECE is an Elastic's on-premises and self-managed solution for deploying, orchestrating, and managing Elasticsearch clusters at scale. It provides a centralized platform that allows organizations to run Elasticsearch, Kibana, and other Elastic Stack components across multiple machines.

ECE evolves from the Elastic hosted Cloud SaaS offering into a standalone product. You can deploy ECE on public or private clouds, virtual machines, or your own premises.

**Why ECE?**

* Host your regulated or sensitive data on your internal network.
* Reuse your existing investment in on-premise infrastructure and reduce total cost.
* Maximize the hardware utilization for the various clusters.
* Centralize the management of multiple Elastic deployments across teams or geographies.

**ECE features**

- [**Microservices**](./cloud-enterprise/ece-containerization.md) - All services are containerized through Docker.
- [**Services oriented architecture**](./cloud-enterprise/ece-architecture.md) - Deployment state coordination using ZooKeeper.
- **High Availability & Resilience** – Ensures uptime through multiple Availability Zones, data replication, and automated restore and snapshot.
- **Automated Scaling & Orchestration** – Handles cluster provisioning, scaling, and upgrades automatically.
- **Centralized Monitoring & Logging** – Provides insights into cluster performance, resource usage, and logs.
- **Role-Based Access Control (RBAC)** – Allows organizations to manage access and security policies.
- **API & UI Management** – Offers a web interface and API to create and manage clusters easily.
- **Air gapped installations** - Support for off-line installations.

Check the [glossary](https://www.elastic.co/guide/en/elastic-stack-glossary/current/terms.html) to get familiar with the terminology for ECE as well as other Elastic products and solutions.

**Use cases**

- Organizations that need **full control over their Elastic Stack** while benefiting from cloud-like automation.
- Enterprises managing **multiple Elasticsearch clusters** across different teams or environments.
- Businesses looking for **a self-hosted alternative to Elastic Cloud** but with centralized administration.

## How it Differs from Elastic Cloud and other orchestrators

- **Elastic Cloud** (hosted by Elastic) is fully managed and runs on AWS, GCP, and Azure.
- **ECE** is for organizations that **want to self-host and manage their own Elastic Stack** deployments across their infrastructure.
