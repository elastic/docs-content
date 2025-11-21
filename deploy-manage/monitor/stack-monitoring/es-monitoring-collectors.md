---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/es-monitoring-collectors.html
applies_to:
  deployment:
    self: deprecated 7.16.0
products:
  - id: elasticsearch
---


# Collectors [es-monitoring-collectors]

:::{include} _snippets/legacy-warning.md
:::

Collectors, as their name implies, collect things. Each collector runs once for each collection interval to obtain data from the public APIs in {{es}} and X-Pack that it chooses to monitor. When the data collection is finished, the data is handed in bulk to the [exporters](es-monitoring-exporters.md) to be sent to the monitoring clusters. Regardless of the number of exporters, each collector only runs once per collection interval.

There is only one collector per data type gathered. In other words, for any monitoring document that is created, it comes from a single collector rather than being merged from multiple collectors. The {{es}} {{monitor-features}} currently have a few collectors because the goal is to minimize overlap between them for optimal performance.

Each collector can create zero or more monitoring documents. For example, the `index_stats` collector collects all index statistics at the same time to avoid many unnecessary calls.

| Collector | Data Types | Description |
| --- | --- | --- |
| Cluster Stats | `cluster_stats` | Gathers details about the cluster state, including parts of the actual clusterstate (for example `GET /_cluster/state`) and statistics about it (for example,`GET /_cluster/stats`). This produces a single document type. In versions priorto X-Pack 5.5, this was actually three separate collectors that resulted inthree separate types: `cluster_stats`, `cluster_state`, and `cluster_info`. In5.5 and later, all three are combined into `cluster_stats`. This only runs onthe *elected* master node and the data collected (`cluster_stats`) largelycontrols the UI. When this data is not present, it indicates either amisconfiguration on the elected master node, timeouts related to the collectionof the data, or issues with storing the data. Only a single document is producedper collection. |
| Index Stats | `indices_stats`, `index_stats` | Gathers details about the indices in the cluster, both in summary andindividually. This creates many documents that represent parts of the indexstatistics output (for example, `GET /_stats`). This information only needs tobe collected once, so it is collected on the *elected* master node. The mostcommon failure for this collector relates to an extreme number of indices — andtherefore time to gather them — resulting in timeouts. One summary`indices_stats` document is produced per collection and one `index_stats`document is produced per index, per collection. |
| Index Recovery | `index_recovery` | Gathers details about index recovery in the cluster. Index recovery representsthe assignment of *shards* at the cluster level. If an index is not recovered,it is not usable. This also corresponds to shard restoration via snapshots. Thisinformation only needs to be collected once, so it is collected on the *elected*master node. The most common failure for this collector relates to an extremenumber of shards — and therefore time to gather them — resulting in timeouts.This creates a single document that contains all recoveries by default, whichcan be quite large, but it gives the most accurate picture of recovery in theproduction cluster. |
| Shards | `shards` | Gathers details about all *allocated* shards for all indices, particularlyincluding what node the shard is allocated to. This information only needs to becollected once, so it is collected on the *elected* master node. The collectoruses the local cluster state to get the routing table without any networktimeout issues unlike most other collectors. Each shard is represented by aseparate monitoring document. |
| Jobs | `job_stats` | Gathers details about all machine learning job statistics (for example, `GET/_ml/anomaly_detectors/_stats`). This information only needs to be collectedonce, so it is collected on the *elected* master node. However, for the masternode to be able to perform the collection, the master node must have`xpack.ml.enabled` set to true (default) and a license level that supports {{ml}}. |
| Node Stats | `node_stats` | Gathers details about the running node, such as memory utilization and CPUusage (for example, `GET /_nodes/_local/stats`). This runs on *every* node with{{monitor-features}} enabled. One common failure results in the timeout of the nodestats request due to too many segment files. As a result, the collector spendstoo much time waiting for the file system stats to be calculated until itfinally times out. A single `node_stats` document is created per collection.This is collected per node to help to discover issues with nodes communicatingwith each other, but not with the monitoring cluster (for example, intermittentnetwork issues or memory pressure). |

The {{es}} {{monitor-features}} use a single threaded scheduler to run the collection of {{es}} monitoring data by all of the appropriate collectors on each node. This scheduler is managed locally by each node and its interval is controlled by specifying the `xpack.monitoring.collection.interval`, which defaults to 10 seconds (`10s`), at either the node or cluster level.

Fundamentally, each collector works on the same principle. Per collection interval, each collector is checked to see whether it should run and then the appropriate collectors run. The failure of an individual collector does not impact any other collector.

Once collection has completed, all of the monitoring data is passed to the exporters to route the monitoring data to the monitoring clusters.

If gaps exist in the monitoring charts in {{kib}}, it is typically because either a collector failed or the monitoring cluster did not receive the data (for example, it was being restarted). In the event that a collector fails, a logged error should exist on the node that attempted to perform the collection.

::::{note}
Collection is currently done serially, rather than in parallel, to avoid extra overhead on the elected master node. The downside to this approach is that collectors might observe a different version of the cluster state within the same collection period. In practice, this does not make a significant difference and running the collectors in parallel would not prevent such a possibility.
::::


For more information about the configuration options for the collectors, see [Monitoring collection settings](elasticsearch://reference/elasticsearch/configuration-reference/monitoring-settings.md#monitoring-collection-settings).


## Collecting data from across the {{stack}} [es-monitoring-stack]

{{es}} {{monitor-features}} also receive monitoring data from other parts of the {{stack}}. In this way, it serves as an unscheduled monitoring data collector for the stack.

By default, data collection is disabled. {{es}} monitoring data is not collected and all monitoring data from other sources such as {{kib}}, Beats, and Logstash is ignored. You must set `xpack.monitoring.collection.enabled` to `true` to enable the collection of monitoring data. See [Monitoring settings](elasticsearch://reference/elasticsearch/configuration-reference/monitoring-settings.md).

Once data is received, it is forwarded to the exporters to be routed to the monitoring cluster like all monitoring data.

::::{warning}
Because this stack-level "collector" lives outside of the collection interval of {{es}} {{monitor-features}}, it is not impacted by the `xpack.monitoring.collection.interval` setting. Therefore, data is passed to the exporters whenever it is received. This behavior can result in indices for {{kib}}, Logstash, or Beats being created somewhat unexpectedly.
::::


While the monitoring data is collected and processed, some production cluster metadata is added to incoming documents. This metadata enables {{kib}} to link the monitoring data to the appropriate cluster. If this linkage is unimportant to the infrastructure that you’re monitoring, it might be simpler to configure Logstash and Beats to report monitoring data directly to the monitoring cluster. This scenario also prevents the production cluster from adding extra overhead related to monitoring data, which can be very useful when there are a large number of Logstash nodes or Beats.

For more information about typical monitoring architectures, see [How it works](../stack-monitoring.md).

