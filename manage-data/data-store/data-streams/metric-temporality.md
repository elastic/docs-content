---
navigation_title: "Metric temporality"
applies_to:
  stack: ga 9.5
  serverless: ga
description: Learn how cumulative and delta metric temporality work in Elasticsearch time series data streams, and how to configure it for queries and downsampling.
products:
  - id: elasticsearch
---

# Metric temporality [metric-temporality]

When working with counters and histograms in a [time series data stream](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) (TSDS), the _temporality_ of a metric determines how its values relate to one another over time. {{es}} supports two temporality models: **cumulative** and **delta**.

Understanding temporality is important because it affects how {{es}} interprets metric values during queries, aggregations, and [downsampling](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md).

## Cumulative versus delta temporality [cumulative-vs-delta]

The difference between cumulative and delta temporality is best explained with a counter metric that tracks the number of HTTP requests a server has handled.

### Cumulative temporality

With cumulative temporality, each data point represents the total count since the process started. The values are monotonically increasing (or reset to zero when the process restarts).

| Timestamp | Value | Meaning                         |
|-----------|-------|---------------------------------|
| 10:01     | 27    | 27 total requests since start   |
| 10:02     | 72    | 72 total requests since start   |
| 10:03     | 113   | 113 total requests since start  |

To determine the rate of change, {{es}} computes the difference between consecutive values. Between 10:01 and 10:02, the total number of requests increased by 45.
Therefore, the `increase` function yields 45 for this time interval. `rate` divides the total increase by the time interval in seconds. This yields 0.75 requests per second in this case, because the time range between 10:01 and 10:02 is 60 seconds.

This is the default temporality for [`counter`](time-series-data-stream-tsds.md#time-series-metric) metrics in {{es}}.

### Delta temporality

With delta temporality, each data point represents the change since the previous measurement. The values are independent of one another.

| Timestamp | Value | Meaning                          |
|-----------|-------|----------------------------------|
| 10:01     | 27    | 27 new requests in this interval |
| 10:02     | 45    | 45 new requests in this interval |
| 10:03     | 41    | 41 new requests in this interval |

To determine the rate of change, {{es}} uses the value directly.
This means that for the time interval between 10:01 and 10:02, as with cumulative temporality, `increase` yields 45 and `rate` 0.75.

This is the default temporality for [`histogram`](time-series-data-stream-tsds.md#time-series-metric) metrics in {{es}}.

## Configure temporality [configure-temporality]

If you use the [HTTP OTLP endpoint](/manage-data/data-store/data-streams/tsds-ingest-otlp.md), [managed OTLP intake](opentelemetry://reference/motlp.md), or [Prometheus remote write](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md), you don't have to configure anything.
Both OTLP intakes come with a dimension called `temporality` preconfigured in the mappings and preserve the temporality of ingested metrics from the OTLP [temporality metadata](https://opentelemetry.io/docs/specs/otel/metrics/data-model/#temporality).
Prometheus remote write V1 only supports counters and classic Prometheus histograms (represented as counters), which are always cumulative. As this matches the default temporality for counters, the {{es}} remote write endpoint does not set up a temporality field.

If you are manually ingesting metrics into custom indices (for example via `_bulk`), you have to explicitly configure temporality on your data stream.
To do so, use the [`index.time_series.temporality_field`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-temporality-field) index setting. This setting specifies the name of the field that stores the temporality for each document.

The temporality field must:

- Be mapped as [`keyword`](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#keyword-field-type)
- Be configured as a [dimension](time-series-data-stream-tsds.md#time-series-dimension) (`time_series_dimension: true`)

Its value must be one of:

- `delta`: metrics in the document use delta temporality
- `cumulative`: metrics in the document use cumulative temporality

If the field is absent or contains any other value, {{es}} uses the default temporality for each metric type: cumulative for counters and delta for histograms.
You don't need to explicitly define the mapping for the field. It's created automatically based on the index setting.

:::{note} 
Because `temporality` is a dimension, you can have mixed temporalities per metric: Some series can have `delta` temporality, while others are `cumulative`.
This is automatically handled when the data is queried or downsampled.
:::

## How temporality affects queries [temporality-and-queries]

The temporality field is used automatically by PromQL and ES|QL time series queries. When you query a TSDS using the [`TS` command](elasticsearch://reference/query-languages/esql/commands/ts.md), {{es}} reads each document's temporality value and adjusts the behavior of supported [time series aggregation functions](elasticsearch://reference/query-languages/esql/functions-operators/time-series-aggregation-functions.md) accordingly:

- **Cumulative metrics:** {{es}} computes the difference between consecutive values to determine the rate of change.
- **Delta metrics:** {{es}} uses the values directly, since they already represent changes.

The supported functions respecting the temporality are `rate`, `increase` and `irate`. So those functions produce the semantically expected results regardless of whether the underlying data is cumulative or delta, as long as the temporality is set correctly.
In ES|QL you cannot use any of those functions on histograms. Instead, ES|QL will automatically use an inner, per-series aggregation which merges the histograms taking the temporality into account.
This is equivalent to how `increase` works for native histograms in PromQL. For example, the following two queries are equivalent:

**ES|QL:**
```esql
TS my-metrics
| STATS PERCENTILE(request_duration, 80) BY endpoint, TBUCKET(1m)
```

Note that in ES|QL you must use the `TS` command. If you use `FROM`, the temporality will be ignored.

**PromQL:**
```
histogram_quantile(0.8, sum by (endpoint) (increase(request_duration[1m])))
```

## How temporality affects downsampling [temporality-and-downsampling]

[Downsampling](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) also respects the temporality field. Because the temporality field is a dimension, cumulative and delta data points are always in separate time series and are downsampled independently.

For details on how each metric type is downsampled, refer to [downsampling methods](/manage-data/data-store/data-streams/downsampling-concepts.md#downsampling-methods).
