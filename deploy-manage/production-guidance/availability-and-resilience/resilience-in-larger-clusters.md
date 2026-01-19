---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/high-availability-cluster-design-large-clusters.html
applies_to:
  deployment:
    self: all
    eck: all
products:
  - id: elasticsearch
---

# Resilience in larger clusters [high-availability-cluster-design-large-clusters]

It’s not unusual for nodes to share common infrastructure, such as network interconnects or a power supply. If so, you should plan for the failure of this infrastructure and ensure that such a failure would not affect too many of your nodes. It is common practice to group all the nodes sharing some infrastructure into *zones* and to plan for the failure of any whole zone at once.

::::{note}
This document focuses on self-managed {{es}} deployments and describes how {{es}} handles zone-aware resilience internally, including behavior during network partitions, shard allocation strategies, and the role of master-eligible nodes.

This information might also be useful for other deployment types, such as {{eck}}. 

For details on how similar principles are implemented in {{ech}} and {{ece}}, refer to [](./resilience-in-ech.md).
::::

{{es}} expects node-to-node connections to be reliable, have low latency, and have adequate bandwidth. Many {{es}} tasks require multiple round-trips between nodes. A slow or unreliable interconnect may have a significant effect on the performance and stability of your cluster.

For example, a few milliseconds of latency added to each round-trip can quickly accumulate into a noticeable performance penalty. An unreliable network may have frequent network partitions. {{es}} will automatically recover from a network partition as quickly as it can but your cluster may be partly unavailable during a partition and will need to spend time and resources to [resynchronize any missing data](../../distributed-architecture/shard-allocation-relocation-recovery.md#shard-recovery) and [rebalance](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#shards-rebalancing-settings) itself once the partition heals. Recovering from a failure may involve copying a large amount of data between nodes so the recovery time is often determined by the available bandwidth.

If you’ve divided your cluster into zones, the network connections within each zone are typically of higher quality than the connections between the zones. Ensure the network connections between zones are of sufficiently high quality. You will see the best results by locating all your zones within a single data center with each zone having its own independent power supply and other supporting infrastructure. You can also *stretch* your cluster across nearby data centers as long as the network interconnection between each pair of data centers is good enough.

$$$high-availability-cluster-design-min-network-perf$$$
There is no specific minimum network performance required to run a healthy {{es}} cluster. In theory, a cluster will work correctly even if the round-trip latency between nodes is several hundred milliseconds. In practice, if your network is that slow then the cluster performance will be very poor. In addition, slow networks are often unreliable enough to cause network partitions that lead to periods of unavailability.

If you want your data to be available in multiple data centers that are further apart or not well connected, deploy a separate cluster in each data center and use [{{ccs}}](../../../explore-analyze/cross-cluster-search.md) or [{{ccr}}](../../tools/cross-cluster-replication.md) to link the clusters together. These features are designed to perform well even if the cluster-to-cluster connections are less reliable or performant than the network within each cluster.

After losing a whole zone’s worth of nodes, a properly-designed cluster may be functional but running with significantly reduced capacity. You may need to provision extra nodes to restore acceptable performance in your cluster when handling such a failure.

For resilience against whole-zone failures, it is important that there is a copy of each shard in more than one zone, which can be achieved by placing data nodes in multiple zones and configuring [shard allocation awareness](../../distributed-architecture/shard-allocation-relocation-recovery/shard-allocation-awareness.md). You should also ensure that client requests are sent to nodes in more than one zone.

You should consider all node roles and ensure that each role is split redundantly across two or more zones. For instance, if you are using [ingest pipelines](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md) or {{ml}}, you should have ingest or {{ml}} nodes in two or more zones. However, the placement of master-eligible nodes requires a little more care because a resilient cluster needs at least two of the three master-eligible nodes in order to function. The following sections explore the options for placing master-eligible nodes across multiple zones.

## Two-zone clusters [high-availability-cluster-design-two-zones]

If you have two zones, you should have a different number of master-eligible nodes in each zone so that the zone with more nodes will contain a majority of them and will be able to survive the loss of the other zone. For instance, if you have three master-eligible nodes then you may put all of them in one zone or you may put two in one zone and the third in the other zone. You should not place an equal number of master-eligible nodes in each zone. If you place the same number of master-eligible nodes in each zone, neither zone has a majority of its own. Therefore, the cluster may not survive the loss of either zone.


## Two-zone clusters with a tiebreaker [high-availability-cluster-design-two-zones-plus]

The two-zone deployment described above is tolerant to the loss of one of its zones but not to the loss of the other one because master elections are majority-based. You cannot configure a two-zone cluster so that it can tolerate the loss of *either* zone because this is theoretically impossible. You might expect that if either zone fails then {{es}} can elect a node from the remaining zone as the master but it is impossible to tell the difference between the failure of a remote zone and a mere loss of connectivity between the zones. If both zones were capable of running independent elections then a loss of connectivity would lead to a [split-brain problem](https://en.wikipedia.org/wiki/Split-brain_(computing)) and therefore data loss. {{es}} avoids this and protects your data by not electing a node from either zone as master until that node can be sure that it has the latest cluster state and that there is no other master in the cluster. This may mean there is no master at all until connectivity is restored.

You can solve this by placing one master-eligible node in each of your two zones and adding a single extra master-eligible node in an independent third zone. The extra master-eligible node acts as a tiebreaker in cases where the two original zones are disconnected from each other. The extra tiebreaker node should be a [dedicated voting-only master-eligible node](../../distributed-architecture/clusters-nodes-shards/node-roles.md#voting-only-node), also known as a dedicated tiebreaker. A dedicated tiebreaker need not be as powerful as the other two nodes since it has no other roles and will not perform any searches nor coordinate any client requests nor be elected as the master of the cluster.

You should use [shard allocation awareness](../../distributed-architecture/shard-allocation-relocation-recovery/shard-allocation-awareness.md) to ensure that there is a copy of each shard in each zone. This means either zone remains fully available if the other zone fails.

All master-eligible nodes, including voting-only nodes, are on the critical path for [publishing cluster state updates](../../distributed-architecture/discovery-cluster-formation/cluster-state-overview.md#cluster-state-publishing). Cluster state updates are usually independent of performance-critical workloads such as indexing or searches, but they are involved in management activities such as index creation and rollover, mapping updates, and recovery after a failure. The performance characteristics of these activities are a function of the speed of the storage on each master-eligible node, as well as the reliability and latency of the network interconnections between all nodes in the cluster. You must therefore ensure that the storage and networking available to the nodes in your cluster are good enough to meet your performance goals.


## Clusters with three or more zones [high-availability-cluster-design-three-zones]

If you have three zones then you should have one master-eligible node in each zone. If you have more than three zones then you should choose three of the zones and put a master-eligible node in each of these three zones. This will mean that the cluster can still elect a master even if one of the zones fails.

As always, your indices should have at least one replica in case a node fails, unless they are [searchable snapshot indices](../../tools/snapshot-and-restore/searchable-snapshots.md). You should also use [shard allocation awareness](../../distributed-architecture/shard-allocation-relocation-recovery/shard-allocation-awareness.md) to limit the number of copies of each shard in each zone. For instance, if you have an index with one or two replicas configured then allocation awareness will ensure that the replicas of the shard are in a different zone from the primary. This means that a copy of every shard will still be available if one zone fails. The availability of this shard will not be affected by such a failure.


## Summary [high-availability-cluster-design-large-cluster-summary]

The cluster will be resilient to the loss of any zone as long as:

* The [cluster health status](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health) is `green`.
* There are at least two zones containing data nodes.
* Every index that is not a [searchable snapshot index](../../tools/snapshot-and-restore/searchable-snapshots.md) has at least one replica of each shard, in addition to the primary.
* [Shard allocation awareness](../../distributed-architecture/shard-allocation-relocation-recovery/shard-allocation-awareness.md) is configured to avoid concentrating all copies of a shard within a single zone.
* The cluster has at least three master-eligible nodes. At least two of these nodes are not [voting-only master-eligible nodes](../../distributed-architecture/clusters-nodes-shards/node-roles.md#voting-only-node), and they are spread evenly across at least three zones.
* Clients are configured to send their requests to nodes in more than one zone or are configured to use a load balancer that balances the requests across an appropriate set of nodes. The [{{ecloud}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body) service provides such a load balancer.


