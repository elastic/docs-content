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

Metrics data can grow quickly. This page points you to the tools for controlling storage costs, managing retention, and keeping metric cardinality in check.

## Time Series Data Streams (TSDS) [metrics-manage-storage-tsds]

Metrics ingested using OTLP and Prometheus remote write are stored as TSDS by default. TSDS is a specialized {{es}} data stream format optimized for time-series data — it reduces storage by up to 70% compared to regular data streams through efficient columnar encoding and automatic rollover.

- [Time Series Data Streams (TSDS)](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) — overview and configuration
- [TSDS quickstart](/manage-data/data-store/data-streams/quickstart-tsds.md)

## Metric temporality [metrics-manage-storage-temporality]

Metric temporality describes how counter values are reported: as cumulative totals (from process start) or as delta values (change since last report). This affects storage and query behavior and must match between your producer and consumer.

- [Metric temporality](/manage-data/data-store/data-streams/metric-temporality.md)

## Downsampling [metrics-manage-storage-downsampling]

Downsampling reduces the number of data points stored by aggregating time-series data into coarser time buckets as data ages. This lets you retain long-term trend data at a fraction of the storage cost.

- [Downsampling a time series data stream](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) — overview
- [Downsampling concepts](/manage-data/data-store/data-streams/downsampling-concepts.md)
- [Run downsampling](/manage-data/data-store/data-streams/run-downsampling.md)
- [Query downsampled data](/manage-data/data-store/data-streams/query-downsampled-data.md)

## Cardinality management [metrics-manage-storage-cardinality]

High cardinality — a large number of unique label or dimension combinations — is one of the most common causes of unexpected storage growth and query slowness in metrics systems.

- [Cardinality and dimensions in Elastic metrics](/solutions/observability/metrics/cardinality-dimensions.md)

## Retention [metrics-manage-storage-retention]

Control how long metrics are retained using {{ilm-cap}} ({{ilm-init}}) or data stream lifecycle settings.

- [{{ilm-cap}}](/manage-data/lifecycle/index-lifecycle-management.md)
- [Data stream lifecycle](/manage-data/lifecycle/data-stream.md)

## Related [metrics-manage-storage-related]

- [Ingest metrics](/solutions/observability/metrics/ingest.md)
- [Plan your metrics setup](/solutions/observability/metrics/plan-your-setup.md)
