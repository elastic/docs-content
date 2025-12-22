---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/set-up-a-data-stream.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Set up a data stream [set-up-a-data-stream]

The process of setting up a data stream in {{stack}} and {{serverless-full}} is similar, making use of their respective APIs. However, because {{serverless-short}} provides a built-in [data stream lifecycle](/manage-data/lifecycle/data-stream.md) mechanism and retention settings, you don't need to configure index lifecycle management ({{ilm-init}}) options as you do in an {{stack}} deployment.

To set up a data stream, follow these steps:

1. [Create an index lifecycle policy](#create-index-lifecycle-policy) {applies_to}`serverless: unavailable`
2. [Create component templates](#create-component-templates)
3. [Create an index template](#create-index-template)
4. [Create the data stream](#create-data-stream)
5. [Secure the data stream](#secure-data-stream)

You can also [convert an index alias to a data stream](#convert-index-alias-to-data-stream).

:::{important}
If you use {{fleet}}, {{agent}}, or {{ls}}, skip this tutorial. They all set up data streams for you.

For {{fleet}} and {{agent}}, refer to [](/reference/fleet/data-streams.md). For {{ls}}, refer to the [data streams settings](logstash-docs-md://lsr/plugins-outputs-elasticsearch.md#plugins-outputs-elasticsearch-data_stream) for the `elasticsearch output` plugin.

:::


## Create an index lifecycle policy [create-index-lifecycle-policy]
```{applies_to}
serverless: unavailable
```

While optional, we recommend using the {{ilm}} ({{ilm-init}}) capability in {{stack}} deployments to automate the management of your data stream’s backing indices. {{ilm-init}} requires an index lifecycle policy.

:::{admonition} Simpler lifecycle management in {{serverless-short}} projects
{{ilm-init}} lets you automatically transition indices through data tiers according to your performance needs and retention requirements. This allows you to balance hardware costs with performance. {{ilm-init}} is not available in {{serverless-short}}, where  performance optimizations are automatic. Instead, [data stream lifecycle](/manage-data/lifecycle/data-stream.md) is available as a data management option.
:::

To create an index lifecycle policy in {{kib}}:

1. Go to the **Index Lifecycle Policies** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Click **Create policy**.

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

:::{tip}
Use the [Elastic Common Schema (ECS)](ecs://reference/index.md) when mapping your fields. ECS fields integrate with several {{stack}} features by default.

If you’re unsure how to map your fields, use [runtime fields](../mapping/define-runtime-fields-in-search-request.md) to extract fields from [unstructured content](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#mapping-unstructured-content) at search time. For example, you can index a log message to a `wildcard` field and later extract IP addresses and other data from this field during a search.
:::

::::{tab-set}
:group: set-up-ds
:::{tab-item} {{kib}}
:sync: kibana
To create a component template in {{kib}}:

1. Go to the **Index Management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. In the **Index Templates** tab, click **Create component template**.
::: 

:::{tab-item} API
:sync: api
Use an API to create a component template:

* In an {{stack}} deployment, use the [create component template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template) API.
* In {{serverless-full}}, use the [create component template](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-cluster-put-component-template) API.

To create a component template for mappings, use this request:

```console
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
```

To create a component template for index settings, use this request:

```console
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

::: 
::::

## Create an index template [create-index-template]

Use your component templates to create an index template. Specify:

* One or more index patterns that match the data stream’s name. We recommend using our [data stream naming scheme](/reference/fleet/data-streams.md#data-streams-naming-scheme).
* That the template is data stream enabled.
* Any component templates that contain your mappings and index settings.
* A priority higher than `200` to avoid collisions with built-in templates. See [Avoid index pattern collisions](../templates.md#avoid-index-pattern-collisions).

::::{tab-set}
:group: set-up-ds
:::{tab-item} {{kib}}
:sync: kibana
To create an index template in {{kib}}:

1. Go to the **Index Management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. In the **Index Templates** tab, click **Create template**.

::: 

:::{tab-item} API
:sync: api
Use an API to create an index template:

* In an {{stack}} deployment, use the [create an index template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) API.
* In {{serverless-full}}, use the [create an index template](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-indices-put-index-template) API.

Include the `data_stream` object to enable data streams:

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

:::
::::

## Create the data stream [create-data-stream]

[Indexing requests](../data-streams/use-data-stream.md#add-documents-to-a-data-stream) add documents to a data stream. These requests must use an `op_type` of `create`. Documents must include a `@timestamp` field.

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
You can also use an API to manually create the data stream:

* In an {{stack}} deployment, use the [create a data stream](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create-data-stream) API.
* In {{serverless-full}}, use the [create a data stream](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-indices-create-data-stream) API.

```console
PUT _data_stream/my-data-stream
```

After it's been created, you can view and manage this and other data streams from the **Index Management** view. Refer to [Manage a data stream](./manage-data-stream.md) for details.

## Secure the data stream [secure-data-stream]

Use [index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) to control access to a data stream. Granting privileges on a data stream grants the same privileges on its backing indices.

For an example, refer to [Data stream privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md#data-stream-privileges).


## Convert an index alias to a data stream [convert-index-alias-to-data-stream]

Prior to {{es}} 7.9, you’d typically use an index alias with a write index to manage time series data. Data streams replace this functionality, require less maintenance, and automatically integrate with [data tiers](../../lifecycle/data-tiers.md).

You can convert an index alias with a write index to a data stream with the same name, using an API:

* In an {{stack}} deployment, use the [convert an index alias to a data stream](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-migrate-to-data-stream) API.
* In {{serverless-full}}, use the [convert an index alias to a data stream](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-indices-migrate-to-data-stream) API.

During conversion, the alias's indices become hidden backing indices for the stream. The alias's write index becomes the stream's write index. The stream still requires a matching index template with data stream enabled.

```console
POST _data_stream/_migrate/my-time-series-data
```


## Get information about a data stream [get-info-about-data-stream]

You can review metadata about each data stream using the {{kib}} UI (visual overview) or the API (raw JSON).

::::{tab-set}
:group: set-up-ds
:::{tab-item} {{kib}}
:sync: kibana
To get information about a data stream in {{kib}}:

1. Go to the **Index Management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. In the **Data Streams** tab, click the data stream’s name.

:::{tip}
:applies_to: {"stack": "ga 9.2, preview 9.1", "serverless": "ga"}
Starting with {{es}} version 9.2, you can use the [**Streams**](/solutions/observability/streams/streams.md) page to view the details of a data stream. The **Streams** page provides a centralized interface for managing your data in {{kib}}.Select a stream to view its details.
:::

:::

:::{tab-item} API
:sync: api
You can also use an API to get this information:

* In an {{stack}} deployment, use the [get data stream](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-data-stream) API.
* In {{serverless-full}}, use the [get data streams](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-indices-get-data-stream) API.

```console
GET _data_stream/my-data-stream
```

:::
::::

## Delete a data stream [delete-data-stream]

You can delete a data stream and its backing indices via the {{kib}} UI or an API. To complete this action, you need the `delete_index` [security privilege](elasticsearch://reference/elasticsearch/security-privileges.md) for the data stream.

::::{tab-set}
:group: set-up-ds
:::{tab-item} {{kib}}
:sync: kibana

To delete a data stream and its backing indices in {{kib}}:

1. Go to the **Index Management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. In the **Data Streams** view, click the trash can icon. The icon only displays if you have the `delete_index` security privilege for the data stream.

::: 
:::{tab-item} API
:sync: api

You can also use an API to delete a data stream:

* In an {{stack}} deployment, use the [delete data streams](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete-data-stream) API.
* In {{serverless-full}}, use the [delete data streams](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-indices-delete-data-stream) API.

```console
DELETE _data_stream/my-data-stream
```

:::
::::