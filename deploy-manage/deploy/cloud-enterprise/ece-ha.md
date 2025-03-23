---
navigation_title: High availability
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-ha.html
---

# High availability in ECE

Ensuring high availability (HA) in {{ece}} (ECE) requires careful planning and implementation across multiple areas, including availability zones, master nodes, replica shards, snapshot backups, and Zookeeper nodes.

::::{note}
This section focuses on ensuring high availability at the ECE platform level, including infrastructure-related considerations and best practices. For deployment level HA and resilience strategies within ECE, refer to [Resilience in ECH and ECE deployments](/deploy-manage/production-guidance/availability-and-resilience/resilience-in-ech.md).

To learn more about running {{es}} and {{kib}} in production environments, refer to the general [production guidance](/deploy-manage/production-guidance.md).
::::

## Availability zones [ece-ece-ha-1-az]

Fault tolerance for ECE is based around the concept of *availability zones*.

An availability zone contains resources available to an ECE installation that are isolated from other availability zones to safeguard against potential failure.

Planning for a fault-tolerant installation with multiple availability zones means avoiding any single point of failure that could bring down ECE.

The main difference between ECE installations that include two or three availability zones is that three availability zones enable ECE to create {{es}} clusters with a [voting-only tiebreaker](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#voting-only-node) instance. If you have only two availability zones in your installation, no tiebreaker can be placed in a third zone, limiting the cluster’s ability to tolerate certain failures.

## Minimum requirements and recommendations

To maintain high availability, you should deploy at least two ECE hosts for each role—**allocator, constructor, and proxy**—and at least three hosts for the **director** role, which runs ZooKeeper and requires quorum to operate reliably.

In addition, to improve resiliency at the availability zone level, it’s recommended to deploy ECE across three availability zones, with at least two allocators per zone and spare capacity to accommodate instance failover and workload redistribution in case of failures.

All Elastic-documented architectures recommend using three availability zones with ECE roles distributed across all zones, refer to [deployment scenarios](./identify-deployment-scenario.md) for examples of small, medium, and large installations.

::::{important}
Regardless of the resiliency level at the platform level, it’s important to also [configure your deployments for high availability](/deploy-manage/production-guidance/availability-and-resilience/resilience-in-ech.md).
::::

## Zookeeper nodes

Make sure you have three Zookeepers - by default, on the Director host - for your ECE installation. Similar to three {{es}} master nodes can form a quorum, three Zookeepers can form the quorum for high availability purposes. Backing up Zookeeper data directory is also recommended, read [rebuilding a broken Zookeeper quorum](../../../troubleshoot/deployments/cloud-enterprise/rebuilding-broken-zookeeper-quorum.md) for more guidance.

## External resources accessibility

If you’re using a [private Docker registry server](ece-install-offline-with-registry.md) or hosting any [custom bundles and plugins](../../../solutions/search/full-text/search-with-synonyms.md) on a web server, make sure these resources are accessible from all ECE allocators, so they can continue to be accessed in the event of a network partition or zone outage.

## Other recommendations

Avoid deleting containers unless explicitly instructed by Elastic Support or official documentation. Doing so may lead to unexpected issues or loss of access to your {{ece}} platform. For more details, refer to [Troubleshooting container engines](../../../troubleshoot/deployments/cloud-enterprise/troubleshooting-container-engines.md).

If you're unsure, don't hesitate to [contact Elastic Support](../../../troubleshoot/deployments/cloud-enterprise/ask-for-help.md).
