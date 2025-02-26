# Snapshot and restore [ec-snapshot-restore]

Snapshots are an efficient way to ensure that your Elasticsearch indices can be recovered in the event of an accidental deletion, or to migrate data across deployments.

The information here is specific to managing repositories and snapshots in {{ech}}. We also support the Elasticsearch snapshot and restore API to back up your data. For details, consult the [Snapshot and Restore documentation](../../../deploy-manage/tools/snapshot-and-restore.md).

When you create a cluster in {{ech}}, a default repository called `found-snapshots` is automatically added to the cluster. This repository is specific to that cluster: the deployment ID is part of the repository’s `base_path`, i.e., `/snapshots/[cluster-id]`.

::::{important} 
Do not disable or delete the default `cloud-snapshot-policy` SLM policy, and do not change the default `found-snapshots` repository defined in that policy. These actions are not supported.

The default policy and repository are used when creating a new deployment from a snapshot, when restoring a snapshot to a different deployment, and when taking automated snapshots in case of deployment changes. You can however customize the snapshot retention settings in that policy to adjust it to your needs.

To use a custom snapshot repository, you can [register a new snapshot repository](../../../deploy-manage/tools/snapshot-and-restore/self-managed.md) and [create another SLM policy](../../../deploy-manage/tools/snapshot-and-restore/create-snapshots.md#create-slm-policy).

::::


To get started with snapshots, check out the following pages:

* [Add your own custom repositories](../../../deploy-manage/tools/snapshot-and-restore/elastic-cloud-hosted.md) to snapshot to and restore from.
* To configure your cluster snapshot settings, see the [Snapshot and Restore documentation](../../../deploy-manage/tools/snapshot-and-restore.md).
* [*Restore a snapshot across clusters*](../../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md).

