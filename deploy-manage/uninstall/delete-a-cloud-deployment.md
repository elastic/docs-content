---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-delete-deployment.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-delete-deployment.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-terminate-deployment.html
  - https://www.elastic.co/guide/en/cloud/current/ec-delete-deployment.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-restore-deployment.html
  - https://www.elastic.co/guide/en/cloud/current/ec-billing-stop.html
navigation_title: "Delete a cloud deployment"
applies_to:
  deployment:
    ess:
    ece:
  serverless:
---

# Delete an Enterprise or Hosted deployment or a Serverless project

This page provides instructions for deleting several types of cloud deployments, and outlines key considerations before proceeding.

## {{ech}} [elastic-cloud-hosted]

To delete an {{ech}} deployment:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the deployment overview page, select **Actions**, then select **Delete deployment** and confirm the deletion.

When you delete your deployment, billing stops immediately, rounding up to the nearest hour.

:::{{warning}}
When deployments are deleted, we erase all data on disk, including snapshots. Snapshots are retained for very a limited amount of time post deletion and we cannot guarantee that deleted deployments can be restored from snapshots for this reason. If you accidentally delete a deployment, please contact support as soon as possible to increase the likelihood of restoring your deployment.
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

Terminating a deployment stops all running instances and **deletes all data**. Only configuration information is saved so that you can restore the deployment in the future. If there is [a snapshot repository associated](/deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md) with the Elasticsearch cluster and at least one snapshot has been taken, you can restore the cluster with the same indices later.

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

