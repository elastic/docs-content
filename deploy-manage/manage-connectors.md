---
mapped_urls:
  - https://www.elastic.co/guide/en/kibana/current/action-types.html
  - https://www.elastic.co/guide/en/serverless/current/action-connectors.html
applies_to:
  stack:
  serverless:
---

# Manage connectors [connector-management]

Connectors serve as a central place to store connection information for both Elastic and third-party systems. They enable the linking of actions to rules, which execute as background tasks on the {{kib}} server when rule conditions are met. This allows rules to route actions to various destinations such as log files, ticketing systems, and messaging tools. Different {{kib}} apps may have their own rule types, but they typically share connectors. The **{{stack-manage-app}} > {{connectors-ui}}** provides a central location to view and manage all connectors in the current space.

::::{note}
This page is about {{kib}} connectors that integrate with services like generative AI model providers. If you’re looking for Search connectors that synchronize third-party data into {{es}}, refer to [Connector clients](https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-integrations-connector-client.html).

::::

## Required permissions [_required_permissions_2]

Access to connectors is granted based on your privileges to alerting-enabled features. For more information, go to [Security](../explore-analyze/alerts-cases/alerts/alerting-setup.md#alerting-security).

## Connector networking configuration [_connector_networking_configuration]

```yaml {applies_to}
stack:
```

If you're using {{stack}}, use the [action configuration settings](https://www.elastic.co/guide/en/kibana/current/alert-action-settings-kb.html#action-settings) to customize connector networking configurations, such as proxies, certificates, or TLS settings. You can set configurations that apply to all your connectors or use `xpack.actions.customHostSettings` to set per-host configurations.

## Connector list [connectors-list]

In **{{stack-manage-app}} > {{connectors-ui}}**, you can find a list of the connectors in the current space. You can use the search bar to find specific connectors by name and type. The **Type** dropdown also enables you to filter to a subset of connector types.

:::{image} ../images/kibana-connector-filter-by-type.png
:alt: Filtering the connector list by types of connectors
:class: screenshot
:::

You can delete individual connectors using the trash icon. Alternatively, select multiple connectors and delete them in bulk using the **Delete** button.

:::{image} ../images/kibana-connector-delete.png
:alt: Deleting connectors individually or in bulk
:class: screenshot
:::

::::{note}
You can delete a connector even if there are still actions referencing it. When this happens the action will fail to run and errors appear in the {{kib}} logs.

::::

## Creating a new connector [creating-new-connector]

New connectors can be created with the **Create connector** button, which guides you to select the type of connector and configure its properties. For a full list of available connectors, see [Available connectors](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/connectors-kibana.md).

::::{note}
Some connector types are paid commercial features, while others are free. For a comparison of the Elastic subscription levels, go to [the subscription page](https://www.elastic.co/subscriptions).
::::

:::{image} ../images/kibana-connector-select-type.png
:alt: Connector select type
:class: screenshot
:width: 75%
:::

After you create a connector, it is available for use any time you set up an action in the current space.

::::{tip}
For out-of-the-box and standardized connectors, refer to [preconfigured connectors](https://www.elastic.co/guide/en/kibana/current/pre-configured-connectors.html). 

You can also manage connectors as resources with the [Elasticstack provider](https://registry.terraform.io/providers/elastic/elasticstack/latest) for Terraform. For more details, refer to the [elasticstack_kibana_action_connector](https://registry.terraform.io/providers/elastic/elasticstack/latest/docs/resources/kibana_action_connector) resource.

Preconfigured connectors and the Terraform resource are not available in {{serverless-full}} projects.
::::

## Importing and exporting connectors [importing-and-exporting-connectors]

To import and export connectors, use the [Saved Objects Management UI](/explore-analyze/find-and-organize/saved-objects.md).

If a connector is missing sensitive information after the import, a **Fix** button appears in **{{connectors-ui}}**.

:::{image} ../images/kibana-connectors-with-missing-secrets.png
:alt: Connectors with missing secrets
:class: screenshot
:::

## Monitoring connectors [monitoring-connectors]

You can query the [Event log index](/explore-analyze/alerts-cases/alerts/event-log-index.md) to gather information on connector successes and failures.

If you're using {{stack}}, then you can also use the [Task Manager health API](/deploy-manage/monitor/kibana-task-manager-health-monitoring.md) to monitor connector performance. However, if connectors fail to run, they will report as successful to Task Manager. The failure stats will not accurately depict connector failures.
