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

If no backing index can accept a document's `@timestamp` value, {{es}} rejects the document.

{{es}} automatically configures `index.time_series.start_time` and `index.time_series.end_time` settings as part of the index creation and rollover process.

### Accepted time range for adding data [tsds-accepted-time-range]

A TSDS is designed to ingest current metrics data. When the TSDS is first created, the initial backing index has the following settings:

- An `index.time_series.start_time` value set to `now - index.look_back_time`
- An `index.time_series.end_time` value set to `now + index.look_ahead_time`

Only data that falls within this range is indexed.

To check the accepted time range for writing to a TSDS, use the [get data stream API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-data-stream):

```console
GET _data_stream/my-tsds
```

::::{tip}
These {{ilm-init}} actions mark the source index as read-only or prevent writes for performance reasons:
 - [Delete](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-delete.md) 
 - [Downsample](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-downsample.md) 
 - [Force merge](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-forcemerge.md) 
 - [Read only](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-readonly.md)
 - [Searchable snapshot](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md) 
 - [Shrink](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-shrink.md) 
 
 {{ilm-cap}} will **not** proceed with executing these actions until [`index.time_series.end_time`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time) has passed.
::::


### Dimension-based routing [dimension-based-routing]

In addition to time-based routing, time series data streams use dimension-based routing to determine which shard to route data to. Documents with the same dimensions are routed to the same shards.

The [`index.routing_path`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-routing-path) setting specifies the dimension fields to use for routing, for example:

```console
"settings": {
  "index.mode": "time_series",
  "index.routing_path": ["host", "service"]
}
```

Documents with the same dimension values are routed to the same shard, improving compression and query performance for time series data.

The `index.routing_path` setting supports wildcards (for example, `dim.*`) and can dynamically match new fields.


