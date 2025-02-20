---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-ha.html
---

# High availability [ece-ha]


## Availability zones [ece-ece-ha-1-az]

Fault tolerance for Elastic Cloud Enterprise is based around the concept of *availability zones*.

An availability zone contains resources available to an Elastic Cloud Enterprise installation that are isolated from other availability zones to safeguard against potential failure.

Planning for a fault-tolerant installation with multiple availability zones means avoiding any single point of failure that could bring down Elastic Cloud Enterprise.

The main difference between Elastic Cloud Enterprise installations that include two or three availability zones is that three availability zones enable Elastic Cloud Enterprise to create clusters with a *tiebreaker*. If you have only two availability zones in total in your installation, no tiebreaker is created.

We recommend that for each deployment you use at least two availability zones for production and three for mission-critical systems. Using more than three availability zones for a deployment is not required nor supported. Availability zones are intended for high availability, not scalability.

::::{warning}
{{es}} clusters that are set up to use only one availability zone are not [highly available](/deploy-manage/production-guidance/availability-and-resilience.md) and are at risk of data loss. To safeguard against data loss, you must use at least two {{ece}} availability zones.
::::


::::{warning}
Increasing the number of zones should not be used to add more resources. The concept of zones is meant for High Availability (2 zones) and Fault Tolerance (3 zones), but neither will work if the cluster relies on the resources from those zones to be operational. The recommendation is to scale up the resources within a single zone until the cluster can take the full load (add some buffer to be prepared for a peak of requests), then scale out by adding additional zones depending on your requirements: 2 zones for High Availability, 3 zones for Fault Tolerance.
::::



## Master nodes [ece-ece-ha-2-master-nodes]

$$$ece-ha-tiebreaker$$$Tiebreakers are used in distributed clusters to avoid cases of [split brain](https://en.wikipedia.org/wiki/Split-brain_(computing)), where an {{es}} cluster splits into multiple, autonomous parts that continue to handle requests independently of each other, at the risk of affecting cluster consistency and data loss. A split-brain scenario is avoided by making sure that a minimum number of [master-eligible nodes](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/node-settings.md#master-node) must be present in order for any part of the cluster to elect a master node and accept user requests. To prevent multiple parts of a cluster from being eligible, there must be a [quorum-based majority](/deploy-manage/distributed-architecture/discovery-cluster-formation/modules-discovery-quorums.md) of `(n/2)+1` nodes, where `n` is the number of master-eligible nodes in the cluster. The minimum number of master nodes to reach quorum in a two-node cluster is the same as for a three-node cluster: two nodes must be available.

When you create a cluster with nodes in two availability zones when a third zone is available, Elastic Cloud Enterprise can create a tiebreaker in the third availability zone to help establish quorum in case of loss of an availability zone. The extra tiebreaker node that helps to provide quorum does not have to be a full-fledged and expensive node, as it does not hold data. For example: By tagging allocators hosts in Elastic Cloud Enterprise, can you create a cluster with eight nodes each in zones `ece-1a` and `ece-1b`, for a total of 16 nodes, and one tiebreaker node in zone `ece-1c`. This cluster can lose any of the three availability zones whilst maintaining quorum, which means that the cluster can continue to process user requests, provided that there is sufficient capacity available when an availability zone goes down.

By default, each node in an {{es}} cluster is a master-eligible node and a data node. In larger clusters, such as production clusters, it’s a good practice to split the roles, so that master nodes are not handling search or indexing work. When you create a cluster, you can specify to use dedicated [master-eligible nodes](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/node-settings.md#master-node), one per availability zone.

::::{warning}
Clusters that only have two or fewer master-eligible node are not [highly available](/deploy-manage/production-guidance/availability-and-resilience.md) and are at risk of data loss. You must have [at least three master-eligible nodes](/deploy-manage/distributed-architecture/discovery-cluster-formation/modules-discovery-quorums.md).
::::



## Replica shards [ece-ece-ha-3-replica-shards]

With multiple {{es}} nodes in multiple availability zones you have the recommended hardware, the next thing to consider is having the recommended index replication. Each index, with the exception of searchable snapshot indexes, should have one or more replicas. Use the index settings API to find any indices with no replica:

```sh
GET _all/_settings/index.number_of_replicas
```

::::{warning}
Indices with no replica, except for [searchable snapshot indices](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md), are not highly available. You should use replicas to mitigate against possible data loss.
::::



## Snapshot backups [ece-ece-ha-4-snapshot]

You should configure and use [{{es}} snapshots](/deploy-manage/tools/snapshot-and-restore.md). Snapshots provide a way to backup and restore your {{es}} indices. They can be used to copy indices for testing, to recover from failures or accidental deletions, or to migrate data to other deployments. We recommend configuring an [{{ece}}-level repository](../../tools/snapshot-and-restore/cloud-enterprise.md) to apply across all deployments. See [Work with snapshots](../../tools/snapshot-and-restore.md) for more guidance.


## Furthermore considerations [ece-ece-ha-5-other]

* Make sure you have three Zookeepers - by default, on the Director host - for your ECE installation. Similar to three Elasticsearch master nodes can form a quorum, three Zookeepers can forum the quorum for high availability purposes. Backing up Zookeeper data directory is also recommended, read [this doc](../../../troubleshoot/deployments/cloud-enterprise/rebuilding-broken-zookeeper-quorum.md) for more guidance.
* Make sure that if you’re using a [private Docker registry server](ece-install-offline-with-registry.md) or are using any [custom bundles and plugins](../../../solutions/search/full-text/search-with-synonyms.md) hosted on a web server, that these are available to all ECE allocators, so that they can continue to be accessed in the event of a network partition or zone outage.
* Don’t delete containers unless guided by Elastic Support or there’s public documentation explicitly describing this as required action. Otherwise, it can cause issues and you may lose access or functionality of your {{ece}} platform. See [Troubleshooting container engines](../../../troubleshoot/deployments/cloud-enterprise/troubleshooting-container-engines.md) for more information.

If in doubt, please [contact support for help](../../../troubleshoot/deployments/cloud-enterprise/ask-for-help.md).

