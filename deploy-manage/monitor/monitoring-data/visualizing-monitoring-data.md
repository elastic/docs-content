---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/xpack-monitoring.html
applies:
  hosted: all
  ece: all
  eck: all
  stack: all
---

# Visualizing monitoring data [xpack-monitoring]

The {{kib}} {{monitor-features}} serve two separate purposes:

1. To visualize monitoring data from across the {{stack}}. You can view health and performance data for {{es}}, {{ls}}, APM, and Beats in real time, as well as analyze past performance.
2. To monitor {{kib}} itself and route that data to the monitoring cluster.

If you enable monitoring across the {{stack}}, each monitored component is considered unique based on its persistent UUID, which is written to the [`path.data`](../../deploy/self-managed/configure.md) directory when the node or instance starts.

For more information, see [Configure monitoring](../stack-monitoring/kibana-monitoring-self-managed.md) and [Monitor a cluster](../../monitor.md).

Want to monitor your fleet of {{agent}}s, too? Use {{fleet}} instead of the Stack Monitoring UI. To learn more, refer to [Monitor {{agent}}s](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/monitor-elastic-agent.md).

