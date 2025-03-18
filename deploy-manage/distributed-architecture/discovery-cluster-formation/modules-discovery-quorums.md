---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-discovery-quorums.html
applies_to:
  stack:
---

# Quorum-based decision making [modules-discovery-quorums]

Electing a master node and changing the cluster state are the two fundamental tasks that master-eligible nodes must work together to perform. It is important that these activities work robustly even if some nodes have failed. Elasticsearch achieves this robustness by considering each action to have succeeded on receipt of responses from a *quorum*, which is a subset of the master-eligible nodes in the cluster. The advantage of requiring only a subset of the nodes to respond is that it means some of the nodes can fail without preventing the cluster from making progress. The quorums are carefully chosen so the cluster does not have a "split brain" scenario where it’s partitioned into two pieces such that each piece may make decisions that are inconsistent with those of the other piece.

Elasticsearch allows you to add and remove master-eligible nodes to a running cluster. In many cases you can do this simply by starting or stopping the nodes as required. See [*Add and remove nodes in your cluster*](../../maintenance/add-and-remove-elasticsearch-nodes.md) for more information.

As nodes are added or removed Elasticsearch maintains an optimal level of fault tolerance by updating the cluster’s [voting configuration](modules-discovery-voting.md), which is the set of master-eligible nodes whose responses are counted when making decisions such as electing a new master or committing a new cluster state. A decision is made only after more than half of the nodes in the voting configuration have responded. Usually the voting configuration is the same as the set of all the master-eligible nodes that are currently in the cluster. However, there are some situations in which they may be different.

::::{important}
To be sure that the cluster remains available you **must not stop half or more of the nodes in the voting configuration at the same time**. As long as more than half of the voting nodes are available the cluster can still work normally. This means that if there are three or four master-eligible nodes, the cluster can tolerate one of them being unavailable. If there are two or fewer master-eligible nodes, they must all remain available.

If you stop half or more of the nodes in the voting configuration at the same time then the cluster will be unavailable until you bring enough nodes back online to form a quorum again. While the cluster is unavailable, any remaining nodes will report in their logs that they cannot discover or elect a master node. See [*Troubleshooting discovery*](../../../troubleshoot/elasticsearch/discovery-troubleshooting.md) for more information.

::::

After a master-eligible node has joined or left the cluster the elected master may issue a cluster-state update that adjusts the voting configuration to match, and this can take a short time to complete. It is important to wait for this adjustment to complete before removing more nodes from the cluster. See [Removing master-eligible nodes](../../maintenance/add-and-remove-elasticsearch-nodes.md#modules-discovery-removing-nodes) for more information.

## Master elections [_master_elections]

Elasticsearch uses an election process to agree on an elected master node, both at startup and if the existing elected master fails. Any master-eligible node can start an election, and normally the first election that takes place will succeed. Elections only usually fail when two nodes both happen to start their elections at about the same time, so elections are scheduled randomly on each node to reduce the probability of this happening. Nodes will retry elections until a master is elected, backing off on failure, so that eventually an election will succeed (with arbitrarily high probability). The scheduling of master elections are controlled by the [master election settings](elasticsearch://reference/elasticsearch/configuration-reference/discovery-cluster-formation-settings.md#master-election-settings).

## Cluster maintenance, rolling restarts and migrations [_cluster_maintenance_rolling_restarts_and_migrations]

Many cluster maintenance tasks involve temporarily shutting down one or more nodes and then starting them back up again. By default {{es}} can remain available if one of its master-eligible nodes is taken offline, such as during a rolling upgrade. Furthermore, if multiple nodes are stopped and then started again then it will automatically recover, such as during a full cluster restart. There is no need to take any further action with the APIs described here in these cases, because the set of master nodes is not changing permanently.
