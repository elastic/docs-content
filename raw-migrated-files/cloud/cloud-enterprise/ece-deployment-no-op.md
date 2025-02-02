# How do I resolve deployment health warnings? [ece-deployment-no-op]

The Elastic Cloud Enterprise **Deployments** page shows the current status of your active deployments. From time to time you may get one or more health warnings, such as the following:

:::{image} ../../../images/cloud-enterprise-ec-ce-deployment-health-warning.png
:alt: A screen capture of the deployment page showing a typical warning: Deployment health warning: Latest change to {{es}} configuration failed.
:::

**Seeing only one warning?**

To resolve a single health warning, we recommended first re-applying any pending changes: Select **Edit** in the deployment menu to open the Edit page and then click **Save** without making any changes. This will check all components for pending changes and will apply the changes as needed. This may impact the uptime of clusters which are not [highly available](../../../deploy-manage/deploy/cloud-enterprise/ece-ha.md).

Re-saving the deployment configuration without making any changes is often all that’s needed to resolve a transient health warning on the UI. Saving will redirect you to the Elastic Cloud Enterprise deployment [Activity page](../../../deploy-manage/deploy/cloud-enterprise/keep-track-of-deployment-activity.md) where you can monitor plan completion. Repeat errors should be investigated; for more information refer to [resolving configuration change errors](../../../troubleshoot/monitoring/node-bootlooping.md).

**Seeing multiple warnings?**

If multiple health warnings appear for one of your deployments, check the list of [Common issues](../../../troubleshoot/deployments/cloud-enterprise/common-issues.md), or [Ask for help](../../../troubleshoot/deployments/cloud-enterprise/ask-for-help.md) if you cannot resolve the problem yourself.
