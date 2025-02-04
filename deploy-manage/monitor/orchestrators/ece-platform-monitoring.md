---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-monitoring-ece.html
applies:
  ece: all
---

# ECE platform monitoring [ece-monitoring-ece]

Elastic Cloud Enterprise by default collects monitoring data for your installation using Filebeat and Metricbeat. This data gets sent as monitoring indices to a dedicated `logging-and-metrics` deployment that is created whenever you install Elastic Cloud Enterprise on your first host. Data is collected on every host that is part of your Elastic Cloud Enterprise installation and includes:

* Logs for all core services that are a part of Elastic Cloud Enterprise and monitoring metrics for core Elastic Cloud Enterprise services, system processes on the host, and any third-party software
* Logs and monitoring metrics for Elasticsearch clusters and for Kibana instances

These monitoring indices are collected in addition to the [monitoring you might have enabled for specific clusters](../stack-monitoring/ece-stack-monitoring.md), which also provides monitoring metrics that you can access in Kibana (note that the `logging-and-metrics` deployment is used for monitoring data from system deployments only; for non-system deployments, monitoring data must be sent to a deployment other than `logging-and-metrics`).

In this section:

* [Access logs and metrics](ece-monitoring-ece-access.md) - Where to find the logs and metrics that are collected.
* [Capture heap dumps](../../../troubleshoot/deployments/cloud-enterprise/heap-dumps.md) - Troubleshoot instances that run out of memory.
* [Capture thread dumps](../../../troubleshoot/deployments/cloud-enterprise/thread-dumps.md) - Troubleshoot instances that are having thread or CPU issues.
* [Set the Retention Period for Logging and Metrics Indices](ece-monitoring-ece-set-retention.md) - Set the retention period for the indices that Elastic Cloud Enterprise collects.

::::{important} 
The `logging-and-metrics` deployment is for use by your ECE installation only. You must not use this deployment to index monitoring data from your own Elasticsearch clusters or use it to index data from Beats and Logstash. Always create a separate, dedicated monitoring deployment for your own use.
::::


