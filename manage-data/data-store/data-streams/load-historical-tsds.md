---
navigation_title: "Load historical metrics"
applies_to:
  stack: ga 9.5
  serverless: ga
products:
  - id: elasticsearch
---

# Load historical metrics into a TSDS [load-historical-tsds]

In {{stack}} 9.5 and {{es-serverless}}, you can load historical metrics into an existing [time series data stream (TSDS)](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) using the same APIs you use for live data. This includes the bulk API, the [OpenTelemetry Protocol (OTLP) endpoint](/manage-data/data-store/data-streams/tsds-ingest-otlp.md), and the [Prometheus remote write endpoint](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md).

When past backing index creation is enabled, {{es}} creates the past backing indices needed to store historical documents as they arrive. Write-time deduplication and TSDS storage optimizations apply to historical data the same way they apply to live data.

Before you begin, review [Time-bound indices](/manage-data/data-store/data-streams/time-bound-tsds.md), especially the [eligible write window](/manage-data/data-store/data-streams/time-bound-tsds.md#tsds-eligible-write-window) and [backfill past timestamps](/manage-data/data-store/data-streams/time-bound-tsds.md#tsds-backfill-past-timestamps) sections.

## Enable past-index creation

Past backing index creation is disabled by default. Enable it at the cluster level:

```console
PUT _cluster/settings
{
  "persistent": {
    "data_stream.past_tsdb_index_creation_enabled": true
  }
}
```

For optional interval configuration, refer to [Configure past index intervals](/manage-data/data-store/data-streams/time-bound-tsds.md#configure-past-index-intervals).

## Load data into a new TSDS

To bootstrap a new TSDS with historical metrics:

1. [Create an index template](/manage-data/data-store/data-streams/set-up-tsds.md) for the TSDS.
2. Index a document with a current `@timestamp` to create the data stream.
3. Index historical documents using the bulk API or your preferred ingest endpoint.

Past backing indices are created automatically as historical documents arrive. By default, each past backing index covers one day of data.

```console
PUT metrics-sensors/_bulk
{ "create": { } }
{ "@timestamp": "2026-07-24T12:00:00.000Z", "sensor_id": "SENSOR-001", "temperature": 22.1 }
{ "create": { } }
{ "@timestamp": "2026-07-20T08:15:00.000Z", "sensor_id": "SENSOR-001", "temperature": 19.4 }
{ "create": { } }
{ "@timestamp": "2026-07-15T14:30:00.000Z", "sensor_id": "SENSOR-001", "temperature": 21.0 }
```

## Load data within the eligible write window

For data that falls within the [eligible write window](/manage-data/data-store/data-streams/time-bound-tsds.md#tsds-eligible-write-window), point your migration or replay pipeline at the live TSDS. {{es}} creates past backing indices as needed.

This approach works well when you're backfilling recent history alongside live ingestion, such as late-arriving metrics or a short bootstrap period.

## Load data beyond the eligible write window

You can't load data older than the eligible write window directly into a TSDS that already has read-only lifecycle actions configured. For example, if downsampling makes indices read-only after seven days, you can't backfill eighteen months of history into that same data stream.

Instead, use a separate historical TSDS without lifecycle actions, load the data, then add lifecycle management when the load is complete.

:::::{stepper}
::::{step} Create an index template for the historical data stream

Use the same mappings as your live TSDS, but don't attach a lifecycle policy in the template:

```console
PUT _index_template/metrics-historical
{
  "index_patterns": ["metrics-historical-*"],
  "data_stream": {},
  "template": {
    "settings": {
      "index.mode": "time_series"
    },
    "mappings": {
      "properties": {
        "@timestamp": { "type": "date" },
        "sensor_id": { "type": "keyword", "time_series_dimension": true },
        "temperature": { "type": "half_float", "time_series_metric": "gauge" }
      }
    }
  }
}
```

::::

::::{step} Create the historical data stream

```console
PUT _data_stream/metrics-historical-2024
```

::::

::::{step} Index historical data

Index historical data into the historical data stream while current data continues flowing into the original TSDS.
::::

::::{step} Add lifecycle management

When the load is complete, add [data stream lifecycle](/manage-data/lifecycle/data-stream.md) to the historical data stream. Lifecycle configuration is supported only at the data stream level, so use data stream lifecycle rather than {{ilm-init}}:

```console
PUT _data_stream/metrics-historical-2024/_lifecycle
{
  "enabled": true,
  "data_retention": "365d",
  "downsampling": [
    {
      "after": "7d",
      "fixed_interval": "10m"
    }
  ]
}
```

::::

::::{step} Query across both data streams

Query both streams with a wildcard pattern or a [data stream alias](/manage-data/data-store/aliases.md):

```console
GET metrics-*/_search
{
  "size": 10,
  "sort": [{ "@timestamp": "desc" }]
}
```

::::
:::::

:::{important}
Historical data must fit on the target tier as a whole before you enable lifecycle management. If you're importing a large dataset, split it into batches. Each batch should fit within available disk space at indexing time. When you enable lifecycle, processing begins immediately and can create a backlog of downsampling work.
:::

If retention is configured, lifecycle management deletes expired backing indices but does not remove the data stream itself. Delete historical data streams manually when their data is no longer needed.

## Protect the cluster during large loads

Loading months of historical data can trigger significant storage use, force merge activity, and lifecycle processing in parallel. Verify that your cluster has enough headroom before you start.

When you enable lifecycle on a data stream with many indices that qualify for downsampling, data stream lifecycle can queue multiple downsampling operations at once. To limit concurrent downsampling per data stream, configure the [`data_streams.lifecycle.downsampling.max_indices_in_progress`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-downsampling-max-indices-in-progress) cluster setting. For details, refer to [Downsample with a data stream lifecycle](/manage-data/data-store/data-streams/run-downsampling.md#downsample-with-a-data-stream-lifecycle).

## Limitations and prerequisites

Backfill and past-index creation have the following limitations:

- The TSDS must already exist with at least one time series backing index.
- Past-index creation does not apply to read-only backing indices. If downsampling or a {{search-snap}} transition has already run on a time period, documents for that period are still rejected.
- System data streams are excluded.
- {{ccr-cap}} ({{ccr-init}}) follower data streams rely on the leader data stream, so you can't backfill follower streams directly.
- Users who trigger past-index creation need the `auto_configure` index privilege. For details, refer to [Secure a time series data stream](/manage-data/data-store/data-streams/set-up-tsds.md#secure-tsds).

## Next steps

- [Time-bound indices](/manage-data/data-store/data-streams/time-bound-tsds.md) for eligible write window and past-index creation details
- [Downsampling a time series data stream](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) to reduce storage after historical data ages
- [Reindex a time series data stream](/manage-data/data-store/data-streams/reindex-tsds.md) if you need to copy data to a new TSDS instead of backfilling in place
