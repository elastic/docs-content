---
navigation_title: "Reindex a TSDS"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tsds-reindex.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Reindex a time series data stream [tsds-reindex]

Reindexing allows you to copy documents from an existing [time series data stream (TSDS)](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) to a new one. All data streams support reindexing, but time series data streams require special handling due to their time-bound backing indices and strict timestamp acceptance windows.

:::{important}
When you reindex, the result is a single backing index of a new data stream.
:::

To reindex, follow the steps on this page.

:::{note}
This process only applies to time series data streams without a [downsampling](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) configuration. To reindex a downsampled data stream, reindex the backing indices individually, then add them to a new, empty data stream.
:::

## Overview

These high-level steps summarize the process of reindexing a time series data stream. Each step is detailed in a later section.

1. Create an index template for the destination data stream
2. Update the template with temporary settings for reindexing
3. Run the reindex operation
4. Revert the temporary index settings
5. Perform a manual rollover to create a new backing index for incoming data

The examples on this page use Dev Tools [Console](/explore-analyze/query-filter/tools/console.md) syntax.

## Create the destination index template [tsds-reindex-create-template]

Create an index template for the new TSDS, using your preferred mappings and settings:

```console
PUT _index_template/my-new-tsds-template
{
  "index_patterns": ["my-new-tsds"],
  "priority": 100,
  "data_stream": {},
  "template": {
    "settings": {
      "index.mode": "time_series"
    },
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date"
        },
        "dimension_field": {
          "type": "keyword",
          "time_series_dimension": true
        },
        "metric_field": {
          "type": "double",
          "time_series_metric": "gauge"
        }
      }
    }
  }
}
```
## Update the template for reindexing 

To support the reindexing process, you need to temporarily modify the template:

  1. Set `index.time_series.start_time` and `index.time_series.end_time` index settings to match the lowest and highest `@timestamp` values in the old data stream. 
  2. Set `index.number_of_shards` to the sum of all primary shards of all backing indices of the old data stream. 
  3. Clear the `index.lifecycle.name` index setting (if any), to prevent ILM from modifying the destination data stream during reindexing.
  4. (Optional) Set `index.number_of_replicas` to zero, to speed up reindexing. Because the data gets copied in the reindexing process, you don't need replicas.

```console
PUT _index_template/new-tsds-template
{
  "index_patterns": ["new-tsds*"],
  "priority": 100,
  "data_stream": {},
  "template": {
    "settings": {
      "index.mode": "time_series",
      "index.routing_path": ["host", "service"], 
      "index.time_series.start_time": "2023-01-01T00:00:00Z", <1>
      "index.time_series.end_time": "2025-01-01T00:00:00Z",  <2>
      "index.number_of_shards": 6, <3>
      "index.number_of_replicas": 0, <4>
      "index.lifecycle.name": null  <5>
    },
    "mappings": {
      ...
    }
  }
}
```

1. Lowest timestamp value in the old data stream
2. Highest timestamp value in the old data stream
3. Sum of the primary shards from all source backing indices
4. Speed up reindexing
5. Pause ILM

### Create the destination data stream and reindex [tsds-reindex-op]

Run the reindex operation:

```console
POST /_reindex
{
  "source": {
    "index": "old-tsds"
  },
  "dest": {
    "index": "new-tsds",
    "op_type": "create"
  }
}
```


## Restore the destination index template [tsds-reindex-restore]

After reindexing completes, update the index template again to remove the temporary settings:

* Remove the overrides for `index.time_series.start_time` and `index.time_series.end_time`.
* Restore the values of `index.number_of_shards`, `index.number_of_replicas`,  and  `index.lifecycle.name` (as applicable).

```console
PUT _index_template/new-tsds-template
{
  "index_patterns": ["new-tsds*"],
  "priority": 100,
  "data_stream": {},
  "template": {
    "settings": { 
      "index.mode": "time_series",
      "index.routing_path": ["host", "service"],
      "index.number_of_replicas": 1, <1>
      "index.lifecycle.name": "my-ilm-policy" <2>
    }, 
    "mappings": {
      ...
    }
  }
}
```

1. Restore replicas
2. Re-enable ILM

## Roll over for new data

Create a new backing index with a manual rollover request:

```console
POST new-tsds/_rollover/
```

The destination data stream is now ready to accept new documents.

## Related resources

- [Time series data streams overview](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md)
- [Reindex API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex)