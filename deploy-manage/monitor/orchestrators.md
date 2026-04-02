---
applies_to:
  deployment:
    ece: all
    eck: all
products:
  - id: cloud-enterprise
  - id: cloud-kubernetes
---

# Monitoring orchestrators

Your [orchestrator](/deploy-manage/deploy.md#about-orchestration) is an important part of your Elastic architecture. It automates the deployment and management of multiple Elastic clusters, handling tasks like scaling, upgrades, and monitoring. Like your cluster or deployment, you need to monitor your orchestrator to ensure that it is healthy and performant. Monitoring is especially important for orchestrators hosted on infrastructure that you control.

In this section, you'll learn how to enable monitoring of your orchestrator.

* [ECK operator metrics](/deploy-manage/monitor/orchestrators/eck-metrics-configuration.md): Open and secure a metrics endpoint that can be used to monitor the operator’s performance and health. This endpoint can be scraped by third-party Kubernetes monitoring tools.
* [ECK platform monitoring](/deploy-manage/monitor/orchestrators/ece-platform-monitoring.md): Learn about how ECE collects monitoring data for your installation in the `logging-and-metrics` deployment, and how to access monitoring data.

:::{admonition} Monitoring {{ecloud}}
Elastic monitors {{ecloud}} service metrics and performance as part of [our shared responsibility](https://www.elastic.co/cloud/shared-responsibility). We provide service availability information on our [service status page](/deploy-manage/cloud-organization/service-status.md).
:::

:::{note}
Orchestrator monitoring can sometimes augment cluster or deployment monitoring, but doesn't replace it. For information about monitoring your cluster or deployment, refer to [](/deploy-manage/monitor.md).
:::