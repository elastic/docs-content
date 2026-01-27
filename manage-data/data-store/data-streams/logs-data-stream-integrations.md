---
applies_to:
  stack: ga 9.0+
navigation_title: "Enable logsdb for integrations"
description: "Enable logsdb index mode for integration data streams using @custom component templates."
products:
  - id: elasticsearch
---

# Enable logsdb for integrations [logsdb-integration]

This page shows you how to enable logsdb index mode for integration data streams, using `@custom` [component templates](/manage-data/data-store/templates.md#component-templates). If your integrations were installed before you upgraded to {{stack}} 9.x, you need to manually enable logsdb mode.

:::{admonition} Why isn't logsdb enabled automatically for integrations when upgrading?
Although logsdb significantly reduces storage costs, it can increase ingestion overhead slightly. On clusters that are already near capacity, enabling logsdb on many data streams at once can impact stability. For this reason, the 8.x to 9.x upgrade process does not automatically apply logsdb mode to existing integration data streams.
:::

Logsdb index mode is automatically applied to _new_ integration data streams in {{stack}} 9.0+. For more details, refer to [Availability of logsdb index mode](/manage-data/data-store/data-streams/logs-data-stream.md#logsdb-availability).

The steps on this page work in {{serverless-full}}, but you typically won't need to enable logsdb manually in {{serverless-short}}.

## Before you begin

To work with integration data streams, you need some details from the package manifest. Find your integration in the [Elastic integrations repository](https://github.com/elastic/integrations/tree/main/packages) or query the [{{package-registry}}](integration-docs://reference/elastic_package_registry.md) and make a note of the following:

- **Package name:** The exact name in the package manifest. For example, the MySQL integration package is named `mysql`. The package name also matches the name shown on the **Installed integrations** tab in {{kib}}, with underscores instead of spaces in multi-word names.
- **Logs dataset names:** Make sure the integration has data streams where the `type` is `logs`. For example, the MySQL integration has `mysql.error` and `mysql.slowlog`. Note the name of each logs dataset for use in later steps.

    :::{dropdown} Elastic Package Registry query (curl)
    You can use this `curl` command to confirm the integration's logs data streams in the [{{package-registry}}](integration-docs://reference/elastic_package_registry.md). Replace `mysql/1.28.1` with your integration package name and version:

    ```bash
    curl -sL epr.elastic.co/package/mysql/1.28.1 | jq '.data_streams[] |
    select(.type == "logs") | {dataset, type}'
    ```

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
    :::

## Enable logsdb

:::::::{stepper}

::::::{step} Find logs data streams and check index mode

1. Go to **{{index-manage-app}}** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). 
2. On the **Data Streams** tab, search for the integration name. 
3. Check the **Index mode** column for each logs data stream in the integration.

    If the index mode shows **LogsDB**, logsdb is already enabled and no action is needed. If it shows a different mode like **Standard** or **Time series**, continue to the next step.

::::::

::::::{step} Edit existing component templates

Use {{kib}} to find and edit `@custom` component templates for the integration log datasets:

1. Go to **{{index-manage-app}}** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. On the **Component Templates** tab, search for `@custom` to check whether templates already exist for the integration's logs datasets.
3. Edit the existing `@custom` templates that correspond to the log datasets you identified in [Before you begin](#before-you-begin). In the **Index settings** step, add the logsdb mode:

   ```json
    {
      "index": {
        "mode": "logsdb"
      }
    }
   ```

::::::

::::::{step} Create component templates

If they don't already exist, create `@custom` component templates for the logs datasets you identified in [Before you begin](#before-you-begin).

:::::{tab-set}
:group: custom
::::{tab-item} {{kib}}
:sync: kib

1. Go to **{{index-manage-app}}** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. On the **Component Templates** tab, click **Create component template** and step through the wizard:
    - In the **Logistics** step, name the template using the pattern `logs-<integration>.<dataset>@custom` (for example, `logs-mysql.error@custom`).
    - In the **Index settings** step, add the logsdb index mode.

Repeat for each logs dataset in the integration.

::::

::::{tab-item} API
:sync: api

To create a `@custom` template for a single integration dataset:

* In an {{stack}} deployment, use the [component template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template) API.
* In {{serverless-full}}, use the [component template](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-cluster-put-component-template) API.

Component template names must use the pattern `logs-<integration>.<dataset>@custom`.

Example:

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

Make sure to consider your cluster's resource usage before enabling logsdb on many data streams at once. On clusters that are already near capacity, this action could impact stability.
:::

To create `@custom` component templates for all logs data streams in an integration at once, run this command in a terminal window:

```bash
curl -sL epr.elastic.co/package/mysql/1.28.1 | jq -r '.data_streams[] |
select(.type == "logs") | .dataset' | xargs -I% curl -s -XPUT \
-H'Authorization: ApiKey <API_KEY>' -H'Content-Type: application/json' \
'<ES_URL>/_component_template/logs-%@custom' \
-d'{"template": {"settings": {"index.mode": "logsdb"}}}'
```

Replace `<API_KEY>` with your API key, `<ES_URL>` with your {{es}} endpoint, and `mysql/1.28.1` with your integration package name and version.

::::

:::::

::::::

::::::{step} Verify logsdb mode

Changes are applied to existing data streams on [rollover](/manage-data/data-store/data-streams.md#data-streams-rollover). Data streams roll over automatically based on your index lifecycle policy, or you can [trigger a rollover manually](/manage-data/data-store/data-streams/use-data-stream.md#manually-roll-over-a-data-stream).

After your data streams roll over, repeat the check in [step 1](#find-logs-data-streams-and-check-index-mode) to make sure the index mode is set to logsdb. If not, make sure the data stream has rolled over since you created or updated the corresponding template.

:::

::::::

:::::::

## Enable logsdb cluster-wide (optional)

You can also enable logsdb for all logs data streams cluster-wide (not just specific integrations). To do so, create or update the `logs@custom` component template. For details about component templates and template composition, refer to [Component templates](/manage-data/data-store/templates.md#component-templates).

:::{important}
If your cluster is already near capacity, stability issues can occur if you enable logsdb on many data streams at once. Make sure to check your cluster's resource usage before editing `logs@custom`.
:::

## Next steps

- Review the documentation for [](logs-data-stream.md), [](/manage-data/data-store/templates.md), and the [](/solutions/observability/logs/logs-index-template-defaults.md)
- [](logs-data-stream-configure.md)
- [](/solutions/security/detect-and-alert/using-logsdb-index-mode-with-elastic-security.md)
