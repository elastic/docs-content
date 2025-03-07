---
navigation_title: "Migrating to downsampling"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/rollup-migrating-to-downsampling.html
applies_to:
  stack: ga
  serverless: ga
---



# Migrating from Rollup to downsampling [rollup-migrating-to-downsampling]


Rollup and downsampling are two different features that allow historical metrics to be rolled up. From a high level rollup is more flexible compared to downsampling, but downsampling is a more robust and easier feature to downsample metrics.

The following aspects of downsampling are easier or more robust:

* No need to schedule jobs. Downsampling is integrated with Index Lifecycle Management (ILM) and Data Stream Lifecycle (DSL).
* No separate search API. Downsampled indices can be accessed via the search api and es|ql.
* No separate rollup configuration. Downsampling uses the time series dimension and metric configuration from the mapping.

It isn’t possible to migrate all rollup usages to downsampling. The main requirement is that the data should be stored in Elasticsearch as [time series data stream (TSDS)](../../data-store/data-streams/time-series-data-stream-tsds.md). Rollup usages that basically roll the data up by time and all dimensions can migrate to downsampling.

An example rollup usage that can be migrated to downsampling:

```console
PUT _rollup/job/sensor
{
  "index_pattern": "sensor-*",
  "rollup_index": "sensor_rollup",
  "cron": "0 0 * * * *",
  "page_size": 1000,
  "groups": {
    "date_histogram": {
      "field": "timestamp",
      "fixed_interval": "60m"
    },
    "terms": {
      "fields": [ "node" ]
    }
  },
  "metrics": [
    {
      "field": "temperature",
      "metrics": [ "min", "max", "sum" ]
    },
    {
      "field": "voltage",
      "metrics": [ "avg" ]
    }
  ]
}
```

The equivalent [time series data stream (TSDS)](../../data-store/data-streams/time-series-data-stream-tsds.md) setup that uses downsampling via DSL:

```console
PUT _index_template/sensor-template
{
  "index_patterns": ["sensor-*"],
  "data_stream": { },
  "template": {
    "lifecycle": {
        "downsampling": [
            {
                "after": "1d", <1>
                "fixed_interval": "1h" <3>
            }
        ]
    },
    "settings": {
      "index.mode": "time_series"
    },
    "mappings": {
      "properties": {
        "node": {
          "type": "keyword",
          "time_series_dimension": true <2>
        },
        "temperature": {
          "type": "half_float",
          "time_series_metric": "gauge" <4>
        },
        "voltage": {
          "type": "half_float",
          "time_series_metric": "gauge" <4>
        },
        "@timestamp": { <2>
          "type": "date"
        }
      }
    }
  }
}
```
%  TEST[continued]

The downsample configuration is included in the above template for a [time series data stream (TSDS)](../../data-store/data-streams/time-series-data-stream-tsds.md). Only the `downsampling` part is necessary to enable downsampling, which indicates when to downsample to what fixed interval.

1. In the rollup job, the `cron` field determines when the rollup documents. In the index template, the `after` field determines when downsampling will rollup documents (note that this the time after a rollover has been performed).
2. In the rollup job, the `groups` field determines all dimensions of the group documents are rolled up to. In the index template, the fields with `time_series_dimension` set `true` and the `@timestamp` field determine the group.
3. In the rollup job, the `fixed_interval` field determines how timestamps are aggregated as part of the grouping. In the index template, the `fixed_interval` field has the same purpose. Note that downsampling does not support calendar intervals.
4. In the rollup job, the `metrics` field define the metrics and how to store these metrics. In the index template, all fields with a `time_series_metric` are metric fields. If a field has `gauge` as `time_series_metric` attribute value, then min, max, sum and value counts are stored for this field in the downsampled index. If a field has `counter` as  `time_series_metric` attribute value, then only the last value stored for this field in the downsampled index.
