---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/rejected-requests.html
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

# Rejected requests [rejected-requests]

When {{es}} rejects a request, it stops the operation and returns an error with a `429` response code. Rejected requests are commonly caused by:

* A [depleted thread pool](high-cpu-usage.md). A depleted `search` or `write` thread pool returns a `TOO_MANY_REQUESTS` error message.
* A [circuit breaker error](circuit-breaker-errors.md).
* High [indexing pressure](elasticsearch://reference/elasticsearch/index-settings/pressure.md) that exceeds the [`indexing_pressure.memory.limit`](elasticsearch://reference/elasticsearch/index-settings/pressure.md#memory-limits).

::::{tip}
If you're using Elastic Cloud Hosted, then you can use AutoOps to monitor your cluster. AutoOps significantly simplifies cluster management with performance recommendations, resource utilization visibility, and real-time issue detection with resolution paths. For more information, refer to [Monitor with AutoOps](/deploy-manage/monitor/autoops.md).

::::



## Check rejected tasks [check-rejected-tasks]

To check the number of rejected tasks for each thread pool, use the [cat thread pool API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-thread-pool). A high ratio of `rejected` to `completed` tasks, particularly in the `search` and `write` thread pools, means {{es}} regularly rejects requests.

```console
GET /_cat/thread_pool?v=true&h=id,name,queue,active,rejected,completed
```

`write` thread pool rejections frequently appear in the erring API and correlating log as `EsRejectedExecutionException` with either `QueueResizingEsThreadPoolExecutor` or `queue capacity`.

These errors are often related to [backlogged tasks](task-queue-backlog.md).

See [this video](https://www.youtube.com/watch?v=auZJRXoAVpI) for a walkthrough of troubleshooting threadpool rejections.


## Check circuit breakers [check-circuit-breakers]

To check the number of tripped [circuit breakers](elasticsearch://reference/elasticsearch/configuration-reference/circuit-breaker-settings.md), use the [node stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats).

```console
GET /_nodes/stats/breaker
```

These statistics are cumulative from node startup. For more information, see [circuit breaker errors](elasticsearch://reference/elasticsearch/configuration-reference/circuit-breaker-settings.md).

See [this video](https://www.youtube.com/watch?v=k3wYlRVbMSw) for a walkthrough of diagnosing circuit breaker errors.


## Check indexing pressure [check-indexing-pressure]

To check the number of [indexing pressure](elasticsearch://reference/elasticsearch/index-settings/pressure.md) rejections, use the [node stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats).

```console
GET _nodes/stats?human&filter_path=nodes.*.indexing_pressure
```

These stats are cumulative from node startup.

Indexing pressure rejections appear as an `EsRejectedExecutionException`, and indicate that they were rejected due to `combined_coordinating_and_primary`, `coordinating`, `primary`, or `replica`.

These errors are often related to [backlogged tasks](task-queue-backlog.md), [bulk index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) sizing, or the ingest target's [`refresh_interval` setting](elasticsearch://reference/elasticsearch/index-settings/index-modules.md).¹

¹ : Starting from versions 8.19+ and 9.1+, indexing to a semantic_text field can also cause 429 errors if the batch may otherwise incur an Out Of Memory (OOM) error.

See [this video](https://www.youtube.com/watch?v=QuV8QqSfc0c) for a walkthrough of diagnosing indexing pressure rejections.


## Prevent rejected requests [prevent-rejected-requests]

**Fix high CPU and memory usage**

If {{es}} regularly rejects requests and other tasks, your cluster likely has high CPU usage or high JVM memory pressure. For tips, see [High CPU usage](high-cpu-usage.md) and [High JVM memory pressure](high-jvm-memory-pressure.md).

**Fix for semantic_text field issues:**

When working with semantic_text fields in versions 8.19+ and 9.1+:

1. Reduce the batch size of documents in your indexing requests.
2. If reducing batch size doesn't resolve the issue, then consider scaling up your machine resources.
3. A last resort option is to adjust the `indexing_pressure.memory.coordinating.limit` cluster setting. The default value is 10% of the heap. Increasing this limit allows more memory to be used for coordinating operations before rejections occur. This adjustment should only be considered after exhausting other options, as setting this value too high may risk Out of Memory (OOM) errors in your cluster. A cluster restart is required for this change to take effect.