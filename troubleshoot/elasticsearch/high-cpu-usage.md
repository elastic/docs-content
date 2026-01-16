---
navigation_title: High CPU usage
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/high-cpu-usage.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Symptom: High CPU usage [high-cpu-usage]

{{es}} uses [thread pools](elasticsearch://reference/elasticsearch/configuration-reference/thread-pool-settings.md) to manage node CPU and JVM resources for concurrent operations. The thread pools are portioned different numbers of threads, frequently based off of the total processors allocated to the node. This helps the node remain responsive while processing either [expensive tasks or a task queue backlog](task-queue-backlog.md). {{es}} [rejects requests](rejected-requests.md) related to a thread pool while its queue is saturated.

An individual task can spawn work on multiple node threads, frequently within these designated thread pools. It is normal for an [individual thread](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-hot-threads) to saturate its CPU usage. A thread reporting CPU saturation could reflect either the thread spending its time processing an ask from an individual expensive task or the thread staying busy due to processing asks from multiple tasks. The hot threads report shows a snapshot of Java threads across a time interval. Therefore, the hot threads cannot be directly mapped to any given [node task](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-tasks).

A node can temporarily saturate all of the CPU threads allocated to it. It's unusual for this state to be ongoing for an extended period. It might suggest that the node is:

* sized disproportionately to its [data tier](/manage-data/lifecycle/data-tiers.md) peers.
* receiving a volume of requests above its workload capability, for example if the node is sized below the [minimum recommendations](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md#ec-minimum-recommendations).
* processing an [expensive task](task-queue-backlog.md).

To mitigate performance outages, we default recommend pulling an [{{es}} diagnostic](/troubleshoot/elasticsearch/diagnostic.md) for post-mortem but trying to resolve using [scaling](/deploy-manage/production-guidance/scaling-considerations.md).

Refer to the sections below to troubleshoot degraded CPU performance.

## Diagnose high CPU usage [diagnose]

### Check CPU usage [check-cpu-usage]

To check the CPU usage per node, use the [cat nodes API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes):

```console
GET _cat/nodes?v=true&s=cpu:desc&h=name,role,master,cpu,load*,allocated_processors
```

The reported metrics are:

* `cpu`: the instantaneous percentage of system CPU usage
* `load_1m`, `load_5m`, and `load_15m`: the average amount of processes waiting for the designated time interval
* `allocated_processors`: number of processors allocated to the node {applies_to}`stack: ga 9.3`

For more detail, refer to the [node statistics](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats) API documentation.

These alerting thresholds for these metrics depend on your team's workload-vs-duration needs. However, as a general start point baseline, you might consider investigating if:

* (Recommended) CPU usage remains elevated above 95% for an extended interval.
* Load average divided by the node's allocated processors is elevated. This metric by itself is insufficient as a gauge  and should be considered alongside elevated response times, as it otherwise might reflect normal background I/O.

If CPU usage is deemed concerning, we recommend checking this output for traffic patterns either segmented by or [hot spotted](/troubleshoot/elasticsearch/hotspotting.md) in the columns `role` and `master`. CPU issues spanning an entire data tier suggest a configuration issue or the tier being undersized. CPU issues spanning a subset of nodes within one or more data tiers suggest [hot spotting](/troubleshoot/elasticsearch/hotspotting.md) tasks.


### Check hot threads [check-hot-threads]

High CPU usage frequently correlates to [a long-running task or a backlog of tasks](task-queue-backlog.md). When a node is reporting elevated CPU usage, to correlate the thread to a task use the [nodes hot threads API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-hot-threads) to check for resource-intensive threads running on it.

```console
GET _nodes/hot_threads
```

This API returns a snapshot of hot Java threads. As a simplified example, the response output might appear like the following:

```text
::: {instance-0000000001}{9fVI1XoXQJCgHwsOPlVEig}{RrJGwEaESRmNs75Gjs1SOg}{instance-0000000001}{10.42.9.84}{10.42.9.84:19058}{himrst}{9.3.0}{7000099-8525000}{region=unknown-region, server_name=instance-0000000001.b84ab96b481f43d791a1a73477a10d40, xpack.installed=true, transform.config_version=10.0.0, ml.config_version=12.0.0, data=hot, logical_availability_zone=zone-1, availability_zone=us-central1-a, instance_configuration=gcp.es.datahot.n2.68x10x45}
   Hot threads at 2025-05-14T17:59:30.199Z, interval=500ms, busiestThreads=10000, ignoreIdleThreads=true:
   
   88.5% [cpu=88.5%, other=0.0%] (442.5ms out of 500ms) cpu usage by thread '[write]'
     8/10 snapshots sharing following 29 elements
       com.fasterxml.jackson.dataformat.smile@2.17.2/com.fasterxml.jackson.dataformat.smile.SmileParser.nextToken(SmileParser.java:434)
       org.elasticsearch.xpack.monitoring.exporter.local.LocalBulk.doAdd(LocalBulk.java:69)
       # ... 
     2/10 snapshots sharing following 37 elements
       app/org.elasticsearch.xcontent/org.elasticsearch.xcontent.support.filtering.FilterPath$FilterPathBuilder.insertNode(FilterPath.java:172)
       # ...
```

The response output is formatted as follows:

```text
::: {NAME}{ID}{...}{HOST_NAME}{ADDRESS}{...}{ROLES}{VERSION}{...}{ATTRIBUTES}
   Hot threads at TIMESTAMP, interval=INTERVAL_FROM_API, busiestThreads=THREADS_FROM_API, ignoreIdleThreads=IDLE_FROM_API:
   
   TOTAL_CPU% [cpu=ELASTIC_CPU%, other=OTHER_CPU%] (Xms out of INTERVAL_FROM_API) cpu usage by thread 'THREAD'
     X/... snapshots sharing following X elements
       STACKTRACE_SAMPLE
       # ... 
     X/... snapshots sharing following X elements
       STACKTRACE_SAMPLE
       # ...
```

Three measures of CPU time are reported in the API output:

* `TOTAL_CPU`: the total CPU used by the CPU thread (either by {{es}} or the operating system)
* `ELASTIC_CPU`: the CPU available to {{es}} and used by {{es}}
* `OTHER_CPU`: a miscellaneous bucket for disk/network IO or garbage collection (GC)

Although `ELASTIC_CPU` is the main driver of elevated `TOTAL_CPU`, you should also investigate the `STACKTRACE_SAMPLE`. These lines frequently emit {{es}} [loggers](/deploy-manage/monitor/logging-configuration.md) but might also surface non-{{es}} processes. Common examples of performance log entries include:

* `org.elasticsearch.action.search` or `org.elasticsearch.search` is a [running search](/explore-analyze/index.md)
* `org.elasticsearch.cluster.metadata.Metadata.findAliases` is an [alias](/manage-data/data-store/aliases.md) look-up/resolver 
* `org.elasticsearch.common.regex` is [custom Regex code](/explore-analyze/scripting/modules-scripting-regular-expressions-tutorial.md)
* `org.elasticsearch.grok` is [custom Grok code](/explore-analyze/scripting/grok.md)
* `org.elasticsearch.index.fielddata.ordinals.GlobalOrdinalsBuilder.build` is [building global ordinals](elasticsearch:///reference/elasticsearch/mapping-reference/eager-global-ordinals.md)
* `org.elasticsearch.ingest.Pipeline` or `org.elasticsearch.ingest.CompoundProcessor` is an [ingest pipeline](/manage-data/ingest/transform-enrich/ingest-pipelines.md)
* `org.elasticsearch.xpack.core.esql` or `org.elasticsearch.xpack.esql` is a [running ES|QL](/explore-analyze/query-filter/languages/esql-kibana.md) query

If your team would like assistance correlating hot threads and node tasks, kindly [{capture your {es}} diagnostics](/troubleshoot/elasticsearch/diagnostic.md) when you [contact us](/troubleshoot/index.md#contact-us).

### Check garbage collection [check-garbage-collection]

High CPU usage is often caused by excessive JVM garbage collection (GC) activity. This excessive GC typically arises from configuration problems or inefficient queries causing increased heap memory usage. 

For troubleshooting information, refer to [high JVM memory pressure](/troubleshoot/elasticsearch/high-jvm-memory-pressure.md).


## Monitor CPU usage [monitor]

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::

To track CPU usage over time, we recommend enabling monitoring:

:::::::{applies-switch}

::::::{applies-item} { ess:, ece: }
* (Recommend) Enable [AutoOps](/deploy-manage/monitor/autoops.md)
* Enable [logs and metrics](/deploy-manage/monitor/stack-monitoring/ece-ech-stack-monitoring.md). When logs and metrics are enabled, monitoring information is visible on {{kib}}'s [Stack Monitoring](../../deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md) page.

    You can also enable the [CPU usage threshold alert](../../deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md) to be notified about potential issues through email.

* From your deployment menu, view the [**Performance**](../../deploy-manage/monitor/access-performance-metrics-on-elastic-cloud.md) page. On this page, you can view two key metrics:

    * **CPU usage**: Your deployment’s CPU usage, represented as a percentage.
    * **CPU credits**: Your remaining CPU credits, measured in seconds of CPU time.


{{ech}} grants [CPU credits](/deploy-manage/deploy/elastic-cloud/ec-vcpu-boost-instance.md) per deployment to provide smaller clusters with performance boosts when needed. High CPU usage can deplete these credits, which might lead to [performance degradation](../monitoring/performance.md) and [increased cluster response times](../monitoring/cluster-response-time.md).
::::::

::::::{applies-item} { self:, eck: }
* (Recommend) Enable [AutoOps](/deploy-manage/monitor/autoops.md)
* Enable [{{es}} monitoring](/deploy-manage/monitor/stack-monitoring.md). When logs and metrics are enabled, monitoring information is visible on {{kib}}'s [Stack Monitoring](../../deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md) page.

    You can also enable the [CPU usage threshold alert](../../deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md) to be notified about potential issues through email.
::::::

:::::::

You might also consider enabling [slow logs](elasticsearch://reference/elasticsearch/index-settings/slow-log.md) to review as part of the [task backlog](task-queue-backlog.md).


## Reduce CPU usage [reduce-cpu-usage]

High CPU usage usually correlates to live [expensive tasks or back-logged tasks](task-queue-backlog.md) running against the node. The following tips outline common causes and solutions for heightened CPU usage occurring even during periods of low or no traffic.

### Oversharding [high-cpu-usage-oversharding]

Oversharding occurs when a cluster has too many shards, often times caused by shards being smaller than optimal. We recommend the following best practices:

* [Aim for shards of up to 200M documents, or with sizes between 10GB and 50GB](/deploy-manage/production-guidance/optimize-performance/size-shards.md#shard-size-recommendation).
* [Master-eligible nodes should have at least 1GB of heap per 3000 indices](/deploy-manage/production-guidance/optimize-performance/size-shards.md#shard-count-recommendation).

While {{es}} doesn’t have a strict minimum shard size, an excessive number of small shards can negatively impact performance. Each shard consumes cluster resources because {{es}} must maintain metadata and manage shard states across all nodes.

If you have too many small shards, you can address this by doing the following:

* Removing empty or unused indices.
* Deleting or closing indices containing outdated or unnecessary data.
* Reindexing smaller shards into fewer, larger shards to optimize cluster performance.

If your shards are sized correctly but you are still experiencing oversharding, creating a more aggressive [index lifecycle management strategy](/manage-data/lifecycle/index-lifecycle-management.md) or deleting old indices can help reduce the number of shards.

### Overrode allocated processors [high-cpu-usage-allocated]

By default, {{es}} allocates processors equal to the number reported available by the operating system. You can override this behaviour by adjusting the value of [`node.processors`](elasticsearch://reference/elasticsearch/configuration-reference/thread-pool-settings.md#node.processors), but this advanced setting should be configured only after you've performed load testing.

{{ech}} supports [vCPU boosting](/deploy-manage/deploy/elastic-cloud/ec-vcpu-boost-instance.md) which should be relied on only for short bursting traffic and not for normal workload traffic.
