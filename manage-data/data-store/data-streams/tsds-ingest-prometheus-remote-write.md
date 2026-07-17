---
navigation_title: "Prometheus remote write endpoint"
applies_to:
  stack: preview =9.4, ga 9.5+
  serverless: ga
products:
  - id: elasticsearch
---

# Prometheus remote write endpoint

In addition to the ingestion of metrics data through the bulk API,
{{es}} offers an endpoint that natively supports the [Prometheus remote write protocol](https://prometheus.io/docs/concepts/remote_write_spec/).

The endpoint is available under `/_prometheus/api/v1/write`.

:::{note}
If you are using {{serverless-full}}, use [managed inputs](opentelemetry://reference/motlp/prometheus-remote-write.md) to send Prometheus metrics instead. Managed inputs are the recommended ingestion path for {{ecloud}} deployments and provide durable buffering, unified authentication, and back-pressure handling.
:::

## Overview

The Prometheus remote write endpoint allows you to send metrics data directly from Prometheus or any Prometheus remote write-compatible client to {{es}}.
Data is automatically stored in [time series data streams (TSDS)](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md).

Ingesting metrics data using the Prometheus remote write endpoint has the following advantages:

* Direct ingestion from Prometheus without needing an intermediate pipeline or converter.
* Simplified index mapping:
  there's no need to manually create data streams, index templates, or define dimensions and metrics.
  Metrics are dynamically mapped based on Prometheus naming conventions.
* Prometheus labels are automatically mapped as time series dimensions.
* Metric types are inferred from naming conventions:
  fields ending in `_sum`, `_count`, `_total`, or `_bucket` are mapped as counters; all others are mapped as gauges.

## How to send data to the Prometheus remote write endpoint

### From Prometheus

To send data from Prometheus to the {{es}} remote write endpoint,
add a `remote_write` configuration to your `prometheus.yml`:

```yaml
remote_write:
  - url: "https://<es_endpoint>/_prometheus/api/v1/write"
    authorization:
      type: ApiKey
      credentials: <api_key>
    # basic_auth:
    #   username: <user>
    #   password: <password>
```

### From Grafana Alloy

To send data using [Grafana Alloy](https://grafana.com/docs/alloy/latest/),
use the `prometheus.remote_write` component:

```
prometheus.remote_write "elasticsearch" {
  endpoint {
    url = "https://<es_endpoint>/_prometheus/api/v1/write"

    headers = {
      "Authorization" = "ApiKey <api_key>",
    }

    // basic_auth {
    //   username = "<user>"
    //   password = "<password>"
    // }
  }
}
```

### Request format

The endpoint accepts `POST` requests with:

* Content type: `application/x-protobuf`
* Compression: `snappy` (as mandated by the Prometheus remote write specification) or uncompressed
* Body: Protocol Buffers encoded `WriteRequest` message as defined by the [Prometheus remote write 1.0 specification](https://prometheus.io/docs/concepts/remote_write_spec/)

## Send data to different data streams

By default, metrics are ingested into the `metrics-generic.prometheus-default` data stream.
You can control the target data stream using URL path parameters or per-time-series labels.
In both cases, Elasticsearch sanitizes dataset and namespace values, replacing any character that is not alphanumeric, a hyphen, or an underscore with `_`.

### Route by URL path

Set the dataset and namespace via URL path segments:

| Endpoint | Data stream |
| --- | --- |
| `/_prometheus/api/v1/write` | `metrics-generic.prometheus-default` |
| `/_prometheus/metrics/{dataset}/api/v1/write` | `metrics-{dataset}.prometheus-default` |
| `/_prometheus/metrics/{dataset}/{namespace}/api/v1/write` | `metrics-{dataset}.prometheus-{namespace}` |

For example, to route infrastructure metrics to a dedicated data stream, set the remote write URL to:

```yaml
remote_write:
  - url: "https://<es_endpoint>/_prometheus/metrics/infrastructure/production/api/v1/write"
```

This sends data to the `metrics-infrastructure.prometheus-production` data stream.

### Route by labels

You can also route individual time series to different data streams by attaching `data_stream_dataset` and `data_stream_namespace` labels to each time series. These labels take precedence over the URL path when set and allow a single remote write endpoint to fan out metrics to multiple data streams.

Elasticsearch treats these as control fields and does not store them in the document's `labels` object.

If only one of the two labels is present on a time series, the other value falls back to the URL path segment (or the default if no path segment was given).

Use `write_relabel_configs` to add routing labels before sending:

```yaml
remote_write:
  - url: "https://<es_endpoint>/_prometheus/api/v1/write"
    write_relabel_configs:
      - target_label: data_stream_dataset
        replacement: myapp
      - target_label: data_stream_namespace
        replacement: production
```

This example attaches `data_stream_dataset=myapp` and `data_stream_namespace=production` to every time series in this remote write target and routes all metrics to `metrics-myapp.prometheus-production`.

## Data mapping

Incoming Prometheus time series are mapped as follows:

| Prometheus concept | {{es}} field | Description |
| --- | --- | --- |
| Timestamp | `@timestamp` | The sample timestamp (in milliseconds) |
| `__name__` label | `metrics.<metric_name>` | The metric value, stored as a field named after the metric |
| `data_stream_dataset` label | _(routing only)_ | Routes the time series to the specified dataset; not stored in `labels` |
| `data_stream_namespace` label | _(routing only)_ | Routes the time series to the specified namespace; not stored in `labels` |
| All other labels (including `__name__`) | `labels.<label_name>` | Mapped as time series dimensions |

### Metric types

Metric types are automatically inferred from metric names using dynamic templates:

* **Counter**: Metric names ending in `_sum`, `_count`, `_total`, or `_bucket` are mapped as `double` with `time_series_metric: counter`.
* **Gauge**: All other metric names are mapped as `double` with `time_series_metric: gauge`.

This means Prometheus histograms and summaries are supported through their component metrics (`_sum`, `_count`, `_bucket`),
with each component automatically receiving the correct metric type.

### Customize metric type mappings

You can override or extend the default metric type inference by creating a `metrics-prometheus@custom` component template with additional dynamic templates.

For example, to map metrics ending in `_counter` as counters:

```console
PUT /_component_template/metrics-prometheus@custom
{
  "template": {
    "mappings": {
      "dynamic_templates": [
        {
          "counter": {
            "path_match": ["metrics.*_counter"],
            "mapping": {
              "type": "double",
              "time_series_metric": "counter"
            }
          }
        }
      ]
    }
  }
}
```

Custom dynamic templates are merged with the built-in ones. The built-in counter patterns (`_sum`, `_count`, `_total`, `_bucket`) and the default gauge fallback continue to apply alongside your custom rules.

### Index template

{{es}} automatically installs a built-in index template matching `metrics-*.prometheus-*` that configures:

* Time series data stream (TSDS) mode
* Labels as [passthrough](/manage-data/data-store/mapping/dynamic-mapping.md) dimensions
* Metrics as passthrough fields with dynamic template-based type inference
* A total field limit of 10,000
* [Failure store](/manage-data/data-store/data-streams/failure-store.md) enabled

## Limitations

* Only the Prometheus remote write 1.0 protocol is supported. Remote write 2.0 is not yet supported.
* Time series with a missing `__name__` label are dropped.
* Samples with non-finite values (NaN, Infinity) are silently dropped.
* [Staleness markers](https://prometheus.io/docs/prometheus/latest/querying/basics/#staleness) are not supported.
