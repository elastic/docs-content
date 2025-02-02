---
navigation_title: "Configure monitoring"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/configuring-monitoring.html
---



# Kibana monitoring self-managed [configuring-monitoring]


If you enable the {{monitor-features}} in your cluster, there are a few methods available to collect metrics about {{kib}}:

* [{{agent}} collection](monitoring-elastic-agent.md): Uses a single agent to gather logs and metrics. Can be managed from a central location in {{fleet}}.
* [{{metricbeat}} collection](monitoring-metricbeat.md): Uses a lightweight {{beats}} shipper to gather metrics. May be preferred if you have an existing investment in {{beats}} or are not yet ready to use {{agent}}.
* [Legacy collection](monitoring-kibana.md): Uses internal collectors to gather metrics. Not recommended. If you have previously configured legacy collection methods, you should migrate to using {{agent}} or {{metricbeat}}.

You can also use {{kib}} to [visualize monitoring data from across the {{stack}}](monitoring-data.md).

To learn about monitoring in general, see [Monitor a cluster](../../monitor.md).





