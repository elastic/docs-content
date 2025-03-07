---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modify-data-streams.html
applies_to:
  stack: ga
  serverless: ga
---

# Modify a data stream [modify-data-streams]


## Change mappings and settings for a data stream [data-streams-change-mappings-and-settings]

Each [data stream](../data-streams.md) has a [matching index template](../data-streams/set-up-data-stream.md#create-index-template). Mappings and index settings from this template are applied to new backing indices created for the stream. This includes the stream’s first backing index, which is auto-generated when the stream is created.

Before creating a data stream, we recommend you carefully consider which mappings and settings to include in this template.

If you later need to change the mappings or settings for a data stream, you have a few options:

* [Add a new field mapping to a data stream](../data-streams/modify-data-stream.md#add-new-field-mapping-to-a-data-stream)
* [Change an existing field mapping in a data stream](../data-streams/modify-data-stream.md#change-existing-field-mapping-in-a-data-stream)
* [Change a dynamic index setting for a data stream](../data-streams/modify-data-stream.md#change-dynamic-index-setting-for-a-data-stream)
* [Change a static index setting for a data stream](../data-streams/modify-data-stream.md#change-static-index-setting-for-a-data-stream)

::::{tip}
If your changes include modifications to existing field mappings or [static index settings](elasticsearch://reference/elasticsearch/index-settings/index.md), a reindex is often required to apply the changes to a data stream’s backing indices. If you are already performing a reindex, you can use the same process to add new field mappings and change [dynamic index settings](elasticsearch://reference/elasticsearch/index-settings/index.md). See [Use reindex to change mappings or settings](../data-streams/modify-data-stream.md#data-streams-use-reindex-to-change-mappings-settings).
::::



### Add a new field mapping to a data stream [add-new-field-mapping-to-a-data-stream]

To add a mapping for a new field to a data stream, following these steps:

1. Update the index template used by the data stream. This ensures the new field mapping is added to future backing indices created for the stream.

    For example, `my-data-stream-template` is an existing index template used by `my-data-stream`.

    The following [create or update index template](../templates.md) request adds a mapping for a new field, `message`, to the template.

    ```console
    PUT /_index_template/my-data-stream-template
    {
      "index_patterns": [ "my-data-stream*" ],
      "data_stream": { },
      "priority": 500,
      "template": {
        "mappings": {
          "properties": {
            "message": {                              <1>
              "type": "text"
            }
          }
        }
      }
    }
    ```

    1. Adds a mapping for the new `message` field.

2. Use the [update mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-mapping) to add the new field mapping to the data stream. By default, this adds the mapping to the stream’s existing backing indices, including the write index.

    The following update mapping API request adds the new `message` field mapping to `my-data-stream`.

    ```console
    PUT /my-data-stream/_mapping
    {
      "properties": {
        "message": {
          "type": "text"
        }
      }
    }
    ```

    To add the mapping only to the stream’s write index, set the update mapping API’s `write_index_only` query parameter to `true`.

    The following update mapping request adds the new `message` field mapping only to `my-data-stream`'s write index. The new field mapping is not added to the stream’s other backing indices.

    ```console
    PUT /my-data-stream/_mapping?write_index_only=true
    {
      "properties": {
        "message": {
          "type": "text"
        }
      }
    }
    ```



### Change an existing field mapping in a data stream [change-existing-field-mapping-in-a-data-stream]

The documentation for each [mapping parameter](elasticsearch://reference/elasticsearch/mapping-reference/mapping-parameters.md) indicates whether you can update it for an existing field using the [update mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-mapping). To update these parameters for an existing field, follow these steps:

1. Update the index template used by the data stream. This ensures the updated field mapping is added to future backing indices created for the stream.

    For example, `my-data-stream-template` is an existing index template used by `my-data-stream`.

    The following [create or update index template](../templates.md) request changes the argument for the `host.ip` field’s [`ignore_malformed`](elasticsearch://reference/elasticsearch/mapping-reference/ignore-malformed.md) mapping parameter to `true`.

    ```console
    PUT /_index_template/my-data-stream-template
    {
      "index_patterns": [ "my-data-stream*" ],
      "data_stream": { },
      "priority": 500,
      "template": {
        "mappings": {
          "properties": {
            "host": {
              "properties": {
                "ip": {
                  "type": "ip",
                  "ignore_malformed": true            <1>
                }
              }
            }
          }
        }
      }
    }
    ```

    1. Changes the `host.ip` field’s `ignore_malformed` value to `true`.

2. Use the [update mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-mapping) to apply the mapping changes to the data stream. By default, this applies the changes to the stream’s existing backing indices, including the write index.

    The following [update mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-mapping) request targets `my-data-stream`. The request changes the argument for the `host.ip` field’s `ignore_malformed` mapping parameter to `true`.

    ```console
    PUT /my-data-stream/_mapping
    {
      "properties": {
        "host": {
          "properties": {
            "ip": {
              "type": "ip",
              "ignore_malformed": true
            }
          }
        }
      }
    }
    ```

    To apply the mapping changes only to the stream’s write index, set the put mapping API’s `write_index_only` query parameter to `true`.

    The following update mapping request changes the `host.ip` field’s mapping only for `my-data-stream`'s write index. The change is not applied to the stream’s other backing indices.

    ```console
    PUT /my-data-stream/_mapping?write_index_only=true
    {
      "properties": {
        "host": {
          "properties": {
            "ip": {
              "type": "ip",
              "ignore_malformed": true
            }
          }
        }
      }
    }
    ```


Except for supported mapping parameters, we don’t recommend you change the mapping or field data type of existing fields, even in a data stream’s matching index template or its backing indices. Changing the mapping of an existing field could invalidate any data that’s already indexed.

If you need to change the mapping of an existing field, create a new data stream and reindex your data into it. See [Use reindex to change mappings or settings](../data-streams/modify-data-stream.md#data-streams-use-reindex-to-change-mappings-settings).


### Change a dynamic index setting for a data stream [change-dynamic-index-setting-for-a-data-stream]

To change a [dynamic index setting](elasticsearch://reference/elasticsearch/index-settings/index.md) for a data stream, follow these steps:

1. Update the index template used by the data stream. This ensures the setting is applied to future backing indices created for the stream.

    For example, `my-data-stream-template` is an existing index template used by `my-data-stream`.

    The following [create or update index template](../templates.md) request changes the template’s `index.refresh_interval` index setting to `30s` (30 seconds).

    ```console
    PUT /_index_template/my-data-stream-template
    {
      "index_patterns": [ "my-data-stream*" ],
      "data_stream": { },
      "priority": 500,
      "template": {
        "settings": {
          "index.refresh_interval": "30s"             <1>
        }
      }
    }
    ```

    1. Changes the `index.refresh_interval` setting to `30s` (30 seconds).

2. Use the [update index settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) to update the index setting for the data stream. By default, this applies the setting to the stream’s existing backing indices, including the write index.

    The following update index settings API request updates the `index.refresh_interval` setting for `my-data-stream`.

    ```console
    PUT /my-data-stream/_settings
    {
      "index": {
        "refresh_interval": "30s"
      }
    }
    ```


::::{important}
To change the `index.lifecycle.name` setting, first use the [remove policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-remove-policy) to remove the existing {{ilm-init}} policy. See [Switch lifecycle policies](../../lifecycle/index-lifecycle-management/configure-lifecycle-policy.md#switch-lifecycle-policies).
::::



### Change a static index setting for a data stream [change-static-index-setting-for-a-data-stream]

[Static index settings](elasticsearch://reference/elasticsearch/index-settings/index.md) can only be set when a backing index is created. You cannot update static index settings using the [update index settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings).

To apply a new static setting to future backing indices, update the index template used by the data stream. The setting is automatically applied to any backing index created after the update.

For example, `my-data-stream-template` is an existing index template used by `my-data-stream`.

The following [create or update index template API](../templates.md) requests adds new `sort.field` and `sort.order index` settings to the template.

```console
PUT /_index_template/my-data-stream-template
{
  "index_patterns": [ "my-data-stream*" ],
  "data_stream": { },
  "priority": 500,
  "template": {
    "settings": {
      "sort.field": [ "@timestamp"],             <1>
      "sort.order": [ "desc"]                    <2>
    }
  }
}
```

1. Adds the `sort.field` index setting.
2. Adds the `sort.order` index setting.


If wanted, you can [roll over the data stream](../data-streams/use-data-stream.md#manually-roll-over-a-data-stream) to immediately apply the setting to the data stream’s write index. This affects any new data added to the stream after the rollover. However, it does not affect the data stream’s existing backing indices or existing data.

To apply static setting changes to existing backing indices, you must create a new data stream and reindex your data into it. See [Use reindex to change mappings or settings](../data-streams/modify-data-stream.md#data-streams-use-reindex-to-change-mappings-settings).


### Use reindex to change mappings or settings [data-streams-use-reindex-to-change-mappings-settings]

You can use a reindex to change the mappings or settings of a data stream. This is often required to change the data type of an existing field or update static index settings for backing indices.

To reindex a data stream, first create or update an index template so that it contains the wanted mapping or setting changes. You can then reindex the existing data stream into a new stream matching the template. This applies the mapping and setting changes in the template to each document and backing index added to the new data stream. These changes also affect any future backing index created by the new stream.

Follow these steps:

1. Choose a name or index pattern for a new data stream. This new data stream will contain data from your existing stream.

    You can use the resolve index API to check if the name or pattern matches any existing indices, aliases, or data streams. If so, you should consider using another name or pattern.

    The following resolve index API request checks for any existing indices, aliases, or data streams that start with `new-data-stream`. If not, the `new-data-stream*` index pattern can be used to create a new data stream.

    ```console
    GET /_resolve/index/new-data-stream*
    ```

    The API returns the following response, indicating no existing targets match this pattern.

    ```console-result
    {
      "indices": [ ],
      "aliases": [ ],
      "data_streams": [ ]
    }
    ```

2. Create or update an index template. This template should contain the mappings and settings you’d like to apply to the new data stream’s backing indices.

    This index template must meet the [requirements for a data stream template](../data-streams/set-up-data-stream.md#create-index-template). It should also contain your previously chosen name or index pattern in the `index_patterns` property.

    ::::{tip}
    If you are only adding or changing a few things, we recommend you create a new template by copying an existing one and modifying it as needed.
    ::::


    For example, `my-data-stream-template` is an existing index template used by `my-data-stream`.

    The following [create or update index template API](../templates.md) request creates a new index template, `new-data-stream-template`. `new-data-stream-template` uses `my-data-stream-template` as its basis, with the following changes:

    * The index pattern in `index_patterns` matches any index or data stream starting with `new-data-stream`.
    * The `@timestamp` field mapping uses the `date_nanos` field data type rather than the `date` data type.
    * The template includes `sort.field` and `sort.order` index settings, which were not in the original `my-data-stream-template` template.

    ```console
    PUT /_index_template/new-data-stream-template
    {
      "index_patterns": [ "new-data-stream*" ],
      "data_stream": { },
      "priority": 500,
      "template": {
        "mappings": {
          "properties": {
            "@timestamp": {
              "type": "date_nanos"                 <1>
            }
          }
        },
        "settings": {
          "sort.field": [ "@timestamp"],          <2>
          "sort.order": [ "desc"]                 <3>
        }
      }
    }
    ```

    1. Changes the `@timestamp` field mapping to the `date_nanos` field data type.
    2. Adds the `sort.field` index setting.
    3. Adds the `sort.order` index setting.

3. Use the [create data stream API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create-data-stream) to manually create the new data stream. The name of the data stream must match the index pattern defined in the new template’s `index_patterns` property.

    We do not recommend [indexing new data to create this data stream](../data-streams/set-up-data-stream.md#create-data-stream). Later, you will reindex older data from an existing data stream into this new stream. This could result in one or more backing indices that contains a mix of new and old data.

    ::::{important}
    $$$data-stream-mix-new-old-data$$$
    **Mixing new and old data in a data stream**

    While mixing new and old data is safe, it could interfere with data retention. If you delete older indices, you could accidentally delete a backing index that contains both new and old data. To prevent premature data loss, you would need to retain such a backing index until you are ready to delete its newest data.

    ::::


    The following create data stream API request targets `new-data-stream`, which matches the index pattern for `new-data-stream-template`. Because no existing index or data stream uses this name, this request creates the `new-data-stream` data stream.

    ```console
    PUT /_data_stream/new-data-stream
    ```
    %  TEST[s/new-data-stream/new-data-stream-two/]

4. If you do not want to mix new and old data in your new data stream, pause the indexing of new documents. While mixing old and new data is safe, it could interfere with data retention. See [Mixing new and old data in a data stream](../data-streams/modify-data-stream.md#data-stream-mix-new-old-data).
5. If you use {{ilm-init}} to [automate rollover](../../lifecycle/index-lifecycle-management/tutorial-automate-rollover.md), reduce the {{ilm-init}} poll interval. This ensures the current write index doesn’t grow too large while waiting for the rollover check. By default, {{ilm-init}} checks rollover conditions every 10 minutes.

    The following [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) request lowers the `indices.lifecycle.poll_interval` setting to `1m` (one minute).

    ```console
    PUT /_cluster/settings
    {
      "persistent": {
        "indices.lifecycle.poll_interval": "1m"
      }
    }
    ```

6. Reindex your data to the new data stream using an `op_type` of `create`.

    If you want to partition the data in the order in which it was originally indexed, you can run separate reindex requests. These reindex requests can use individual backing indices as the source. You can use the [get data stream API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-data-stream) to retrieve a list of backing indices.

    For example, you plan to reindex data from `my-data-stream` into `new-data-stream`. However, you want to submit a separate reindex request for each backing index in `my-data-stream`, starting with the oldest backing index. This preserves the order in which the data was originally indexed.

    The following get data stream API request retrieves information about `my-data-stream`, including a list of its backing indices.

    ```console
    GET /_data_stream/my-data-stream
    ```

    The response’s `indices` property contains an array of the stream’s current backing indices. The first item in the array contains information about the stream’s oldest backing index.

    ```console-result
    {
      "data_streams": [
        {
          "name": "my-data-stream",
          "timestamp_field": {
            "name": "@timestamp"
          },
          "indices": [
            {
              "index_name": ".ds-my-data-stream-2099.03.07-000001", <1>
              "index_uuid": "Gpdiyq8sRuK9WuthvAdFbw",
              "prefer_ilm": true,
              "managed_by": "Unmanaged"
            },
            {
              "index_name": ".ds-my-data-stream-2099.03.08-000002",
              "index_uuid": "_eEfRrFHS9OyhqWntkgHAQ",
              "prefer_ilm": true,
              "managed_by": "Unmanaged"
            }
          ],
          "generation": 2,
          "status": "GREEN",
          "next_generation_managed_by": "Unmanaged",
          "prefer_ilm": true,
          "template": "my-data-stream-template",
          "hidden": false,
          "system": false,
          "allow_custom_routing": false,
          "replicated": false,
          "rollover_on_write": false
        }
      ]
    }
    ```

    1. First item in the `indices` array for `my-data-stream`. This item contains information about the stream’s oldest backing index, `.ds-my-data-stream-2099.03.07-000001`.


    The following [reindex API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) request copies documents from `.ds-my-data-stream-2099.03.07-000001` to `new-data-stream`. The request’s `op_type` is `create`.

    ```console
    POST /_reindex
    {
      "source": {
        "index": ".ds-my-data-stream-2099.03.07-000001"
      },
      "dest": {
        "index": "new-data-stream",
        "op_type": "create"
      }
    }
    ```

    You can also use a query to reindex only a subset of documents with each request.

    The following [reindex API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) request copies documents from `my-data-stream` to `new-data-stream`. The request uses a [`range` query](elasticsearch://reference/query-languages/query-dsl-range-query.md) to only reindex documents with a timestamp within the last week. Note the request’s `op_type` is `create`.

    ```console
    POST /_reindex
    {
      "source": {
        "index": "my-data-stream",
        "query": {
          "range": {
            "@timestamp": {
              "gte": "now-7d/d",
              "lte": "now/d"
            }
          }
        }
      },
      "dest": {
        "index": "new-data-stream",
        "op_type": "create"
      }
    }
    ```

7. If you previously changed your {{ilm-init}} poll interval, change it back to its original value when reindexing is complete. This prevents unnecessary load on the master node.

    The following cluster update settings API request resets the `indices.lifecycle.poll_interval` setting to its default value.

    ```console
    PUT /_cluster/settings
    {
      "persistent": {
        "indices.lifecycle.poll_interval": null
      }
    }
    ```

8. Resume indexing using the new data stream. Searches on this stream will now query your new data and the reindexed data.
9. Once you have verified that all reindexed data is available in the new data stream, you can safely remove the old stream.

    The following [delete data stream API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete-data-stream) request deletes `my-data-stream`. This request also deletes the stream’s backing indices and any data they contain.

    ```console
    DELETE /_data_stream/my-data-stream
    ```



## Update or add an alias to a data stream [data-streams-change-alias]

Use the [aliases API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-update-aliases) to update an existing data stream’s aliases. Changing an existing data stream’s aliases in its index pattern has no effect.

For example, the `logs` alias points to a single data stream. The following request swaps the stream for the alias. During this swap, the `logs` alias has no downtime and never points to both streams at the same time.

```console
POST _aliases
{
  "actions": [
    {
      "remove": {
        "index": "logs-nginx.access-prod",
        "alias": "logs"
      }
    },
    {
      "add": {
        "index": "logs-my_app-default",
        "alias": "logs"
      }
    }
  ]
}
```
%  TEST[s/^/PUT _data_stream/logs-nginx.access-prod\nPUT _data_stream/logs-my_app-default\n/]

