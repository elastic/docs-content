---
navigation_title: "APM Anomaly"
---

# APM Anomaly rule [apm-anomaly-rule]


::::{important}
To use the APM Anomaly rule, you have to enable [machine learning](../../../solutions/observability/apps/integrate-with-machine-learning.md#observability-apm-integrate-with-machine-learning-enable-anomaly-detection), which requires an [appropriate license](https://www.elastic.co/subscriptions).

::::


APM Anomaly rules trigger when the latency, throughput, or failed transaction rate of a service is abnormal.


## Filters and conditions [apm-anomaly-rule-filters-conditions]

Because some parts of an application may be more important than others, you might have a different tolerance for abnormal performance across services in your application. You can filter the services in your application to apply an APM Anomaly rule to specific services (`SERVICE`), transaction types (`TYPE`), and environments (`ENVIRONMENT`).

Then, you can specify which conditions should result in an alert. This includes specifying:

* The types of anomalies that are detected (`DETECTOR TYPES`): `latency`, `throughput`, and/or `failed transaction rate`.
* The severity level (`HAS ANOMALY WITH SEVERITY`): `critical`, `major`, `minor`, `warning`.

:::::{admonition} Example
This example creates a rule for all production services that would result in an alert when a critical latency anomaly is detected:

:::{image} ../../../images/observability-apm-anomaly-rule-filters-conditions.png
:alt: apm anomaly rule filters conditions
:::

:::::



## Rule schedule [_rule_schedule]

Define how often to evaluate the condition in seconds, minutes, hours, or days. Checks are queued so they run as close to the defined value as capacity allows.


## Advanced options [_advanced_options]

Optionally define an **Alert delay**. An alert will only occur when the specified number of consecutive runs meet the rule conditions.


## Actions [_actions]

Extend your rules by connecting them to actions that use built-in integrations.


### Action types [_action_types]

Supported built-in integrations include:

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



### Action frequency [_action_frequency]

After you select a connector, you must set the action frequency. You can choose to create a summary of alerts on each check interval or on a custom interval. Alternatively, you can set the action frequency such that you choose how often the action runs (for example, at each check interval, only when the alert status changes, or at a custom action interval).

You can also further refine the conditions under which actions run by specifying that actions only run they match a KQL query or when an alert occurs within a specific time frame:

* **If alert matches query**: Enter a KQL query that defines field-value pairs or query conditions that must be met for notifications to send. The query only searches alert documents in the indices specified for the rule.
* **If alert is generated during timeframe**: Set timeframe details. Notifications are only sent if alerts are generated within the timeframe you define.


### Action variables [apm-anomaly-rule-action-variables]

A default message is provided as a starting point for your alert. If you want to customize the message, add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

::::{tip}
To add variables to alert messages, use [Mustache](https://mustache.github.io/) template syntax, for example `{{variable.name}}`.
::::


:::{image} ../../../images/observability-apm-anomaly-rule-action-variables.png
:alt: apm anomaly rule action variables
:::

The following variables are specific to this rule type. You an also specify [variables common to all rules](../../../explore-analyze/alerts-cases/alerts/rule-action-variables.md).

`context.alertDetailsUrl`
:   Link to the alert troubleshooting view for further context and details. This will be an empty string if the server.publicBaseUrl is not configured.

`context.environment`
:   The transaction type the alert is created for.

`context.reason`
:   A concise description of the reason for the alert.

`context.serviceName`
:   The service the alert is created for.

`context.threshold`
:   Any trigger value above this value will cause the alert to fire.

`context.transactionType`
:   The transaction type the alert is created for.

`context.triggerValue`
:   The value that breached the threshold and triggered the alert.

`context.viewInAppUrl`
:   Link to the alert source.

