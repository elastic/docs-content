---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/infrastructure-threshold-alert.html
  - https://www.elastic.co/guide/en/serverless/current/observability-create-inventory-threshold-alert-rule.html

navigation_title: "Inventory"
---

# Create an inventory rule [observability-create-inventory-threshold-alert-rule]


::::{admonition} Required role
:class: note

For Observability serverless projects, the **Editor** role or higher is required to create inventory threshold rules. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


Based on the resources listed on the **Infrastructure inventory** page within the {{infrastructure-app}}, you can create a threshold rule to notify you when a metric has reached or exceeded a value for a specific resource or a group of resources within your infrastructure.

Additionally, each rule can be defined using multiple conditions that combine metrics and thresholds to create precise notifications and reduce false positives.

1. To access this page, go to **{{observability}}** → **Infrastructure**.
2. On the **Infrastructure inventory** page or the **Metrics Explorer** page, click **Alerts and rules** → **Infrastructure**.
3. Select **Create inventory rule**.

::::{tip}
When you select **Create inventory alert**, the parameters you configured on the **Infrastructure inventory** page will automatically populate the rule. You can use the Inventory first to view which nodes in your infrastructure you’d like to be notified about and then quickly create a rule in just a few clicks.

::::



## Inventory conditions [inventory-conditions]

Conditions for each rule can be applied to specific metrics relating to the inventory type you select. You can choose the aggregation type, the metric, and by including a warning threshold value, you can be alerted on multiple threshold values based on severity scores. When creating the rule, you can still get notified if no data is returned for the specific metric or if the rule fails to query {{es}}.

In this example, Kubernetes Pods is the selected inventory type. The conditions state that you will receive a critical alert for any pods within the `ingress-nginx` namespace with a memory usage of 95% or above and a warning alert if memory usage is 90% or above. The chart shows the results of applying the rule to the last 20 minutes of data. Note that the chart time range is 20 times the value of the look-back window specified in the `FOR THE LAST` field.

:::{image} ../../../images/serverless-inventory-alert.png
:alt: Inventory rule
:class: screenshot
:::


## Add actions [action-types-infrastructure]

You can extend your rules with actions that interact with third-party systems, write to logs or indices, or send user notifications. You can add an action to a rule at any time. You can create rules without adding actions, and you can also define multiple actions for a single rule.

To add actions to rules, you must first create a connector for that service (for example, an email or external incident management system), which you can then use for different rules, each with their own action frequency.

:::::{dropdown} Connector types
Connectors provide a central place to store connection information for services and integrations with third party systems. The following connectors are available when defining actions for alerting rules:

