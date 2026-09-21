---
navigation_title: Explore metrics
description: Visualize and alert on metrics in Discover, the Infrastructure UI, and Kibana dashboards, or point Grafana at Elasticsearch as a Prometheus data source.
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

After your metrics are in Elastic, explore them in {{kib}} and act on them with {{observability}} rules. Use **Discover**, or **Metrics Explorer** on Stack versions 9.0-9.3, for ad hoc time-series charts, the Infrastructure UI for host and {{k8s}} inventory, and dashboards for shared views. If your team works in Grafana, keep it and point it at {{es}} as a Prometheus data source.

## Explore time-series metrics [metrics-explore-discover]

The UI you use to explore time-series metrics depends on your deployment and {{stack}} version.

{applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Use **Discover** in {{kib}} to explore time-series metrics data, apply filters, and run Elasticsearch Query Language ({{esql}}) queries. For the Discover metrics workflow, including dimension breakdowns and adding charts to a dashboard, refer to [Explore metrics data with Discover in {{kib}}](/solutions/observability/infra-and-hosts/discover-metrics.md).

{applies_to}`stack: deprecated 9.4+, ga 9.0-9.3` Use **Metrics Explorer** to create time-series visualizations of your metrics, chart them against related metrics, and break them down by the field of your choice. For the Metrics Explorer workflow, refer to [Explore infrastructure metrics over time](/solutions/observability/infra-and-hosts/explore-infrastructure-metrics-over-time.md).

## Infrastructure views [metrics-explore-infra]

These views give you a resource-centric perspective on your infrastructure, with metrics-driven health and performance indicators:

[View infrastructure metrics by resource type](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md)
:   Use the **Infrastructure inventory** page, organized by resource groupings.

[Analyze and compare hosts](/solutions/observability/infra-and-hosts/analyze-compare-hosts.md)
:   Open the **Hosts** page to compare host metrics side by side.

[Detect metric anomalies](/solutions/observability/infra-and-hosts/detect-metric-anomalies.md)
:   Use {{anomaly-detect}} powered by {{ml}} for memory usage and network traffic. Not available for hosts monitored with OpenTelemetry.

## Dashboards [metrics-explore-dashboards]

Build dashboards in {{kib}} Lens to track metrics over time, compare resources, and share views with your team. Metrics stored as a time series data stream (TSDS) support efficient time-series aggregations in Lens visualizations. Start with [Create a dashboard](/explore-analyze/dashboards/create-dashboard.md), then add charts using [Visualize data with Lens](/explore-analyze/visualize/lens.md).

## Grafana [metrics-explore-grafana]
```{applies_to}
stack: preview =9.4, ga 9.5+
serverless: ga
```

If you use Grafana, you can point it at {{es}} as a Prometheus data source and run your existing PromQL dashboards without rewriting them, as long as they use supported PromQL. For the data source URL and authentication, refer to [Use {{es}} as a Prometheus data source in Grafana](elasticsearch://reference/query-languages/promql/promql-grafana.md). For constructs {{es}} doesn't support, refer to [PromQL limitations](elasticsearch://reference/query-languages/promql/promql-limitations.md).

## Alert on metrics [metrics-explore-alerts]

After you can see the time series you care about, create a rule so a threshold notifies you. Select a rule type from the following list. Each page has the conditions, filters, and action setup.

[Create a custom threshold rule](/solutions/observability/incident-management/create-custom-threshold-rule.md)
:   Alert when a metric in a data view crosses a threshold. Use this rule for OpenTelemetry and Prometheus remote write metrics on every deployment type.

[Create an inventory rule](/solutions/observability/incident-management/create-an-inventory-rule.md)
:   Alert on infrastructure resources from the **Infrastructure inventory** page.

[Create a metric threshold rule](/solutions/observability/incident-management/create-metric-threshold-rule.md) {applies_to}`serverless: unavailable`
:   Alert on metrics in the Infrastructure metrics indices. Create this rule from the **Rules** page. For Stack versions 9.0-9.3, you can also create it from **Metrics Explorer**.

For the full list of {{observability}} rule types, refer to [Create and manage rules](/solutions/observability/incident-management/create-manage-rules.md).

## Related pages [metrics-explore-related]

- [Query metrics](/solutions/observability/metrics/query.md)
- [Manage metrics storage](/solutions/observability/metrics/manage-storage.md)
