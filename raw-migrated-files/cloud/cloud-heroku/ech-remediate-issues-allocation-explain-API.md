# Remediate common issues returned by the cluster allocation explain API [ech-remediate-issues-allocation-explain-API]

Here’s how to resolve the most common causes of unassigned shards reported by the cluster allocation explain API.

* [Disk is full](../../../troubleshoot/monitoring/unavailable-shards.md#ech-disk-full)
* [A node containing data has moved to a different host](../../../troubleshoot/monitoring/unavailable-shards.md#ech-node-moved-to-another-host)
* [Unable to assign shards based on the allocation rule](../../../troubleshoot/monitoring/unavailable-shards.md#ech-cannot-assign-shards-on-allocation-rule)
* [The number of eligible data nodes is less than the number of replicas](../../../troubleshoot/monitoring/unavailable-shards.md#ech-eligible-data-nodes-less-than-replicas)
* [A snapshot issue prevents searchable snapshot indices from being allocated](../../../troubleshoot/monitoring/unavailable-shards.md#ech-searchable-snapshot-indices-not-allocated)
* [Maximum retry times exceeded](../../../troubleshoot/monitoring/unavailable-shards.md#ech-max-retry-exceeded)
* [Max shard per node reached the limit](../../../troubleshoot/monitoring/unavailable-shards.md#ech-max-shard-per-node)

If your issue is not addressed here, then [contact Elastic support for help](../../../deploy-manage/deploy/elastic-cloud/ech-get-help.md).

## Disk is full [ech-disk-full]

**Symptom**

If the disk usage exceeded the threshold, you may get one or more of the following messages:

`the node is above the high watermark cluster setting [cluster.routing.allocation.disk.watermark.high=90%], using more disk space than the maximum allowed [90.0%], actual free: [9.273781776428223%]`

`unable to force allocate shard to [%s] during replacement, as allocating to this node would cause disk usage to exceed 100%% ([%s] bytes above available disk space)`

`the node is above the low watermark cluster setting [cluster.routing.allocation.disk.watermark.low=85%], using more disk space than the maximum allowed [85.0%], actual free: [14.119771122932434%]`

`after allocating [[restored-xxx][0], node[null], [P], recovery_source[snapshot recovery [Om66xSJqTw2raoNyKxsNWg] from xxx/W5Yea4QuR2yyZ4iM44fumg], s[UNASSIGNED], unassigned_info[[reason=NEW_INDEX_RESTORED], at[2022-03-02T10:56:58.210Z], delayed=false, details[restore_source[xxx]], allocation_status[fetching_shard_data]]] node [GTXrECDRRmGkkAnB48hPqw] would have more than the allowed 10% free disk threshold (8.7% free), preventing allocation`

**Resolutions**

Review the topic for your deployment architecture:

* [Full disk on single-node deployment](../../../troubleshoot/monitoring/unavailable-nodes.md)
* [Full disk on multiple-nodes deployment](../../../troubleshoot/monitoring/unavailable-nodes.md)

To learn more, review the following topics:

* [Cluster-level shard allocation and routing settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cluster.html)
* [Fix watermark errors](../../../troubleshoot/elasticsearch/fix-watermark-errors.md)


## A node containing data has moved to a different host [ech-node-moved-to-another-host]

**Symptom**

During the routine system maintenance performed by Elastic, it might happen that a node moves to a different host. If the indices are not configured with replica shards, the shard data on the {{es}} node that is moved will be lost, and you might get one or more of these messages:

`cannot allocate because a previous copy of the primary shard existed but can no longer be found on the nodes in the cluster`

**Resolutions**

Configure an [highly available cluster](../../../deploy-manage/production-guidance/plan-for-production-elastic-cloud.md) to keep your service running. Also, consider taking the following actions to bring your deployment back to health and recover your data from the snapshot.

* [Close the red indices](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-close.html)
* [Restore the indices](../../../deploy-manage/tools/snapshot-and-restore.md) from the last successful snapshot

For more information, check also [Designing for resilience](../../../deploy-manage/production-guidance/availability-and-resilience.md).


## Unable to assign shards based on the allocation rule [ech-cannot-assign-shards-on-allocation-rule]

**Symptom**

When shards cannot be assigned, due to [data tier allocation](../../../manage-data/lifecycle/data-tiers.md#data-tier-allocation) or [attribute-based allocation](../../../deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md), you might get one or more of these messages:

`node does not match index setting [index.routing.allocation.include] filters [node_type:\"cold\"]`

`index has a preference for tiers [data_cold] and node does not meet the required [data_cold] tier`

`index has a preference for tiers [data_cold,data_warm,data_hot] and node does not meet the required [data_cold] tier`

`index has a preference for tiers [data_warm,data_hot] and node does not meet the required [data_warm] tier`

`this node's data roles are exactly [data_frozen] so it may only hold shards from frozen searchable snapshots, but this index is not a frozen searchable snapshot`

**Resolutions**

* Make sure nodes are available in each data tier and have sufficient disk space.
* [Check the index settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices.html#index-settings) and ensure shards can be allocated to the expected data tier.
* Check the [ILM policy](../../../manage-data/lifecycle/index-lifecycle-management.md) and check for issues with the [allocate action](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-allocate.html).
* Inspect the [index templates](../../../manage-data/data-store/templates.md) and check for issues with the index settings.


## The number of eligible data nodes is less than the number of replicas [ech-eligible-data-nodes-less-than-replicas]

**Symptom**

Unassigned replica shards are often caused by there being fewer eligible data nodes than the configured number_of_replicas.

**Resolutions**

* Add more [eligible data nodes or more availability zones](../../../deploy-manage/deploy/elastic-cloud/ech-customize-deployment-components.md) to ensure resiliency.
* Adjust the `number_of_replicas` [setting](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-update-settings.html) for your indices to the number of eligible data nodes -1.


## A snapshot issue prevents searchable snapshot indices from being allocated [ech-searchable-snapshot-indices-not-allocated]

**Symptom**

Some snapshots operations might be impacted, as shown in the following example:

`failed shard on node [Yc_Jbf73QVSVYSqZT8HPlA]: failed recovery, failure RecoveryFailedException[[restored-my_index-2021.32][1]: … SnapshotMissingException[[found-snapshots:2021.08.25-my_index-2021.32-default_policy-_j2k8it9qnehe1t-2k0u6a/iOAoyjWLTyytKkW3_wF1jw] is missing]; nested: NoSuchFileException[Blob object [snapshots/52bc3ae2030a4df8ab10559d1720a13c/indices/WRlkKDuPSLW__M56E8qbfA/1/snap-iOAoyjWLTyytKkW3_wF1jw.dat] not found: The specified key does not exist. (Service: Amazon S3; Status Code: 404; Error Code: NoSuchKey; Request ID: 4AMTM1XFMTV5F00V; S3 Extended Request ID:`

**Resolutions**

Upgrade to {{es}} version 7.17.0 or later, which resolves bugs that affected  snapshot operations in earlier versions. Check [Upgrade versions](../../../deploy-manage/upgrade/deployment-or-cluster.md) for more details.

If you can’t upgrade, you can recreate the snapshot repository as a workaround.

The bugs also affect searchable snapshots. If you still have data in the cluster but cannot restore from the searchable snapshot, you can try reindexing and recreating the searchable snapshot:

* Reindex all the affected indices to new regular indices
* Remove the affected frozen indices
* Take the snapshot and mount the indices again


## Max shard per node reached the limit [ech-max-shard-per-node]

**Symptom**

The parameter [`cluster.max_shards_per_node`](https://www.elastic.co/guide/en/elasticsearch/reference/current/misc-cluster-settings.html#cluster-max-shards-per-node) limits the total number of primary and replica shards for the cluster. If your cluster has a number of shards beyond this limit, you might get the following message:

`Validation Failed: 1: this action would add [2] shards, but this cluster currently has [1000]/[1000] maximum normal shards open`

**Resolutions**

Delete unnecessary indices, add more data nodes, and [avoid oversharding](../../../deploy-manage/production-guidance/optimize-performance/size-shards.md) as too many shards can overwhelm your cluster. If you cannot take these actions, and you’re confident your changes won’t destabilize the cluster, you can temporarily increase the limit using the [cluster update settings API](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-update-settings.html) and retry the action. For more details, check [Troubleshoot shard-related errors](../../../deploy-manage/production-guidance/optimize-performance/size-shards.md#troubleshoot-shard-related-errors).


## Maximum retry times exceeded [ech-max-retry-exceeded]

**Symptom**

The cluster will attempt to allocate a shard a few times, before giving up and leaving the shard unallocated. On {{es}} Service,  `index.allocation.max_retries` defaults to 5. If allocation fails after the maximum number of retries, you might get the following message:

`shard has exceeded the maximum number of retries [%d] on failed allocation attempts - manually call [/_cluster/reroute?retry_failed=true] to retry, [%s]`

**Resolutions**

Run [`POST /_cluster/reroute?retry_failed=true`](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-reroute.html) API to retry. If it still fails, rerun the [Cluster allocation explain](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-allocation-explain.html) API to diagnose the problem.


