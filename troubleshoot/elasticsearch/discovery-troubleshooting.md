---
navigation_title: Discovery
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/discovery-troubleshooting.html
---

# Troubleshoot discovery [discovery-troubleshooting]

In most cases, the discovery and election process completes quickly, and the master node remains elected for a long period of time.

If your cluster doesn’t have a stable master, many of its features won’t work correctly and {{es}} will report errors to clients and in its logs. You must fix the master node’s instability before addressing these other issues. It will not be possible to solve any other issues while there is no elected master node or the elected master node is unstable.

If your cluster has a stable master but some nodes can’t discover or join it, these nodes will report errors to clients and in their logs. You must address the obstacles preventing these nodes from joining the cluster before addressing other issues. It will not be possible to solve any other issues reported by these nodes while they are unable to join the cluster.

If the cluster has no elected master node for more than a few seconds, the master is unstable, or some nodes are unable to discover or join a stable master, then {{es}} will record information in its logs explaining why. If the problems persist for more than a few minutes, {{es}} will record additional information in its logs. To properly troubleshoot discovery and election problems, collect and analyse logs covering at least five minutes from all nodes.

The following sections describe some common discovery and election problems.


## No master is elected [discovery-no-master] 

When a node wins the master election, it logs a message containing `elected-as-master` and all nodes log a message containing `master node changed` identifying the new elected master node.

If there is no elected master node and no node can win an election, all nodes will repeatedly log messages about the problem using a logger called `org.elasticsearch.cluster.coordination.ClusterFormationFailureHelper`. By default, this happens every 10 seconds.

Master elections only involve master-eligible nodes, so focus your attention on the master-eligible nodes in this situation. These nodes' logs will indicate the requirements for a master election, such as the discovery of a certain set of nodes. The [Health](https://www.elastic.co/guide/en/elasticsearch/reference/current/health-api.html) API on these nodes will also provide useful information about the situation.

If the logs or the health report indicate that {{es}} can’t discover enough nodes to form a quorum, you must address the reasons preventing {{es}} from discovering the missing nodes. The missing nodes are needed to reconstruct the cluster metadata. Without the cluster metadata, the data in your cluster is meaningless. The cluster metadata is stored on a subset of the master-eligible nodes in the cluster. If a quorum can’t be discovered, the missing nodes were the ones holding the cluster metadata.

Ensure there are enough nodes running to form a quorum and that every node can communicate with every other node over the network. {{es}} will report additional details about network connectivity if the election problems persist for more than a few minutes. If you can’t start enough nodes to form a quorum, start a new cluster and restore data from a recent snapshot. Refer to [Quorum-based decision making](../../deploy-manage/distributed-architecture/discovery-cluster-formation/modules-discovery-quorums.md) for more information.

If the logs or the health report indicate that {{es}} *has* discovered a possible quorum of nodes, the typical reason that the cluster can’t elect a master is that one of the other nodes can’t discover a quorum. Inspect the logs on the other master-eligible nodes and ensure that they have all discovered enough nodes to form a quorum.

If the logs suggest that discovery or master elections are failing due to timeouts or network-related issues then narrow down the problem as follows.

