---
navigation_title: "Quickstart"
description: "Create a time series data stream, ingest sample metrics, and run an ES|QL query."
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Quickstart: Time series data stream basics

Use this quickstart to set up a time series data stream (TSDS), ingest a few documents, and run a basic query. These steps show how a TSDS works so you can decide whether it fits your data.

A _time series_ is a sequence of data points collected at regular time intervals. For example, you might track CPU usage or stock price over time. This quickstart uses simplified weather sensor readings to show how a TSDS helps you analyze metrics data over time.

By the end of this quickstart, you can:

* Create an index template for a TSDS
* Ingest sample metrics into a data stream
* Query the data with {{esql}}

## Before you begin [quickstart-tsds-prereqs]

* Access to [{{dev-tools-app}} Console](/explore-analyze/query-filter/tools/console.md) in {{kib}}, or another way to make {{es}} API requests

* Cluster and index permissions:
  * [Cluster privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster): `manage_index_templates`
  * [Index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices): `create_doc`, `create_index`, `read`, and `delete_index`

* Familiarity with [time series data stream concepts](time-series-data-stream-tsds.md) and [{{es}} index and search basics](/solutions/search/get-started.md)

You can follow this guide using any {{es}} deployment.
To see all deployment options, refer to [](/deploy-manage/deploy.md#choosing-your-deployment-type).
To get started quickly, spin up a cluster [locally in Docker](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md).

## Create and query a TSDS

:::::{stepper}
::::{step} Create an index template

To create a data stream, you need an index template to base it on. The template defines the data stream structure and settings. (For this quickstart, you don't need to understand template details.)

A TSDS uses _dimension_ fields and _metric_ fields. [Dimensions](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md#time-series-dimension) uniquely identify the time series and are typically based on a descriptive property like `location`. [Metrics](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md#time-series-metric) are measurements that change over time.

Use the [create index template API]({{es-apis}}operation/operation-indices-put-index-template) to create a template with two identifying dimension fields and two metric fields for weather measurements:

```console
PUT _index_template/quickstart-tsds-template
{
  "index_patterns": ["quickstart-*"],
  "data_stream": { }, <1>
  "priority": 100,
  "template": {
    "settings": {
      "index.mode": "time_series" <2>
    },
    "mappings": {
      "properties": {
        "sensor_id": {
          "type": "keyword",
          "time_series_dimension": true <3>
        },
        "location": {
          "type": "keyword",
          "time_series_dimension": true
        },
        "temperature": {
          "type": "half_float",
          "time_series_metric": "gauge" <4>
        },
        "humidity": {
          "type": "half_float",
          "time_series_metric": "gauge"
        },
        "@timestamp": {
          "type": "date"
        }
      }
    }
  }
}
```

1. Indicates this is a data stream, not a regular index.
2. Required index mode for a TSDS.
3. Marks `sensor_id` as a dimension. The template also defines `location` as a dimension.
4. Marks `temperature` as a gauge metric. The template also defines `humidity` as a gauge.

This example defines a `@timestamp` field for illustration purposes. Usually, you can use the default `@timestamp` field (which has a default type of `date`) instead of defining a timestamp in the mapping.

The response includes `"acknowledged": true`, which confirms the template was created.

::::

::::{step} Create a data stream and add sample data

In this step, create a new data stream called `quickstart-weather` based on the index template defined in Step 1. You can create the data stream and add documents in a single API call.

Use the [bulk API]({{es-apis}}operation/operation-bulk) to add multiple documents at once. Before you run the request, set each `@timestamp` to within a few minutes of the current time:

```console
PUT quickstart-weather/_bulk
{ "create":{ } }
{ "@timestamp": "2026-08-17T15:27:00Z", "sensor_id": "STATION-0001", "location": "base", "temperature": 26.7, "humidity": 49.9 }
{ "create":{ } }
{ "@timestamp": "2026-08-17T15:28:00Z", "sensor_id": "STATION-0002", "location": "base", "temperature": 27.2, "humidity": 50.1 }
{ "create":{ } }
{ "@timestamp": "2026-08-17T15:35:00Z", "sensor_id": "STATION-0003", "location": "base", "temperature": 28.1, "humidity": 48.7 }
{ "create":{ } }
{ "@timestamp": "2026-08-17T15:27:00Z", "sensor_id": "STATION-0004", "location": "satellite", "temperature": 32.4, "humidity": 88.9 }
{ "create":{ } }
{ "@timestamp": "2026-08-17T15:36:00Z", "sensor_id": "STATION-0005", "location": "satellite", "temperature": 32.3, "humidity": 87.5 }
```

A successful request returns `"errors": false` and a `create` item for each document.

:::{dropdown} Example response

```console-result
{
  "errors": false,
  "took": 201,
  "items": [
    {
      "create": {
        "_index": ".ds-quickstart-weather-2026.08.17-000001",
        "_id": "n1TMXZekg4PbwmflIo-DEH___l_vqrZfe0V20A",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 2,
          "successful": 1,
          "failed": 0
        },
        "_seq_no": -2,
        "_primary_term": 0,
        "status": 201
      }
    },
    ...
  ]
}
```

:::

:::{tip}
If you get an error about timestamp values, check the error response for the valid timestamp range and run the bulk API again with appropriate `@timestamp` values.
For more details, refer to [Accepted time range for adding data](/manage-data/data-store/data-streams/time-bound-tsds.md#tsds-accepted-time-range).
:::

::::
::::{step} Run a query

With documents in the data stream, you can use the {{esql}} [query API]({{es-apis}}operation/operation-esql-query) to query the data. This sample aggregation shows the maximum of average temperature per sensor for each location, in hourly buckets.

```console
POST _query?format=txt
{
  "query": "TS quickstart-weather | STATS max(avg_over_time(temperature)) BY location, TBUCKET(1h)"
}
```

:::{dropdown} Example response

```txt
max(avg_over_time(temperature))|   location    |      TBUCKET(1h)       
-------------------------------+---------------+------------------------
28.09375                       |base           |2026-08-17T15:00:00.000Z
32.40625                       |satellite      |2026-08-17T15:00:00.000Z
```
:::

:::{tip}
You can also try this aggregation in a [data view](/explore-analyze/find-and-organize/data-views.md) in {{kib}}.
:::

::::

::::{step} Delete the TSDS

When you no longer need the TSDS and index template created in this quickstart, use the [delete data streams API]({{es-apis}}operation/operation-indices-delete-data-stream) and [delete index template API]({{es-apis}}operation/operation-indices-delete-index-template).
For example:

```console
DELETE /_data_stream/quickstart-weather
DELETE /_index_template/quickstart-tsds-template
```

::::
:::::

## Next steps

This quickstart introduced the basics of time series data streams. To learn more, explore these topics:

* [](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md)
* [](/manage-data/data-store/data-streams/set-up-tsds.md)

If you're working with OpenTelemetry (OTLP) or Prometheus data, refer to:

* [](/manage-data/data-store/data-streams/tsds-ingest-otlp.md)
* [](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md)
* [](/solutions/observability/get-started/opentelemetry/quickstart/index.md)

For more information about the APIs used in this quickstart, review the {{es}} API reference documentation:

* [Bulk API]({{es-apis}}operation/operation-bulk)
* [Index template API]({{es-apis}}operation/operation-indices-put-index-template)
* [ES|QL query API]({{es-apis}}operation/operation-esql-query)
