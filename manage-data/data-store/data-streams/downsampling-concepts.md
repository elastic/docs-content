---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Downsampling concepts [how-downsampling-works]

:::{warning}
🚧 Work in progress 🚧
:::

A [time series](time-series-data-stream-tsds.md#time-series) is a sequence of observations taken over time for a specific entity. The observed samples can be represented as a continuous function, where the time series dimensions remain constant and the time series metrics change over time.

:::{image} /manage-data/images/elasticsearch-reference-time-series-function.png
:alt: time series function
:::

In an Elasticsearch index, a single document is created for each timestamp. The document contains the immutable time series dimensions, together with metric names and values. Several time series dimensions and metrics can be stored for a single timestamp.

:::{image} /manage-data/images/elasticsearch-reference-time-series-metric-anatomy.png
:alt: time series metric anatomy
:::

For your most current and relevant data, the metrics series typically has a low sampling time interval, so it's optimized for queries that require a high data resolution.

:::{image} /manage-data/images/elasticsearch-reference-time-series-original.png
:alt: time series original
:title: Original metrics series
:::

Downsampling reduces the footprint of older, less frequently accessed data by replacing the original time series with a data stream of a higher sampling interval, plus statistical representations of the data. For example, if the original metrics samples were taken every 10 seconds, as the data ages you might choose to reduce the sample granularity to hourly or daily. Or you might choose to reduce the granularity of `cold` archival data to monthly or less.

:::{image} /manage-data/images/elasticsearch-reference-time-series-downsampled.png
:alt: time series downsampled
:title: Downsampled metrics series
:::


### The downsampling process [downsample-api-process]

The downsampling operation traverses the source TSDS index and performs the following steps:

1. Creates a new document for each value of the `_tsid` field and each `@timestamp` value, rounded to the `fixed_interval` defined in the downsampling configuration.
2. For each new document, copies all [time series dimensions](time-series-data-stream-tsds.md#time-series-dimension) from the source index to the target index. Dimensions in a TSDS are constant, so this step happens only once per bucket.
3. For each [time series metric](time-series-data-stream-tsds.md#time-series-metric) field, computes aggregations for all documents in the bucket. The set of pre-aggregated results differs by metric field type:

    * `gauge` field type:
        * `min`, `max`, `sum`, and `value_count` are stored 
        * `value_count` is stored as type `aggregate_metric_double`
    * `counter field type:
        * `last_value` is stored.

4. For all other fields, the most recent value is copied to the target index.

% TODO ^^ consider mini table in step 3; refactor generally

### Source and target index field mappings [downsample-api-mappings]

Fields in the target downsampled index are created based on fields in the original source index, as follows:

1. **Dimensions:** Fields mapped with the `time-series-dimension` parameter are created in the target downsampled index with the same mapping as in the source index.
2. **Metrics:** Fields mapped with the `time_series_metric` parameter are created in the target downsampled index with the same mapping as in the source index, with one exception: `time_series_metric: gauge` fields are changed to `aggregate_metric_double`.
3. **Labels:** Label fields (fields that are neither dimensions nor metrics) are created in the target downsampled index with the same mapping as in the source index.

% TODO ^^ make this more concise

% first pass edits up to here
% TODO resume editing from this line down

## Querying downsampled indices [querying-downsampled-indices]

You can use the [`_search`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) and [`_async_search`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit) endpoints to query a downsampled index. Multiple raw data and downsampled indices can be queried in a single request, and a single request can include downsampled indices at different granularities (different bucket timespan). That is, you can query data streams that contain downsampled indices with multiple downsampling intervals (for example, `15m`, `1h`, `1d`).

The result of a time based histogram aggregation is in a uniform bucket size and each downsampled index returns data ignoring the downsampling time interval. For example, if you run a `date_histogram` aggregation with `"fixed_interval": "1m"` on a downsampled index that has been downsampled at an hourly resolution (`"fixed_interval": "1h"`), the query returns one bucket with all of the data at minute 0, then 59 empty buckets, and then a bucket with data again for the next hour.


### Notes on downsample queries [querying-downsampled-indices-notes]

There are a few things to note about querying downsampled indices:

* When you run queries in {{kib}} and through Elastic solutions, a normal response is returned without notification that some of the queried indices are downsampled.
* For [date histogram aggregations](elasticsearch://reference/aggregations/search-aggregations-bucket-datehistogram-aggregation.md), only `fixed_intervals` (and not calendar-aware intervals) are supported.
* Timezone support comes with caveats:

    * Date histograms at intervals that are multiples of an hour are based on values generated at UTC. This works well for timezones that are on the hour, e.g. +5:00 or -3:00, but requires offsetting the reported time buckets, e.g. `2020-01-01T10:30:00.000` instead of `2020-03-07T10:00:00.000` for timezone +5:30 (India), if downsampling aggregates values per hour. In this case, the results include the field `downsampled_results_offset: true`, to indicate that the time buckets are shifted. This can be avoided if a downsampling interval of 15 minutes is used, as it allows properly calculating hourly values for the shifted buckets.
    * Date histograms at intervals that are multiples of a day are similarly affected, in case downsampling aggregates values per day. In this case, the beginning of each day is always calculated at UTC when generated the downsampled values, so the time buckets need to be shifted, e.g. reported as `2020-03-07T19:00:00.000` instead of `2020-03-07T00:00:00.000` for timezone `America/New_York`. The field `downsampled_results_offset: true` is added in this case too.
    * Daylight savings and similar peculiarities around timezones affect reported results, as [documented](elasticsearch://reference/aggregations/search-aggregations-bucket-datehistogram-aggregation.md#datehistogram-aggregation-time-zone) for date histogram aggregation. Besides, downsampling at daily interval hinders tracking any information related to daylight savings changes.



## Restrictions and limitations [downsampling-restrictions]

The following restrictions and limitations apply for downsampling:

* Only indices in a [time series data stream](time-series-data-stream-tsds.md) are supported.
* Data is downsampled based on the time dimension only. All other dimensions are copied to the new index without any modification.
* Within a data stream, a downsampled index replaces the original index and the original index is deleted. Only one index can exist for a given time period.
* A source index must be in read-only mode for the downsampling process to succeed. Check the [Run downsampling manually](./run-downsampling-manually.md) example for details.
* Downsampling data for the same period many times (downsampling of a downsampled index) is supported. The downsampling interval must be a multiple of the interval of the downsampled index.
* Downsampling is provided as an ILM action. See [Downsample](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-downsample.md).
* The new, downsampled index is created on the data tier of the original index and it inherits its settings (for example, the number of shards and replicas).
* The numeric `gauge` and `counter` [metric types](elasticsearch://reference/elasticsearch/mapping-reference/mapping-field-meta.md) are supported.
* The downsampling configuration is extracted from the time series data stream [index mapping](./set-up-tsds.md#create-tsds-index-template). The only additional required setting is the downsampling `fixed_interval`.


