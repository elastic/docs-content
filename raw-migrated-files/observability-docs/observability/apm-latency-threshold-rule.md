---
navigation_title: "Latency threshold"
---

# Latency threshold rule [apm-latency-threshold-rule]


Alert when the latency or failed transaction rate is abnormal. Threshold rules can be as broad or as granular as you’d like, enabling you to define exactly when you want to be alerted—​whether that’s at the environment level, service name level, transaction type level, and/or transaction name level.


## Filter and conditions [_filter_and_conditions]

Filter the transactions coming from your application to apply an Latency threshold rule to specific services (`SERVICE`), environments (`ENVIRONMENT`), transaction types (`TYPE`), or transaction names (`NAME`). Alternatively, you can use a [KQL filter](../../../explore-analyze/query-filter/languages/kql.md) to limit the scope of the alert by toggling on the **Use KQL Filter** option.

Then, you can specify which conditions should result in an alert. This includes specifying:

* Which latency measurement to evaluate against (`WHEN`): average, 95th percentile, or 99th percentile.
* The minimum value of the chosen latency measurement (`IS ABOVE`) in milliseconds.
* The timeframe in which the failures must occur (`FOR THE LAST`) in seconds, minutes, hours, or days.

:::::{admonition} Example
This example creates a rule for all `request` transactions coming from production that would result in an alert when the average latency is above 1 second (1000ms) for the last 30 minutes:

:::{image} ../../../images/observability-apm-latency-threshold-rule-filters-conditions.png
:alt: apm latency threshold rule filters conditions
:::

Alternatively, you can use a KQL filter to limit the scope of the alert:

1. Toggle on **Use KQL Filter**.
2. Add a filter:

    ```txt
    service.environment:"Production" and transaction.type:"request"
    ```


:::::



## Groups [_groups_3]

Set one or more **group alerts by** fields for custom threshold rules to perform a composite aggregation against the selected fields. When any of these groups match the selected rule conditions, an alert is triggered *per group*.

When you select multiple groupings, the group name is separated by commas.

When you select **Alert me if a group stops reporting data**, the rule is triggered if a group that previously reported metrics does not report them again over the expected time period.

::::{admonition} Example: Group by one field
If you group alerts by the `service.name` field and there are two services (`Service A` and `Service B`), when `Service A` matches the conditions but `Service B` doesn’t, one alert is triggered for `Service A`. If both groups match the conditions, alerts are triggered for both groups.

::::


::::{admonition} Example: Group by multiple fields
If you group alerts by both the `service.name` and `service.environment` fields, and there are two services (`Service A` and `Service B`) and two environments (`Production` and `Staging`), the composite aggregation forms multiple groups.

If the `Service A, Production` group matches the rule conditions, but the `Service B, Staging` group doesn’t, one alert is triggered for `Service A, Production`.

::::



## Rule schedule [_rule_schedule_4]

Define how often to evaluate the condition in seconds, minutes, hours, or days. Checks are queued so they run as close to the defined value as capacity allows.


## Advanced options [_advanced_options_4]

Optionally define an **Alert delay**. An alert will only occur when the specified number of consecutive runs meet the rule conditions.


## Actions [_actions_4]

Extend your rules by connecting them to actions that use built-in integrations.


### Action types [_action_types_4]

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



### Action frequency [_action_frequency_4]

After you select a connector, you must set the action frequency. You can choose to create a summary of alerts on each check interval or on a custom interval. Alternatively, you can set the action frequency such that you choose how often the action runs (for example, at each check interval, only when the alert status changes, or at a custom action interval).

You can also further refine the conditions under which actions run by specifying that actions only run they match a KQL query or when an alert occurs within a specific time frame:

* **If alert matches query**: Enter a KQL query that defines field-value pairs or query conditions that must be met for notifications to send. The query only searches alert documents in the indices specified for the rule.
* **If alert is generated during timeframe**: Set timeframe details. Notifications are only sent if alerts are generated within the timeframe you define.


### Action variables [_action_variables_4]

A default message is provided as a starting point for your alert. If you want to customize the message, add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

::::{tip}
To add variables to alert messages, use [Mustache](https://mustache.github.io/) template syntax, for example `{{variable.name}}`.
::::


:::{image} ../../../images/observability-apm-latency-threshold-rule-action-variables.png
:alt: apm latency threshold rule action variables
:::

The following variables are specific to this rule type. You an also specify [variables common to all rules](../../../explore-analyze/alerts-cases/alerts/rule-action-variables.md).

`context.alertDetailsUrl`
:   Link to the alert troubleshooting view for further context and details. This will be an empty string if the server.publicBaseUrl is not configured.

`context.environment`
:   The transaction type the alert is created for.

`context.interval`
:   The length and unit of the time period where the alert conditions were met.

`context.reason`
:   A concise description of the reason for the alert.

`context.serviceName`
:   The service the alert is created for.

`context.threshold`
:   Any trigger value above this value will cause the alert to fire.

`context.transactionName`
:   The transaction name the alert is created for.

`context.transactionType`
:   The transaction type the alert is created for.

`context.triggerValue`
:   The value that breached the threshold and triggered the alert.

`context.viewInAppUrl`
:   Link to the alert source.

