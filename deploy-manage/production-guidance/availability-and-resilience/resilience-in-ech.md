---
navigation_title: Resilience in Elastic Cloud Hosted deployments
applies_to:
  deployment:
    ess: all
---

# Resiliency in Elastic Cloud Hosted deployments

With {{ech}}, your deployment can be spread across up to three separate availability zones, each hosted in an isolated infrastructure domain, such as separate data centers in the case of {{ech}}.

::::{note}
While this document focuses on {{ech}}, the concepts also apply to {{ece}} and {{eck}} deployments. In ECK, you will have to manually configure [availability zone distribution and node scheduling](/deploy-manage/deploy/cloud-on-k8s/advanced-elasticsearch-node-scheduling.md) through your Kubernetes platform.
::::

Why this matters:

* Data centers can have issues with availability. Internet outages, earthquakes, floods, or other events could affect the availability of a single data center. With a single availability zone, you have a single point of failure that can bring down your deployment.
* Multiple availability zones help your deployment remain available. This includes your {{es}} cluster, provided that your cluster is sized so that it can sustain your workload on the remaining data centers and that your indices are configured to have at least one replica.
* Multiple availability zones enable you to perform changes to resize your deployment with zero downtime.

## Recommendations [ec-ha]

We recommend that you use at least two availability zones for production and three for mission-critical systems. Just one zone might be sufficient, if your {{es}} cluster is mainly used for testing or development and downtime is acceptable, but should never be used for production.

With multiple {{es}} nodes in multiple availability zones you have the recommended hardware, the next thing to consider is having the recommended index replication. Each index, with the exception of searchable snapshot indexes, should have one or more replicas. Use the index settings API to find any indices with no replica:

```sh
GET _all/_settings/index.number_of_replicas
```

A high availability (HA) cluster requires at least three master-eligible nodes. For clusters that have fewer than six {{es}} nodes, any data node in the hot tier will also be a master-eligible node. You can achieve this by having hot nodes (serving as both data and master-eligible nodes) in three availability zones, or by having data nodes in two zones and a tiebreaker (will be automatically added if you choose two zones). For clusters that have six {{es}} nodes and beyond, dedicated master-eligible nodes are introduced. When your cluster grows, consider separating dedicated master-eligible nodes from dedicated data nodes. We recommend using at least 4GB RAM for dedicated master nodes.

The data in your {{es}} clusters is also backed up every 30 minutes, 4 hours, or 24 hours, depending on which snapshot interval you choose. These regular intervals provide an extra level of redundancy. We do support [snapshot and restore](../../../deploy-manage/tools/snapshot-and-restore.md), regardless of whether you use one, two, or three availability zones. However, with only a single availability zone and in the event of an outage, it might take a while for your cluster come back online. Using a single availability zone also leaves your cluster exposed to the risk of data loss, if the backups you need are not useable (failed or partial snapshots missing the indices to restore) or no longer available by the time that you realize that you might need the data (snapshots have a retention policy).

## Important considerations

* Clusters that use only one availability zone are not highly available and are at risk of data loss. To safeguard against data loss, you must use at least two availability zones.
* Indices with no replica, except for searchable snapshot indices, are not highly available. You should use replicas to mitigate against possible data loss.
* Clusters that only have one master node are not highly available and are at risk of data loss. You must have three master-eligible nodes.



