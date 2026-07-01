---
navigation_title: "OTLP/HTTP endpoint"
description: "Send metrics, logs, and traces directly to Elasticsearch through its native OTLP/HTTP endpoints, without running an OpenTelemetry Collector."
applies_to:
  deployment:
    self: ga 9.2
    ece: ga
    eck: ga
products:
  - id: elasticsearch
---

# {{es}} OTLP/HTTP endpoint

In addition to ingesting data through the Bulk API, {{es}} accepts data through the [OpenTelemetry Protocol (OTLP)](https://opentelemetry.io/docs/specs/otlp).
The {{es}} OTLP/HTTP endpoint exposes three signal-specific paths:

| Signal | Path | Availability |
| --- | --- | --- |
| Metrics | `/_otlp/v1/metrics` | {applies_to}`stack: ga 9.2+` |
| Logs | `/_otlp/v1/logs` | {applies_to}`stack: preview 9.5` |
| Traces | `/_otlp/v1/traces` | {applies_to}`stack: preview 9.5` |

:::{important}
{{es}} only supports [OTLP/HTTP](https://opentelemetry.io/docs/specs/otlp/#otlphttp), not [OTLP/gRPC](https://opentelemetry.io/docs/specs/otlp/#otlpgrpc).
:::

## When to use the {{es}} OTLP endpoint

For most users, one of the following higher-level ingestion paths is recommended:

| Deployment | Recommended ingestion path |
| --- | --- |
| {{ech}} and {{serverless-short}} | [{{motlp}}](opentelemetry://reference/motlp.md) |
| {{ece}}, {{eck}}, and self-managed | OpenTelemetry Collector in [Gateway mode](elastic-agent://reference/edot-collector/config/default-config-standalone.md#gateway-mode), using the [{{es}} exporter](opentelemetry://reference/edot-collector/components/elasticsearchexporter.md) |

Use {{motlp}} if it's available in your deployment, even when an application can target the {{es}} OTLP endpoint directly.

For an overview of the recommended OpenTelemetry-based ingestion architecture, refer to the [EDOT reference architecture](opentelemetry://reference/architecture/index.md).

Use the {{es}} OTLP endpoint directly when one of the following applies:

* You have an application that exports OTLP natively and you want it to send data to {{es}} without running an OpenTelemetry Collector.
  For example, a lightweight development setup (SDK to {{es}}).
* You operate a self-managed gateway Collector and prefer the `OTLP/HTTP` exporter over the [{{es}} exporter](opentelemetry://reference/edot-collector/components/elasticsearchexporter.md).

:::{warning}
Don't send telemetry from many individual applications directly to the {{es}} OTLP endpoint at the same time.
Send to an OpenTelemetry Collector first so it can absorb connection churn and batch records to improve ingestion performance.
:::

## Advantages of OTLP ingest over Bulk API

Compared to the Bulk API, ingesting through OTLP offers:

* Improved ingestion performance, especially for payloads with many resource attributes.
* Simplified mapping: data streams, index templates, dimensions, and metrics are derived dynamically from OTLP metadata.
  There's no need to set them up manually.

## How to send data to the {{es}} OTLP endpoint

### Create an API key

Authenticate to the {{es}} OTLP endpoint with an API key.
Refer to the API key documentation for your deployment type for instructions on how to create one:

* [{{es}} API keys](/deploy-manage/api-keys/elasticsearch-api-keys.md) (self-managed, {{ece}}, {{eck}})
* [{{ech}} API keys](/deploy-manage/api-keys/elastic-cloud-api-keys.md)
* [{{ece}} API keys](/deploy-manage/api-keys/elastic-cloud-enterprise-api-keys.md)
* [{{serverless-short}} project API keys](/deploy-manage/api-keys/serverless-project-api-keys.md)

The API key needs `create_doc` and `auto_configure` privileges on the data stream patterns it writes to.
`create_doc` allows writing documents without overwriting existing ones.
`auto_configure` allows the endpoint to create the target data streams on first write.

The minimum index patterns depend on which signals you ingest:

| Signals ingested | Required `names` patterns |
| --- | --- |
| Metrics | `metrics-*` |
| Logs | `logs-*` |
| Traces | `traces-*`, `logs-*` |
| All three | `metrics-*`, `logs-*`, `traces-*` |

Traces ingestion also writes span events to `logs-*` data streams, so it requires both patterns.

For example, an API key role descriptor that allows ingesting all three signals:

```json
{
  "indices": [
    {
      "names": ["logs-*", "metrics-*", "traces-*"],
      "privileges": ["create_doc", "auto_configure"]
    }
  ]
}
```

### Configure an OpenTelemetry Collector

To send data from an OpenTelemetry Collector to an {{es}} OTLP endpoint, configure the [`OTLP/HTTP` exporter](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/otlphttpexporter):

```yaml
exporters:
  otlphttp/elasticsearch:
    endpoint: <es_endpoint>/_otlp
    headers:
      Authorization: "ApiKey <api_key>"
    sending_queue:
      enabled: true
      sizer: bytes <1>
      queue_size: 50_000_000 <2>
      block_on_overflow: true
      batch: <3>
        flush_timeout: 1s
        min_size: 1_000_000
        max_size: 4_000_000
service:
  pipelines:
    logs:
      exporters: [otlphttp/elasticsearch]
      receivers: ...
    traces:
      exporters: [otlphttp/elasticsearch]
      receivers: ...
    metrics:
      exporters: [otlphttp/elasticsearch]
      receivers: ...
```

1. Sizes the queue and batches by uncompressed bytes.
2. Limits the queue to 50 MB of uncompressed data.
   Increasing this value can absorb longer {{es}} outages or traffic bursts, but also increases Collector memory usage.
3. Controls the uncompressed batch size sent to {{es}}.
   In this example, batches are sent at 1 MB and capped at 4 MB.
   Larger batches reduce request overhead, but increase peak memory usage and the amount of data retried after a failed request.

The exporter appends the signal-specific path (`/v1/logs`, `/v1/traces`, `/v1/metrics`) to the configured `endpoint`.

These values are starting points for a gateway Collector.
Tune them for your workload and Collector resources.
They are local to each Collector instance and don't increase {{es}} ingest capacity.
If many applications need to send telemetry, scale out the gateway Collector instead of sending directly from each application.

Supported `compression` values are `gzip` (the `OTLP/HTTP` exporter default) and `none`.

To send data from a custom application, use the [OpenTelemetry language SDK](https://opentelemetry.io/docs/getting-started/dev/) of your choice and point its OTLP/HTTP exporter at the corresponding {{es}} OTLP endpoint path.

:::{note}
Only `encoding: proto` is supported, which the `OTLP/HTTP` exporter uses by default.
:::

## Routing to data streams

By default, records are written to the following data streams:

| Signal | Default data stream |
| --- | --- |
| Logs | `logs-generic.otel-default` |
| Traces | `traces-generic.otel-default` |
| Metrics | `metrics-generic.otel-default` |

For more about how OTLP metrics are stored as time series data streams, refer to [Ingest metrics into a TSDS using the OTLP/HTTP endpoint](/manage-data/data-store/data-streams/tsds-ingest-otlp.md).

The target data stream name follows the pattern `<type>-<dataset>.otel-<namespace>`.
You can influence `dataset` and `namespace` by setting attributes on your data:

* Set `data_stream.dataset` and/or `data_stream.namespace` as attributes.
  Precedence: data point or log record attribute, then scope attribute, then resource attribute.
* Otherwise, if the scope name contains `/receiver/<somereceiver>`, `data_stream.dataset` is set to the receiver name.
* Otherwise, `data_stream.dataset` falls back to `generic` and `data_stream.namespace` falls back to `default`.

Examples:

| Signal | Attributes or scope name | Target data stream |
| --- | --- | --- |
| Logs | `data_stream.dataset: nginx.access`, `data_stream.namespace: prod` | `logs-nginx.access.otel-prod` |
| Traces | `data_stream.dataset: checkout`, `data_stream.namespace: staging` | `traces-checkout.otel-staging` |
| Metrics | Scope name contains `/receiver/hostmetrics`, no `data_stream.*` attributes | `metrics-hostmetrics.otel-default` |
| Metrics | No matching attributes or receiver scope name | `metrics-generic.otel-default` |

## Configure histogram handling for metrics
```{applies_to}
stack: preview =9.3, ga 9.4+
```

You can configure how OTLP histogram metrics are mapped using the `xpack.otel_data.histogram_field_type` cluster setting.
Valid values are:

 - `histogram` (default on {applies_to}`stack: preview =9.3`): Map histograms as T-Digests using the `histogram` field type
 - `exponential_histogram` (default on {applies_to}`stack: ga 9.4+`): Map histograms as exponential histograms using the `exponential_histogram` field type

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

This setting only applies to metrics ingested through the {{es}} OTLP endpoint.
Documents ingested using the Bulk API (for example through the {{es}} exporter for the OpenTelemetry Collector) are not affected.

## Metrics temporality
```{applies_to}
stack: ga 9.5
```

The OTLP endpoint preserves the [temporality](/manage-data/data-store/data-streams/metrics-temporality.md) of ingested metrics and stores it in a `temporality` [dimension](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md#time-series-dimension). This allows {{es}} to correctly interpret counter and histogram values during [ES|QL time series queries](/manage-data/data-store/data-streams/metrics-temporality.md#temporality-and-queries) and [downsampling](/manage-data/data-store/data-streams/metrics-temporality.md#temporality-and-downsampling).

The `temporality` dimension is set automatically based on the OTLP [AggregationTemporality](https://opentelemetry.io/docs/specs/otel/metrics/data-model/#temporality) of each metric data point. No additional configuration is needed.

Note that cumulative temporality for histograms is only supported if `xpack.otel_data.histogram_field_type` is set to `exponential_histogram` (which is the default).

## Limitations

* **Delivery guarantees:** {{es}} can only acknowledge an OTLP request as a whole, not on a per-record basis.
  If part of a request fails, the client retries the entire batch, which can produce duplicate logs or trace spans.
  Metrics are not affected because metric points written to time series data streams are [deduplicated based on their dimensions and timestamp](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md#time-series-dimension).
* **Profiles:** Profiles are not supported.
  To ingest profiles, use a distribution of the OpenTelemetry Collector that includes the [{{es}} exporter](opentelemetry://reference/edot-collector/components/elasticsearchexporter.md), such as the [{{edot}} (EDOT) Collector](opentelemetry://reference/edot-collector/index.md).
* **Histogram temporality:** Histograms are only supported in delta temporality.
  Set the temporality preference to delta in your SDKs, or use the [`cumulativetodelta` processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/cumulativetodeltaprocessor) so cumulative histograms aren't dropped.
* **Exemplars:** Exemplars are not supported yet.
