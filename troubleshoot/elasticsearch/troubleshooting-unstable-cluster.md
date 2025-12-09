---
navigation_title: Unstable clusters
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/troubleshooting-unstable-cluster.html
applies_to:
  stack:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Troubleshoot an unstable cluster [troubleshooting-unstable-cluster]

Normally, a node will only leave a cluster if deliberately shut down. If a node leaves the cluster unexpectedly, it’s important to address the cause. A cluster in which nodes leave unexpectedly is unstable and can create several issues. For instance:

* The cluster health may be yellow or red.
* Some shards will be initializing and other shards may be failing.
* Search, indexing, and monitoring operations may fail and report exceptions in logs.
* The `.security` index may be unavailable, blocking access to the cluster.
* The master may appear busy due to frequent cluster state updates.

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::

To troubleshoot a cluster in this state, first ensure the cluster has a [stable master](discovery-troubleshooting.md). Next, focus on the nodes unexpectedly leaving the cluster ahead of all other issues. It will not be possible to solve other issues until the cluster has a stable master node and stable node membership.

Diagnostics and statistics are usually not useful in an unstable cluster. These tools only offer a view of the state of the cluster at a single point in time. Instead, look at the cluster logs to see the pattern of behavior over time. Focus particularly on logs from the elected master. When a node leaves the cluster, logs for the elected master include a message like this (with line breaks added to make it easier to read):

```text
[2022-03-21T11:02:35,513][INFO ][o.e.c.c.NodeLeftExecutor] [instance-0000000000]
    node-left: [{instance-0000000004}{bfcMDTiDRkietFb9v_di7w}{aNlyORLASam1ammv2DzYXA}{172.27.47.21}{172.27.47.21:19054}{m}]
    with reason [disconnected]
```

This message says that the `NodeLeftExecutor` on the elected master (`instance-0000000000`) processed a `node-left` task, identifying the node that was removed and the reason for its removal. When the node joins the cluster again, logs for the elected master will include a message like this (with line breaks added to make it easier to read):

```text
[2022-03-21T11:02:59,892][INFO ][o.e.c.c.NodeJoinExecutor] [instance-0000000000]
    node-join: [{instance-0000000004}{bfcMDTiDRkietFb9v_di7w}{UNw_RuazQCSBskWZV8ID_w}{172.27.47.21}{172.27.47.21:19054}{m}]
    with reason [joining after restart, removed [24s] ago with reason [disconnected]]
```

This message says that the `NodeJoinExecutor` on the elected master (`instance-0000000000`) processed a `node-join` task, identifying the node that was added to the cluster and the reason for the task.

Other nodes may log similar messages, but report fewer details:

```text
[2020-01-29T11:02:36,985][INFO ][o.e.c.s.ClusterApplierService]
    [instance-0000000001] removed {
        {instance-0000000004}{bfcMDTiDRkietFb9v_di7w}{aNlyORLASam1ammv2DzYXA}{172.27.47.21}{172.27.47.21:19054}{m}
        {tiebreaker-0000000003}{UNw_RuazQCSBskWZV8ID_w}{bltyVOQ-RNu20OQfTHSLtA}{172.27.161.154}{172.27.161.154:19251}{mv}
    }, term: 14, version: 1653415, reason: Publication{term=14, version=1653415}
```

These messages are not especially useful for troubleshooting, so focus on the ones from the `NodeLeftExecutor` and `NodeJoinExecutor` which are only emitted on the elected master and which contain more details. If you don’t see the messages from the `NodeLeftExecutor` and `NodeJoinExecutor`, check that:

* You’re looking at the logs for the elected master node.
* The logs cover the correct time period.
* Logging is enabled at `INFO` level.

Nodes will also log a message containing `master node changed` whenever they start or stop following the elected master. You can use these messages to determine each node’s view of the state of the master over time.

If a node restarts, it will leave the cluster and then join the cluster again. When it rejoins, the `NodeJoinExecutor` will log that it processed a `node-join` task indicating that the node is `joining after restart`. If a node is unexpectedly restarting, look at the node’s logs to see why it is shutting down.

The [Health](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-health-report) API on the affected node will also provide some useful information about the situation.

If the node did not restart then you should look at the reason for its departure more closely. Each reason has different troubleshooting steps, described below. There are three possible reasons:

