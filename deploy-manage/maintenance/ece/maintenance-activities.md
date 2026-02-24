---
applies_to:
  deployment:
    ece:
products:
  - id: cloud-enterprise
---
# Maintenance activities

Maintenance activities ensure the smooth operation and scalability of your {{es}} installation. This section provides guidelines on performing essential maintenance tasks while minimizing downtime and maintaining high availability.

## Available maintenance operations

### [Enable maintenance mode](enable-maintenance-mode.md)

Before performing maintenance on an allocator, you should enable maintenance mode to prevent new {{es}} clusters and {{kib}} instances from being provisioned. This ensures that existing deployments can be safely moved to other allocators or adjusted without disruption.

### [Scale out installation](scale-out-installation.md)

You can scale out your installation by adding capacity to meet growing demand or improve high availability. This process involves installing ECE on additional hosts, assigning roles to new hosts, and resizing deployments to utilize the expanded resources.

### [Move nodes and instances between allocators](move-nodes-instances-from-allocators.md)

Moving {{es}} nodes, {{kib}} instances, and other components between allocators may be necessary to free up space, avoid downtime, or handle allocator failures. The process involves selecting target allocators and ensuring enough capacity to accommodate the migration.

### [Perform ECE host maintenance](perform-ece-hosts-maintenance.md)

Maintaining ECE hosts is critical for applying system patches, performing hardware upgrades, and ensuring compliance with security standards. Learn about the various methods of maintaining hosts, and their impact on your ECE installation.

### [Delete ECE hosts](delete-ece-hosts.md)

If a host is no longer required or is faulty, it can be removed from the {{ece}} installation. Deleting a host only removes it from the installation but does not uninstall the software from the physical machine. Before deletion, allocators should be placed in maintenance mode, and nodes should be migrated to avoid disruption.

## Best practices for maintenance

* Always check available capacity before making changes.

* Use maintenance mode to avoid unexpected disruptions.

* Move nodes strategically to maintain high availability.

* Perform maintenance during off-peak hours when possible.

* Regularly review and optimize resource allocation.

By following these guidelines, you can ensure the stability and efficiency of your environment while carrying out necessary maintenance activities.
