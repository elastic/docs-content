---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-auto-follow.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Manage auto-follow patterns [ccr-auto-follow]

To replicate time series indices, you configure an auto-follow pattern so that each new index in the series is replicated automatically. Whenever the name of a new index on the remote cluster matches the auto-follow pattern, a corresponding follower index is added to the local cluster.

::::{note}
Auto-follow patterns only match open indices on the remote cluster that have all primary shards started. Auto-follow patterns do not match indices that can’t be used for {{ccr-init}} such as [closed indices]({{es-apis}}operation/operation-indices-open) or [{{search-snaps}}](../snapshot-and-restore/searchable-snapshots.md). Avoid using an auto-follow pattern that matches indices with a [read or write block](elasticsearch://reference/elasticsearch/index-settings/index-block.md). These blocks prevent follower indices from replicating such indices.
::::

You can also create auto-follow patterns for data streams. When a new backing index is generated on a remote cluster, that index and its data stream are automatically followed if the data stream name matches an auto-follow pattern. If you create a data stream after creating the auto-follow pattern, all backing indices are followed automatically.

The data streams replicated from a remote cluster by {{ccr-init}} are protected from local rollovers. The [promote data stream API]({{es-apis}}operation/operation-indices-promote-data-stream) can be used to turn these data streams into regular data streams.

## Use {{ilm-init}} with auto-follow patterns [ccr-auto-follow-ilm]

Auto-follow patterns are especially useful with [{{ilm-cap}}](../../../manage-data/lifecycle/index-lifecycle-management.md). {{ilm-cap}} detects when a managed index participates in {{ccr}} as a leader or follower and adapts lifecycle actions that cannot run safely while replication is active.

{{ccr-cap}} copies the `index.lifecycle.name` setting from a leader index to its follower, but it [does not replicate the policy definition](../cross-cluster-replication.md#ccr-limitations). To manage follower indices with {{ilm}}, define a policy with that name on the local cluster. You can use the same policy definition on both clusters or configure different lifecycle actions and retention periods.

When {{ilm}} rolls over a matching leader index, the auto-follow pattern detects the new index and creates its corresponding follower on the local cluster. When the policy on the local cluster reaches the rollover action on the previous follower, {{ilm}} waits until indexing on the leader index is complete and all operations have been replicated. It then [unfollows the previous index automatically](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-unfollow.md) and continues its lifecycle without performing a separate rollover. The shrink and {{search-snap}} actions also trigger this automatic unfollow behavior.

::::{admonition} Index deletions
{{ccr-cap}} does not propagate index deletions. Auto-follow patterns do not delete follower indices when their leader indices are deleted.

The {{ilm}} delete action on a leader index waits until all follower indices cease following it. To manage follower index retention, define an appropriate lifecycle policy on the local cluster.
::::

## Access auto-follow patterns in {{kib}} [ccr-access-ccr-auto-follow]

To manage auto-follow patterns, open {{kib}} for the local cluster that contains the follower indices:

1. Go to the **Cross Cluster Replication** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the **Auto-follow patterns** tab.

From this tab, you can create, pause, resume, and delete auto-follow patterns.





