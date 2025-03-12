---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-discovery.html
applies_to:
  stack:
---

% Discovery and cluster formation content (7 pages): add introductory note to specify that the endpoints/settings are possibly for self-managed only, and review the content.

# Discovery and cluster formation [modules-discovery]

The discovery and cluster formation processes are responsible for discovering nodes, electing a master, forming a cluster, and publishing the cluster state each time it changes.

The following processes and settings are part of discovery and cluster formation:

[Discovery](discovery-cluster-formation/discovery-hosts-providers.md)
:   Discovery is the process where nodes find each other when the master is unknown, such as when a node has just started up or when the previous master has failed.

[Quorum-based decision making](discovery-cluster-formation/modules-discovery-quorums.md)
:   How {{es}} uses a quorum-based voting mechanism to make decisions even if some nodes are unavailable.

[Voting configurations](discovery-cluster-formation/modules-discovery-voting.md)
:   How {{es}} automatically updates voting configurations as nodes leave and join a cluster.

[Bootstrapping a cluster](discovery-cluster-formation/modules-discovery-bootstrap-cluster.md)
:   Bootstrapping a cluster is required when an {{es}} cluster starts up for the very first time. In [development mode](../deploy/self-managed/bootstrap-checks.md#dev-vs-prod-mode), with no discovery settings configured, this is automatically performed by the nodes themselves. As this auto-bootstrapping is [inherently unsafe](discovery-cluster-formation/modules-discovery-quorums.md), running a node in [production mode](../deploy/self-managed/bootstrap-checks.md#dev-vs-prod-mode) requires bootstrapping to be [explicitly configured](discovery-cluster-formation/modules-discovery-bootstrap-cluster.md).

[Adding and removing master-eligible nodes](../maintenance/add-and-remove-elasticsearch-nodes.md)
:   It is recommended to have a small and fixed number of master-eligible nodes in a cluster, and to scale the cluster up and down by adding and removing master-ineligible nodes only. However there are situations in which it may be desirable to add or remove some master-eligible nodes to or from a cluster. This section describes the process for adding or removing master-eligible nodes, including the extra steps that need to be performed when removing more than half of the master-eligible nodes at the same time.

[Publishing the cluster state](discovery-cluster-formation/cluster-state-overview.md#cluster-state-publishing)
:   Cluster state publishing is the process by which the elected master node updates the cluster state on all the other nodes in the cluster.

[Cluster fault detection](discovery-cluster-formation/cluster-fault-detection.md)
:   {{es}} performs health checks to detect and remove faulty nodes.

[Settings](elasticsearch://reference/elasticsearch/configuration-reference/discovery-cluster-formation-settings.md)
:   There are settings that enable users to influence the discovery, cluster formation, master election and fault detection processes.

[Quorum-based decision making](discovery-cluster-formation/modules-discovery-quorums.md): How {{es}} uses a quorum-based voting mechanism to make decisions even if some nodes are unavailable.

[Voting configurations](discovery-cluster-formation/modules-discovery-voting.md): How {{es}} automatically updates voting configurations as nodes leave and join a cluster.

[Bootstrapping a cluster](discovery-cluster-formation/modules-discovery-bootstrap-cluster.md): Bootstrapping a cluster is required when an {{es}} cluster starts up for the very first time. In [development mode](../deploy/self-managed/bootstrap-checks.md#dev-vs-prod-mode), with no discovery settings configured, this is automatically performed by the nodes themselves. As this auto-bootstrapping is [inherently unsafe](discovery-cluster-formation/modules-discovery-quorums.md), running a node in [production mode](../deploy/self-managed/bootstrap-checks.md#dev-vs-prod-mode) requires bootstrapping to be [explicitly configured](discovery-cluster-formation/modules-discovery-bootstrap-cluster.md).

[Adding and removing master-eligible nodes](../maintenance/add-and-remove-elasticsearch-nodes.md): It is recommended to have a small and fixed number of master-eligible nodes in a cluster, and to scale the cluster up and down by adding and removing master-ineligible nodes only. However there are situations in which it may be desirable to add or remove some master-eligible nodes to or from a cluster. This section describes the process for adding or removing master-eligible nodes, including the extra steps that need to be performed when removing more than half of the master-eligible nodes at the same time.

[Publishing the cluster state](discovery-cluster-formation/cluster-state-overview.md#cluster-state-publishing): Cluster state publishing is the process by which the elected master node updates the cluster state on all the other nodes in the cluster.

[Cluster fault detection](discovery-cluster-formation/cluster-fault-detection.md): {{es}} performs health checks to detect and remove faulty nodes.

[Settings](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/discovery-cluster-formation-settings.md): There are settings that enable users to influence the discovery, cluster formation, master election and fault detection processes.