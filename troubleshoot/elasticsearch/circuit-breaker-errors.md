---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/circuit-breaker-errors.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Circuit breaker errors [circuit-breaker-errors]

{{es}} uses [circuit breakers](elasticsearch://reference/elasticsearch/configuration-reference/circuit-breaker-settings.md) to prevent nodes from running out of JVM heap memory. If Elasticsearch estimates an operation would exceed a circuit breaker, it stops the operation and returns an error.

By default, the [parent circuit breaker](elasticsearch://reference/elasticsearch/configuration-reference/circuit-breaker-settings.md#parent-circuit-breaker) triggers at 95% JVM memory usage. To prevent errors, we recommend taking steps to reduce memory pressure if usage consistently exceeds 85%.

See [this video](https://www.youtube.com/watch?v=k3wYlRVbMSw) for a walkthrough of diagnosing circuit breaker errors.

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::



## Diagnose circuit breaker errors [diagnose-circuit-breaker-errors]

**Error messages**

A circuit breaker trips to prevent a request from executing in order to protect the node's stability. When a request triggers a circuit breaker, {{es}} [rejects the request](/troubleshoot/elasticsearch/rejected-requests.md) with a `429` HTTP status code error.

```js
{
  'error': {
    'type': 'circuit_breaking_exception',
    'reason': '[parent] Data too large, data for [<http_request>] would be [123848638/118.1mb], which is larger than the limit of [123273216/117.5mb], real usage: [120182112/114.6mb], new bytes reserved: [3666526/3.4mb]',
    'bytes_wanted': 123848638,
    'bytes_limit': 123273216,
    'durability': 'TRANSIENT'
  },
  'status': 429
}
```

{{es}} also writes circuit breaker errors to [`elasticsearch.log`](../../deploy-manage/monitor/logging-configuration/elasticsearch-log4j-configuration-self-managed.md). This is helpful when automated processes, such as allocation, trigger a circuit breaker.

```txt
Caused by: org.elasticsearch.common.breaker.CircuitBreakingException: [parent] Data too large, data for [<transport_request>] would be [num/numGB], which is larger than the limit of [num/numGB], usages [request=0/0b, fielddata=num/numKB, in_flight_requests=num/numGB, accounting=num/numGB]
```

**Check circuit breaker statistics**

To get statistics about the circuit breaker per node. Use one of the following:

::::{applies-switch}

:::{applies-item} { "stack": "ga" }
Use the [get node statistics](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats) API:

```console
GET _nodes/stats?filter_path=nodes.*.breakers
```
:::

:::{applies-item} { "stack": "ga 9.3" }
Use the [get circuit breakers statistics](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-circuit-breaker) API:
```console
GET /_cat/circuit_breaker/
```
:::

::::

The response provides the following information:
- Estimated memory used for the operation.
- Memmory limit for the circuit breaker.
- Total number of times the circuit breaker has been triggered and prevented an out of memory error since node uptime.
- And an overhead which is a constant that all estimates for the circuit breaker are multiplied with to calculate a final estimate.

**Check JVM memory usage**

If you’ve enabled Stack Monitoring, you can view JVM memory usage in {{kib}}. In the main menu, click **Stack Monitoring**. On the Stack Monitoring **Overview** page, click **Nodes**. The **JVM Heap** column lists the current memory usage for each node.

You can also use the [cat nodes API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes) to get the current `heap.percent` for each node.

```console
GET _cat/nodes?v=true&h=name,node*,heap*
```

To get the JVM memory usage for each circuit breaker, use the [node stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats).

```console
GET _nodes/stats/breaker
```


## Prevent circuit breaker errors [prevent-circuit-breaker-errors]

**Reduce JVM memory pressure**

High JVM memory pressure often causes circuit breaker errors. See [High JVM memory pressure](high-jvm-memory-pressure.md).

**Avoid using fielddata on `text` fields**

For high-cardinality `text` fields, fielddata can use a large amount of JVM memory. To avoid this, {{es}} disables fielddata on `text` fields by default. If you’ve enabled fielddata and triggered the [fielddata circuit breaker](elasticsearch://reference/elasticsearch/configuration-reference/circuit-breaker-settings.md#fielddata-circuit-breaker), consider disabling it and using a `keyword` field instead. See [`fielddata` mapping parameter](elasticsearch://reference/elasticsearch/mapping-reference/text.md#fielddata-mapping-param).

**Clear the fielddata cache**

If you’ve triggered the fielddata circuit breaker and can’t disable fielddata, use the [clear cache API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-clear-cache) to clear the fielddata cache. This may disrupt any in-flight searches that use fielddata.

```console
POST _cache/clear?fielddata=true
```

## Memory evaluation

Circuit breakers may either directly evaluate memory usage estimates or indirectly limit operations that are likely to cause excessive memory consumption. For example, the `script` circuit breaker checks memory indirectly by rate-limiting Painless/Mustache script compilations. However, even with circuit breakers in place, nodes can still encounter out-of-memory (OOM) conditions. This can occur, for example, because:

- Circuit breaker relies on point-in-time memory usage estimations.
- Parallel operations may still heap DOS-attack the node even with `parent` circuit breakers.
- Certain dynamic operations can quickly consume substantial memory. For example [aggregations](/explore-analyze/query-filter/aggregations.md) and [complex queries](elasticsearch://reference/query-languages/query-dsl/compound-queries.md).
Circuit breakers protect the node's JVM heap. OOM can still trigger due to non-heap memory, for example within the compilation or thread stacks.

