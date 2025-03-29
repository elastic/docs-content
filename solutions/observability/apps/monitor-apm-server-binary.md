---
navigation_title: "APM Server binary"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-monitoring.html
applies_to:
  stack: all
---

# Monitor the APM Server binary [apm-monitoring]


There are two methods to monitor the APM Server binary. Make sure monitoring is enabled on your {{es}} cluster, then configure one of these methods to collect APM Server metrics:

* [Internal collection](use-internal-collection-to-send-monitoring-data.md) - Internal collectors send monitoring data directly to your monitoring cluster.
* [{{metricbeat}} collection](use-metricbeat-to-send-monitoring-data.md) - {{metricbeat}} collects monitoring data from your APM Server instance and sends it directly to your monitoring cluster.
* [Local collection](use-select-metrics-emitted-directly-to-monitoring-cluster.md) - Local collection sends select monitoring data directly to the standard indices of your monitoring cluster.