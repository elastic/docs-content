---
navigation_title: "Quickstart"
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Quickstart: Create a time series data stream (TSDS)

Use this quickstart to set up a simple time series data stream (TSDS), ingest a few documents, and run a basic query. These high-level steps help you see how a TSDS works, so you can decide whether it's right for your data.

This quickstart uses some basic sample data to show how you might use a TSDS to analyze weather sensor readings over time. 

## Prerequisites

* Familiarity with time series data stream [concepts](time-series-data-stream-tsds.md) 
* Access to [{{dev-tools-app}} console](/explore-analyze/query-filter/tools/console.md) in Kibana, or another way to make {{es}} API requests
* Required permissions: 
    * [Cluster privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-cluster): `manage_ilm` and `manage_index_templates`
    * [Index privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices): `create_doc` and `create_index`


## Step 1: Create an index template

To create a data stream, you'll need an index template. The template defines the data stream structure and settings. (For this quickstart, you don't need to understand template details.)

Data streams created with this quickstart template have the following characteristics:

* Two identifying dimension fields: `sensor_id`, `location`
* Two measurements or metric fields: `temperature`, `humidity `
* A timestamp field: `@timestamp` 

To create the template, paste the following index template API request into the {{dev-tools-app}} console, or use another method to make the request:

% TODO improve callout comments

``` console
PUT _index_template/quickstart-tsds-template  
{
  "index_patterns": ["quickstart-*"],
  "data_stream": { },   # Indicates this is a data stream, not a regular index
  "priority": 100, 
  "template": {
    "settings": {
      "index.mode": "time_series"   # The required index mode for TSDS
    },
    "mappings": {
      "properties": {
        "sensor_id": {
          "type": "keyword",
          "time_series_dimension": true   # Defines a dimension field
        },
        "location": {
          "type": "keyword",
          "time_series_dimension": true   
        },
        "temperature": {
          "type": "half_float",
          "time_series_metric": "gauge"   # A supported field type for metrics
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


This example defines a `@timestamp` field for illustration purposes. In most cases, you can use the default `@timestamp` field (which has a default type of `date`) instead of defining a timestamp in the mapping. 

## Step 2: Add sample documents

Add a few sample documents to automatically create a new data stream, using bulk ingest. 

In step 1, you specified the template index pattern `quickstart-*`. In this step, you set the data stream name to `quickstart-weather`, to match the template pattern.

:::{note}
By default, new data streams accept documents with `@timestamp` values up to 2 hours before stream creation and 30 minutes after the current time. Specify timestamps that fall within this range, or adjust the `index.look_ahead_time` and `index.look_back_time` [settings](https://www.elastic.co/docs/reference/elasticsearch/index-settings/time-series) to suit your use case.  
:::

Paste the following bulk API request (with adjusted timestamps if needed) into the {{dev-tools-app}} console, or use another method to make the request.

% TODO In practice, bulk requests use more compact formatting. The structure is expanded below for clarity.

```console
PUT quickstart-weather/_bulk
{ "create":{ } }
{ 
  "@timestamp": "2025-08-27T14:00:00.000Z", 
  "sensor_id": "STATION-0001",  
  "location": "base", 
  "temperature": 26.7, 
  "humidity": 49.9 
}
{ "create":{ } }
{ 
  "@timestamp": "2025-08-27T18:00:00.000Z", 
  "sensor_id": "STATION-0002", 
  "location": "satellite", 
  "temperature": 32.4, 
  "humidity": 88.9 
}
{ "create":{ } }
{ 
  "@timestamp": "2025-08-27T19:30:00.000Z", 
  "sensor_id": "STATION-0003", 
  "location": "rover", 
  "temperature": 35.4, 
  "humidity": 78.3 
}
```

If you get an error about timestamp values, check the error response for the valid timestamp range.

## Step 3: Run a query

Now that your data stream has some documents, you can query the data. This sample aggregation calculates average temperature by location, in hourly buckets. (You don't need to understand the details of aggregations to follow this example.) 

Paste the following search API request into the {{dev-tools-app}} console, or use another method to make the request:

```console
POST quickstart-weather/_search  
{
  "size": 0,
  "aggs": {
    "by_location": {
      "terms": {
        "field": "location"  # The location dimension defined in the template
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
                "field": "temperature"  # A metric field defined in the template
              }
            }
          }
        }
      }
    }
  }
}
```

:::{tip}
You can also try this aggregation in a data view in Kibana.
:::

% TODO ## Next steps

% To learn more about time series data streams, explore these topics:

## API reference
This quickstart uses the following {{es}} APIs:
* [Bulk API ](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk)
* [Index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template)
* [Search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search)