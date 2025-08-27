---
navigation_title: "Concepts"
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Downsampling concepts [how-downsampling-works]

:::{admonition} Page status
🟢 Ready for review
:::

A [time series](time-series-data-stream-tsds.md#time-series) is a sequence of observations taken over time for a specific entity. The observed samples can be represented as a continuous function, where the time series dimensions remain constant and the time series metrics change over time.

:::{image} /manage-data/images/elasticsearch-reference-time-series-function.png
:alt: time series function
:::

In an {{es}} index, a single document is created for each timestamp. The document contains the immutable time series dimensions, plus metric names and values. Several time series dimensions and metrics can be stored for a single timestamp.

:::{image} /manage-data/images/elasticsearch-reference-time-series-metric-anatomy.png
:alt: time series metric anatomy
:::

For the most current data, the metrics series typically has a low sampling time interval, to optimize for queries that require a high data resolution.

:::{image} /manage-data/images/elasticsearch-reference-time-series-original.png
:alt: time series original
:title: Original metrics series
:::

Downsampling reduces the footprint of older, less frequently accessed data by replacing the original time series with a data stream of a higher sampling interval, plus statistical representations of the data. For example, if the original metrics samples were taken every 10 seconds, you might choose to reduce the sample granularity to hourly as the data ages. Or you might choose to reduce the granularity of `cold` archival data to monthly or less.

:::{image} /manage-data/images/elasticsearch-reference-time-series-downsampled.png
:alt: time series downsampled
:title: Downsampled metrics series
:::


## How downsampling works [downsample-api-process]

The downsampling operation traverses the source TSDS index and performs the following steps:

1. Creates a new document for each value of the `_tsid` field and each `@timestamp` value, rounded to the `fixed_interval` defined in the downsampling configuration.
2. For each new document, copies all [time series dimensions](time-series-data-stream-tsds.md#time-series-dimension) from the source index to the target index. Dimensions in a TSDS are constant, so this step happens only once per bucket.
3. For each [time series metric](time-series-data-stream-tsds.md#time-series-metric) field, computes aggregations for all documents in the bucket.

    * `gauge` field type:
        * `min`, `max`, `sum`, and `value_count` are stored 
        * `value_count` is stored as type `aggregate_metric_double`
    * `counter` field type:
        * `last_value` is stored.

4. For all other fields, copies the most recent value to the target index.
5. Deletes the original index and replaces it with the downsampled index. Within a data stream, only one index can exist for a time period.

The new, downsampled index is created on the data tier of the original index and inherits the original settings, like number of shards and replicas.

:::{tip}
You can downsample a downsampled index. The subsequent downsampling interval must be a multiple of the interval used in the preceding downsampling operation.
:::

% TODO ^^ consider mini table in step 3; refactor generally

### Source and target index field mappings [downsample-api-mappings]

Fields in the target downsampled index are created based on fields in the original source index, as follows:

1. **Dimensions:** Fields mapped with the `time-series-dimension` parameter are created in the target downsampled index with the same mapping as in the source index.
2. **Metrics:** Fields mapped with the `time_series_metric` parameter are created in the target downsampled index with the same mapping as in the source index, with one exception: `time_series_metric: gauge` fields are changed to `aggregate_metric_double`.
3. **Labels:** Label fields (fields that are neither dimensions nor metrics) are created in the target downsampled index with the same mapping as in the source index.

% TODO ^^ make this more concise / a table?

## Querying downsampled indices [querying-downsampled-indices]

To query a downsampled index, use the [`_search`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) and [`_async_search`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit) endpoints. 

* You can query multiple raw data and downsampled indices in a single request, and a single request can include downsampled indices with multiple downsampling intervals (for example, `15m`, `1h`, `1d`).
* When you run queries in {{kib}} and through Elastic solutions, a standard response is returned, with no indication that some of the queried indices are downsampled.
* [Date histogram aggregations](elasticsearch://reference/aggregations/search-aggregations-bucket-datehistogram-aggregation.md) support `fixed_intervals` only (not calendar-aware intervals).
* Time-based histogram aggregations use a uniform bucket size, without regard to the downsampling time interval specified in the request.

### Time zone offsets

Date histograms are based on UTC values. Some time zone situations require offsetting (shifting the time buckets) when downsampling:
     
* For time zone `+5:30` (India), offset by 30 minutes -- for example, `2020-01-01T10:30:00.000` instead of `2020-03-07T10:00:00.000`. Or use a downsampling interval of 15 minutes instead of offsetting.
* For intervals based on days rather than hours, adjust the buckets to the appropriate time zone -- for example, `2020-03-07T19:00:00.000` instead of `2020-03-07T00:00:00.000` for `America/New_York`. 

When offsetting is applied, responses include the field `downsampled_results_offset: true`.

For more details, refer to [Date histogram aggregation: Time zone](elasticsearch://reference/aggregations/search-aggregations-bucket-datehistogram-aggregation.md#datehistogram-aggregation-time-zone).



