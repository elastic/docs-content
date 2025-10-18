---
navigation_title: Failed docs
products:
  - id: observability
  - id: cloud-serverless
applies_to:
  stack: ga 9.1
  serverless: ga
---

# Create a failed docs rule [observability-create-failed-docs-rule]


::::{note}

The **Editor** role or higher is required to create a failed docs rule using custom threshold rule. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::

Create a failed docs rule using the [custom threshold rule](../incident-management/create-custom-threshold-rule.md) to alert when the number of failed documents in your data stream reaches or exceeds a given value.

:::{image} /solutions/images/failed-docs-rule.png
:alt: Create failed docs rule using the custom threshold rule type
:screenshot:
:::

When creating a failed docs rule, the process depends on your deployment type and your space's solution view. You can check your solution view by selecting the **Spaces** icon.

Select the appropriate tab for your setup, then follow the instructions to create a failed docs rule:

::::{tab-set}

:::{tab-item} Serverless and Observability solution view
1. From the main menu, open the **Data Set Quality** page from **Management** → **Stack Management**, or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Find the data set you want to create a rule for in the table, and select **Open** from the **Actions** column.
1. Select **Alerts** → **Create custom threshold rule**.
1. Select **Add aggregation/field**.
1. For your new aggregation, set **Aggregation type** to **Count** and **KQL Filter** to `_index : ".fs*"`.
1. Select **Equation**, and set the equation to `(B / A) * 100`.
1. Set **Is above** to the desired threshold. For example, `1.5`.
1. Set the **Label** to `Failed docs`.
1. Select **Next** to go to the **Details** step.
1. Set the **Rule name** to `Data set quality` and add `failed_docs` to the **Tags**.
1. Select **Create rule**.
:::

:::{tab-item} Classic solution view
1. Select **Manage rules and connectors**.
1. Select **Create rule**, then **Custom threshold**.
1. Select **Data view**, then **Create a data view**.
1. Find your data stream under **All sources**.
1. Name your data view.
1. Add your index pattern with `::failures` appended. For example, `logs-synth.2-default::data,logs-synth.2-default::failures`.
1. Select **Save data view to Kibana**.
1. Select **Add aggregation/field**.
1. For your new aggregation, set **Aggregation type** to **Count** and **KQL Filter** to `_index : ".fs*"`.
1. Select **Equation**, and set the equation to `(B / A) * 100`.
1. Set **Is above** to the desired threshold. For example, `1.5`.
1. Set the **Label** to `Failed docs`.
1. Select **Next** to go to the **Details** menu.
1. Set the **Rule name** to `Data set quality` and add `failed_docs` to the **Tags**.
1. Select **Create rule**.
:::

::::

## Add actions [observability-create-failed-docs-alert-rule-add-actions]

You can extend your rules with actions that interact with third-party systems, write to logs or indices, or send user notifications. You can add an action to a rule at any time. You can create rules without adding actions, and you can also define multiple actions for a single rule.

To add actions to rules, you must first create a connector for that service (for example, an email or external incident management system), which you can then use for different rules, each with their own action frequency.

:::::{dropdown} Connector types
Connectors provide a central place to store connection information for services and integrations with third party systems. The following connectors are available when defining actions for alerting rules:

* [Cases](kibana://reference/connectors-kibana/cases-action-type.md)
* [D3 Security](kibana://reference/connectors-kibana/d3security-action-type.md)
* [Email](kibana://reference/connectors-kibana/email-action-type.md)
* [{{ibm-r}}](kibana://reference/connectors-kibana/resilient-action-type.md)
* [Index](kibana://reference/connectors-kibana/index-action-type.md)
* [Jira](kibana://reference/connectors-kibana/jira-action-type.md)
* [Microsoft Teams](kibana://reference/connectors-kibana/teams-action-type.md)
* [Observability AI Assistant](kibana://reference/connectors-kibana/obs-ai-assistant-action-type.md)
* [{{opsgenie}}](kibana://reference/connectors-kibana/opsgenie-action-type.md)
* [PagerDuty](kibana://reference/connectors-kibana/pagerduty-action-type.md)
* [Server log](kibana://reference/connectors-kibana/server-log-action-type.md)
* [{{sn-itom}}](kibana://reference/connectors-kibana/servicenow-itom-action-type.md)
* [{{sn-itsm}}](kibana://reference/connectors-kibana/servicenow-action-type.md)
* [{{sn-sir}}](kibana://reference/connectors-kibana/servicenow-sir-action-type.md)
* [Slack](kibana://reference/connectors-kibana/slack-action-type.md)
* [{{swimlane}}](kibana://reference/connectors-kibana/swimlane-action-type.md)
* [Torq](kibana://reference/connectors-kibana/torq-action-type.md)
* [{{webhook}}](kibana://reference/connectors-kibana/webhook-action-type.md)
* [xMatters](kibana://reference/connectors-kibana/xmatters-action-type.md)

::::{note}
Some connector types are paid commercial features, while others are free. For a comparison of the Elastic subscription levels, go to [the subscription page](https://www.elastic.co/subscriptions).

::::


For more information on creating connectors, refer to [Connectors](/deploy-manage/manage-connectors.md).

:::::


:::::{dropdown} Action frequency
After you select a connector, you must set the action frequency. You can choose to create a summary of alerts on each check interval or on a custom interval. Alternatively, you can set the action frequency such that you choose how often the action runs (for example, at each check interval, only when the alert status changes, or at a custom action interval). In this case, you must also select the specific threshold condition that affects when actions run: `Alert`, `No Data`, or `Recovered`.

:::{image} /solutions/images/serverless-custom-threshold-run-when.png
:alt: Configure when a rule is triggered
:screenshot:
:::

You can also further refine the conditions under which actions run by specifying that actions only run when they match a KQL query or when an alert occurs within a specific time frame:

* **If alert matches query**: Enter a KQL query that defines field-value pairs or query conditions that must be met for notifications to send. The query only searches alert documents in the indices specified for the rule.
* **If alert is generated during timeframe**: Set timeframe details. Notifications are only sent if alerts are generated within the timeframe you define.

:::{image} /solutions/images/serverless-logs-threshold-conditional-alert.png
:alt: Configure a conditional alert
:screenshot:
:::

:::::


:::::{dropdown} Action variables
Use the default notification message or customize it. You can add more context to the message by clicking the Add variable icon ![Add variable](/solutions/images/serverless-indexOpen.svg "") and selecting from a list of available variables.

:::{image} /solutions/images/serverless-action-variables-popup.png
:alt: Action variables list
:screenshot:
:::

The following variables are specific to this rule type. You can also specify [variables common to all rules](/explore-analyze/alerts-cases/alerts/rule-action-variables.md).

`context.alertDetailsUrl`
:   Link to the alert troubleshooting view for further context and details. This will be an empty string if the `server.publicBaseUrl` is not configured.

`context.cloud`
:   The cloud object defined by ECS if available in the source.

`context.container`
:   The container object defined by ECS if available in the source.

`context.group`
:   The array of objects containing groups that are reporting data.

`context.grouping` {applies_to}`stack: ga 9.1`
:   The object containing groups that are reporting data.

`context.host`
:   The host object defined by ECS if available in the source.

`context.labels`
:   List of labels associated with the entity where this alert triggered.

`context.orchestrator`
:   The orchestrator object defined by ECS if available in the source.

`context.reason`
:   A concise description of the reason for the alert.

`context.tags`
:   List of tags associated with the entity where this alert triggered.

`context.timestamp`
:   A timestamp of when the alert was detected.

`context.value`
:   List of the condition values.

`context.viewInAppUrl`
:   Link to the alert source.

:::::