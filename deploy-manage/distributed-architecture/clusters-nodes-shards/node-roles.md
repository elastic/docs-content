---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/node-roles-overview.html
---

# Node roles [node-roles-overview]

Any time that you start an instance of {{es}}, you are starting a *node*. A collection of connected nodes is called a [cluster](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md). If you are running a single node of {{es}}, then you have a cluster of one node. All nodes know about all the other nodes in the cluster and can forward client requests to the appropriate node.

Each node performs one or more roles. Roles control the behavior of the node in the cluster.

## Set node roles [set-node-roles]

You define a node’s roles by setting `node.roles` in [`elasticsearch.yml`](../../deploy/self-managed/configure-elasticsearch.md). If you set `node.roles`, the node is only assigned the roles you specify. If you don’t set `node.roles`, the node is assigned the following roles:

* `master`
* `data`
* `data_content`
* `data_hot`
* `data_warm`
* `data_cold`
* `data_frozen`
* `ingest`
* `ml`
* `remote_cluster_client`
* `transform`

::::{important}
If you set `node.roles`, ensure you specify every node role your cluster needs. Every cluster requires the following node roles:

* `master`
* `data_content` and `data_hot`<br> OR<br> `data`

Some {{stack}} features also require specific node roles:

* {{ccs-cap}} and {{ccr}} require the `remote_cluster_client` role.
* {{stack-monitor-app}} and ingest pipelines require the `ingest` role.
* {{fleet}}, the {{security-app}}, and {{transforms}} require the `transform` role. The `remote_cluster_client` role is also required to use {{ccs}} with these features.
* {{ml-cap}} features, such as {{anomaly-detect}}, require the `ml` role.

::::


As the cluster grows and in particular if you have large {{ml}} jobs or {{ctransforms}}, consider separating dedicated master-eligible nodes from dedicated data nodes, {{ml}} nodes, and {{transform}} nodes.


## Change the role of a node [change-node-role]

Each data node maintains the following data on disk:

* the shard data for every shard allocated to that node,
* the index metadata corresponding with every shard allocated to that node, and
* the cluster-wide metadata, such as settings and index templates.

Similarly, each master-eligible node maintains the following data on disk:

* the index metadata for every index in the cluster, and
* the cluster-wide metadata, such as settings and index templates.

