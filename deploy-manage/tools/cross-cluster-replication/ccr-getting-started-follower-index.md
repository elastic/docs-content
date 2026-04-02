---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-getting-started-follower-index.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Create a follower index to replicate a specific index [ccr-getting-started-follower-index]

When you create a follower index, you reference the remote cluster and the leader index in your remote cluster.

To create a follower index in {{kib}}:

1. Go to the **Cross Cluster Replication** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Choose the **Follower Indices** tab.
3. Choose the cluster (ClusterA) containing the leader index you want to replicate.
4. Enter the name of the leader index, which is `kibana_sample_data_ecommerce` if you are following the tutorial.
5. Enter a name for your follower index, such as `follower-kibana-sample-data`.

{{es}} initializes the follower using the [remote recovery](../cross-cluster-replication.md#ccr-remote-recovery) process, which transfers the existing Lucene segment files from the leader index to the follower index. The index status changes to **Paused**. When the remote recovery process is complete, the index following begins and the status changes to **Active**.

When you index documents into your leader index, {{es}} replicates the documents in the follower index.

:::{image} /deploy-manage/images/elasticsearch-reference-ccr-follower-index.png
:alt: The Cross-Cluster Replication page in {{kib}}
:screenshot:
:::

::::{dropdown} API example
You can also use the [create follower API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-follow) to create follower indices. When you create a follower index, you must reference the remote cluster and the leader index that you created in the remote cluster.

When initiating the follower request, the response returns before the [remote recovery](../cross-cluster-replication.md#ccr-remote-recovery) process completes. To wait for the process to complete, add the `wait_for_active_shards` parameter to your request.

```console
PUT /server-metrics-follower/_ccr/follow?wait_for_active_shards=1
{
  "remote_cluster" : "leader",
  "leader_index" : "server-metrics"
}
```

Use the [get follower stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-follow-stats) to inspect the status of replication.

::::


