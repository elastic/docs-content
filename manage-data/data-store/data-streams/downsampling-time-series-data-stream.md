---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/downsampling.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Downsampling a time series data stream [downsampling]

Downsampling provides a method to reduce the footprint of your [time series data](time-series-data-stream-tsds.md) by storing it at reduced granularity.

Metrics solutions collect large amounts of time series data that grow over time. As that data ages, it becomes less relevant to the current state of the system. The downsampling process rolls up documents within a fixed time interval into a single summary document. Each summary document includes statistical representations of the original data: the `min`, `max`, `sum` and `value_count` for each metric. Data stream [time series dimensions](time-series-data-stream-tsds.md#time-series-dimension) are stored unchanged.

Downsampling, in effect, lets you to trade data resolution and precision for storage size. You can include it in an [{{ilm}} ({{ilm-init}})](../../lifecycle/index-lifecycle-management.md) policy to automatically manage the volume and associated cost of your metrics data at it ages.

Check the following sections to learn more:

* [How it works](#how-downsampling-works)
* [Running downsampling on time series data](#running-downsampling)
* [Querying downsampled indices](#querying-downsampled-indices)
* [Restrictions and limitations](#downsampling-restrictions)
* [Try it out](#try-out-downsampling)


## How it works [how-downsampling-works]

A [time series](time-series-data-stream-tsds.md#time-series) is a sequence of observations taken over time for a specific entity. The observed samples can be represented as a continuous function, where the time series dimensions remain constant and the time series metrics change over time.

:::{image} /manage-data/images/elasticsearch-reference-time-series-function.png
:alt: time series function
:::

In an Elasticsearch index, a single document is created for each timestamp, containing the immutable time series dimensions, together with the metrics names and the changing metrics values. For a single timestamp, several time series dimensions and metrics may be stored.

:::{image} /manage-data/images/elasticsearch-reference-time-series-metric-anatomy.png
:alt: time series metric anatomy
:::

For your most current and relevant data, the metrics series typically has a low sampling time interval, so it’s optimized for queries that require a high data resolution.

:::{image} /manage-data/images/elasticsearch-reference-time-series-original.png
:alt: time series original
:title: Original metrics series
:::

Downsampling works on older, less frequently accessed data by replacing the original time series with both a data stream of a higher sampling interval and statistical representations of that data. Where the original metrics samples may have been taken, for example, every ten seconds, as the data ages you may choose to reduce the sample granularity to hourly or daily. You may choose to reduce the granularity of `cold` archival data to monthly or less.

:::{image} /manage-data/images/elasticsearch-reference-time-series-downsampled.png
:alt: time series downsampled
:title: Downsampled metrics series
:::


### The downsampling process [downsample-api-process]

The downsampling operation traverses the source TSDS index and performs the following steps:

1. Creates a new document for each value of the `_tsid` field and each `@timestamp` value, rounded to the `fixed_interval` defined in the downsample configuration.
2. For each new document, copies all [time series dimensions](time-series-data-stream-tsds.md#time-series-dimension) from the source index to the target index. Dimensions in a TSDS are constant, so this is done only once per bucket.
3. For each [time series metric](time-series-data-stream-tsds.md#time-series-metric) field, computes aggregations for all documents in the bucket. Depending on the metric type of each metric field a different set of pre-aggregated results is stored:

    * `gauge`: The `min`, `max`, `sum`, and `value_count` are stored; `value_count` is stored as type `aggregate_metric_double`.
    * `counter`: The `last_value` is stored.

4. For all other fields, the most recent value is copied to the target index.


### Source and target index field mappings [downsample-api-mappings]

Fields in the target, downsampled index are created based on fields in the original source index, as follows:

1. All fields mapped with the `time-series-dimension` parameter are created in the target downsample index with the same mapping as in the source index.
2. All fields mapped with the `time_series_metric` parameter are created in the target downsample index with the same mapping as in the source index. An exception is that for fields mapped as `time_series_metric: gauge` the field type is changed to `aggregate_metric_double`.
3. All other fields that are neither dimensions nor metrics (that is, label fields), are created in the target downsample index with the same mapping that they had in the source index.


## Running downsampling on time series data [running-downsampling]

To downsample a time series index, use the [Downsample API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-downsample) and set `fixed_interval` to the level of granularity that you’d like:

```console
POST /my-time-series-index/_downsample/my-downsampled-time-series-index
{
    "fixed_interval": "1d"
}
```

To downsample time series data as part of ILM, include a [Downsample action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-downsample.md) in your ILM policy and set `fixed_interval` to the level of granularity that you’d like:

```console
PUT _ilm/policy/my_policy
{
  "policy": {
    "phases": {
      "warm": {
        "actions": {
          "downsample" : {
            "fixed_interval": "1h"
          }
        }
      }
    }
  }
}
```


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


## Try it out [try-out-downsampling]

To take downsampling for a test run, try our example of [running downsampling manually](./run-downsampling-manually.md).

Downsampling can easily be added to your ILM policy. To learn how, try our [Run downsampling with ILM](./run-downsampling-with-ilm.md) example.

