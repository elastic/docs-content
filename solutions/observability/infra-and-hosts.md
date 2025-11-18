---
navigation_title: Infrastructure and hosts
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/infrastructure-and-host-monitoring-intro.html
  - https://www.elastic.co/guide/en/serverless/current/infrastructure-and-host-monitoring-intro.html
applies_to:
  stack: ga
  serverless:
products:
  - id: observability
  - id: cloud-serverless
---

# Infrastructure and host monitoring [infrastructure-and-host-monitoring-intro]

% Stateful only for Profiling, Tutorials, Metrics reference.

Explore the topics in this section to learn how to observe and monitor hosts and other systems running in your environment.

:::{tip}
We recommend using the [Elastic Distribution of OpenTelemetry (EDOT) Collector](/solutions/observability/get-started/quickstart-monitor-hosts-with-opentelemetry.md) as the preferred way to collect infrastructure metrics and logs. You can also use the [Elastic Agent](/solutions/observability/infra-and-hosts/get-started-with-system-metrics.md) with integrations for infrastructure monitoring.
:::

|     |     |
| --- | --- |
| [Analyze infrastructure and host metrics](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) | Visualize infrastructure metrics to help diagnose problematic spikes, identify high resource utilization, automatically discover and track pods, and unify your metrics with other observability data. |
| [Universal Profiling](/solutions/observability/infra-and-hosts/universal-profiling.md) | Profile all the code running on a machine, including application code, kernel, and third-party libraries. |
| [Tutorial: Observe your Kubernetes deployments](/solutions/observability/infra-and-hosts/tutorial-observe-kubernetes-deployments.md) | Observe all layers of your application, including the orchestration software itself. |
| [Tutorial: Observe your nginx instances](/solutions/observability/infra-and-hosts/tutorial-observe-nginx-instances.md) | Collect valuable metrics and logs from your nginx instances. |
| [Troubleshooting](/troubleshoot/observability/troubleshooting-infrastructure-monitoring.md) | Troubleshoot common issues on your own or ask for help. |
| [Metrics reference](/reference/observability/metrics-reference.md) | Learn about the key metrics displayed in the Infrastructure UI and how they are calculated. |