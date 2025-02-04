---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-pause-replication.html
---

# Pause and resume replication [ccr-pause-replication]

To pause and resume replication of the leader index, [access Cross-Cluster Replication](manage-cross-cluster-replication.md#ccr-access-ccr) and choose the **Follower indices** tab.

Select the follower index you want to pause and choose **Manage > Pause Replication**. The follower index status changes to Paused.

To resume replication, select the follower index and choose **Resume replication**.

::::{dropdown} API example
You can pause replication with the [pause follower API](https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-post-pause-follow.html) and then later resume replication with the [resume follower API](https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-post-resume-follow.html). Using these APIs in tandem enables you to adjust the read and write parameters on the follower shard task if your initial configuration is not suitable for your use case.

::::


