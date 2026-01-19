---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_connect_to_a_remote_cluster.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Connect to a remote cluster [_connect_to_a_remote_cluster]

Cross-cluster replication (CCR) relies on the [remote clusters](/deploy-manage/remote-clusters.md) feature. Before configuring CCR, ensure that the source cluster (Cluster A) is registered as a remote cluster on the destination cluster (Cluster B).


:::{image} /deploy-manage/images/elasticsearch-reference-ccr-tutorial-clusters.png
:alt: ClusterA contains the leader index and ClusterB contains the follower index
:::

:::{include} _snippets/terminology.md
:::

Connecting to a remote cluster depends on the environment your local and remote clusters are deployed on and the security model you wish to use.

The exact details needed to connect to a remote cluster vary. Select a suitable option for your specific scenario based on the local cluster you're configuring:
  * [](/deploy-manage/remote-clusters/remote-clusters-self-managed.md)
  * [](/deploy-manage/remote-clusters/ec-enable-ccs.md)
  * [](/deploy-manage/remote-clusters/ece-enable-ccs.md)
  * [](/deploy-manage/remote-clusters/eck-remote-clusters-landing.md)
