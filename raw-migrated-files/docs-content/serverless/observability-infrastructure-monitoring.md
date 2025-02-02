# Analyze infrastructure and host metrics [observability-infrastructure-monitoring]

{{obs-serverless}} allows you to visualize infrastructure metrics to help diagnose problematic spikes, identify high resource utilization, automatically discover and track pods, and unify your metrics with logs and APM data.

Using {{agent}} integrations, you can ingest and analyze metrics from servers, Docker containers, Kubernetes orchestrations, explore and analyze application telemetry, and more.

For more information, refer to the following links:

* [Get started with system metrics](../../../solutions/observability/infra-and-hosts/get-started-with-system-metrics.md): Learn how to onboard your system metrics data quickly.
* [View infrastructure metrics by resource type](../../../solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md): Use the **Inventory page** to get a metrics-driven view of your infrastructure grouped by resource type.
* [Analyze and compare hosts](../../../solutions/observability/infra-and-hosts/analyze-compare-hosts.md): Use the **Hosts** page to get a metrics-driven view of your infrastructure backed by an easy-to-use interface called Lens.
* [Detect metric anomalies](../../../solutions/observability/infra-and-hosts/detect-metric-anomalies.md): Detect and inspect memory usage and network traffic anomalies for hosts and Kubernetes pods.
* [Configure settings](../../../solutions/observability/infra-and-hosts/configure-settings.md): Learn how to configure infrastructure UI settings.
* [Metrics reference](https://www.elastic.co/guide/en/serverless/current/observability-metrics-reference.html): Learn about key metrics used for infrastructure monitoring.
* [Infrastructure app fields](https://www.elastic.co/guide/en/serverless/current/observability-infrastructure-monitoring-required-fields.html): Learn about the fields required to display data in the Infrastructure UI.

By default, the Infrastructure UI displays metrics from {{es}} indices that match the `metrics-*` and `metricbeat-*` index patterns. To learn how to change this behavior, refer to [Configure settings](../../../solutions/observability/infra-and-hosts/configure-settings.md).
