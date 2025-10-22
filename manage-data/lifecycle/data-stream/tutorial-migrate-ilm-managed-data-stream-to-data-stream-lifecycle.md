---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tutorial-migrate-data-stream-from-ilm-to-dsl.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Tutorial: Migrate ILM managed data stream to data stream lifecycle [tutorial-migrate-data-stream-from-ilm-to-dsl]

In this tutorial we’ll look at migrating an existing data stream from [Index Lifecycle Management ({{ilm-init}})](../index-lifecycle-management.md) to [data stream lifecycle](../data-stream.md). The existing {{ilm-init}} managed backing indices will continue to be managed by {{ilm-init}} until they age out and get deleted by {{ilm-init}}; however, the new backing indices will be managed by data stream lifecycle. This way, a data stream is gradually migrated away from being managed by {{ilm-init}} to being managed by data stream lifecycle. As we’ll see, {{ilm-init}} and data stream lifecycle can co-manage a data stream; however, an index can only be managed by one system at a time.


:::{admonition} Configure data retention policies for Streams
:applies_to: {"stack": "ga 9.2, preview 9.1", "serverless": "ga"}

Starting with {{stack}} version 9.2, [Streams](/solutions/observability/streams/streams.md) provides a centralized interface for common data management tasks in {{kib}}, including tasks such as configuring data retention policies. You can choose to retain your data indefinitely, for a custom period, or by following an existing ILM policy. For more information, refer to [Manage data retention in Streams](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md#data-retention-streams).

:::

To migrate a data stream from {{ilm-init}} to data stream lifecycle using APIs you need to run two steps:

1. Update the index template that’s backing the data stream to set [prefer_ilm](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm) to `false`, and to configure data stream lifecycle.
2. Configure the data stream lifecycle for the *existing* data stream using the [lifecycle API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-data-lifecycle).

For more details see the [migrate to data stream lifecycle](#migrate-from-ilm-to-dsl) section.


## Setup ILM managed data stream [setup-test-data]

Let’s first create a data stream with two backing indices managed by {{ilm-init}}. We first create an {{ilm-init}} policy:

```console
PUT _ilm/policy/pre-dsl-ilm-policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_primary_shard_size": "50gb"
          }
        }
      },
      "delete": {
        "min_age": "7d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

And let’s create an index template that’ll back the data stream and configures {{ilm-init}}:

```console
PUT _index_template/dsl-data-stream-template
{
  "index_patterns": ["dsl-data-stream*"],
  "data_stream": { },
  "priority": 500,
  "template": {
    "settings": {
      "index.lifecycle.name": "pre-dsl-ilm-policy"
    }
  }
}
```

We’ll now index a document targetting `dsl-data-stream` to create the data stream and we’ll also manually rollover the data stream to have another generation index created:

```console
POST dsl-data-stream/_doc?
{
  "@timestamp": "2023-10-18T16:21:15.000Z",
  "message": "192.0.2.42 - - [06/May/2099:16:21:15 +0000] \"GET /images/bg.jpg HTTP/1.0\" 200 24736"
}
```

```console
POST dsl-data-stream/_rollover
```

We’ll use the [GET _data_stream](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-data-stream) API to inspect the state of the data stream:

```console
GET _data_stream/dsl-data-stream
```

Inspecting the response we’ll see that both backing indices are managed by {{ilm-init}} and that the next generation index will also be managed by {{ilm-init}}:

```console-result
{
  "data_streams": [
    {
      "name": "dsl-data-stream",
      "timestamp_field": {
        "name": "@timestamp"
      },
      "indices": [
        {
          "index_name": ".ds-dsl-data-stream-2023.10.19-000001",    <1>
          "index_uuid": "xCEhwsp8Tey0-FLNFYVwSg",
          "prefer_ilm": true,                                       <2>
          "ilm_policy": "pre-dsl-ilm-policy",                       <3>
          "managed_by": "Index Lifecycle Management"                <4>
        },
        {
          "index_name": ".ds-dsl-data-stream-2023.10.19-000002",
          "index_uuid": "PA_JquKGSiKcAKBA8DJ5gw",
          "prefer_ilm": true,
          "ilm_policy": "pre-dsl-ilm-policy",
          "managed_by": "Index Lifecycle Management"
        }
      ],
      "generation": 2,
      "status": "GREEN",
      "template": "dsl-data-stream-template",
      "next_generation_managed_by": "Index Lifecycle Management",   <5>
      "prefer_ilm": true,                                           <6>
      "ilm_policy": "pre-dsl-ilm-policy",                           <7>
      "hidden": false,
      "system": false,
      "allow_custom_routing": false,
      "replicated": false,
      "rollover_on_write": false
    }
  ]
}
```

1. The name of the backing index.
2. For each backing index we display the value of the [prefer_ilm](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm) configuration which will indicate if {{ilm-init}} takes precedence over data stream lifecycle in case both systems are configured for an index.
3. The {{ilm-init}} policy configured for this index.
4. The system that manages this index (possible values are "Index Lifecycle Management", "Data stream lifecycle", or "Unmanaged")
5. The system that will manage the next generation index (the new write index of this data stream, once the data stream is rolled over). The possible values are "Index Lifecycle Management", "Data stream lifecycle", or "Unmanaged".
6. The [prefer_ilm](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm) value configured in the index template that’s backing the data stream. This value will be configured for all the new backing indices. If it’s not configured in the index template the backing indices will receive the `true` default value ({{ilm-init}} takes precedence over data stream lifecycle by default as it’s currently richer in features).
7. The {{ilm-init}} policy configured in the index template that’s backing this data stream (which will be configured on all the new backing indices, as long as it exists in the index template).



## Migrate data stream to data stream lifecycle [migrate-from-ilm-to-dsl]

To migrate the `dsl-data-stream` to data stream lifecycle we’ll have to execute two steps:

1. Update the index template that’s backing the data stream to set [prefer_ilm](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm) to `false`, and to configure data stream lifecycle.
2. Configure the data stream lifecycle for the *existing* `dsl-data-stream` using the [lifecycle API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-data-lifecycle).

::::{important}
The data stream lifecycle configuration that’s added to the index template, being a data stream configuration, will only apply to **new** data streams. Our data stream exists already, so even though we added a data stream lifecycle configuration in the index template it will not be applied to `dsl-data-stream`.
::::


$$$update-index-template-for-dsl$$$
Let’s update the index template:

```console
PUT _index_template/dsl-data-stream-template
{
  "index_patterns": ["dsl-data-stream*"],
  "data_stream": { },
  "priority": 500,
  "template": {
    "settings": {
      "index.lifecycle.name": "pre-dsl-ilm-policy",
      "index.lifecycle.prefer_ilm": false             <1>
    },
    "lifecycle": {
      "data_retention": "7d"                          <2>
    }
  }
}
```

1. The `prefer_ilm` setting will now be configured on the **new** backing indices (created by rolling over the data stream) such that {{ilm-init}} does *not* take precedence over data stream lifecycle.
2. We’re configuring the data stream lifecycle so *new* data streams will be managed by data stream lifecycle.


We’ve now made sure that new data streams will be managed by data stream lifecycle.

Let’s update our existing `dsl-data-stream` and configure data stream lifecycle:

```console
PUT _data_stream/dsl-data-stream/_lifecycle
{
    "data_retention": "7d"
}
```

We can inspect the data stream to check that the next generation will indeed be managed by data stream lifecycle:

```console
GET _data_stream/dsl-data-stream
```

```console-result
{
  "data_streams": [
    {
      "name": "dsl-data-stream",
      "timestamp_field": {
        "name": "@timestamp"
      },
      "indices": [
        {
          "index_name": ".ds-dsl-data-stream-2023.10.19-000001",
          "index_uuid": "xCEhwsp8Tey0-FLNFYVwSg",
          "prefer_ilm": true,
          "ilm_policy": "pre-dsl-ilm-policy",
          "managed_by": "Index Lifecycle Management"                <1>
        },
        {
          "index_name": ".ds-dsl-data-stream-2023.10.19-000002",
          "index_uuid": "PA_JquKGSiKcAKBA8DJ5gw",
          "prefer_ilm": true,
          "ilm_policy": "pre-dsl-ilm-policy",
          "managed_by": "Index Lifecycle Management"                <2>
        }
      ],
      "generation": 2,
      "status": "GREEN",
      "template": "dsl-data-stream-template",
      "lifecycle": {
        "enabled": true,
        "data_retention": "7d",
        "effective_retention": "7d",
        "retention_determined_by": "data_stream_configuration"
      },
      "ilm_policy": "pre-dsl-ilm-policy",
      "next_generation_managed_by": "Data stream lifecycle",         <3>
      "prefer_ilm": false,                                           <4>
      "hidden": false,
      "system": false,
      "allow_custom_routing": false,
      "replicated": false,
      "rollover_on_write": false
    }
  ]
}
```

1. The existing backing index will continue to be managed by {{ilm-init}}
2. The existing backing index will continue to be managed by {{ilm-init}}
3. The next generation index will be managed by Data stream lifecycle
4. The `prefer_ilm` setting value we configured in the index template is reflected and will be configured accordingly for new backing indices.


We’ll now rollover the data stream to see the new generation index being managed by data stream lifecycle:

```console
POST dsl-data-stream/_rollover
```

```console
GET _data_stream/dsl-data-stream
```

```console-result
{
  "data_streams": [
    {
      "name": "dsl-data-stream",
      "timestamp_field": {
        "name": "@timestamp"
      },
      "indices": [
        {
          "index_name": ".ds-dsl-data-stream-2023.10.19-000001",
          "index_uuid": "xCEhwsp8Tey0-FLNFYVwSg",
          "prefer_ilm": true,
          "ilm_policy": "pre-dsl-ilm-policy",
          "managed_by": "Index Lifecycle Management"                <1>
        },
        {
          "index_name": ".ds-dsl-data-stream-2023.10.19-000002",
          "index_uuid": "PA_JquKGSiKcAKBA8DJ5gw",
          "prefer_ilm": true,
          "ilm_policy": "pre-dsl-ilm-policy",
          "managed_by": "Index Lifecycle Management"                <2>
        },
        {
          "index_name": ".ds-dsl-data-stream-2023.10.19-000003",
          "index_uuid": "PA_JquKGSiKcAKBA8abcd1",
          "prefer_ilm": false,                                      <3>
          "ilm_policy": "pre-dsl-ilm-policy",
          "managed_by": "Data stream lifecycle"                     <4>
        }
      ],
      "generation": 3,
      "status": "GREEN",
      "template": "dsl-data-stream-template",
      "lifecycle": {
        "enabled": true,
        "data_retention": "7d",
        "effective_retention": "7d",
        "retention_determined_by": "data_stream_configuration"
      },
      "ilm_policy": "pre-dsl-ilm-policy",
      "next_generation_managed_by": "Data stream lifecycle",
      "prefer_ilm": false,
      "hidden": false,
      "system": false,
      "allow_custom_routing": false,
      "replicated": false,
      "rollover_on_write": false
    }
  ]
}
```

1. The backing indices that existed before rollover will continue to be managed by {{ilm-init}}
2. The backing indices that existed before rollover will continue to be managed by {{ilm-init}}
3. The new write index received the `false` value for the `prefer_ilm` setting, as we configured in the index template
4. The new write index is managed by `Data stream lifecycle`

## Migrate data stream back to ILM [migrate-from-dsl-to-ilm]

We can easily change this data stream to be managed by {{ilm-init}} because we didn’t remove the {{ilm-init}} policy when we [updated the index template](#update-index-template-for-dsl).

We can achieve this in two ways:

1. [Delete the lifecycle](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete-data-lifecycle) from the data streams
2. Disable data stream lifecycle by configuring the `enabled` flag to `false`.

Let’s implement option 2 and disable the data stream lifecycle:

```console
PUT _data_stream/dsl-data-stream/_lifecycle
{
    "data_retention": "7d",
    "enabled": false <1>
}
```

1. The `enabled` flag can be omitted and defaults to `true` however, here we explicitly configure it to `false` Let’s check the state of the data stream:


```console
GET _data_stream/dsl-data-stream
```

```console-result
{
  "data_streams": [
    {
      "name": "dsl-data-stream",
      "timestamp_field": {
        "name": "@timestamp"
      },
      "indices": [
        {
          "index_name": ".ds-dsl-data-stream-2023.10.19-000001",
          "index_uuid": "xCEhwsp8Tey0-FLNFYVwSg",
          "prefer_ilm": true,
          "ilm_policy": "pre-dsl-ilm-policy",
          "managed_by": "Index Lifecycle Management"
        },
        {
          "index_name": ".ds-dsl-data-stream-2023.10.19-000002",
          "index_uuid": "PA_JquKGSiKcAKBA8DJ5gw",
          "prefer_ilm": true,
          "ilm_policy": "pre-dsl-ilm-policy",
          "managed_by": "Index Lifecycle Management"
        },
        {
          "index_name": ".ds-dsl-data-stream-2023.10.19-000003",
          "index_uuid": "PA_JquKGSiKcAKBA8abcd1",
          "prefer_ilm": false,
          "ilm_policy": "pre-dsl-ilm-policy",
          "managed_by": "Index Lifecycle Management"                <1>
        }
      ],
      "generation": 3,
      "status": "GREEN",
      "template": "dsl-data-stream-template",
      "lifecycle": {
        "enabled": false,                                          <2>
        "data_retention": "7d"
      },
      "ilm_policy": "pre-dsl-ilm-policy",
      "next_generation_managed_by": "Index Lifecycle Management",  <3>
      "prefer_ilm": false,
      "hidden": false,
      "system": false,
      "allow_custom_routing": false,
      "replicated": false,
      "rollover_on_write": false
    }
  ]
}
```

1. The write index is now managed by {{ilm-init}}
2. The `lifecycle` configured on the data stream is now disabled.
3. The next write index will be managed by {{ilm-init}}


Had we removed the {{ilm-init}} policy from the index template when we [updated](#update-index-template-for-dsl) it, the write index of the data stream will now be `Unmanaged` because the index wouldn’t have the {{ilm-init}} policy configured to fallback onto.
