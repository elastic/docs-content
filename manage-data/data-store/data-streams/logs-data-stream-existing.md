---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Enable logsdb"
description: "Enable logsdb index mode for existing logs data streams, including Elastic integrations."
products:
  - id: elasticsearch
---

# Enable `logsdb` mode for existing data streams [enable-logsdb-existing]

This page explains how to enable `logsdb` index mode for existing [logs data streams](/manage-data/data-store/data-streams/logs-data-stream.md), including data streams for {{product.integrations}}.

## About enabling logsdb

As of version 8.17, the `logsdb` index mode is automatically applied to new data streams matching `logs-*-*`. You might need to enable `logsdb` manually for integrations and data streams that existed before 8.17, or for data streams with names that don't match the `logs-*-*` pattern.

You enable `logsdb` by creating or modifying `@custom` [component templates](/manage-data/data-store/templates.md#component-templates) that apply the `index.mode: logsdb` setting.

:::{important}
Changes to component templates take effect when the data stream [rolls over](/manage-data/data-store/data-streams.md#data-streams-rollover). Data streams roll over automatically based on your index lifecycle policy, or you can [trigger a rollover manually](/manage-data/data-store/data-streams.md#data-streams-rollover).
:::

## Check the current index mode

Before making changes, check whether `logsdb` mode is already enabled for your data stream.

In {{kib}}, go to **{{index-manage-app}}** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). On the **Data Streams** tab, search for your data stream name (for example, `mysql` or `logs-myapp`). Check the **Index mode** column. If it shows **LogsDB**, the correct index mode is already enabled.

You can also use the [Get data stream API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-data-stream):

```console
GET _data_stream/logs-mysql*
```

In the response, check the `index_mode` field. If it's already set to `logsdb`, you don't need to continue.

## Enable logsdb for a specific data stream

If you already know which logs data stream you want to modify, you can enable `logsdb` by creating a `@custom` component template with the naming pattern `logs-<data-stream-name>@custom`.

For example, to enable `logsdb` for a data stream named `logs-myapp-prod`, create a component template named `logs-myapp@custom`:

```console
PUT _component_template/logs-myapp@custom
{
  "template": {
    "settings": {
      "index": {
        "mode": "logsdb"
      }
    }
  }
}
```

If a `@custom` component template already exists for your data stream, [edit it](/manage-data/data-store/index-basics.md#index-management-manage-component-templates) to add the `index.mode: logsdb` setting.

After the data stream rolls over, [verify that logsdb is enabled](#verify-that-logsdb-is-enabled).

## Enable logsdb for an integration

For integrations, first identify which logs data streams the integration creates, then create or update `@custom` component templates.

:::::::{stepper}

::::::{step} Identify the integration's logs data streams

In {{kib}} go to the **{{integrations}}** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Find your integration in the list of **Installed integrations** and click it to view more details. Note the integration name and version number.

You can find the integration's logs data streams by querying the [{{package-registry}}](integration-docs://reference/elastic_package_registry.md). Replace `mysql/1.28.1` with your integration's package name and version:

```bash
curl -sL epr.elastic.co/package/mysql/1.28.1 | jq '.data_streams[] |
select(.type == "logs") | {dataset, type}'
```

This command returns logs data streams used by the integration. For MySQL, the result is:

```json
{
  "dataset": "mysql.error",
  "type": "logs"
}
{
  "dataset": "mysql.slowlog",
  "type": "logs"
}
```

If the command returns nothing, the integration doesn't collect logs and `logsdb` doesn't apply.

::::::

::::::{step} Check for existing @custom component templates

Before creating new templates, check whether `@custom` component templates already exist for your data streams. Go to **{{index-manage-app}}** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). On the **Component Templates** tab, search for `@custom`. If templates already exist for your integration's data streams (for example, `logs-mysql.error@custom`), you'll update them in the next step instead of creating new ones.

::::::

::::::{step} Create or update @custom component templates

::::{tab-set}

:::{tab-item} Create

If no `@custom` templates exist, create them using the API. To create templates for all of an integration's logs data streams at once:

```bash
curl -sL epr.elastic.co/package/mysql/1.28.1 | jq -r '.data_streams[] |
select(.type == "logs") | .dataset' | xargs -I% curl -s -XPUT \
-H'Authorization: ApiKey <API_KEY>' -H'Content-Type: application/json' \
'<ES_URL>/_component_template/logs-%@custom' \
-d'{"template": {"settings": {"index": {"mode": "logsdb"}}}}'
```

Replace `<API_KEY>` with your API key and `<ES_URL>` with your {{es}} endpoint. Replace `mysql/1.28.1` with your integration's package name and version.

:::

:::{tab-item} Update 

If `@custom` templates already exist, [edit them](/manage-data/data-store/index-basics.md#index-management-manage-component-templates) to add the `index.mode: logsdb` setting:

```json
{
  "index": {
    "mode": "logsdb"
  }
}
```

Make this change for each of the integration's logs data streams.

:::



::::

::::::

:::::::

After the data stream rolls over, continue to [verify that logsdb is enabled](#verify-that-logsdb-is-enabled).

## Enable logsdb for all logs data streams

Instead of creating individual `@custom` templates, you can enable `logsdb` for all data streams matching `logs-*-*` by creating or modifying a component template named `logs@custom`.

Check whether `logs@custom` already exists:

```console
GET _component_template/logs@custom
```

If the component template exists, [edit it](/manage-data/data-store/index-basics.md#index-management-manage-component-templates) to add the `index.mode: logsdb` setting.

If the component template doesn't exist, create it:

```console
PUT _component_template/logs@custom
{
  "template": {
    "settings": {
      "index.mode": "logsdb"
    }
  }
}
```

This applies `logsdb` to all `logs-*-*` data streams after they roll over.

## Verify that logsdb is enabled

After your data streams roll over, verify that `logsdb` is enabled. Go to **{{index-manage-app}}** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). On the **Data Streams** tab, make sure the **Index mode** column shows **LogsDB** for your data streams.

You can also use the API:

```console
GET _data_stream/logs-mysql.error-default
```

In the response, confirm that `index_mode` is set to `logsdb`. If the index mode is incorrect, make sure the data stream has rolled over since you updated the component template.

## Related resources

- [Logs data streams](logs-data-stream.md)
- [Configure a logs data stream](logs-data-stream-configure.md)
- [Component templates](/manage-data/data-store/templates.md#component-templates)
- [Index templates](../templates.md)
- [Elastic API documentation]({{apis}})
