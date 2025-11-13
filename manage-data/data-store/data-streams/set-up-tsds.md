---
navigation_title: "Set up a TSDS"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/set-up-tsds.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Set up a time series data stream [set-up-tsds]

This page shows you how to manually set up a [time series data stream](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) (TSDS).

## Before you begin [tsds-prereqs]

- Before you create a time series data stream, review [](../data-streams.md) and [TSDS concepts](time-series-data-stream-tsds.md). You can also try the [quickstart](/manage-data/data-store/data-streams/quickstart-tsds.md) for a hands-on introduction.
- Make sure you have the following permissions:
    - [Cluster privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster)
        - `manage_index_templates` for creating a template to base the TSDS on
        - {applies_to}`stack: ga` `manage_ilm` if you're using [index lifecycle management](#tsds-ilm-policy)
    - [Index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) 
        - `create_doc` and `create_index` for creating or converting a TSDS
        - `manage` to [roll over](#convert-existing-data-stream-to-tsds) a TSDS

::::{note}
If you're working with OpenTelemetry data, try the [OpenTelemetry quickstarts](/solutions/observability/get-started/opentelemetry/quickstart/index.md).
::::

## Set up a TSDS

:::::{stepper}
:::{step} Create an index lifecycle policy (optional)
:anchor: tsds-ilm-policy

```{applies_to}
stack: ga
serverless: unavailable
```

In most cases, you can use a [data stream lifecycle](/manage-data/lifecycle/data-stream.md) to manage your time series data stream. If you're using [data tiers](/manage-data/lifecycle/data-tiers.md) in {{stack}}, you can use [index lifecycle management](/manage-data/lifecycle/index-lifecycle-management.md).

:::{dropdown} Create an ILM policy

If you're using {{stack}}, {{ilm-init}} can help you manage a time series data stream's backing indices. {{ilm-init}} requires an index lifecycle policy.

For best results, specify a `max_age` for the `rollover` action in the policy. This ensures the [`timestamp` ranges](/manage-data/data-store/data-streams/time-bound-tsds.md) for the backing indices are consistent. For example, setting a `max_age` of `1d` for the `rollover` action ensures your backing indices consistently contain one day's worth of data.

**Example:**

```console
PUT _ilm/policy/my-weather-sensor-lifecycle-policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_age": "1d",
            "max_primary_shard_size": "50gb"
          }
        }
      }
      // Additional phases (warm, cold, delete) as needed
      }
    }
  }
}
```

:::


::::{step} Create an index template 
:anchor: create-tsds-index-template

The structure of a time series data stream is defined by an index template. Create an index template with the following required elements and settings:

- **Index patterns:** One or more wildcard patterns matching the name of your TSDS, such as `weather-sensors-*`. For best results, use the [data stream naming scheme](/reference/fleet/data-streams.md#data-streams-naming-scheme).
- **Data stream object:** The template must include `"data_stream": {}`.
- **Time series mode:** Set `index.mode: time_series`.
- **Field mappings:** Define at least one dimension field and typically one or more metric fields:
    - **Dimensions:** To define a dimension, set `time_series_dimension` to `true`. For details, refer to [Dimensions](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md#time-series-dimension). 
        - To define dimensions dynamically, you can use a pass-through object. For details, refer to [Defining sub-fields as time series dimensions](elasticsearch://reference/elasticsearch/mapping-reference/passthrough.md#passthrough-dimensions).
    - **Metrics:** To define a metric, use the `time_series_metric` mapping parameter. For details, refer to [Metrics](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md#time-series-metric).
    - **Timestamp** (optional): Define a `date` or `date_nanos` mapping for the `@timestamp` field. If you don't specify a mapping, {{es}} maps `@timestamp` as a `date` field with default options.
    -  {applies_to}`serverless: unavailable` {applies_to}`stack: ga` **Lifecycle management**: For {{stack}}, include lifecycle settings to enable automatic rollover and prevent indices from growing too large. 
        - Set `"lifecycle": { "enabled": true }`. 
        - If you created an ILM policy in [step 1](#tsds-ilm-policy), reference it with `index.lifecycle.name`.
    - **Other settings**  (optional): Additional index settings, such as [`index.number_of_replicas`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#dynamic-index-number-of-replicas), for the data stream's backing indices.
- **Priority:** Set the priority higher than `200` to avoid [collisions](/manage-data/data-store/templates.md#avoid-index-pattern-collisions) with built-in templates.

**Example index template PUT request:**

```console
PUT _index_template/my-weather-sensor-index-template
{
  "index_patterns": ["metrics-weather_sensors-*"],
  "data_stream": { },
  "template": {
    "settings": {
      "index.mode": "time_series",
      "index.lifecycle.name": "my-lifecycle-policy", <1>
      "lifecycle": { 
        "enabled": true <2>
      }
    },
    "mappings": {
      "properties": {
        "sensor_id": {
          "type": "keyword",
          "time_series_dimension": true
        },
        "location": {
          "type": "keyword",
          "time_series_dimension": true
        },
        "temperature": {
          "type": "half_float",
          "time_series_metric": "gauge"
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
  },
  "priority": 500,
  "_meta": {
    "description": "Template for my weather sensor data"
  }
}
```
1. {{stack}} only
2. {{stack}} only

:::{important}
:applies_to: stack: ga
Without lifecycle management enabled, time series data streams can grow into very large indices that never roll over. This can lead to performance issues. Always configure lifecycle management for {{stack}} production deployments.
:::

:::{dropdown} Component templates (optional)

If you're using component templates with a time series data stream, check the following requirements:

- Each component template is valid on its own
- The `index.routing_path` setting and its referenced dimension fields are defined in the same component template
- The `time_series_dimension` attribute is enabled for fields referenced in `index.routing_path`
:::

::::

::::{step} Create the time series data stream and add data
:anchor: create-tsds

After creating the index template, you can create a time series data stream by [indexing a document](use-data-stream.md#add-documents-to-a-data-stream). The TSDS is created automatically when you index the first document, as long as the index name matches the index template pattern. You can use a bulk API request or a POST request.

:::{important}
To test the following `_bulk` example, update the timestamps to within two hours of your current time. Data added to a TSDS must fit the [accepted time range](/manage-data/data-store/data-streams/time-bound-tsds.md#tsds-accepted-time-range).
:::

```console
PUT metrics-weather-sensors/_bulk
{ "create":{ } }
{ "@timestamp": "2099-05-06T16:21:15.000Z", "sensor_id": "SENSOR-001", "location": "warehouse-A", "temperature": 26.7,"humidity": 49.9 }
{ "create":{ } }
{ "@timestamp": "2099-05-06T16:25:42.000Z", "sensor_id": "SENSOR-002", "location": "warehouse-B", "temperature": 32.4, "humidity": 88.9 }
```

```console
POST metrics-weather-sensors/_doc
{
  "@timestamp": "2099-05-06T16:21:15.000Z",
  "sensor_id": "SENSOR-00002",
  "location": "warehouse-B",
  "temperature": 32.4,
  "humidity": 88.9
}
```
::::

::::{step} Verify setup
To make sure your time series data stream is working, try some GET requests.

View data stream details:

```console
GET _data_stream/metrics-prod 
```

Check the document count in a time series data stream:

```console
GET metrics-prod/_count 
```

Query the time series data:

```console
GET metrics-prod/_search 
{
  "size": 5,
  "sort": ["@timestamp"]
}
```


::::


## Advanced setup

### Convert an existing data stream to a TSDS [convert-existing-data-stream-to-tsds]

You can convert an existing regular data stream to a TSDS. Follow these steps:

1. Update your existing index template and component templates (if any) to include time series settings. For {{stack}}, configure lifecycle management. 
2. Use the [rollover API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover) to manually roll over the existing data stream's write index, to apply the changes you made in step 1:

```console
POST metrics-weather-sensors/_rollover
```

:::{note}
After the rollover, new backing indices will have time series functionality. Existing backing indices are not affected by the rollover (because their `index.mode` cannot be changed).
:::

### Secure a time series data stream [secure-tsds]

To control access to a TSDS, use [index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices). Privileges set on a TSDS also apply to the backing indices.

For an example, refer to [Data stream privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md#data-stream-privileges).

## Next steps [set-up-tsds-whats-next]

Now that you've set up a time series data stream, you can manage and use it like a regular data stream. For more information, refer to:

* [Use a data stream](use-data-stream.md) for indexing and searching
* [Change data stream settings](modify-data-stream.md#data-streams-change-mappings-and-settings) as needed
* Query time series data using the {{esql}} [`TS` command](elasticsearch://reference/query-languages/esql/commands/ts.md)
* Use [data stream APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-data-stream)
