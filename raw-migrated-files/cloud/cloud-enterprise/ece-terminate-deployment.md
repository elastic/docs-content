# Terminate a deployment [ece-terminate-deployment]

Terminating a deployment stops all running instances and **deletes all data**. Only configuration information is saved so that you can restore the deployment in the future. If there is [a snapshot repository associated](../../../deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md) with the Elasticsearch cluster and at least one snapshot has been taken, you can restore the cluster with the same indices later.

To terminate a deployment in Elastic Cloud Enterprise:

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. In the **Deployment Management** section, select **Terminate deployment**.

