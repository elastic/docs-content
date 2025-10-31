---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-restore-snapshots-into-new-deployment.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-restore-snapshots-into-new-deployment.html
applies_to:
  deployment:
    ess:
    ece:
products:
  - id: cloud-hosted
  - id: cloud-enterprise
---

# Restore snapshot into a new deployment [ece-restore-snapshots-into-new-deployment]

1. First, [create a new deployment](../../deploy/cloud-enterprise/create-deployment.md) and select **Restore snapshot data**. Select the deployment that you want to restore a snapshot *from*. If you don’t know the exact name, you can enter a few characters and then select from the list of matching deployments.
2. Select the snapshot that you want to restore from. If none is chosen, the latest successful snapshot from the cluster you selected is restored on the new cluster when you create it.
   **Please note that this only supports snapshots created in the `found-snpashots` repository**.

    ![Restoring from a snapshot](/deploy-manage/images/cloud-enterprise-restore-from-snapshot.png "")

4. Manually recreate users using the X-Pack security features or using Shield on the new cluster. User information is not included when you restore across clusters.

