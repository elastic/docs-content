---
applies_to:
  deployment:
    ess: 
---

# Configure a snapshot repository using Azure Blob storage [ec-azure-snapshotting]

Configure a custom snapshot repository using your Azure Blob storage account.


## Prepare a container [ec-prepare-azure-container]

Follow the Microsoft documentation to [set up an Azure storage account](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-create) with an access key, and then [create a container](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal).


## Enable the `repository-azure` plugin in Elastic Stack 7.17 and earlier [ec-enable-azure-plugin]

For deployments with **Elastic Stack version 7.17 and earlier**, you’ll need to enable the `repository-azure` plugin to use the Azure repository type. On the Azure platform, the plugin is enabled by default. If your deployment is on AWS or GCP, follow these steps to enable the `repository-azure` plugin:

1. Refer to [Azure Repository Plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/7.17/repository-azure.html) to download the version of the plugin that matches your Elastic Stack version.
2. Upload the plugin to your deployment:

    1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
    2. Open the **Features > Extensions** page and select **Upload extension**.
    3. Specify the plugin name (`repository-azure`) and the version.
    4. Select **An installable plugin (Compiled, no source code)**.
    5. Select **Create extension**.
    6. Navigate back to the **Features > Extensions** page.
    7. Select the extension name.
    8. Drag and drop to upload the `repository-azure` plugin zip file.



### Configure the keystore [ec-configure-azure-keystore]

Create an entry for the Azure client in the Elasticsearch keystore:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Navigate to the **Security** page of the deployment you wish to configure.
3. Locate **Elasticsearch keystore** and select **Add settings**.
4. With **Type** set to **Single string**, add the following keys and their values:

    * `azure.client.secondary.account`
    * `azure.client.secondary.key`

5. Select **Save**.


### Create the repository [ec-create-azure-repository]

1. Open Kibana and go to **Management** > **Snapshot and Restore**.
2. On the **Repositories** tab, select **Register a repository**.
3. Provide a name for your repository and select type **Azure**.
4. Provide the following settings:

    * Client: `secondary`

        * You can also use `default`, but we recommend using `secondary` to ensure that your secure settings are mapped to the correct repository definition.

    * Container: The name of your Azure container
    * base_path: A directory to contain the snapshots

        * This setting is optional. Include a `base_path` if you have multiple clusters writing to the same Azure repository. This ensures that a snapshot won’t overwrite the snapshot metadata for another cluster.

5. Add any other settings that you wish to configure.
6. Select Register.
7. Select **Verify** to confirm that your settings are correct and the deployment can connect to your repository.

Your snapshot repository is now set up using Azure Blob storage! You can use Kibana to manage your snapshots and begin sending Elasticsearch snapshots to your own container. For details, check the [Snapshot and Restore](create-snapshots.md) documentation.

