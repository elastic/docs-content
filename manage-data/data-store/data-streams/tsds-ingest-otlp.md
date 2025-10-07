---
navigation_title: "Ingest OTLP metrics"
applies_to:
  stack: preview 9.2
products:
  - id: elasticsearch
---

# Ingest metrics using the OpenTelemetry Protocol (OTLP)

In addition to the ingestion of metrics data through the bulk API,
{{es}} offers an alternative way to ingest data via the [OpenTelemetry Protocol (OTLP)](https://opentelemetry.io/docs/specs/otlp).

The endpoint is available under `/_otlp/v1/metrics`.

Ingesting metrics data using the OTLP endpoint has the following advantages:

* Improved ingestion performance, especially if the data contains many resource attributes.
* Simplified index mapping:
  there's no need to manually create an index template, or define dimensions and metrics.
  Using the OTLP endpoint, metrics are dynamically mapped using the metadata included in the OTLP requests.

:::{important}
On {{ecloud}} , use the [{{motlp}}](opentelemetry:/reference/motlp.md) instead of connecting directly to the {{es}} OTLP endpoint.
:::

## How to send data to the OTLP endpoint

To send data from an OpenTelemetry Collector to the {{es}} OTLP endpoint,
use the [`OTLP/HTTP` exporter](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/otlphttpexporter).
This is an example configuration:

```yaml
extensions:
  basicauth/elasticsearch:
    client_auth:
      username: <user>
      password: <password>
exporters:
  otlphttp/elasticsearch:
    endpoint: <es_endpoint>/_otlp
    sending_queue:
      enabled: true
      sizer: requests
      queue_size: 5000
      block_on_overflow: true
      batch:
        flush_timeout: 5s
        sizer: bytes
        min_size: 2_000_000
        max_size: 5_000_000
    auth:
      authenticator: basicauth/elasticsearch
```
:::{note} 
Only `encoding: proto` is supported, which the `OTLP/HTTP` exporter uses by default.
:::
The supported options for `compression` are `gzip` (default value of the `OTLP/HTTP` exporter) and `none`.

% TODO we might actually also support snappy and zstd, test and update accordingly)

To track metrics in your custom application,
use the [OpenTelemetry language SDK](https://opentelemetry.io/docs/getting-started/dev/) of your choice.

## When not to use the {{es}} OTLP endpoint

Do not send metrics from applications directly to the {{es}} OTLP endpoint, especially if there are many individual applications that periodically send a small amount of metrics. Instead, send data to an OpenTelemetry Collector first. This helps with handling many connections, and with creating bigger batches to improve ingestion performance. For more details on the recommended way to set up OpenTelemetry-based data ingestion, refer to the [EDOT reference architecture](opentelemetry:/reference/architecture/index.md).

At this point, {{es}} only supports the OTLP metrics endpoint (`/_otlp/v1/metrics`). Other signals are not supported through a native {{es}} OTLP endpoint at the moment. To ingest logs, traces, and profiles, use a distribution of the OpenTelemetry Collector that includes the [{{es}} exporter](opentelemetry:/reference/edot-collector/components/elasticsearchexporter.md), like the [Elastic Distribution of OpenTelemetry (EDOT) Collector](opentelemetry:/reference/edot-collector/index.md).

## Send data to different data streams

By default, metrics are ingested into the `metrics-generic.otel-default` data stream. You can influence the target data stream by setting specific attributes on your data:

- `data_stream.dataset` or `data_stream.namespace` in attributes, with the following order of precedence: data point attribute -> scope attribute -> resource attribute
- Otherwise, if the scope name contains `/receiver/<somereceiver>`, `data_stream.dataset` is set to the receiver name.
- Otherwise, `data_stream.dataset` falls back to `generic` and `data_stream.namespace` falls back to `default`.

The target data stream name is constructed as `metrics-${data_stream.dataset}.otel-${data_stream.namespace}`.

## Mapping hints

## Limitations

* Histograms are only supported in delta temporality. Set the temporality preference to delta in your SDKs, or use the [`cumulativetodelta` processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/cumulativetodeltaprocessor) to avoid cumulative histograms to be dropped.
* Exemplars are not supported.
