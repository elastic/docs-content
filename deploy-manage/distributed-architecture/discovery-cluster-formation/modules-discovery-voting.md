---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-discovery-voting.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Voting configurations [modules-discovery-voting]

Each {{es}} cluster has a *voting configuration*, which is the set of [master-eligible nodes](../clusters-nodes-shards/node-roles.md#master-node-role) whose responses are counted when making decisions such as electing a new master or committing a new cluster state. Decisions are made only after a majority (more than half) of the nodes in the voting configuration respond.

Usually the voting configuration is the same as the set of all the master-eligible nodes that are currently in the cluster. However, there are some situations in which they may be different.

::::{important}
To be sure that the cluster remains available you **must not stop half or more of the nodes in the voting configuration at the same time**. As long as more than half of the voting nodes are available the cluster can still work normally. This means that if there are three or four master-eligible nodes, the cluster can tolerate one of them being unavailable. If there are two or fewer master-eligible nodes, they must all remain available.

If you stop half or more of the nodes in the voting configuration at the same time then the cluster will be unavailable until you bring enough nodes back online to form a quorum again. While the cluster is unavailable, any remaining nodes will report in their logs that they cannot discover or elect a master node. See [*Troubleshooting discovery*](../../../troubleshoot/elasticsearch/discovery-troubleshooting.md) for more information.

::::


After a node joins or leaves the cluster, {{es}} reacts by automatically making corresponding changes to the voting configuration in order to ensure that the cluster is as resilient as possible. It is important to wait for this adjustment to complete before you remove more nodes from the cluster. For more information, see [*Add and remove nodes in your cluster*](../../maintenance/add-and-remove-elasticsearch-nodes.md).

The current voting configuration is stored in the cluster state so you can inspect its current contents as follows:

```console
GET /_cluster/state?filter_path=metadata.cluster_coordination.last_committed_config
```

::::{note}
The current voting configuration is not necessarily the same as the set of all available master-eligible nodes in the cluster. Altering the voting configuration involves taking a vote, so it takes some time to adjust the configuration as nodes join or leave the cluster. Also, there are situations where the most resilient configuration includes unavailable nodes or does not include some available nodes. In these situations, the voting configuration differs from the set of available master-eligible nodes in the cluster.
::::

Larger voting configurations are usually more resilient, so {{es}} normally prefers to add master-eligible nodes to the voting configuration after they join the cluster. Similarly, if a node in the voting configuration leaves the cluster and there is another master-eligible node in the cluster that is not in the voting configuration then it is preferable to swap these two nodes over. The size of the voting configuration is thus unchanged but its resilience increases.

It is not so straightforward to automatically remove nodes from the voting configuration after they have left the cluster. Different strategies have different benefits and drawbacks, so the right choice depends on how the cluster will be used. You can control whether the voting configuration automatically shrinks by using the [`cluster.auto_shrink_voting_configuration` setting](elasticsearch://reference/elasticsearch/configuration-reference/discovery-cluster-formation-settings.md).

::::{note}
If `cluster.auto_shrink_voting_configuration` is set to `true` (which is the default and recommended value) and there are at least three master-eligible nodes in the cluster, {{es}} remains capable of processing cluster state updates as long as all but one of its master-eligible nodes are healthy.
::::

There are situations in which {{es}} might tolerate the loss of multiple nodes, but this is not guaranteed under all sequences of failures. If the `cluster.auto_shrink_voting_configuration` setting is `false`, you must remove departed nodes from the voting configuration manually. Use the [voting exclusions API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-post-voting-config-exclusions) to achieve the desired level of resilience.

No matter how it is configured, {{es}} will not suffer from a "split-brain" inconsistency. The `cluster.auto_shrink_voting_configuration` setting affects only its availability in the event of the failure of some of its nodes and the administrative tasks that must be performed as nodes join and leave the cluster.

## Even numbers of master-eligible nodes [_even_numbers_of_master_eligible_nodes]

There should normally be an odd number of master-eligible nodes in a cluster. If there is an even number, {{es}} leaves one of them out of the voting configuration to ensure that it has an odd size. This omission does not decrease the failure-tolerance of the cluster. In fact, improves it slightly: if the cluster suffers from a network partition that divides it into two equally-sized halves then one of the halves will contain a majority of the voting configuration and will be able to keep operating. If all of the votes from master-eligible nodes were counted, neither side would contain a strict majority of the nodes and so the cluster would not be able to make any progress.

For instance if there are four master-eligible nodes in the cluster and the voting configuration contained all of them, any quorum-based decision would require votes from at least three of them. This situation means that the cluster can tolerate the loss of only a single master-eligible node. If this cluster were split into two equal halves, neither half would contain three master-eligible nodes and the cluster would not be able to make any progress. If the voting configuration contains only three of the four master-eligible nodes, however, the cluster is still only fully tolerant to the loss of one node, but quorum-based decisions require votes from two of the three voting nodes. In the event of an even split, one half will contain two of the three voting nodes so that half will remain available.

## Setting the initial voting configuration [_setting_the_initial_voting_configuration]

When a brand-new cluster starts up for the first time, it must elect its first master node. To do this election, it needs to know the set of master-eligible nodes whose votes should count. This initial voting configuration is known as the *bootstrap configuration* and is set in the [cluster bootstrapping process](modules-discovery-bootstrap-cluster.md).

It is important that the bootstrap configuration identifies exactly which nodes should vote in the first election. It is not sufficient to configure each node with an expectation of how many nodes there should be in the cluster. It is also important to note that the bootstrap configuration must come from outside the cluster: there is no safe way for the cluster to determine the bootstrap configuration correctly on its own.

If the bootstrap configuration is not set correctly, when you start a brand-new cluster there is a risk that you will accidentally form two separate clusters instead of one. This situation can lead to data loss: you might start using both clusters before you notice that anything has gone wrong and it is impossible to merge them together later.

::::{note}
To illustrate the problem with configuring each node to expect a certain cluster size, imagine starting up a three-node cluster in which each node knows that it is going to be part of a three-node cluster. A majority of three nodes is two, so normally the first two nodes to discover each other form a cluster and the third node joins them a short time later. However, imagine that four nodes were erroneously started instead of three. In this case, there are enough nodes to form two separate clusters. Of course if each node is started manually then it’s unlikely that too many nodes are started. If you’re using an automated orchestrator, however, it’s certainly possible to get into this situation—particularly if the orchestrator is not resilient to failures such as network partitions.
::::

The initial quorum is only required the very first time a whole cluster starts up. New nodes joining an established cluster can safely obtain all the information they need from the elected master. Nodes that have previously been part of a cluster will have stored to disk all the information that is required when they restart.
