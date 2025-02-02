---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-roles.html
---

# Separation of roles [ece-roles]

The separation of roles is required to group components on ECE and prevent conflicting workloads. When you install Elastic Cloud Enterprise on the first host, it is assigned many different host roles: Allocator, coordinator, director, and proxy. This role assignment is required to bring up your initial deployments. In a production environment, some of these roles need to be separated, as their loads scale differently and can create conflicting demands when placed on the same hosts. There are also certain [security implications that are addressed by separating roles](../../security/secure-your-elastic-cloud-enterprise-installation.md#ece-securing-vectors).

Roles that should not be held by the same host:

* Allocators and coordinators
* Allocators and directors
* Coordinators and proxies

If this separation of roles is not possible, fewer hosts that provide substantial hardware resources with fast SSD storage can be used, but we recommend this setup only for development, test, and small-scale use cases. For example, even if you have only three hosts, sharing roles might be feasible in some cases. If SSD-only storage is not feasible, you must separate the ECE management services provided by the coordinators and directors from your proxies and allocators and place them on different hosts that use fast SSD storage.

Some roles are safe for hosts to hold at the same time:

* Directors and coordinators (the ECE management services)

To learn more about how you can assign roles, check [Assign Roles](assign-roles-to-hosts.md).

