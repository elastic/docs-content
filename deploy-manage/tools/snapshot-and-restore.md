---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshot-restore.html
  - https://www.elastic.co/guide/en/cloud/current/ec-snapshot-restore.html
  - https://www.elastic.co/guide/en/cloud/current/ec-restoring-snapshots.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-snapshot-restore.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-restoring-snapshots.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-snapshots.html
applies_to:
  stack: all
products:
  - id: elasticsearch
  - id: cloud-hosted
  - id: cloud-enterprise
---

# Snapshot and restore

A snapshot is a backup of a running {{es}} cluster. You can use snapshots to:

- Regularly back up a cluster with no downtime
- Recover data after deletion or a hardware failure
- Transfer data between clusters
- Reduce storage costs by using **[searchable snapshots](snapshot-and-restore/searchable-snapshots.md)** in the cold and frozen data tiers

::::{important}
Snapshots preserve more than your data. They also include the configuration and internal data of {{stack}} features, such as {{ilm-init}} policies, index templates and pipelines, {{kib}} saved objects, alerting rules, {{fleet}} settings and integrations, {{elastic-sec}} data, and more, depending on your use case.

Consider using snapshots to back up, at minimum, all {{es}} system indices and the cluster state, even if your data can be reindexed or recovered from other external sources. Without these backups, a disaster recovery scenario can result in the loss of your stack configuration and feature states, even if the underlying data can be restored.
::::

## Snapshot workflow

