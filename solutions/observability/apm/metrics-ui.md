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