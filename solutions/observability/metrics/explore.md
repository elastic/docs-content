---
navigation_title: Explore metrics
description: Explore and visualize metrics in Elastic using Discover, the Infrastructure UI, Kibana dashboards, or Grafana with PromQL.
applies_to:
  stack: ga
  serverless:
    observability:
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Explore metrics [metrics-explore]

After your metrics are flowing into Elastic, use these tools to explore, visualize, and act on them. The primary explore experience is metrics data in Discover — the old Metrics Explorer is deprecated.

## Explore metrics in Discover [metrics-explore-discover]

Use Discover in {{kib}} to explore time-series metrics data, apply filters, and run {{esql}} queries against your metrics. This is the recommended path for interactive exploration.

[Explore metrics data with Discover in {{kib}}](/solutions/observability/infra-and-hosts/discover-metrics.md)

## Infrastructure views [metrics-explore-infra]

These views give you a resource-centric perspective on your infrastructure, with metrics-driven health and performance indicators:

- [View infrastructure metrics by resource type](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md) — the Inventory view, organized by resource groupings
- [Analyze infrastructure and host metrics](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) — the Hosts page with a {{kib}} Lens visualization
- [Detect metric anomalies](/solutions/observability/infra-and-hosts/detect-metric-anomalies.md) — {{ml-cap}}-powered {{anomaly-detect}} for memory usage and network traffic

## Dashboards [metrics-explore-dashboards]

Build dashboards in {{kib}} Lens to track metrics over time, compare resources, and share views with your team. Metrics stored as TSDS support efficient time-series aggregations in Lens visualizations.

- [Create a dashboard](/explore-analyze/dashboards/create-dashboard.md)
- [Visualize data with Lens](/explore-analyze/visualize/lens.md)

## Grafana [metrics-explore-grafana]

If you use Grafana, you can point it at {{es}} as a Prometheus data source and run your existing PromQL dashboards without rewriting them.

Refer to [Use {{es}} as a Prometheus data source in Grafana](/reference/query-languages/promql/promql-grafana.md).

## Related [metrics-explore-related]

- [Query metrics](/solutions/observability/metrics/query.md)
- [Manage metrics storage](/solutions/observability/metrics/manage-storage.md)
