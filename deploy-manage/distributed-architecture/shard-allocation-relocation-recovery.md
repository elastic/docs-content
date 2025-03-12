---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/shard-allocation-relocation-recovery.html
---

# Shard allocation, relocation, and recovery [shard-allocation-relocation-recovery]

Each [index](../../manage-data/data-store/index-basics.md) in Elasticsearch is divided into one or more [shards](../../deploy-manage/index.md). Each document in an index belongs to a single shard.

A cluster can contain multiple copies of a shard. Each shard has one distinguished shard copy called the *primary*, and zero or more non-primary copies called *replicas*. The primary shard copy serves as the main entry point for all indexing operations. The operations on the primary shard copy are then forwarded to its replicas.

Replicas maintain redundant copies of your data across the [nodes](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md) in your cluster, protecting against hardware failure and increasing capacity to serve read requests like searching or retrieving a document. If the primary shard copy fails, then a replica is promoted to primary and takes over the primary’s responsibilities.

Over the course of normal operation, Elasticsearch allocates shard copies to nodes, relocates shard copies across nodes to balance the cluster or satisfy new allocation constraints, and recovers shards to initialize new copies. In this topic, you’ll learn how these operations work and how you can control them.

::::{tip}
To learn about optimizing the number and size of shards in your cluster, refer to [Size your shards](../production-guidance/optimize-performance/size-shards.md). To learn about how read and write operations are replicated across shards and shard copies, refer to [Reading and writing documents](reading-and-writing-documents.md).
::::

## Shard allocation [shard-allocation]

Shard allocation is the process of assigning shard copies to nodes. This can happen during initial recovery, replica allocation, rebalancing, when nodes are added to or removed from the cluster, or when cluster or index settings that impact allocation are updated.

By default, the primary and replica shard copies for an index can be allocated to any node in the cluster, and may be relocated to rebalance the cluster.

### Adjust shard allocation settings [_adjust_shard_allocation_settings]

You can control how shard copies are allocated using the following settings:

* [Cluster-level shard allocation settings](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md): Use these settings to control how shard copies are allocated and balanced across the entire cluster. For example, you might want to [allocate nodes availability zones](shard-allocation-relocation-recovery/shard-allocation-awareness.md), or prevent certain nodes from being used so you can perform maintenance.
* [Index-level shard allocation settings](shard-allocation-relocation-recovery/index-level-shard-allocation.md): Use these settings to control how the shard copies for a specific index are allocated. For example, you might want to allocate an index to a node in a specific data tier, or to an node with specific attributes.

### Monitor shard allocation [_monitor_shard_allocation]

If a shard copy is unassigned, it means that the shard copy is not allocated to any node in the cluster. This can happen if there are not enough nodes in the cluster to allocate the shard copy, or if the shard copy can’t be allocated to any node that satisfies the shard allocation filtering rules. When a shard copy is unassigned, your cluster is considered unhealthy and returns a yellow or red cluster health status.

You can use the following APIs to monitor shard allocation:

* [Cluster allocation explain](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-allocation-explain)
* [cat allocation](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-allocation)
* [cluster health](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health)

[Learn more about troubleshooting unassigned shard copies and recovering your cluster health](../../troubleshoot/elasticsearch/red-yellow-cluster-status.md).

## Shard recovery [shard-recovery]

Shard recovery is the process of initializing a shard copy, such as restoring a primary shard from a snapshot or creating a replica shard from a primary shard. When a shard recovery completes, the recovered shard is available for search and indexing.

Recovery automatically occurs during the following processes:

* When creating an index for the first time.
* When a node rejoins the cluster and starts up any missing primary shard copies using the data that it holds in its data path.
* Creation of new replica shard copies from the primary.
* Relocation of a shard copy to a different node in the same cluster.
* A [snapshot restore](../tools/snapshot-and-restore/restore-snapshot.md) operation.
* A [clone](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-clone), [shrink](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-shrink), or [split](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-split) operation.

You can determine the cause of a shard recovery using the [recovery](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-recovery) or  [cat recovery](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-recovery) APIs.

### Adjust shard recovery settings [_adjust_shard_recovery_settings]

To control how shards are recovered, for example the resources that can be used by recovery operations, and which indices should be prioritized for recovery, you can adjust the following settings:

* [Index recovery settings](elasticsearch://reference/elasticsearch/configuration-reference/index-recovery-settings.md)
* [Cluster-level shard allocation settings](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md)
* [Index-level shard allocation settings](shard-allocation-relocation-recovery/index-level-shard-allocation.md), including [delayed allocation](shard-allocation-relocation-recovery/delaying-allocation-when-node-leaves.md) and [index recovery prioritization](shard-allocation-relocation-recovery/index-level-shard-allocation.md)

Shard recovery operations also respect general shard allocation settings.

### Monitor shard recovery [_monitor_shard_recovery]

You can use the following APIs to monitor shard allocation:

* View a list of in-progress and completed recoveries using the [cat recovery API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-recovery)
* View detailed information about a specific recovery using the [index recovery API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-recovery)

## Shard relocation [shard-relocation]

Shard relocation is the process of moving shard copies from one node to another. This can happen when a node joins or leaves the cluster, or when the cluster is rebalancing.

When a shard copy is relocated, it is created as a new shard copy on the target node. When the shard copy is fully allocated and recovered, the old shard copy is deleted. If the shard copy being relocated is a primary, then the new shard copy is marked as primary before the old shard copy is deleted.

### Adjust shard relocation settings [_adjust_shard_relocation_settings]

You can control how and when shard copies are relocated. For example, you can adjust the rebalancing settings that control when shard copies are relocated to balance the cluster, or the high watermark for disk-based shard allocation that can trigger relocation. These settings are part of the [cluster-level shard allocation settings](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md).

Shard relocation operations also respect shard allocation and recovery settings.