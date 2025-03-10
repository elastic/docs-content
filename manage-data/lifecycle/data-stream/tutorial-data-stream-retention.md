---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tutorial-manage-data-stream-retention.html
applies_to:
  stack: ga
  serverless: ga
---

# Tutorial: Data stream retention [tutorial-manage-data-stream-retention]

In this tutorial, we are going to go over the data stream lifecycle retention; we will define it, go over how it can be configured and how it can gets applied. Keep in mind, the following options apply only to data streams that are managed by the data stream lifecycle.

1. [What is data stream retention?](#what-is-retention)
2. [How to configure retention?](#retention-configuration)
3. [How is the effective retention calculated?](#effective-retention-calculation)
4. [How is the effective retention applied?](#effective-retention-application)

You can verify if a data steam is managed by the data stream lifecycle via the [get data stream lifecycle API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-data-lifecycle):

```console
GET _data_stream/my-data-stream/_lifecycle
```
%  TEST[continued]

The result should look like this:

```console-result
{
  "data_streams": [
    {
      "name": "my-data-stream",                                   <1>
      "lifecycle": {
        "enabled": true                                           <2>
      }
    }
  ]
}
```
%  TESTRESPONSE[skip:the result is for illustrating purposes only]

1. The name of your data stream.
2. Ensure that the lifecycle is enabled, meaning this should be `true`.



## What is data stream retention? [what-is-retention]

We define retention as the least amount of time the data of a data stream are going to be kept in {{es}}. After this time period has passed, {{es}} is allowed to remove these data to free up space and/or manage costs.

::::{note}
Retention does not define the period that the data will be removed, but the minimum time period they will be kept.
::::


We define 4 different types of retention:

* The data stream retention, or `data_retention`, which is the retention configured on the data stream level. It can be set via an [index template](../../data-store/templates.md) for future data streams or via the [PUT data stream lifecycle API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-data-lifecycle) for an existing data stream. When the data stream retention is not set, it implies that the data need to be kept forever.
* The global default retention, let’s call it `default_retention`, which is a retention configured via the cluster setting [`data_streams.lifecycle.retention.default`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-retention-default) and will be applied to all data streams managed by data stream lifecycle that do not have `data_retention` configured. Effectively, it ensures that there will be no data streams keeping their data forever. This can be set via the [update cluster settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings).
* The global max retention, let’s call it `max_retention`, which is a retention configured via the cluster setting [`data_streams.lifecycle.retention.max`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-retention-max) and will be applied to all data streams managed by data stream lifecycle. Effectively, it ensures that there will be no data streams whose retention will exceed this time period. This can be set via the [update cluster settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings).
* The effective retention, or `effective_retention`, which is the retention applied at a data stream on a given moment. Effective retention cannot be set, it is derived by taking into account all the configured retention listed above and is calculated as it is described [here](#effective-retention-calculation).

::::{note}
Global default and max retention do not apply to data streams internal to elastic. Internal data streams are recognised either by having the `system` flag set to `true` or if their name is prefixed with a dot (`.`).
::::



## How to configure retention? [retention-configuration]

* By setting the `data_retention` on the data stream level. This retention can be configured in two ways:

     — For new data streams, it can be defined in the index template that would be applied during the data stream’s creation. You can use the [create index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template), for example:

    ```console
    PUT _index_template/template
    {
      "index_patterns": ["my-data-stream*"],
      "data_stream": { },
      "priority": 500,
      "template": {
        "lifecycle": {
          "data_retention": "7d"
        }
      },
      "_meta": {
        "description": "Template with data stream lifecycle"
      }
    }
    ```

     — For an existing data stream, it can be set via the [PUT lifecycle API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-data-lifecycle).

    ```console
    PUT _data_stream/my-data-stream/_lifecycle
    {
      "data_retention": "30d" <1>
    }
    ```

    1. The retention period of this data stream is set to 30 days.

* By setting the global retention via the `data_streams.lifecycle.retention.default` and/or `data_streams.lifecycle.retention.max` that are set on a cluster level. You can be set via the [update cluster settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). For example:

    ```console
    PUT /_cluster/settings
    {
      "persistent" : {
        "data_streams.lifecycle.retention.default" : "7d",
        "data_streams.lifecycle.retention.max" : "90d"
      }
    }
    ```



## How is the effective retention calculated? [effective-retention-calculation]

The effective is calculated in the following way:

* The `effective_retention` is the `default_retention`, when `default_retention` is defined and the data stream does not have `data_retention`.
* The `effective_retention` is the `data_retention`, when `data_retention` is defined and if `max_retention` is defined, it is less than the `max_retention`.
* The `effective_retention` is the `max_retention`, when `max_retention` is defined, and the data stream has either no `data_retention` or its `data_retention` is greater than the `max_retention`.

The above is demonstrated in the examples below:

| `default_retention` | `max_retention` | `data_retention` | `effective_retention` | Retention determined by |
| --- | --- | --- | --- | --- |
| Not set | Not set | Not set | Infinite | N/A |
| Not relevant | 12 months | **30 days** | 30 days | `data_retention` |
| Not relevant | Not set | **30 days** | 30 days | `data_retention` |
| **30 days** | 12 months | Not set | 30 days | `default_retention` |
| **30 days** | 30 days | Not set | 30 days | `default_retention` |
| Not relevant | **30 days** | 12 months | 30 days | `max_retention` |
| Not set | **30 days** | Not set | 30 days | `max_retention` |

Considering our example, if we retrieve the lifecycle of `my-data-stream`:

```console
GET _data_stream/my-data-stream/_lifecycle
```
%  TEST[continued]

We see that it will remain the same with what the user configured:

```console-result
{
  "global_retention" : {
    "max_retention" : "90d",                                   <1>
    "default_retention" : "7d"                                 <2>
  },
  "data_streams": [
    {
      "name": "my-data-stream",
      "lifecycle": {
        "enabled": true,
        "data_retention": "30d",                                <3>
        "effective_retention": "30d",                           <4>
        "retention_determined_by": "data_stream_configuration"  <5>
      }
    }
  ]
}
```

1. The maximum retention configured in the cluster.
2. The default retention configured in the cluster.
3. The requested retention for this data stream.
4. The retention that is applied by the data stream lifecycle on this data stream.
5. The configuration that determined the effective retention. In this case it’s the `data_configuration` because it is less than the `max_retention`.



## How is the effective retention applied? [effective-retention-application]

Retention is applied to the remaining backing indices of a data stream as the last step of [a data stream lifecycle run](../data-stream.md#data-streams-lifecycle-how-it-works). Data stream lifecycle will retrieve the backing indices whose `generation_time` is longer than the effective retention period and delete them. The `generation_time` is only applicable to rolled over backing indices and it is either the time since the backing index got rolled over, or the time optionally configured in the [`index.lifecycle.origination_date`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-data-stream-lifecycle-origination-date) setting.

::::{important}
We use the `generation_time` instead of the creation time because this ensures that all data in the backing index have passed the retention period. As a result, the retention period is not the exact time data get deleted, but the minimum time data will be stored.
::::
