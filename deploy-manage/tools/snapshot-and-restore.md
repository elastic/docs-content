---
applies_to:
  deployment:
    eck: 
    ess: 
    ece: 
    self: 
---

# Snapshot and restore

A snapshot is a backup of a running Elasticsearch cluster. You can use snapshots to:

- Regularly back up a cluster with no downtime
- Recover data after deletion or a hardware failure
- Transfer data between clusters
- Reduce storage costs by using **[searchable snapshots](snapshot-and-restore/searchable-snapshots.md)** in the cold and frozen data tiers

## Snapshot workflow

Elasticsearch stores snapshots in an off-cluster storage location called a **snapshot repository**. Before you can take or restore snapshots, you must [register a snapshot repository](snapshot-and-restore/self-managed.md#manage-snapshot-repos) on the cluster. Elasticsearch supports different repository types depending on your deployment type:

* [**Elastic Cloud Hosted repository types**](/deploy-manage/tools/snapshot-and-restore/elastic-cloud-hosted.md)
* [**Self-managed repository types**](/deploy-manage/tools/snapshot-and-restore/self-managed.md)

After you register a snapshot repository, you can use [snapshot lifecycle management (SLM)](snapshot-and-restore/create-snapshots.md#automate-snapshots-slm) to automatically take and manage snapshots. You can then [restore a snapshot](snapshot-and-restore/restore-snapshot.md) to recover or transfer its data.

::::{note}
While the majority of snapshot-related operations are similar across all deployment types, Elastic Cloud Hosted, Elastic Cloud Enterprise (ECE), and Elastic Cloud on Kubernetes (ECK) offer additional capabilities, as described below.
::::

::::{dropdown} Elastic Cloud Hosted
When you create a deployment, a default repository called `found-snapshots` is automatically added to the {{es}} cluster. This repository is specific to that cluster: the `cluster ID` is part of the repository’s `base_path`, such as `/snapshots/[cluster-id]`.

:::{note}
Do not disable or delete the default `cloud-snapshot-policy` SLM policy, and do not change the default `found-snapshots` repository defined in that policy. These actions are not supported.
:::

The default policy and repository are used when:

- Creating a new deployment from a snapshot
- Restoring a snapshot to a different deployment
- Taking automated snapshots in case of deployment changes

In Elastic Cloud Hosted, you can [restore snapshots](snapshot-and-restore/restore-snapshot.md) across clusters, but only within the same region.

You can customize the snapshot retention settings in that policy to adjust them to your needs.

To use a custom snapshot repository, [register a new snapshot repository](snapshot-and-restore/self-managed.md#manage-snapshot-repos) and [create another SLM policy](snapshot-and-restore/create-snapshots.md#automate-snapshots-slm).
::::

::::{dropdown} Elastic Cloud Enterprise
To enable snapshots for your Elasticsearch clusters, you must first [configure a repository](snapshot-and-restore/cloud-enterprise.md) at the platform level in ECE and then associate it with your deployments. Once configured, snapshots are taken every 30 minutes or at the interval you specify.

Use **Kibana** to manage your snapshots. In Kibana, you can:

- Set up additional repositories where snapshots are stored (other than the one managed by Elastic Cloud Enterprise)
- View and delete snapshots
- Configure a snapshot lifecycle management (SLM) policy to automate when snapshots are created and deleted

In **Elastic Cloud Enterprise**, you can also [restore snapshots](snapshot-and-restore/restore-snapshot.md) across clusters.
::::
  
::::{dropdown} Elastic Cloud on Kubernetes (ECK)
On Elastic Cloud on Kubernetes, you must manually configure snapshot repositories. The system does not create **Snapshot Lifecycle Management (SLM) policies** or **automatic snapshots** by default.

For detailed configuration steps, refer to [Configuring snapshots on ECK](snapshot-and-restore/cloud-on-k8s.md).
::::

:::{note}
Snapshots back up only open indices. If you close an index, it is not included in snapshots and you will not be able to restore the data.
:::

## Snapshot contents

By default, a snapshot of a cluster contains the cluster state, all regular data streams, and all regular indices. The cluster state includes:

- [Persistent cluster settings](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#cluster-setting-types) 
- [Index templates](/manage-data/data-store/templates.md)
- [Legacy index templates](https://www.elastic.co/guide/en/elasticsearch/reference/8.17/indices-templates-v1.html)
- [Ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md)
- [ILM policies](/manage-data/lifecycle/index-lifecycle-management.md)
- [Stored scripts](/explore-analyze/scripting/modules-scripting-using.md#script-stored-scripts)
- For snapshots taken after 7.12.0, [feature states](#feature-state)

You can also take snapshots of only specific data streams or indices in the cluster. A snapshot that includes a data stream or index automatically includes its aliases. When you restore a snapshot, you can choose whether to restore these aliases.

Snapshots don’t contain or back up:

- Transient cluster settings
- Registered snapshot repositories
- Node configuration files
- [Security configuration files](/deploy-manage/security.md)

### Feature states [feature-state]

A **feature state** contains the indices and data streams used to store configurations, history, and other data for an Elastic feature, such as **Elasticsearch security** or **Kibana**.

::::{note}
To retrieve a list of feature states, use the [Features API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-features-get-features).
::::

A feature state typically includes one or more [system indices or system data streams](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/rest-apis/api-conventions.md#system-indices). It may also include regular indices and data streams used by the feature. For example, a feature state may include a regular index that contains the feature’s execution history. Storing this history in a regular index lets you more easily search it.

In Elasticsearch 8.0 and later versions, feature states are the only way to back up and restore system indices and system data streams.

## How snapshots work

Snapshots are **automatically deduplicated** to save storage space and reduce network transfer costs. To back up an index, a snapshot makes a copy of the index’s [segments](/manage-data/data-store/near-real-time-search.md) and stores them in the snapshot repository. Since segments are immutable, the snapshot only needs to copy any new segments created since the repository’s last snapshot.

Each snapshot is **logically independent**. When you delete a snapshot, Elasticsearch only deletes the segments used exclusively by that snapshot. Elasticsearch doesn’t delete segments used by other snapshots in the repository.

### Snapshots and shard allocation [snapshots-shard-allocation]

A snapshot copies segments from an index’s primary shards. When you start a snapshot, Elasticsearch immediately starts copying the segments of any available primary shards. If a shard is starting or relocating, Elasticsearch will wait for these processes to complete before copying the shard’s segments. If one or more primary shards aren’t available, the snapshot attempt fails.

Once a snapshot begins copying a shard’s segments, Elasticsearch won’t move the shard to another node, even if rebalancing or shard allocation settings would typically trigger reallocation. Elasticsearch will only move the shard after the snapshot finishes copying the shard’s data.

### Snapshot start and stop times

A snapshot doesn’t represent a cluster at a precise point in time. Instead, each snapshot includes a start and end time. The snapshot represents a view of each shard’s data at some point between these two times.

## Snapshot compatibility

To restore a snapshot to a cluster, the versions for the snapshot, cluster, and any restored indices must be compatible.

### Snapshot version compatibility [snapshot-restore-version-compatibility]

You can’t restore a snapshot to an earlier version of Elasticsearch. For example, you can’t restore a snapshot taken in 7.6.0 to a cluster running 7.5.0.

### Index compatibility

Any index you restore from a snapshot must also be compatible with the current cluster’s version. If you try to restore an index created in an incompatible version, the restore attempt will fail.

| Index creation version | 6.8 | 7.0–7.1 | 7.2–7.17 | 8.0–8.2 | 8.3–8.17 |
|------------------------|-----|---------|---------|---------|---------|
| 5.0–5.6               | ✅   | ❌       | ❌       | ❌       | ✅ [1]   |
| 6.0–6.7               | ✅   | ✅       | ✅       | ❌       | ✅ [1]   |
| 6.8                   | ✅   | ❌       | ✅       | ❌       | ✅ [1]   |
| 7.0–7.1               | ❌   | ✅       | ✅       | ✅       | ✅       |
| 7.2–7.17              | ❌   | ❌       | ✅       | ✅       | ✅       |
| 8.0–8.17              | ❌   | ❌       | ❌       | ✅       | ✅       |

[¹] Supported with [archive indices](/deploy-manage/upgrade/deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md).

You can’t restore an index to an earlier version of Elasticsearch. For example, you can’t restore an index created in 7.6.0 to a cluster running 7.5.0.

A compatible snapshot can contain indices created in an older incompatible version. For example, a snapshot of a 7.17 cluster can contain an index created in 6.8. Restoring the 6.8 index to an 8.17 cluster fails unless you can use the [archive functionality](/deploy-manage/upgrade/deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md). Keep this in mind if you take a snapshot before upgrading a cluster.

As a workaround, you can first restore the index to another cluster running the latest version of Elasticsearch that’s compatible with both the index and your current cluster. You can then use [reindex-from-remote](https://www.elastic.co/guide/en/elasticsearch/reference/8.17/docs-reindex.html#reindex-from-remote) to rebuild the index on your current cluster. Reindex from remote is only possible if the index’s [`_source`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/mapping-source-field.md) is enabled.

Reindexing from remote can take significantly longer than restoring a snapshot. Before you start, test the reindex from remote process with a subset of the data to estimate your time requirements.

## Warnings

### Other backup methods

**Taking a snapshot is the only reliable and supported way to back up a cluster.** You cannot back up an Elasticsearch cluster by making copies of the data directories of its nodes. There are no supported methods to restore any data from a filesystem-level backup. If you try to restore a cluster from such a backup, it may fail with reports of corruption or missing files or other data inconsistencies, or it may appear to have succeeded having silently lost some of your data.

A copy of the data directories of a cluster’s nodes does not work as a backup because it is not a consistent representation of their contents at a single point in time. You cannot fix this by shutting down nodes while making the copies, nor by taking atomic filesystem-level snapshots, because Elasticsearch has consistency requirements that span the whole cluster. You must use the built-in snapshot functionality for cluster backups.

### Repository contents [snapshot-repository-contents]

**Don’t modify anything within the repository or run processes that might interfere with its contents.** If something other than Elasticsearch modifies the contents of the repository then future snapshot or restore operations may fail, reporting corruption or other data inconsistencies, or may appear to succeed having silently lost some of your data.

You may however safely [restore a repository from a backup](snapshot-and-restore/self-managed.md#snapshots-repository-backup) as long as

1. The repository is not registered with Elasticsearch while you are restoring its contents.
2. When you have finished restoring the repository its contents are exactly as they were when you took the backup.

If you no longer need any of the snapshots in a repository, unregister it from Elasticsearch before deleting its contents from the underlying storage.

Additionally, snapshots may contain security-sensitive information, which you may wish to [store in a dedicated repository](snapshot-and-restore/create-snapshots.md#cluster-state-snapshots).
