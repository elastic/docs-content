---
navigation_title: "Time-bound indices"
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Time-bound indices and dimension-based routing [time-bound-indices]

Unlike regular data streams that write only to the most recent backing index, {{tsds}} ({{tsds-init}}) are backed by a set of time-bound indices, each covering a contiguous, non-overlapping time range.
{{es}} enforces that the `@timestamp` for each ingested document falls within the time range of exactly one backing index.

## How time-bound indices work [tsds-accepted-time-range]

Each {{tsds-init}} backing index has a range of `@timestamp` values that it accepts, which are tracked in index settings.
When the {{tsds-init}} is created, the first backing index has the following range:

- Its [`index.time_series.start_time`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-start-time), which is the earliest accepted timestamp (inclusive), is set to `now` minus the [`index.look_back_time`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-look-back-time).
- Its [`index.time_series.end_time`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time), which is the latest accepted timestamp (exclusive), is set to `now` plus [`index.look_ahead_time`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-look-ahead-time).

Thereafter, {{es}} automatically configures the settings for backing indices as part of the index creation and rollover process.
Each new backing index starts at the previous index's `end_time` and extends further ahead using `look_ahead_time`.

When you add a document to the TSDS, {{es}} routes it to the appropriate backing index based on its `@timestamp` value.
This means a TSDS can write to multiple backing indices simultaneously, not only the most recent one.

:::{image} /manage-data/images/elasticsearch-reference-time-bound-indices.svg
:alt: Time bound indices
:::

Late-arriving data can still be indexed into an older backing index, as long as that index exists, remains writable, and its accepted time range includes the timestamp.
To inspect the accepted time ranges of TSDS backing indices, use the [get data stream API]({{es-apis}}operation/operation-indices-get-data-stream):

```console
GET _data_stream/my-tsds
```

By default, if no existing backing index can accept a document's `@timestamp`, {{es}} rejects the document.
{{es}} does not create missing past backing indices unless you [turn on past index creation](#tsds-past-index-creation).

::::{tip}
Writes might still be rejected even when a timestamp fits the accepted time range of a backing index. The following actions can affect the writable time range, either because they make a backing index read-only or remove it:

- [Delete](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-delete.md)
- [Downsample](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-downsample.md)
- [Force merge](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-forcemerge.md)
- [Read only](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-readonly.md)
- [Searchable snapshot](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md)
- [Shrink](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-shrink.md), which might revert the read-only status at the end of the action

{{ilm-cap}} will **not** proceed with running these actions until [`index.time_series.end_time`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time) has passed.
::::

## Past index creation [tsds-past-index-creation]
```{applies_to}
stack: ga 9.5
```

In addition to accepted time ranges for each backing index, a {{tsds}} has an _eligible write window_.
It is the period of time that extends from the present back to whichever comes first:

- the first lifecycle action that makes a backing index read-only (such as [downsampling](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) or a {{search-snap}} transition), or
- the data stream retention limit (configured in a [data stream lifecycle](/manage-data/lifecycle/data-stream.md), for example)

When the
[data_stream.past_tsdb_index_creation_enabled](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#time-series-data-stream) cluster setting is set to `true`, {{es}} automatically creates missing past backing indices for an existing {{tsds}} while indexing documents that fall within the eligible write window.

Timestamps outside the eligible write window or in the future are still rejected.
If a [failure store](/manage-data/data-store/data-streams/failure-store.md) is enabled, rejected timestamp failures can be redirected there.

:::{admonition} Lifecycle age for past indices

Past backing indices hold old data but are new indices.
{{es}} sets [`index.lifecycle.origination_date`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-data-stream-lifecycle-origination-date) from `index.time_series.end_time` so that data stream lifecycle and {{ilm-init}} treat the index age based on the data it contains, not when the index was created.

:::

Each new past backing index covers a configurable time interval.
Use the [`data_streams.past_tsdb_index_interval`](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#time-series-data-stream) cluster setting to control the interval.

When the gap between existing indices is up to 1.3 times the configured interval, {{es}} might create a single bridging index instead of many small indices.

For guidance on loading historical data, refer to [Load historical data into a TSDS](/manage-data/data-store/data-streams/load-historical-tsds.md).

## Dimension-based routing [dimension-based-routing]

In addition to time-based routing, time series data streams use dimension-based routing to determine which shard to route data to. Documents with the same dimensions are routed to the same shards, using one of two strategies:

**Index dimensions** {applies_to}`stack: ga 9.2` {applies_to}`serverless: all`
:    Routing based on the internally managed `index.dimensions` setting.

**Routing path**
:    Routing based on the [`index.routing_path`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-routing-path)  setting (as a fallback).

The `index.dimensions`-based strategy offers better ingest performance. It uses a list of dimension paths that is automatically updated (and is not user-configurable). This strategy is not available for time series data streams with dynamic templates that set `time_series_dimension: true`.

To disable routing based on `index.dimensions`, set [`index.index_dimensions_tsid_strategy_enabled`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-dimensions-tsid-strategy-enabled) to `false`,
or manually set the [`index.routing_path`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-routing-path) to the dimensions you want to use:

```console
"settings": {
  "index.mode": "time_series",
  "index.routing_path": ["host", "service"]
}
```

Documents with the same dimension values are routed to the same shard, improving compression and query performance for time series data.

The `index.routing_path` setting supports wildcards (for example, `dim.*`) and can dynamically match new fields.
