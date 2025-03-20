---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tsds.html
applies_to:
  stack: ga
  serverless: ga
---

# Time series data stream (TSDS) [tsds]

A time series data stream (TSDS) models timestamped metrics data as one or more time series.

You can use a TSDS to store metrics data more efficiently. In our benchmarks, metrics data stored in a TSDS used 70% less disk space than a regular data stream. The exact impact will vary per data set.


## When to use a TSDS [when-to-use-tsds]

Both a [regular data stream](../data-streams.md) and a TSDS can store timestamped metrics data. Only use a TSDS if you typically add metrics data to {{es}} in near real-time and `@timestamp` order.

A TSDS is only intended for metrics data. For other timestamped data, such as logs or traces, use a [logs data stream](logs-data-stream.md) or regular data stream.


## Differences from a regular data stream [differences-from-regular-data-stream]

A TSDS works like a regular data stream with some key differences:

* The matching index template for a TSDS requires a `data_stream` object with the [`index.mode: time_series`](#time-series-mode) option. This option enables most TSDS-related functionality.
* In addition to a `@timestamp`, each document in a TSDS must contain one or more [dimension fields](#time-series-dimension). The matching index template for a TSDS must contain mappings for at least one `keyword` dimension.

    TSDS documents also typically contain one or more [metric fields](#time-series-metric).

* {{es}} generates a hidden [`_tsid`](#tsid) metadata field for each document in a TSDS.
* A TSDS uses [time-bound backing indices](#time-bound-indices) to store data from the same time period in the same backing index.
* The matching index template for a TSDS must contain the `index.routing_path` index setting. A TSDS uses this setting to perform [dimension-based routing](#dimension-based-routing).
* A TSDS uses internal [index sorting](elasticsearch://reference/elasticsearch/index-settings/sorting.md) to order shard segments by `_tsid` and `@timestamp`.
* TSDS documents only support auto-generated document `_id` values. For TSDS documents, the document `_id` is a hash of the document’s dimensions and `@timestamp`. A TSDS doesn’t support custom document `_id` values.
* A TSDS uses [synthetic `_source`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#synthetic-source), and as a result is subject to some [restrictions](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#synthetic-source-restrictions) and [modifications](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#synthetic-source-modifications) applied to the `_source` field.

::::{note}
A time series index can contain fields other than dimensions or metrics.
::::



## What is a time series? [time-series]

A time series is a sequence of observations for a specific entity. Together, these observations let you track changes to the entity over time. For example, a time series can track:

* CPU and disk usage for a computer
* The price of a stock
* Temperature and humidity readings from a weather sensor.

:::{image} /manage-data/images/elasticsearch-reference-time-series-chart.svg
:alt: time series chart
:title: Time series of weather sensor readings plotted as a graph
:::

In a TSDS, each {{es}} document represents an observation, or data point, in a specific time series. Although a TSDS can contain multiple time series, a document can only belong to one time series. A time series can’t span multiple data streams.


### Dimensions [time-series-dimension]

Dimensions are field names and values that, in combination, identify a document’s time series. In most cases, a dimension describes some aspect of the entity you’re measuring. For example, documents related to the same weather sensor may always have the same `sensor_id` and `location` values.

A TSDS document is uniquely identified by its time series and timestamp, both of which are used to generate the document `_id`. So, two documents with the same dimensions and the same timestamp are considered to be duplicates. When you use the `_bulk` endpoint to add documents to a TSDS, a second document with the same timestamp and dimensions overwrites the first. When you use the `PUT /<target>/_create/<_id>` format to add an individual document and a document with the same `_id` already exists, an error is generated.

You mark a field as a dimension using the boolean `time_series_dimension` mapping parameter. The following field types support the `time_series_dimension` parameter:

* [`keyword`](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#keyword-field-type)
* [`ip`](elasticsearch://reference/elasticsearch/mapping-reference/ip.md)
* [`byte`](elasticsearch://reference/elasticsearch/mapping-reference/number.md)
* [`short`](elasticsearch://reference/elasticsearch/mapping-reference/number.md)
* [`integer`](elasticsearch://reference/elasticsearch/mapping-reference/number.md)
* [`long`](elasticsearch://reference/elasticsearch/mapping-reference/number.md)
* [`unsigned_long`](elasticsearch://reference/elasticsearch/mapping-reference/number.md)
* [`boolean`](elasticsearch://reference/elasticsearch/mapping-reference/boolean.md)

For a flattened field, use the `time_series_dimensions` parameter to configure an array of fields as dimensions. For details refer to [`flattened`](elasticsearch://reference/elasticsearch/mapping-reference/flattened.md#flattened-params).

Dimension definitions can be simplified through [pass-through](elasticsearch://reference/elasticsearch/mapping-reference/passthrough.md#passthrough-dimensions) fields.


### Metrics [time-series-metric]

Metrics are fields that contain numeric measurements, as well as aggregations and/or downsampling values based off of those measurements. While not required, documents in a TSDS typically contain one or more metric fields.

Metrics differ from dimensions in that while dimensions generally remain constant, metrics are expected to change over time, even if rarely or slowly.

To mark a field as a metric, you must specify a metric type using the `time_series_metric` mapping parameter. The following field types support the `time_series_metric` parameter:

* [`aggregate_metric_double`](elasticsearch://reference/elasticsearch/mapping-reference/aggregate-metric-double.md)
* [`histogram`](elasticsearch://reference/elasticsearch/mapping-reference/histogram.md)
* All [numeric field types](elasticsearch://reference/elasticsearch/mapping-reference/number.md)

Accepted metric types vary based on the field type:

:::::{dropdown} Valid values for `time_series_metric`
`counter`
:   A cumulative metric that only monotonically increases or resets to `0` (zero). For example, a count of errors or completed tasks.

    A counter field has additional semantic meaning, because it represents a cumulative counter. This works well with the `rate` aggregation, since a rate can be derived from a cumulative monotonically increasing counter. However a number of aggregations (for example `sum`) compute results that don’t make sense for a counter field, because of its cumulative nature.

    Only numeric and `aggregate_metric_double` fields support the `counter` metric type.


::::{note}
Due to the cumulative nature of counter fields, the following aggregations are supported and expected to provide meaningful results with the `counter` field: `rate`, `histogram`, `range`, `min`, `max`, `top_metrics` and `variable_width_histogram`. In order to prevent issues with existing integrations and custom dashboards, we also allow the following aggregations, even if the result might be meaningless on counters: `avg`, `box plot`, `cardinality`, `extended stats`, `median absolute deviation`, `percentile ranks`, `percentiles`, `stats`, `sum` and `value count`.
::::


`gauge`
:   A metric that represents a single numeric that can arbitrarily increase or decrease. For example, a temperature or available disk space.

    Only numeric and `aggregate_metric_double` fields support the `gauge` metric type.


`null` (Default)
:   Not a time series metric.

:::::



## Time series mode [time-series-mode]

The matching index template for a TSDS must contain a `data_stream` object with the `index_mode: time_series` option. This option ensures the TSDS creates backing indices with an [`index.mode`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-mode) setting of `time_series`. This setting enables most TSDS-related functionality in the backing indices.

If you convert an existing data stream to a TSDS, only backing indices created after the conversion have an `index.mode` of `time_series`. You can’t change the `index.mode` of an existing backing index.


### `_tsid` metadata field [tsid]

When you add a document to a TSDS, {{es}} automatically generates a `_tsid` metadata field for the document. The `_tsid` is an object containing the document’s dimensions. Documents in the same TSDS with the same `_tsid` are part of the same time series.

The `_tsid` field is not queryable or updatable. You also can’t retrieve a document’s `_tsid` using a [get document](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-get) request. However, you can use the `_tsid` field in aggregations and retrieve the `_tsid` value in searches using the [`fields` parameter](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md#search-fields-param).

::::{warning}
The format of the `_tsid` field shouldn’t be relied upon. It may change from version to version.
::::



### Time-bound indices [time-bound-indices]

In a TSDS, each backing index, including the most recent backing index, has a range of accepted `@timestamp` values. This range is defined by the [`index.time_series.start_time`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-start-time) and [`index.time_series.end_time`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time) index settings.

When you add a document to a TSDS, {{es}} adds the document to the appropriate backing index based on its `@timestamp` value. As a result, a TSDS can add documents to any TSDS backing index that can receive writes. This applies even if the index isn’t the most recent backing index.

:::{image} /manage-data/images/elasticsearch-reference-time-bound-indices.svg
:alt: time bound indices
:::

::::{tip}
Some {{ilm-init}} actions mark the source index as read-only, or expect the index to not be actively written anymore in order to provide good performance. These actions are: - [Delete](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-delete.md) - [Downsample](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-downsample.md) - [Force merge](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-forcemerge.md) - [Read only](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-readonly.md) - [Searchable snapshot](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md) - [Shrink](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-shrink.md) {{ilm-cap}} will **not** proceed with executing these actions until the upper time-bound for accepting writes, represented by the [`index.time_series.end_time`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time) index setting, has lapsed.
::::


If no backing index can accept a document’s `@timestamp` value, {{es}} rejects the document.

{{es}} automatically configures `index.time_series.start_time` and `index.time_series.end_time` settings as part of the index creation and rollover process.


### Look-ahead time [tsds-look-ahead-time]

Use the [`index.look_ahead_time`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-look-ahead-time) index setting to configure how far into the future you can add documents to an index. When you create a new write index for a TSDS, {{es}} calculates the index’s `index.time_series.end_time` value as:

`now + index.look_ahead_time`

At the time series poll interval (controlled via `time_series.poll_interval` setting), {{es}} checks if the write index has met the rollover criteria in its index lifecycle policy. If not, {{es}} refreshes the `now` value and updates the write index’s `index.time_series.end_time` to:

`now + index.look_ahead_time + time_series.poll_interval`

This process continues until the write index rolls over. When the index rolls over, {{es}} sets a final `index.time_series.end_time` value for the index. This value borders the `index.time_series.start_time` for the new write index. This ensures the `@timestamp` ranges for neighboring backing indices always border but never overlap.


### Look-back time [tsds-look-back-time]

Use the [`index.look_back_time`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-look-back-time) index setting to configure how far in the past you can add documents to an index. When you create a data stream for a TSDS, {{es}} calculates the index’s `index.time_series.start_time` value as:

`now - index.look_back_time`

This setting is only used when a data stream gets created and controls the `index.time_series.start_time` index setting of the first backing index. Configuring this index setting can be useful to accept documents with `@timestamp` field values that are older than 2 hours (the `index.look_back_time` default).


### Accepted time range for adding data [tsds-accepted-time-range]

A TSDS is designed to ingest current metrics data. When the TSDS is first created the initial backing index has:

* an `index.time_series.start_time` value set to `now - index.look_back_time`
* an `index.time_series.end_time` value set to `now + index.look_ahead_time`

Only data that falls inside that range can be indexed.

You can use the [get data stream API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-data-stream) to check the accepted time range for writing to any TSDS.


### Dimension-based routing [dimension-based-routing]

Within each TSDS backing index, {{es}} uses the [`index.routing_path`](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-routing-path) index setting to route documents with the same dimensions to the same shards.

When you create the matching index template for a TSDS, you must specify one or more dimensions in the `index.routing_path` setting. Each document in a TSDS must contain one or more dimensions that match the `index.routing_path` setting.

The `index.routing_path` setting accepts wildcard patterns (for example `dim.*`) and can dynamically match new fields. However, {{es}} will reject any mapping updates that add scripted, runtime, or non-dimension fields that match the `index.routing_path` value.

[Pass-through](elasticsearch://reference/elasticsearch/mapping-reference/passthrough.md#passthrough-dimensions) fields may be configured as dimension containers. In this case, their sub-fields get included to the routing path automatically.

TSDS documents don’t support a custom `_routing` value. Similarly, you can’t require a `_routing` value in mappings for a TSDS.


### Index sorting [tsds-index-sorting]

{{es}} uses [compression algorithms](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-codec) to compress repeated values. This compression works best when repeated values are stored near each other — in the same index, on the same shard, and side-by-side in the same shard segment.

Most time series data contains repeated values. Dimensions are repeated across documents in the same time series. The metric values of a time series may also change slowly over time.

Internally, each TSDS backing index uses [index sorting](elasticsearch://reference/elasticsearch/index-settings/sorting.md) to order its shard segments by `_tsid` and `@timestamp`. This makes it more likely that these repeated values are stored near each other for better compression. A TSDS doesn’t support any [`index.sort.*`](elasticsearch://reference/elasticsearch/index-settings/sorting.md) index settings.


## What’s next? [tsds-whats-next]

Now that you know the basics, you’re ready to [create a TSDS](../data-streams/time-series-data-stream-tsds.md) or [convert an existing data stream to a TSDS](../data-streams/time-series-data-stream-tsds.md).
