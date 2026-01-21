---
navigation_title: Metric threshold
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/metrics-threshold-alert.html
applies_to:
  stack: ga
  serverless: unavailable 
products:
  - id: observability
---



# Create a metric threshold rule [metrics-threshold-alert]


Based on the metrics that are listed on the **Metrics Explorer** page within the {{infrastructure-app}}, you can create a threshold rule to notify you when a metric has reached or exceeded a value for a specific time period.

Additionally, each rule can be defined using multiple conditions that combine metrics and thresholds to create precise notifications.

::::{tip}
When you create this rule on the **Metrics Explorer** page, the rule is automatically populated with the same parameters as the page. If you’ve chosen a **graph per** value, your rule is preconfigured to monitor and notify about each individual graph displayed on the page.

You can also create a rule based on a single graph. On the **Metrics Explorer** page, click **Alerts and rules** → **Create alert**. The condition and filter sections of the threshold rule are automatically populated.

::::



## Metric conditions [metrics-conditions]

Conditions for each rule can be applied to specific metrics that you select. You can select the aggregation type (refer to [Aggregation options](aggregation-options.md)), the metric, and by including a warning threshold value, you can be alerted on multiple threshold values based on severity scores. To help you determine which thresholds are meaningful to you, the preview charts provide a visualization.

In this example, the conditions state that you will receive a critical alert for hosts with a CPU usage of 120% or above and a warning alert if CPU usage is 100% or above. Note that you will receive an alert only if memory usage is 20% or above, as per the second condition.

:::{image} /solutions/images/observability-metrics-alert.png
:alt: Metric threshold alert
:screenshot:
:::

When you select **Alert me if there’s no data**, the rule is triggered if the metrics don’t report any data over the expected time period, or if the rule fails to query {{es}}.


## Filtering and grouping [filtering-and-grouping]

:::{image} /solutions/images/observability-metrics-alert-filters-and-group.png
:alt: Metric threshold filter and group fields
:screenshot:
:::

The **Filters** control the scope of the rule. If used, the rule will only evaluate metric data that matches the query in this field. In this example, the rule will only alert on metrics reported from a Cloud region called `us-east`.

::::{note}
If you've made a rule with the [create rule API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-alerting-rule-id) and added Query DSL filters using the `filterQuery` parameter, the filters won't appear in the UI for editing a rule. As a workaround, manually re-add the filters through the UI and save the rule. As you're modifying the rule's filters from the UI, be mindful of the following:

- The **Filter** field only accepts KQL syntax, meaning you may need to manually convert your Query DSL filters to KQL.
- After you save the rule, filters you've added to the **Filter** field are converted appropriately and specified in the rule's `filterQuery` parameter.
::::

The **Group alerts by** creates an instance of the alert for every unique value of the `field` added. For example, you can create a rule per host or every mount point of each host. You can also add multiple fields. In this example, the rule will individually track the status of each `host.name` in your infrastructure. You will only receive an alert about `host-1`, if `host.name: host-1` passes the threshold, but `host-2` and `host-3` do not.

When you select **Alert me if a group stops reporting data**, the rule is triggered if a group that previously reported metrics does not report them again over the expected time period.

::::{important}
If you include the same field in both your **Filter** and your **Group by**, you may receive fewer results than you’re expecting. For example, if you filter by `cloud.region: us-east`, then grouping by `cloud.region` will have no effect because the filter query can only match one region.

::::


In the **Advanced options**, you can change the number of consecutive runs that must meet the rule conditions before an alert occurs. The default value is `1`.


## Action types [action-types-metrics]

Extend your rules by connecting them to actions that use the following supported built-in integrations.

* [D3 Security](kibana://reference/connectors-kibana/d3security-action-type.md)
* [Email](kibana://reference/connectors-kibana/email-action-type.md)
* [{{ibm-r}}](kibana://reference/connectors-kibana/resilient-action-type.md)
* [Index](kibana://reference/connectors-kibana/index-action-type.md)
* [Jira](kibana://reference/connectors-kibana/jira-action-type.md)
* [Microsoft Teams](kibana://reference/connectors-kibana/teams-action-type.md)
* [Observability AI Assistant connector](kibana://reference/connectors-kibana/obs-ai-assistant-action-type.md)
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


After you select a connector, you must set the action frequency. You can choose to create a summary of alerts on each check interval or on a custom interval. For example, send email notifications that summarize the new, ongoing, and recovered alerts each hour:

:::{image} /solutions/images/observability-action-alert-summary.png
:alt: Action types
:screenshot:
:::

Alternatively, you can set the action frequency such that you choose how often the action runs (for example, at each check interval, only when the alert status changes, or at a custom action interval). In this case, you must also select the specific threshold condition that affects when actions run: `Alert`, `Warning`, `No data`, or `Recovered` (a value that was once above a threshold has now dropped below it).

:::{image} /solutions/images/observability-metrics-threshold-run-when-selection.png
:alt: Configure when a rule is triggered
:screenshot:
:::

You can also further refine the conditions under which actions run by specifying that actions only run when they match a KQL query or when an alert occurs within a specific time frame:

* **If alert matches query**: Enter a KQL query that defines field-value pairs or query conditions that must be met for notifications to send. The query only searches alert documents in the indices specified for the rule.
* **If alert is generated during timeframe**: Set timeframe details. Notifications are only sent if alerts are generated within the timeframe you define.

:::{image} /solutions/images/observability-metric-threshold-conditional-alerts.png
:alt: Configure a conditional alert
:screenshot:
:::


## Action variables [_action_variables_6]

Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

:::{image} /solutions/images/observability-metrics-threshold-alert-default-message.png
:alt: Default notification message for metric threshold rules with open "Add variable" popup listing available action variables
:screenshot:
:::

The following variables are specific to this rule type. You an also specify [variables common to all rules](/explore-analyze/alerts-cases/alerts/rule-action-variables.md).

`context.alertDetailsUrl`
:   Link to the alert troubleshooting view for further context and details. This will be an empty string if the `server.publicBaseUrl` is not configured.

`context.alertState`
:   Current state of the alert.

`context.cloud`
:   The cloud object defined by ECS if available in the source.

`context.container`
:   The container object defined by ECS if available in the source.

`context.group`
:   Name of the group(s) reporting data. For accessing each group key, use `context.groupByKeys`.

`context.groupByKeys`
:   The object containing groups that are reporting data.

`context.grouping` {applies_to}`stack: ga 9.2`
:   The object containing groups that are reporting data.

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

`context.originalAlertStateWasNO_DATA`
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


## Settings [metrics-alert-settings]

With metric threshold rules, it’s not possible to set an explicit index pattern as part of the configuration. The index pattern is instead inferred from **Metrics indices** on the [Settings](../infra-and-hosts/configure-settings.md) page of the {{infrastructure-app}}.

With each execution of the rule check, the **Metrics indices** setting is checked, but it is not stored when the rule is created.

The **Timestamp** field that is set under **Settings** determines which field is used for timestamps in queries.
