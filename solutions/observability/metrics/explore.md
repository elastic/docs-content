---
navigation_title: Explore metrics
description: Explore, visualize, and alert on metrics in Elastic using Discover or Metrics Explorer, the Infrastructure UI, Kibana dashboards, Grafana, or Observability rules.
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

After your metrics are flowing into Elastic, use these tools to explore, visualize, and act on them.

## Explore time-series metrics [metrics-explore-discover]

The UI you use to explore time-series metrics depends on your deployment and {{stack}} version.

::::{applies-switch}

:::{applies-item} { stack: ga 9.4+, serverless: ga }
Use **Discover** in {{kib}} to explore time-series metrics data, apply filters, and run {{esql}} queries. For the Discover metrics workflow, including dimension breakdowns and adding charts to a dashboard, refer to [Explore metrics data with Discover in {{kib}}](/solutions/observability/infra-and-hosts/discover-metrics.md).
:::

:::{applies-item} { stack: deprecated 9.4+, ga 9.0-9.3 }
Use **Metrics Explorer** to create time-series visualizations of your metrics, chart them against related metrics, and break them down by the field of your choice. For the Metrics Explorer workflow, refer to [Explore infrastructure metrics over time](/solutions/observability/infra-and-hosts/explore-infrastructure-metrics-over-time.md).
:::

::::

## Infrastructure views [metrics-explore-infra]

These views give you a resource-centric perspective on your infrastructure, with metrics-driven health and performance indicators:

[View infrastructure metrics by resource type](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md)
:   Use the Inventory view, organized by resource groupings.

[Analyze infrastructure and host metrics](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md)
:   Open the Hosts page with a {{kib}} Lens visualization.

[Detect metric anomalies](/solutions/observability/infra-and-hosts/detect-metric-anomalies.md)
:   Use {{ml-cap}}-powered {{anomaly-detect}} for memory usage and network traffic.

## Dashboards [metrics-explore-dashboards]

Build dashboards in {{kib}} Lens to track metrics over time, compare resources, and share views with your team. Metrics stored as TSDS support efficient time-series aggregations in Lens visualizations. Start with [Create a dashboard](/explore-analyze/dashboards/create-dashboard.md), then add charts using [Visualize data with Lens](/explore-analyze/visualize/lens.md).

## Grafana [metrics-explore-grafana]

If you use Grafana, you can point it at {{es}} as a Prometheus data source and run your existing PromQL dashboards without rewriting them. For the data source URL and authentication, refer to [Use {{es}} as a Prometheus data source in Grafana](elasticsearch://reference/query-languages/promql/promql-grafana.md).

## Alert on metrics [metrics-explore-alerts]

After you can see the time series you care about, create a rule so a threshold notifies you. Pick a rule type from the following list. Each page has the conditions, filters, and action setup.

[Create a custom threshold rule](/solutions/observability/incident-management/create-custom-threshold-rule.md)
:   Alert when a metric in a data view crosses a threshold. Use this rule for OpenTelemetry and Prometheus remote write metrics on every deployment type.

[Create an inventory rule](/solutions/observability/incident-management/create-an-inventory-rule.md)
:   Alert on infrastructure resources from the Inventory view.

[Create a metric threshold rule](/solutions/observability/incident-management/create-metric-threshold-rule.md) {applies_to}`serverless: unavailable`
:   Alert on metrics in the Infrastructure metrics indices. You can create this rule from **Metrics Explorer** or from the **Rules** page.

For the full list of {{observability}} rule types, refer to [Create and manage rules](/solutions/observability/incident-management/create-manage-rules.md).

## Related pages [metrics-explore-related]

- [Query metrics](/solutions/observability/metrics/query.md)
- [Manage metrics storage](/solutions/observability/metrics/manage-storage.md)