* [Cases](https://www.elastic.co/guide/en/kibana/current/cases-action-type.html)
* [D3 Security](https://www.elastic.co/guide/en/kibana/current/d3security-action-type.html)
* [Email](https://www.elastic.co/guide/en/kibana/current/email-action-type.html)
* [{{ibm-r}}](https://www.elastic.co/guide/en/kibana/current/resilient-action-type.html)
* [Index](https://www.elastic.co/guide/en/kibana/current/index-action-type.html)
* [Jira](https://www.elastic.co/guide/en/kibana/current/jira-action-type.html)
* [Microsoft Teams](https://www.elastic.co/guide/en/kibana/current/teams-action-type.html)
* [Observability AI Assistant](https://www.elastic.co/guide/en/kibana/current/obs-ai-assistant-action-type.html)
* [{{opsgenie}}](https://www.elastic.co/guide/en/kibana/current/opsgenie-action-type.html)
* [PagerDuty](https://www.elastic.co/guide/en/kibana/current/pagerduty-action-type.html)
* [Server log](https://www.elastic.co/guide/en/kibana/current/server-log-action-type.html)
* [{{sn-itom}}](https://www.elastic.co/guide/en/kibana/current/servicenow-itom-action-type.html)
* [{{sn-itsm}}](https://www.elastic.co/guide/en/kibana/current/servicenow-action-type.html)
* [{{sn-sir}}](https://www.elastic.co/guide/en/kibana/current/servicenow-sir-action-type.html)
* [Slack](https://www.elastic.co/guide/en/kibana/current/slack-action-type.html)
* [{{swimlane}}](https://www.elastic.co/guide/en/kibana/current/swimlane-action-type.html)
* [Torq](https://www.elastic.co/guide/en/kibana/current/torq-action-type.html)
* [{{webhook}}](https://www.elastic.co/guide/en/kibana/current/webhook-action-type.html)
* [xMatters](https://www.elastic.co/guide/en/kibana/current/xmatters-action-type.html)

::::{note}
Some connector types are paid commercial features, while others are free. For a comparison of the Elastic subscription levels, go to [the subscription page](https://www.elastic.co/subscriptions).

::::


For more information on creating connectors, refer to [Connectors](../../../deploy-manage/manage-connectors.md).

:::::


:::::{dropdown} Action frequency
After you select a connector, you must set the action frequency. You can choose to create a summary of alerts on each check interval or on a custom interval. For example, send email notifications that summarize the new, ongoing, and recovered alerts each hour:

:::{image} ../../../images/serverless-action-alert-summary.png
:alt: Action types
:class: screenshot
:::

Alternatively, you can set the action frequency such that you choose how often the action runs (for example, at each check interval, only when the alert status changes, or at a custom action interval). In this case, you define precisely when the alert is triggered by selecting a specific threshold condition: `Alert`, `Warning`, or `Recovered` (a value that was once above a threshold has now dropped below it).

:::{image} ../../../images/serverless-inventory-threshold-run-when-selection.png
:alt: Configure when an alert is triggered
:class: screenshot
:::

You can also further refine the conditions under which actions run by specifying that actions only run when they match a KQL query or when an alert occurs within a specific time frame:

* **If alert matches query**: Enter a KQL query that defines field-value pairs or query conditions that must be met for notifications to send. The query only searches alert documents in the indices specified for the rule.
* **If alert is generated during timeframe**: Set timeframe details. Notifications are only sent if alerts are generated within the timeframe you define.

:::{image} ../../../images/serverless-conditional-alerts.png
:alt: Configure a conditional alert
:class: screenshot
:::

:::::


:::::{dropdown} Action variables
Use the default notification message or customize it. You can add more context to the message by clicking the Add variable icon ![Add variable](../../../images/serverless-indexOpen.svg "") and selecting from a list of available variables.

:::{image} ../../../images/serverless-action-variables-popup.png
:alt: Action variables list
:class: screenshot
:::

The following variables are specific to this rule type. You can also specify [variables common to all rules](../../../explore-analyze/alerts-cases/alerts/rule-action-variables.md).

`context.alertDetailsUrl`
:   Link to the alert troubleshooting view for further context and details. This will be an empty string if the `server.publicBaseUrl` is not configured.

`context.alertState`
:   Current state of the alert.

`context.cloud`
:   The cloud object defined by ECS if available in the source.

`context.container`
:   The container object defined by ECS if available in the source.

`context.group`
:   Name of the group reporting data.

`context.host`
:   The host object defined by ECS if available in the source.

`context.labels`
:   List of labels associated with the entity where this alert triggered.

`context.metric`
:   The metric name in the specified condition. Usage: (`ctx.metric.condition0`, `ctx.metric.condition1`, and so on).

`context.orchestrator`
:   The orchestrator object defined by ECS if available in the source.

`context.originalAlertState`
:   The state of the alert before it recovered. This is only available in the recovery context.

`context.originalAlertStateWasALERT`
:   Boolean value of the state of the alert before it recovered. This can be used for template conditions. This is only available in the recovery context.

`context.originalAlertStateWasWARNING`
:   Boolean value of the state of the alert before it recovered. This can be used for template conditions. This is only available in the recovery context.

`context.reason`
:   A concise description of the reason for the alert.

`context.tags`
:   List of tags associated with the entity where this alert triggered.

`context.threshold`
:   The threshold value of the metric for the specified condition. Usage: (`ctx.threshold.condition0`, `ctx.threshold.condition1`, and so on)

`context.timestamp`
:   A timestamp of when the alert was detected.

`context.value`
:   The value of the metric in the specified condition. Usage: (`ctx.value.condition0`, `ctx.value.condition1`, and so on).

`context.viewInAppUrl`
:   Link to the alert source.

:::::



## Settings [infra-alert-settings]

With infrastructure threshold rules, it’s not possible to set an explicit index pattern as part of the configuration. The index pattern is instead inferred from **Metrics indices** on the [Settings](../../../solutions/observability/infra-and-hosts/configure-settings.md) page of the {{infrastructure-app}}.

With each execution of the rule check, the **Metrics indices** setting is checked, but it is not stored when the rule is created.