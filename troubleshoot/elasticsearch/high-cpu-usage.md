---
navigation_title: High CPU usage
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/high-cpu-usage.html
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

# Symptom: High CPU usage [high-cpu-usage]

{{es}} uses [thread pools](elasticsearch://reference/elasticsearch/configuration-reference/thread-pool-settings.md) to manage CPU resources for concurrent operations. High CPU usage typically means one or more thread pools are running low.

If a thread pool is depleted, {{es}} will [reject requests](rejected-requests.md) related to the thread pool. For example, if the `search` thread pool is depleted, {{es}} will reject search requests until more threads are available.

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::



## Diagnose high CPU usage [diagnose-high-cpu-usage]

### Check CPU usage [check-cpu-usage]

You can check the CPU usage per node using the [cat nodes API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes):

```console
GET _cat/nodes?v=true&s=cpu:desc
```

The response’s `cpu` column contains the current CPU usage as a percentage. The `name` column contains the node’s name. Elevated but transient CPU usage is normal. However, if CPU usage is elevated for an extended duration, it should be investigated.

To track CPU usage over time, we recommend enabling monitoring:

:::::::{applies-switch}

::::::{applies-item} ess:
* (Recommended) Enable [logs and metrics](../../deploy-manage/monitor/stack-monitoring/ece-ech-stack-monitoring.md). When logs and metrics are enabled, monitoring information is visible on {{kib}}'s [Stack Monitoring](../../deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md) page.

    You can also enable the [CPU usage threshold alert](../../deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md) to be notified about potential issues through email.

* From your deployment menu, view the [**Performance**](../../deploy-manage/monitor/access-performance-metrics-on-elastic-cloud.md) page. On this page, you can view two key metrics:

    * **CPU usage**: Your deployment’s CPU usage, represented as a percentage.
    * **CPU credits**: Your remaining CPU credits, measured in seconds of CPU time.


{{ech}} grants [CPU credits](/deploy-manage/deploy/elastic-cloud/ec-vcpu-boost-instance.md) per deployment to provide smaller clusters with performance boosts when needed. High CPU usage can deplete these credits, which might lead to [performance degradation](../monitoring/performance.md) and [increased cluster response times](../monitoring/cluster-response-time.md).
::::::

::::::{applies-item} self:
* Enable [{{es}} monitoring](../../deploy-manage/monitor/stack-monitoring.md). When logs and metrics are enabled, monitoring information is visible on {{kib}}'s [Stack Monitoring](../../deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md) page.

    You can also enable the [CPU usage threshold alert](../../deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md) to be notified about potential issues through email.
::::::

:::::::
### Check hot threads [check-hot-threads]

If a node has high CPU usage, use the [nodes hot threads API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-hot-threads) to check for resource-intensive threads running on the node.

```console
GET _nodes/hot_threads
```

This API returns a breakdown of any hot threads in plain text. High CPU usage frequently correlates to [a long-running task, or a backlog of tasks](task-queue-backlog.md).


## Reduce CPU usage [reduce-cpu-usage]

The following tips outline the most common causes of high CPU usage and their solutions.

### Check JVM garbage collection [check-jvm-garbage-collection]

High CPU usage is often caused by excessive JVM garbage collection (GC) activity. This excessive GC typically arises from configuration problems or inefficient queries causing increased heap memory usage.

For optimal JVM performance, garbage collection should meet these criteria:

| GC type | Completion time | Frequency |
|---------|----------------|---------------------|
| Young GC | <50ms | ~once per 10 seconds |
| Old GC | <1s | ≤once per 10 minutes |

Excessive JVM garbage collection usually indicates high heap memory usage. Common potential reasons for increased heap memory usage include:

* Oversharding of indices
* Very large aggregation queries
* Excessively large bulk indexing requests
* Inefficient or incorrect mapping definitions
* Improper heap size configuration
* Misconfiguration of JVM new generation ratio (`-XX:NewRatio`)

### Hot spotting [high-cpu-usage-hot-spotting]

You might experience high CPU usage on specific data nodes or an entire [data tier](/manage-data/lifecycle/data-tiers.md) if traffic isn’t evenly distributed. This is known as [hot spotting](hotspotting.md). Hot spotting commonly occurs when read or write applications don’t evenly distribute requests across nodes, or when indices receiving heavy write activity, such as indices in the hot tier, have their shards concentrated on just one or a few nodes.

For details on diagnosing and resolving these issues, refer to [](hotspotting.md).

### Oversharding [high-cpu-usage-oversharding]

Oversharding occurs when a cluster has too many shards, often times caused by shards being smaller than optimal. While {{es}} doesn’t have a strict minimum shard size, an excessive number of small shards can negatively impact performance. Each shard consumes cluster resources because {{es}} must maintain metadata and manage shard states across all nodes.

If you have too many small shards, you can address this by doing the following:

* Removing empty or unused indices.
* Deleting or closing indices containing outdated or unnecessary data.
* Reindexing smaller shards into fewer, larger shards to optimize cluster performance.

If your shards are sized correctly but you are still experiencing oversharding, creating a more aggressive [index lifecycle management strategy](/manage-data/lifecycle/index-lifecycle-management.md) or deleting old indices can help reduce the number of shards.

For more information, refer to [](/deploy-manage/production-guidance/optimize-performance/size-shards.md).

### Additional recommendations

To further reduce CPU load or mitigate temporary spikes in resource usage, consider these steps:

#### Scale your cluster [scale-your-cluster]

Heavy indexing and search loads can deplete smaller thread pools. Add nodes or upgrade existing ones to handle increased indexing and search loads more effectively.

#### Spread out bulk requests [spread-out-bulk-requests]

Submit smaller [bulk indexing](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk-1) or multi-search requests, and space them out to avoid overwhelming thread pools.

#### Cancel long-running searches [cancel-long-running-searches]

Regularly use the [task management API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-tasks-list) to identify and cancel searches that consume excessive CPU time.

```console
GET _tasks?actions=*search&detailed
```

The response’s `description` contains the search request and its queries. `running_time_in_nanos` shows how long the search has been running.

```console-result
{
  "nodes" : {
    "oTUltX4IQMOUUVeiohTt8A" : {
      "name" : "my-node",
      "transport_address" : "127.0.0.1:9300",
      "host" : "127.0.0.1",
      "ip" : "127.0.0.1:9300",
      "tasks" : {
        "oTUltX4IQMOUUVeiohTt8A:464" : {
          "node" : "oTUltX4IQMOUUVeiohTt8A",
          "id" : 464,
          "type" : "transport",
          "action" : "indices:data/read/search",
          "description" : "indices[my-index], search_type[QUERY_THEN_FETCH], source[{\"query\":...}]",
          "start_time_in_millis" : 4081771730000,
          "running_time_in_nanos" : 13991383,
          "cancellable" : true
        }
      }
    }
  }
}
```

To cancel a search and free up resources, use the API’s `_cancel` endpoint.

```console
POST _tasks/oTUltX4IQMOUUVeiohTt8A:464/_cancel
```

For additional tips on how to track and avoid resource-intensive searches, see [Avoid expensive searches](high-jvm-memory-pressure.md#avoid-expensive-searches).
