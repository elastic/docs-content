---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_data_store_architecture.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
---

# Distributed architecture [_data_store_architecture]

{{es}} is a distributed document store. Instead of storing information as rows of columnar data, {{es}} stores complex data structures that have been serialized as JSON documents. When you have multiple {{es}} nodes in a cluster, stored documents are distributed across the cluster and can be accessed immediately from any node.

The topics in this section provides information about the architecture of {{es}} and how it stores and retrieves data:

::::{note}
{{serverless-full}} scales with your workload and automates nodes, shards, and replicas for you. Some of the content in this section does not apply to you if you are using {{serverless-full}}. Instead, the information in this section will provide you information about how the platform works for you.
::::

* [Cluster, nodes, and shards](distributed-architecture/clusters-nodes-shards.md): Learn about the basic building blocks of an {{es}} cluster, including nodes, shards, primaries, and replicas.
  * [Node roles](distributed-architecture/clusters-nodes-shards/node-roles.md): Learn about the different roles that nodes can have in an {{es}} cluster.
* [Reading and writing documents](distributed-architecture/reading-and-writing-documents.md): Learn how {{es}} replicates read and write operations across shards and shard copies.
* [Shard allocation, relocation, and recovery](distributed-architecture/shard-allocation-relocation-recovery.md): Learn how {{es}} allocates and balances shards across nodes.
  * [Shard allocation awareness](distributed-architecture/shard-allocation-relocation-recovery/shard-allocation-awareness.md): Learn how to use custom node attributes to distribute shards across different racks or availability zones.
* [Discovery and cluster formation](distributed-architecture/discovery-cluster-formation.md): Learn about the cluster formation process including voting, adding nodes and publishing the cluster state.
* [Shard request cache](/deploy-manage/distributed-architecture/shard-request-cache.md): Learn how {{es}} caches search requests to improve performance.
* [{{kib}} task management](distributed-architecture/kibana-tasks-management.md): Learn how {{kib}} runs background tasks and distribute work across multiple {{kib}} instances to be persistent and scale with your deployment.