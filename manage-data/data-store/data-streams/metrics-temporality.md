---
navigation_title: "Metrics temporality"
applies_to:
  stack: ga 9.5
  serverless: ga
products:
  - id: elasticsearch
---

# Metrics temporality [metrics-temporality]

When working with metrics in a [time series data stream](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) (TSDS), the _temporality_ of a metric determines how its values relate to one another over time. {{es}} supports two temporality models: **cumulative** and **delta**.

Understanding temporality is important because it affects how {{es}} interprets metric values during queries, aggregations, and [downsampling](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md).

## Cumulative vs. delta temporality [cumulative-vs-delta]

The difference between cumulative and delta temporality is best explained with a counter metric that tracks the number of HTTP requests a server has handled.

### Cumulative temporality

With cumulative temporality, each data point represents the total count since the process started. The values are monotonically increasing (or reset to zero when the process restarts).

| Timestamp | Value | Meaning                         |
|-----------|-------|---------------------------------|
| 10:01     | 5     | 5 total requests since start    |
| 10:02     | 12    | 12 total requests since start   |
| 10:03     | 20    | 20 total requests since start   |

To determine the rate of change, {{es}} computes the difference between consecutive values. Between 10:01 and 10:02, the rate was 7 requests per interval.

This is the default temporality for `counter` metrics in {{es}}.

### Delta temporality

With delta temporality, each data point represents the change since the previous measurement. The values are independent of one another.

| Timestamp | Value | Meaning                          |
|-----------|-------|----------------------------------|
| 10:01     | 5     | 5 new requests in this interval  |
| 10:02     | 7     | 7 new requests in this interval  |
| 10:03     | 8     | 8 new requests in this interval  |

To determine the rate of change, {{es}} uses the value directly. At 10:02, the rate was 7 requests per interval.

This is the default temporality for `histogram` metrics in {{es}}.

## Configure temporality [configure-temporality]

If you use managed inputs (e.g. the OTLP intake or Prometheus remote write) you don't have to configure anything.
The OTLP intake comes with a dimension called `temporality` preconfigured in the mappings and preserves the temporality of ingested metrics from the OTLP [temporality metadata](https://opentelemetry.io/docs/specs/otel/metrics/data-model/#temporality).
Prometheus remote write V1 only support counters and classic prometheus histograms (represented as counters) which are always cumulative. As this matches the default temporality for counters, the {{es}} remote write endpoint does not set up a temporality field.

If you are manually ingesting metrics into custom indices (e.g. via _bulk), you have to explicitly configure temporality on your datastream.
To do so, use the [`index.time_series.temporality_field`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-temporality-field) index setting. This setting specifies the name of the field that stores the temporality for each document.

The temporality field must:

- Be mapped as [`keyword`](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#keyword-field-type)
- Be configured as a [dimension](time-series-data-stream-tsds.md#time-series-dimension) (`time_series_dimension: true`)

Its value must be one of:

- `delta` — metrics in the document use delta temporality
- `cumulative` — metrics in the document use cumulative temporality

If the field is absent or contains any other value, {{es}} uses the default temporality for each metric type: cumulative for counters and delta for histograms.
You don't have to explicitly define the mapping for the field, it will be created automatically based on the index setting.

Note that because `temporality` is a dimension, you can have mixed temporalities per metric: Some series can have `delta` temporality, while others are `cumulative`.
This is automatically handled when the data is queried or downsampled.

## How temporality affects queries [temporality-and-queries]

The temporality field is used automatically by PromQL and ES|QL time series queries. When you query a TSDS using the [`TS` command](elasticsearch://reference/query-languages/esql/commands/ts.md), {{es}} reads each document's temporality value and adjusts the behavior of time series aggregation functions like `rate` and `increase` accordingly:

- **Cumulative metrics:** {{es}} computes the difference between consecutive values to determine the rate of change.
- **Delta metrics:** {{es}} uses the values directly, since they already represent changes.

This means that the `rate` and `increase` functions produce correct results regardless of whether the underlying data is cumulative or delta, as long as the temporality is set correctly.
Note that in ES|QL you cannot use `rate` or `increase` on histograms: Instead, ES|QL will automatically use an inner, per-series aggregation which merges the histograms taking the temporality into account.
This is equivalent to how `increase` works for native histograms in PromQL. For example, the following two queries are equivalent:

## How temporality affects downsampling [temporality-and-downsampling]

[Downsampling](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) also respects the temporality field. Because the temporality field is a dimension, cumulative and delta data points are always in separate time series and are downsampled independently.

For `counter` metrics:

- **Cumulative counters** are downsampled by storing representative data points from the bucket (the first value, plus up to two points if a counter reset is detected).
- **Delta counters** are downsampled by summing the values in the bucket.

## OTLP ingestion [temporality-and-otlp]

When you ingest metrics through the [OTLP/HTTP endpoint](/manage-data/ingest/otlp-endpoint.md), {{es}} automatically populates the temporality field based on the OpenTelemetry [temporality metadata](https://opentelemetry.io/docs/specs/otel/metrics/data-model/#temporality). No additional configuration is needed for OTLP-ingested metrics.
