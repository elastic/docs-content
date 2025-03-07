---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/set-up-a-data-stream.html
applies_to:
  stack: ga
  serverless: ga
---

# Set up a data stream [set-up-a-data-stream]

To set up a data stream, follow these steps:

1. [Create an index lifecycle policy](#create-index-lifecycle-policy)
2. [Create component templates](#create-component-templates)
3. [Create an index template](#create-index-template)
4. [Create the data stream](#create-data-stream)
5. [Secure the data stream](#secure-data-stream)

You can also [convert an index alias to a data stream](#convert-index-alias-to-data-stream).

::::{important}
If you use {{fleet}}, {{agent}}, or {{ls}}, skip this tutorial. They all set up data streams for you.

For {{fleet}} and {{agent}}, check out this [data streams documentation](/reference/ingestion-tools/fleet/data-streams.md). For {{ls}}, check out the [data streams settings](logstash://reference/plugins-outputs-elasticsearch.md#plugins-outputs-elasticsearch-data_stream) for the `elasticsearch output` plugin.

::::



## Create an index lifecycle policy [create-index-lifecycle-policy]

While optional, we recommend using {{ilm-init}} to automate the management of your data stream’s backing indices. {{ilm-init}} requires an index lifecycle policy.

To create an index lifecycle policy in {{kib}}, open the main menu and go to **Stack Management > Index Lifecycle Policies**. Click **Create policy**.

You can also use the [create lifecycle policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-put-lifecycle).

```console
PUT _ilm/policy/my-lifecycle-policy
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


## Create component templates [create-component-templates]

A data stream requires a matching index template. In most cases, you compose this index template using one or more component templates. You typically use separate component templates for mappings and index settings. This lets you reuse the component templates in multiple index templates.

When creating your component templates, include:

* A [`date`](elasticsearch://reference/elasticsearch/mapping-reference/date.md) or [`date_nanos`](elasticsearch://reference/elasticsearch/mapping-reference/date_nanos.md) mapping for the `@timestamp` field. If you don’t specify a mapping, {{es}} maps `@timestamp` as a `date` field with default options.
* Your lifecycle policy in the `index.lifecycle.name` index setting.

::::{tip}
Use the [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/current) when mapping your fields. ECS fields integrate with several {{stack}} features by default.

If you’re unsure how to map your fields, use [runtime fields](../mapping/define-runtime-fields-in-search-request.md) to extract fields from [unstructured content](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#mapping-unstructured-content) at search time. For example, you can index a log message to a `wildcard` field and later extract IP addresses and other data from this field during a search.

::::


To create a component template in {{kib}}, open the main menu and go to **Stack Management > Index Management**. In the **Index Templates** view, click **Create component template**.

You can also use the [create component template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template).

```console
# Creates a component template for mappings
PUT _component_template/my-mappings
{
  "template": {
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date",
          "format": "date_optional_time||epoch_millis"
        },
        "message": {
          "type": "wildcard"
        }
      }
    }
  },
  "_meta": {
    "description": "Mappings for @timestamp and message fields",
    "my-custom-meta-field": "More arbitrary metadata"
  }
}

# Creates a component template for index settings
PUT _component_template/my-settings
{
  "template": {
    "settings": {
      "index.lifecycle.name": "my-lifecycle-policy"
    }
  },
  "_meta": {
    "description": "Settings for ILM",
    "my-custom-meta-field": "More arbitrary metadata"
  }
}
```
%  TEST[continued]


## Create an index template [create-index-template]

Use your component templates to create an index template. Specify:

* One or more index patterns that match the data stream’s name. We recommend using our [data stream naming scheme](/reference/ingestion-tools/fleet/data-streams.md#data-streams-naming-scheme).
* That the template is data stream enabled.
* Any component templates that contain your mappings and index settings.
* A priority higher than `200` to avoid collisions with built-in templates. See [Avoid index pattern collisions](../templates.md#avoid-index-pattern-collisions).

To create an index template in {{kib}}, open the main menu and go to **Stack Management > Index Management**. In the **Index Templates** view, click **Create template**.

You can also use the [create index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template). Include the `data_stream` object to enable data streams.

```console
PUT _index_template/my-index-template
{
  "index_patterns": ["my-data-stream*"],
  "data_stream": { },
  "composed_of": [ "my-mappings", "my-settings" ],
  "priority": 500,
  "_meta": {
    "description": "Template for my time series data",
    "my-custom-meta-field": "More arbitrary metadata"
  }
}
```
%  TEST[continued]


## Create the data stream [create-data-stream]

[Indexing requests](../data-streams/use-data-stream.md#add-documents-to-a-data-stream)     [Indexing requests](./use-data-stream.md#add-documents-to-a-data-stream)  add documents to a data stream. These requests must use an `op_type` of `create`. Documents must include a `@timestamp` field.

To automatically create your data stream, submit an indexing request that targets the stream’s name. This name must match one of your index template’s index patterns.

```console
PUT my-data-stream/_bulk
{ "create":{ } }
{ "@timestamp": "2099-05-06T16:21:15.000Z", "message": "192.0.2.42 - - [06/May/2099:16:21:15 +0000] \"GET /images/bg.jpg HTTP/1.0\" 200 24736" }
{ "create":{ } }
{ "@timestamp": "2099-05-06T16:25:42.000Z", "message": "192.0.2.255 - - [06/May/2099:16:25:42 +0000] \"GET /favicon.ico HTTP/1.0\" 200 3638" }

POST my-data-stream/_doc
{
  "@timestamp": "2099-05-06T16:21:15.000Z",
  "message": "192.0.2.42 - - [06/May/2099:16:21:15 +0000] \"GET /images/bg.jpg HTTP/1.0\" 200 24736"
}
```
%  TEST[continued]

You can also manually create the stream using the [create data stream API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create-data-stream). The stream’s name must still match one of your template’s index patterns.

```console
PUT _data_stream/my-data-stream
```
%  TEST[continued]
%  TEST[s/my-data-stream/my-data-stream-alt/]

After it's been created, you can view and manage this and other data streams from the **Stack Management > Index Management** view. Refer to [Manage a data stream](./manage-data-stream.md) for details.

## Secure the data stream [secure-data-stream]

Use [index privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices) to control access to a data stream. Granting privileges on a data stream grants the same privileges on its backing indices.

For an example, see [Data stream privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md#data-stream-privileges).


## Convert an index alias to a data stream [convert-index-alias-to-data-stream]

Prior to {{es}} 7.9, you’d typically use an [index alias with a write index](../../lifecycle/index-lifecycle-management/tutorial-automate-rollover.md#manage-time-series-data-without-data-streams) to manage time series data. Data streams replace this functionality, require less maintenance, and automatically integrate with [data tiers](../../lifecycle/data-tiers.md).

To convert an index alias with a write index to a data stream with the same name, use the [migrate to data stream API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-migrate-to-data-stream). During conversion, the alias’s indices become hidden backing indices for the stream. The alias’s write index becomes the stream’s write index. The stream still requires a matching index template with data stream enabled.

```console
POST _data_stream/_migrate/my-time-series-data
```
%  TEST[continued]


## Get information about a data stream [get-info-about-data-stream]

To get information about a data stream in {{kib}}, open the main menu and go to **Stack Management > Index Management**. In the **Data Streams** view, click the data stream’s name.

You can also use the [get data stream API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-data-stream).

```console
GET _data_stream/my-data-stream
```
%  TEST[continued]


## Delete a data stream [delete-data-stream]

To delete a data stream and its backing indices in {{kib}}, open the main menu and go to **Stack Management > Index Management**. In the **Data Streams** view, click the trash icon. The icon only displays if you have the `delete_index` [security privilege](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md) for the data stream.

You can also use the [delete data stream API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete-data-stream).

```console
DELETE _data_stream/my-data-stream
```
%  TEST[continued]

