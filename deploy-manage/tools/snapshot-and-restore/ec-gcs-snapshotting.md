---
applies_to:
  deployment:
    ess: 
---

# Configure a snapshot repository using GCS [ec-gcs-snapshotting]

Configure a custom snapshot repository using your Google Cloud Storage account.


## Set up your service account credentials [ec-gcs-service-account-key]

You’ll need to have an existing Google Cloud account and have the appropriate permissions to generate credentials.

1. Create a [service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) in your Google Cloud project.

    The service account should be configured to have permission to read, write, and list the bucket objects. For more information, refer to [Recommended bucket permission](/deploy-manage/tools/snapshot-and-restore/google-cloud-storage-repository.md#repository-gcs-bucket-permission) in the Elasticsearch docs.

2. Save the service account key in JSON file format. You are going to use it later to configure your Elasticsearch deployment for snapshotting.

For more detailed information on the JSON account service key, refer to [Using a Service Account](/deploy-manage/tools/snapshot-and-restore/google-cloud-storage-repository.md#repository-gcs-using-service-account).


## Prepare a bucket [ec-prepare-gcs-bucket]

Follow the Google Cloud Storage documentation to [create a GCS bucket](https://cloud.google.com/storage/docs/creating-buckets).


## Enable the `repository-gcs` plugin in Elastic Stack 7.17 and earlier [ec-enable-gcs-plugin]

For deployments with **Elastic Stack version 7.17 and earlier**, you’ll need to enable the `repository-gcs` plugin to use the Google Cloud Storage repository type. On Google Cloud Platform, the plugin is enabled by default. If your deployment is on AWS or Azure, follow these steps to enable the `repository-gcs` plugin:

1. Refer to [Google Cloud Storage Repository Plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/7.17/repository-gcs.html) to download the version of the plugin that matches your Elastic Stack version.
2. Upload the plugin to your deployment:

    1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
    2. Open the **Features > Extensions** page and select **Upload extension**.
    3. Specify the plugin name (`repository-gcs`) and the version.
    4. Select **An installable plugin (Compiled, no source code)**.
    5. Select **Create extension**.
    6. Navigate back to the **Features > Extensions** page.
    7. Select the extension name.
    8. Drag and drop to upload the `repository-gcs` plugin zip file.



### Configure the keystore [ec-configure-gcs-keystore]

Create an entry for the GCS client in the Elasticsearch keystore:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Navigate to the **Security** page of the deployment you wish to configure.
3. Locate **Elasticsearch keystore** and select **Add settings**.
4. Enter the **Setting name** `gcs.client.secondary.credentials_file`.
5. With **Type** set to **JSON block / file**, add your [GCS service account key JSON file](#ec-gcs-service-account-key).
6. Select **Save**.


### Create the repository [ec-create-gcs-repository]

1. Open Kibana and go to **Management** > **Snapshot and Restore**.
2. On the **Repositories** tab, select **Register a repository**.
3. Provide a name for your repository and select type **Google Cloud Storage**.
4. Provide the following settings:

    * Client: `secondary`
    * Bucket: Your GCS bucket name
    * Base path: A directory to contain the snapshots

        * This setting is optional. Include a `base_path` if you have multiple clusters writing to the same GCS repository. This ensures that a snapshot won’t overwrite the snapshot metadata for another cluster.

5. Add any other settings that you wish to configure.
6. Select **Register**.
7. Select **Verify** to confirm that your settings are correct and the deployment can connect to your repository.

Your snapshot repository is now set up using GCS! You can use Kibana to manage your snapshots and begin sending Elasticsearch snapshots to your own bucket. For details, check the [Snapshot and Restore](create-snapshots.md) documentation.

