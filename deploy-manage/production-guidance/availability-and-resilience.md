---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/high-availability-cluster-design.html
---

# Availability and resilience [high-availability-cluster-design]

Distributed systems like {{es}} are designed to keep working even if some of their components have failed. As long as there are enough well-connected nodes to take over their responsibilities, an {{es}} cluster can continue operating normally if some of its nodes are unavailable or disconnected.

There is a limit to how small a resilient cluster can be. All {{es}} clusters require the following components to function:

* One [elected master node](../distributed-architecture/discovery-cluster-formation/modules-discovery-quorums.md)
* At least one node for each [role](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html)
* At least one copy of every [shard](../../deploy-manage/index.md)

A resilient cluster requires redundancy for every required cluster component. This means a resilient cluster must have the following components:

* At least three master-eligible nodes
* At least two nodes of each role
* At least two copies of each shard (one primary and one or more replicas, unless the index is a [searchable snapshot index](../tools/snapshot-and-restore/searchable-snapshots.md))

A resilient cluster needs three master-eligible nodes so that if one of them fails then the remaining two still form a majority and can hold a successful election.

Similarly, redundancy of nodes of each role means that if a node for a particular role fails, another node can take on its responsibilities.

Finally, a resilient cluster should have at least two copies of each shard. If one copy fails then there should be another good copy to take over. {{es}} automatically rebuilds any failed shard copies on the remaining nodes in order to restore the cluster to full health after a failure.

Failures temporarily reduce the total capacity of your cluster. In addition, after a failure the cluster must perform additional background activities to restore itself to health. You should make sure that your cluster has the capacity to handle your workload even if some nodes fail.

Depending on your needs and budget, an {{es}} cluster can consist of a single node, hundreds of nodes, or any number in between. When designing a smaller cluster, you should typically focus on making it resilient to single-node failures. Designers of larger clusters must also consider cases where multiple nodes fail at the same time. The following pages give some recommendations for building resilient clusters of various sizes:

* [Resilience in small clusters](availability-and-resilience/resilience-in-small-clusters.md)
* [Resilience in larger clusters](availability-and-resilience/resilience-in-larger-clusters.md)



