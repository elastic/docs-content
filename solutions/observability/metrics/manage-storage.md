---
navigation_title: Manage storage
description: Control metrics storage costs using TSDS, downsampling, cardinality management, and index lifecycle management.
applies_to:
  stack: ga
  serverless:
    observability:
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Manage metrics storage [metrics-manage-storage]

Metrics data grows quickly. Use these tools to keep storage costs down, retain the history you still need, and avoid cardinality surprises.

## Time series data streams (TSDS) [metrics-manage-storage-tsds]

A time series data stream (TSDS) is an {{es}} data stream with `index.mode` set to `time_series`. It identifies each series by its dimension fields (for example, the host a CPU metric belongs to), stores values in metric fields typed as `counter`, `gauge`, or `histogram`, and sorts and compresses samples per series. In Elastic's benchmarks, metrics in a TSDS used 70% less disk space than the same data in a regular data stream. The exact impact varies by data set.

Naming a data stream `metrics-*` doesn't make it a TSDS. The index template that matches the data stream must set `index.mode: time_series`. Elastic's built-in templates do this for the OpenTelemetry Protocol (OTLP) and Prometheus remote write paths, so you don't create templates yourself:

- OTLP metrics from the Managed OTLP Endpoint, {{agent}} in OTel mode, and the {{es}} OTLP/HTTP endpoint land in `metrics-*.otel-*` data streams (`metrics-generic.otel-default` by default). To extend the mappings, use the `metrics-otel@custom` component template. Refer to [Ingest metrics into a TSDS using the OTLP/HTTP endpoint](/manage-data/data-store/data-streams/tsds-ingest-otlp.md).
- Prometheus remote write metrics land in `metrics-*.prometheus-*` data streams (`metrics-generic.prometheus-default` by default) through the built-in template for that pattern. To extend the mappings, use the `metrics-prometheus@custom` component template. Refer to [Index template](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md#index-template).
- {{agent}} integrations store metrics as a TSDS when the integration enables it.

Choose a TSDS when you add metrics in near real time and in `@timestamp` order. For logs or traces, use a logs data stream or a regular data stream instead.

To learn how TSDS storage, dimensions, and metric types work, refer to [Time series data streams](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md). To try a TSDS with sample data, follow the [TSDS quickstart](/manage-data/data-store/data-streams/quickstart-tsds.md).

## Metric temporality [metrics-manage-storage-temporality]
```{applies_to}
stack: ga 9.5+
serverless: ga
```

When counters and histograms live in a TSDS, temporality is how each sample relates to the last one. Cumulative values are running totals since the process started. Delta values are the change since the previous sample. {{es}} needs the same temporality your producer uses. If they don't match, rates, aggregations, and downsampling can be wrong.

For how to set and verify temporality, refer to [Metric temporality](/manage-data/data-store/data-streams/metric-temporality.md).

## Downsampling [metrics-manage-storage-downsampling]

Downsampling works with a TSDS only. As metrics age, you usually need less detail: last week's CPU at 10-second resolution matters less than the hourly trend. Downsampling replaces those raw samples with coarser buckets plus min, max, sum, and similar stats, so you keep long-term trends at a fraction of the storage cost.

You typically turn it on in an index lifecycle management ({{ilm-init}}) policy or a data stream lifecycle, not with a one-off API call.

For configuration and how to query the coarser buckets, refer to [Downsampling a time series data stream](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md).

## Cardinality and dimensions [metrics-manage-storage-cardinality]

Cardinality is the number of unique dimension combinations on a metric. A request-count metric labeled with `host`, `region`, and `status_code` can produce `hosts × regions × status_codes` separate time series. Each series uses storage and query cost, so an extra high-cardinality label can grow a data stream far faster than extra samples on an existing series. High cardinality is a common cause of unexpected storage growth and slow queries.

In a TSDS, every new combination of dimension values is a new series, so review which fields are dimensions before you add labels or attributes. For how {{es}} defines dimension fields, refer to [Dimensions](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md#time-series-dimension).

## Retention [metrics-manage-storage-retention]

Retention is how long metrics stay in {{es}}, when backing indices roll over, and when old data is deleted.

{applies_to}`serverless: unavailable` On the {{stack}}, {{ilm-cap}} ({{ilm-init}}) automates those actions with policies that move data through hot, warm, cold, frozen, and delete phases. Refer to [{{ilm-cap}}](/manage-data/lifecycle/index-lifecycle-management.md) for policy phases and how to apply them.

Data stream lifecycle is a built-in alternative that sets rollover, retention, and downsampling on the data stream itself. It's available on the {{stack}} and is the retention option for {{serverless-short}}. Refer to [Data stream lifecycle](/manage-data/lifecycle/data-stream.md) for how to set retention on the data stream.

## Related pages [metrics-manage-storage-related]

- [Ingest metrics](/solutions/observability/metrics/ingest.md)
- [Plan your metrics setup](/solutions/observability/metrics/plan-your-setup.md)
