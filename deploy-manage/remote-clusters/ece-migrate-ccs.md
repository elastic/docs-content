---
navigation_title: Migrate from the CCS deployment template
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-migrate-ccs.html
applies_to:
  deployment:
    ece: ga
products:
  - id: cloud-enterprise
---

# Migrate from the legacy cross-cluster search deployment template in {{ece}} [ece-migrate-ccs]

The legacy cross-cluster search deployment template was removed in {{ece}} 3.0. You no longer need a dedicated template to search across deployments. Instead, you can now use any template to [configure remote clusters](ece-enable-ccs.md) and search across them. Existing deployments created using this template are not affected, but they are required to migrate to another template before upgrading to {{stack}} 8.x.

::::{important}
This guide only applies to {{ece}} 3.x installations and to deployments on {{stack}} versions earlier than 8.0 that were created using the legacy cross-cluster search template.
::::

Follow these instructions to migrate your existing CCS deployment that uses the legacy cross-cluster search template and its data to a new deployment.

## Use a snapshot to migrate deployments that use the cross-cluster search deployment template [ece-migrate-ccs-deployment-using-snapshot]

You can make this change in the user Cloud UI. The only drawback of this method is that it changes the URL used to access the {{es}} cluster and {{kib}}.

1. The first step for any approach is to remove the remote clusters from your deployment. You will need to add them back later.
2. From the deployment menu, open the **Snapshots** page and click **Take Snapshot now**. Wait for the snapshot to finish.
3. From the main **Deployments** page, click **Create deployment**. Next to **Settings** toggle on **Restore snapshot data**, and then select your deployment and the snapshot that you created.

   :::{image} /deploy-manage/images/cloud-enterprise-ce-create-from-snapshot-updated.png
   :alt: Create a Deployment using a snapshot
   :screenshot:
   :::

4. Finally, [configure the remote clusters](/deploy-manage/remote-clusters/ece-remote-cluster-other-ece.md).

