---
navigation_title: "Inventory"
---

# Create an inventory threshold rule [infrastructure-threshold-alert]


Based on the resources listed on the **Infrastructure inventory** page within the {{infrastructure-app}}, you can create a threshold rule to notify you when a metric has reached or exceeded a value for a specific resource or a group of resources within your infrastructure.

Additionally, each rule can be defined using multiple conditions that combine metrics and thresholds to create precise notifications and reduce false positives.

::::{tip}
When you select **Create inventory alert**, the parameters you configured on the **Infrastructure inventory** page will automatically populate the rule. You can use the Inventory first to view which nodes in your infrastructure you’d like to be notified about and then quickly create a rule in just a few clicks.

::::



## Inventory conditions [inventory-conditions]

Conditions for each rule can be applied to specific metrics relating to the inventory type you select. You can choose the aggregation type, the metric, and by including a warning threshold value, you can be alerted on multiple threshold values based on severity scores. When creating the rule, you can still get notified if no data is returned for the specific metric or if the rule fails to query {{es}}. You can also set advanced options such as the number of consecutive runs that must meet the rule conditions before an alert occurs.

In this example, Kubernetes Pods is the selected inventory type. The conditions state that you will receive a critical alert for any pods within the `ingress-nginx` namespace with a memory usage of 95% or above and a warning alert if memory usage is 90% or above. The chart shows the results of applying the rule to the last 20 minutes of data. Note that the chart time range is 20 times the value of the look-back window specified in the `FOR THE LAST` field.

:::{image} ../../../images/observability-inventory-alert.png
:alt: Inventory rule
:class: screenshot
:::


## Action types [action-types-infrastructure]

Extend your rules by connecting them to actions that use the following supported built-in integrations.

* [D3 Security](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/d3security-action-type.md)
* [Email](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/email-action-type.md)
* [{{ibm-r}}](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/resilient-action-type.md)
* [Index](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/index-action-type.md)
* [Jira](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/jira-action-type.md)
* [Microsoft Teams](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/teams-action-type.md)
* [Observability AI Assistant connector](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/obs-ai-assistant-action-type.md)
* [{{opsgenie}}](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/opsgenie-action-type.md)
* [PagerDuty](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/pagerduty-action-type.md)
* [Server log](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/server-log-action-type.md)
* [{{sn-itom}}](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/servicenow-itom-action-type.md)
* [{{sn-itsm}}](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/servicenow-action-type.md)
* [{{sn-sir}}](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/servicenow-sir-action-type.md)
* [Slack](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/slack-action-type.md)
* [{{swimlane}}](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/swimlane-action-type.md)
* [Torq](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/torq-action-type.md)
* [{{webhook}}](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/webhook-action-type.md)
* [xMatters](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/xmatters-action-type.md)

::::{note}
Some connector types are paid commercial features, while others are free. For a comparison of the Elastic subscription levels, go to [the subscription page](https://www.elastic.co/subscriptions).

::::


After you select a connector, you must set the action frequency. You can choose to create a summary of alerts on each check interval or on a custom interval. For example, send email notifications that summarize the new, ongoing, and recovered alerts each hour:

:::{image} ../../../images/observability-action-alert-summary.png
:alt: Action types
:class: screenshot
:::

Alternatively, you can set the action frequency such that you choose how often the action runs (for example, at each check interval, only when the alert status changes, or at a custom action interval). In this case, you define precisely when the alert is triggered by selecting a specific threshold condition: `Alert`, `Warning`, or `Recovered` (a value that was once above a threshold has now dropped below it).

:::{image} ../../../images/observability-infrastructure-threshold-run-when-selection.png
:alt: Configure when an alert is triggered
:class: screenshot
:::

You can also further refine the conditions under which actions run by specifying that actions only run they match a KQL query or when an alert occurs within a specific time frame:

* **If alert matches query**: Enter a KQL query that defines field-value pairs or query conditions that must be met for notifications to send. The query only searches alert documents in the indices specified for the rule.
* **If alert is generated during timeframe**: Set timeframe details. Notifications are only sent if alerts are generated within the timeframe you define.

:::{image} ../../../images/observability-conditional-alerts.png
:alt: Configure a conditional alert
:class: screenshot
:::


## Action variables [_action_variables_3]

Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

:::{image} ../../../images/observability-infrastructure-threshold-alert-default-message.png
:alt: Default notification message for infrastructure threshold rules with open "Add variable" popup listing available action variables
:class: screenshot
:::

The following variables are specific to this rule type. You an also specify [variables common to all rules](../../../explore-analyze/alerts-cases/alerts/rule-action-variables.md).

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
:   The value of the metric in the specified condition. Usage: (`ctx.value.condition0`, `ctx.value.condition1`, and so on)

`context.viewInAppUrl`
:   Link to the alert source.


## Settings [infra-alert-settings]

With infrastructure threshold rules, it’s not possible to set an explicit index pattern as part of the configuration. The index pattern is instead inferred from **Metrics indices** on the [Settings](../../../solutions/observability/infra-and-hosts/configure-settings.md) page of the {{infrastructure-app}}.

With each execution of the rule check, the **Metrics indices** setting is checked, but it is not stored when the rule is created.

The **Timestamp** field that is set under **Settings** determines which field is used for timestamps in queries.

