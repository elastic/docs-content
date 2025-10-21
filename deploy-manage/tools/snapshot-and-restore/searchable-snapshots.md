---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/searchable-snapshots.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Searchable snapshots [searchable-snapshots]
::::{important}
Searchable snapshots is a feature that requires an Enterprise license. 
::::

{{search-snaps-cap}} let you use [snapshots](../snapshot-and-restore.md) to search infrequently accessed and read-only data in a very cost-effective fashion. The [cold](../../../manage-data/lifecycle/data-tiers.md#cold-tier) and [frozen](../../../manage-data/lifecycle/data-tiers.md#frozen-tier) data tiers use {{search-snaps}} to reduce your storage and operating costs.

{{search-snaps-cap}} eliminate the need for [replica shards](../../../deploy-manage/index.md) after rolling over from the hot tier, potentially halving the local storage needed to search your data. {{search-snaps-cap}} rely on the same snapshot mechanism you already use for backups and have minimal impact on your snapshot repository storage costs.


## Using {{search-snaps}} [using-searchable-snapshots]

Searching a {{search-snap}} index is the same as searching any other index.

By default, {{search-snap}} indices have no replicas. The underlying snapshot provides resilience and the query volume is expected to be low enough that a single shard copy will be sufficient. However, if you need to support a higher query volume, you can add replicas by adjusting the `index.number_of_replicas` index setting.

If a node fails and {{search-snap}} shards need to be recovered elsewhere, there is a brief window of time while {{es}} allocates the shards to other nodes where the cluster health will not be `green`. Searches that hit these shards may fail or return partial results until the shards are reallocated to healthy nodes.

You typically manage {{search-snaps}} through {{ilm-init}}. The [searchable snapshots](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md) action automatically converts a regular index into a {{search-snap}} index when it reaches the `cold` or `frozen` phase. You can also make indices in existing snapshots searchable by manually mounting them using the [mount snapshot](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-searchable-snapshots-mount) API.

To mount an index from a snapshot that contains multiple indices, we recommend creating a [clone](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-clone) of the snapshot that contains only the index you want to search, and mounting the clone. You should not delete a snapshot if it has any mounted indices, so creating a clone enables you to manage the lifecycle of the backup snapshot independently of any {{search-snaps}}. If you use {{ilm-init}} to manage your {{search-snaps}} then it will automatically look after cloning the snapshot as needed.

You can control the allocation of the shards of {{search-snap}} indices using the same mechanisms as for regular indices. For example, you could use [Index-level shard allocation filtering](../../distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md) to restrict {{search-snap}} shards to a subset of your nodes.

The speed of recovery of a {{search-snap}} index is limited by the repository setting `max_restore_bytes_per_sec` and the node setting `indices.recovery.max_bytes_per_sec` just like a normal restore operation. By default `max_restore_bytes_per_sec` is unlimited, but the default for `indices.recovery.max_bytes_per_sec` depends on the configuration of the node. See [Recovery settings](elasticsearch://reference/elasticsearch/configuration-reference/index-recovery-settings.md#recovery-settings).

We recommend that you [force-merge](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-forcemerge) indices to a single segment per shard before taking a snapshot that will be mounted as a {{search-snap}} index. Each read from a snapshot repository takes time and costs money, and the fewer segments there are the fewer reads are needed to restore the snapshot or to respond to a search.

::::{tip}
{{search-snaps-cap}} are ideal for managing a large archive of historical data. Historical information is typically searched less frequently than recent data and therefore may not need replicas for their performance benefits.

For more complex or time-consuming searches, you can use [Async search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit) with {{search-snaps}}.

::::


$$$searchable-snapshots-repository-types$$$
Use any of the following repository types with searchable snapshots:

* [AWS S3](s3-repository.md)
* [Google Cloud Storage](google-cloud-storage-repository.md)
* [Azure Blob Storage](azure-repository.md)
* [Hadoop Distributed File Store (HDFS)](elasticsearch://reference/elasticsearch-plugins/repository-hdfs.md)
* [Shared filesystems](shared-file-system-repository.md) such as NFS
* [Read-only HTTP and HTTPS repositories](read-only-url-repository.md)

You can also use alternative implementations of these repository types, for instance [MinIO](s3-repository.md#repository-s3-client), as long as they are fully compatible. Use the [Repository analysis](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-repository-analyze) API to analyze your repository’s suitability for use with searchable snapshots.


## How {{search-snaps}} work [how-searchable-snapshots-work]

When an index is mounted from a snapshot, {{es}} allocates its shards to data nodes within the cluster. The data nodes then automatically retrieve the relevant shard data from the repository onto local storage, based on the [mount options](#searchable-snapshot-mount-storage-options) specified. If possible, searches use data from local storage. If the data is not available locally, {{es}} downloads the data that it needs from the snapshot repository.

If a node holding one of these shards fails, {{es}} automatically allocates the affected shards on another node, and that node restores the relevant shard data from the repository. No replicas are needed, and no complicated monitoring or orchestration is necessary to restore lost shards. Although searchable snapshot indices have no replicas by default, you may add replicas to these indices by adjusting `index.number_of_replicas`. Replicas of {{search-snap}} shards are recovered by copying data from the snapshot repository, just like primaries of {{search-snap}} shards. In contrast, replicas of regular indices are restored by copying data from the primary.


### Mount options [searchable-snapshot-mount-storage-options]

To search a snapshot, you must first mount it locally as an index. Usually {{ilm-init}} will do this automatically, but you can also call the [mount snapshot](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-searchable-snapshots-mount) API yourself. There are two options for mounting an index from a snapshot, each with different performance characteristics and local storage footprints:

$$$fully-mounted$$$

Fully mounted index
:   Fully caches the snapshotted index’s shards in the {{es}} cluster. {{ilm-init}} uses this option in the `hot` and `cold` phases.

    Search performance for a fully mounted index is normally comparable to a regular index, since there is minimal need to access the snapshot repository. While recovery is ongoing, search performance may be slower than with a regular index because a search may need some data that has not yet been retrieved into the local cache. If that happens, {{es}} will eagerly retrieve the data needed to complete the search in parallel with the ongoing recovery. On-disk data is preserved across restarts, such that the node does not need to re-download data that is already stored on the node after a restart.

    Indices managed by {{ilm-init}} are prefixed with `restored-` when fully mounted.


$$$partially-mounted$$$

Partially mounted index
:   Uses a local cache containing only recently searched parts of the snapshotted index’s data. This cache has a fixed size and is shared across shards of partially mounted indices allocated on the same data node. {{ilm-init}} uses this option in the `frozen` phase.

    If a search requires data that is not in the cache, {{es}} fetches the missing data from the snapshot repository. Searches that require these fetches are slower, but the fetched data is stored in the cache so that similar searches can be served more quickly in future. {{es}} will evict infrequently used data from the cache to free up space. The cache is cleared when a node is restarted.

    Although slower than a fully mounted index or a regular index, a partially mounted index still returns search results quickly, even for large data sets, because the layout of data in the repository is heavily optimized for search. Many searches will need to retrieve only a small subset of the total shard data before returning results.

    Indices managed by {{ilm-init}} are prefixed with `partial-` when partially mounted.


To partially mount an index, you must have one or more nodes with a shared cache available. By default, dedicated frozen data tier nodes (nodes with the `data_frozen` role and no other data roles) have a shared cache configured using the greater of 90% of total disk space and total disk space subtracted a headroom of 100GB.

Using a dedicated frozen tier is highly recommended for production use. If you do not have a dedicated frozen tier, you must configure the `xpack.searchable.snapshot.shared_cache.size` setting to reserve space for the cache on one or more nodes. Partially mounted indices are only allocated to nodes that have a shared cache.

::::{admonition} Manual snapshot mounting
:class: warning

:name: manually-mounting-snapshots

Manually mounting snapshots captured by an Index Lifecycle Management ({{ilm-init}}) policy can interfere with {{ilm-init}}'s automatic management. This may lead to issues such as data loss or complications with snapshot handling.

For optimal results, allow {{ilm-init}} to manage snapshots automatically.

[Learn more about {{ilm-init}} snapshot management](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md).

::::


$$$searchable-snapshots-shared-cache$$$

`xpack.searchable.snapshot.shared_cache.size`
:   ([Static](../../deploy/self-managed/configure-elasticsearch.md#static-cluster-setting)) Disk space reserved for the shared cache of partially mounted indices. Accepts a percentage of total disk space or an absolute [byte value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#byte-units). Defaults to `90%` of total disk space for dedicated frozen data tier nodes. Otherwise defaults to `0b`.

`xpack.searchable.snapshot.shared_cache.size.max_headroom`
:   ([Static](../../deploy/self-managed/configure-elasticsearch.md#static-cluster-setting), [byte value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#byte-units)) For dedicated frozen tier nodes, the max headroom to maintain. If `xpack.searchable.snapshot.shared_cache.size` is not explicitly set, this setting defaults to `100GB`. Otherwise it defaults to `-1` (not set). You can only configure this setting if `xpack.searchable.snapshot.shared_cache.size` is set as a percentage.

To illustrate how these settings work in concert let us look at two examples when using the default values of the settings on a dedicated frozen node:

* A 4000 GB disk will result in a shared cache sized at 3900 GB. 90% of 4000 GB is 3600 GB, leaving 400 GB headroom. The default `max_headroom` of 100 GB takes effect, and the result is therefore 3900 GB.
* A 400 GB disk will result in a shared cache sized at 360 GB.

You can configure the settings in [`elasticsearch.yml`](/deploy-manage/stack-settings.md):

```yaml
xpack.searchable.snapshot.shared_cache.size: 4TB
```

::::{important}
You can only configure these settings on nodes with the [`data_frozen`](../../distributed-architecture/clusters-nodes-shards/node-roles.md#data-frozen-node) role. Additionally, nodes with a shared cache can only have a single [data path](/deploy-manage/deploy/self-managed/important-settings-configuration.md#path-settings).
::::


{{es}} also uses a dedicated system index named `.snapshot-blob-cache` to speed up the recoveries of {{search-snap}} shards. This index is used as an additional caching layer on top of the partially or fully mounted data and contains the minimal required data to start the {{search-snap}} shards. {{es}} automatically deletes the documents that are no longer used in this index. This periodic clean up can be tuned using the following settings:

`searchable_snapshots.blob_cache.periodic_cleanup.interval`
:   ([Dynamic](../../deploy/self-managed/configure-elasticsearch.md#dynamic-cluster-setting)) The interval at which the periodic cleanup of the `.snapshot-blob-cache` index is scheduled. Defaults to every hour (`1h`).

`searchable_snapshots.blob_cache.periodic_cleanup.retention_period`
:   ([Dynamic](../../deploy/self-managed/configure-elasticsearch.md#dynamic-cluster-setting)) The retention period to keep obsolete documents in the `.snapshot-blob-cache` index. Defaults to every hour (`1h`).

`searchable_snapshots.blob_cache.periodic_cleanup.batch_size`
:   ([Dynamic](../../deploy/self-managed/configure-elasticsearch.md#dynamic-cluster-setting)) The number of documents that are searched for and bulk-deleted at once during the periodic cleanup of the `.snapshot-blob-cache` index. Defaults to `100`.

`searchable_snapshots.blob_cache.periodic_cleanup.pit_keep_alive`
:   ([Dynamic](../../deploy/self-managed/configure-elasticsearch.md#dynamic-cluster-setting)) The value used for the [point-in-time keep alive](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-open-point-in-time) requests executed during the periodic cleanup of the `.snapshot-blob-cache` index. Defaults to `10m`.


## Reduce costs with {{search-snaps}} [searchable-snapshots-costs]

In most cases, {{search-snaps}} reduce the costs of running a cluster by removing the need for replica shards  and for shard data to be copied between nodes. However, if it’s particularly expensive to retrieve data from a snapshot repository in your environment, {{search-snaps}} may be more costly than regular indices. Ensure that the cost structure of your operating environment is compatible with {{search-snaps}} before using them.


### Replica costs [searchable-snapshots-costs-replicas]

For resiliency, a regular index requires multiple redundant copies of each shard across multiple nodes. If a node fails, {{es}} uses the redundancy to rebuild any lost shard copies. A {{search-snap}} index doesn’t require replicas. If a node containing a {{search-snap}} index fails, {{es}} can rebuild the lost shard cache from the snapshot repository.

Without replicas, rarely-accessed {{search-snap}} indices require far fewer resources. A cold data tier that contains replica-free fully-mounted {{search-snap}} indices requires half the nodes and disk space of a tier containing the same data in regular indices. The frozen tier, which contains only partially-mounted {{search-snap}} indices, requires even fewer resources.


### Data transfer costs [snapshot-retrieval-costs]

When a shard of a regular index is moved between nodes, its contents are copied from another node in your cluster. In many environments, the costs of moving data between nodes are significant, especially if running in a Cloud environment with nodes in different zones. In contrast, when mounting a {{search-snap}} index or moving one of its shards, the data is always copied from the snapshot repository. This is typically much cheaper.

::::{warning}
Most cloud providers charge significant fees for data transferred between regions and for data transferred out of their platforms. You should only mount snapshots into a cluster that is in the same region as the snapshot repository. If you wish to search data across multiple regions, configure multiple clusters and use [{{ccs}}](../../../solutions/search/cross-cluster-search.md) or [{{ccr}}](../cross-cluster-replication.md) instead of {{search-snaps}}.
::::


It’s worth noting that if a searchable snapshot index has no replicas, then when the node hosting it is shut down, allocation will immediately try to relocate the index to a new node in order to maximize availability. For fully mounted indices this will result in the new node downloading the entire index snapshot from the cloud repository. Under a rolling cluster restart, this may happen multiple times for each searchable snapshot index. Temporarily disabling allocation during planned node restart will prevent this, as described in the [cluster restart procedure](../../maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling).


## Back up and restore {{search-snaps}} [back-up-restore-searchable-snapshots]

You can use [regular snapshots](create-snapshots.md) to back up a cluster containing {{search-snap}} indices. When you restore a snapshot containing {{search-snap}} indices, these indices are restored as {{search-snap}} indices again.

Before you restore a snapshot containing a {{search-snap}} index, you must first [register the repository](self-managed.md) containing the original index snapshot. When restored, the {{search-snap}} index mounts the original index snapshot from its original repository. If wanted, you can use separate repositories for regular snapshots and {{search-snaps}}.

A snapshot of a {{search-snap}} index contains only a small amount of metadata which identifies its original index snapshot. It does not contain any data from the original index. The restore of a backup will fail to restore any {{search-snap}} indices whose original index snapshot is unavailable.

Because {{search-snap}} indices are not regular indices, it is not possible to use a [source-only repository](source-only-repository.md) to take snapshots of {{search-snap}} indices.

::::{admonition} Reliability of searchable snapshots
:class: warning

:name: searchable-snapshots-reliability

The sole copy of the data in a {{search-snap}} index is the underlying snapshot, stored in the repository. If you remove this snapshot, the data will be permanently lost. Although {{es}} may have cached some of the data onto local storage for faster searches, this cached data is incomplete and cannot be used for recovery if you remove the underlying snapshot. For example:

* You must not unregister a repository while any of the {{search-snaps}} it contains are mounted in {{es}}.
* You must not delete a snapshot if any of its indices are mounted as {{search-snap}} indices. The snapshot contains the sole full copy of your data. If you delete it then the data cannot be recovered from elsewhere.
* If you mount indices from snapshots held in a repository to which a different cluster has write access then you must make sure that the other cluster does not delete these snapshots. The snapshot contains the sole full copy of your data. If you delete it then the data cannot be recovered from elsewhere.
* The data in a searchable snapshot index are cached in local storage, so if you delete the underlying searchable snapshot {{es}} will continue to operate normally until the first cache miss. This may be much later, for instance when a shard relocates to a different node, or when the node holding the shard restarts.
* If the repository fails or corrupts the contents of the snapshot and you cannot restore it to its previous healthy state then the data is permanently lost.

    The blob storage offered by all major public cloud providers typically offers very good protection against failure or corruption. If you manage your own repository storage then you are responsible for its reliability.


::::


