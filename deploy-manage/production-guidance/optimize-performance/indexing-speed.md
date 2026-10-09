---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-indexing-speed.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Tune for indexing speed [tune-for-indexing-speed]

{{es}} offers a wide range of indexing performance optimizations, which are especially useful for high-throughput ingestion workloads. This page provides practical recommendations to help you maximize indexing speed, from bulk sizing and refresh intervals to hardware and thread management.

This page covers client-side optimizations, which you control through how you send data, and server-side optimizations, which tune the {{es}} infrastructure. In {{serverless-full}}, Elastic manages the infrastructure, so only the client-side optimizations apply.

::::{note}
Indexing performance is also affected by your indexing strategy, including whether you’re indexing into a single index or hundreds in parallel.

{applies_to}`stack: ga` Your sharding strategy also matters. How many shards each index has, your cluster’s shard count, and overall data distribution can significantly influence indexing speed. Refer to [](./size-shards.md) for more details about sharding strategies and recommendations.
::::

## Client-side optimizations [client-side-optimizations]

These optimizations depend on how you send data to and configure indexing in {{es}}. They apply to all deployment types, including {{serverless-full}}, unless a section says otherwise.

### Use bulk requests [_use_bulk_requests]

Bulk requests will yield much better performance than single-document index requests. In order to know the optimal size of a bulk request, you should run a benchmark on a single node with a single shard. First try to index 100 documents at once, then 200, then 400, etc. doubling the number of documents in a bulk request in every benchmark run. When the indexing speed starts to plateau then you know you reached the optimal size of a bulk request for your data. In case of tie, it is better to err in the direction of too few rather than too many documents. Beware that too large bulk requests might put the cluster under memory pressure when many of them are sent concurrently, so it is advisable to avoid going beyond a couple tens of megabytes per request even if larger requests seem to perform better.

:::{note}
In {{serverless-full}}, the minimum response time for a single bulk indexing request is 200ms.
:::

### Tune bulk request size for large indexing jobs [tune-bulk-request-size]
```{applies_to}
serverless: ga
```

For large indexing or reindexing operations, aim to keep each bulk request around 4 MB. This helps stay well below the overall concurrent bulk indexing limit of about 100 MB.

As a starting point, use these batch sizes based on average document size:

| Document size | Recommended batch size |
|---|---|
| ~1 KB | 4,000 documents |
| ~4 KB | 1,000 documents |

Adjust proportionally for other document sizes. There is no one-size-fits-all setting. Test different batch sizes and thread counts to find the optimal configuration for your workload.

### Use multiple workers/threads to send data to {{es}} [multiple-workers-threads]

A single thread sending bulk requests is unlikely to be able to max out the indexing capacity of an {{es}} cluster. In order to use all resources of the cluster, you should send data from multiple threads or processes. In addition to making better use of the resources of the cluster, this should help reduce the cost of each fsync.

On the other hand, sending data to a single shard from too many concurrent threads or processes can overwhelm the cluster. If the indexing load exceeds what {{es}} can handle, it may become a bottleneck and start rejecting requests or slowing down overall performance.

Make sure to watch for `TOO_MANY_REQUESTS (429)` response codes (`EsRejectedExecutionException` with the Java client), which is the way that {{es}} tells you that it cannot keep up with the current indexing rate. When it happens, you should pause indexing a bit before trying again, ideally with randomized exponential backoff.

Similarly to sizing bulk requests, only testing can tell what the optimal number of workers is. This can be tested by progressively increasing the number of workers until either I/O or CPU is saturated on the cluster.

:::{note}
In {{serverless-full}}, avoid starting your client at maximum parallelism. Instead, increase the number of client threads or workers in steps, for example 1, 2, 4, 8, 16, 32, while monitoring throughput and error rates. {{serverless-full}} scales resources automatically in response to demand, and sudden large spikes can cause temporary backpressure or transient errors while scaling catches up. A gradual ramp-up allows the platform to scale more efficiently and can result in faster overall job completion. For large-scale operations, doubling throughput approximately every 30 minutes is a reasonable starting point. Optimal settings vary by workload.
:::

### Use resiliency patterns [use-resiliency-patterns]

