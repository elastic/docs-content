---
navigation_title: Metrics UI
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-metrics.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-metrics.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Metrics UI in Elastic APM [apm-metrics]

The **Metrics** overview provides APM agent-specific metrics, which lets you perform more in-depth root cause analysis investigations within the Applications UI.

If you’re experiencing a problem with your service, you can use this page to attempt to find the underlying cause. For example, you might be able to correlate a high number of errors with a long transaction duration, high CPU usage, or a memory leak.

:::{image} /solutions/images/observability-apm-metrics.png
:alt: Example view of the Metrics overview in Applications UI in Kibana
:screenshot:
:::

:::{note}
Dashboard resolution is version-aware: the Metrics tab uses the service’s runtime version — alongside data format, SDK name, and language — to load the correct dashboard. For example, .NET 9 and later services use a built-in runtime metrics dashboard, while .NET 8 and earlier services use a legacy contrib metrics dashboard. This ensures you always see the metrics that match your service’s runtime version.
:::

## Instrumentation changes during migration [instrumentation-change]
```{applies_to}
stack: ga 9.3
serverless: ga
```

When migrating a service to OpenTelemetry instrumentation, you may have date ranges that contain both classic {{product.apm}} and OpenTelemetry data. The **Metrics** tab shows callouts to help you navigate this transition period.

**Instrumentation change detected**
:   When the **Metrics** tab detects a change in instrumentation, it shows: "We have detected a change on `<timestamp>` in the instrumentation of your service." It also shows the current instrumentation type and time period, and provides the date range for the previous instrumentation period so you can switch to it.

**Overlapping instrumentation types**
:   If classic {{product.apm}} and OpenTelemetry data overlap in the selected time range, the **Metrics** tab shows: "This service has overlapping data from multiple instrumentation types." It provides date ranges for each instrumentation type so you can click to switch to a specific period.

## JVM metrics

If you’re using the Java APM agent, you can view metrics for each JVM.

:::{image} /solutions/images/observability-jvm-metrics-overview.png
:alt: Example view of the Metrics overview for the Java Agent
:screenshot:
:::

Breaking down metrics by JVM makes it much easier to analyze the provided metrics: CPU usage, memory usage, heap or non-heap memory, thread count, garbage collection rate, and garbage collection time spent per minute.

:::{image} /solutions/images/observability-jvm-metrics.png
:alt: Example view of the Metrics overview for the Java Agent
:screenshot:
:::