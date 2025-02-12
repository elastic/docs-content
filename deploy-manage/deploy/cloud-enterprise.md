---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/Elastic-Cloud-Enterprise-overview.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-administering-ece.html
---

# Elastic Cloud Enterprise

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/339

% Scope notes: Ensure the landing page makes sense and its aligned with the section overview and the overview about orchestators. What content should be in deployment types overview or in the main overview and what in the ECE landing page...

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/Elastic-Cloud-Enterprise-overview.md
%      Notes: 2 child docs
% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/ece-administering-ece.md
%      Notes: redirect only


# Introducing Elastic Cloud Enterprise [Elastic-Cloud-Enterprise-overview]

This page provides a high-level introduction to Elastic Cloud Enterprise (ECE).

::::{note}
Try one of the [getting started guides](https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/getting-started-guides.html) to discover the core concepts of the Elastic Stack and understand how Elastic can help you.
::::


**What is ECE?**

ECE evolves from the Elastic hosted Cloud SaaS offering into a standalone product. You can deploy ECE on public or private clouds, virtual machines, or your own premises.

**Why ECE?**

* Host your regulated or sensitive data on your internal network.
* Reuse your existing investment in on-premise infrastructure and reduce total cost.
* Maximize the hardware utilization for the various clusters.
* Centralize the management of multiple Elastic deployments across teams or geographies.

**ECE features**

* All services are containerized through Docker.
* High Availability through multiple Availability Zones.
* Deployment state coordination using ZooKeeper.
* Easy access for admins through the Cloud UI and API.
* Support for off-line installations.
* Automated restore and snapshot.

Check the [glossary](https://www.elastic.co/guide/en/elastic-stack-glossary/current/terms.html) to get familiar with the terminology for ECE as well as other Elastic products and solutions.

% this should go to deploy ECE for example, not in the intro
# Administering your installation [ece-administering-ece]

Now that you have Elastic Cloud Enterprise up and running, take a look at the things you can do to keep your installation humming along, from adding more capacity to dealing with hosts that require maintenance or have failed:

* [Scale Out Your Installation](../../../deploy-manage/maintenance/ece/scale-out-installation.md) - Need to add more capacity? Here’s how.
* [Assign Roles to Hosts](../../../deploy-manage/deploy/cloud-enterprise/assign-roles-to-hosts.md) - Make sure new hosts can be used for their intended purpose after you install ECE on them.
* [Enable Maintenance Mode](../../../deploy-manage/maintenance/ece/enable-maintenance-mode.md) - Perform administrative actions on allocators safely by putting them into maintenance mode first.
* [Move Nodes From Allocators](../../../deploy-manage/maintenance/ece/move-nodes-instances-from-allocators.md) - Moves all Elasticsearch clusters and Kibana instances to another allocator, so that the allocator is no longer used for handling user requests.
* [Delete Hosts](../../../deploy-manage/maintenance/ece/delete-ece-hosts.md) - Remove a host from your ECE installation, either because it is no longer needed or because it is faulty.
* [Perform Host Maintenance](../../../deploy-manage/maintenance/ece/perform-ece-hosts-maintenance.md) - Apply operating system patches and other maintenance to hosts safely without removing them from your ECE installation.
* [Manage Elastic Stack Versions](../../../deploy-manage/deploy/cloud-enterprise/manage-elastic-stack-versions.md) - View, add, or update versions of the Elastic Stack that are available on your ECE installation.
* [Upgrade Your Installation](../../../deploy-manage/upgrade/orchestrator/upgrade-cloud-enterprise.md) - A new version of Elastic Cloud Enterprise is available and you want to upgrade. Here’s how.


