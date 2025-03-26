---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/high-availability-cluster-small-clusters.html
applies_to:
  deployment:
    self: all
    eck: all
---

# Resilience in small clusters [high-availability-cluster-small-clusters]

In smaller clusters, it is most important to be resilient to single-node failures. This section gives some guidance on making your cluster as resilient as possible to the failure of an individual node.

::::{note}
This document focuses on self-managed {{es}} deployments and describes resilience strategies for clusters with one to a few nodes. While the guidance is tailored to these environments, many of the core concepts, such as master elections, replica configuration, and client request distribution, are also relevant to other deployment types, like {{eck}}.

For a more in-depth description of how resilience is handled in {{ech}} and {{ece}}, refer to [](./resilience-in-ech.md).
::::

## One-node clusters [high-availability-cluster-design-one-node]

If your cluster consists of one node, that single node must do everything. To accommodate this, {{es}} assigns nodes every role by default.

A single node cluster is not resilient. If the node fails, the cluster will stop working. Because there are no replicas in a one-node cluster, you cannot store your data redundantly. However, by default at least one replica is required for a [`green` cluster health status](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health). To ensure your cluster can report a `green` status, override the default by setting [`index.number_of_replicas`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md) to `0` on every index.

If the node fails, you may need to restore an older copy of any lost indices from a [snapshot](../../tools/snapshot-and-restore.md).

Because they are not resilient to any failures, we do not recommend using one-node clusters in production.


## Two-node clusters [high-availability-cluster-design-two-nodes]

