---
navigation_title: "OTLP/HTTP endpoint"
applies_to:
  stack: preview 9.2
  deployment:
    self:
products:
  - id: elasticsearch
---

# OTLP/HTTP endpoint

In addition to the ingestion of metrics data through the bulk API,
{{es}} offers an alternative way to ingest data through the [OpenTelemetry Protocol (OTLP)](https://opentelemetry.io/docs/specs/otlp).

The endpoint is available under `/_otlp/v1/metrics`.

## Overview and deployment options

:::{important}
The recommended approach for sending OpenTelemetry Protocol (OTLP) data depends on your deployment:

- **ECH and {{serverless-short}}:** Use the [Elastic Cloud Managed OTLP Endpoint](opentelemetry:/reference/motlp.md) directly.
- **ECE, ECK, and self-managed:** Use the {{es}} OTLP endpoint described on this page, ideally through an OpenTelemetry Collector in [Gateway mode](elastic-agent://reference/edot-collector/config/default-config-standalone.md#gateway-mode).

For details on the recommended way to set up OpenTelemetry-based data ingestion, refer to the [EDOT reference architecture](opentelemetry:/reference/architecture/index.md).
:::

Ingesting metrics data using the OTLP endpoint has the following advantages:

* Improved ingestion performance, especially if the data contains many resource attributes.
* Simplified index mapping:
  there's no need to manually create data streams, index templates, or define dimensions and metrics.
  Metrics are dynamically mapped using the metadata included in the OTLP requests.

:::{note}
{{es}} only supports [OTLP/HTTP](https://opentelemetry.io/docs/specs/otlp/#otlphttp),
not [OTLP/gRPC](https://opentelemetry.io/docs/specs/otlp/#otlpgrpc).
:::

Don't send metrics from applications directly to the {{es}} OTLP endpoint, especially if there are many individual applications that periodically send a small amount of metrics. Instead, send data to an OpenTelemetry Collector first. This helps with handling many connections, and with creating bigger batches to improve ingestion performance.

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
  otlphttp/elasticsearch-metrics:
    endpoint: <es_endpoint>/_otlp
    sending_queue:
      enabled: true
      sizer: bytes
      queue_size: 50_000_000 # 50MB uncompressed
      block_on_overflow: true
      batch:
        flush_timeout: 1s
        min_size: 1_000_000 # 1MB uncompressed
        max_size: 4_000_000 # 4MB uncompressed
    auth:
      authenticator: basicauth/elasticsearch
service:
  extensions: [basicauth/elasticsearch]
  pipelines:
    metrics:
      exporters: [otlphttp/elasticsearch-metrics]
      receivers: ...
```

The supported options for `compression` are `gzip` (default value of the `OTLP/HTTP` exporter) and `none`.

% TODO we might actually also support snappy and zstd, test and update accordingly)

To track metrics in your custom application,
use the [OpenTelemetry language SDK](https://opentelemetry.io/docs/getting-started/dev/) of your choice.

:::{note} 
Only `encoding: proto` is supported, which the `OTLP/HTTP` exporter uses by default.
:::

## Send data to different data streams

By default, metrics are ingested into the `metrics-generic.otel-default` data stream. You can influence the target data stream by setting specific attributes on your data:

- `data_stream.dataset` or `data_stream.namespace` in attributes, with the following order of precedence: data point attribute -> scope attribute -> resource attribute
- Otherwise, if the scope name contains `/receiver/<somereceiver>`, `data_stream.dataset` is set to the receiver name.
- Otherwise, `data_stream.dataset` falls back to `generic` and `data_stream.namespace` falls back to `default`.

The target data stream name is constructed as `metrics-${data_stream.dataset}.otel-${data_stream.namespace}`.

## Configure histogram handling
```{applies_to}
stack: preview 9.3
```

You can configure how OTLP histograms are mapped using the `xpack.otel_data.histogram_field_type` cluster setting. Valid values are:

 - `histogram` (default): Map histograms as T-Digests using the `histogram` field type
 - `exponential_histogram`: Map histograms as exponential histograms using the `exponential_histogram` field type

The setting is dynamic and can be updated at runtime:

```console
PUT /_cluster/settings
{
  "persistent" : {
    "xpack.otel_data.histogram_field_type" : "exponential_histogram"
  }
}
```

Because both `histogram` and `exponential_histogram` support [coerce](elasticsearch://reference/elasticsearch/mapping-reference/coerce.md), changing this setting dynamically does not risk mapping conflicts or ingestion failures.

## Limitations

* Only the OTLP metrics endpoint (`/_otlp/v1/metrics`) is supported.
  To ingest logs, traces, and profiles, use a distribution of the OpenTelemetry Collector that includes the [{{es}} exporter](opentelemetry:/reference/edot-collector/components/elasticsearchexporter.md),
  such as the [Elastic Distribution of OpenTelemetry (EDOT) Collector](opentelemetry:/reference/edot-collector/index.md).
* Histograms are only supported in delta temporality. Set the temporality preference to delta in your SDKs, or use the [`cumulativetodelta` processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/cumulativetodeltaprocessor) to avoid cumulative histograms to be dropped.
* Exemplars are not supported.
