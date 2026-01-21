---
navigation_title: Manage deployments
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-manage-deployment.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Manage deployments in {{ech}} [ec-manage-deployment]

{{ech}} allows you to configure and maintain your deployments with a high level of control on every component of the {{stack}}. You can adjust the settings of any of your deployments at any time.

* Define the [core configuration](configure.md) of your deployment, including available features, hardware settings and capacity, autoscaling, and high availability.
  * Select a [hardware profile](/deploy-manage/deploy/elastic-cloud/ec-change-hardware-profile.md) optimized for your use case.
  * Make adjustments to specific [deployment components](/deploy-manage/deploy/elastic-cloud/ec-customize-deployment-components.md), such as the {{es}} cluster or an Integrations Server.
  * [Manage data tiers](/manage-data/lifecycle/data-tiers.md).

* Ensure the health of your deployment over time

  * [Keep track of your deployment's activity](keep-track-of-deployment-activity.md) or [Enable logging and monitoring](../../monitor/stack-monitoring/ece-ech-stack-monitoring.md) of the deployment performance.
  * Perform maintenance operations to ensure the health of your deployment, such as [restarting your deployment](../../maintenance/start-stop-services/restart-cloud-hosted-deployment.md) or [stopping routing](../../maintenance/start-stop-routing-requests.md).

* Manage the lifecycle of your deployment:

  * [Upgrade your deployment](/deploy-manage/upgrade/deployment-or-cluster.md) and its components to a newer version of the {{stack}}.
  * [Delete your deployment](../../uninstall/delete-a-cloud-deployment.md).









