---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-recreate-follower-index.html
---

# Recreate a follower index [ccr-recreate-follower-index]

When a document is updated or deleted, the underlying operation is retained in the Lucene index for a period of time defined by the [`index.soft_deletes.retention_lease.period`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index.md#ccr-index-soft-deletes-retention-period) parameter. You configure this setting on the [leader index](../cross-cluster-replication.md#ccr-leader-requirements).

When a follower index starts, it acquires a retention lease from the leader index. This lease informs the leader that it should not allow a soft delete to be pruned until either the follower indicates that it has received the operation, or until the lease expires.

If a follower index falls sufficiently behind a leader and cannot replicate operations, {{es}} reports an `indices[].fatal_exception` error. To resolve the issue, recreate the follower index. When the new follow index starts, the [remote recovery](../cross-cluster-replication.md#ccr-remote-recovery) process recopies the Lucene segment files from the leader.

::::{important} 
Recreating the follower index is a destructive action. All existing Lucene segment files are deleted on the cluster containing the follower index.
::::


To recreate a follower index, [access Cross-Cluster Replication](manage-cross-cluster-replication.md#ccr-access-ccr) and choose the **Follower indices** tab.

Select the follower index and pause replication. When the follower index status changes to Paused, reselect the follower index and choose to unfollow the leader index.

The follower index will be converted to a standard index and will no longer display on the Cross-Cluster Replication page.

In the side navigation, choose **Index Management**. Select the follower index from the previous steps and close the follower index.

You can then [recreate the follower index](ccr-getting-started-follower-index.md) to restart the replication process.

::::{dropdown} Use the API
Use the [pause follow API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-pause-follow) to pause the replication process. Then, close the follower index and recreate it. For example:

```console
POST /follower_index/_ccr/pause_follow

POST /follower_index/_close

PUT /follower_index/_ccr/follow?wait_for_active_shards=1
{
  "remote_cluster" : "remote_cluster",
  "leader_index" : "leader_index"
}
```

::::


