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

# Reindex a {{tsds}}

Copy documents from an existing {{tsds}} ({{tsds-init}}) into a new data stream when you need to change [mappings or static index settings](/manage-data/data-store/data-streams/modify-data-stream.md#data-streams-use-reindex-to-change-mappings-settings), or when you want to [filter or transform documents](elasticsearch://reference/elasticsearch/rest-apis/reindex-indices.md) during the copy.
A {{tsds-init}} needs extra steps because it stores metrics in time-bound backing indices and {{es}} accepts a document only when its `@timestamp` falls in one of those time ranges.

Use this process for a {{tsds-init}} that doesn't have a [downsampling](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) configuration.
To reindex a downsampled data stream, reindex the backing indices individually, then add them to a new, empty data stream.

For a major version upgrade, use the [reindex legacy backing indices API]({{es-apis}}operation/operation-indices-migrate-reindex) instead of this reindex operation.

## Before you begin [overview]

- You must be familiar with [{{tsds-init}} concepts](time-series-data-stream-tsds.md). Try the [quickstart](/manage-data/data-store/data-streams/quickstart-tsds.md) for a hands-on introduction.
- You must have the following permissions:
  - [Cluster privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster)
    - `manage_index_templates` to create a template
    - {applies_to}`stack: ga 9.0-9.4` `manage_ilm` if you use [{{ilm}}](/manage-data/lifecycle/index-lifecycle-management.md)
    - {applies_to}`stack: ga 9.5+` `manage` to update cluster settings
  - [Index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices)
    - `create_doc` and `create_index` to create a {{tsds-init}}
    - `read` on the source and `write` on the destination to reindex a {{tsds-init}}
    - `manage` to roll over a {{tsds-init}}
    - `manage_data_stream_lifecycle` if you use [data stream lifecycle](/manage-data/lifecycle/data-stream.md)
    - {applies_to}`stack: ga 9.5+` `auto_configure` to automatically create past indices

The examples on this page use {{dev-tools-app}} [**Console**](/explore-analyze/query-filter/tools/console.md) syntax.
You must have access to [{{dev-tools-app}} Console](/explore-analyze/query-filter/tools/console.md) in {{kib}} or another way to make {{es}} API requests.

## Reindex the data stream

:::::::{applies-switch}
::::::{applies-item} stack: ga 9.5+
:::::{stepper}
::::{step} Turn on past index creation

:::{include} /manage-data/_snippets/enable-backfill.md
:::
::::
::::{step} Create the destination index template
:anchor: tsds-reindex-create-template

Create an index template for the destination {{tsds-init}} with the [create an index template API]({{es-apis}}operation/operation-indices-put-index-template).
Use your preferred mappings and settings.
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

Don't add data stream lifecycle or {{ilm}} details to the template yet.
That keeps lifecycle actions such as downsampling from modifying the destination while you reindex.
::::
::::{step} Create the destination data stream
:anchor: create-destination

Create a data stream with the [create a data stream API]({{es-apis}}operation/operation-indices-create-data-stream).
The data stream name must match the `index_patterns` in your index template.
For example:

```console
PUT _data_stream/my-new-tsds
```

::::
::::{step} Run the reindex operation
:anchor: tsds-reindex-op

Use the [reindex API]({{es-apis}}operation/operation-reindex) to copy documents from the source to the destination data stream.
For example:

```console
POST /_reindex
{
  "source": {
    "index": "my-old-tsds"
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
:anchor: add-lifecycle

:::{include} /manage-data/_snippets/add-lifecycle.md
:::
::::
::::{step} Turn off past index creation

If you don't want the [past index creation](/manage-data/data-store/data-streams/time-bound-tsds.md#tsds-past-index-creation) feature enabled for all of the data streams in your cluster, turn it off:

```console
PUT _cluster/settings
{
  "persistent": {
    "data_stream.past_tsdb_index_creation_enabled": false
  }
}
```

Refer to [`data_streams.past_tsdb_index_interval`](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#time-series-data-stream).
::::
:::::
::::::
::::::{applies-item} stack: ga 9.0-9.4
:::::{stepper}
::::{step} Identify time bounds
:anchor: time-bounds

Search for the lowest and highest `@timestamp` values in the old data stream.
For example:

```console
POST my-old-tsds/_search?size=0
{
  "aggs": {
    "min_ts": { "min": { "field": "@timestamp" } },
    "max_ts": { "max": { "field": "@timestamp" } }
  }
}
```

Add a buffer on both sides of these values.
Subtract a small amount from the `min` date and add a small amount to the `max` date.
For example, if your observed range is from `2026-10-13T17:50:23.747Z` to `2026-10-13T18:50:21.747Z`, use values like `2026-10-13T17:50:22.747Z` and `2026-10-13T18:50:22.747Z` when you create the destination index template.
::::
::::{step} Identify number of shards
:anchor: shards

Calculate the sum of all primary shards of all backing indices of the old data stream.
For example, list the backing indices for the data stream with the [get data streams API]({{es-apis}}operation/operation-indices-get-data-stream):

```console
GET _data_stream/my-old-tsds
```

For each backing index, check its `index.number_of_shards` setting.
For example:

```console
GET .ds-my-old-tsds-*/_settings/index.number_of_shards
```

Sum the`index.number_of_shards` values for all backing indices of the source data stream.
This value is used when you create the destination index template.
::::
::::{step} Create the destination index template
:anchor: update-the-template-for-reindexing

Create an index template for the destination {{tsds-init}} with the [create an index template API]({{es-apis}}operation/operation-indices-put-index-template).
Use temporary settings so the first backing index can accept the source timestamps:

1. Set `index.time_series.start_time` and `index.time_series.end_time` to the time bounds you identified in the previous step.
2. Set `index.number_of_shards` to the number of shards you identified in the previous step.
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

1. Lowest timestamp value in the old data stream minus a small buffer
2. Highest timestamp value in the old data stream plus a small buffer
3. Sum of the primary shards from all source backing indices
4. Speed up reindexing
5. Pause {{ilm}} if it was configured
::::

::::{step} Create the destination data stream
:anchor: create-90-destination

Create a data stream with the [create a data stream API]({{es-apis}}operation/operation-indices-create-data-stream).
The data stream name must match the `index_patterns` in your index template.
For example:

```console
PUT _data_stream/my-new-tsds
```

::::
::::{step} Run the reindex operation
:anchor: reindex-90-op

Use the [reindex API]({{es-apis}}operation/operation-reindex) to copy documents from the source to the destination data stream.
For example:

```console
POST /_reindex
{
  "source": {
    "index": "my-old-tsds"
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
2. Re-enable {{ilm}} if it was configured
::::
::::{step} Add data stream lifecycle
:anchor: add-90-lifecycle

:::{include} /manage-data/_snippets/add-lifecycle.md
:::
::::

::::{step} Roll over for new data
:anchor: roll-over-for-new-data

The reindex operation copies documents into a single backing index of the destination data stream.
Roll over the data stream so new documents go to a fresh backing index created with the intended lifecycle configuration.
For example, use the [roll over API]({{es-apis}}operation/operation-indices-rollover):

```console
POST my-new-tsds/_rollover/
```

When this step is complete, the destination data stream can accept new documents.
::::
:::::
::::::

% Serverless project users can't set shard count, replica count, or an ILM policy, and they can't turn on past index creation. Keep this tab limited to public time-bound settings and data stream lifecycle.
::::::{applies-item} serverless: ga
:::::{stepper}
::::{step} Identify time bounds
:anchor: serverless-time-bounds

Search for the lowest and highest `@timestamp` values in the old data stream.
For example:

```console
POST my-old-tsds/_search?size=0
{
  "aggs": {
    "min_ts": { "min": { "field": "@timestamp" } },
    "max_ts": { "max": { "field": "@timestamp" } }
  }
}
```

Add a buffer on both sides of these values.
Subtract a small amount from the `min` date and add a small amount to the `max` date.
For example, if your observed range is from `2026-10-13T17:50:23.747Z` to `2026-10-13T18:50:21.747Z`, use values like `2026-10-13T17:50:22.747Z` and `2026-10-13T18:50:22.747Z` in the next step.

::::
::::{step} Create the destination index template
:anchor: serverless-template

Create an index template for the destination {{tsds-init}} with the [create an index template API](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-indices-put-index-template).
Set `index.time_series.start_time` and `index.time_series.end_time` to the time bounds identified in the preceding step so the first backing index can accept the source timestamps.
For example:

```console
PUT _index_template/my-new-tsds-template
{
  "index_patterns": ["my-new-tsds"],
  "priority": 100,
  "data_stream": {},
  "template": {
    "settings": {
      "index.mode": "time_series",
      "index.time_series.start_time": "2023-01-01T00:00:00Z", <1>
      "index.time_series.end_time": "2025-01-01T00:00:00Z", <2>
      <!-- TBD "index.lifecycle.skip": true <3> -->
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
<!-- 3. Instruct data stream lifecycle to not manage the backing indices. -->

<!--
Don't add a data stream lifecycle to the template yet.
That keeps lifecycle actions such as downsampling from modifying the destination while you reindex.
-->
::::

::::{step} Create the destination data stream
:anchor: serverless-destination

Create a data stream with the [create a data stream API]({{es-serverless-apis}}operation/operation-indices-create-data-stream).
The data stream name must match the `index_patterns` in your index template.
For example:

```console
PUT _data_stream/my-new-tsds
```

::::
::::{step} Run the reindex operation
:anchor: serverless-reindex-op

Use the [reindex API]({{es-serverless-apis}}operation/operation-reindex) to copy documents from the source to the destination data stream.
For example:

```console
POST /_reindex
{
  "source": {
    "index": "my-old-tsds"
  },
  "dest": {
    "index": "my-new-tsds",
    "op_type": "create"
  }
}
```

Documents land in that one backing index because its time range was set on the template.

Use the [get data stream API]({{es-serverless-apis}}operation/operation-indices-get-data-stream) to check that the backing index covers the timestamps you reindexed.
For example:

```console
GET _data_stream/my-new-tsds
```

The response lists each backing index and the time range it accepts.
::::

::::{step} Restore the destination index template
:anchor: serverless-restore

After reindexing completes, update the index template and remove `index.time_series.start_time` and `index.time_series.end_time`.
<!-- and `index.lifecycle.skip`. -->

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

::::
::::{step} Add data stream lifecycle
:anchor: add-serverless-lifecycle

After the reindex completes, optionally customise the data stream lifecycle to manage retention, performance, and storage.
For example, use the [update data stream lifecycles]({{es-apis}}operation/operation-indices-put-data-lifecycle) API:

```console
PUT _data_stream/my-new-tsds/_lifecycle
{
  "enabled": true,
  "data_retention": "365d" <1>
}
```

1. The retention period of this data stream is set to 365 days. This means that {{es}} is allowed to delete data that is older than a year at its own discretion.

For more details, refer to [Set a data stream's lifecycle](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md#set-lifecycle).
::::
::::{step} Roll over for new data
:anchor: serverless-roll-over

The reindex operation copies documents into a single backing index of the destination data stream.
Roll over the data stream so new documents go to a fresh backing index created with the intended lifecycle configuration.
For example, use the [roll over API](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-indices-rollover):

```console
POST my-new-tsds/_rollover/
```

When this step is complete, the destination data stream can accept new documents.
Later rollovers happen automatically.
::::
:::::
::::::
:::::::

## Related pages [related-resources]

- [Time series data streams overview](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md)
- [Time-bound indices](/manage-data/data-store/data-streams/time-bound-tsds.md)
- [Reindex indices examples](elasticsearch://reference/elasticsearch/rest-apis/reindex-indices.md)
- [Reindex with a data stream](/manage-data/data-store/data-streams/use-data-stream.md#reindex-with-a-data-stream)
- [Load historical data into a {{tsds}}](/manage-data/data-store/data-streams/load-historical-tsds.md)
