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

1. Launch {{kib}}:

    <div class="tabs" data-tab-group="spin-up-stack">
      <div role="tablist" aria-label="Configure Server">
        <button role="tab"
                aria-selected="true"
                aria-controls="cloud-tab-open-kib"
                id="cloud-open-kib">
          Elasticsearch Service
        </button>
        <button role="tab"
                aria-selected="false"
                aria-controls="self-managed-tab-open-kib"
                id="self-managed-open-kib"
                tabindex="-1">
          Self-managed
        </button>
      </div>
      <div tabindex="0"
           role="tabpanel"
           id="cloud-tab-open-kib"
           aria-labelledby="cloud-open-kib">
    1. [Log in](https://cloud.elastic.co/) to your {{ecloud}} account.
    2. Navigate to the {{kib}} endpoint in your deployment.

      </div>
      <div tabindex="0"
           role="tabpanel"
           id="self-managed-tab-open-kib"
           aria-labelledby="self-managed-open-kib"
           hidden="">
    Point your browser to [http://localhost:5601](http://localhost:5601), replacing `localhost` with the name of the {{kib}} host.

      </div>
    </div>

2. Find **Discover** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
3. Select `apm-*` as your index pattern.
4. Filter the data to only show documents with metrics: `[data_stream][type]: "metrics"`
5. Narrow your search with a known OpenTelemetry field. For example, if you have an `order_value` field, add `order_value: *` to your search to return only OpenTelemetry metrics documents.


## Visualize in {{kib}} [apm-open-telemetry-visualize]

Use **Lens** to create visualizations for OpenTelemetry metrics. Lens enables you to build visualizations by dragging and dropping data fields. It makes smart visualization suggestions for your data, allowing you to switch between visualization types.

For more information on using Lens, refer to the [Lens documentation](../../../explore-analyze/visualize/lens.md).
