---
applies_to:
  stack: ga
  serverless: ga
  deployment:
    ess: ga
navigation_title: "Enable logsdb for integrations"
products:
  - id: elasticsearch
---

# Enable `logsdb` mode for {{product.integrations}} [enable-logsdb-integrations]

This page explains how to enable `logsdb` index mode for [{{product.integrations}}](integration-docs://reference/index.md) that are already installed. 

:::{tip}
If you're creating a new logs data stream from scratch, refer to [Create a logs data stream](logs-data-stream.md#how-to-use-logsds).
:::

% TODO better xrefs

{{integrations}} use [index templates](../templates.md) managed by Elastic. To enable `logsdb` mode, create custom [component templates](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template) that apply the setting to the integration's log data.

:::::{stepper}

::::{step} Find your installed integrations 

% TODO check navigation patterns in integration docs
% TODO package mainfest?

Go to the **{{integrations}}** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Check the list of **Installed integrations** and note the name of the integration you want to modify (for example, `MySQL`).

% TODO: add screenshot?

::::

::::{step} Confirm the integration collects logs

Not all integrations collect log data. To make sure your integration includes logs, run the following command, specifying your integration name and version:

% TODO streamline with | .dataset ?

```bash
curl -sL epr.elastic.co/package/mysql/1.28.1 | jq '.data_streams[] |
select(.type == "logs") | {dataset, type}'
```

If the integration collects logs, the command returns one or more dataset names:

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

Note these dataset names for use in later steps.

If the command returns nothing, the integration does not collect logs and `logsdb` mode does not apply.

::::


::::{step} Create custom component templates

To enable `logsdb` mode, add the `index.mode: logsdb` setting to a custom component template for each log dataset.

First, check whether custom component templates already exist for your integration:

% TODO confirm navigation patterns 

1. Go to the **Component Templates** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for the integration name, such as `mysql`. Look for templates ending in `@custom`, such as `logs-mysql.error@custom`.

If matching component templates exist, edit them to add the `logsdb` setting. Otherwise, create new component templates using one of the following methods:

::::{tab-set}

:::{tab-item} All integration datasets

You can use a single command to create component templates for all log datasets in an integration:

```bash
curl -sL epr.elastic.co/package/mysql/1.28.1 | jq '.data_streams[] |
select(.type == "logs") | .dataset' | xargs -I% curl -s -XPUT \
-H'Authorization: ApiKey <API_KEY>' -H'Content-Type: application/json' \
'<ES_URL>/_component_template/logs-%@custom' \
-d'{"template": {"settings": {"index": {"mode": "logsdb"}}}}'
```

Replace `<API_KEY>` with your API key and `<ES_URL>` with your {{es}} endpoint, and replace the `mysql` example with your integration name.

:::

:::{tab-item} Single dataset

To create a component template for one dataset at a time, use {{dev-tools-app}} Console or the command line.

The component template name must follow the pattern `logs-<dataset>@custom`. For example, for the `mysql.slowlog` dataset, the corresponding component template name is `logs-mysql.slowlog@custom`.

% TODO confirm this kind of pair (dev tools + cli) in other docs

% TODO validate examples

**{{dev-tools-app}} Console:**

```console
PUT _component_template/logs-mysql.slowlog@custom
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

**Command line:**

```bash
curl -s -XPUT -H'Authorization: ApiKey <API_KEY>' -H'Content-Type: application/json' \
'<ES_URL>/_component_template/logs-mysql.slowlog@custom' \
-d'{"template": {"settings": {"index": {"mode": "logsdb"}}}}'
```

Repeat for each dataset you want to modify, such as `logs-mysql.error@custom`.

::: 

:::: 

:::: 

::::{step} Roll over and verify

To apply your changes, [roll over](/manage-data/data-store/data-streams.md#data-streams-rollover) the data stream (automatically or manually).

After rollover, verify that `logsdb` mode is enabled:

1. Go to the **Data Streams** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for your integration name (for example, `mysql`).
3. Check the **Index mode** column.

The index mode column should now show `LogsDB`.

% TODO: add screenshot?
::::

:::::



