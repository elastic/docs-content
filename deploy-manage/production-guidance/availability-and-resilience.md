---
navigation_title: Design for resilience
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/high-availability-cluster-design.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
---

% In the future we could consider merging the ECE/ECH resiliency doc with the content of the 2 original ES docs about resilience (small and large clusters), as some of the topics and concepts overlap
# Design for resilience [high-availability-cluster-design]

Distributed systems like {{es}} are designed to keep working even if some of their components have failed. As long as there are enough well-connected nodes to take over their responsibilities, an {{es}} cluster can continue operating normally if some of its nodes are unavailable or disconnected.

{{es}} implements high availability (HA) at three key levels:

* **Node level**: Running multiple nodes within the cluster to avoid single points of failure and maintain operational stability.
* **Cluster level**: Ensuring redundancy by distributing nodes and shards across availability zones to prevent failures from affecting the entire cluster.
* **Index level**: Configuring shard replication to protect against data loss and improve search performance by distributing queries across multiple copies.

Each of these HA mechanisms contributes to {{es}}’s resilience and scalability. The appropriate strategy depends on factors such as data criticality, query patterns, and infrastructure constraints. It is up to you to determine the level of resiliency and high availability that best fits your use case. This section provides detailed guidance on designing a production-ready {{es}} deployment that balances availability, performance, and scalability.

::::{note}
* In the context of {{es}} deployments, an `availability zone`, or simply `zone`, represents an isolated failure domain within your infrastructure. Depending on the design of your cluster, this could be a physically separate data center, a different section within the same data center, distinct server racks, or logically separated node groups. The goal of using availability zones is to minimize the risk of a single point of failure affecting the entire deployment.

* For example, in {{ech}}, availability zones correspond to the cloud provider’s availability zones. Each of these is typically a physically separate data center, ensuring redundancy and fault tolerance at the infrastructure level.
::::

## Cluster sizes

There is a limit to how small a resilient cluster can be. All {{es}} clusters require the following components to function:

* One [elected master node](../distributed-architecture/discovery-cluster-formation/modules-discovery-quorums.md)
* At least one node for each [role](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md)
* At least one copy of every [shard](../../deploy-manage/index.md)

A resilient cluster requires redundancy for every required cluster component. This means a resilient cluster must have the following components:

* At least three master-eligible nodes
* At least two nodes of each role
* At least two copies of each shard (one primary and one or more replicas, unless the index is a [searchable snapshot index](../tools/snapshot-and-restore/searchable-snapshots.md))

A resilient cluster needs three master-eligible nodes so that if one of them fails then the remaining two still form a majority and can hold a successful election.

Similarly, redundancy of nodes of each role means that if a node for a particular role fails, another node can take on its responsibilities.

Finally, a resilient cluster should have at least two copies of each shard. If one copy fails then there should be another good copy to take over. {{es}} automatically rebuilds any failed shard copies on the remaining nodes in order to restore the cluster to full health after a failure.

::::{important}
Failures temporarily reduce the total capacity of your cluster. After a failure, the cluster must also perform background activities to restore itself to health. You should make sure that your cluster has the capacity to handle your workload even if some nodes fail.
::::

Depending on your needs and budget, an {{es}} cluster can consist of a single node, hundreds of nodes, or any number in between. When designing a smaller cluster, you should typically focus on making it resilient to single-node failures. Designers of larger clusters must also consider cases where multiple nodes fail at the same time.

The following pages give some recommendations for building resilient clusters of various sizes:

* [Resilience in small clusters](availability-and-resilience/resilience-in-small-clusters.md)
* [Resilience in larger clusters](availability-and-resilience/resilience-in-larger-clusters.md)

In addition, the following page outlines how {{ech}} and {{ece}} orchestrators implement resilience, and offers guidance to ensure your deployments follow best practices:

* [Resilience in {{ech}} and {{ece}} deployments](./availability-and-resilience/resilience-in-ech.md)
