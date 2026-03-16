---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-azure-snapshotting.html
applies_to:
  deployment:
    ece:
products:
  - id: cloud-enterprise
---

# Azure Storage repository [ece-configure-azure-snapshotting]

This guide focuses on registering an Azure snapshot repository at the {{ece}} (ECE) platform level. Platform-level repositories can be assigned to deployments and are used by ECE to automatically manage snapshots through the `found-snapshots` repository.

If you have custom requirements or deployment-specific use cases that are independent of the ECE-managed automation, you can also register snapshot repositories directly at the deployment level. To do that, follow the [{{ech}} guide for Azure Blob Storage](/deploy-manage/tools/snapshot-and-restore/ec-azure-snapshotting.md), which is also applicable to {{ece}} deployments.

At the ECE platform level, you can enable your {{es}} clusters to regularly snapshot data to Microsoft Azure Storage.

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

  3. Select **Save**.

## Configure your deployment to use the repository [ece_configure_your_deployment_for_azure_snapshots]

After adding the snapshots repository, [configure your deployment to use it](./cloud-enterprise.md#ece-manage-repositories-clusters). Once configured, snapshots run automatically according to the scheduled interval. You can update this schedule from the **Snapshots** section in the **{{es}}** menu of your deployment page.