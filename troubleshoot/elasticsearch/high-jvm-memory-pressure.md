---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/high-jvm-memory-pressure.html
---

# High JVM memory pressure [high-jvm-memory-pressure]

High JVM memory usage can degrade cluster performance and trigger [circuit breaker errors](circuit-breaker-errors.md). To prevent this, we recommend taking steps to reduce memory pressure if a node’s JVM memory usage consistently exceeds 85%.

::::{tip}
If you’re using Elastic Cloud Hosted, then you can use AutoOps to monitor your cluster. AutoOps significantly simplifies cluster management with performance recommendations, resource utilization visibility, real-time issue detection and resolution paths. For more information, refer to [Monitor with AutoOps](/deploy-manage/monitor/autoops.md).

::::



## Diagnose high JVM memory pressure [diagnose-high-jvm-memory-pressure]

**Check JVM memory pressure**

:::::::{tab-set}

::::::{tab-item} {{ech}}
From your deployment menu, click **Elasticsearch**. Under **Instances**, each instance displays a **JVM memory pressure** indicator. When the JVM memory pressure reaches 75%, the indicator turns red.

You can also use the [nodes stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats) to calculate the current JVM memory pressure for each node.

```console
GET _nodes/stats?filter_path=nodes.*.jvm.mem.pools.old
```

Use the response to calculate memory pressure as follows:

JVM Memory Pressure = `used_in_bytes` / `max_in_bytes`
::::::

::::::{tab-item} Self-managed
To calculate the current JVM memory pressure for each node, use the [nodes stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats).

```console
GET _nodes/stats?filter_path=nodes.*.jvm.mem.pools.old
```

Use the response to calculate memory pressure as follows:

JVM Memory Pressure = `used_in_bytes` / `max_in_bytes`
::::::

:::::::
**Check garbage collection logs**

As memory usage increases, garbage collection becomes more frequent and takes longer. You can track the frequency and length of garbage collection events in [`elasticsearch.log`](../../deploy-manage/monitor/logging-configuration/elasticsearch-log4j-configuration-self-managed.md). For example, the following event states {{es}} spent more than 50% (21 seconds) of the last 40 seconds performing garbage collection.

```txt
[timestamp_short_interval_from_last][INFO ][o.e.m.j.JvmGcMonitorService] [node_id] [gc][number] overhead, spent [21s] collecting in the last [40s]
```

**Capture a JVM heap dump**

To determine the exact reason for the high JVM memory pressure, capture a heap dump of the JVM while its memory usage is high, and also capture the [garbage collector logs](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/jvm-settings.md#gc-logging) covering the same time period.


## Reduce JVM memory pressure [reduce-jvm-memory-pressure]

This section contains some common suggestions for reducing JVM memory pressure.

**Reduce your shard count**

Every shard uses memory. In most cases, a small set of large shards uses fewer resources than many small shards. For tips on reducing your shard count, see [*Size your shards*](../../deploy-manage/production-guidance/optimize-performance/size-shards.md).

$$$avoid-expensive-searches$$$
**Avoid expensive searches**

Expensive searches can use large amounts of memory. To better track expensive searches on your cluster, enable [slow logs](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/slow-log.md).

Expensive searches may have a large [`size` argument](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/rest-apis/paginate-search-results.md), use aggregations with a large number of buckets, or include [expensive queries](../../explore-analyze/query-filter/languages/querydsl.md#query-dsl-allow-expensive-queries). To prevent expensive searches, consider the following setting changes:

* Lower the `size` limit using the [`index.max_result_window`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-modules.md#index-max-result-window) index setting.
* Decrease the maximum number of allowed aggregation buckets using the [search.max_buckets](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/search-settings.md#search-settings-max-buckets) cluster setting.
* Disable expensive queries using the [`search.allow_expensive_queries`](../../explore-analyze/query-filter/languages/querydsl.md#query-dsl-allow-expensive-queries) cluster setting.
* Set a default search timeout using the [`search.default_search_timeout`](../../solutions/search/the-search-api.md#search-timeout) cluster setting.

```console
PUT _settings
{
  "index.max_result_window": 5000
}

PUT _cluster/settings
{
  "persistent": {
    "search.max_buckets": 20000,
    "search.allow_expensive_queries": false
  }
}
```

**Prevent mapping explosions**

Defining too many fields or nesting fields too deeply can lead to [mapping explosions](../../manage-data/data-store/mapping.md#mapping-limit-settings) that use large amounts of memory. To prevent mapping explosions, use the [mapping limit settings](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/mapping-limit.md) to limit the number of field mappings.

**Spread out bulk requests**

While more efficient than individual requests, large [bulk indexing](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) or [multi-search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch) requests can still create high JVM memory pressure. If possible, submit smaller requests and allow more time between them.

**Upgrade node memory**

Heavy indexing and search loads can cause high JVM memory pressure. To better handle heavy workloads, upgrade your nodes to increase their memory capacity.
