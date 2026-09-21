---
navigation_title: Manage storage
description: Control metrics storage costs using TSDS, downsampling, cardinality management, and Index Lifecycle Management.
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

## Time Series Data Streams (TSDS) [metrics-manage-storage-tsds]

A time series data stream (TSDS) is an {{es}} data stream built for metrics. It stores each series (for example, CPU usage for one host) as a sequence of timestamped samples, and it sorts those samples so similar values compress well. In Elastic's benchmarks, metrics in a TSDS used up to 70% less disk space than the same data in a regular data stream. The exact savings depend on your data set.

Metrics you ingest with OTLP or Prometheus remote write land in a TSDS by default. Choose a TSDS when you add metrics in near real time and in `@timestamp` order. For logs or traces, use a logs data stream or a regular data stream instead.

To learn how TSDS storage and dimensions work, refer to [Time series data streams](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md). To try a TSDS with sample data, follow the [TSDS quickstart](/manage-data/data-store/data-streams/quickstart-tsds.md).

## Metric temporality [metrics-manage-storage-temporality]
```{applies_to}
stack: ga 9.5+
serverless: ga
```

When counters and histograms live in a TSDS, temporality is how each sample relates to the last one. Cumulative values are running totals since the process started. Delta values are the change since the previous sample. {{es}} needs the same temporality your producer uses. If they do not match, rates, aggregations, and downsampling can be wrong.

For how to set and verify temporality, refer to [Metric temporality](/manage-data/data-store/data-streams/metric-temporality.md).

## Downsampling [metrics-manage-storage-downsampling]

Downsampling works with a TSDS only. As metrics age, you usually need less detail: last week's CPU at 10-second resolution matters less than the hourly trend. Downsampling replaces those raw samples with coarser buckets plus min, max, sum, and similar stats, so you keep long-term trends at a fraction of the storage cost.

You typically turn it on in an {{ilm-init}} policy or a data stream lifecycle, not with a one-off API call.

For configuration and how to query the coarser buckets, refer to [Downsampling a time series data stream](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md).

## Cardinality and dimensions [metrics-manage-storage-cardinality]

Cardinality is the number of unique dimension combinations on a metric. A request-count metric labeled with `host`, `region`, and `status_code` can produce `hosts × regions × status_codes` separate time series. Each series uses storage and query cost, so an extra high-cardinality label can grow a data stream far faster than extra samples on an existing series. High cardinality is a common cause of unexpected storage growth and slow queries.

TSDS tracks dimension combinations explicitly, which stores high-cardinality data more efficiently than a regular data stream and also makes a cardinality problem easier to identify.

For how {{es}} defines and limits dimension fields, refer to [Dimensions](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md#time-series-dimension).

## Retention [metrics-manage-storage-retention]

Retention is how long metrics stay in {{es}}, when backing indices roll over, and when old data is deleted.

{applies_to}`serverless: unavailable` On the {{stack}}, {{ilm-cap}} ({{ilm-init}}) automates those actions with policies that move data through hot, warm, cold, frozen, and delete phases. Refer to [{{ilm-cap}}](/manage-data/lifecycle/index-lifecycle-management.md) for policy phases and how to apply them.

Data stream lifecycle is a built-in alternative that sets rollover, retention, and downsampling on the data stream itself. It is available on the {{stack}} and is the retention option for {{serverless-short}}. Refer to [Data stream lifecycle](/manage-data/lifecycle/data-stream.md) for how to set retention on the data stream.

## Related pages [metrics-manage-storage-related]

- [Ingest metrics](/solutions/observability/metrics/ingest.md)
- [Plan your metrics setup](/solutions/observability/metrics/plan-your-setup.md)
