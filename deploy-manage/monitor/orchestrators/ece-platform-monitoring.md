---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-monitoring-ece.html
applies_to:
  deployment:
    ece: all
---

# ECE platform monitoring [ece-monitoring-ece]

By default, {{ece}} collects monitoring data for your installation using Filebeat and Metricbeat. This data gets sent as monitoring indices to a dedicated `logging-and-metrics` deployment that is created whenever you install {{ece}} on your first host. Data is collected on every host that is part of your {{ece}} installation and includes:

* Logs for all core services that are a part of {{ece}} 
* Monitoring metrics for core {{ece}} services, system processes on the host, and any third-party software
* Logs and monitoring metrics for {{es}} clusters and for {{kib}} instances

These monitoring indices are collected in addition to the [stack monitoring you might have enabled for specific clusters](/deploy-manage/monitor/stack-monitoring/ece-ech-stack-monitoring.md), which also provides monitoring metrics that you can access in {{kib}}. 

In this section, you'll learn the following about using ECE platform monitoring:

* [](ece-monitoring-ece-access.md): The types of logs and metrics that are collected for deployments, and where to find them.
% where do we find logs and metrics for the installation itself? 
* [](/deploy-manage/monitor/orchestrators/ece-proxy-log-fields.md): The fields that are included in proxy logs. Proxy logs capture the search and indexing requests that proxies have sent to the {{es}} cluster, and requests that proxies have sent to the {{kib}} instance.
* [](ece-monitoring-ece-set-retention.md): How to set the retention period for the indices that {{ece}} collects.

For information about troubleshooting {{ECE}} using these metrics, and guidance on capturing other diagnostic information like heap dumps and thread dumps, refer to [](/troubleshoot/deployments/cloud-enterprise/cloud-enterprise.md).

::::{important} 
The `logging-and-metrics` deployment is for use by your ECE installation only. You must not use this deployment to index monitoring data from your own Elasticsearch clusters or use it to index data from Beats and Logstash. Always create a separate, dedicated monitoring deployment for your own use.
::::