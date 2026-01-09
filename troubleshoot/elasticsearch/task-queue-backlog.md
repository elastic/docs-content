---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/task-queue-backlog.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Task queue backlog [task-queue-backlog]

% **Product:** Elasticsearch<br> **Deployment type:** Elastic Cloud % Enterprise, Elastic Cloud Hosted, Elastic Cloud on Kubernetes, Elastic
% Self-Managed <br> **Versions:** All

A backlogged task queue can prevent tasks from completing and lead to an unhealthy cluster state. Contributing factors include resource constraints, a large number of tasks triggered at once, and long-running tasks.


## Diagnose a backlogged task queue [diagnose-task-queue-backlog] 

To identify the cause of the backlog, try these diagnostic actions.

* [Check the thread pool status](#diagnose-task-queue-thread-pool)
* [Inspect hot threads on each node](#diagnose-task-queue-hot-thread)
* [Identify long-running node tasks](#diagnose-task-queue-long-running-node-tasks)
* [Look for long-running cluster tasks](#diagnose-task-queue-long-running-cluster-tasks)
* [Monitor slow logs](#diagnose-task-slow-logs)


### Check the thread pool status [diagnose-task-queue-thread-pool] 

A [depleted thread pool](high-cpu-usage.md) can result in [rejected requests](rejected-requests.md).

Use the [cat thread pool API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-thread-pool) to monitor active threads, queued tasks, rejections, and completed tasks:

```console
GET /_cat/thread_pool?v&s=t,n&h=type,name,node_name,active,queue,rejected,completed
```

* Look for high `active` and `queue` metrics, which indicate potential bottlenecks and opportunities to [reduce CPU usage](high-cpu-usage.md#reduce-cpu-usage).
* Determine whether thread pool issues are specific to a [data tier](../../manage-data/lifecycle/data-tiers.md).
* Check whether a specific node’s thread pool is depleting faster than others. This might indicate [hot spotting](#resolve-task-queue-backlog-hotspotting).


### Inspect hot threads on each node [diagnose-task-queue-hot-thread] 

If a particular thread pool queue is backed up, periodically poll the [nodes hot threads API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-hot-threads) to gauge the thread’s progression and ensure it has sufficient resources:

```console
GET /_nodes/hot_threads
```

Although the hot threads API response does not list the specific tasks running on a thread, it provides a summary of the thread’s activities. You can correlate a hot threads response with a [task management API response](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-tasks) to identify any overlap with specific tasks. For example, if the hot threads response indicates the thread is `performing a search query`, you can [check for long-running search tasks](#diagnose-task-queue-long-running-node-tasks) using the task management API.


### Identify long-running node tasks [diagnose-task-queue-long-running-node-tasks] 

Long-running tasks can also cause a backlog. Use the [task management API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-tasks) to check for excessive `running_time_in_nanos` values:

```console
GET /_tasks?pretty=true&human=true&detailed=true
```

You can filter on a specific `action`, such as [bulk indexing](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) or search-related tasks. These tend to be long-running.

* Filter on [bulk index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) actions:

    ```console
    GET /_tasks?human&detailed&actions=indices:*write*
    ```

* Filter on search actions:

    ```console
    GET /_tasks?human&detailed&actions=indices:*search*
    ```


Long-running tasks might need to be [canceled](#resolve-task-queue-backlog-stuck-tasks).

See this [this video](https://www.youtube.com/watch?v=lzw6Wla92NY) for a walkthrough of troubleshooting the [task management API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-tasks) output.

### Look for long-running cluster tasks [diagnose-task-queue-long-running-cluster-tasks] 

Use the [cluster pending tasks API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-pending-tasks) to identify delays in cluster state synchronization:

```console
GET /_cluster/pending_tasks
```

Tasks with a high `timeInQueue` value are likely contributing to the backlog and might need to be [canceled](#resolve-task-queue-backlog-stuck-tasks).

### Monitor slow logs [diagnose-task-slow-logs]

If you're not present during an incident to investigate backlogged tasks, you might consider enabling [slow logs](elasticsearch://reference/elasticsearch/index-settings/slow-log.md) to review later.

For example, you can review slow search logs later using the [search profiler](elasticsearch://reference/elasticsearch/rest-apis/search-profile.md), so that time consuming requests can be optimized.

## Recommendations [resolve-task-queue-backlog] 

After identifying problematic threads and tasks, resolve the issue by increasing resources or canceling tasks.


### Increase available resources [resolve-task-queue-backlog-resources] 

If tasks are progressing slowly, try [reducing CPU usage](high-cpu-usage.md#reduce-cpu-usage).

In some cases, you might need to increase the thread pool size. For example, the `force_merge` thread pool defaults to a single thread. Increasing the size to 2 might help reduce a backlog of force merge requests.


### Cancel stuck tasks [resolve-task-queue-backlog-stuck-tasks] 

If an active task’s [hot thread](#diagnose-task-queue-hot-thread) shows no progress, consider [canceling the task](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-tasks#task-cancellation).

For example, you can use the [task management API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-tasks-list) to identify and cancel searches that consume excessive CPU time.

```console
GET _tasks?actions=*search&detailed
```

The response `description` contains the search request and its queries. The `running_time_in_nanos` parameter shows how long the search has been running.

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

To cancel this example search to free up resources, you would run:

```console
POST _tasks/oTUltX4IQMOUUVeiohTt8A:464/_cancel
```

For additional tips on how to track and avoid resource-intensive searches, see [Avoid expensive searches](high-jvm-memory-pressure.md#avoid-expensive-searches).


### Address hot spotting [resolve-task-queue-backlog-hotspotting] 

If a specific node’s thread pool is depleting faster than others, try addressing uneven node resource utilization, also known as hot spotting. For details on actions you can take, such as rebalancing shards, see [Hot spotting](hotspotting.md).


## Resources [_resources] 

Related symptoms:

* [High CPU usage](high-cpu-usage.md)
* [Rejected requests](rejected-requests.md)
* [Hot spotting](hotspotting.md)
* [Troubleshooting overview](/troubleshoot/index.md)
