---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-snapshot-repository-azure-migration.html
applies_to:
  deployment:
    ess:
products:
  - id: cloud-hosted
navigation_title: Azure
---

# Repository isolation on Azure [ec-snapshot-repository-azure-migration]

::::{note}
This configuration is automatic for all newly created deployments, but may have to be triggered manually on any existing Azure deployments you have. If a deployment can be moved to a dedicated repository, a notification will show up in the deployments menu under **Elasticsearch** > **Snapshots**.
::::


Azure deployments of your organization in the same region currently may use the same Azure Blob storage container as shared repository to store their snapshots. To make sure that no other deployment can have access to this deployment’s snapshots, you can instead use a dedicated repository for this deployment.

When enabling a dedicated repository for storing snapshots, a configuration change triggers for your deployment and:

* Renames the existing `found-snapshots` repository to `\_clone_<clusterid>`. In this repository, all existing snapshots and searchable snapshots can still be accessed.
* Adds a new (empty) `found-snapshots` repository using a new container.
* Takes a full snapshot in this new `found-snapshots` repository.


## Restoring from a snapshot created before the migration [ec_restoring_from_a_snapshot_created_before_the_migration]

The snapshots are still available and can be restored just like snapshots in `found-snapshots`. You can find more information in [Snapshot and restore](../snapshot-and-restore.md).


## Removing the old repository [ec_removing_the_old_repository]

If you no longer need the old snapshots, you can remove the repository. By doing this, you also prevent accessing snapshots of other deployments from this deployment:

1. From your deployment menu, go to **Elasticsearch** > **Snapshots**.
2. On the **Snapshots** page, **Snapshot repositories of other deployments** shows the old repository.
3. With **Remove Access**, the snapshot repository will be removed.

::::{note}
If the repository is still in use (for example by mounted searchable snapshots), it can’t be removed. Remove any indices stored in this repository first.
::::


:::{image} /deploy-manage/images/cloud-ec-elasticsearch-snapshots-of-other-deployments.png
:alt: View of the old snapshot repository in the Cloud UI
:::

