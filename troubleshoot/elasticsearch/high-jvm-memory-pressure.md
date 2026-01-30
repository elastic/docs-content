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

### Field data related JVM pressure issues [reduce-jvm-memory-pressure-fielddata]

This section describes how [field data mapping](elasticsearch://reference/elasticsearch/mapping-reference/text.md#fielddata-mapping-param) and [global ordinal mapping](elasticsearch://reference/elasticsearch/mapping-reference/eager-global-ordinals.md) can contribute to JVM memory pressure and how to mitigate their impact.

#### Why field data is problematic [reduce-jvm-memory-pressure-fielddata-problematic]

* Loading field data in memory can consume significant memory.
* The field data is consumed at search time so it primarily affects cluster performance during search execution on specific fields (except if `eager_global_ordinals` are enabled - which does not reduce the memory usage, but  moves the generation of global ordinals at indexing time instead of search time)
* As `fielddata` and `global ordinals` are expensive to be built, they're kept in the JVM heap, in the [field data cache settings](elasticsearch://reference/elasticsearch/configuration-reference/field-data-cache-settings.md). By default, it's unbounded. Limiting the cache with `indices.fielddata.cache.size` would lead to possible thrashing (if the queries really need the `fielddata` continuously, the cluster will be continuously generating and thrashing the results, leading to worse performance) and this will be visible in `fielddata` evictions in the Nodes stats APIs.

#### Identify high field data cache usage [reduce-jvm-memory-pressure-fielddata-cache-usage]

Field data is primarily loaded into heap in the following scenarios when you:

* [Explicitly enable `fielddata` on `text` fields](elasticsearch://reference/elasticsearch/mapping-reference/text.md#enable-fielddata-text-fields)
* Use [global ordinals](elasticsearch://reference/elasticsearch/mapping-reference/eager-global-ordinals.md#_what_are_global_ordinals) by aggregating and sorting on `keyword`, `ip`, and `flattened` fields with high cardinality of values.

Common symptoms of high field data usage include:

* Nodes using high amounts of JVM Heap
  * Possible `OutOfMemory` exceptions (the node crashes or stops)
  * Possible [CircuitBreaker exceptions related to fielddata](elasticsearch://reference/elasticsearch/configuration-reference/circuit-breaker-settings.md#fielddata-circuit-breaker) (the request will be not fulfilled)
  * High GC activity on the nodes storing the shards of the indices affected (both in terms of frequency and duration)
* Performance issues due to time and resources needed to generate the field data (usually affects the CPU)

To understand whether field data is a major contributor to memory pressure, compare it with total heap usage:

```console
GET /_nodes/stats/jvm,indices/fielddata?filter_path=nodes.*.name,nodes.*.jvm.mem.heap_used_in_bytes,nodes.*.jvm.mem.heap_max_in_bytes,nodes.*.indices.fielddata.memory_size_in_bytes
```
If field data accounts for a significant percentage of heap usage, for example more than 10-20% on hot nodes, it is likely contributing to memory pressure.

Use the [cat fielddata API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-fielddata) to find which fields are using field data and how much per node.

#### Reduce field data usage [reduce-jvm-memory-pressure-fielddata-reduce-usage]

##### Field data on `text` fields [reduce-jvm-memory-pressure-fielddata-on-text]

In rare cases, `text` fields with `fielddata: true` enabled can load large amounts of data into the JVM heap and should be avoided unless strictly required.

Avoid enabling `fielddata: true` on `text` fields. If aggregations or sorting are required, use multi-fields (`text` + `keyword`) and aggregate only on `.keyword` fields.

##### Workaround: clear the field data cache [reduce-jvm-memory-pressure-fielddata-clear-cache]

You can clear the cache for specific fields or for all the fields.

:::{important}
Clearing the field data cache frees the memory used by field data temporarily, until a query re-triggers its generation. It might generate performance issues if the field data was actively used.
::: 

Examples:

* `POST <index name>/_cache/clear?fielddata=true&fields=fieldname1,fieldname2` to clear the fielddata cache only for fields `fieldname1` and `fieldname2` on the `<index name>` index
* `POST */_cache/clear?fielddata=true` to clear any fielddata cache entry on all indices

##### Field data generated by `keyword` fields (global ordinals) [reduce-jvm-memory-pressure-fielddata-global-ordinals]

If the field which is using field data is a `keyword` field, it is likely that queries are aggregating and/or sorting on this field and the field has a high cardinality.

The aggregation or sorting on high cardinality keyword fields can happen:

* directly, when a user creates a visualization, dashboard, or query which explicitly aggregates on this field
* indirectly, when the Kibana autocomplete feature in KQL runs aggregations behind the scenes to offer autocomplete on `non-text` fields

In order to avoid global ordinals, follow [the guidance in our documentation](elasticsearch://reference/elasticsearch/mapping-reference/eager-global-ordinals.md#_avoiding_global_ordinal_loading).

In general:
* If the high cardinality field contains only `numeric` values, map the field as a `numeric` type since numeric fields don't require global ordinals being generated. You'd need to reindexed the index with the new mapping.
* If the index is not being written to, force merging the index to 1 segment will prevent global ordinals from being generated because the field will be sorted in the segment. This can be enforced in the ILM policy after a rollover or in the warm phase of your data streams).
