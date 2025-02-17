# Snapshot and restore [snapshot-restore]

A snapshot is a backup of a running {{es}} cluster. You can use snapshots to:

* Regularly back up a cluster with no downtime
* Recover data after deletion or a hardware failure
* Transfer data between clusters
* Reduce your storage costs by using [searchable snapshots](../../../deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md) in the cold and frozen data tiers


## The snapshot workflow [snapshot-workflow]

{{es}} stores snapshots in an off-cluster storage location called a snapshot repository. Before you can take or restore snapshots, you must [register a snapshot repository](../../../deploy-manage/tools/snapshot-and-restore/self-managed.md) on the cluster. {{es}} supports several repository types with cloud storage options, including:

* AWS S3
* Google Cloud Storage (GCS)
* Microsoft Azure

After you register a snapshot repository, you can use [{{slm}} ({{slm-init}})](../../../deploy-manage/tools/snapshot-and-restore/create-snapshots.md#automate-snapshots-slm) to automatically take and manage snapshots. You can then [restore a snapshot](../../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md) to recover or transfer its data.


## Snapshot contents [snapshot-contents]

By default, a snapshot of a cluster contains the cluster state, all regular data streams, and all regular indices. The cluster state includes:

* [Persistent cluster settings](../../../deploy-manage/deploy/self-managed/configure-elasticsearch.md#cluster-setting-types)
* [Index templates](../../../manage-data/data-store/templates.md)
* [Legacy index templates](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-template)
* [Ingest pipelines](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md)
* [{{ilm-init}} policies](../../../manage-data/lifecycle/index-lifecycle-management.md)
* [Stored scripts](../../../explore-analyze/scripting/modules-scripting-using.md#script-stored-scripts)
* For snapshots taken after 7.12.0, [feature states](../../../deploy-manage/tools/snapshot-and-restore.md#feature-state)

You can also take snapshots of only specific data streams or indices in the cluster. A snapshot that includes a data stream or index automatically includes its aliases. When you restore a snapshot, you can choose whether to restore these aliases.

Snapshots don’t contain or back up:

* Transient cluster settings
* Registered snapshot repositories
* Node configuration files
* [Security configuration files](../../../deploy-manage/security.md)

::::{note}
When restoring a data stream, if the target cluster does not have an index template that matches the data stream, the data stream will not be able to roll over until a matching index template is created. This will affect the lifecycle management of the data stream and interfere with the data stream size and retention.
::::



### Feature states [feature-state]

A feature state contains the indices and data streams used to store configurations, history, and other data for an Elastic feature, such as {{es}} security or {{kib}}.

::::{tip}
To retrieve a list of feature states, use the [Features API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-features-get-features).
::::


A feature state typically includes one or more [system indices or system data streams](https://www.elastic.co/guide/en/elasticsearch/reference/current/api-conventions.html#system-indices). It may also include regular indices and data streams used by the feature. For example, a feature state may include a regular index that contains the feature’s execution history. Storing this history in a regular index lets you more easily search it.

In {{es}} 8.0 and later versions, feature states are the only way to back up and restore system indices and system data streams.


## How snapshots work [how-snapshots-work]

Snapshots are automatically deduplicated to save storage space and reduce network transfer costs. To back up an index, a snapshot makes a copy of the index’s [segments](../../../solutions/search/search-approaches/near-real-time-search.md) and stores them in the snapshot repository. Since segments are immutable, the snapshot only needs to copy any new segments created since the repository’s last snapshot.

Each snapshot is also logically independent. When you delete a snapshot, {{es}} only deletes the segments used exclusively by that snapshot. {{es}} doesn’t delete segments used by other snapshots in the repository.


### Snapshots and shard allocation [snapshots-shard-allocation]

A snapshot copies segments from an index’s primary shards. When you start a snapshot, {{es}} immediately starts copying the segments of any available primary shards. If a shard is starting or relocating, {{es}} will wait for these processes to complete before copying the shard’s segments. If one or more primary shards aren’t available, the snapshot attempt fails.

Once a snapshot begins copying a shard’s segments, {{es}} won’t move the shard to another node, even if rebalancing or shard allocation settings would typically trigger reallocation. {{es}} will only move the shard after the snapshot finishes copying the shard’s data.


### Snapshot start and stop times [snapshot-start-stop-times]

A snapshot doesn’t represent a cluster at a precise point in time. Instead, each snapshot includes a start and end time. The snapshot represents a view of each shard’s data at some point between these two times.


## Snapshot compatibility [snapshot-restore-version-compatibility]

To restore a snapshot to a cluster, the versions for the snapshot, cluster, and any restored indices must be compatible.


### Snapshot version compatibility [snapshot-cluster-compatibility]

You can’t restore a snapshot to an earlier version of {{es}}. For example, you can’t restore a snapshot taken in 7.6.0 to a cluster running 7.5.0.

::::{note}
:name: snapshot-prerelease-build-compatibility

This documentation is for {{es}} version 9.0.0-beta1, which is not yet released. The compatibility table above applies only to snapshots taken in a released version of {{es}}. If you’re testing a pre-release build of {{es}} then you can still restore snapshots taken in earlier released builds as permitted by this compatibility table. You can also take snapshots using your pre-release build, and restore them using the same build. However once a pre-release build of {{es}} has written to a snapshot repository you must not use the same repository with other builds of {{es}}, even if the builds have the same version. Different pre-release builds of {{es}} may use different and incompatible repository layouts. If the repository layout is incompatible with the {{es}} build in use then taking and restoring snapshots may result in errors or may appear to succeed having silently lost some data. You should discard your repository before using a different build.
::::



### Index compatibility [snapshot-index-compatibility]

Any index you restore from a snapshot must also be compatible with the current cluster’s version. If you try to restore an index created in an incompatible version, the restore attempt will fail.

|     |     |
| --- | --- |
|  | Cluster version |
| Index creation version | 6.8 | 7.0–7.1 | 7.2–8.17 | 8.0–8.2 | 8.3-9.0 |
| 5.0–5.6 | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "")[[1]](../../../deploy-manage/tools/snapshot-and-restore.md#fn-archive) |
| 6.0–6.7 | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "")[[1]](../../../deploy-manage/tools/snapshot-and-restore.md#fn-archive) |
| 6.8 | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "")[[1]](../../../deploy-manage/tools/snapshot-and-restore.md#fn-archive) |
| 7.0–7.1 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 7.2–8.17 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| 8.0–9.0 | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |

$$$fn-archive$$$
1. Supported with [archive indices](../../../deploy-manage/upgrade/deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md).

You can’t restore an index to an earlier version of {{es}}. For example, you can’t restore an index created in 7.6.0 to a cluster running 7.5.0.

A compatible snapshot can contain indices created in an older incompatible version. For example, a snapshot of a 8.17 cluster can contain an index created in 6.8. Restoring the 6.8 index to an 9.0 cluster fails unless you can use the [archive functionality](../../../deploy-manage/upgrade/deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md). Keep this in mind if you take a snapshot before upgrading a cluster.

As a workaround, you can first restore the index to another cluster running the latest version of {{es}} that’s compatible with both the index and your current cluster. You can then use [reindex-from-remote](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) to rebuild the index on your current cluster. Reindex from remote is only possible if the index’s [`_source`](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-source-field.html) is enabled.

Reindexing from remote can take significantly longer than restoring a snapshot. Before you start, test the reindex from remote process with a subset of the data to estimate your time requirements.


## Warnings [snapshot-restore-warnings]


### Other backup methods [other-backup-methods]

**Taking a snapshot is the only reliable and supported way to back up a cluster.** You cannot back up an {{es}} cluster by making copies of the data directories of its nodes. There are no supported methods to restore any data from a filesystem-level backup. If you try to restore a cluster from such a backup, it may fail with reports of corruption or missing files or other data inconsistencies, or it may appear to have succeeded having silently lost some of your data.

A copy of the data directories of a cluster’s nodes does not work as a backup because it is not a consistent representation of their contents at a single point in time. You cannot fix this by shutting down nodes while making the copies, nor by taking atomic filesystem-level snapshots, because {{es}} has consistency requirements that span the whole cluster. You must use the built-in snapshot functionality for cluster backups.


### Repository contents [snapshot-repository-contents]

**Don’t modify anything within the repository or run processes that might interfere with its contents.** If something other than {{es}} modifies the contents of the repository then future snapshot or restore operations may fail, reporting corruption or other data inconsistencies, or may appear to succeed having silently lost some of your data.

You may however safely [restore a repository from a backup](../../../deploy-manage/tools/snapshot-and-restore/self-managed.md#snapshots-repository-backup) as long as

1. The repository is not registered with {{es}} while you are restoring its contents.
2. When you have finished restoring the repository its contents are exactly as they were when you took the backup.

If you no longer need any of the snapshots in a repository, unregister it from {{es}} before deleting its contents from the underlying storage.

Additionally, snapshots may contain security-sensitive information, which you may wish to [store in a dedicated repository](../../../deploy-manage/tools/snapshot-and-restore/create-snapshots.md#cluster-state-snapshots).
