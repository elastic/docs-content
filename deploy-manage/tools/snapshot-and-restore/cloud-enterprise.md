---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-manage-repositories.html
---

# Elastic Cloud Enterprise [ece-manage-repositories]

Snapshot repositories are managed for your entire Elastic Cloud Enterprise installation and can be specified for an Elasticsearch cluster when you create or manage it.

When a repository is specified, a snapshot is taken every 30 minutes by default. The interval can be adjusted on per deployment basis.

Snapshots are configured and restored using the [snapshot and restore feature](../snapshot-and-restore.md).

Elastic Cloud Enterprise installations support the following {{es}} [snapshot repository types](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html#ess-repo-types):

* [Azure](https://www.elastic.co/guide/en/elasticsearch/reference/current/repository-azure.html)
* [Google Cloud Storage](https://www.elastic.co/guide/en/elasticsearch/reference/current/repository-gcs.html)
* [AWS S3](https://www.elastic.co/guide/en/elasticsearch/reference/current/repository-s3.html)

::::{note}
No repository types other than those listed are supported in the Elastic Cloud Enterprise platform, even if they are supported by {{es}}.
::::


To configure Google Cloud Storage (GCS) as a snapshot repository, you must use [Google Default Authentication](https://developers.google.com/identity/protocols/application-default-credentials). To learn more, check [Snapshotting to Google Cloud Storage](google-cloud-storage-gcs-repository.md).

To configure Microsoft Azure Storage as a snapshot repository, refer to [Snapshotting to Azure Storage](azure-storage-repository.md).

For more details about how snapshots are used with Elasticsearch, check [Snapshot and Restore](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-snapshots.html). You can also review the official documentation for these storage repository options:

* [Amazon S3 documentation](http://docs.aws.amazon.com/AmazonS3/latest/dev/Introduction.md)
* [Microsoft Azure storage documentation](https://docs.microsoft.com/en-us/azure/storage/common/storage-quickstart-create-account)
* [Google Cloud Storage documentation](https://cloud.google.com/storage/docs/)

::::{tip}
If you are installing ECE without internet access (commonly called an offline or air-gapped installation), you will need to use an on-premise storage service.  We suggest that you use [Minio](https://www.minio.io/). For our installation notes, check [Snapshotting to Minio On-Premise Storage](minio-on-premise-repository.md).
::::



## Add snapshot repository configurations [ece-manage-repositories-add]

Before any snapshot or restore operation can be performed for Elasticsearch clusters, at least one snapshot repository configuration needs to be added to your Elastic Cloud Enterprise installation.

To add a snapshot repository:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Repositories**.
3. Select **Add Repository** to add an existing repository.
4. Provide a name for the repository configuration.

    ECE Snapshot Repository names are now required to meet the same standards as S3 buckets. Refer to the official AWS documentation on [Bucket naming rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.md).

5. Select one of the supported repository types and specify the necessary settings:

    * Amazon S3 configuration:

        All repository options must be specified, as there are no default values.

        Region
        :   The region where the bucket is located.

        Bucket
        :   The name of the bucket to be used for snapshots.

        Access key
        :   The access key to use for authentication.

        Secret key
        :   The secret key to use for authentication.

    * Advanced configuration:

        Used for Microsoft Azure, Google Cloud Platform, or for some Amazon S3 repositories where you need to provide additional configuration parameters not supported by the S3 repository option. Configurations must be specified in a valid JSON format. For example:

        Amazon S3 (check [supported settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/repository-s3.html#repository-s3-repository)):

        ```json
        {
          "type": "s3",
          "settings": {
            "bucket": "my_bucket_name",
            "region": "us-west"
          }
        }
        ```

        ::::{note}
        Don’t set `base_path` when configuring a snapshot repository for {{ECE}}. {{ECE}} automatically generates the `base_path` for each deployment so that multiple deployments may share the same bucket.
        ::::

6. Select **Save**.


## Edit snapshot repository configurations [ece_edit_snapshot_repository_configurations]

To edit a snapshot repository configuration from your Elastic Cloud Enterprise installation:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Repositories**.
3. Select **Edit** to modify a snapshot repository configuration.

    For available options that you can change, check [Add Snapshot Repository Configurations]().

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
2. Optional: If you need to use a repository that is not yet listed, [add a snapshot repository configuration]() first.
3. From the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

4. From the **Elasticsearch** menu, select **Snapshots**.
5. Under **Snapshot repository**, choose a different repository and select **Save repository**.

Future snapshots will be sent to the new repository.




