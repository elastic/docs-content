---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-azure-snapshotting.html
applies_to:
  deployment:
    ece: 
---

# Azure Storage repository [ece-configure-azure-snapshotting]

With Elastic Cloud Enterprise, you can enable your Elasticsearch clusters to regularly snapshot data to Microsoft Azure Storage.


## Add the Azure repository [ece_add_the_azure_repository]

Add your Azure Storage Container as a repository to the platform:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. Go to **Platform > Repositories** and add the following snapshot repository configuration under the advanced mode:

    If needed, set additional options for configuring chunk_size, compressions, and retries. Check the [supported settings](/deploy-manage/tools/snapshot-and-restore/azure-repository.md#repository-azure-repository-settings).

    ```json
    {
      "type": "azure",
      "settings": {
        "account": "AZURE STORAGE ACCOUNT NAME",
        "sas_token": "AZURE SAS_TOKEN",
        "container": "BACKUP-CONTAINER"
      }
    }
    ```


Snapshots are stored in the container you provide. Use the repository name you define here to configure your Elasticsearch clusters for snapshotting to this repository.


## Configure your deployment for Azure snapshots [ece_configure_your_deployment_for_azure_snapshots]

To save deployment snapshots to the Azure repository:

1. Configure your deployment to [snapshot to the Azure repository](cloud-enterprise.md).

The cluster should then have snapshots enabled and and begins snapshotting immediately. You can configure the how frequently snapshotting occurs on the **Snapshots** in the **Elasticsearch** menu.

