---
navigation_title: "Time-bound indices"
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Time-bound indices and dimension-based routing [time-bound-indices]

Unlike regular data streams that only write to the most recent backing index, time series data streams (TSDS) use time-bound backing indices that accept documents based on their timestamp values. This page provides details and best practices to help you work with time-bound indices.

## How time-bound indices work

Each TSDS backing index has a time range for accepted `@timestamp` values, defined by two settings:

- [`index.time_series.start_time`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-start-time): The earliest accepted timestamp (inclusive)
- [`index.time_series.end_time`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time): The latest accepted timestamp (exclusive)

When you add a document to a TSDS, {{es}} adds the document to the appropriate backing index based on its `@timestamp` value. This means a TSDS can write to multiple backing indices simultaneously, not just the most recent one.

:::{image} /manage-data/images/elasticsearch-reference-time-bound-indices.svg
:alt: time bound indices
:::

If no backing index can accept a document's `@timestamp` value, {{es}} rejects the document by default. {applies_to}`stack: ga 9.5` {applies_to}`serverless: ga` When you enable past backing index creation, {{es}} can create missing past indices for timestamps inside the [eligible write window](#tsds-eligible-write-window) before indexing the document. For details, refer to [Backfill past timestamps](#tsds-backfill-past-timestamps).

{{es}} automatically configures `index.time_series.start_time` and `index.time_series.end_time` settings as part of the index creation and rollover process.

### Accepted time range for adding data [tsds-accepted-time-range]

A TSDS is designed to ingest current metrics data. When the TSDS is first created, the initial backing index has the following settings:

- An `index.time_series.start_time` value set to `now - index.look_back_time`
- An `index.time_series.end_time` value set to `now + index.look_ahead_time`

Only data that falls within this range is indexed into the backing index that covers that timestamp.

The accepted time range describes the writable window for **each** backing index. It is separate from the [eligible write window](#tsds-eligible-write-window), which limits how far back you can write to the data stream as a whole.

To check the accepted time range for writing to a TSDS, use the [get data stream API]({{es-apis}}operation/operation-indices-get-data-stream):

```console
GET _data_stream/my-tsds
```

::::{tip}
Writes might still be rejected even when a timestamp fits the accepted time range of a backing index, or when past-index creation is enabled but no backing index exists yet for that timestamp. Common causes include:

- No backing index covers the document's `@timestamp` value and past-index creation is disabled (the default).
- A lifecycle action has made the target backing index read-only or removed it. Examples include:
  - [Delete](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-delete.md)
  - [Downsample](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-downsample.md)
  - [Force merge](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-forcemerge.md)
  - [Read only](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-readonly.md)
  - [Searchable snapshot](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md)
  - [Shrink](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-shrink.md), which might then revert the read-only status at the end of the action
- The timestamp falls outside the [eligible write window](#tsds-eligible-write-window).

{{ilm-cap}} will **not** proceed with executing these actions until [`index.time_series.end_time`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time) has passed.
::::

### Eligible write window [tsds-eligible-write-window]

```{applies_to}
stack: ga 9.5
serverless: ga
```

The eligible write window is the range of past timestamps that a TSDS accepts for writes. It extends from the present back to the first lifecycle action that makes a backing index read-only, or to the configured retention limit, whichever comes first. If neither is configured, the window extends back indefinitely.

Lifecycle actions that make backing indices read-only include [downsampling](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) and {{search-snap}} transitions. Documents for time periods that are already read-only are still rejected, because {{es}} cannot write to summarized or snapshotted indices.

The eligible write window is relative to the current time. As time passes, the window moves forward with it.

This window is distinct from the per-index accepted time range defined by `index.look_back_time` and `index.look_ahead_time`. The eligible write window governs whether a timestamp is allowed at all; the accepted time range governs which backing index receives the document.

### Backfill past timestamps [tsds-backfill-past-timestamps]

```{applies_to}
stack: ga 9.5
serverless: ga
```

When past backing index creation is enabled, {{es}} can create missing past backing indices on demand during indexing. This lets you load historical metrics into an existing TSDS without manually creating backing indices.

Past-index creation applies only when all of the following are true:

- The TSDS already exists and has at least one time series backing index.
- The document's `@timestamp` is not covered by any existing backing index.
- The timestamp is inside the [eligible write window](#tsds-eligible-write-window).
- The cluster setting [`data_stream.past_tsdb_index_creation_enabled`](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#time-series-data-stream) is enabled.

Timestamps outside the eligible write window or in the future are still rejected. If a [failure store](/manage-data/data-store/data-streams/failure-store.md) is enabled, rejected timestamp failures can be redirected there.

#### Enable past-index creation

Past-index creation is disabled by default. Enable it at the cluster level:

```console
PUT _cluster/settings
{
  "persistent": {
    "data_stream.past_tsdb_index_creation_enabled": true
  }
}
```

#### Configure past index intervals [configure-past-index-intervals]

Each new past backing index covers a configurable time interval. Use the [`data_streams.past_tsdb_index_interval`](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#time-series-data-stream) cluster setting to control the interval. The default is `1d`, with a minimum of `1h` and a maximum of `7d`.

When the gap between existing indices is up to 1.3 times the configured interval, {{es}} may create a single bridging index instead of many small indices.

#### Lifecycle age for past indices

Past backing indices hold old data but are new indices. {{es}} sets [`index.lifecycle.origination_date`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-data-stream-lifecycle-origination-date) from `index.time_series.end_time` so that [data stream lifecycle](/manage-data/lifecycle/data-stream.md) and {{ilm-init}} treat the index age based on the data it contains, not when the index was created.

#### Security

Users who write documents that trigger past-index creation need the `auto_configure` index privilege on the data stream, in addition to privileges that allow indexing. Users with only the `index` privilege receive a `security_exception` when a write would create a past backing index.

#### After disabling the feature

If you disable past-index creation after past backing indices were created, writes to those existing past indices still succeed. Only the automatic creation of new past indices is disabled.

For step-by-step guidance on loading historical data, refer to [Load historical metrics into a TSDS](/manage-data/data-store/data-streams/load-historical-tsds.md).

### Dimension-based routing [dimension-based-routing]

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
