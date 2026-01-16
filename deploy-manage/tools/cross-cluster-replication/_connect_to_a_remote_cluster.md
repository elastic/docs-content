---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_connect_to_a_remote_cluster.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Connect to a remote cluster [_connect_to_a_remote_cluster]

To replicate an index on a remote cluster (Cluster A) to a local cluster (Cluster B), you configure Cluster A as a remote on Cluster B.

:::{image} /deploy-manage/images/elasticsearch-reference-ccr-tutorial-clusters.png
:alt: ClusterA contains the leader index and ClusterB contains the follower index
:::

To connect to a remote cluster, you consider the preferred [security model](/deploy-manage/remote-clusters/security-models.md) to use for authenticating remote connections between clusters, choose a [connection mode](/deploy-manage/remote-clusters/connection-modes.md), and depending on where the cluster you want to use as remote is hosted, you configure its connection address.

Find detailed instructions on the available options for your specific scenario:
  * [](/deploy-manage/remote-clusters/remote-clusters-self-managed.md#add-remote-clusters)
  * [](/deploy-manage/remote-clusters/ec-enable-ccs.md#set-up-remote-clusters-ech)
  * [](/deploy-manage/remote-clusters/ece-enable-ccs.md#set-up-remote-clusters-ece)
  * [](/deploy-manage/remote-clusters/eck-remote-clusters-landing.md#eck-rcs-setup)
