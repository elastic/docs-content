---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Enable logsdb for existing data streams"
description: "Enable logsdb index mode for existing logs data streams, including Elastic integrations."
products:
  - id: elasticsearch
---

# Enable `logsdb` mode for existing data streams [enable-logsdb-existing]

This page shows you how to enable `logsdb` index mode for existing [logs data streams](/manage-data/data-store/data-streams/logs-data-stream.md). You can enable `logsdb` [cluster-wide](#logsdb-cluster-wide) or for {{product.integrations}}.

% TODO look for prior art on jump links/sections

## About enabling logsdb 

The `logsdb` index mode is [automatically applied](/manage-data/data-store/data-streams/logs-data-stream.md#logsdb-availability) to some data streams. You might need to enable `logsdb` manually for other data streams, such as older integration logs data streams.

Before you enable `logsdb` mode for an existing data stream, review these tips:

- **Mappings:** If `host.name` already exists in your data stream with a non-keyword type, mapping errors can occur. For details, refer to [Configure a logs data stream](/manage-data/data-store/data-streams/logs-data-stream-configure.md#logsdb-sort-settings).
- **Capacity:** Consider your cluster's current resource usage before enabling `logsdb` for many data streams simultaneously. Although `logsdb` significantly reduces storage costs, it can increase ingestion overhead slightly, which can impact stability on clusters that are already near capacity.
- **Rollover:** The `logsdb` index mode won't take effect until the data stream [rolls over](/manage-data/data-store/data-streams.md#data-streams-rollover) (automatically via lifecycle policy or manually).


## Enable `logsdb` cluster-wide [logsdb-cluster-wide]

% TODO confirm this section should come first (simplest but possible capacity issues?)

To enable `logsdb` for all data streams matching the `logs-*-*` pattern, create or modify a [component template](/manage-data/data-store/index-basics.md#index-management-manage-component-templates) named `logs@custom`.

First, check whether `logs@custom` already exists:

```console
GET _component_template/logs@custom
```

If the component template exists, edit it to add the `index.mode: logsdb` setting:

```json
{
  "template": {
    "settings": {
      "index.mode": "logsdb"
    }
  }
}
```

If the `logs@custom` template doesn't exist yet, create it:

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

To make sure `logsdb` mode is enabled, refer to [Verify the logsdb setting](#verify-the-logsdb-setting).

## Enable `logsdb` for an integration

Integrations use [index templates](/manage-data/data-store/templates.md) managed by Elastic. To set `logsdb` mode for an integration, create or modify `@custom` [component templates](/manage-data/data-store/index-basics.md#index-management-manage-component-templates) for each logs data stream in the integration.

:::::::{stepper}

::::::{step} Confirm integration details

In {{kib}}, go to the **{{integrations}}** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Find your integration in the list of **Installed integrations** and click it to view details, including the integration version number.

Next, query the [{{package-registry}}](integration-docs://reference/elastic_package_registry.md) to confirm the integration has logs data streams. Replace `mysql/1.28.1` with your integration's package name and version:

```bash
curl -sL epr.elastic.co/package/mysql/1.28.1 | jq '.data_streams[] |
select(.type == "logs") | {dataset, type}'
```

This command returns the integration's logs data streams. Example:

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

If the command returns nothing, the integration doesn't collect logs data and `logsdb` mode doesn't apply.

::::::

::::::{step} Check the current index mode

Go to **{{index-manage-app}}** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). On the **Data Streams** tab, search for the integration name. Check the **Index mode** column for each integration data stream that collects logs data. (If it already shows **LogsDB**, you don't need to complete additional steps.)

% TODO add screenshot?

Note the logs data stream names for reference in the next step.

::::::

::::::{step} Edit existing `@custom` component templates

Go to **{{index-manage-app}}** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). On the **Component Templates** tab, search for `@custom`. 

If `@custom` component templates exist for the data streams you identified in the previous step, edit each one to add the `logsdb` setting:

```json
{
  "index": {
    "mode": "logsdb"
  }
}
```

After the data stream has rolled over, you can [verify the setting](#verify-the-logsdb-setting) to make sure `logsdb` mode is active.

If no `@custom` component templates exist, continue to the next step.

::::::

::::::{step} (Optional) Create `@custom` templates

If you didn't find existing `@custom` templates in the preceding step, create one for each logs dataset.

:::::{tab-set}
:group: example-group

::::{tab-item} {{kib}}
:sync: tab1

Go to **{{index-manage-app}}** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). On the **Component Templates** tab, click **Create component template** and step through the wizard. 

Repeat for each logs dataset in the integration.

::::

::::{tab-item} API

:::{warning}
This option uses a `PUT` request, which **overwrites** existing component templates. Use this request only if you confirmed in the preceding step that `@custom` templates don't already exist.
:::

To create a specific `@custom` template, use the [component template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template) :

```console
PUT _component_template/logs-mysql.error@custom
{
  "template": {
    "settings": {
      "index.mode": "logsdb"
    }
  }
}
```
::::

::::{tab-item} API (all)

:::{warning}
This option uses a `PUT` request, which **overwrites** existing component templates. Use this request only if you confirmed in the preceding step that `@custom` templates don't already exist.
:::

To create `@custom` component templates for all logs data streams in an integration at once, use this command:

```bash
curl -sL epr.elastic.co/package/mysql/1.28.1 | jq -r '.data_streams[] |
select(.type == "logs") | .dataset' | xargs -I% curl -s -XPUT \
-H'Authorization: ApiKey <API_KEY>' -H'Content-Type: application/json' \
'<ES_URL>/_component_template/logs-%@custom' \
-d'{"template": {"settings": {"index": {"mode": "logsdb"}}}}'
```

Replace `<API_KEY>` with your API key, `<ES_URL>` with your {{es}} endpoint, and `mysql/1.28.1` with your integration's package name and version.

::::

% end tab set
:::::

::::::

:::::::


## Verify the `logsdb` setting

:::{important}
Template changes take effect when a data stream [rolls over](/manage-data/data-store/data-streams.md#data-streams-rollover). Data streams roll over automatically based on your index lifecycle policy, or you can [trigger a rollover manually](/manage-data/data-store/data-streams.md#data-streams-rollover).
:::

After your data streams roll over, verify that `logsdb` is enabled. 

::::{tab-set}

:::{tab-item} {{kib}}

Go to **{{index-manage-app}}** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). On the **Data Streams** tab, make sure the **Index mode** column shows **LogsDB** for your data streams.

:::

:::{tab-item} API

Use the [Get data stream API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-data-stream):

```console
GET _data_stream/logs-mysql.error-default
```

In the response, confirm that `index_mode` is set to `logsdb`:

```json
{
  "data_streams": [
    {
      "name": "logs-mysql.error-default",
      "indices": [...],
      "index_mode": "logsdb"
    }
  ]
}
```

:::

::::

If the index mode is not `logsdb`, make sure the data stream has rolled over since you created or updated the corresponding template.

## Related resources

% TODO improve; add context

- [Logs data streams](logs-data-stream.md)
- [Configure a logs data stream](logs-data-stream-configure.md)
- [Index templates](/manage-data/data-store/templates.md) and [component templates](/manage-data/data-store/templates.md#component-templates)
% TODO - relevant api doc links