* GC pauses are recorded in the GC logs that {{es}} emits by default, and also usually by the `JvmMonitorService` in the main node logs. Use these logs to confirm whether or not the node is experiencing high heap usage with long GC pauses. If so, [the troubleshooting guide for high heap usage](high-jvm-memory-pressure.md) has some suggestions for further investigation but typically you will need to capture a heap dump and the [garbage collector logs](https://www.elastic.co/guide/en/elasticsearch/reference/current/advanced-configuration.html#gc-logging) during a time of high heap usage to fully understand the problem.
* VM pauses also affect other processes on the same host. A VM pause also typically causes a discontinuity in the system clock, which {{es}} will report in its logs. If you see evidence of other processes pausing at the same time, or unexpected clock discontinuities, investigate the infrastructure on which you are running {{es}}.
* Packet captures will reveal system-level and network-level faults, especially if you capture the network traffic simultaneously at all relevant nodes and analyse it alongside the {{es}} logs from those nodes. You should be able to observe any retransmissions, packet loss, or other delays on the connections between the nodes.
* Long waits for particular threads to be available can be identified by taking stack dumps of the main {{es}} process (for example, using `jstack`) or a profiling trace (for example, using Java Flight Recorder) in the few seconds leading up to the relevant log message.

    The [Nodes hot threads](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-nodes-hot-threads.html) API sometimes yields useful information, but bear in mind that this API also requires a number of `transport_worker` and `generic` threads across all the nodes in the cluster. The API may be affected by the very problem you’re trying to diagnose. `jstack` is much more reliable since it doesn’t require any JVM threads.

    The threads involved in discovery and cluster membership are mainly `transport_worker` and `cluster_coordination` threads, for which there should never be a long wait. There may also be evidence of long waits for threads in the {{es}} logs, particularly looking at warning logs from `org.elasticsearch.transport.InboundHandler`. See [Networking threading model](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-network.html#modules-network-threading-model) for more information.



## Master is elected but unstable [discovery-master-unstable] 

When a node wins the master election, it logs a message containing `elected-as-master`. If this happens repeatedly, the elected master node is unstable. In this situation, focus on the logs from the master-eligible nodes to understand why the election winner stops being the master and triggers another election. If the logs suggest that the master is unstable due to timeouts or network-related issues then narrow down the problem as follows.

* GC pauses are recorded in the GC logs that {{es}} emits by default, and also usually by the `JvmMonitorService` in the main node logs. Use these logs to confirm whether or not the node is experiencing high heap usage with long GC pauses. If so, [the troubleshooting guide for high heap usage](high-jvm-memory-pressure.md) has some suggestions for further investigation but typically you will need to capture a heap dump and the [garbage collector logs](https://www.elastic.co/guide/en/elasticsearch/reference/current/advanced-configuration.html#gc-logging) during a time of high heap usage to fully understand the problem.
* VM pauses also affect other processes on the same host. A VM pause also typically causes a discontinuity in the system clock, which {{es}} will report in its logs. If you see evidence of other processes pausing at the same time, or unexpected clock discontinuities, investigate the infrastructure on which you are running {{es}}.
* Packet captures will reveal system-level and network-level faults, especially if you capture the network traffic simultaneously at all relevant nodes and analyse it alongside the {{es}} logs from those nodes. You should be able to observe any retransmissions, packet loss, or other delays on the connections between the nodes.
* Long waits for particular threads to be available can be identified by taking stack dumps of the main {{es}} process (for example, using `jstack`) or a profiling trace (for example, using Java Flight Recorder) in the few seconds leading up to the relevant log message.

    The [Nodes hot threads](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-nodes-hot-threads.html) API sometimes yields useful information, but bear in mind that this API also requires a number of `transport_worker` and `generic` threads across all the nodes in the cluster. The API may be affected by the very problem you’re trying to diagnose. `jstack` is much more reliable since it doesn’t require any JVM threads.

    The threads involved in discovery and cluster membership are mainly `transport_worker` and `cluster_coordination` threads, for which there should never be a long wait. There may also be evidence of long waits for threads in the {{es}} logs, particularly looking at warning logs from `org.elasticsearch.transport.InboundHandler`. See [Networking threading model](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-network.html#modules-network-threading-model) for more information.



## Node cannot discover or join stable master [discovery-cannot-join-master] 

If there is a stable elected master but a node can’t discover or join its cluster, it will repeatedly log messages about the problem using the `ClusterFormationFailureHelper` logger. The [Health](https://www.elastic.co/guide/en/elasticsearch/reference/current/health-api.html) API on the affected node will also provide useful information about the situation. Other log messages on the affected node and the elected master may provide additional information about the problem. If the logs suggest that the node cannot discover or join the cluster due to timeouts or network-related issues then narrow down the problem as follows.

* GC pauses are recorded in the GC logs that {{es}} emits by default, and also usually by the `JvmMonitorService` in the main node logs. Use these logs to confirm whether or not the node is experiencing high heap usage with long GC pauses. If so, [the troubleshooting guide for high heap usage](high-jvm-memory-pressure.md) has some suggestions for further investigation but typically you will need to capture a heap dump and the [garbage collector logs](https://www.elastic.co/guide/en/elasticsearch/reference/current/advanced-configuration.html#gc-logging) during a time of high heap usage to fully understand the problem.
* VM pauses also affect other processes on the same host. A VM pause also typically causes a discontinuity in the system clock, which {{es}} will report in its logs. If you see evidence of other processes pausing at the same time, or unexpected clock discontinuities, investigate the infrastructure on which you are running {{es}}.
* Packet captures will reveal system-level and network-level faults, especially if you capture the network traffic simultaneously at all relevant nodes and analyse it alongside the {{es}} logs from those nodes. You should be able to observe any retransmissions, packet loss, or other delays on the connections between the nodes.
* Long waits for particular threads to be available can be identified by taking stack dumps of the main {{es}} process (for example, using `jstack`) or a profiling trace (for example, using Java Flight Recorder) in the few seconds leading up to the relevant log message.

    The [Nodes hot threads](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-nodes-hot-threads.html) API sometimes yields useful information, but bear in mind that this API also requires a number of `transport_worker` and `generic` threads across all the nodes in the cluster. The API may be affected by the very problem you’re trying to diagnose. `jstack` is much more reliable since it doesn’t require any JVM threads.

    The threads involved in discovery and cluster membership are mainly `transport_worker` and `cluster_coordination` threads, for which there should never be a long wait. There may also be evidence of long waits for threads in the {{es}} logs, particularly looking at warning logs from `org.elasticsearch.transport.InboundHandler`. See [Networking threading model](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-network.html#modules-network-threading-model) for more information.



## Node joins cluster and leaves again [discovery-node-leaves] 

If a node joins the cluster but {{es}} determines it to be faulty then it will be removed from the cluster again. See [Troubleshooting an unstable cluster](../../deploy-manage/distributed-architecture/discovery-cluster-formation/cluster-fault-detection.md#cluster-fault-detection-troubleshooting) for more information.

