---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/logs-data-stream.html
applies_to:
  stack: ga 9.0+
  serverless: ga
products:
  - id: elasticsearch
---

# Logs data streams [logs-data-stream]

Logs data streams store log data more efficiently. In benchmarks, logsdb index mode reduced the storage footprint of log data by up to 60%, with a small impact (10-20%) to indexing performance. Results vary depending on your data set and {{es}} version.

Logs data streams are created when the `index.mode` in the relevant template is set to `logsdb`, either automatically or manually.

Logsdb index mode is enabled by default for logs in {{serverless-full}}, and for new logs data streams in {{stack}} 9.0 and later.

## Availability of logsdb index mode [logsdb-availability]

Logsdb index mode is automatically enabled for the following data streams:

- **{{serverless-full}}:** Logsdb mode is automatically set on new and existing data streams with names matching the `logs-*-*` pattern.
- **{{stack}}:** Automatic logsdb mode depends on your version and configuration:
  - As of {{es}} version 9.0, logsdb mode is automatically set on **new** data streams with names matching the `logs-*-*` pattern.
  - In clusters that were upgraded from 8.x to 9.x:
    - If the instance had no existing `logs-*-*` data streams when you upgraded, new `logs-*-*` data streams are set to logsdb mode.
    - Existing data streams, including those used for integrations or APM in 8.x instances, are **not** automatically set to logsdb mode.

You can enable logsdb on existing data streams as needed, by editing the relevant [index templates](#logsdb-index-template). For integrations, use [@custom component templates](#logsdb-component-template).

## Enable logsdb index mode [how-to-use-logsds]

In most cases, you won't need to enable logsdb mode manually. If you do need to enable it, you can either create a new template or update an existing one.

Set `index.mode` to `logsdb` in the relevant [index template](#logsdb-index-template) or [@custom component template](#logsdb-component-template):

- **New data streams:** Create a new template, specifying `logsdb` for the index mode. New data streams matching the template's index pattern use logsdb mode automatically.
- **Existing data streams:** Update the templates the data stream references. Logsdb mode will take effect on the next [rollover](/manage-data/data-store/data-streams.md#data-streams-rollover). For integrations, refer to [](/manage-data/data-store/data-streams/logs-data-stream-integrations.md).

### Set logsdb mode in an index template [logsdb-index-template]

::::{tab-set}
:::{tab-item} {{kib}}

To create or edit an index template in {{kib}}:

1. Go to **{{index-manage-app}}** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. On the **Index Templates** tab, click **Create template** to create a new template, or click the name of an existing template to edit it.

    :::{tip}
    If you have existing templates labeled **Managed**, refer to [](logs-data-stream-integrations.md) or [](/solutions/observability/logs/logs-index-template-defaults.md).
    :::

3. Complete the steps in the wizard. In the **Logistics** step:

    - {applies_to}`serverless: ga` Click the **Set index mode** toggle to show the **Index mode** field.
    - Select **LogsDB** as the **Index mode**.

:::

:::{tab-item} API

To create or update an index template:

* In an {{stack}} deployment, use the [create index template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) API.
* In {{serverless-full}}, use the [create index template](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-indices-put-index-template) API.

First retrieve the current configuration, if any, so you can preserve existing settings. The PUT request **overwrites** any existing template.

```console
GET _index_template/my-index-template
```

Set `index.mode` to `logsdb` in the template request:

```console
PUT _index_template/my-index-template
{
  "index_patterns": ["my-data-*"],
  "data_stream": { },
  "template": {
     "settings": {
        "index.mode": "logsdb"
     }
  },
  "priority": 200
}
```
:::
::::

### Set logsdb mode for integrations [logsdb-component-template]

To enable logsdb mode for integration data streams, create or update a `@custom` component template for each logs dataset. For details, refer to [Enable logsdb for integrations](/manage-data/data-store/data-streams/logs-data-stream-integrations.md).

## Next steps

- [](/manage-data/data-store/data-streams/logs-data-stream-configure.md)
- [Review mappings and sorting](/manage-data/data-store/data-streams/logs-data-stream-configure.md#logsdb-host-name)
- [](/manage-data/data-store/data-streams/use-data-stream.md)
- [](/manage-data/data-store/data-streams/logs-data-stream-integrations.md)
- [](/solutions/security/detect-and-alert/using-logsdb-index-mode-with-elastic-security.md)