Each node checks the contents of its data path at startup. If it discovers unexpected data then it will refuse to start. This is to avoid importing unwanted [dangling indices](elasticsearch://reference/elasticsearch/configuration-reference/local-gateway.md#dangling-indices) which can lead to a red cluster health. To be more precise, nodes without the `data` role will refuse to start if they find any shard data on disk at startup, and nodes without both the `master` and `data` roles will refuse to start if they have any index metadata on disk at startup.

It is possible to change the roles of a node by adjusting its `elasticsearch.yml` file and restarting it. This is known as *repurposing* a node. In order to satisfy the checks for unexpected data described above, you must perform some extra steps to prepare a node for repurposing when starting the node without the `data` or `master` roles.

* If you want to repurpose a data node by removing the `data` role then you should first use an [allocation filter](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-shard-allocation-filtering) to safely migrate all the shard data onto other nodes in the cluster.
* If you want to repurpose a node to have neither the `data` nor `master` roles then it is simplest to start a brand-new node with an empty data path and the desired roles. You may find it safest to use an [allocation filter](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-shard-allocation-filtering) to migrate the shard data elsewhere in the cluster first.

If it is not possible to follow these extra steps then you may be able to use the [`elasticsearch-node repurpose`](elasticsearch://reference/elasticsearch/command-line-tools/node-tool.md#node-tool-repurpose) tool to delete any excess data that prevents a node from starting.


## Available node roles [node-roles-list]

The following is a list of the roles that a node can perform in a cluster. A node can have one or more roles.

* [Master-eligible node](#master-node-role) (`master`): A node that is eligible to be [elected as the *master* node](../discovery-cluster-formation.md), which controls the cluster.
* [Data node](#data-node-role) (`data`, `data_content`, `data_hot`, `data_warm`, `data_cold`, `data_frozen`): A node that has one of several data roles. Data nodes hold data and perform data related operations such as CRUD, search, and aggregations. You might use multiple data roles in a cluster so you can implement [data tiers](../../../manage-data/lifecycle/data-tiers.md).
* [Ingest node](#node-ingest-node) (`ingest`): Ingest nodes are able to apply an [ingest pipeline](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md) to a document in order to transform and enrich the document before indexing. With a heavy ingest load, it makes sense to use dedicated ingest nodes and to not include the `ingest` role from nodes that have the `master` or `data` roles.
* [Remote-eligible node](#remote-node) (`remote_cluster_client`): A node that is eligible to act as a remote client.
* [Machine learning node](#ml-node-role) (`ml`): A node that can run {{ml-features}}. If you want to use {{ml-features}}, there must be at least one {{ml}} node in your cluster. For more information, see [Machine learning settings](../../deploy/self-managed/configure-elasticsearch.md) and [Machine learning in the {{stack}}](/explore-analyze/machine-learning.md).
* [{{transform-cap}} node](#transform-node-role) (`transform`): A node that can perform {{transforms}}. If you want to use {{transforms}}, there must be at least one {{transform}} node in your cluster. For more information, see [{{transforms-cap}} settings](../../deploy/self-managed/configure-elasticsearch.md) and [*Transforming data*](../../../explore-analyze/transforms.md).

::::{admonition} Coordinating node
:class: note

:name: coordinating-node

Requests like search requests or bulk-indexing requests may involve data held on different data nodes. A search request, for example, is executed in two phases which are coordinated by the node which receives the client request — the *coordinating node*.

In the *scatter* phase, the coordinating node forwards the request to the data nodes which hold the data. Each data node executes the request locally and returns its results to the coordinating node. In the *gather* phase, the coordinating node reduces each data node’s results into a single global result set.

Every node is implicitly a coordinating node. This means that a node that has an explicit empty list of roles in the `node.roles` setting will only act as a coordinating node, which cannot be disabled. As a result, such a node needs to have enough memory and CPU in order to deal with the gather phase.

::::



### Master-eligible node [master-node-role]

The master node is responsible for lightweight cluster-wide actions such as creating or deleting an index, tracking which nodes are part of the cluster, and deciding which shards to allocate to which nodes. It is important for cluster health to have a stable master node.

Any master-eligible node that is not a [voting-only node](#voting-only-node) may be elected to become the master node by the [master election process](../discovery-cluster-formation.md).

::::{important}
Master nodes must have a `path.data` directory whose contents persist across restarts, just like data nodes, because this is where the cluster metadata is stored. The cluster metadata describes how to read the data stored on the data nodes, so if it is lost then the data stored on the data nodes cannot be read.
::::



#### Dedicated master-eligible node [dedicated-master-node]

It is important for the health of the cluster that the elected master node has the resources it needs to fulfill its responsibilities. If the elected master node is overloaded with other tasks then the cluster will not operate well. The most reliable way to avoid overloading the master with other tasks is to configure all the master-eligible nodes to be *dedicated master-eligible nodes* which only have the `master` role, allowing them to focus on managing the cluster. Master-eligible nodes will still also behave as [coordinating nodes](#coordinating-node) that route requests from clients to the other nodes in the cluster, but you should *not* use dedicated master nodes for this purpose.

A small or lightly-loaded cluster may operate well if its master-eligible nodes have other roles and responsibilities, but once your cluster comprises more than a handful of nodes it usually makes sense to use dedicated master-eligible nodes.

To create a dedicated master-eligible node, set:

```yaml
node.roles: [ master ]
```


#### Voting-only master-eligible node [voting-only-node]

A voting-only master-eligible node is a node that participates in [master elections](../discovery-cluster-formation.md) but which will not act as the cluster’s elected master node. In particular, a voting-only node can serve as a tiebreaker in elections.

It may seem confusing to use the term "master-eligible" to describe a voting-only node since such a node is not actually eligible to become the master at all. This terminology is an unfortunate consequence of history: master-eligible nodes are those nodes that participate in elections and perform certain tasks during cluster state publications, and voting-only nodes have the same responsibilities even if they can never become the elected master.

To configure a master-eligible node as a voting-only node, include `master` and `voting_only` in the list of roles. For example to create a voting-only data node:

```yaml
node.roles: [ data, master, voting_only ]
```

::::{important}
Only nodes with the `master` role can be marked as having the `voting_only` role.
::::


High availability (HA) clusters require at least three master-eligible nodes, at least two of which are not voting-only nodes. Such a cluster will be able to elect a master node even if one of the nodes fails.

Voting-only master-eligible nodes may also fill other roles in your cluster. For instance, a node may be both a data node and a voting-only master-eligible node. A *dedicated* voting-only master-eligible nodes is a voting-only master-eligible node that fills no other roles in the cluster. To create a dedicated voting-only master-eligible node, set:

```yaml
node.roles: [ master, voting_only ]
```

Since dedicated voting-only nodes never act as the cluster’s elected master, they may require less heap and a less powerful CPU than the true master nodes. However all master-eligible nodes, including voting-only nodes, are on the critical path for [publishing cluster state updates](../discovery-cluster-formation/cluster-state-overview.md#cluster-state-publishing). Cluster state updates are usually independent of performance-critical workloads such as indexing or searches, but they are involved in management activities such as index creation and rollover, mapping updates, and recovery after a failure. The performance characteristics of these activities are a function of the speed of the storage on each master-eligible node, as well as the reliability and latency of the network interconnections between the elected master node and the other nodes in the cluster. You must therefore ensure that the storage and networking available to the nodes in your cluster are good enough to meet your performance goals.


### Data nodes [data-node-role]

Data nodes hold the shards that contain the documents you have indexed. Data nodes handle data related operations like CRUD, search, and aggregations. These operations are I/O-, memory-, and CPU-intensive. It is important to monitor these resources and to add more data nodes if they are overloaded.

The main benefit of having dedicated data nodes is the separation of the master and data roles.

In a multi-tier deployment architecture, you use specialized data roles to assign data nodes to specific tiers: `data_content`,`data_hot`, `data_warm`, `data_cold`, or `data_frozen`. A node can belong to multiple tiers.

If you want to include a node in all tiers, or if your cluster does not use multiple tiers, then you can use the generic `data` role.

[Cluster shard limits](../../deploy/self-managed/configure-elasticsearch.md#cluster-shard-limit) prevent creation of more than 1000 non-frozen shards per node, and 3000 frozen shards per dedicated frozen node. Make sure you have enough nodes of each type in your cluster to handle the number of shards you need.

::::{warning}
If you assign a node to a specific tier using a specialized data role, then you shouldn’t also assign it the generic `data` role. The generic `data` role takes precedence over specialized data roles.
::::



#### Generic data node [generic-data-node]

Generic data nodes are included in all content tiers. A node with a generic `data` role can fill any of the specialized data node roles.

To create a dedicated generic data node, set:

```yaml
node.roles: [ data ]
```


#### Content data node [data-content-node]

Content data nodes are part of the content tier. Data stored in the content tier is generally a collection of items such as a product catalog or article archive. Unlike time series data, the value of the content remains relatively constant over time, so it doesn’t make sense to move it to a tier with different performance characteristics as it ages. Content data typically has long data retention requirements, and you want to be able to retrieve items quickly regardless of how old they are.

Content tier nodes are usually optimized for query performance—​they prioritize processing power over IO throughput so they can process complex searches and aggregations and return results quickly. While they are also responsible for indexing, content data is generally not ingested at as high a rate as time series data such as logs and metrics. From a resiliency perspective the indices in this tier should be configured to use one or more replicas.

The content tier is required and is often deployed within the same node grouping as the hot tier. System indices and other indices that aren’t part of a data stream are automatically allocated to the content tier.

To create a dedicated content node, set:

```yaml
node.roles: [ data_content ]
```


#### Hot data node [data-hot-node]

Hot data nodes are part of the hot tier. The hot tier is the {{es}} entry point for time series data and holds your most-recent, most-frequently-searched time series data. Nodes in the hot tier need to be fast for both reads and writes, which requires more hardware resources and faster storage (SSDs). For resiliency, indices in the hot tier should be configured to use one or more replicas.

The hot tier is required. New indices that are part of a [data stream](../../../manage-data/data-store/data-streams.md) are automatically allocated to the hot tier.

To create a dedicated hot node, set:

```yaml
node.roles: [ data_hot ]
```


#### Warm data node [data-warm-node]

Warm data nodes are part of the warm tier. Time series data can move to the warm tier once it is being queried less frequently than the recently-indexed data in the hot tier. The warm tier typically holds data from recent weeks. Updates are still allowed, but likely infrequent. Nodes in the warm tier generally don’t need to be as fast as those in the hot tier. For resiliency, indices in the warm tier should be configured to use one or more replicas.

To create a dedicated warm node, set:

```yaml
node.roles: [ data_warm ]
```


#### Cold data node [data-cold-node]

Cold data nodes are part of the cold tier. When you no longer need to search time series data regularly, it can move from the warm tier to the cold tier. While still searchable, this tier is typically optimized for lower storage costs rather than search speed.

For better storage savings, you can keep [fully mounted indices](../../tools/snapshot-and-restore/searchable-snapshots.md#fully-mounted) of [{{search-snaps}}](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md) on the cold tier. Unlike regular indices, these fully mounted indices don’t require replicas for reliability. In the event of a failure, they can recover data from the underlying snapshot instead. This potentially halves the local storage needed for the data. A snapshot repository is required to use fully mounted indices in the cold tier. Fully mounted indices are read-only.

Alternatively, you can use the cold tier to store regular indices with replicas instead of using {{search-snaps}}. This lets you store older data on less expensive hardware but doesn’t reduce required disk space compared to the warm tier.

To create a dedicated cold node, set:

```yaml
node.roles: [ data_cold ]
```


#### Frozen data node [data-frozen-node]

Frozen data nodes are part of the frozen tier. Once data is no longer being queried, or being queried rarely, it may move from the cold tier to the frozen tier where it stays for the rest of its life.

The frozen tier requires a snapshot repository. The frozen tier uses [partially mounted indices](../../tools/snapshot-and-restore/searchable-snapshots.md#partially-mounted) to store and load data from a snapshot repository. This reduces local storage and operating costs while still letting you search frozen data. Because {{es}} must sometimes fetch frozen data from the snapshot repository, searches on the frozen tier are typically slower than on the cold tier.

To create a dedicated frozen node, set:

```yaml
node.roles: [ data_frozen ]
```


### Ingest node [node-ingest-node]

Ingest nodes can execute pre-processing pipelines, composed of one or more ingest processors. Depending on the type of operations performed by the ingest processors and the required resources, it may make sense to have dedicated ingest nodes, that will only perform this specific task.

To create a dedicated ingest node, set:

```yaml
node.roles: [ ingest ]
```


### Coordinating only node [coordinating-only-node-role]

If you take away the ability to be able to handle master duties, to hold data, and pre-process documents, then you are left with a *coordinating* node that can only route requests, handle the search reduce phase, and distribute bulk indexing. Essentially, coordinating only nodes behave as smart load balancers.

Coordinating only nodes can benefit large clusters by offloading the coordinating node role from data and master-eligible nodes. They join the cluster and receive the full [cluster state](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-state), like every other node, and they use the cluster state to route requests directly to the appropriate place(s).

::::{warning}
Adding too many coordinating only nodes to a cluster can increase the burden on the entire cluster because the elected master node must await acknowledgement of cluster state updates from every node! The benefit of coordinating only nodes should not be overstated — data nodes can happily serve the same purpose.
::::


To create a dedicated coordinating node, set:

```yaml
node.roles: [ ]
```


### Remote-eligible node [remote-node]

A remote-eligible node acts as a cross-cluster client and connects to [remote clusters](../../remote-clusters.md). Once connected, you can search remote clusters using [{{ccs}}](../../../solutions/search/cross-cluster-search.md). You can also sync data between clusters using [{{ccr}}](../../tools/cross-cluster-replication.md).

```yaml
node.roles: [ remote_cluster_client ]
```


### Machine learning node [ml-node-role]

{{ml-cap}} nodes run jobs and handle {{ml}} API requests. For more information, see [Machine learning settings](../../deploy/self-managed/configure-elasticsearch.md).

To create a dedicated {{ml}} node, set:

```yaml
node.roles: [ ml, remote_cluster_client]
```

The `remote_cluster_client` role is optional but strongly recommended. Otherwise, {{ccs}} fails when used in {{ml}} jobs or {{dfeeds}}. If you use {{ccs}} in your {{anomaly-jobs}}, the `remote_cluster_client` role is also required on all master-eligible nodes. Otherwise, the {{dfeed}} cannot start. See [Remote-eligible node](#remote-node).


### {{transform-cap}} node [transform-node-role]

{{transform-cap}} nodes run {{transforms}} and handle {{transform}} API requests. For more information, see [{{transforms-cap}} settings](../../deploy/self-managed/configure-elasticsearch.md).

To create a dedicated {{transform}} node, set:

```yaml
node.roles: [ transform, remote_cluster_client ]
```

The `remote_cluster_client` role is optional but strongly recommended. Otherwise, {{ccs}} fails when used in {{transforms}}. See [Remote-eligible node](#remote-node).

