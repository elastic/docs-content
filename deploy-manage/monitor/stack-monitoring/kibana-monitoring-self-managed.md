---
navigation_title: "Self-managed: {{kib}}"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/configuring-monitoring.html
applies_to:
  self: all
---



# Kibana monitoring self-managed [configuring-monitoring]


If you enable the {{monitor-features}} in your cluster, there are a few methods available to collect metrics about {{kib}}:

* [{{agent}} collection](kibana-monitoring-elastic-agent.md): Uses a single agent to gather logs and metrics. Can be managed from a central location in {{fleet}}.
* [{{metricbeat}} collection](kibana-monitoring-metricbeat.md): Uses a lightweight {{beats}} shipper to gather metrics. May be preferred if you have an existing investment in {{beats}} or are not yet ready to use {{agent}}.
* [Legacy collection](/deploy-manage/monitor/stack-monitoring/kibana-monitoring-legacy.md): Uses internal collectors to gather metrics. Not recommended. If you have previously configured legacy collection methods, you should migrate to using {{agent}} or {{metricbeat}}.

You can also use {{kib}} to [visualize monitoring data from across the {{stack}}](kibana-monitoring-data.md).

To learn about monitoring in general, refer to [](/deploy-manage/monitor/stack-monitoring.md).





