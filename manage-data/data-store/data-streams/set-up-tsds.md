---
navigation_title: "Set up a TSDS"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/set-up-tsds.html
applies_to:
  stack: ga
  serverless: ga
---



# Set up a TSDS [set-up-tsds]


To set up a [time series data stream (TSDS)](../data-streams/time-series-data-stream-tsds.md), follow these steps:

1. Check the [prerequisites](#tsds-prereqs).
2. [Create an index lifecycle policy](#tsds-ilm-policy).
3. [Create an index template](#create-tsds-index-template).
4. [Create the TSDS](#create-tsds).
5. [Secure the TSDS](#secure-tsds).


## Prerequisites [tsds-prereqs]

* Before you create a TSDS, you should be familiar with [data streams](../data-streams.md) and [TSDS concepts](time-series-data-stream-tsds.md).
* To follow this tutorial, you must have the following permissions:

    * [Cluster privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-cluster): `manage_ilm` and `manage_index_templates`.
    * [Index privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices): `create_doc` and `create_index` for any TSDS you create or convert. To roll over a TSDS, you must have the `manage` privilege.



## Create an index lifecycle policy [tsds-ilm-policy]

While optional, we recommend using {{ilm-init}} to automate the management of your TSDS’s backing indices. {{ilm-init}} requires an index lifecycle policy.

We recommend you specify a `max_age` criteria for the `rollover` action in the policy. This ensures the [`@timestamp` ranges](time-series-data-stream-tsds.md#time-bound-indices) for the TSDS’s backing indices are consistent. For example, setting a `max_age` of `1d` for the `rollover` action ensures your backing indices consistently contain one day’s worth of data.

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
      },
      "warm": {
        "min_age": "30d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          }
        }
      },
      "cold": {
        "min_age": "60d",
        "actions": {
          "searchable_snapshot": {
            "snapshot_repository": "found-snapshots"
          }
        }
      },
      "frozen": {
        "min_age": "90d",
        "actions": {
          "searchable_snapshot": {
            "snapshot_repository": "found-snapshots"
          }
        }
      },
      "delete": {
        "min_age": "735d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```


## Create an index template [create-tsds-index-template]

To setup a TSDS create an index template with the following details:

* One or more index patterns that match the TSDS’s name. We recommend using our [data stream naming scheme](/reference/ingestion-tools/fleet/data-streams.md#data-streams-naming-scheme).
* Enable data streams.
* Specify a mapping that defines your dimensions and metrics:

    * One or more [dimension fields](time-series-data-stream-tsds.md#time-series-dimension) with a `time_series_dimension` value of `true`. Alternatively, one or more [pass-through](elasticsearch://reference/elasticsearch/mapping-reference/passthrough.md#passthrough-dimensions) fields configured as dimension containers, provided that they will contain at least one sub-field (mapped statically or dynamically).
    * One or more [metric fields](time-series-data-stream-tsds.md#time-series-metric), marked using the `time_series_metric` mapping parameter.
    * Optional: A `date` or `date_nanos` mapping for the `@timestamp` field. If you don’t specify a mapping, Elasticsearch maps `@timestamp` as a `date` field with default options.

* Define index settings:

    * Set `index.mode` setting to `time_series`.
    * Your lifecycle policy in the `index.lifecycle.name` index setting.
    * Optional: Other index settings, such as [`index.number_of_replicas`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#dynamic-index-number-of-replicas), for your TSDS’s backing indices.

* A priority higher than `200` to avoid collisions with built-in templates. See [Avoid index pattern collisions](../templates.md#avoid-index-pattern-collisions).
* Optional: Component templates containing your mappings and other index settings.

```console
PUT _index_template/my-weather-sensor-index-template
{
  "index_patterns": ["metrics-weather_sensors-*"],
  "data_stream": { },
  "template": {
    "settings": {
      "index.mode": "time_series",
      "index.lifecycle.name": "my-lifecycle-policy"
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
%  TEST[continued]


## Create the TSDS [create-tsds]

[Indexing requests](use-data-stream.md#add-documents-to-a-data-stream) add documents to a TSDS. Documents in a TSDS must include:

* A `@timestamp` field
* One or more dimension fields. At least one dimension must match the `index.routing_path` index setting, if specified. If not specified explicitly, `index.routing_path` is set automatically to whichever mappings have `time_series_dimension` set to `true`.

To automatically create your TSDS, submit an indexing request that targets the TSDS’s name. This name must match one of your index template’s index patterns.

::::{important}
To test the following example, update the timestamps to within three hours of your current time. Data added to a TSDS must always fall within an [accepted time range](time-series-data-stream-tsds.md#tsds-accepted-time-range).
::::


```console
PUT metrics-weather_sensors-dev/_bulk
{ "create":{ } }
{ "@timestamp": "2099-05-06T16:21:15.000Z", "sensor_id": "HAL-000001", "location": "plains", "temperature": 26.7,"humidity": 49.9 }
{ "create":{ } }
{ "@timestamp": "2099-05-06T16:25:42.000Z", "sensor_id": "SYKENET-000001", "location": "swamp", "temperature": 32.4, "humidity": 88.9 }

POST metrics-weather_sensors-dev/_doc
{
  "@timestamp": "2099-05-06T16:21:15.000Z",
  "sensor_id": "SYKENET-000001",
  "location": "swamp",
  "temperature": 32.4,
  "humidity": 88.9
}
```
%  TEST[skip: The @timestamp value won’t match an accepted range in the TSDS]

You can also manually create the TSDS using the [create data stream API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create-data-stream). The TSDS’s name must still match one of your template’s index patterns.

```console
PUT _data_stream/metrics-weather_sensors-dev
```
%  TEST[setup:tsds_template]
%  TEST[teardown:tsds_cleanup]


## Secure the TSDS [secure-tsds]

Use [index privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices) to control access to a TSDS. Granting privileges on a TSDS grants the same privileges on its backing indices.

For an example, refer to [Data stream privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md#data-stream-privileges).


## Convert an existing data stream to a TSDS [convert-existing-data-stream-to-tsds]

You can also use the above steps to convert an existing regular data stream to a TSDS. In this case, you’ll want to:

* Edit your existing index lifecycle policy, component templates, and index templates instead of creating new ones.
* Instead of creating the TSDS, manually roll over its write index. This ensures the current write index and any new backing indices have an [`index.mode` of `time_series`](time-series-data-stream-tsds.md#time-series-mode).

    You can manually roll over the write index using the [rollover API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover).

    ```console
    POST metrics-weather_sensors-dev/_rollover
    ```



## A note about component templates and index.mode setting [set-up-component-templates]

Configuring a TSDS via an index template that uses component templates is a bit more complicated. Typically with component templates mappings and settings get scattered across multiple component templates. If the `index.routing_path` is defined, the fields it references need to be defined in the same component template with the `time_series_dimension` attribute enabled.

The reasons for this is that each component template needs to be valid on its own. When configuring the `index.mode` setting in an index template, the `index.routing_path` setting is configured automatically. It is derived from the field mappings with `time_series_dimension` attribute enabled.


## What’s next? [set-up-tsds-whats-next]

Now that you’ve set up your TSDS, you can manage and use it like a regular data stream. For more information, refer to:

* [*Use a data stream*](use-data-stream.md)
* [Change mappings and settings for a data stream](modify-data-stream.md#data-streams-change-mappings-and-settings)
* [data stream APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-data-stream)

