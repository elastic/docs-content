---
navigation_title: High CPU usage
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/high-cpu-usage.html
---

# Symptom: High CPU usage [high-cpu-usage]

{{es}} uses [thread pools](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/thread-pool-settings.md) to manage CPU resources for concurrent operations. High CPU usage typically means one or more thread pools are running low.

If a thread pool is depleted, {{es}} will [reject requests](rejected-requests.md) related to the thread pool. For example, if the `search` thread pool is depleted, {{es}} will reject search requests until more threads are available.

You might experience high CPU usage if a [data tier](../../manage-data/lifecycle/data-tiers.md), and therefore the nodes assigned to that tier, is experiencing more traffic than other tiers. This imbalance in resource utilization is also known as [hot spotting](hotspotting.md).

::::{tip}
If you’re using Elastic Cloud Hosted, then you can use AutoOps to monitor your cluster. AutoOps significantly simplifies cluster management with performance recommendations, resource utilization visibility, real-time issue detection and resolution paths. For more information, refer to [Monitor with AutoOps](/deploy-manage/monitor/autoops.md).

::::



## Diagnose high CPU usage [diagnose-high-cpu-usage]

**Check CPU usage**

You can check the CPU usage per node using the [cat nodes API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes):

```console
GET _cat/nodes?v=true&s=cpu:desc
```

The response’s `cpu` column contains the current CPU usage as a percentage. The `name` column contains the node’s name. Elevated but transient CPU usage is normal. However, if CPU usage is elevated for an extended duration, it should be investigated.

To track CPU usage over time, we recommend enabling monitoring:

:::::::{tab-set}

::::::{tab-item} {{ech}}
* (Recommended) Enable [logs and metrics](../../deploy-manage/monitor/stack-monitoring/elastic-cloud-stack-monitoring.md). When logs and metrics are enabled, monitoring information is visible on {{kib}}'s [Stack Monitoring](../../deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md) page.

    You can also enable the [CPU usage threshold alert](../../deploy-manage/monitor/monitoring-data/kibana-alerts.md) to be notified about potential issues through email.

* From your deployment menu, view the [**Performance**](../../deploy-manage/monitor/monitoring-data/access-performance-metrics-on-elastic-cloud.md) page. On this page, you can view two key metrics:

    * **CPU usage**: Your deployment’s CPU usage, represented as a percentage.
    * **CPU credits**: Your remaining CPU credits, measured in seconds of CPU time.


{{ech}} grants [CPU credits](../../deploy-manage/monitor/monitoring-data/ec-vcpu-boost-instance.md) per deployment to provide smaller clusters with performance boosts when needed. High CPU usage can deplete these credits, which might lead to [performance degradation](../monitoring/performance.md) and [increased cluster response times](../monitoring/cluster-response-time.md).
::::::

::::::{tab-item} Self-managed
* Enable [{{es}} monitoring](../../deploy-manage/monitor/stack-monitoring.md). When logs and metrics are enabled, monitoring information is visible on {{kib}}'s [Stack Monitoring](../../deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md) page.

    You can also enable the [CPU usage threshold alert](../../deploy-manage/monitor/monitoring-data/kibana-alerts.md) to be notified about potential issues through email.
::::::

:::::::
**Check hot threads**

If a node has high CPU usage, use the [nodes hot threads API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-hot-threads) to check for resource-intensive threads running on the node.

```console
GET _nodes/hot_threads
```

This API returns a breakdown of any hot threads in plain text. High CPU usage frequently correlates to [a long-running task, or a backlog of tasks](task-queue-backlog.md).


## Reduce CPU usage [reduce-cpu-usage]

The following tips outline the most common causes of high CPU usage and their solutions.

**Scale your cluster**

Heavy indexing and search loads can deplete smaller thread pools. To better handle heavy workloads, add more nodes to your cluster or upgrade your existing nodes to increase capacity.

**Spread out bulk requests**

While more efficient than individual requests, large [bulk indexing](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) or [multi-search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch) requests still require CPU resources. If possible, submit smaller requests and allow more time between them.

**Cancel long-running searches**

Long-running searches can block threads in the `search` thread pool. To check for these searches, use the [task management API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-tasks).

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
