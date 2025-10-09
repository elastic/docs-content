---
navigation_title: "Quickstart"
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Quickstart: Time series data stream basics

Use this quickstart to set up a time series data stream (TSDS), ingest a few documents, and run a basic query. These high-level steps help you see how a TSDS works, so you can decide whether it's right for your data.

A _time series_ is a sequence of data points collected at regular time intervals. For example, you might track CPU usage or stock price over time. This quickstart uses simplified weather sensor readings to show how a TSDS helps you analyze metrics data over time. 

## Prerequisites

* Access to [{{dev-tools-app}} Console](/explore-analyze/query-filter/tools/console.md) in {{kib}}, or another way to make {{es}} API requests

* Cluster and index permissions: 
    * [Cluster privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster):  `manage_index_templates`
    * [Index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices): `create_doc` and `create_index`

* Familiarity with [time series data stream concepts](time-series-data-stream-tsds.md) and [{{es}} index and search basics](/solutions/search/get-started.md) 

You can follow this guide using any {{es}} deployment.
To see all deployment options, refer to [](/deploy-manage/deploy.md#choosing-your-deployment-type).
To get started quickly, spin up a cluster [locally in Docker](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md).


## Create and query a TSDS

:::::{stepper}
::::{step} Create an index template

To create a data stream, you need an index template to base it on. The template defines the data stream structure and settings. (For this quickstart, you don't need to understand template details.)

A TSDS uses _dimension_ fields and _metric_ fields. [Dimensions](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md#time-series-dimension) are used to uniquely identify the time series and are typically based on a descriptive property like `location`.  [Metrics](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md#time-series-metric) are measurements that change over time.  

Use an [`_index_template` request](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) to create a template with two identifying dimension fields and two metric fields for weather measurements:

``` console
PUT _index_template/quickstart-tsds-template  
{
  "index_patterns": ["quickstart-*"],
  "data_stream": { },   # Indicates this is a data stream, not a regular index.
  "priority": 100, 
  "template": {
    "settings": {
      "index.mode": "time_series"   # The required index mode for TSDS.
    },
    "mappings": {
      "properties": {
        "sensor_id": {
          "type": "keyword",
          "time_series_dimension": true   # Defines a dimension field.
        },
        "location": {
          "type": "keyword",
          "time_series_dimension": true   # Another dimension field.
        },
        "temperature": {
          "type": "half_float",
          "time_series_metric": "gauge"   # A supported field type for metrics.
         },
        "humidity": {
          "type": "half_float",
          "time_series_metric": "gauge"   # A second measurement.
        },
        "@timestamp": {
          "type": "date"
        }
      }
    }
  }
}

```

This example defines a `@timestamp` field for illustration purposes. In most cases, you can use the default `@timestamp` field (which has a default type of `date`) instead of defining a timestamp in the mapping. 

You should get a response of `"acknowledged": true` that confirms the template was created.

::::

::::{step} Create a data stream and add sample data

In this step, create a new data stream called `quickstart-weather` based on the index template defined in Step 1. You can create the data stream and add documents in a single API call.

Use a [`_bulk` API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) request to add multiple documents at once. Make sure to adjust the timestamps to within a few minutes of the current time.

% TODO simplify timestamps

```console
PUT quickstart-weather/_bulk
{ "create":{ } }
{ "@timestamp": "2025-09-08T21:25:00.000Z", "sensor_id": "STATION-0001", "location": "base", "temperature": 26.7, "humidity": 49.9 }
{ "create":{ } }
{ "@timestamp": "2025-09-08T21:26:00.000Z", "sensor_id": "STATION-0002", "location": "base", "temperature": 27.2, "humidity": 50.1 }
{ "create":{ } }
{ "@timestamp": "2025-09-08T21:35:00.000Z", "sensor_id": "STATION-0003", "location": "base", "temperature": 28.1, "humidity": 48.7 }
{ "create":{ } }
{ "@timestamp": "2025-09-08T21:27:00.000Z", "sensor_id": "STATION-0004", "location": "satellite", "temperature": 32.4, "humidity": 88.9 }
{ "create":{ } }
{ "@timestamp": "2025-09-08T21:36:00.000Z", "sensor_id": "STATION-0005", "location": "satellite", "temperature": 32.3, "humidity": 87.5 }
```

The response shows five sample weather data documents. 

:::{dropdown} Example response

```console-result
{
  "errors": false,
  "took": 0,
  "items": [
    {
      "create": {
        "_index": ".ds-quickstart-weather-2025.09.08-000001",
        "_id": "cFJZQJlNh-Xl8V_rAAABmSs3x-A",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 2,
          "successful": 2,
          "failed": 0
        },
        "_seq_no": 0,
        "_primary_term": 1,
        "status": 201
      }
    },
    {
      "create": {
        "_index": ".ds-quickstart-weather-2025.09.08-000001",
        "_id": "c-wsTT0T4CtI3hOuAAABmSs4skA",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 2,
          "successful": 2,
          "failed": 0
        },
        "_seq_no": 1,
        "_primary_term": 1,
        "status": 201
      }
    },
    {
      "create": {
        "_index": ".ds-quickstart-weather-2025.09.08-000001",
        "_id": "Hdee5vMpBvZymWvHAAABmStA76A",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 2,
          "successful": 2,
          "failed": 0
        },
        "_seq_no": 2,
        "_primary_term": 1,
        "status": 201
      }
    },
    {
      "create": {
        "_index": ".ds-quickstart-weather-2025.09.08-000001",
        "_id": "e3Z2UirUQldsjLr2AAABmSs5nKA",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 2,
          "successful": 2,
          "failed": 0
        },
        "_seq_no": 3,
        "_primary_term": 1,
        "status": 201
      }
    },
    {
      "create": {
        "_index": ".ds-quickstart-weather-2025.09.08-000001",
        "_id": "N3-RYtQAp6JEsLRNAAABmStB2gA",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 2,
          "successful": 2,
          "failed": 0
        },
        "_seq_no": 4,
        "_primary_term": 1,
        "status": 201
      }
    }
  ]
}
```
:::

:::{tip}
If you get an error about timestamp values, check the error response for the valid timestamp range. For more details, refer to [Accepted time range for adding data](/manage-data/data-store/data-streams/time-bound-tsds.md#tsds-accepted-time-range).

:::

::::
::::{step} Run a query

Now that your data stream has some documents, you can use the [`_search` endpoint](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) to query the data. This sample aggregation shows average temperature for each location, in hourly buckets. (You don't need to understand the details of aggregations to follow this example.) 

```console
POST quickstart-weather/_search  
{
  "size": 0,
  "aggs": {
    "by_location": {
      "terms": {
        "field": "location"  # The location dimension defined in the template.
      },
      "aggs": {
        "avg_temp_per_hour": {
          "date_histogram": {
            "field": "@timestamp",
            "fixed_interval": "1h"
          },
          "aggs": {
            "avg_temp": {
              "avg": {
                "field": "temperature"  # A metric field defined in the template.
              }
            }
          }
        }
      }
    }
  }
}
```

:::{dropdown} Example response

```console-result
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 5,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "by_location": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "base",
          "doc_count": 3,
          "avg_temp_per_hour": {
            "buckets": [
              {
                "key_as_string": "2025-09-08T21:00:00.000Z",
                "key": 1757365200000,
                "doc_count": 3,
                "avg_temp": {
                  "value": 27.333333333333332
                }
              }
            ]
          }
        },
        {
          "key": "satellite",
          "doc_count": 2,
          "avg_temp_per_hour": {
            "buckets": [
              {
                "key_as_string": "2025-09-08T21:00:00.000Z",
                "key": 1757365200000,
                "doc_count": 2,
                "avg_temp": {
                  "value": 32.359375
                }
              }
            ]
          }
        }
      ]
    }
  }
}
```
:::

:::{tip}
You can also try this aggregation in a [data view](/explore-analyze/find-and-organize/data-views.md) in {{kib}}.
:::

::::
:::::

## Next steps

This quickstart introduced the basics of time series data streams. To learn more, explore these topics:

* [](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md)
* [](/manage-data/data-store/data-streams/set-up-tsds.md)

If you're working with OpenTelemetry (OTLP) data, refer to the OTLP documentation:
* [](/manage-data/data-store/data-streams/tsds-ingest-otlp.md)
* [](/solutions/observability/get-started/opentelemetry/quickstart/index.md)

For more information about the APIs used in this quickstart, review the {{es}} API reference documentation:

* [Bulk API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk)
* [Index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template)
* [Search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search)