{{es}} stores snapshots in an off-cluster storage location called a **snapshot repository**. Before you can take or restore snapshots, you must [register a snapshot repository](snapshot-and-restore/self-managed.md#manage-snapshot-repos) on the cluster. {{es}} supports different repository types depending on your deployment type:

* [**{{ech}} repository types**](/deploy-manage/tools/snapshot-and-restore/elastic-cloud-hosted.md)
* [**Self-managed repository types**](/deploy-manage/tools/snapshot-and-restore/self-managed.md)

After you register a snapshot repository, you can use [snapshot lifecycle management (SLM)](snapshot-and-restore/create-snapshots.md#automate-snapshots-slm) to automatically take and manage snapshots. You can then [restore a snapshot](snapshot-and-restore/restore-snapshot.md) to recover or transfer its data.

::::{note}
While the majority of snapshot-related operations are similar across all deployment types, {{ech}}, {{ece}} (ECE), and {{eck}} (ECK) offer additional capabilities, as described below.
::::

::::{dropdown} {{ech}}
When you create a deployment, a default repository called `found-snapshots` is automatically added to the {{es}} cluster. This repository is specific to that cluster: the `cluster ID` is part of the repository’s `base_path`, such as `/snapshots/[cluster-id]`.

:::{note}
Do not disable or delete the default `cloud-snapshot-policy` SLM policy, and do not change the default `found-snapshots` repository defined in that policy. These actions are not supported.
:::

The default policy and repository are used when:

- Creating a new deployment from a snapshot
- Restoring a snapshot to a different deployment
- Taking automated snapshots in case of deployment changes

In {{ech}}, you can [restore snapshots](snapshot-and-restore/restore-snapshot.md) across clusters, but only within the same region.

For API-driven deployment linking of platform-managed snapshots, refer to [Manage snapshot repositories in {{ech}}](snapshot-and-restore/elastic-cloud-hosted.md#register-snapshot-repos-ech).

You can customize the snapshot retention settings in that policy to adjust them to your needs.

To use a custom snapshot repository, [register a new snapshot repository](snapshot-and-restore/self-managed.md#manage-snapshot-repos) and [create another SLM policy](snapshot-and-restore/create-snapshots.md#automate-snapshots-slm).
::::

::::{dropdown} {{ece}}
To enable snapshots for your {{es}} clusters, you must first [configure a repository](snapshot-and-restore/cloud-enterprise.md) at the platform level in ECE and then associate it with your deployments. Once configured, snapshots are taken every 30 minutes or at the interval you specify.

Use **Kibana** to manage your snapshots. In {{kib}}, you can:

- Set up additional repositories where snapshots are stored (other than the one managed by {{ece}})
- View and delete snapshots
- Configure a snapshot lifecycle management (SLM) policy to automate when snapshots are created and deleted

In **{{ece}}**, you can also [restore snapshots](snapshot-and-restore/restore-snapshot.md) across clusters.
::::

::::{dropdown} {{eck}} (ECK)
On {{eck}}, you must manually configure snapshot repositories. The system does not create **Snapshot Lifecycle Management (SLM) policies** or **automatic snapshots** by default.

For detailed configuration steps, refer to [Configuring snapshots on ECK](snapshot-and-restore/cloud-on-k8s.md).
::::

:::{note}
Snapshots back up only open indices. If you close an index, it is not included in snapshots and you will not be able to restore the data.
:::

## Snapshot contents

By default, a snapshot of a cluster contains the cluster state, all regular data streams, and all regular indices. The cluster state includes:

- [Persistent cluster settings](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#cluster-setting-types)
- [Index templates](/manage-data/data-store/templates.md)
- [Legacy index templates](https://www.elastic.co/guide/en/elasticsearch/reference/8.18/indices-templates-v1.html)
- [Ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md)
- [ILM policies](/manage-data/lifecycle/index-lifecycle-management.md)
- [Stored scripts](/explore-analyze/scripting/modules-scripting-store-and-retrieve.md)
- For snapshots taken after 7.12.0, [feature states](#feature-state)

You can also take snapshots of only specific data streams or indices in the cluster. A snapshot that includes a data stream or index automatically includes its aliases. When you restore a snapshot, you can choose whether to restore these aliases.

Snapshots don’t contain or back up:

- Transient cluster settings
- Registered snapshot repositories
- Node configuration files
- [Security configuration files](/deploy-manage/security.md)

### Feature states [feature-state]

A feature state contains the indices and data streams used to store configurations, history, and other data for an Elastic feature, such as {{es}} security, {{kib}}, {{fleet}}, or {{watcher}}. To retrieve a list of feature states, use the [Features API]({{es-apis}}operation/operation-features-get-features).

```console
GET /_features
```

A feature state typically includes one or more [system indices or system data streams](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#system-indices). It may also include regular indices and data streams used by the feature. For example, a feature state may include a regular index that contains the feature’s execution history. Storing this history in a regular index lets you more easily search it.

Starting with {{es}} 8.0 and later versions, feature states are the only way to back up and restore system indices and system data streams. Attempting to restore a system index or data stream outside its feature state is not permitted and will result in the following error:

```
requested system indices [.example], but system indices can only be restored as part of a feature state
```

Restoring system indices and data streams will require temporary elevated permissions to edit restricted indices. For more information, refer to [File-based access recovery](/troubleshoot/elasticsearch/file-based-recovery.md). Attempting to restore a system index or data stream without the required temporary elevated permissions will result in the following error:

```
Indices [.example] use and access is reserved for system operations
```


## How snapshots work

Snapshots are **automatically deduplicated** to save storage space and reduce network transfer costs. To back up an index, a snapshot makes a copy of the index’s [segments](/manage-data/data-store/near-real-time-search.md) and stores them in the snapshot repository. Since segments are immutable, the snapshot only needs to copy any new segments created since the repository’s last snapshot.

Each snapshot is **logically independent**. When you delete a snapshot, {{es}} only deletes the segments used exclusively by that snapshot. {{es}} doesn’t delete segments used by other snapshots in the repository.

### Snapshots and shard allocation [snapshots-shard-allocation]

A snapshot copies segments from an index’s primary shards. When you start a snapshot, {{es}} immediately starts copying the segments of any available primary shards. If a shard is starting or relocating, {{es}} will wait for these processes to complete before copying the shard’s segments. If one or more primary shards aren’t available, the snapshot attempt fails.

Once a snapshot begins copying a shard’s segments, {{es}} won’t move the shard to another node, even if rebalancing or shard allocation settings would typically trigger reallocation. {{es}} will only move the shard after the snapshot finishes copying the shard’s data.

### Snapshot start and stop times

A snapshot doesn’t represent a cluster at a precise point in time. Instead, each snapshot includes a start and end time. The snapshot represents a view of each shard’s data at some point between these two times.

## Snapshot compatibility

To restore a snapshot to a cluster, the versions for the snapshot, cluster, and any restored indices must be compatible.

### Snapshot version compatibility [snapshot-restore-version-compatibility]

You can’t restore a snapshot to an earlier version of {{es}}. For example, you can’t restore a snapshot taken in 7.6.0 to a cluster running 7.5.0.

### Index compatibility

Any index you restore from a snapshot must also be compatible with the current cluster’s version. If you try to restore an index created in an incompatible version, the restore attempt fails.

The following table shows whether an index can be restored to a given cluster version. Find your index’s creation version in the left column and your cluster version (which is the restore target version) across the top. For example, an index created in 6.8 can be restored to a {{version.stack.base}}–{{version.stack}} cluster (✅) but not to a 7.0–7.1 cluster (❌).

:::{table}
:widths: 3-2-1-2-2-1-1

|                       |     |        |       |          |         |     |
|-----------------------|-----|--------|-------|----------|---------|-----|
|                       | Restore to <br> {{version.stack.base}}–{{version.stack}} |  8.3–8.19 | 8.0–8.2 |  7.2–7.17 | 7.0–7.1  | 6.8  |
| Index created in version |  |  |  |  |  |  |
| 5.0–5.6               | ✅ ^1^                                   | ✅ ^1^   | ❌      | ❌       | ❌      | ✅  |
| 6.0–6.7               | ✅ ^1^                                   | ✅ ^1^   | ❌      | ✅       | ✅      | ✅  |
| 6.8                   | ✅ ^1^                                   | ✅ ^1^   | ❌      | ✅       | ❌      | ✅  |
| 7.0–7.1               | ✅ ^1, 2^                                | ✅       | ✅      | ✅       | ✅      | ❌  |
| 7.2–7.17              | ✅ ^1, 2^                                | ✅       | ✅      | ✅       | ❌      | ❌  |
| 8.0–8.19              | ✅                                       | ✅       | ✅      | ❌       | ❌      | ❌  |
| {{version.stack.base}}–{{version.stack}} | ✅                            | ❌       | ❌      | ❌       | ❌      | ❌  |
:::


^1^ $$$footnote-1$$$ Supported with [archive indices](/deploy-manage/upgrade/deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md).

^2^ $$$footnote-2$$$ Supported with [searchable snapshots](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md).

You can’t restore an index to an earlier version of {{es}}. For example, you can’t restore an index created in 8.18.0 to a cluster running 8.15.0.


#### Restoring incompatible indices

A compatible snapshot can contain indices created in an older incompatible version. To restore these incompatible indices, you must take additional steps. For example, a snapshot of a 7.17 cluster might contain an index created in 6.8. Restoring the 6.8 index to an 8.18 cluster fails unless you use the [archive functionality](/deploy-manage/upgrade/deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md). To restore a 7.17 index to a 9.0 cluster, you can use the [archive functionality](/deploy-manage/upgrade/deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md) or [searchable snapshots](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md). Keep this in mind if you take a snapshot before upgrading a cluster.

To ensure index compatibility, you can first restore the index to another cluster running the latest version of {{es}} that’s compatible with both the index and your current cluster. You can then use [reindex-from-remote](https://www.elastic.co/guide/en/elasticsearch/reference/8.18/docs-reindex.html#reindex-from-remote) to rebuild the index on your current cluster. Reindex from remote is only possible if the index’s [`_source`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md) is enabled.

Reindexing from remote can take significantly longer than restoring a snapshot. Before you start, test the reindex from remote process with a subset of the data to estimate your time requirements.

### {{kib}} compatibility

{{es}} and {{kib}} apply different compatibility rules to restored snapshots. A restore that {{es}} accepts can still fail when {{kib}} starts.

{{es}} can typically read data from indices created in a previous major version. For example, restoring a snapshot from an 8.1.0 cluster to a 9.2.4 cluster can succeed at the {{es}} layer, but can fail at the {{kib}} layer. This might happen due to an additional check {{kib}} applies on startup: it inspects version aliases on the `.kibana` index and runs saved object migrations. 

If the restored {{kib}} system indices, such as `.kibana` and `.kibana_task_manager`, were last written by a version older than 8.18.0, {{kib}} 9.x doesn't start the migrations and reports an error similar to:

```
FATAL  Error: Kibana 8.1.0 deployment detected. Please upgrade to Kibana 8.18.0 or newer before upgrading to 9.x series.
```

Restoring an old snapshot directly to a 9.x cluster is not a shortcut around the normal [upgrade paths](/deploy-manage/upgrade.md#upgrade-paths). It is recommended you upgrade to the latest compatible minor release before a major upgrade, even when you use snapshots to move data between clusters.

#### Move {{kib}} configuration and saved objects across major versions [move-kibana-config-saved-objects]

To make the {{kib}} state from an older 8.x snapshot compatible with a 9.x cluster, restore and migrate to an intermediate 8.19.x cluster first, then create a snapshot on the intermediate cluster, and then restore again on the target version:

1. [Restore the snapshot](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md) to a cluster running {{kib}} 8.19.x, or, if your target is 9.0.x, to a cluster running 8.18.x, as described in [Prepare to upgrade](/deploy-manage/upgrade/prepare-to-upgrade.md).
2. Start {{kib}} on the intermediate cluster and wait for startup to complete. During the startup, {{kib}} detects data from a previous compatible version and runs saved object migrations, similar to what would happen during a {{kib}} upgrade. This process rewrites the `.kibana` system indices from their restored version (for example, 8.1.0) to the 8.19.x format, which is fully compatible with 9.x. {{es}} does not run these migrations during a snapshot restore.
3. [Take a new snapshot](/deploy-manage/tools/snapshot-and-restore/create-snapshots.md) of the migrated cluster, then restore that snapshot to your 9.x cluster. Start {{kib}} and wait for the startup to complete. During startup, {{kib}} runs saved object migrations, as it would when upgrading from 8.19.x to 9.x.

For example, to restore the {{kib}} state from an 8.1.0 snapshot to a 9.2.4 cluster, restore the 8.1.0 snapshot to an 8.19.x cluster, let {{kib}} complete its startup migrations, snapshot the 8.19.x cluster, restore that snapshot to 9.2.4, and let {{kib}} perform the latest data migrations.

Alternatively, if you only need to recover data and can accept a fresh {{kib}} setup, restore the snapshot without the `kibana` feature state.

:::{admonition} Roll back after a failed upgrade
The steps described in [moving the {{kib}} configuration and saved objects across major versions](#move-kibana-config-saved-objects) move {{kib}} state forward to a newer major version. Don't use these steps to roll back after a failed upgrade.

To roll back {{kib}}, restore the `kibana` feature state from a snapshot taken immediately before the failed upgrade, then start {{kib}} on the version that was running before that upgrade attempt. For more information, refer to [Roll back {{kib}}](/deploy-manage/upgrade/deployment-or-cluster/kibana-roll-back.md).
:::

## Warnings

### Other backup methods

**Taking a snapshot is the only reliable and supported way to back up a cluster.** You cannot back up an {{es}} cluster by making copies of the data directories of its nodes. There are no supported methods to restore any data from a filesystem-level backup. If you try to restore a cluster from such a backup, it may fail with reports of corruption or missing files or other data inconsistencies, or it may appear to have succeeded having silently lost some of your data.

A copy of the data directories of a cluster’s nodes does not work as a backup because it is not a consistent representation of their contents at a single point in time. You cannot fix this by shutting down nodes while making the copies, nor by taking atomic filesystem-level snapshots, because {{es}} has consistency requirements that span the whole cluster. You must use the built-in snapshot functionality for cluster backups.

### Repository contents [snapshot-repository-contents]

**Don’t modify anything within the repository or run processes that might interfere with its contents.** If something other than {{es}} modifies the contents of the repository then future snapshot or restore operations may fail, reporting corruption or other data inconsistencies, or may appear to succeed having silently lost some of your data.

You may however safely [restore a repository from a backup](snapshot-and-restore/self-managed.md#snapshots-repository-backup) as long as

1. The repository is not registered with {{es}} while you are restoring its contents.
2. When you have finished restoring the repository its contents are exactly as they were when you took the backup.

If you no longer need any of the snapshots in a repository, unregister it from {{es}} before deleting its contents from the underlying storage.

Additionally, snapshots may contain security-sensitive information, which you may wish to [store in a dedicated repository](snapshot-and-restore/create-snapshots.md#cluster-state-snapshots).
