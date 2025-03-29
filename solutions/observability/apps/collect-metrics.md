---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-open-telemetry-collect-metrics.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-agents-opentelemetry-collect-metrics.html
---

# Collect metrics [apm-open-telemetry-collect-metrics]

::::{important}
When collecting metrics, please note that the [`DoubleValueRecorder`](https://www.javadoc.io/doc/io.opentelemetry/opentelemetry-api/latest/io/opentelemetry/api/metrics/DoubleValueRecorder.md) and [`LongValueRecorder`](https://www.javadoc.io/doc/io.opentelemetry/opentelemetry-api/latest/io/opentelemetry/api/metrics/LongValueObserver.md) metrics are not yet supported.
::::


Here’s an example of how to capture business metrics from a Java application.

```java
// initialize metric
Meter meter = GlobalMetricsProvider.getMeter("my-frontend");
DoubleCounter orderValueCounter = meter.doubleCounterBuilder("order_value").build();

public void createOrder(HttpServletRequest request) {

   // create order in the database
   ...
   // increment business metrics for monitoring
   orderValueCounter.add(orderPrice);
}
```

See the [Open Telemetry Metrics API](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/metrics/api.md) for more information.


## Verify OpenTelemetry metrics data [apm-open-telemetry-verify-metrics]

Use **Discover** to validate that metrics are successfully reported to {{kib}}.

1. Open your Observability instance.
2. Find **Discover** in the main menu or use the [global search field](../../../get-started/the-stack.md#kibana-navigation-search), and select the **Logs Explorer** tab.
3. Click **All logs** → **Data Views** then select **APM**.
4. Filter the data to only show documents with metrics: `processor.name :"metric"`
5. Narrow your search with a known OpenTelemetry field. For example, if you have an `order_value` field, add `order_value: *` to your search to return only OpenTelemetry metrics documents.


## Visualize your metrics[apm-open-telemetry-visualize]

Use **Lens** to create visualizations for OpenTelemetry metrics. Lens enables you to build visualizations by dragging and dropping data fields. It makes smart visualization suggestions for your data, allowing you to switch between visualization types.

To get started with a new Lens visualization:

1. Go to **Visualizations**.
2. Click **Create new visualization**.
3. Select **Lens**.

For more information on using Lens, refer to the [Lens documentation](../../../explore-analyze/visualize/lens.md).