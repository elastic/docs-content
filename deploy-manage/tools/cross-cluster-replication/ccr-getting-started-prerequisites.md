---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-getting-started-prerequisites.html
---

# Prerequisites [ccr-getting-started-prerequisites]

To complete this tutorial, you need:

* The `manage` cluster privilege on the local cluster.
* A license on both clusters that includes {{ccr}}. [Activate a free 30-day trial](../../license/manage-your-license-in-self-managed-cluster.md).
* An index on the remote cluster that contains the data you want to replicate. This tutorial uses the sample eCommerce orders data set. [Load sample data](../../../explore-analyze/overview/kibana-quickstart.md#gs-get-data-into-kibana).
* In the local cluster, all nodes with the `master` [node role](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html#node-roles) must also have the [`remote_cluster_client`](../../distributed-architecture/clusters-nodes-shards/node-roles.md#remote-node) role. The local cluster must also have at least one node with both a data role and the [`remote_cluster_client`](../../distributed-architecture/clusters-nodes-shards/node-roles.md#remote-node) role. Individual tasks for coordinating replication scale based on the number of data nodes with the `remote_cluster_client` role in the local cluster.

