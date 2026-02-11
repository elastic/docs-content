---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/rejected-requests.html
applies_to:
  stack:
  serverless: ga
products:
  - id: elasticsearch
---

# Rejected requests [rejected-requests]

When {{es}} rejects a request, it stops the operation and returns an HTTP `429` response code for a `TOO_MANY_REQUESTS` error. The returned HTTP response body includes information on why the operation was rejected. You can retry HTTP `429` errors, but it's generally best to implement [exponential backoff](https://en.wikipedia.org/wiki/Exponential_backoff) to avoid exacerbating performance issues.

## Check rejected tasks [check-rejected-tasks]

Rejected requests are frequently caused by depleted resources. The most common of these are described here.

### Review thread pools [check-threadpools]

To check the number of rejected tasks for each thread pool, use the [cat thread pool API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-thread-pool):

```console
GET /_cat/thread_pool?v=true&h=id,name,queue,active,rejected,completed
```

A high ratio of `rejected` to `completed` tasks, particularly in the `search` and `write` thread pools, indicates that {{es}} regularly rejects requests.

The following examples demonstrate typical `queue capacity` errors.

* The API response body returns an `es_rejected_execution_exception` error:

   ```json
   {
      "shard" : 0,
      "node" : "XXXX",
      "reason" : {
         "reason" : "rejected execution of org.elasticsearch.common.util.concurrent.TimedRunnable@26c03d4a on QueueResizingEsThreadPoolExecutor[name = XXXXX/search, queue capacity = 1000, min queue capacity = 1000, max queue capacity = 1000, frame size = 2000, targeted response rate = 1s, task execution EWMA = 968.1ms, adjustment amount = 50, org.elasticsearch.common.util.concurrent.QueueResizingEsThreadPoolExecutor@70be0765[Running, pool size = 25, active threads = 25, queued tasks = 1000, completed tasks = 616499351]]",
         "type" : "es_rejected_execution_exception"
      },
      "index" : "my-index-000001"
   }
   ```
   
* The error log returns an `EsRejectedExecutionException` error:

    ```
    Caused by: org.elasticsearch.common.util.concurrent.EsRejectedExecutionException: rejected execution of org.elasticsearch.common.util.concurrent.TimedRunnable@1a25fe82 on QueueResizingEsThreadPoolExecutor[name = XXXXX/search, queue capacity = 1000, min queue capacity = 1000, max queue capacity = 1000, frame size = 2000, targeted response rate = 1s, task execution EWMA = 10.7ms, adjustment amount = 50, org.elasticsearch.common.util.concurrent.QueueResizingEsThreadPoolExecutor@6312a0bb[Running, pool size = 25, active threads = 25, queued tasks = 1000, completed tasks = 616499351]]
    ```

To troubleshoot ongoing thread pool rejection errors, check [task queue backlog due to thread pool](task-queue-backlog.md#diagnose-task-queue-thread-pool). Refer to the [Threadpool Rejections video](https://www.youtube.com/watch?v=auZJRXoAVpI) for a troubleshooting walkthrough.

## Inspect circuit breakers [check-circuit-breakers]

To check the number of tripped [circuit breakers](elasticsearch://reference/elasticsearch/configuration-reference/circuit-breaker-settings.md), use the [node stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats).

```console
GET /_nodes/stats/breaker
```

These statistics are cumulative from node startup. For more information, see [circuit breaker errors](circuit-breaker-errors.md).

Refer to the [Circuit Breaker Error video](https://www.youtube.com/watch?v=k3wYlRVbMSw) for a troubleshooting walkthrough.

## Analyze indexing pressure [check-indexing-pressure]

{{es}} reserves part of its JVM for indexing. An error can occur if heap usage exceeds the [`indexing_pressure.memory.limit` setting](elasticsearch://reference/elasticsearch/index-settings/pressure.md#memory-limits). To check the number of [indexing pressure](elasticsearch://reference/elasticsearch/index-settings/pressure.md) rejections, use the [node stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats).

```console
GET _nodes/stats?human&filter_path=nodes.*.indexing_pressure
```

These statistics are cumulative from node startup.

The following examples demonstrate indexing pressure rejections.

* The API response body returns an `es_rejected_execution_exception` error:

    ```json
    {
      "error" : {
        "root_cause" : [
          {
            "type" : "es_rejected_execution_exception",
            "reason" : "rejected execution of primary operation [coordinating_and_primary_bytes=XXXXX, replica_bytes=XXXXX, all_bytes=XXXXX, coordinating_operation_bytes=XXXXX, max_coordinating_and_primary_bytes=XXXXX]"
          }
        ],
        "type" : "es_rejected_execution_exception",
        "reason" : "rejected execution of coordinating operation [coordinating_and_primary_bytes=XXXXX, replica_bytes=XXXXX, all_bytes=XXXXX, coordinating_operation_bytes=XXXXX, max_coordinating_and_primary_bytes=XXXXX]"
      },
      "status" : 429
    }
    ```

* The error log returns an `EsRejectedExecutionException` error:

    ```
    Caused by: org.elasticsearch.common.util.concurrent.EsRejectedExecutionException: rejected execution of primary operation [coordinating_and_primary_bytes=XXXXX, replica_bytes=XXXXX, all_bytes=XXXXX, coordinating_operation_bytes=XXXXX, max_coordinating_and_primary_bytes=XXXXX]
    ```

As part of the [Reading and writing documents](/deploy-manage/distributed-architecture/reading-and-writing-documents.md) outlined models, the portion of the error `rejected execution of <category> operation` reports one of the following categories: `combined_coordinating_and_primary`, `coordinating`, `primary`, or `replica`.

These errors are often related to:

* The quantity of [backlogged tasks](task-queue-backlog.md).
* The value of [Bulk index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) is set to too large of a size.
* Large search response sizes.
* Use of the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type, which can cause rejections when indexing large batches of documents if the batch may otherwise incur an Out of Memory (OOM) error. {applies_to}`stack: ga 9.1`{applies_to}`serverless: ga`

Refer to the [Index Pressure Rejections video](https://www.youtube.com/watch?v=QuV8QqSfc0c) for a troubleshooting walkthrough.

## Prevent rejected requests [prevent-rejected-requests]

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::

### Fix high CPU and memory usage [fix-high-cpu-memory-usage]

If {{es}} regularly rejects requests and other tasks, your cluster likely has high CPU usage or high JVM memory pressure. For tips, refer to [High CPU usage](high-cpu-usage.md) and [High JVM memory pressure](high-jvm-memory-pressure.md).

### Fix for `semantic_text` ingestion issues [fix-semantic-text-ingestion-issues]
```{applies_to}
stack: ga 9.1
serverless: ga
```
When bulk indexing documents with the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type, you might encounter rejections due to high memory usage during inference processing. These rejections appear as an `InferenceException` in your cluster logs.

To resolve this issue:

1. Reduce the batch size of documents in your indexing requests.
2. If reducing batch size doesn't resolve the issue, then consider scaling up your machine resources.
3. {applies_to}`serverless: unavailable` A last resort option is to adjust the `indexing_pressure.memory.coordinating.limit` cluster setting. The default value is 10% of the heap. Increasing this limit allows more memory to be used for coordinating operations before rejections occur.

  ::::{warning}
  This adjustment should only be considered after exhausting other options, as setting this value too high may risk Out of Memory (OOM) errors in your cluster. A cluster restart is required for this change to take effect.
  ::::
