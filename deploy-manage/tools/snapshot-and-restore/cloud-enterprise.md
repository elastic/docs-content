---
navigation_title: "Elastic Cloud Enterprise"

applies_to:
  deployment:
    ece: 
---

# Manage snapshot repositories in Elastic Cloud Enterprise [ece-manage-repositories]

Snapshots enable you to back up and restore Elasticsearch indices, protecting data from accidental deletion and supporting migration between clusters. In Elastic Cloud Enterprise (ECE), snapshot repositories are managed at the platform level and can be assigned to individual deployments.

When a repository is assigned to a deployment, a snapshot is taken every 30 minutes by default. The snapshot interval can be adjusted per deployment.

## Supported repository types

Elastic Cloud Enterprise installations support the following {{es}} snapshot repository types:

* AWS S3
* Azure Blob Storage
* Google Cloud Storage
* Minio S3

::::{note}
No repository types other than those listed are supported in the Elastic Cloud Enterprise platform, even if they are supported by {{es}}.
::::


For more details about how snapshots are used with Elasticsearch, check [Snapshot and Restore](/deploy-manage/tools/snapshot-and-restore.md). You can also review the official documentation for these storage repository options:

* [Amazon S3 documentation](https://docs.aws.amazon.com/s3/)
* [Microsoft Azure Blob Storage documentation](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction)
* [Google Cloud Storage documentation](https://cloud.google.com/storage/docs/)

::::{tip}
If you are installing ECE without internet access (commonly called an offline or air-gapped installation), you will need to use an on-premise storage service.  We suggest that you use [Minio](https://www.minio.io/). For our installation notes, check [Snapshotting to Minio On-Premise Storage](minio-on-premise-repository.md).
::::


## Add snapshot repository configurations [ece-manage-repositories-add]

The following guides provide instructions on adding a snapshot repository in ECE for all supported types:

* [AWS S3](/deploy-manage/tools/snapshot-and-restore/ece-aws-custom-repository.md) 
* [Azure](/deploy-manage/tools/snapshot-and-restore/azure-storage-repository.md)
* [Google Cloud Storage](/deploy-manage/tools/snapshot-and-restore/google-cloud-storage-gcs-repository.md)
* [Minio](/deploy-manage/tools/snapshot-and-restore/minio-on-premise-repository.md)

## Edit snapshot repository configurations [ece_edit_snapshot_repository_configurations]

To edit a snapshot repository configuration from your Elastic Cloud Enterprise installation:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Repositories**.
3. Select **Edit** to modify a snapshot repository configuration.
4. Select **Save**.


## Delete snapshot repository configurations [ece_delete_snapshot_repository_configurations]

Deleting a snapshot repository configuration does not remove the snapshot repository itself from S3. Only the configuration that enables Elastic Cloud Enterprise to access the repository is removed. Existing snapshots are also retained and need to be deleted separately if you no longer need them.

To delete a snapshot repository configuration from your Elastic Cloud Enterprise installation:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Repositories**.
3. Find the repository name that you want to remove.
4. Run the following command against the repository name:

    ```sh
    curl -s -XDELETE -u USER:PASSWORD https://COORDINATOR_HOST:12443/api/v1/platform/configuration/snapshots/repositories/REPOSITORY_NAME
    ```

    ::::{note}
    The user must have sufficient privileges, such as the `admin` user.
    ::::



## Manage Elasticsearch cluster repositories [ece-manage-repositories-clusters]

You might need to update existing Elasticsearch clusters to use a different snapshot repository for one of the following reasons:

* If you do not want all snapshots for a specific Elasticsearch cluster to go into the same bucket as your other clusters, you can add a new snapshot repository configuration with separate permissions and then change your Elasticsearch cluster to use the new repository.
* If you created an Elasticsearch cluster with no snapshot repository configured, you can add a repository later on. Elastic Cloud Enterprise will start taking snapshots of the cluster automatically.

To change the snapshot repository for an existing Elasticsearch cluster:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. Optional: If you need to use a repository that is not yet listed, add a snapshot repository configuration first.
3. From the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

4. From the **Elasticsearch** menu, select **Snapshots**.
5. Under **Snapshot repository**, choose a different repository and select **Save repository**.

Future snapshots will be sent to the new repository.




