---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-auto-follow.html
---

# Manage auto-follow patterns [ccr-auto-follow]

To replicate time series indices, you configure an auto-follow pattern so that each new index in the series is replicated automatically. Whenever the name of a new index on the remote cluster matches the auto-follow pattern, a corresponding follower index is added to the local cluster.

::::{note} 
Auto-follow patterns only match open indices on the remote cluster that have all primary shards started. Auto-follow patterns do not match indices that can’t be used for {{ccr-init}} such as [closed indices](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-open) or [{{search-snaps}}](../snapshot-and-restore/searchable-snapshots.md). Avoid using an auto-follow pattern that matches indices with a [read or write block](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-blocks.html#index-block-settings). These blocks prevent follower indices from replicating such indices.
::::


You can also create auto-follow patterns for data streams. When a new backing index is generated on a remote cluster, that index and its data stream are automatically followed if the data stream name matches an auto-follow pattern. If you create a data stream after creating the auto-follow pattern, all backing indices are followed automatically.

The data streams replicated from a remote cluster by CCR are protected from local rollovers. The [promote data stream API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-promote-data-stream) can be used to turn these data streams into regular data streams.

Auto-follow patterns are especially useful with [{{ilm-cap}}](../../../manage-data/lifecycle/index-lifecycle-management.md), which might continually create new indices on the cluster containing the leader index.

$$$ccr-access-ccr-auto-follow$$$
To start using {{ccr}} auto-follow patterns from Stack Management in {{kib}}, select **Cross-Cluster Replication** from the side navigation and choose the **Auto-follow patterns** tab.





