---
applies_to:
  deployment:
    ece: ga
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-migrate-ccs.html
navigation_title: "Migrate the CCS deployment template"
---

# Migrate the cross-cluster search deployment template [ece-migrate-ccs]

The cross-cluster search deployment template is now deprecated was removed in {{ece}} 3.0. You no longer need to use the dedicated cross-cluster template to search across deployments. Instead, you can now use any template to [configure remote clusters](ece-enable-ccs.md) and search across them. Existing deployments created using this template are not affected, but they are required to migrate to another template before upgrading to {{stack}} 8.x.

In order to migrate your existing CCS deployment using the CCS Deployment template to the new mechanism which supports CCR and cross-environment remote clusters you will need to migrate your data a new deployment [following these steps](#ece-migrate-ccs-deployment-using-snapshot).


## Use a snapshot to migrate deployments that use the cross-cluster search deployment template [ece-migrate-ccs-deployment-using-snapshot]

You can make this change in the user Cloud UI. The only drawback of this method is that it changes the URL used to access the {{es}} cluster and {{kib}}.

1. The first step for any approach is to remove the remote clusters from your deployment. You will need to add them back later.
2. From the deployment menu, open the **Snapshots** page and click **Take Snapshot now**. Wait for the snapshot to finish.
3. From the main **Deployments** page, click **Create deployment**. Next to **Settings** toggle on **Restore snapshot data**, and then select your deployment and the snapshot that you created.

   :::{image} ../../images/cloud-enterprise-ce-create-from-snapshot-updated.png
   :alt: Create a Deployment using a snapshot
   :class: screenshot
   :::

4. Finally, [configure the remote clusters](/deploy-manage/remote-clusters/ece-remote-cluster-other-ece.md).

