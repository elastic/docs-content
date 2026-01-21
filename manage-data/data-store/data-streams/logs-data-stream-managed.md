---
applies_to:
  stack: ga 9.0+
  serverless: ga
navigation_title: "Enable logsdb for managed templates"
description: "Enable logsdb index mode for managed templates, using @custom component templates."
products:
  - id: elasticsearch
---

# Enable logsdb for integrations and managed templates [logsdb-managed]

This page shows you how to enable logsdb index mode for data streams that use managed templates, such as integration data streams. You can use `@custom` [component templates](/manage-data/data-store/index-basics.md#index-management-manage-component-templates) to enable logsdb for managed templates.

Logsdb index mode is [automatically applied](/manage-data/data-store/data-streams/logs-data-stream.md#logsdb-availability) to new data streams in {{serverless-short}} and {{stack}} 9.0+. You might need to enable logsdb manually for older {{stack}} data streams, such as integration data streams that existed before you upgraded to 9.x. 

In {{serverless-full}}, you typically won't need to enable logsdb, but the instructions on this page work in both {{serverless-short}} and {{stack}}.

:::{admonition} Why isn't logsdb enabled automatically for all logs data when upgrading?

Although logsdb significantly reduces storage costs, it can increase ingestion overhead slightly. On clusters that are already near capacity, enabling logsdb on many data streams at once can impact stability. For this reason, the 8.x to 9.x upgrade process does not automatically apply logsdb mode to existing data streams that collect logs data.
:::

## Enable logsdb for an integration [logsdb-integration]

Integrations use index templates managed by Elastic. To enable logsdb for an integration, create or modify a `@custom` [component template](/manage-data/data-store/index-basics.md#index-management-manage-component-templates) for each logs data stream in the integration.

:::::::{stepper}

::::::{step} Confirm integration details

In {{kib}}, go to the **{{integrations}}** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Find your integration in the list of **Installed integrations** and click it to view details, including the integration version number.

In a terminal window, query the [{{package-registry}}](integration-docs://reference/elastic_package_registry.md) to confirm that the integration uses logs data streams. Replace `mysql/1.28.1` with your integration's package name and version:

```bash
curl -sL epr.elastic.co/package/mysql/1.28.1 | jq '.data_streams[] |
select(.type == "logs") | {dataset, type}'
```

This command returns the integration's logs data streams.

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

Note the dataset names for use in the next step.

If the command returns nothing, the integration doesn't collect logs data and logsdb mode doesn't apply.

::::::

::::::{step} Create or update @custom component templates

:::::{tab-set}
:group: custom
::::{tab-item} {{kib}}
:sync: kib

Go to **{{index-manage-app}}** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). 

On the **Component Templates** tab, search for `@custom`. If `@custom` component templates exist for the data streams you identified in the previous step, edit each one to add the logsdb setting. 

If no `@custom` component templates exist, click **Create component template** and step through the wizard. In the **Index settings** step, specify `logsdb`.

```json
{
  "template": {
    "settings": {
      "index.mode": "logsdb"
    }
  }
}
```
Repeat for each logs dataset in the integration.

::::

::::{tab-item} API
:sync: api

To create or update a `@custom` template for a single integration dataset:

* In an {{stack}} deployment, use the [component template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template) API.
* In {{serverless-full}}, use the [component template](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-cluster-put-component-template) API.

First check whether the template exists, so you can preserve any existing settings:

```console
GET _component_template/logs-mysql.error@custom
```

Then create or update the template, making sure to include any existing settings retrieved in the GET request:

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

Repeat for each logs dataset in the integration.

::::

::::{tab-item} API (all datasets)

:::{warning}
This `curl` command uses `PUT`, which **overwrites** any existing component templates. Before using this command, confirm that no `@custom` templates exist for your integration. 
:::

To create `@custom` component templates for all logs data streams in an integration at once, run this command in a terminal window:

```bash
curl -sL epr.elastic.co/package/mysql/1.28.1 | jq -r '.data_streams[] |
select(.type == "logs") | .dataset' | xargs -I% curl -s -XPUT \
-H'Authorization: ApiKey <API_KEY>' -H'Content-Type: application/json' \
'<ES_URL>/_component_template/logs-%@custom' \
-d'{"template": {"settings": {"index.mode": "logsdb"}}}'
```

Replace `<API_KEY>` with your API key, `<ES_URL>` with your {{es}} endpoint, and `mysql/1.28.1` with your integration's package name and version.

:::{important}
Make sure to consider your cluster's resource usage before enabling logsdb on many data streams at once. On clusters that are already near capacity, this action could impact stability.
:::


::::

:::::

::::::

::::::{step} Verify logsdb mode

Changes are applied to existing data streams on [rollover](/manage-data/data-store/data-streams.md#data-streams-rollover). Data streams roll over automatically based on your index lifecycle policy, or you can [trigger a rollover manually](/manage-data/data-store/data-streams/use-data-stream.md#manually-roll-over-a-data-stream).

After your data streams roll over, verify that logsdb is enabled.

::::{tab-set}
:group: custom
:::{tab-item} {{kib}}
:sync: kib

Go to **{{index-manage-app}}** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). On the **Data Streams** tab, make sure the **Index mode** column shows **LogsDB** for your data streams.

:::

:::{tab-item} API
:sync: api

To verify logsdb mode:


* In an {{stack}} deployment, use the [get data streams](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-data-stream) API.
* In {{serverless-full}}, use the [get data streams](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-indices-get-data-stream) API.

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

::::::

:::::::

## Enable logsdb for other logs data streams [logsdb-logs-pattern]

Data streams that follow the `logs-*-*` naming pattern use Elastic's [managed `logs` index template](/solutions/observability/logs/logs-index-template-defaults.md). In {{stack}} 9.0+ and {{serverless-full}}, these data streams use logsdb mode [by default](/manage-data/data-store/data-streams/logs-data-stream.md#logsdb-availability). In older instances and clusters upgraded from 8.x, you might need to enable logsdb manually using `@custom` component templates.

To enable logsdb for these data streams, create or edit a `@custom` component template:

- **For a specific data stream:** Create or update `logs-<dataset>@custom` (for example, `logs-myapp@custom`).
- **For all `logs-*-*` data streams:** Create or update `logs@custom`.

    :::{important}
    Make sure to consider your cluster's resource usage before enabling logsdb on many data streams at once. On clusters that are already near capacity, this action could impact stability.
    :::

Follow the steps under [Create or update @custom component templates](#create-or-update-custom-component-templates) in the preceding section, targeting the `logs-*-*` template instead of an integration template. 

## Next steps

To optimize your use of logsdb, review these additional resources:

- [](logs-data-stream.md)
- [](logs-data-stream-configure.md)
- [](/manage-data/data-store/templates.md)
- [](/solutions/observability/logs/logs-index-template-defaults.md)
- [](/solutions/security/detect-and-alert/using-logsdb-index-mode-with-elastic-security.md)

