---
navigation_title: Migrate data using snapshots
applies_to:
  stack: ga
products:
  - id: elasticsearch
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
---

# Migrate {{es}} data with minimal downtime using snapshots [migrate-elasticsearch-data-with-minimal-downtime]

When moving your data and services from one {{es}} cluster to another, such as to {{ech}}, {{ece}}, new on-premises hardware, or any other {{es}} environment, you can migrate with minimal downtime using incremental snapshots. 

Migrating with incremental snapshots is useful when you want to:

* Migrate all data in your indices and configurations, such as roles and {{kib}} dashboards, from the old cluster to a new cluster.
* Ensure data ingestion, such as {{ls}} or {{beats}}, and data consumption, such as applications using {{es}} as a backend, seamlessly migrate to the new cluster.
* Maintain data consistency and minimize disruption.  

## How incremental snapshots work [how-incremental-snapshots-work]
Incremental snapshots save only the data that has changed since the last snapshot. The first snapshot is a full copy of the data. Each subsequent snapshot contains only the differences, which makes creating and restoring snapshots faster and more efficient over time. 

When restoring, {{es}} copies only the missing data segments from the snapshot repository to the new cluster local storage. When the changes between snapshots are small, the restore process is significantly faster. 

By taking and restoring incremental snapshots in sequence, you can keep a new cluster closely synchronized with the old cluster, allowing you to migrate most of your data ahead of time and minimize downtime during the final cutover. 

For more information about migrating your data with snapshot and restore, check [Snapshot and restore](/deploy-manage/tools/snapshot-and-restore.md).

## Before you begin [incremental-snapshots-before-you-begin]
Before you migrate, review the prerequisites and requirements.

