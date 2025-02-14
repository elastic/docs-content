---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/es-monitoring-exporters.html
applies:
  stack: deprecated 7.16.0
---

# Exporters [es-monitoring-exporters]

::::{important} 
{{agent}} and {{metricbeat}} are the recommended methods for collecting and shipping monitoring data to a monitoring cluster.

If you have previously configured legacy collection methods, you should migrate to using [{{agent}}](collecting-monitoring-data-with-elastic-agent.md) or [{{metricbeat}}](collecting-monitoring-data-with-metricbeat.md) collection. Do not use legacy collection alongside other collection methods.

::::


The purpose of exporters is to take data collected from any Elastic Stack source and route it to the monitoring cluster. It is possible to configure more than one exporter, but the general and default setup is to use a single exporter.

There are two types of exporters in {{es}}:

`local`
:   The default exporter used by {{es}} {{monitor-features}}. This exporter routes data back into the *same* cluster. See [Local exporters](es-local-exporter.md).

`http`
:   The preferred exporter, which you can use to route data into any supported {{es}} cluster accessible via HTTP. Production environments should always use a separate monitoring cluster. See [HTTP exporters](es-http-exporter.md).

Both exporters serve the same purpose: to set up the monitoring cluster and route monitoring data. However, they perform these tasks in very different ways. Even though things happen differently, both exporters are capable of sending all of the same data.

Exporters are configurable at both the node and cluster level. Cluster-wide settings, which are updated with the [`_cluster/settings` API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings), take precedence over settings in the `elasticsearch.yml` file on each node. When you update an exporter, it is completely replaced by the updated version of the exporter.

::::{important} 
It is critical that all nodes share the same setup. Otherwise, monitoring data might be routed in different ways or to different places.
::::


When the exporters route monitoring data into the monitoring cluster, they use `_bulk` indexing for optimal performance. All monitoring data is forwarded in bulk to all enabled exporters on the same node. From there, the exporters serialize the monitoring data and send a bulk request to the monitoring cluster. There is no queuing—​in memory or persisted to disk—​so any failure during the export results in the loss of that batch of monitoring data. This design limits the impact on {{es}} and the assumption is that the next pass will succeed.

Routing monitoring data involves indexing it into the appropriate monitoring indices. Once the data is indexed, it exists in a monitoring index that, by default, is named with a daily index pattern. For {{es}} monitoring data, this is an index that matches `.monitoring-es-6-*`. From there, the data lives inside the monitoring cluster and must be curated or cleaned up as necessary. If you do not curate the monitoring data, it eventually fills up the nodes and the cluster might fail due to lack of disk space.

::::{tip} 
You are strongly recommended to manage the curation of indices and particularly the monitoring indices. To do so, you can take advantage of the [cleaner service](es-local-exporter.md#local-exporter-cleaner) or [Elastic Curator](https://www.elastic.co/guide/en/elasticsearch/client/curator/current/index.html).
::::


There is also a disk watermark (known as the flood stage watermark), which protects clusters from running out of disk space. When this feature is triggered, it makes all indices (including monitoring indices) read-only until the issue is fixed and a user manually makes the index writeable again. While an active monitoring index is read-only, it will naturally fail to write (index) new data and will continuously log errors that indicate the write failure. For more information, see [Disk-based shard allocation settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cluster.html#disk-based-shard-allocation).


## Default exporters [es-monitoring-default-exporter] 

If a node or cluster does not explicitly define an exporter, the following default exporter is used:

```yaml
xpack.monitoring.exporters.default_local: <1>
  type: local
```

1. The exporter name uniquely defines the exporter, but it is otherwise unused. When you specify your own exporters, you do not need to explicitly overwrite or reference `default_local`.


If another exporter is already defined, the default exporter is *not* created. When you define a new exporter, if the default exporter exists, it is automatically removed.


## Exporter templates and ingest pipelines [es-monitoring-templates] 

Before exporters can route monitoring data, they must set up certain {{es}} resources. These resources include templates and ingest pipelines. The following table lists the templates that are required before an exporter can route monitoring data:

| Template | Purpose |
| --- | --- |
| `.monitoring-alerts` | All cluster alerts for monitoring data. |
| `.monitoring-beats` | All Beats monitoring data. |
| `.monitoring-es` | All {{es}} monitoring data. |
| `.monitoring-kibana` | All {{kib}} monitoring data. |
| `.monitoring-logstash` | All Logstash monitoring data. |

The templates are ordinary {{es}} templates that control the default settings and mappings for the monitoring indices.

By default, monitoring indices are created daily (for example, `.monitoring-es-6-2017.08.26`). You can change the default date suffix for monitoring indices with the `index.name.time_format` setting. You can use this setting to control how frequently monitoring indices are created by a specific `http` exporter. You cannot use this setting with `local` exporters. For more information, see [HTTP exporter settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/monitoring-settings.html#http-exporter-settings).

::::{warning} 
Some users create their own templates that match *all* index patterns, which therefore impact the monitoring indices that get created. It is critical that you do not disable `_source` storage for the monitoring indices. If you do, {{kib}} {{monitor-features}} do not work and you cannot visualize monitoring data for your cluster.
::::


The following table lists the ingest pipelines that are required before an exporter can route monitoring data:

| Pipeline | Purpose |
| --- | --- |
| `xpack_monitoring_2` | Upgrades X-Pack monitoring data coming from X-Pack5.0 - 5.4 to be compatible with the format used in 5.5 {{monitor-features}}. |
| `xpack_monitoring_6` | A placeholder pipeline that is empty. |

Exporters handle the setup of these resources before ever sending data. If resource setup fails (for example, due to security permissions), no data is sent and warnings are logged.

::::{note} 
Empty pipelines are evaluated on the coordinating node during indexing and they are ignored without any extra effort. This inherently makes them a safe, no-op operation.
::::


For monitoring clusters that have disabled `node.ingest` on all nodes, it is possible to disable the use of the ingest pipeline feature. However, doing so blocks its purpose, which is to upgrade older monitoring data as our mappings improve over time. Beginning in 6.0, the ingest pipeline feature is a requirement on the monitoring cluster; you must have `node.ingest` enabled on at least one node.

::::{warning} 
Once any node running 5.5 or later has set up the templates and ingest pipeline on a monitoring cluster, you must use {{kib}} 5.5 or later to view all subsequent data on the monitoring cluster. The easiest way to determine whether this update has occurred is by checking for the presence of indices matching `.monitoring-es-6-*` (or more concretely the existence of the new pipeline). Versions prior to 5.5 used `.monitoring-es-2-*`.
::::


Each resource that is created by an exporter has a `version` field, which is used to determine whether the resource should be replaced. The `version` field value represents the latest version of {{monitor-features}} that changed the resource. If a resource is edited by someone or something external to the {{monitor-features}}, those changes are lost the next time an automatic update occurs.

