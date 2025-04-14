---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-delete-deployment.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-delete-deployment.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-terminate-deployment.html
  - https://www.elastic.co/guide/en/cloud/current/ec-delete-deployment.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-restore-deployment.html
  - https://www.elastic.co/guide/en/cloud/current/ec-billing-stop.html
navigation_title: "Delete an orchestrated deployment"
applies_to:
  deployment:
    ess:
    ece:
    eck:
  serverless:
---

# Delete an orchestrated deployment

This page provides instructions for deleting several types of cloud deployments, and outlines key considerations before proceeding.

## {{ech}} [elastic-cloud-hosted]

To delete an {{ech}} deployment:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the deployment overview page, select **Actions**, then select **Delete deployment** and confirm the deletion.

When you delete your deployment, billing stops immediately, rounding up to the nearest hour.

:::{{warning}}
When deployments are deleted, we erase all data on disk, including snapshots. Snapshots are retained for very a limited amount of time post deletion and we cannot guarantee that deleted deployments can be restored from snapshots for this reason. If you accidentally delete a deployment, contact support as soon as possible to increase the likelihood of restoring your deployment.
:::

:::{{tip}}
If you want to keep the snapshot for future purposes even after the deployment deletion, you should [use a custom snapshot repository](/deploy-manage/tools/snapshot-and-restore/elastic-cloud-hosted.md).
:::

## Serverless

To delete a {{serverless-full}} project:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your project on the home page in the **Serverless Projects** card and select **Manage** to access it directly. Or, select **Serverless Projects** to go to the projects page to view all of your projects.
3. Select **Actions**, then select **Delete project** and confirm the deletion.

:::{warning}
All data is lost. Billing for usage is by the hour and any outstanding charges for usage before you deleted the project will still appear on your next bill.
:::

## {{ece}}

### Delete a deployment

To delete an {{ece}} deployment:

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. Terminate the deployment.
4. Select **Delete deployment** and follow the steps to delete the deployment permanently.

:::{warning}
Deleting a deployment cannot be undone.
:::

### Terminate a deployment

Terminating a deployment stops all running instances and **deletes all data**. Only configuration information is saved so that you can restore the deployment in the future. If there is [a snapshot repository associated](/deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md) with the {{es}} cluster and at least one snapshot has been taken, you can restore the cluster with the same indices later.

To terminate an {{ece}} deployment,

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. In the **Deployment Management** section, select **Terminate deployment**.


### Restore a deployment

You can restore a deployment that was previously terminated to its original configuration. Note that the data that was in the deployment is not restored, since it is deleted as part of the termination process. If you have a snapshot, you can [restore it](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md) to recover the {{es}} indices.

To restore a terminated deployment,

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.
    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.
3. In the **Deployment Management** section, select **Restore** and then acknowledge the confirmation message.

## {{eck}} [elastic-cloud-kubernetes]

To delete a deployment managed by {{eck}}, remove the corresponding {{es}}, {{kib}}, and any other related custom resources from your Kubernetes cluster. This action deletes all associated pods and their persistent data.

To delete an {{es}} cluster created with {{eck}}:

1. Run the following command to delete the {{es}} custom resource:

   ```shell
   kubectl delete elasticsearch <elasticsearch-resource-name>
   ```
   For example:

   ```shell
   kubectl delete elasticsearch test-deployment
   ```
   :::{warning}
   This deletes the custom resource and all associated resources, such as {{es}} nodes, services, and persistent data volumes. By default, this also deletes the data stored in those volumes, but you can [configure](/deploy-manage/deploy/cloud-on-k8s/volume-claim-templates.md#k8s_controlling_volume_claim_deletion) the `volumeClaimDeletePolicy` field in the {{es}} resource manifest to retain the volumes if you plan to recreate the cluster later.
   :::


2. If you also deployed {{kib}} or other stack components, delete those resources as well:

   ```shell
   kubectl delete kibana <kibana-resource-name>
   ```
   
:::{{tip}}
To fully uninstall {{eck}} from your cluster including all managed resources and the ECK operator, refer to the [](/deploy-manage/uninstall/uninstall-elastic-cloud-on-kubernetes.md) guide.
:::