### Prerequisites
* Learn how to [set up and manage snapshot repositories](/deploy-manage/tools/snapshot-and-restore/manage-snapshot-repositories.md). 
* If restoring to a different cluster, review [Restore to a different cluster](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#restore-different-cluster).
* As an alternative migration method, you can [reindex from a remote cluster](/manage-data/migrate/migrate-data-using-reindex-api.md).

### Requirements
* **Cluster size** – The new cluster must be the same size or larger than the old cluster. 
* **Version compatibility** – Both clusters must use [compatible {{es}} versions](/deploy-manage/tools/snapshot-and-restore.md#snapshot-compatibility). To check if your cluster versions are compatible, check [Snapshot version compatibility](/deploy-manage/tools/snapshot-and-restore.md#snapshot-restore-version-compatibility).
* **Storage requirements** - Ensure sufficient repository storage. Usage grows with snapshot frequency and data volume. 
* **Network overhead** – Transferring snapshots across networks, regions, or providers can be time consuming and incur costs.
* **Resource usage** – Snapshot and restore operations can be resource intensive and affect cluster performance.
* **Custom integrations** – Some integrations that use the {{es}} API directly, such as the [Elasticsearch Java Client library](elasticsearch-java://reference/index.md), can require additional handling during cutover.

::::{note}
For {{ece}}, Amazon S3 is the most common snapshot storage, but you can restore from any accessible external storage that contains your {{es}} snapshots.
::::

## Recommended migration timeline [recommended-migration-timeline]
Tp complete the migration with minimal downtime, use incremental snapshots. While the exact sequence may differ depending on your infrastructure and operational requirements, you can use the recommended migration timeline as a reliable baseline that you can adapt. Adjust the steps and times to fit your own operational needs.

1. **09:00**: Take the initial full snapshot of the old cluster. You can also take the initial full snapshot the day before.
2. **09:30**: Restore the snapshot to the new cluster.
3. **09:55**: Take another snapshot of the old cluster and restore it to the new cluster. Repeat this process until the snapshot and restore operations take only a few seconds or minutes. Remember that when restoring indices that _already_ exist in the new cluster (for example, to pull in recently copied data), they first need to be [closed](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#considerations). Also, remember that the restore operation automatically opens indices, so you will likely need to close the actively written ones after restoring them.
4. **10:15**: Perform the final cutover.
    1. In the old cluster, pause indexing or set indices to read-only. For details on setting indices to read-only to safely pause indexing during migration, check [Index lifecycle actions: Read-only](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-readonly.md).
    2. Take a final snapshot. 
    3. Restore the snapshot to the new cluster. Again, remember that to restore indices that already exist, they first need to be closed.
    4. Change ingestion and querying to the new cluster. 
    5. Open the indices in the new cluster. 


## Migrate your data using snapshot and restore [migrate-data-snapshot-restore]

Follow these steps to migrate your {{es}} data.

### Step 1: Set up the repository in the new cluster [migrate-repo-setup]

In this step, you’ll configure a read-only snapshot repository in the new cluster that points to the storage location used by the old cluster. This allows the new cluster to access and restore snapshots created in the original environment.

::::{tip}
If your new deployment cannot connect to the same repository used by your self-managed cluster, for example if it's a private Network File System (NFS) share, consider one of the following alternatives:

* [Back up your repository](/deploy-manage/tools/snapshot-and-restore/self-managed.md#snapshots-repository-backup) to a supported storage system such as AWS S3, Google Cloud Storage, or Azure Blob Storage, and then configure your new cluster to use that location for the data migration.
* Expose the repository contents over `ftp`, `http`, or `https`, and use a [read-only URL repository](/deploy-manage/tools/snapshot-and-restore/read-only-url-repository.md) type in your new deployment to access the snapshots.
::::

1. On your old {{es}} cluster, retrieve the snapshot repository configuration:

    ```sh
    GET /_snapshot/_all
    ```

    Take note of the repository name and type (for example, `s3`, `gcs`, or `azure`), its base path, and any additional settings. Authentication credentials are often stored in the [secure settings](/deploy-manage/security/secure-settings.md) on each node. You’ll need to replicate all this configuration when registering the repository in the new ECH or ECE deployment.

    If your old cluster has multiple repositories configured, identify the repository with the snapshots containing the data that you want to migrate.

2. Add the snapshot repository on the new cluster.

    Considerations:

      * If you're migrating [searchable snapshots](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md), the repository name must be identical in the old and new clusters.
      * If the old cluster still has write access to the repository, register the repository as read-only to avoid data corruption. You can do this using the `readonly: true` option.

    To connect the existing snapshot repository to your new deployment, follow the steps for the storage provider where the repository is hosted:

    * **Amazon Web Services (AWS) Storage**
        * [Store credentials in the keystore](/deploy-manage/tools/snapshot-and-restore/ec-aws-custom-repository.md#ec-snapshot-secrets-keystore)
        * [Create the repository](/deploy-manage/tools/snapshot-and-restore/ec-aws-custom-repository.md#ec-create-aws-repository)
    * **Google Cloud Storage (GCS)**
        * [Store credentials in the keystore](/deploy-manage/tools/snapshot-and-restore/ec-gcs-snapshotting.md#ec-configure-gcs-keystore)
        * [Create the repository](/deploy-manage/tools/snapshot-and-restore/ec-gcs-snapshotting.md#ec-create-gcs-repository)
    * **Azure Blob Storage**
        * [Store credentials in the keystore](/deploy-manage/tools/snapshot-and-restore/ec-azure-snapshotting.md#ec-configure-azure-keystore).
        * [Create the repository](/deploy-manage/tools/snapshot-and-restore/ec-azure-snapshotting.md#ec-create-azure-repository).

    ::::{important}
    Although these instructions focus on {{ech}}, you should follow the same steps for {{ece}} by configuring the repository directly **at the deployment level**.

    **Do not** configure the repository as an [ECE-managed repository](/deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md), which is intended for automatic snapshots of deployments. In this case, you need to add a custom repository that already contains snapshots from another cluster.
    ::::


### Step 2: Run the snapshot restore [migrate-restore]

After you have registered and verified the repository, you are ready to restore any data from any of its snapshots to your new cluster.

You can run a restore operation using the {{kib}} Management UI, or using the {{es}} API. Refer to [Restore a snapshot](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md) for more details, including API-based examples.

For details about the contents of a snapshot, refer to [](/deploy-manage/tools/snapshot-and-restore.md#snapshot-contents).

To start the restore process:

1. Open Kibana and go to the **Snapshot and Restore** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under the **Snapshots** tab, you can find the available snapshots from your newly added snapshot repository. Select any snapshot to view its details, and from there you can choose to restore it.
3. Select **Restore**.
4. Select the index or indices you wish to restore.
5. Optionally, configure additional restore options, such as **Restore aliases**, **Restore global state**, or **Restore feature state**.
6. Select **Restore snapshot** to begin the process.

7. Verify that each restored index is available in your deployment. You can do this using {{kib}} **Index Management** UI, or by running this query:

    ```sh
    GET INDEX_NAME/_search?pretty
    ```

    If you have restored many indices you can also run `GET _cat/indices?s=index` to list all indices for verification.







## Additional support [incremental-snapshots-additional-support]
To get expert assistance for your {{es}} migrations, go to [Elastic Professional Services](https://www.elastic.co/consulting).
