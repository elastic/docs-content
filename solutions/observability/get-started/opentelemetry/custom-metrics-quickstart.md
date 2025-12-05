---
navigation_title: Ingest custom metrics with EDOT
description: Learn how to send custom metrics to Elastic using EDOT and OTLP. This lightweight quickstart covers the minimal setup to ingest and validate metrics in Elastic Observability.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_collector: ga
products:
  - id: cloud-serverless
  - id: cloud-hosted
  - id: observability
  - id: edot-collector
---

# Quickstart: Ingest custom metrics with EDOT

Use this quickstart to send custom metrics to Elastic using the Elastic Distribution of the OpenTelemetry Collector (EDOT).

You’ll install a lightweight EDOT Collector, configure a minimal OTLP metrics pipeline, and verify the data in {{product.observability}}.

## Prerequisites

- An Elastic deployment ({{serverless-short}}, Cloud Hosted, or self-managed)
- An {{observability}} project {{kib}} instance
- Permissions to create API keys
- A system to run the EDOT Collector (Docker, host, or VM)
- Optional: An application that emits OpenTelemetry metrics

:::::{stepper}

::::{step} Create an Elastic API key

In your {{product.observability}} deployment:

1. Go to **{{manage-app}}** > **{{stack-manage-app}}** > **API keys**.
2. Create a new API key and copy the value.
3. Note your deployment's OTLP ingest endpoint.
::::

::::{step} Run the EDOT Collector with a minimal metrics pipeline

Update the `collector-config.yaml` file with the following Collector configuration to receive OTLP metrics and export them to Elastic:

```yaml
receivers:
  otlp:
    protocols:
      http:
      grpc:

processors:
  batch: {}

exporters:
 elasticsearch:
   endpoints: ["<OTLP_ENDPOINT>"]
   api_key: "<YOUR_API_KEY>"
   mapping:
     mode: otel
   metrics_dynamic_index:
     enabled: true

service:
 pipelines:
   metrics:
     receivers: [otlp]
     processors: [batch]
     exporters: [elasticsearch]
```

Run the configuration with Docker:

```bash
docker run --rm \
  -v $(pwd)/collector-config.yaml:/etc/otel/config.yaml \
  -p 4317:4317 -p 4318:4318 \
  docker.elastic.co/observability/otel-collector:latest
```
::::

::::{step} Optional: Port conflict handling

If you encounter a port conflict error like:

```bash
bind: address already in use
```

Add the following to the `service` section:

```yaml
service:
 telemetry:
   metrics:
     address: localhost:8889  # Using different port if 8888 is already in use
```

You can also verify if the Collector is listening on the correct ports:

```bash
lsof -i :4318 -i :4317
```
::::

::::{step} Send a custom metric

In this Python example, you use an application that emits OTLP metrics:

```python
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

exporter = OTLPMetricExporter(endpoint="http://localhost:4318/v1/metrics")
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter("custom-app")

temperature = meter.create_observable_gauge(
    "custom.temperature",
    callbacks=[lambda options: [metrics.Observation(26.7)]],
)

input("Sending metrics periodically... press Enter to stop")
```
::::

::::{step} Verify metrics in {{product.observability}}

In {{kib}}:

1. Go to **Infrastructure** > **Metrics Explorer**.
2. Search for `custom.temperature`.
3. Visualize or aggregate the metric data.
::::

:::::

## Explore your metrics

You've successfully set up a minimal OTLP metrics pipeline with the EDOT Collector. Your custom metrics are flowing into {{product.observability}} and can be visualized in {{kib}}.

Now you can:

- Use **Metrics Explorer** to create custom visualizations and dashboards
- Set up alerts based on your custom metrics
- Aggregate and analyze metric trends over time

## Extend your setup

You can expand your metrics collection setup in several ways:

- Add more receivers to collect additional metrics
- Configure the same Collector to send logs and traces alongside metrics

To learn more, refer to the [Elastic Distribution of the OpenTelemetry Collector documentation](elastic-agent://reference/edot-collector/index.md).