* `disconnected`: The connection from the master node to the removed node was closed.
* `lagging`: The master published a cluster state update, but the removed node did not apply it within the permitted timeout. By default, this timeout is 2 minutes. Refer to [Discovery and cluster formation settings](elasticsearch://reference/elasticsearch/configuration-reference/discovery-cluster-formation-settings.md) for information about the settings which control this mechanism.
* `followers check retry count exceeded`: The master sent a number of consecutive health checks to the removed node. These checks were rejected or timed out. By default, each health check times out after 10 seconds and {{es}} removes the node removed after three consecutively failed health checks. Refer to [Discovery and cluster formation settings](elasticsearch://reference/elasticsearch/configuration-reference/discovery-cluster-formation-settings.md) for information about the settings which control this mechanism.


## Diagnosing `disconnected` nodes [troubleshooting-unstable-cluster-disconnected]

Nodes typically leave the cluster with reason `disconnected` when they shut down, but if they rejoin the cluster without restarting then there is some other problem.

{{es}} is designed to run on a fairly reliable network. It opens a number of TCP connections between nodes and expects these connections to remain open [forever](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#long-lived-connections). If a connection is closed then {{es}} will try and reconnect, so the occasional blip may fail some in-flight operations but should otherwise have limited impact on the cluster. In contrast, repeatedly-dropped connections will severely affect its operation.

The connections from the elected master node to every other node in the cluster are particularly important. The elected master never spontaneously closes its outbound connections to other nodes. Similarly, once an inbound connection is fully established, a node never spontaneously closes it unless the node is shutting down.

To determine whether the node which left the cluster with the `disconnected` reason did so because it was shutting down, look for the message from the `NodeJoinExecutor` logged when the node rejoined the cluster again as described in the previous section. This message indicates whether the node restarted or not. If the node did not restart, the disconnect is unexpected and indicates that something other than {{es}} caused the connection to close. Refer to [Diagnosing network disconnections](#troubleshooting-unstable-cluster-network) for further information about troubleshooting network disconnections.

## Diagnosing `lagging` nodes [troubleshooting-unstable-cluster-lagging]

{{es}} needs every node to process cluster state updates reasonably quickly. If a node takes too long to process a cluster state update, it can be harmful to the cluster. The master will remove these nodes with the `lagging` reason. Refer to [Discovery and cluster formation settings](elasticsearch://reference/elasticsearch/configuration-reference/discovery-cluster-formation-settings.md) for information about the settings which control this mechanism.

Lagging is typically caused by performance issues on the removed node. However, a node may also lag due to severe network delays. To rule out network delays, ensure that `net.ipv4.tcp_retries2` is [configured properly](../../deploy-manage/deploy/self-managed/system-config-tcpretries.md). Log messages that contain `warn threshold` may provide more information about the root cause.

If you’re an advanced user, you can get more detailed information about what the node was doing when it was removed by configuring the following logger:

```yaml
logger.org.elasticsearch.cluster.coordination.LagDetector: DEBUG
```

When this logger is enabled, {{es}} will attempt to run the [Nodes hot threads](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-hot-threads) API on the faulty node and report the results in the logs on the elected master. The results are compressed, encoded, and split into chunks to avoid truncation:

```text
[DEBUG][o.e.c.c.LagDetector      ] [master] hot threads from node [{node}{g3cCUaMDQJmQ2ZLtjr-3dg}{10.0.0.1:9300}] lagging at version [183619] despite commit of cluster state version [183620] [part 1]: H4sIAAAAAAAA/x...
[DEBUG][o.e.c.c.LagDetector      ] [master] hot threads from node [{node}{g3cCUaMDQJmQ2ZLtjr-3dg}{10.0.0.1:9300}] lagging at version [183619] despite commit of cluster state version [183620] [part 2]: p7x3w1hmOQVtuV...
[DEBUG][o.e.c.c.LagDetector      ] [master] hot threads from node [{node}{g3cCUaMDQJmQ2ZLtjr-3dg}{10.0.0.1:9300}] lagging at version [183619] despite commit of cluster state version [183620] [part 3]: v7uTboMGDbyOy+...
[DEBUG][o.e.c.c.LagDetector      ] [master] hot threads from node [{node}{g3cCUaMDQJmQ2ZLtjr-3dg}{10.0.0.1:9300}] lagging at version [183619] despite commit of cluster state version [183620] [part 4]: 4tse0RnPnLeDNN...
[DEBUG][o.e.c.c.LagDetector      ] [master] hot threads from node [{node}{g3cCUaMDQJmQ2ZLtjr-3dg}{10.0.0.1:9300}] lagging at version [183619] despite commit of cluster state version [183620] (gzip compressed, base64-encoded, and split into 4 parts on preceding log lines)
```

To reconstruct the output, base64-decode the data and decompress it using `gzip`. For instance, on Unix-like systems:

```sh
cat lagdetector.log | sed -e 's/.*://' | base64 --decode | gzip --decompress
```


## Diagnosing `follower check retry count exceeded` nodes [troubleshooting-unstable-cluster-follower-check]

Nodes sometimes leave the cluster with reason `follower check retry count exceeded` when they shut down, but if they rejoin the cluster without restarting then there is some other problem.

{{es}} needs every node to respond to network messages successfully and reasonably quickly. If a node rejects requests or does not respond at all then it can be harmful to the cluster. If enough consecutive checks fail then the master will remove the node with reason `follower check retry count exceeded` and will indicate in the `node-left` message how many of the consecutive unsuccessful checks failed and how many of them timed out. Refer to [Discovery and cluster formation settings](elasticsearch://reference/elasticsearch/configuration-reference/discovery-cluster-formation-settings.md) for information about the settings which control this mechanism.

Timeouts and failures may be due to network delays or performance problems on the affected nodes. Ensure that `net.ipv4.tcp_retries2` is [configured properly](../../deploy-manage/deploy/self-managed/system-config-tcpretries.md) to eliminate network delays as a possible cause for this kind of instability. Log messages containing `warn threshold` may give further clues about the cause of the instability.

If the last check failed with an exception then the exception is reported, and typically indicates the problem that needs to be addressed. If any of the checks timed out then narrow down the problem as follows.

* GC pauses are recorded in the GC logs that {{es}} emits by default, and also usually by the `JvmMonitorService` in the main node logs. Use these logs to confirm whether or not the node is experiencing high heap usage with long GC pauses. If so, [the troubleshooting guide for high heap usage](high-jvm-memory-pressure.md) has some suggestions for further investigation but typically you will need to capture a heap dump and the [garbage collector logs](elasticsearch://reference/elasticsearch/jvm-settings.md#gc-logging) during a time of high heap usage to fully understand the problem.
* VM pauses also affect other processes on the same host. A VM pause also typically causes a discontinuity in the system clock, which {{es}} will report in its logs. If you see evidence of other processes pausing at the same time, or unexpected clock discontinuities, investigate the infrastructure on which you are running {{es}}.
* Packet captures will reveal system-level and network-level faults, especially if you capture the network traffic simultaneously at the elected master and the faulty node and analyse it alongside the {{es}} logs from those nodes. The connection used for follower checks is not used for any other traffic so it can be easily identified from the flow pattern alone, even if TLS is in use: almost exactly every second there will be a few hundred bytes sent each way, first the request by the master and then the response by the follower. You should be able to observe any retransmissions, packet loss, or other delays on such a connection.
* Long waits for particular threads to be available can be identified by taking stack dumps of the main {{es}} process (for example, using `jstack`) or a profiling trace (for example, using Java Flight Recorder) in the few seconds leading up to the relevant log message.

    The [Nodes hot threads](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-hot-threads) API sometimes yields useful information, but bear in mind that this API also requires a number of `transport_worker` and `generic` threads across all the nodes in the cluster. The API may be affected by the very problem you’re trying to diagnose. `jstack` is much more reliable since it doesn’t require any JVM threads.

    The threads involved in discovery and cluster membership are mainly `transport_worker` and `cluster_coordination` threads, for which there should never be a long wait. There may also be evidence of long waits for threads in the {{es}} logs, particularly looking at warning logs from `org.elasticsearch.transport.InboundHandler`. See [Networking threading model](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#modules-network-threading-model) for more information.


By default the follower checks will time out after 30s, so if node departures are unpredictable then capture stack dumps every 15s to be sure that at least one stack dump was taken at the right time.


## Diagnosing `ShardLockObtainFailedException` failures [troubleshooting-unstable-cluster-shardlockobtainfailedexception]

If a node leaves and rejoins the cluster then {{es}} will usually shut down and re-initialize its shards. If the shards do not shut down quickly enough then {{es}} may fail to re-initialize them due to a `ShardLockObtainFailedException`.

To gather more information about the reason for shards shutting down slowly, configure the following logger:

```yaml
logger.org.elasticsearch.env.NodeEnvironment: DEBUG
```

When this logger is enabled, {{es}} will attempt to run the [Nodes hot threads](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-hot-threads) API whenever it encounters a `ShardLockObtainFailedException`. The results are compressed, encoded, and split into chunks to avoid truncation:

```text
[DEBUG][o.e.e.NodeEnvironment    ] [master] hot threads while failing to obtain shard lock for [index][0] [part 1]: H4sIAAAAAAAA/x...
[DEBUG][o.e.e.NodeEnvironment    ] [master] hot threads while failing to obtain shard lock for [index][0] [part 2]: p7x3w1hmOQVtuV...
[DEBUG][o.e.e.NodeEnvironment    ] [master] hot threads while failing to obtain shard lock for [index][0] [part 3]: v7uTboMGDbyOy+...
[DEBUG][o.e.e.NodeEnvironment    ] [master] hot threads while failing to obtain shard lock for [index][0] [part 4]: 4tse0RnPnLeDNN...
[DEBUG][o.e.e.NodeEnvironment    ] [master] hot threads while failing to obtain shard lock for [index][0] (gzip compressed, base64-encoded, and split into 4 parts on preceding log lines)
```

To reconstruct the output, base64-decode the data and decompress it using `gzip`. For instance, on Unix-like systems:

```sh
cat shardlock.log | sed -e 's/.*://' | base64 --decode | gzip --decompress
```


## Diagnosing network disconnections [troubleshooting-unstable-cluster-network]

{{es}} is designed to run on a fairly reliable network. It opens a number of TCP connections between nodes and expects these transport connections to remain open [forever](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#long-lived-connections). If a transport connection is closed then {{es}} tries to reopen the connection, failing any in-flight operations that were using the connection at the time. Occasional closures of transport connections might be acceptable since they have a small impact on the cluster, but repeatedly-dropped transport connections severely affect its operations.

{{es}} nodes only actively close an outbound transport connection to another node if the other node leaves the cluster. Refer to [Troubleshooting an unstable cluster](../../deploy-manage/distributed-architecture/discovery-cluster-formation/cluster-fault-detection.md#cluster-fault-detection-troubleshooting) for further information about identifying and troubleshooting this situation. If an outbound transport connection closes for some other reason, {{es}} logs messages such as the following:

```text
[INFO ][o.e.t.ClusterConnectionManager] [node-1] transport connection to [{node-2}{g3cCUaMDQJmQ2ZLtjr-3dg}{10.0.0.1:9300}] closed by remote
[WARN ][o.e.c.NodeConnectionsService  ] [node-1] reopened transport connection to node [{node-2}{g3cCUaMDQJmQ2ZLtjr-3dg}{10.0.0.1:9300}] which disconnected exceptionally [500ms] ago but did not restart, so the disconnection is unexpected
```

Similarly, once an inbound transport connection is fully established, a node never spontaneously closes it unless the node is shutting down.

Therefore if a node reports that a transport connection to another node closed unexpectedly, something other than {{es}} likely caused the connection to close. A common cause is a misconfigured firewall with an improper timeout or another policy that’s [incompatible with {{es}}](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#long-lived-connections). It could also be caused by general connectivity issues, such as packet loss due to faulty hardware or severe network congestion.

On Linux, the exception message `Connection timed out` indicates that some data or a sequence of consecutive keepalives went unacknowledged after many retransmission attempts. These acknowledgments and retransmissions are the responsibility of the operating systems on the hosts running the {{es}} nodes and cannot be influenced by {{es}} itself. Therefore a `Connection timed out` exception always indicates a problem in the environment in which {{es}} is running. Other exceptions may also arise from general connectivity issues.

If you’re an advanced user, configure the following loggers to get more detailed information about network exceptions:

```yaml
logger.org.elasticsearch.transport.TcpTransport: DEBUG
logger.org.elasticsearch.xpack.core.security.transport.netty4.SecurityNetty4Transport: DEBUG
```

If these logs do not show enough information to diagnose the problem, obtain a packet capture simultaneously from the nodes at both ends of an unstable connection and analyse it alongside the {{es}} logs from those nodes to determine if traffic between the nodes is being disrupted by another device on the network.
