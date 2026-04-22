---
navigation_title: "Concepts"
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Downsampling concepts [how-downsampling-works]

This page explains core downsampling concepts. 

:::{important}
Downsampling works with [time series data streams](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) only.
:::

A [time series](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md#time-series) is a sequence of observations taken over time for a specific entity. The observed samples can be represented as a continuous function, where the time series dimensions remain constant and the time series metrics change over time.

:::{image} /manage-data/images/elasticsearch-reference-time-series-function.png
:alt: time series function
:::

In a time series data stream, a single document is created for each timestamp. The document contains the immutable time series dimensions, plus metric names and values. Several time series dimensions and metrics can be stored for a single timestamp.

:::{image} /manage-data/images/elasticsearch-reference-time-series-metric-anatomy.png
:alt: time series metric anatomy
:::

For the most current data, the metrics series typically has a low sampling time interval to optimize for queries that require a high data resolution.

:::{image} /manage-data/images/elasticsearch-reference-time-series-original.png
:alt: time series original
:title: Original metrics series
:::

_Downsampling_ reduces the footprint of older, less frequently accessed data by replacing the original time series with a data stream of a higher sampling interval, plus statistical representations of the data. For example, if the original metrics samples were taken every 10 seconds, you might choose to reduce the sample granularity to hourly as the data ages. Or you might choose to reduce the granularity of `cold` archival data to monthly or less.

:::{image} /manage-data/images/elasticsearch-reference-time-series-downsampled.png
:alt: time series downsampled
:title: Downsampled metrics series
:::


## How downsampling works [downsample-api-process]

Downsampling is applied to the individual backing indices of the TSDS. The downsampling operation traverses the source time series index and performs the following steps:

1. Creates a new document for each group of documents with  matching `_tsid` values (time series dimension fields), grouped into buckets that correspond to timestamps in a specific interval.

    For example, a TSDS index that contains metrics sampled every 10 seconds can be downsampled to an hourly index. All documents within a given hour interval are summarized and stored as a single document in the downsampled index.

2. For each new document, copies all [time series dimensions](time-series-data-stream-tsds.md#time-series-dimension) from the source index to the target index. Dimensions in a TSDS are constant, so this step happens only once per bucket.
3. For each [time series metric](time-series-data-stream-tsds.md#time-series-metric) field, it computes the downsampled values based on the [downsampling method](#downsampling-methods).
4. For all other fields, copies the most recent value to the target index.
5. Replaces the original index with the downsampled index, then deletes the original index.

The new, downsampled index is created on the data tier of the original index and inherits the original settings, like number of shards and replicas.

:::{tip}
You can downsample a downsampled index. The subsequent downsampling interval must be a multiple of the interval used in the preceding downsampling operation.
:::

% TODO ^^ consider mini table in step 3; refactor generally

### Downsampling methods [downsampling-methods]

Downsampling supports two methods for reducing multiple values in the same bucket to a single representative result:

* `last_value`: {applies_to}`stack: preview 9.3` {applies_to}`serverless: ga`
  Stores only the most recent value for each metric in the bucket. This method reduces the storage footprint the most, but it also reduces data accuracy. It applies to all metric types.

* `aggregate`
  Stores statistical summaries for the values in each bucket. This method preserves more information than `last_value`, but it requires more storage. It applies to each metric type as follows:
  * `gauge` fields:
    * Stores `min`, `max`, `sum`, and `value_count` as `aggregate_metric_double`.
  * `counter` fields:
    * Stores the first value, and stores up to two data points if a counter reset is detected {applies_to}`stack: ga 9.4` {applies_to}`serverless: ga`. The field type is preserved.
    * In previous versions, only the last value is stored.
  * `histogram` fields {applies_to}`stack: preview 9.3` {applies_to}`serverless: preview`
    * Merges individual histograms into a single histogram, preserving the field type. Both the [`histogram`](elasticsearch://reference/elasticsearch/mapping-reference/histogram.md) and the
    [`exponential_histogram`](elasticsearch://reference/elasticsearch/mapping-reference/exponential-histogram.md)) are supported; the `histogram` field type uses the [T-Digest](elasticsearch://reference/aggregations/search-aggregations-metrics-percentile-aggregation.md) algorithm for merging.

:::{tip}
When downsampling a downsampled index, use the same downsampling method as the source index.
:::

### Source and target index field mappings [downsample-api-mappings]

The target downsampled index uses the same field mappings as the source index, with one exception: `time_series_metric: gauge` fields are mapped to `aggregate_metric_double`.

An `aggregate_metric_double` can be used in `max`, `min`, `sum`, `value_count`, and `avg` aggregations without losing accuracy.

{applies_to}`stack: ga 9.4` {applies_to}`serverless: ga` In ES|QL, a downsampled gauge stored as `aggregate_metric_double` can still be used as a `double` in other operations, but with reduced accuracy. In this case, the average value for each downsample interval is used as the single representative value.





