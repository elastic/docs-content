---
navigation_title: "Load historical data"
applies_to:
  stack: ga 9.5
products:
  - id: elasticsearch
---

# Load historical data into a {{tsds}} [load-historical-tsds]

By default, a {{tsds-cap}} ({{tsds-init}}) works well for continuous, near-real-time ingestion.
Only documents with `@timestamp` values that fall inside the time range of existing backing indices are accepted.

If you turn on the [data_stream.past_tsdb_index_creation_enabled](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#time-series-data-stream) cluster setting, however, you can import historical data into an existing {{tsds-init}} using the same APIs you use for live data.
{{es}} creates the past backing indices needed to store past documents as they arrive.
The documents must fall within the [eligible write window](/manage-data/data-store/data-streams/time-bound-tsds.md#tsds-past-index-creation), which is the period of time between "current" and the data stream retention limit or the first occurrence of a lifecycle action that makes a backing index read-only, whichever occurs first.
Write-time deduplication and {{tsds-init}} storage optimizations apply to historical data the same way they apply to live data.

:::{note}
Users who trigger past index creation need the `auto_configure` index privilege.
For details, refer to [Secure a {{tsds-init}}](/manage-data/data-store/data-streams/set-up-tsds.md#secure-tsds).
:::

## Load data within the eligible write window

For data that falls within the eligible write window, point your migration or replay pipeline at the live {{tsds}}.
{{es}} creates past backing indices as needed.

This approach works well when you're backfilling recent history alongside live ingestion, such as late-arriving metrics or a short bootstrap period.

Go to [](/manage-data/data-store/data-streams/set-up-tsds.md) for an example of setting up and loading historical data into a new {{tsds}}.

## Load data beyond the eligible write window

You can't load data older than the eligible write window directly into a {{tsds-init}}.
For example, if downsampling makes indices read-only after seven days, you can't backfill eighteen months of history into that same data stream.

Instead, use a separate historical {{tsds-init}} without lifecycle, load the data, then add [data stream lifecycle](/manage-data/lifecycle/data-stream.md) when the load is complete.

:::::{stepper}
::::{step} Create an index template for the historical data stream

Use the same mappings as your live {{tsds-init}}, but don't attach a lifecycle policy in the template.
For example:

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

Create a data stream with a name that matches the pattern in the index template.
For example:

```console
PUT _data_stream/metrics-historical-2024
```

::::

::::{step} Index historical data

Index historical data into the historical data stream while current data continues flowing into the original {{tsds-init}}.

:::{important}
Historical data must fit on the target tier as a whole before you enable data stream lifecycle.
If you're importing a large data set, split it into batches.
Each batch should fit within available disk space at indexing time.
:::
::::

::::{step} Add data stream lifecycle

When the load is complete, add a [data stream lifecycle](/manage-data/lifecycle/data-stream.md) to the historical data stream.
For example:

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

Processing begins immediately and creates a backlog of downsampling work.
If you include `data_retention` settings, data stream lifecycle deletes expired backing indices but does not remove the data stream itself.
::::

::::{step} Query across both data streams

Query both streams with a wildcard pattern or a [data stream alias](/manage-data/data-store/aliases.md).
For example:

```console
GET metrics-*/_search
{
  "size": 10,
  "sort": [{ "@timestamp": "desc" }]
}
```

::::
:::::
Delete historical data streams manually when their data is no longer needed.

## Protect the cluster during large loads

Loading months of historical data can trigger significant storage use, force merge activity, and lifecycle processing in parallel.
Verify that your cluster has enough headroom before you start.

When you enable a lifecycle on a data stream with many indices that qualify for downsampling, data stream lifecycle can queue multiple downsampling operations at once.
To limit concurrent downsampling per data stream, configure the [`data_streams.lifecycle.downsampling.max_indices_in_progress`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-downsampling-max-indices-in-progress) cluster setting.
For details, refer to [Downsample with a data stream lifecycle](/manage-data/data-store/data-streams/run-downsampling.md#downsample-with-a-data-stream-lifecycle).

## Limitations

Backfill and creation of past indices have the following limitations:

- System data streams are excluded.
- {{ccr-cap}} ({{ccr-init}}) follower data streams rely on the leader data stream, so you can't backfill follower streams directly.

## Next steps

- [Time-bound indices](/manage-data/data-store/data-streams/time-bound-tsds.md) for eligible write window and past index creation details
- [Downsampling a time series data stream](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) to reduce storage after historical data ages
- [Reindex a time series data stream](/manage-data/data-store/data-streams/reindex-tsds.md) if you need to copy data to a new {{tsds-init}} instead of backfilling in place
