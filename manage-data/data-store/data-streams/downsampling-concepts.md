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

For the most current data, the metrics series typically has a low sampling time interval, to optimize for queries that require a high data resolution.

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
3. For each [time series metric](time-series-data-stream-tsds.md#time-series-metric) field, computes aggregations for all documents in the bucket.

    * `gauge` field type:
        * `min`, `max`, `sum`, and `value_count` are stored as type `aggregate_metric_double`
    * `counter` field type:
        * `last_value` is stored.

4. For all other fields, copies the most recent value to the target index.
5. Replaces the original index with the downsampled index, then deletes the original index.

The new, downsampled index is created on the data tier of the original index and inherits the original settings, like number of shards and replicas.

:::{tip}
You can downsample a downsampled index. The subsequent downsampling interval must be a multiple of the interval used in the preceding downsampling operation.
:::

% TODO ^^ consider mini table in step 3; refactor generally

### Source and target index field mappings [downsample-api-mappings]

Fields in the target downsampled index are created with the same mapping as in the source index, with one exception: `time_series_metric: gauge` fields are changed to `aggregate_metric_double`.






