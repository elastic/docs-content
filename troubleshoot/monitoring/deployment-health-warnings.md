---
navigation_title: Deployment health warnings
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-deployment-no-op.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-deployment-no-op.html
applies_to:
  deployment:
    ess: all
products:
  - id: cloud-hosted
---

# Troubleshoot deployment health warnings [ec-deployment-no-op]

The {{ecloud}} [Deployments](https://cloud.elastic.co/deployments) page shows the current status of your active deployments. From time to time you may get one or more health warnings, such as the following:

:::{image} /troubleshoot/images/cloud-ec-ce-deployment-health-warning.png
:alt: A screen capture of the deployment page showing a typical warning: Deployment health warning: Latest change to {{es}} configuration failed.
:::

**Single warning**

To resolve a single health warning, we recommended first re-applying any pending changes: Select **Edit** in the deployment menu to open the Edit page and then click **Save** without making any changes. This will check all components for pending changes and will apply the changes as needed. This may impact the uptime of clusters which are not [highly available](/deploy-manage/production-guidance/availability-and-resilience/resilience-in-ech.md).

Re-saving the deployment configuration without making any changes is often all that’s needed to resolve a transient health warning on the UI. Saving will redirect you to the {{ech}} deployment [Activity page](/deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md) where you can monitor plan completion. Repeat errors should be investigated; for more information refer to [resolving configuration change errors](/troubleshoot/monitoring/node-bootlooping.md).

**Multiple warnings**

If multiple health warnings appear for one of your deployments, or if your deployment is unhealthy, we recommend [Getting help](/troubleshoot/index.md) through the Elastic Support Portal.

**Warning about system changes**

If the warning refers to a system change, check the deployment’s [Activity](/deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md) page.

:::{important}
 If you’re using Elastic Cloud Hosted, then you can use AutoOps to monitor your cluster. AutoOps significantly simplifies cluster management with performance recommendations, resource utilization visibility, and real-time issue detection with resolution paths. For more information, refer to [Monitor with AutoOps](/deploy-manage/monitor/autoops.md).
:::

## Additional resources
* [Elastic Cloud Enterprise deployment health warnings](/troubleshoot/deployments/cloud-enterprise/deployment-health-warnings.md)
* [Troubleshooting overview](/troubleshoot/index.md)