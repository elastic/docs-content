---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/high-jvm-memory-pressure.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# High JVM memory pressure [high-jvm-memory-pressure]

High JVM memory usage can degrade cluster performance and trigger [circuit breaker errors](circuit-breaker-errors.md). To prevent this, we recommend taking steps to reduce memory pressure if a node’s JVM memory usage consistently exceeds 85%.

## Diagnose high JVM memory pressure [diagnose-high-jvm-memory-pressure]

### Check JVM memory pressure [diagnose-check-pressure] 

{{es}}'s JVM [uses a G1GC garbage collector](/deploy-manage/deploy/self-managed/bootstrap-checks.md). Over time this causes the JVM heap usage metric to reflect a sawtooth pattern as shown in [Understanding JVM heap memory](https://www.elastic.co/blog/jvm-essentials-for-elasticsearch). This causes the reported heap percent to fluctuate as it is an instantaneous measurement. You should focus monitoring on the JVM memory pressure, which is a rolling average of old garbage collection, and better represents the node's ongoing JVM responsiveness.

Use the [nodes stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats) to calculate the current JVM memory pressure for each node.

```console
GET _nodes/stats?filter_path=nodes.*.name,nodes.*.jvm.mem.pools.old
```

From the previous output, you can calculate the memory pressure as the ratio of `used_in_bytes` to `max_in_bytes`. For example, you can store this output into `nodes_stats.json` and then using [third-party tool JQ](https://jqlang.github.io/jq/) to process it:

```bash
cat nodes_stats.json | jq -rc '.nodes[]|.name as $n|.jvm.mem.pools.old|{name:$n, memory_pressure:(100*.used_in_bytes/.max_in_bytes|round) }'
```

{{ech}} and {{ece}} also include a JVM memory pressure indicator for each node in your cluster in the deployment's overview page. These indicators turn red when JVM memory pressure reaches 75%. [Learn more about memory pressure monitoring](/deploy-manage/monitor/ec-memory-pressure.md).

:::::::

### Check garbage collection logs [diagnose-check-gc]

As memory usage increases, garbage collection becomes more frequent and takes longer. You can track the frequency and length of garbage collection events in [`elasticsearch.log`](../../deploy-manage/monitor/logging-configuration/elasticsearch-log4j-configuration-self-managed.md). For example, the following event states {{es}} spent more than 50% (21 seconds) of the last 40 seconds performing garbage collection.

```txt
[timestamp_short_interval_from_last][INFO ][o.e.m.j.JvmGcMonitorService] [node_id] [gc][number] overhead, spent [21s] collecting in the last [40s]
```

Garbage collection activity can also appear in the output of the [nodes hot threads API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-hot-threads), under the `OTHER_CPU` category, as described in [troubleshooting high CPU usage](/troubleshoot/elasticsearch/high-cpu-usage.md#check-hot-threads).

For optimal JVM performance, garbage collection (GC) should meet these criteria:

| GC type | Completion time | Frequency |
|---------|----------------|---------------------|
| Young GC | <50ms | ~once per 10 seconds |
| Old GC | <1s | ≤once per 10 minutes |


### Capture a JVM heap dump [diagnose-check-dump] 

To determine the exact reason for the high JVM memory pressure, capture and review a heap dump of the JVM while its memory usage is high. 

If you have an [Elastic subscription](https://www.elastic.co/pricing), you can [request Elastic's assistance](/troubleshoot/index.md#contact-us) reviewing this output. When reaching out, follow these guidelines:

* Grant written permission for Elastic to review your uploaded heap dumps within the support case.
* Share this file only after receiving any necessary business approvals as it might contain private information. Files are handled according to [Elastic's privacy statement](https://www.elastic.co/legal/privacy-statement).
* Share heap dumps through our secure [Support Portal](https://support.elastic.co/). If your files are too large to upload, you can request a secure URL in the support case.
* Share the [garbage collector logs](elasticsearch://reference/elasticsearch/jvm-settings.md#gc-logging) covering the same time period.

## Monitor JVM memory pressure [monitor-jvm-memory-pressure]

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::

To track JVM memory pressure over time, enable monitoring using one of the following options, depending on your deployment type:

:::::::{applies-switch}

::::::{applies-item} { ess:, ece: }
* (Recommend) Enable [AutoOps](/deploy-manage/monitor/autoops.md).
* Enable [logs and metrics](/deploy-manage/monitor/stack-monitoring/ece-ech-stack-monitoring.md). When logs and metrics are enabled, monitoring information is visible on {{kib}}'s [Stack Monitoring](../../deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md) page. You can also enable the [JVM memory threshold alert](../../deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md) to be notified about potential issues through email.
* From your deployment menu, view the [**Performance**](../../deploy-manage/monitor/access-performance-metrics-on-elastic-cloud.md) page's [memory pressure troubleshooting charts](/troubleshoot/monitoring/high-memory-pressure.md).
::::::

::::::{applies-item} { self:, eck: }
* (Recommend) Enable [AutoOps](/deploy-manage/monitor/autoops.md).
* Enable [{{es}} monitoring](/deploy-manage/monitor/stack-monitoring.md). When logs and metrics are enabled, monitoring information is visible on {{kib}}'s [Stack Monitoring](../../deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md) page. You can also enable the [JVM memory threshold alert](../../deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md) to be notified about potential issues through email.
::::::

:::::::

## Reduce JVM memory pressure [reduce-jvm-memory-pressure]

This section contains some common suggestions for reducing JVM memory pressure.

### Common setup issues [reduce-jvm-memory-pressure-setup]

This section highlights common setup issues that can cause JVM memory pressure to remain elevated, even in the absence of obvious load, or to respond non-linearly during performance issues.

#### Disable swapping [reduce-jvm-memory-pressure-setup-swap]

```{applies_to}
deployment:
  self: ga
```

{{es}}'s JVM handles its own executables and can suffer severe performance degredation due to operating system swapping. We recommend [disabling swap](/deploy-manage/deploy/self-managed/setup-configuration-memory.md#bootstrap-memory_lock).

{{es}} recommends completely disabling swap on the operating system. This is because anything set {{es}}-level is best effort but swap can have severe impact on {{es}} performance. To check if any nodes are currently swapping, poll the [nodes stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats):

```console
GET _nodes/stats?filter_path=**.swap,nodes.*.name
```

For example, you can store this output into `nodes_stats.json` and then using [third-party tool JQ](https://jqlang.github.io/jq/) to process it:

```bash
cat nodes_stats.json | jq -rc '.nodes[]|{name:.name, swap_used:.os.swap.used_in_bytes}' | sort
```

If nodes are found to be swapping after attempting to disable on the {{es}} level, you need to escalate to [disabling swap on the operating system level](/deploy-manage/deploy/self-managed/setup-configuration-memory.md#disable-swap-files) to avoid performance impact.

#### Enable compressed OOPs [reduce-jvm-memory-pressure-setup-oops]

```{applies_to}
deployment:
  self: ga
  eck: ga
```

JVM performance strongly depends on having [Compressed OOPs](https://docs.oracle.com/javase/7/docs/technotes/guides/vm/performance-enhancements-7.html#compressedOop) enabled. The exact max heap size cutoff depends on operating system, but is typically around 30GB. To check if it is enabled, poll the [node information API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes):

```console
GET _nodes?filter_path=nodes.*.name,nodes.*.jvm.using_compressed_ordinary_object_pointers
```

For example, you can store this output into `nodes.json` and then using [third-party tool JQ](https://jqlang.github.io/jq/) to process it:

```bash
cat nodes.json | jq -rc '.nodes[]|{node:.name, compressed:.jvm.using_compressed_ordinary_object_pointers}'
```

#### Limit heap size to less than half of total RAM [reduce-jvm-memory-pressure-setup-heap]

```{applies_to}
deployment:
  self: ga
  eck: ga
```


By default, {{es}} manages the JVM heap size. If manually overridden, `Xms` and `Xmx` should be equal and not more than half of total operating system RAM. Refer to [Set the JVM heap size](elasticsearch://reference/elasticsearch/jvm-settings.md#set-jvm-heap-size) for detailed guidance and best practices.

To check these heap settings, poll the [node information API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes):

```console
GET _nodes?filter_path=nodes.*.name,nodes.*.jvm.mem
```

For example, you can store this output into `nodes.json` and then using [third-party tool JQ](https://jqlang.github.io/jq/) to process it:

```bash
cat nodes.json | jq -rc '.nodes[]|.name as $n|.jvm.mem|{name:$n, heap_min:.heap_init, heap_max:.heap_max}'
```

#### Reduce your shard count [reduce-jvm-memory-pressure-setup-shards]

Every shard uses memory. Usually, a small set of large shards uses fewer resources than many small shards. For tips on reducing your shard count, refer to [](/deploy-manage/production-guidance/optimize-performance/size-shards.md).

### Common traffic issues [reduce-jvm-memory-pressure-traffic]

This section contains some common suggestions for reducing JVM memory pressure related to traffic patterns.

#### Avoid expensive searches [reduce-jvm-memory-pressure-setup-searches]

Expensive searches can use large amounts of memory. To better track expensive searches on your cluster, enable [slow logs](/deploy-manage/monitor/logging-configuration/slow-logs.md).

Expensive searches may have a large [`size` argument](elasticsearch://reference/elasticsearch/rest-apis/paginate-search-results.md), use aggregations with a large number of buckets, or include [expensive queries](../../explore-analyze/query-filter/languages/querydsl.md#query-dsl-allow-expensive-queries). To prevent expensive searches, consider the following setting changes:

* Lower the `size` limit using the [`index.max_result_window`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-max-result-window) index setting.
* Decrease the maximum number of allowed aggregation buckets using the [search.max_buckets](elasticsearch://reference/elasticsearch/configuration-reference/search-settings.md#search-settings-max-buckets) cluster setting.
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

#### Prevent mapping explosion [reduce-jvm-memory-pressure-setup-mapping]

Defining too many fields or nesting fields too deeply can lead to [mapping explosions](/troubleshoot/elasticsearch/mapping-explosion.md) that use large amounts of memory. To prevent mapping explosions, use the [mapping limit settings](elasticsearch://reference/elasticsearch/index-settings/mapping-limit.md) to limit the number of field mappings.

You can also configure the {{kib}} [advanced setting](kibana://reference/advanced-settings.md) `data_views:fields_excluded_data_tiers` to improve performance by preventing {{kib}} from retrieving field data from specific data tiers. For example, to exclude cold and frozen tiers, typically used for searchable snapshots, set this value to `data_cold,data_frozen`. This can help Discover load fields faster, as described in [Troubleshooting guide: Solving 6 common issues in Kibana Discover load](https://www.elastic.co/blog/troubleshooting-guide-common-issues-kibana-discover-load#2.-load-fields).

#### Spread out bulk requests [reduce-jvm-memory-pressure-setup-bulks]

While more efficient than individual requests, large [bulk indexing](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) or [multi-search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch) requests can still create high JVM memory pressure. If possible, submit smaller requests and allow more time between them.

#### Scale node memory [reduce-jvm-memory-pressure-setup-scale]

Heavy indexing and search loads can cause high JVM memory pressure. To better handle heavy workloads, upgrade your nodes to increase their memory capacity.

### Reduce field data usage [reduce-jvm-memory-pressure-fielddata]

Computing the [field data mapping](elasticsearch://reference/elasticsearch/mapping-reference/text.md#fielddata-mapping-param) can be [expensive against CPU usage](/troubleshoot/elasticsearch/high-cpu-usage.md). By default, field data is computed at search time but can be [eager loaded](elasticsearch://reference/elasticsearch/mapping-reference/eager-global-ordinals.md) to compute after ingestion. 

Computed field data is loaded into JVM from disk based on usage frequency. Field data can consume JVM up to the lower value between [field data cache setting](elasticsearch://reference/elasticsearch/configuration-reference/field-data-cache-settings.md) and [field data circuit breaker](elasticsearch://reference/elasticsearch/configuration-reference/circuit-breaker-settings.md). [Circuit breakers](/troubleshoot/elasticsearch/circuit-breaker-errors.md) would report as [rejected requests](/troubleshoot/elasticsearch/rejected-requests.md#check-circuit-breakers). Setting `indices.fielddata.cache.size` too low would lead to thrashing inducing surging evictions. 

To check `fielddata` evictions as well as see if it is a major contributor to JVM usage, refer to the [cat nodes API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes):

```console
GET _cat/nodes?v=true&h=name,heap.*,fielddata.*
```

If field data reports as a significant contributor to JVM usage, use the [cat fielddata API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-fielddata) to determine which fields are using field data and how much per node.

```console
GET _cat/fielddata?v=true&s=size:desc
```

You can use the [clear cache API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-clear-cache) to temporarily reset the field data JVM usage. For example:

* To clear the fielddata cache only for fields `fieldname1` and `fieldname2` on the `my-index-000001` index

  ```console
  POST my-index-000001/_cache/clear?fielddata=true&fields=fieldname1,fieldname2
  ```

* To clear any fielddata cache across all indices

  ```console
  POST */_cache/clear?fielddata=true&expand_wildcards=all&ignore_unavailable=true
  ```

The most common reasons for field data JVM usage include when you:

* Enable [`fielddata` on `text` fields](elasticsearch://reference/elasticsearch/mapping-reference/text.md#enable-fielddata-text-fields). Normally instead you should use a [multi-field](elasticsearch://reference/elasticsearch/mapping-reference/multi-fields.md) and search against the [keyword field](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md).
* Either [aggregate](/explore-analyze/query-filter/aggregations.md) or [sort](elasticsearch://reference/elasticsearch/rest-apis/sort-search-results.md) on high cardinality fields which have computed [global ordinals](elasticsearch://reference/elasticsearch/mapping-reference/eager-global-ordinals.md#_what_are_global_ordinals). For example, this can occur from {{kib}} autocomplete of `non-text` fields or loading [visualizations](/explore-analyze/visualize/visualize-library.md). Refer to [avoiding global ordinal loading](elasticsearch://reference/elasticsearch/mapping-reference/eager-global-ordinals.md#_avoiding_global_ordinal_loading) for guidance.
