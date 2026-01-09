---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/xpack-monitoring.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
products:
  - id: kibana
---

# Visualizing monitoring data [xpack-monitoring]

From within the **Stack Monitoring** section of {{kib}}, you can view health and performance data for {{es}}, {{ls}}, {{kib}}, and Beats in real time, as well as analyze past performance.

Before you can see this data inside of {{kib}}, you need to [configure stack monitoring](/deploy-manage/monitor/stack-monitoring.md) and, for {{eck}} and self-managed deployments, [configure {{kib}} to retrieve and display monitoring data](/deploy-manage/monitor/stack-monitoring/kibana-monitoring-data.md).

Review the following topics to learn more about the metrics and visualizations available in the **Stack Monitoring** area:

* [](/deploy-manage/monitor/monitoring-data/elasticsearch-metrics.md)
* [](/deploy-manage/monitor/monitoring-data/kibana-page.md)
* [](/deploy-manage/monitor/monitoring-data/integrations-server-page.md) {applies_to}`ess: ga` {applies_to}`ece: ga`
* [](/deploy-manage/monitor/monitoring-data/beats-page.md)
* [](/deploy-manage/monitor/monitoring-data/logstash-page.md)

From the **Stack Monitoring** section, you can also configure [{{kib}} alerts](/deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md) for stack monitoring metrics.

If you're having trouble accessing your monitoring data within the **Stack Monitoring** section, then refer to [](/deploy-manage/monitor/monitoring-data/monitor-troubleshooting.md).

If you enable monitoring across the {{stack}}, each monitored component is considered unique based on its persistent UUID, which is written to the [`path.data`](kibana://reference/configuration-reference/general-settings.md#path-data) directory when the node or instance starts.


