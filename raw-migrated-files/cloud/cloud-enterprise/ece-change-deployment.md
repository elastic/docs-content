# Change your deployment configuration [ece-change-deployment]

There are several reasons why you might want to change the configuration of a deployment:

* To increase or decrease deployment capacity by changing the amount of reserved memory and storage.
* To enable [autoscaling](../../../deploy-manage/autoscaling.md) so that available resources for certain deployment components adjust automatically as the demands on them change.
* To enable high availability by adjusting the number of availability zones that your deployment runs in.
* To upgrade to new versions of Elasticsearch. You can upgrade from one major version to another, such as from 7.17 to 8.0, or from one minor version to another, such as 8.9.0 to 8.9.2. You can’t downgrade versions.
* To update Elasticsearch clusters and Kibana after an updated Elastic Stack pack for a particular version has been added to your Elastic Cloud Enterprise installation.
* To change what plugins are available on your deployment.

For single availability zone deployments, there is downtime to portions of your cluster when changes are applied. For HA deployments and with the exception of major version upgrades, we can perform all these changes without interrupting your deployment. During the application of these changes, you can continue to search and index.

Many changes can also be done in bulk: in one action, you can add more memory and storage, upgrade minor versions, adjust the number of plugins and adjust fault tolerance by changing the number of availability zones. Elastic Cloud Enterprise performs all of these changes with a grow-and-shrink operation, making an Elasticsearch cluster and other instances with the new configuration join the existing deployment. After re-joining, updated nodes recover their indexes and start handling requests. When all updated new nodes are ready, the old nodes that were replaced are removed. If you do a major version upgrade, you cannot change the cluster configuration at the same time. Perform these configuration changes separately.

::::{tip} 
When you scale up a deployment, existing data may be migrated to new nodes. For clusters containing large amounts of data, this migration can take some time, especially if your deployment is under a heavy workload. (Is your deployment under a heavy load? You might need to [stop routing requests](../../../deploy-manage/maintenance/ece/deployments-maintenance.md) first.)
::::








