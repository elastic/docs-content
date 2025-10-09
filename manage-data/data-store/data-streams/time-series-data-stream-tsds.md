---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tsds.html
navigation_title: "Time series data streams"
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Time series data streams [tsds]

A time series data stream (TSDS) is a type of [data stream](/manage-data/data-store/data-streams.md) optimized for indexing metrics data. A TSDS helps you analyze a sequence of data points as a whole.

A TSDS can also help you store metrics data more efficiently. In our benchmarks, metrics data stored in a TSDS used 70% less disk space than a regular data stream. The exact impact varies by data set.

Before setting up a time series data stream, make sure you're familiar with general [data stream](/manage-data/data-store/data-streams.md) concepts.

## When to use a time series data stream [when-to-use-tsds]

_Metrics_ consist of data point&ndash;timestamp pairs, identified by [dimension fields](#time-series-dimension), that can be used in aggregation queries. Both a regular data stream and a time series data stream can store metrics data. 

Choose a time series data stream if you typically add metrics data to {{es}} in near real-time and in `@timestamp` order. For other timestamped data, such as logs or traces, use a [logs data stream](logs-data-stream.md) or a [regular data stream](/manage-data/data-store/data-streams.md).

To make sure a TSDS is right for your use case, review the list of [differences from a regular data stream](#differences-from-regular-data-stream) on this page.

## Time series overview [time-series]

A time series is a sequence of observations for a specific entity. Together, these observations let you track changes to the entity over time. For example, a time series can track:

- CPU and disk usage for a computer
- The price of a stock
- Temperature and humidity readings from a weather sensor

:::{image} /manage-data/images/elasticsearch-reference-time-series-chart2.svg
:alt: time series chart
:title: Time series of weather sensor readings plotted as a graph
:::

### Time series fields

Compared to a regular data stream, a TSDS uses some additional fields specific to time series:  dimension fields and metric fields, plus an internal `_tsid` metadata field.

#### Dimensions [time-series-dimension]

Dimension fields often correspond to characteristics of the items you're measuring. For example, documents related to the same weather sensor might have the same `sensor_id` and `location` values.

:::{tip}
{{es}} uses dimensions and timestamps to generate time series document `_id` values. Two documents with the same dimensions and timestamp are considered duplicates.
::: 

To mark a field as a dimension, set the Boolean `time_series_dimension` mapping parameter to `true`. The following field types support the `time_series_dimension` parameter:

* [`keyword`](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#keyword-field-type)
* [`ip`](elasticsearch://reference/elasticsearch/mapping-reference/ip.md)
* [`byte`](elasticsearch://reference/elasticsearch/mapping-reference/number.md)
* [`short`](elasticsearch://reference/elasticsearch/mapping-reference/number.md)
* [`integer`](elasticsearch://reference/elasticsearch/mapping-reference/number.md)
* [`long`](elasticsearch://reference/elasticsearch/mapping-reference/number.md)
* [`unsigned_long`](elasticsearch://reference/elasticsearch/mapping-reference/number.md)
* [`boolean`](elasticsearch://reference/elasticsearch/mapping-reference/boolean.md)

To work with a flattened field, use the `time_series_dimensions` parameter to configure an array of fields as dimensions. For details, refer to [`flattened`](elasticsearch://reference/elasticsearch/mapping-reference/flattened.md#flattened-params).

You can also simplify dimension definitions by using [pass-through](elasticsearch://reference/elasticsearch/mapping-reference/passthrough.md#passthrough-dimensions) fields.

#### Metrics [time-series-metric]

Metrics are numeric measurements that change over time. Documents in a TSDS typically contain one or more metric fields. 

To mark a field as a metric, use the `time_series_metric` mapping parameter. This parameter ensures data is stored in an optimal way for time series analysis. The following field types support the `time_series_metric` parameter:

* All [numeric field types](elasticsearch://reference/elasticsearch/mapping-reference/number.md)
* [`aggregate_metric_double`](elasticsearch://reference/elasticsearch/mapping-reference/aggregate-metric-double.md), for internal use during downsampling (rarely user-populated)

The valid values for `time_series_metric` are `counter` and `gauge`:

`counter`
:   A cumulative metric that only monotonically increases or resets to `0` (zero). For example, a count of errors or completed tasks that resets when a serving process restarts. 

`gauge`
:   A metric that represents a single numeric that can arbitrarily increase or decrease. For example, a temperature or available disk space. 

#### `_tsid` metadata field [tsid]

The `_tsid` is an automatically generated object derived from the document’s dimensions. It's intended for internal {{es}} use, so in most cases you won't need to work with it. The format of the `_tsid` field is subject to change. 

### Differences from a regular data stream [differences-from-regular-data-stream]

A time series data stream works like a regular data stream, with some key differences:

* **Time series index mode:** The matching index template for a TSDS must include a `data_stream` object with `index.mode` set to `time_series`. This option enables most TSDS-related functionality.
* **Fields:** In a TSDS, each document contains:
  * A `@timestamp` field
  * One or more [dimension fields](#time-series-dimension), set with `time_series_dimension: true`  
  * One or more [metric fields](#time-series-metric)
  * An auto-generated document `_id` (custom `_id` values are not supported)
* **Backing indices:** A TSDS uses [time-bound indices](/manage-data/data-store/data-streams/time-bound-tsds.md) to store data from the same time period in the same backing index.
* **Dimension-based routing:** The routing logic uses dimension fields to map data to shards, improving storage efficiency and query performance.
* **Sorting:** A TSDS uses internal [index sorting](elasticsearch://reference/elasticsearch/index-settings/sorting.md) to order shard segments by `_tsid` and `@timestamp`, for better compression. Time series data streams do not use `index.sort.*` settings.

## Query time series data
```{applies_to}
stack: preview
serverless: preview
```

You can use the {{esql}} [`TS` command](elasticsearch://reference/query-languages/esql/commands/ts.md) (in technical preview) to query time series data streams. The `TS` command is optimized for time series data. It also enables the use of aggregation functions that efficiently process metrics per time series, before aggregating results.


## Next steps [tsds-whats-next]

* Try the [quickstart](/manage-data/data-store/data-streams/quickstart-tsds.md) for a hands-on introduction
* [Set up a time series data stream](/manage-data/data-store/data-streams/set-up-tsds.md)
* [Ingest data using the OpenTelemetry Protocol (OTLP)](/manage-data/data-store/data-streams/tsds-ingest-otlp.md)
* Learn about [downsampling](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) to reduce storage footprint

% suppress anchor warnings until chicken-and-egg resolved
##### [time-series-mode]
##### [tsds-look-ahead-time]
##### [tsds-look-back-time]
##### [time-bound-indices]
##### [dimension-based-routing]
##### [tsds-accepted-time-range]
