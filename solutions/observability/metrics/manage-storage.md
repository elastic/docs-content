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

Refer to [Time series data streams](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) for more information. To try a TSDS with sample data, refer to the [TSDS quickstart](/manage-data/data-store/data-streams/quickstart-tsds.md).

## Metric temporality [metrics-manage-storage-temporality]
```{applies_to}
stack: ga 9.5+
```

When counters and histograms live in a TSDS, temporality is how each sample relates to the last one. Cumulative values are running totals since the process started. Delta values are the change since the previous sample. {{es}} needs the same temporality your producer uses. If they do not match, rates, aggregations, and downsampling can be wrong.

Refer to [Metric temporality](/manage-data/data-store/data-streams/metric-temporality.md) for more information.

## Downsampling [metrics-manage-storage-downsampling]

Downsampling works with a TSDS only. As metrics age, you usually need less detail: last week's CPU at 10-second resolution matters less than the hourly trend. Downsampling replaces those raw samples with coarser buckets plus min, max, sum, and similar stats, so you keep long-term trends at a fraction of the storage cost.

You typically turn it on in an {{ilm-init}} policy or a data stream lifecycle, not with a one-off API call.

Refer to [Downsampling a time series data stream](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) for more information, including how to configure downsampling and query downsampled data.

## Cardinality management [metrics-manage-storage-cardinality]

Cardinality is the number of unique dimension combinations on a metric. A request-count metric labeled with `host`, `region`, and `status_code` can produce `hosts × regions × status_codes` separate time series. Each series uses storage and query cost, so an extra high-cardinality label can grow a data stream far faster than extra samples on an existing series.

TSDS tracks dimension combinations explicitly, which stores high-cardinality data more efficiently than a regular data stream and also makes a cardinality problem easier to see.

Refer to [Cardinality and dimensions in Elastic metrics](/solutions/observability/metrics/cardinality-dimensions.md) for more information.

## Retention [metrics-manage-storage-retention]

Retention is how long metrics stay in {{es}}, when backing indices roll over, and when old data is deleted.

{applies_to}`serverless: unavailable` On the {{stack}}, {{ilm-cap}} ({{ilm-init}}) automates those actions with policies that move data through hot, warm, cold, frozen, and delete phases. Refer to [{{ilm-cap}}](/manage-data/lifecycle/index-lifecycle-management.md) for more information.

Data stream lifecycle is a built-in alternative that sets rollover, retention, and downsampling on the data stream itself. It is available on the {{stack}} and is the retention option for {{serverless-short}}. Refer to [Data stream lifecycle](/manage-data/lifecycle/data-stream.md) for more information.

## Related [metrics-manage-storage-related]

- [Ingest metrics](/solutions/observability/metrics/ingest.md)
- [Plan your metrics setup](/solutions/observability/metrics/plan-your-setup.md)
