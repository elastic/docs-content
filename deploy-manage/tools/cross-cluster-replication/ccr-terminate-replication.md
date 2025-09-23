---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-terminate-replication.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Terminate replication [ccr-terminate-replication]

You can unfollow a leader index to terminate replication and convert the follower index to a standard index.

[Access Cross-Cluster Replication](manage-cross-cluster-replication.md#ccr-access-ccr) and choose the **Follower indices** tab.

Select the follower index and pause replication. When the follower index status changes to Paused, reselect the follower index and choose to unfollow the leader index.

The follower index will be converted to a standard index and will no longer display on the Cross-Cluster Replication page.

You can then choose **Index Management**, select the follower index from the previous steps, and close the follower index.

::::{dropdown} Use the API
You can terminate replication with the [unfollow API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-unfollow). This API converts a follower index to a standard (non-follower) index.

::::


