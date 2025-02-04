---
navigation_title: "Uni-directional disaster recovery"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-disaster-recovery-uni-directional-tutorial.html
---



# Uni-directional disaster recovery [ccr-disaster-recovery-uni-directional-tutorial]


Learn how to failover and failback between two clusters based on uni-directional {{ccr}}. You can also visit [Bi-directional disaster recovery](bi-directional-disaster-recovery.md) to set up replicating data streams that automatically failover and failback without human intervention.

* Setting up uni-directional {{ccr}} replicated from `clusterA` to `clusterB`.
* Failover - If `clusterA` goes offline, `clusterB` needs to "promote" follower indices to regular indices to allow write operations. All ingestion will need to be redirected to `clusterB`, this is controlled by the clients ({{ls}}, {{beats}}, {{agents}}, etc).
* Failback - When `clusterA` is back online, it assumes the role of a follower and replicates the leader indices from `clusterB`.

:::{image} ../../../images/elasticsearch-reference-ccr-uni-directional-disaster-recovery.png
:alt: Uni-directional cross cluster replication failover and failback
:::

::::{note}
{{ccr-cap}} provides functionality to replicate user-generated indices only. {{ccr-cap}} isn’t designed for replicating system-generated indices or snapshot settings, and can’t replicate {{ilm-init}} or {{slm-init}} policies across clusters. Learn more in {{ccr}} [limitations](../cross-cluster-replication.md#ccr-limitations).
::::





