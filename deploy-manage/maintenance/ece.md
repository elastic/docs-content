---
applies_to:
  deployment:
    ece:
products:
  - id: cloud-enterprise
---

# ECE maintenance

{{ece}} (ECE), being a self-managed {{stack}} deployment platform, abstracts much of the complexity of running {{es}}, but still requires regular maintenance at both the platform and deployment levels. Maintenance activities range from managing individual deployments to performing infrastructure-level updates on ECE hosts.

## Deployment maintenance and host infrastructure maintenance [ece-deployment-host-infra-maintenance]

[Deployment maintenance](ece/deployments-maintenance.md) focuses on managing individual {{es}} and {{kib}} instances within ECE. This includes actions such as [pausing instances](ece/pause-instance.md), [stopping request routing to nodes](/deploy-manage/maintenance/start-stop-routing-requests.md), and [moving instances between allocators](ece/move-nodes-instances-from-allocators.md) to optimize resource usage or prepare for maintenance. These tasks help maintain service availability and performance without affecting the underlying infrastructure.

[ECE host infrastructure maintenance](ece/perform-ece-hosts-maintenance.md) involves managing virtual machines that host ECE itself. This includes tasks like applying operating system patches, upgrading software, or decommissioning hosts. Infrastructure maintenance often requires more careful planning, as it can impact multiple deployments running on the affected hosts. Methods such as placing allocators into [maintenance mode](ece/enable-maintenance-mode.md) and redistributing workloads provide a smooth transition during maintenance operations.

This section provides guidance on best practices for both types of maintenance, helping you maintain a resilient ECE environment.
