# Delete your deployment [ech-delete-deployment]

To do that, select **Delete deployment** from the deployment overview page.

When you delete your deployment, billing stops immediately rounding up to the nearest hour.

::::{warning} 
When deployments are deleted, we erase all data on disk, including snapshots. Snapshots are retained for very a limited amount of time post deletion and we cannot guarantee that deleted deployments can be restored from snapshots for this reason. If you accidentally delete a deployment, please contact support as soon as possible to increase the likelihood of restoring your deployment.
::::


::::{tip} 
If you want to keep the snapshot for future purposes even after the deployment deletion, you should [use a custom snapshot repository](../../../deploy-manage/tools/snapshot-and-restore/elastic-cloud-hosted.md).
::::


Billing restarts as soon as the deployment is restored.

