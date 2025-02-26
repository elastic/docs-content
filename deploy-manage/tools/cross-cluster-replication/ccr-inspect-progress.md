---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-inspect-progress.html

applies_to:
  deployment:
    eck: 
    ess: 
    ece: 
    self: 
---

# Inspect replication statistics [ccr-inspect-progress]

To inspect the progress of replication for a follower index and view detailed shard statistics, [access Cross-Cluster Replication](manage-cross-cluster-replication.md#ccr-access-ccr) and choose the **Follower indices** tab.

Select the name of the follower index you want to view replication details for. The slide-out panel shows settings and replication statistics for the follower index, including read and write operations that are managed by the follower shard.

To view more detailed statistics, click **View in Index Management**, and then select the name of the follower index in Index Management. Open the tabs for detailed statistics about the follower index.

::::{dropdown} API example
Use the [get follower stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-follow-stats) to inspect replication progress at the shard level. This API provides insight into the read and writes managed by the follower shard. The API also reports read exceptions that can be retried and fatal exceptions that require user intervention.

::::


