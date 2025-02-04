# Metrics [observability-apm-metrics]

The **Metrics** overview provides APM agent-specific metrics, which lets you perform more in-depth root cause analysis investigations within the Applications UI.

If you’re experiencing a problem with your service, you can use this page to attempt to find the underlying cause. For example, you might be able to correlate a high number of errors with a long transaction duration, high CPU usage, or a memory leak.

:::{image} ../../../images/serverless-apm-metrics.png
:alt: Example view of the Metrics overview in the Applications UI
:class: screenshot
:::

If you’re using the Java APM agent, you can view metrics for each JVM.

:::{image} ../../../images/serverless-jvm-metrics-overview.png
:alt: Example view of the Metrics overview for the Java Agent
:class: screenshot
:::

Breaking down metrics by JVM makes it much easier to analyze the provided metrics: CPU usage, memory usage, heap or non-heap memory, thread count, garbage collection rate, and garbage collection time spent per minute.

:::{image} ../../../images/serverless-jvm-metrics.png
:alt: Example view of the Metrics overview for the Java Agent
:class: screenshot
:::
