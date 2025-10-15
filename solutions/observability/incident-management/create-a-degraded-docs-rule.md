---
navigation_title: Degraded docs
products:
  - id: observability
  - id: cloud-serverless
applies_to:
  stack: ga 9.1
  serverless: ga
---

# Create a degraded docs rule [degraded-docs-alert]

::::{note}

Users need the **Data Set Quality** role with the **Manage rules** privilege or the **Editor** role or higher to create degraded docs rules. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/manage-users.md#general-assign-user-roles).

::::


Based on the data found on the [**Data Set Quality**](../data-set-quality-monitoring.md) page, you can create a rule to notify you when the percentage of degraded documents for a specific data view has exceeded a value over a specific time period.

:::{image} /solutions/images/observability-degraded-docs-rule.png
:alt: Create rule for degraded docs
:screenshot:
:::

To access this rule from the **Alerts** page:

1. Go to **Alerts**.
1. Click **Manage Rules** → **Create rule**.
1. Under **Select rule type**, select **Degraded docs**.

You can also access this rule from the **Data Set Quality** page:

1. To open the **Data Set Quality** management page, find it in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select a data set name from the data set table.
1. Select **Actions** in the upper-right corner of the page.
1. Select **Create rule**.

## Define the conditions [degraded-docs-rule-conditions]

Define the following conditions for your rule:

1. Set the data view you want to create the rule for. If you access the rule from the **Data Set Quality** page, the data view is automatically populated.
1. Set the threshold percentage that, when exceeded for a period of time, the rule sends an alert.
1. Specify how long the threshold must be exceeded before an alert is sent.
1. (Optional) Set one or more **Group alerts by** fields. Every unique value will create an alert.
1. Set how often to check the rule conditions by selecting a time value and unit under **Rule schedule**.
1. (Optional) Configure **Advanced options**:
   - Define the number of consecutive matches required before an alert is triggered under **Alert delay**.
   - Enable or disable **Flapping Detection** to reduce noise from frequently changing alerts. You can customize the flapping detection settings if you need different thresholds for detecting flapping behavior.

## Preview chart [degraded-docs-rule-chart-preview]

The preview chart provides a visualization of how many entries match your configuration. The shaded area shows the threshold you’ve set.

If you use the **Group alerts by** option, the maximum bar size will be 3. It will only show the top 3 fields.

## Add actions [observability-create-custom-threshold-alert-rule-add-actions]

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