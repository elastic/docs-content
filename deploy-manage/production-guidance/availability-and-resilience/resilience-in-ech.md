---
navigation_title: Resilience in ECH and ECE
applies_to:
  deployment:
    ess: all
    ece: all
---

# Resiliency in ECH and ECE deployments

With {{ech}} (ECH) and {{ece}} (ECE), your deployment can be spread across up to three separate availability zones, each hosted in an isolated infrastructure domain, such as separate data centers in the case of {{ech}}.

::::{note}
While this document focuses on how ECH and ECE handle resilience, all the concepts and recommendations described in this section are also applicable to other deployment types. For example, in {{eck}}, you can configure [availability zone distribution and node scheduling](/deploy-manage/deploy/cloud-on-k8s/advanced-elasticsearch-node-scheduling.md) through your Kubernetes platform.
::::

Why this matters:

* Data centers can have issues with availability. Internet outages, earthquakes, floods, or other events could affect the availability of a single data center. With a single availability zone, you have a single point of failure that can bring down your deployment.
* Multiple availability zones help your deployment remain available. This includes your {{es}} cluster, provided that your cluster is sized so that it can sustain your workload on the remaining data centers and that your indices are configured to have at least one replica.
* Multiple availability zones enable you to perform changes to resize your deployment with zero downtime.

::::{important}
ECH and ECE orchestators automatically handle several aspects of cluster resilience that are discussed in the self-managed resiliency guidance for [small](./resilience-in-small-clusters.md) and [large](./resilience-in-larger-clusters.md) clusters:

* Configuring master-eligible nodes:
  * Setting up a [voting-only tiebreaker](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#voting-only-node) when the cluster spans to two availability zones.
  * Promoting [dedicated master nodes](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#dedicated-master-node) as the cluster grows to improve stability and fault tolerance.
* Enabling [shard allocation awareness](../../distributed-architecture/shard-allocation-relocation-recovery/shard-allocation-awareness.md) to maintain resilience during whole-zone failures.
* Automatically assigning [node roles](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md) based on the configured [data tiers](/manage-data/lifecycle/data-tiers.md).
* Creating [automatic snapshots](/deploy-manage/tools/snapshot-and-restore.md) at regular configurable intervals, to provide an extra level of redundancy.
::::

## Recommendations [ec-ha]

We recommend that you use at least two availability zones for production and three for mission-critical systems. Just one zone might be sufficient, if your {{es}} cluster is mainly used for testing or development and downtime is acceptable, but should never be used for production.

Additionally, using a single availability zone leaves your cluster vulnerable to data loss if backups are unavailable, whether due to failed or incomplete snapshots, missing indices, or expired retention policies that remove the data before it’s needed.

With multiple {{es}} nodes in multiple availability zones you have the recommended hardware, the next thing to consider is the number of replicas for each index. Each index, with the exception of searchable snapshot indexes, should have one or more replicas. Use the [index settings API](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-indices-get-settings-1) to find any indices with no replica:

```sh
GET _all/_settings/index.number_of_replicas
```

A high availability (HA) cluster requires at least three master-eligible nodes. For clusters that have fewer than six {{es}} nodes, any data node in the hot tier will also be a master-eligible node. You can achieve this by having hot nodes (serving as both data and master-eligible nodes) in three availability zones, or by having data nodes in two zones and a tiebreaker.

For clusters that have six {{es}} nodes and beyond, dedicated master-eligible nodes are introduced. When your cluster grows, consider separating dedicated master-eligible nodes from dedicated data nodes. We recommend using at least 4GB of RAM for dedicated master nodes.

::::{note}
In {{ece}}, you can customize the threshold at which dedicated master-eligible nodes are introduced by modifying the [deployment templates](/deploy-manage/deploy/cloud-enterprise/deployment-templates.md).
::::

## Summary

* Clusters that use only one availability zone are not highly available and are at risk of data loss. To safeguard against data loss, you must use at least two availability zones.
* Indices with no replica, except for searchable snapshot indices, are not highly available. You should use replicas to mitigate against possible data loss.
* Clusters that only have one master node are not highly available and are at risk of data loss. You must have three master-eligible nodes.



