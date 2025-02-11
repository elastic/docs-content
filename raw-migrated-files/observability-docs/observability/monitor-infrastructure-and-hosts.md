# Analyze infrastructure and host metrics [monitor-infrastructure-and-hosts]

In the {{infrastructure-app}}, visualize infrastructure metrics to help diagnose problematic spikes, identify high resource utilization, automatically discover and track pods, and unify your metrics with logs and APM data in {{es}}.

Using {{agent}} integrations, you can ingest and analyze metrics from servers, Docker containers, Kubernetes orchestrations, explore and analyze application telemetry, and more.

To access the {{infrastructure-app}}, find **Infrastructure** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

The {{infrastructure-app}} provides a few different views of your data.

|     |     |
| --- | --- |
| **Infrastructure inventory** | Provides a metrics-driven view of your entire infrastructure grouped by the resources that you are monitoring.<br>[Learn more about the Inventory page > ](../../../solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md) |
| **Metrics Explorer** | Enables you to create time-series visualizations based on aggregation of your metrics, chart them against related metrics, and break them down per the field of your choice.<br>[Learn more about the Metrics Explorer > ](../../../solutions/observability/infra-and-hosts/explore-infrastructure-metrics-over-time.md) |
| **Hosts** | Provides a metrics-driven view of your infrastructure backed by an easy-to-use interface called Lens.<br>[Learn more about the Hosts page > ](../../../solutions/observability/infra-and-hosts/analyze-compare-hosts.md) |

By default, the {{infrastructure-app}} displays metrics from {{es}} indices that match the `metrics-*` and `metricbeat-*` index patterns. To learn how to change this behavior, refer to [Configure settings](../../../solutions/observability/infra-and-hosts/configure-settings.md).

To learn more about the metrics shown in the {{infrastructure-app}}, refer to the [Metrics reference](https://www.elastic.co/guide/en/observability/current/metrics-reference.html) documentation.
