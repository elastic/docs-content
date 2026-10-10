---
navigation_title: "Load historical data"
description: Load historical documents into a time series data stream using the live stream for recent timestamps and a separate stream for data older than the eligible write window.
applies_to:
  stack: ga 9.5+
products:
  - id: elasticsearch
type: how-to
---

# Load historical data into a {{tsds}} [load-historical-tsds]

There are two methods for loading historical documents into a {{tsds}} ({{tsds-init}}).
If the timestamps fall inside the [eligible write window](/manage-data/data-store/data-streams/time-bound-tsds.md#tsds-past-index-creation), turn on past index creation and load the documents into the existing stream.
If they're older, load them into a separate historical stream.

Follow [Load data within the eligible write window](#load-data-within-the-eligible-write-window) or [Load data beyond the eligible write window](#load-data-beyond-the-eligible-write-window) based on whether your timestamps fall inside that window.

## Before you begin

Loading months of historical data can trigger significant storage use, force merge activity, and lifecycle processing in parallel.
Verify that your cluster has enough available resources before you start.

## Load data within the eligible write window [load-data-within-the-eligible-write-window]

This approach works well when you're backfilling recent history alongside live ingestion, such as late-arriving metrics or a short bootstrap period.

:::::{stepper}
::::{step} Turn on past index creation

:::{include} /manage-data/_snippets/enable-backfill.md
:::

After you turn on past index creation, {{es}} creates past backing indices as documents arrive.
Write-time deduplication and {{tsds-init}} storage optimizations apply to historical data the same way they apply to live data.

:::{note}
You need the `auto_configure` index privilege to trigger past index creation.
For details, refer to [Secure a {{tsds-init}}](/manage-data/data-store/data-streams/set-up-tsds.md#secure-tsds).
:::
::::

::::{step} Index the historical documents

Point your migration or replay pipeline at the live {{tsds}}.
You can use the same APIs you use for live data.

If the stream already has a downsampling lifecycle, those past indices might qualify immediately.
{{es}} ages them from the data they contain, not from when the index was created.
To limit concurrent downsampling per data stream, configure the [`data_streams.lifecycle.downsampling.max_indices_in_progress`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-downsampling-max-indices-in-progress) cluster setting.

For an example of setting up a {{tsds-init}} and loading historical data into it, refer to [Set up a {{tsds}}](/manage-data/data-store/data-streams/set-up-tsds.md).
::::

::::{step} Confirm the load

Use the [get data stream API]({{es-apis}}operation/operation-indices-get-data-stream) to check that backing indices cover the timestamps you loaded.
For example:

```console
GET _data_stream/metrics-weather-sensors
```

The response lists each backing index and the time range it accepts.
::::
:::::

## Load data beyond the eligible write window [load-data-beyond-the-eligible-write-window]

You can't load data older than the eligible write window directly into a {{tsds-init}}.
For example, if downsampling makes indices read-only after seven days, you can't backfill eighteen months of history into that same data stream.

Instead, create a separate historical {{tsds-init}} without a lifecycle, load the data, then add a [data stream lifecycle](/manage-data/lifecycle/data-stream.md) when the load is complete.

:::::{stepper}
::::{step} Create an index template for the historical data stream

Use the same mappings as your live {{tsds-init}}, but don't include a lifecycle policy in the template.
For example, use the [create index template]({{es-apis}}operation/operation-indices-put-index-template) API:

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
For example, use the [create a data stream]({{es-apis}}operation/operation-indices-create-data-stream) API:

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

For an example of how to check disk space with the [cat allocation API]({{es-apis}}operation/operation-cat-allocation), refer to [Estimate the amount of required disk capacity](/troubleshoot/elasticsearch/increase-capacity-data-node.md#estimate-required-capacity).
:::
::::

::::{step} Add data stream lifecycle

When the load is complete, add a [data stream lifecycle](/manage-data/lifecycle/data-stream.md) to the historical data stream.
For example, use the [update data stream lifecycles]({{es-apis}}operation/operation-indices-put-data-lifecycle) API:

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
When you add a lifecycle to a data stream with many indices that qualify for downsampling, data stream lifecycle can queue multiple downsampling operations at once.
To limit concurrent downsampling per data stream, configure the [`data_streams.lifecycle.downsampling.max_indices_in_progress`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-downsampling-max-indices-in-progress) cluster setting.
For details, refer to [Downsample with a data stream lifecycle](/manage-data/data-store/data-streams/run-downsampling.md#downsample-with-a-data-stream-lifecycle).
If you include `data_retention` settings, data stream lifecycle deletes expired backing indices but does not remove the data stream itself.
::::

::::{step} Query across both data streams

Query both streams with a wildcard pattern or a [data stream alias](/manage-data/data-store/aliases.md).
For example, use the [search]({{es-apis}}operation/operation-search) API:

```console
GET metrics-*/_search
{
  "size": 10,
  "sort": [{ "@timestamp": "desc" }]
}
```

The results include documents from both the live stream and the historical stream.
::::
:::::
Delete historical data streams manually when their data is no longer needed.

## Limitations

Backfill and creation of past indices have the following limitations:

- System data streams are excluded.
- {{ccr-cap}} ({{ccr-init}}) follower data streams rely on the leader data stream, so you can't backfill follower streams directly.

## Next steps

- [Downsample a time series data stream](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) to reduce storage after historical data ages
- [Reindex a time series data stream](/manage-data/data-store/data-streams/reindex-tsds.md) if you need to copy data to a new {{tsds-init}} instead of backfilling in place

## Related pages

- [Time-bound indices](/manage-data/data-store/data-streams/time-bound-tsds.md) for eligible write window and past index creation details
