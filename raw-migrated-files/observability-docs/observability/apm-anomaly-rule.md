---
navigation_title: "APM Anomaly"
---

# APM Anomaly rule [apm-anomaly-rule]


::::{important}
To use the APM Anomaly rule, you have to enable [machine learning](../../../solutions/observability/apps/integrate-with-machine-learning.md#create-ml-integration), which requires an [appropriate license](https://www.elastic.co/subscriptions).

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

* [D3 Security](https://www.elastic.co/guide/en/kibana/current/d3security-action-type.html)
* [Email](https://www.elastic.co/guide/en/kibana/current/email-action-type.html)
* [{{ibm-r}}](https://www.elastic.co/guide/en/kibana/current/resilient-action-type.html)
* [Index](https://www.elastic.co/guide/en/kibana/current/index-action-type.html)
* [Jira](https://www.elastic.co/guide/en/kibana/current/jira-action-type.html)
* [Microsoft Teams](https://www.elastic.co/guide/en/kibana/current/teams-action-type.html)
* [Observability AI Assistant connector](https://www.elastic.co/guide/en/kibana/current/obs-ai-assistant-action-type.html)
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

The following variables are specific to this rule type. You an also specify [variables common to all rules](../../../explore-analyze/alerts/kibana/rule-action-variables.md).

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

