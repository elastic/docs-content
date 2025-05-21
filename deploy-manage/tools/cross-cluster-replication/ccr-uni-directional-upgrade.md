---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-uni-directional-upgrade.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Uni-directional index following [ccr-uni-directional-upgrade]

In a uni-directional configuration, one cluster contains only leader indices, and the other cluster contains only follower indices that replicate the leader indices.

In this strategy, the cluster with follower indices should be upgraded first and the cluster with leader indices should be upgraded last. Upgrading the clusters in this order ensures that index following can continue during the upgrade without downtime.

You can also use this strategy to upgrade a [replication chain](../cross-cluster-replication.md#ccr-chained-replication). Start by upgrading clusters at the end of the chain and working your way back to the cluster that contains the leader indices.

For example, consider a configuration where Cluster A contains all leader indices. Cluster B follows indices in Cluster A, and Cluster C follows indices in Cluster B.

```
Cluster A
        ^--Cluster B
                   ^--Cluster C
```
In this configuration, upgrade the clusters in the following order:

1. Cluster C
2. Cluster B
3. Cluster A

