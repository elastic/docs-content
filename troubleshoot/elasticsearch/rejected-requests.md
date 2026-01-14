---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/rejected-requests.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Rejected requests [rejected-requests]

When {{es}} rejects a request, it stops the operation and returns an error with a `429` response code. Rejected requests are commonly caused by:

* A [depleted thread pool](high-cpu-usage.md). A depleted `search` or `write` thread pool returns a `TOO_MANY_REQUESTS` error message.
* A [circuit breaker error](circuit-breaker-errors.md).
* High [indexing pressure](elasticsearch://reference/elasticsearch/index-settings/pressure.md) that exceeds the [`indexing_pressure.memory.limit`](elasticsearch://reference/elasticsearch/index-settings/pressure.md#memory-limits).

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::



## Check rejected tasks [check-rejected-tasks]

To check the number of rejected tasks for each thread pool, use the [cat thread pool API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-thread-pool). A high ratio of `rejected` to `completed` tasks, particularly in the `search` and `write` thread pools, means {{es}} regularly rejects requests.

```console
GET /_cat/thread_pool?v=true&h=id,name,queue,active,rejected,completed
```

`write` thread pool rejections frequently appear in the erring API and correlating log as `EsRejectedExecutionException` with either `QueueResizingEsThreadPoolExecutor` or `queue capacity`.

The `queue` and `active` pools are point-in-time values. `rejected` and `completed` are cumulative counters on each node that reset when the node process restarts. Therefore, avoid interpreting a single snapshot “rejected/completed ratio” in isolation — compare deltas over a time window (e.g., sample every 1–5 minutes and calculate the increase in `rejected` vs the increase in `completed`). Sustained non-zero `rejected` deltas indicate ongoing request drops (typically surfaced to clients as HTTP 429).

These errors are often related to [backlogged tasks](task-queue-backlog.md). See [this video](https://www.youtube.com/watch?v=auZJRXoAVpI) for a walkthrough of troubleshooting threadpool rejections.

Example 1 - Queue building (backlog), but still no rejections
```
node_name  name   active queue rejected completed
es-02      search 13     240   0        90112
es-02      write  2      35    0        51003
```
Requests are arriving faster than workers can drain them (queue > 0). If it’s transient, it may be fine; if it persists/grows, it commonly precedes rejects.

Example 2 — Rejections happening (queue at/near limit)
```
node_name  name   active queue rejected completed
es-02      search 13     1000  842      90510
```
The queue is saturated, and new work is being rejected (`rejected` increasing). Clients typically see HTTP 429 for those rejected requests.


## Check circuit breakers [check-circuit-breakers]

To check the number of tripped [circuit breakers](elasticsearch://reference/elasticsearch/configuration-reference/circuit-breaker-settings.md), use the [node stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats).

```console
GET /_nodes/stats/breaker
```

These statistics are cumulative from node startup. For more information, see [circuit breaker errors](circuit-breaker-errors.md).

See [this video](https://www.youtube.com/watch?v=k3wYlRVbMSw) for a walkthrough of diagnosing circuit breaker errors.


## Check indexing pressure [check-indexing-pressure]

To check the number of [indexing pressure](elasticsearch://reference/elasticsearch/index-settings/pressure.md) rejections, use the [node stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats).

```console
GET _nodes/stats?human&filter_path=nodes.*.indexing_pressure
```

These stats are cumulative from node startup.

Indexing pressure rejections appear as an `EsRejectedExecutionException`, and indicate that they were rejected due to `combined_coordinating_and_primary`, `coordinating`, `primary`, or `replica`.

These errors are often related to [backlogged tasks](task-queue-backlog.md), [bulk index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) sizing, or the ingest target's [`refresh_interval` setting](elasticsearch://reference/elasticsearch/index-settings/index-modules.md).  

::::{note}
{applies_to}`stack: ga 9.1`{applies_to}`serverless: ga`
Another cause of indexing pressure rejections might be the use of the [`semantic_text`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-text) field type, which can cause rejections when indexing large batches of documents if the batch may otherwise incur an Out of Memory (OOM) error.
::::  

See [this video](https://www.youtube.com/watch?v=QuV8QqSfc0c) for a walkthrough of diagnosing indexing pressure rejections.


## Prevent rejected requests [prevent-rejected-requests]

### Fix high CPU and memory usage [fix-high-cpu-memory-usage]

If {{es}} regularly rejects requests and other tasks, your cluster likely has high CPU usage or high JVM memory pressure. For tips, see [High CPU usage](high-cpu-usage.md) and [High JVM memory pressure](high-jvm-memory-pressure.md).

### Fix indexing/search request bursts and concurrency (HTTP 429)

Rejections (HTTP 429) typically indicate the cluster is receiving work faster than it can execute (for example, during traffic bursts or when indexing/search requests are not optimized). Prevent them by shaping workload—use client-side backoff/throttling for bursts and tune request patterns (bulk sizing, concurrency, query cost) to match the cluster’s sustained throughput.

### Fix for `semantic_text` ingestion issues [fix-semantic-text-ingestion-issues]
```{applies_to}
stack: ga 9.1
serverless: ga
```
When bulk indexing documents with the `semantic_text` field type, you may encounter rejections due to high memory usage during inference processing. 
These rejections will appear as an `InferenceException` in your cluster logs.

**To resolve this issue:**

1. Reduce the batch size of documents in your indexing requests.
2. If reducing batch size doesn't resolve the issue, then consider scaling up your machine resources.
3. {applies_to}`serverless: unavailable` A last resort option is to adjust the `indexing_pressure.memory.coordinating.limit` cluster setting. The default value is 10% of the heap. Increasing this limit allows more memory to be used for coordinating operations before rejections occur. 
::::{warning}
This adjustment should only be considered after exhausting other options, as setting this value too high may risk Out of Memory (OOM) errors in your cluster. A cluster restart is required for this change to take effect.
::::
