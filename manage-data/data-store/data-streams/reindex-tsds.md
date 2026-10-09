---
navigation_title: "Reindex a TSDS"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tsds-reindex.html
applies_to:
  stack: ga
  serverless:
    elasticsearch: ga
    observability: ga
    security: ga
    vectordb: unavailable
products:
  - id: elasticsearch
type: how-to
description: Reindex documents into a new time series data stream with the reindex API. Account for time-bound backing indices and timestamp windows.
---

# Reindex a time series data stream [tsds-reindex]

Copy documents from an existing {{tsds}} ({{tsds-init}}) into a new data stream when you need to change [mappings or static index settings](/manage-data/data-store/data-streams/modify-data-stream.md#data-streams-use-reindex-to-change-mappings-settings), or when you want to [filter or transform documents](elasticsearch://reference/elasticsearch/rest-apis/reindex-indices.md) during the copy. A {{tsds-init}} needs extra steps because it stores metrics in time-bound backing indices and {{es}} accepts a document only when its `@timestamp` falls in one of those time ranges.

## Before you begin [tsds-reindex-prereqs]

- Use this process for a {{tsds-init}} that doesn't have a [downsampling](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) configuration. To reindex a downsampled data stream, reindex the backing indices individually, then add them to a new, empty data stream.
- For a major version upgrade, use the [reindex legacy backing indices API]({{es-apis}}operation/operation-indices-migrate-reindex) instead of this reindex operation.
- Review [time-bound indices](/manage-data/data-store/data-streams/time-bound-tsds.md) so you understand the timestamp window each backing index accepts.

The examples on this page use Dev Tools [**Console**](/explore-analyze/query-filter/tools/console.md) syntax.

## Reindex the data stream [reindex-the-data-stream]

:::::::{applies-switch}

::::::{applies-item} stack: ga 9.5+

:::::{stepper}

::::{step} Turn on past index creation

:::{include} /manage-data/_snippets/enable-backfill.md
:::
::::

::::{step} Create the destination index template
:anchor: tsds-reindex-create-template

Create an index template for the destination {{tsds-init}} with your preferred mappings and settings.
For example:

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

Don't add [data stream lifecycle](/manage-data/lifecycle/data-stream.md) or [{{ilm}}](/manage-data/lifecycle/index-lifecycle-management.md) details to the template yet.
That keeps lifecycle actions such as downsampling from modifying the destination while you reindex.
::::

::::{step} Create the destination data stream
:anchor: tsds-reindex-create-data-stream-op

Create a data stream with the [create a data stream API]({{es-apis}}operation/operation-indices-create-data-stream).
The data stream name must match the `index_patterns` in your index template.
For example:

```console
PUT _data_stream/my-new-tsds
```

::::

::::{step} Run the reindex operation

Use the [reindex API]({{es-apis}}operation/operation-reindex) to copy documents from the source to the destination data stream.
For example:

```console
POST /_reindex
{
  "source": {
    "index": "old-tsds"
  },
  "dest": {
    "index": "my-new-tsds",
    "op_type": "create"
  }
}
```

{{es}} adds past backing indices to the destination data stream because you turned on past index creation.

Use the [get data stream API]({{es-apis}}operation/operation-indices-get-data-stream) to check that backing indices cover the timestamps you reindexed.
For example:

```console
GET _data_stream/my-new-tsds
```

The response lists each backing index and the time range it accepts.
::::

::::{step} Add data stream lifecycle
:anchor: tsds-lifecycle

After the reindex completes, add a [data stream lifecycle](/manage-data/lifecycle/data-stream.md) to manage retention, performance, and storage.
For example, use the [update data stream lifecycles]({{es-apis}}operation/operation-indices-put-data-lifecycle) API:

```console
PUT _data_stream/my-new-tsds/_lifecycle
{
  "enabled": true,
  "data_retention": "365d"
}
```

You can also update the index template to add lifecycle details.
For more details, refer to [Set a data stream's lifecycle](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md#set-lifecycle).
::::
:::::

::::::

::::::{applies-item} { stack: ga 9.0-9.4, serverless: ga }

:::::{stepper}

::::{step} Create the destination index template

Create an index template for the destination {{tsds-init}} with temporary settings so the first backing index can accept the source timestamps:

1. Set `index.time_series.start_time` and `index.time_series.end_time` to match the lowest and highest `@timestamp` values in the old data stream.
2. Set `index.number_of_shards` to the sum of all primary shards of all backing indices of the old data stream.
3. Clear the `index.lifecycle.name` index setting (if any), to prevent {{ilm}} from modifying the destination data stream during reindexing.
4. (Optional) Set `index.number_of_replicas` to zero to speed up reindexing. Because the data is copied, you don't need replicas.

```console
PUT _index_template/my-new-tsds-template
{
  "index_patterns": ["my-new-tsds"],
  "priority": 100,
  "data_stream": {},
  "template": {
    "settings": {
      "index.mode": "time_series",
      "index.routing_path": ["dimension_field"],
      "index.time_series.start_time": "2023-01-01T00:00:00Z", <1>
      "index.time_series.end_time": "2025-01-01T00:00:00Z", <2>
      "index.number_of_shards": 6, <3>
      "index.number_of_replicas": 0, <4>
      "index.lifecycle.name": null <5>
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

1. Lowest timestamp value in the old data stream
2. Highest timestamp value in the old data stream
3. Sum of the primary shards from all source backing indices
4. Speed up reindexing
5. Pause {{ilm}}
::::

::::{step} Create the destination data stream

Create a data stream with the [create a data stream API]({{es-apis}}operation/operation-indices-create-data-stream).
The data stream name must match the `index_patterns` in your index template.
For example:

```console
PUT _data_stream/my-new-tsds
```

::::

::::{step} Run the reindex operation

Use the [reindex API]({{es-apis}}operation/operation-reindex) to copy documents from the source to the destination data stream.
For example:

```console
POST /_reindex
{
  "source": {
    "index": "old-tsds"
  },
  "dest": {
    "index": "my-new-tsds",
    "op_type": "create"
  }
}
```

Use the [get data stream API]({{es-apis}}operation/operation-indices-get-data-stream) to check that backing indices cover the timestamps you reindexed.
For example:

```console
GET _data_stream/my-new-tsds
```

The response lists each backing index and the time range it accepts.
::::

::::{step} Restore the destination index template
:anchor: tsds-reindex-restore

After reindexing completes, update the index template to remove the temporary settings:

* Remove the overrides for `index.time_series.start_time` and `index.time_series.end_time`.
* Restore the values of `index.number_of_shards`, `index.number_of_replicas`, and `index.lifecycle.name` (as applicable).

```console
PUT _index_template/my-new-tsds-template
{
  "index_patterns": ["my-new-tsds"],
  "priority": 100,
  "data_stream": {},
  "template": {
    "settings": {
      "index.mode": "time_series",
      "index.routing_path": ["dimension_field"],
      "index.number_of_replicas": 1, <1>
      "index.lifecycle.name": "my-ilm-policy" <2>
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

1. Restore replicas
2. Re-enable {{ilm}}
::::

::::{step} Roll over for new data

The reindex operation copies documents into a single backing index of the destination data stream.
Create a new backing index with a manual rollover request for incoming data:

```console
POST my-new-tsds/_rollover/
```

The destination data stream can accept new documents.
::::
:::::

::::::
:::::::

## Related pages

- [Time series data streams overview](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md)
- [Time-bound indices](/manage-data/data-store/data-streams/time-bound-tsds.md)
- [Reindex indices examples](elasticsearch://reference/elasticsearch/rest-apis/reindex-indices.md)
- [Reindex with a data stream](/manage-data/data-store/data-streams/use-data-stream.md#reindex-with-a-data-stream)
- [Load historical data into a {{tsds}}](/manage-data/data-store/data-streams/load-historical-tsds.md)
