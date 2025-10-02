---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-indexing-speed.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
products:
  - id: elasticsearch
---

# Tune for indexing speed [tune-for-indexing-speed]

{{es}} offers a wide range of indexing performance optimizations, which are especially useful for high-throughput ingestion workloads. This page provides practical recommendations to help you maximize indexing speed, from bulk sizing and refresh intervals to hardware and thread management.

::::{note}
Indexing performance is also affected by your sharding and indexing strategies. Whether you’re indexing into a single index or hundreds in parallel, and how many shards each index has, can significantly influence indexing speed.

Make sure to consider also your cluster’s shard count, index layout, and overall data distribution when tuning for indexing speed. Refer to [](./size-shards.md) for more details about sharing strategies and recommendations.
::::

## Use bulk requests [_use_bulk_requests]

Bulk requests will yield much better performance than single-document index requests. In order to know the optimal size of a bulk request, you should run a benchmark on a single node with a single shard. First try to index 100 documents at once, then 200, then 400, etc. doubling the number of documents in a bulk request in every benchmark run. When the indexing speed starts to plateau then you know you reached the optimal size of a bulk request for your data. In case of tie, it is better to err in the direction of too few rather than too many documents. Beware that too large bulk requests might put the cluster under memory pressure when many of them are sent concurrently, so it is advisable to avoid going beyond a couple tens of megabytes per request even if larger requests seem to perform better.

:::{note}
In {{serverless-full}}, the minimum response time for a single bulk indexing request is 200ms.
:::

## Use multiple workers/threads to send data to {{es}} [multiple-workers-threads]

A single thread sending bulk requests is unlikely to be able to max out the indexing capacity of an {{es}} cluster. In order to use all resources of the cluster, you should send data from multiple threads or processes. In addition to making better use of the resources of the cluster, this should help reduce the cost of each fsync.

On the other hand, sending data to a single shard from too many concurrent threads or processes can overwhelm the cluster. If the indexing load exceeds what {{es}} can handle, it may become a bottleneck and start rejecting requests or slowing down overall performance.

Make sure to watch for `TOO_MANY_REQUESTS (429)` response codes (`EsRejectedExecutionException` with the Java client), which is the way that {{es}} tells you that it cannot keep up with the current indexing rate. When it happens, you should pause indexing a bit before trying again, ideally with randomized exponential backoff.

Similarly to sizing bulk requests, only testing can tell what the optimal number of workers is. This can be tested by progressively increasing the number of workers until either I/O or CPU is saturated on the cluster.

## Unset or increase the refresh interval [_unset_or_increase_the_refresh_interval]

The operation that consists of making changes visible to search - called a [refresh](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-refresh) - is costly, and calling it often while there is ongoing indexing activity can hurt indexing speed.

By default, {{es}} periodically refreshes indices every second, but only on indices that have received one search request or more in the last 30 seconds.

This is the optimal configuration if you have no or very little search traffic (e.g. less than one search request every 5 minutes) and want to optimize for indexing speed. This behavior aims to automatically optimize bulk indexing in the default case when no searches are performed. In order to opt out of this behavior set the refresh interval explicitly.

On the other hand, if your index experiences regular search requests, this default behavior means that {{es}} will refresh your index every 1 second. If you can afford to increase the amount of time between when a document gets indexed and when it becomes visible, increasing the [`index.refresh_interval`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-refresh-interval-setting) to a larger value, e.g. `30s`, might help improve indexing speed.

### Disable refresh interval

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

When bulk indexing is complete, consider running a [force merge](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-forcemerge) to optimize search performance. Force merging is not available on {{serverless-full}}.

```console
POST /my-index-000001/_forcemerge?max_num_segments=5
```
% TEST[continued]

::::{warning}
Force merge is an expensive operation.
::::

## Disable replicas for initial loads [_disable_replicas_for_initial_loads]

If you have a large amount of data that you want to load all at once into {{es}}, it may be beneficial to set `index.number_of_replicas` to `0` in order to speed up indexing. Having no replicas means that losing a single node may incur data loss, so it is important that the data lives elsewhere so that this initial load can be retried in case of an issue. Once the initial load is finished, you can set `index.number_of_replicas` back to its original value.

If `index.refresh_interval` is configured in the index settings, it may further help to unset it during this initial load and setting it back to its original value once the initial load is finished.


## Disable swapping [_disable_swapping_2]
```yaml {applies_to}
deployment:
  self: all
```
You should make sure that the operating system is not swapping out the java process by [disabling swapping](../../deploy/self-managed/setup-configuration-memory.md).

## Give memory to the filesystem cache [_give_memory_to_the_filesystem_cache]
```yaml {applies_to}
deployment:
  self: all
  eck: all
```

The filesystem cache is used to buffer I/O operations and plays a critical role in {{es}} performance. You should make sure to give at least half of the system's memory to the filesystem cache.

By default, {{es}} automatically sets its [JVM heap size](/deploy-manage/deploy/self-managed/important-settings-configuration.md#heap-size-settings) to follow this best practice. However, in self-managed or {{eck}} deployments, you have the flexibility to allocate even more memory to the filesystem cache.

While the filesystem cache primarily benefits search workloads, it can also improve indexing speed in certain scenarios—especially when indexing into many shards or performing frequent segment merges that involve reading existing data.

::::{note}
On Linux, the filesystem cache uses any memory not actively used by applications. To allocate memory to the cache, ensure that enough system memory remains available and is not consumed by {{es}} or other processes. 
::::

## Use auto-generated ids [_use_auto_generated_ids]

When indexing a document that has an explicit id, {{es}} needs to check whether a document with the same id already exists within the same shard, which is a costly operation and gets even more costly as the index grows. By using auto-generated ids, {{es}} can skip this check, which makes indexing faster.


## Use faster hardware [indexing-use-faster-hardware]

If indexing is I/O-bound, consider increasing the size of the filesystem cache (see above) or using faster storage. {{es}} generally creates individual files with sequential writes. However, indexing involves writing multiple files concurrently, and a mix of random and sequential reads too, so SSD drives tend to perform better than spinning disks.

Stripe your index across multiple SSDs by configuring a RAID 0 array. Remember that it will increase the risk of failure since the failure of any one SSD destroys the index. However this is typically the right tradeoff to make: optimize single shards for maximum performance, and then add replicas across different nodes so there’s redundancy for any node failures. You can also use [snapshot and restore](../../tools/snapshot-and-restore.md) to backup the index for further insurance.

::::{note}
In {{ech}} and {{ece}}, you can choose the underlying hardware by selecting different hardware profiles or deployment templates. Refer to [ECH > Manage hardware profiles](/deploy-manage/deploy/elastic-cloud/ec-change-hardware-profile.md) and [ECE > Manage deployment templates](/deploy-manage/deploy/cloud-enterprise/configure-deployment-templates.md) for more details.
::::

### Local vs. remote storage [_local_vs_remote_storage]
```yaml {applies_to}
deployment:
  self: all
  eck: all
  ece: all
```

Directly-attached (local) storage generally performs better than remote storage because it is simpler to configure well and avoids communications overheads.

Some remote storage performs very poorly, especially under the kind of load that {{es}} imposes. However, with careful tuning, it is sometimes possible to achieve acceptable performance using remote storage too. Before committing to a particular storage architecture, benchmark your system with a realistic workload to determine the effects of any tuning parameters. If you cannot achieve the performance you expect, work with the vendor of your storage system to identify the problem.

::::{note}
For {{eck}} deployments, refer to the [ECK storage recommendations](/deploy-manage/deploy/cloud-on-k8s/storage-recommendations.md) for a complete overview of storage options in Kubernetes, along with their implications and best practices. In Kubernetes, remote storage solutions are commonly used and well-supported.
::::

## Indexing buffer size [_indexing_buffer_size]

If your node is doing only heavy indexing, be sure [`indices.memory.index_buffer_size`](elasticsearch://reference/elasticsearch/configuration-reference/indexing-buffer-settings.md) is large enough to give at most 512 MB indexing buffer per shard doing heavy indexing (beyond that indexing performance does not typically improve). {{es}} takes that setting (a percentage of the java heap or an absolute byte-size), and uses it as a shared buffer across all active shards. Very active shards will naturally use this buffer more than shards that are performing lightweight indexing.

The default is `10%` which is often plenty: for example, if you give the JVM 10GB of memory, it will give 1GB to the index buffer, which is enough to host two shards that are heavily indexing.


## Use {{ccr}} to prevent searching from stealing resources from indexing [_use_ccr_to_prevent_searching_from_stealing_resources_from_indexing]

Within a single cluster, indexing and searching can compete for resources. By setting up two clusters, configuring [{{ccr}}](../../tools/cross-cluster-replication.md) to replicate data from one cluster to the other one, and routing all searches to the cluster that has the follower indices, search activity will no longer steal resources from indexing on the cluster that hosts the leader indices.


## Avoid hot spotting [_avoid_hot_spotting]

[Hot Spotting](../../../troubleshoot/elasticsearch/hotspotting.md) can occur when node resources, shards, or requests are not evenly distributed. {{es}} maintains cluster state by syncing it across nodes, so continually hot spotted nodes can cause overall cluster performance degradation.


## Additional optimizations [_additional_optimizations]

Many of the strategies outlined in [Tune for disk usage](disk-usage.md) can also help improve indexing speed.