Configure your clients with timeouts, and retry transient errors with exponential backoff as described for `429` responses in [Use multiple workers/threads](#multiple-workers-threads). These patterns are essential for any distributed data store. They are particularly important in {{serverless-full}}, where automated scaling, maintenance, and software updates can occasionally cause transient failures or increased latency.

Focus on the end-to-end success rate rather than raw error counts alone. Many transient errors resolve on retry, so the final outcome of each request is often a more meaningful indicator of application health than the number of individual errors.

### Unset or increase the refresh interval [_unset_or_increase_the_refresh_interval]

The operation that consists of making changes visible to search - called a [refresh]({{es-apis}}operation/operation-indices-refresh) - is costly, and calling it often while there is ongoing indexing activity can hurt indexing speed.

By default, {{es}} periodically refreshes indices every second, but only on indices that have received one search request or more in the last 30 seconds.

This is the optimal configuration if you have no or very little search traffic (e.g. less than one search request every 5 minutes) and want to optimize for indexing speed. This behavior aims to automatically optimize bulk indexing in the default case when no searches are performed. In order to opt out of this behavior set the refresh interval explicitly.

On the other hand, if your index experiences regular search requests, this default behavior means that {{es}} will refresh your index every 1 second. If you can afford to increase the amount of time between when a document gets indexed and when it becomes visible, increasing the [`index.refresh_interval`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-refresh-interval-setting) to a larger value, e.g. `30s`, might help improve indexing speed.

#### Disable refresh interval

To maximize indexing performance during large bulk operations, you can disable refreshing by setting the refresh interval to `-1`. This prevents {{es}} from performing any refreshes during the bulk indexing process.

To disable the refresh interval, run the following request:

```console
PUT /my-index-000001/_settings
{
  "index" : {
    "refresh_interval" : "-1"
  }
}
```
% TEST[setup:my_index]

While refresh is disabled, your newly indexed documents will not be visible to search operations. Only re-enable refreshing after your bulk indexing is complete and you need the data to be searchable.

To restore the refresh interval, run the following request with your desired value:

```console
PUT /my-index-000001/_settings
{
  "index" : {
    "refresh_interval" : "5s" <1>
  }
}
```
% TEST[continued]


1. For {{serverless-full}} deployments, `refresh_interval` must be either `-1`, or equal to or greater than `5s`

When bulk indexing is complete, consider running a [force merge]({{es-apis}}operation/operation-indices-forcemerge) to optimize search performance. Force merging is not available on {{serverless-full}}.

```console
POST /my-index-000001/_forcemerge?max_num_segments=5
```
% TEST[continued]

::::{warning}
Force merge is an expensive operation.
::::

### Use auto-generated ids [_use_auto_generated_ids]

When indexing a document that has an explicit id, {{es}} needs to check whether a document with the same id already exists within the same shard, which is a costly operation and gets even more costly as the index grows. By using auto-generated ids, {{es}} can skip this check, which makes indexing faster.

### Batch small writes [batch-small-writes]
```{applies_to}
serverless: ga
```

In {{serverless-full}}, there is a 15-minute cooldown before the platform can scale down the resources it uses for indexing. If you send frequent, small writes instead of batching your requests, each write extends the cooldown, so the platform can't scale down. Batch your writes where possible.

## Server-side optimizations [server-side-optimizations]

::::{note}
In {{serverless-full}}, Elastic manages infrastructure-level details such as hardware, storage, memory, and replication, so the optimizations in this section don't apply.
::::

### Disable replicas for initial loads [_disable_replicas_for_initial_loads]
```{applies_to}
stack: ga
```

If you have a large amount of data that you want to load all at once into {{es}}, it may be beneficial to set `index.number_of_replicas` to `0` in order to speed up indexing. Having no replicas means that losing a single node may incur data loss, so it is important that the data lives elsewhere so that this initial load can be retried in case of an issue. Once the initial load is finished, you can set `index.number_of_replicas` back to its original value.

If `index.refresh_interval` is configured in the index settings, it may further help to unset it during this initial load and setting it back to its original value once the initial load is finished.

### Disable swapping [_disable_swapping_2]
```{applies_to}
deployment:
  self: ga
```
You should make sure that the operating system is not swapping out the java process by [disabling swapping](../../deploy/self-managed/setup-configuration-memory.md).

### Give memory to the filesystem cache [_give_memory_to_the_filesystem_cache]
```{applies_to}
deployment:
  self: ga
  eck: ga
```

The filesystem cache is used to buffer I/O operations and plays a critical role in {{es}} performance. You should make sure to give at least half of the system's memory to the filesystem cache.

By default, {{es}} automatically sets its [JVM heap size](/deploy-manage/deploy/self-managed/important-settings-configuration.md#heap-size-settings) to follow this best practice. However, in self-managed or {{eck}} deployments, you have the flexibility to allocate even more memory to the filesystem cache.

While the filesystem cache primarily benefits search workloads, it can also improve indexing speed in certain scenarios, especially when indexing into many shards or performing frequent segment merges that involve reading existing data.

::::{note}
On Linux, the filesystem cache uses any memory not actively used by applications. To allocate memory to the cache, ensure that enough system memory remains available and is not consumed by {{es}} or other processes. 
::::

### Use faster hardware [indexing-use-faster-hardware]
```{applies_to}
stack: ga
```

If indexing is I/O-bound, consider increasing the size of the filesystem cache (see above) or using faster storage. {{es}} generally creates individual files with sequential writes. However, indexing involves writing multiple files concurrently, and a mix of random and sequential reads too, so SSD drives tend to perform better than spinning disks.

Stripe your index across multiple SSDs by configuring a RAID 0 array. Remember that it will increase the risk of failure since the failure of any one SSD destroys the index. However this is typically the right tradeoff to make: optimize single shards for maximum performance, and then add replicas across different nodes so there’s redundancy for any node failures. You can also use [snapshot and restore](../../tools/snapshot-and-restore.md) to backup the index for further insurance.

::::{note}
In {{ech}} and {{ece}}, you can choose the underlying hardware by selecting different hardware profiles or deployment templates. Refer to [ECH > Manage hardware profiles](/deploy-manage/deploy/elastic-cloud/ec-change-hardware-profile.md) and [ECE > Manage deployment templates](/deploy-manage/deploy/cloud-enterprise/configure-deployment-templates.md) for more details.
::::

#### Local vs. remote storage [_local_vs_remote_storage]
```{applies_to}
deployment:
  self: ga
  eck: ga
  ece: ga
```

{{es}} clusters using directly-attached (local) storage generally perform better than those using remote storage. Direct storage typically provides lower latency for I/O operations, which is more critical for most {{es}} workloads than the high throughput that remote storage can often achieve.

Some remote storage performs very poorly, especially under the kind of load that {{es}} imposes. However, on certain workloads and with careful tuning, it is sometimes possible to achieve acceptable performance using remote storage too. Before committing to a particular storage architecture, benchmark your system with a realistic workload to determine whether it will meet your performance goals. If you cannot achieve the performance you expect, work with the vendor of your storage system to identify suitable tuning parameter values.

::::{note}
For {{eck}} deployments, refer to the [ECK storage recommendations](/deploy-manage/deploy/cloud-on-k8s/storage-recommendations.md) for a complete overview of storage options in Kubernetes, along with their implications and best practices. In Kubernetes, remote storage solutions are commonly used and well-supported.
::::

### Indexing buffer size [_indexing_buffer_size]
```{applies_to}
deployment:
  self: ga
```

If your node is doing only heavy indexing, be sure [`indices.memory.index_buffer_size`](elasticsearch://reference/elasticsearch/configuration-reference/indexing-buffer-settings.md) is large enough to give at most 512 MB indexing buffer per shard doing heavy indexing (beyond that indexing performance does not typically improve). {{es}} takes that setting (a percentage of the java heap or an absolute byte-size), and uses it as a shared buffer across all active shards. Very active shards will naturally use this buffer more than shards that are performing lightweight indexing.

The default is `10%` which is often plenty: for example, if you give the JVM 10GB of memory, it will give 1GB to the index buffer, which is enough to host two shards that are heavily indexing.

### Use {{ccr}} to prevent searching from stealing resources from indexing [_use_ccr_to_prevent_searching_from_stealing_resources_from_indexing]
```{applies_to}
stack: ga
```

Within a single cluster, indexing and searching can compete for resources. By setting up two clusters, configuring [{{ccr}}](../../tools/cross-cluster-replication.md) to replicate data from one cluster to the other one, and routing all searches to the cluster that has the follower indices, search activity will no longer steal resources from indexing on the cluster that hosts the leader indices.

### Avoid hot spotting [_avoid_hot_spotting]
```{applies_to}
stack: ga
```

[Hot Spotting](../../../troubleshoot/elasticsearch/hotspotting.md) can occur when node resources, shards, or requests are not evenly distributed. {{es}} maintains cluster state by syncing it across nodes, so continually hot spotted nodes can cause overall cluster performance degradation.

## Additional optimizations [_additional_optimizations]
```{applies_to}
stack: ga
```

Many of the strategies outlined in [Tune for disk usage](disk-usage.md) can also help improve indexing speed.
