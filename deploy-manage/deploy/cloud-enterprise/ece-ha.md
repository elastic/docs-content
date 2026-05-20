---
navigation_title: High availability
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-ha.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# High availability in ECE

Ensuring high availability (HA) in {{ece}} (ECE) requires careful planning and implementation across multiple areas, including availability zones, master nodes, replica shards, snapshot backups, and Zookeeper nodes.

::::{note}
This section focuses on ensuring high availability at the ECE platform level. For deployment-level considerations, including resiliency, scaling, and performance optimizations for running {{es}} and {{kib}}, refer to the general [production guidance](/deploy-manage/production-guidance.md).
::::

To maintain a minimum HA, you should deploy at least two ECE hosts for each role—**allocator, constructor, and proxy**—and at least three hosts for the **director** role, which runs ZooKeeper and requires quorum to operate reliably.

In addition, to improve resiliency at the availability zone level, it’s recommended to deploy ECE across three availability zones, with at least two allocators per zone and spare capacity to accommodate instance failover and workload redistribution in case of failures.

All Elastic-documented architectures recommend using three availability zones with ECE roles distributed across all zones. Refer to [deployment scenarios](./identify-deployment-scenario.md) for examples of small, medium, and large installations.

Regardless of the resiliency level at the platform level, it’s important to also [configure your deployments for high availability](/deploy-manage/production-guidance/availability-and-resilience/resilience-in-ech.md).

## Availability zones [ece-ece-ha-1-az]

Fault tolerance for ECE is based around the concept of *availability zones*.

An availability zone contains resources available to an ECE installation that are isolated from other availability zones to safeguard against potential failure.

Planning for a fault-tolerant installation with multiple availability zones means avoiding any single point of failure that could bring down ECE.

::::{important}
Adding more availability zones should not be used as a way to increase processing capacity and performance. The concept of zones is meant for high availability (2 zones) and fault tolerance (3 zones), but neither will work if your deployments rely on the resources from those zones to be operational. Refer to [scaling considerations](/deploy-manage/production-guidance/scaling-considerations.md#scaling-and-fault-tolerance) for more information.
::::

The main difference between ECE installations that include two or three availability zones is that three availability zones enable ECE to create {{es}} clusters with a [voting-only tiebreaker](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#voting-only-node) instance. If you have only two availability zones in your installation, no tiebreaker can be placed in a third zone, limiting the cluster’s ability to tolerate certain failures.

## Tiebreaker master nodes

A tiebreaker is a lightweight voting-only node used in distributed clusters to help avoid split-brain scenarios, where the cluster could incorrectly split into multiple autonomous parts during a network partition.

When you create a cluster with nodes in two availability zones when a third zone is available, ECE can create a tiebreaker in the third availability zone to help establish quorum in case of loss of an availability zone. The extra tiebreaker node that helps to provide quorum does not have to be a full-fledged and expensive node, as it does not hold data. For example: By [tagging allocators](./ece-configuring-ece-tag-allocators.md) hosts in ECE, can you create a cluster with eight nodes each in zones `ece-1a` and `ece-1b`, for a total of 16 nodes, and one tiebreaker node in zone `ece-1c`. This cluster can lose any of the three availability zones whilst maintaining quorum, which means that the cluster can continue to process user requests, provided that there is sufficient capacity available when an availability zone goes down.

## Zookeeper nodes

Make sure you have three Zookeepers—by default, on the Director host—for your ECE installation. Similar to three {{es}} master nodes can form a quorum, three Zookeepers can form the quorum for high availability purposes.

Backing up Zookeeper data directory is also recommended. Refer to [rebuilding a broken Zookeeper quorum](../../../troubleshoot/deployments/cloud-enterprise/rebuilding-broken-zookeeper-quorum.md) for more guidance.

## External resources accessibility

If you're using a [private Docker registry server](ece-install-offline-with-registry.md) or hosting any [custom bundles and plugins](/solutions/search/full-text/search-with-synonyms.md) on a web server, make sure these resources are accessible from all ECE allocators, so they can continue to be accessed in the event of a network partition or zone outage.

## Other recommendations

Avoid deleting containers unless explicitly instructed by Elastic Support or official documentation. Doing so may lead to unexpected issues or loss of access to your {{ece}} platform. For more details, refer to [](/troubleshoot/deployments/cloud-enterprise/troubleshooting-container-engines.md).

If in doubt, [contact support for help](/troubleshoot/index.md#contact-us).