If you have two nodes, we recommend they both be data nodes. You should also ensure every shard is stored redundantly on both nodes by setting [`index.number_of_replicas`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md) to `1` on every index that is not a [searchable snapshot index](../../tools/snapshot-and-restore/searchable-snapshots.md). This is the default behaviour but may be overridden by an [index template](../../../manage-data/data-store/templates.md). [Auto-expand replicas](elasticsearch://reference/elasticsearch/index-settings/index-modules.md) can also achieve the same thing, but it’s not necessary to use this feature in such a small cluster.

We recommend you set only one of your two nodes to be [master-eligible](../../distributed-architecture/clusters-nodes-shards/node-roles.md#master-node-role). This means you can be certain which of your nodes is the elected master of the cluster. The cluster can tolerate the loss of the other master-ineligible node. If you set both nodes to master-eligible, two nodes are required for a master election. Since the election will fail if either node is unavailable, your cluster cannot reliably tolerate the loss of either node.

By default, each node is assigned every role. We recommend you assign both nodes all other roles except master eligibility. If one node fails, the other node can handle its tasks.

You should avoid sending client requests to just one of your nodes. If you do and this node fails, such requests will not receive responses even if the remaining node is a healthy cluster on its own. Ideally, you should balance your client requests across both nodes. A good way to do this is to specify the addresses of both nodes when configuring the client to connect to your cluster. Alternatively, you can use a resilient load balancer to balance client requests across the nodes in your cluster.

Because it’s not resilient to failures, we do not recommend deploying a two-node cluster in production.


## Two-node clusters with a tiebreaker [high-availability-cluster-design-two-nodes-plus]

Because master elections are majority-based, the two-node cluster described above is tolerant to the loss of one of its nodes but not the other one. You cannot configure a two-node cluster so that it can tolerate the loss of *either* node because this is theoretically impossible. You might expect that if either node fails then {{es}} can elect the remaining node as the master, but it is impossible to tell the difference between the failure of a remote node and a mere loss of connectivity between the nodes. If both nodes were capable of running independent elections, a loss of connectivity would lead to a [split-brain problem](https://en.wikipedia.org/wiki/Split-brain_(computing)) and therefore data loss. {{es}} avoids this and protects your data by electing neither node as master until that node can be sure that it has the latest cluster state and that there is no other master in the cluster. This could result in the cluster having no master until connectivity is restored.

You can solve this problem by adding a third node and making all three nodes master-eligible. A [master election](../../distributed-architecture/discovery-cluster-formation/modules-discovery-quorums.md) requires only two of the three master-eligible nodes. This means the cluster can tolerate the loss of any single node. This third node acts as a tiebreaker in cases where the two original nodes are disconnected from each other. You can reduce the resource requirements of this extra node by making it a [dedicated voting-only master-eligible node](../../distributed-architecture/clusters-nodes-shards/node-roles.md#voting-only-node), also known as a dedicated tiebreaker. Because it has no other roles, a dedicated tiebreaker does not need to be as powerful as the other two nodes. It will not perform any searches nor coordinate any client requests and cannot be elected as the master of the cluster.

The two original nodes should not be voting-only master-eligible nodes since a resilient cluster requires at least three master-eligible nodes, at least two of which are not voting-only master-eligible nodes. If two of your three nodes are voting-only master-eligible nodes then the elected master must be the third node. This node then becomes a single point of failure.

We recommend assigning both non-tiebreaker nodes all other roles. This creates redundancy by ensuring any task in the cluster can be handled by either node.

You should not send any client requests to the dedicated tiebreaker node. You should also avoid sending client requests to just one of the other two nodes. If you do, and this node fails, then any requests will not receive responses, even if the remaining nodes form a healthy cluster. Ideally, you should balance your client requests across both of the non-tiebreaker nodes. You can do this by specifying the address of both nodes when configuring your client to connect to your cluster. Alternatively, you can use a resilient load balancer to balance client requests across the appropriate nodes in your cluster. The [Elastic Cloud](https://cloud.elastic.co/registration?page=docs&placement=docs-body) service provides such a load balancer.

A two-node cluster with an additional tiebreaker node is the smallest possible cluster that is suitable for production deployments.


## Three-node clusters [high-availability-cluster-design-three-nodes]

If you have three nodes, we recommend they all be [data nodes](../../distributed-architecture/clusters-nodes-shards/node-roles.md#data-node-role) and every index that is not a [searchable snapshot index](../../tools/snapshot-and-restore/searchable-snapshots.md) should have at least one replica. Nodes are data nodes by default. You may prefer for some indices to have two replicas so that each node has a copy of each shard in those indices. You should also configure each node to be [master-eligible](../../distributed-architecture/clusters-nodes-shards/node-roles.md#master-node-role) so that any two of them can hold a master election without needing to communicate with the third node. Nodes are master-eligible by default. This cluster will be resilient to the loss of any single node.

You should avoid sending client requests to just one of your nodes. If you do, and this node fails, then any requests will not receive responses even if the remaining two nodes form a healthy cluster. Ideally, you should balance your client requests across all three nodes. You can do this by specifying the address of multiple nodes when configuring your client to connect to your cluster. Alternatively you can use a resilient load balancer to balance client requests across your cluster. The [Elastic Cloud](https://cloud.elastic.co/registration?page=docs&placement=docs-body) service provides such a load balancer.


## Clusters with more than three nodes [high-availability-cluster-design-three-plus-nodes]

Once your cluster grows to more than three nodes, you can start to specialise these nodes according to their responsibilities, allowing you to scale their resources independently as needed. You can have as many [data nodes](../../distributed-architecture/clusters-nodes-shards/node-roles.md#data-node-role), [ingest nodes](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md), [{{ml}} nodes](../../distributed-architecture/clusters-nodes-shards/node-roles.md#ml-node-role), etc. as needed to support your workload. As your cluster grows larger, we recommend using dedicated nodes for each role. This allows you to independently scale resources for each task.

However, it is good practice to limit the number of master-eligible nodes in the cluster to three. Master nodes do not scale like other node types since the cluster always elects just one of them as the master of the cluster. If there are too many master-eligible nodes then master elections may take a longer time to complete. In larger clusters, we recommend you configure some of your nodes as dedicated master-eligible nodes and avoid sending any client requests to these dedicated nodes. Your cluster may become unstable if the master-eligible nodes are overwhelmed with unnecessary extra work that could be handled by one of the other nodes.

You may configure one of your master-eligible nodes to be a [voting-only node](../../distributed-architecture/clusters-nodes-shards/node-roles.md#voting-only-node) so that it can never be elected as the master node. For instance, you may have two dedicated master nodes and a third node that is both a data node and a voting-only master-eligible node. This third voting-only node will act as a tiebreaker in master elections but will never become the master itself.


## Summary [high-availability-cluster-design-small-cluster-summary]

The cluster will be resilient to the loss of any node as long as:

* The [cluster health status](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health) is `green`.
* There are at least two data nodes.
* Every index that is not a [searchable snapshot index](../../tools/snapshot-and-restore/searchable-snapshots.md) has at least one replica of each shard, in addition to the primary.
* The cluster has at least three master-eligible nodes, as long as at least two of these nodes are not voting-only master-eligible nodes.
* Clients are configured to send their requests to more than one node or are configured to use a load balancer that balances the requests across an appropriate set of nodes. The [Elastic Cloud](https://cloud.elastic.co/registration?page=docs&placement=docs-body) service provides such a load balancer.


