---
navigation_title: "SLO burn rate"
---

# Create a service-level objective (SLO) burn rate rule [slo-burn-rate-alert]


::::{important}
To create and manage SLOs, you need an [appropriate license](https://www.elastic.co/subscriptions), an {{es}} cluster with both `transform` and `ingest` [node roles](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html#node-roles) present, and [SLO access](../../../solutions/observability/incident-management/configure-service-level-objective-slo-access.md) must be configured.

::::


You can create a SLO burn rate rule to get alerts when the burn rate is above a defined threshold for two different lookback periods: a long period and a short period that is 1/12th of the long period. For example, if your long lookback period is one hour, your short lookback period is five minutes.

For each lookback period, the burn rate is computed as the error rate divided by the error budget. When the burn rates for both periods surpass the threshold, an alert is triggered.

::::{note}
When you use the UI to create an SLO, a default SLO burn rate alert rule is created automatically. The burn rate rule will use the default configuration and no connector. You must configure a connector if you want to receive alerts for SLO breaches.
::::


To create an SLO burn rate rule, go to **Observability → SLOs**. Click the more options icon to the right of the SLO you want to add a burn rate rule for, and select **Create new alert rule** from the drop-down menu:

:::{image} ../../../images/observability-create-new-alert-rule-menu.png
:alt: create new alert rule menu
:class: screenshot
:::

To create your SLO burn rate rule:

1. Set your long lookback period under **Lookback period (hours)**. Your short lookback period is set automatically.
2. Set your **Burn rate threshold**. Under this field, you’ll see how long you have until your error budget is exhausted.
3. Set how often the condition is evaluated in the **Check every** field.
4. Optionally, change the number of consecutive runs that must meet the rule conditions before an alert occurs in the **Advanced options**.


## Action types [action-types-slo]

Extend your rules by connecting them to actions that use the following supported built-in integrations. Actions are {{kib}} services or integrations with third-party systems that run as background tasks on the {{kib}} server when rule conditions are met.

You can configure action types on the [Settings](../../../solutions/observability/apps/configure-settings.md#configure-uptime-alert-connectors) page.

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


After you select a connector, you must set the action frequency. You can choose to create a **Summary of alerts** on each check interval or on a custom interval. For example, you can send email notifications that summarize the new, ongoing, and recovered alerts every twelve hours.

Alternatively, you can set the action frequency to **For each alert** and specify the conditions each alert must meet for the action to run. For example, you can send an email only when the alert status changes to critical.

:::{image} ../../../images/observability-slo-action-frequency.png
:alt: Configure when a rule is triggered
:class: screenshot
:::


## Action variables [action-variables-slo]

Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

:::{image} ../../../images/observability-slo-action-variables.png
:alt: Action variables with default SLO message
:class: screenshot
:::

The following variables are specific to this rule type. You an also specify [variables common to all rules](../../../explore-analyze/alerts/kibana/rule-action-variables.md).

`context.alertDetailsUrl`
:   Link to the alert troubleshooting view for further context and details. This will be an empty string if the `server.publicBaseUrl` is not configured.

`context.burnRateThreshold`
:   The burn rate threshold value.

`context.longWindow`
:   The window duration with the associated burn rate value.

`context.reason`
:   A concise description of the reason for the alert.

`context.shortWindow`
:   The window duration with the associated burn rate value.

`context.sloId`
:   The SLO unique identifier.

`context.sloInstanceId`
:   The SLO instance id.

`context.sloName`
:   The SLO name.

`context.timestamp`
:   A timestamp of when the alert was detected.

`context.viewInAppUrl`
:   The URL to the SLO details page to help with further investigation.


## Alert recovery [recovery-variables-slo]

To receive a notification when the alert recovers, select **Run when Recovered**. Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

:::{image} ../../../images/observability-duration-anomaly-alert-recovery.png
:alt: Default recovery message for Uptime duration anomaly rules with open "Add variable" popup listing available action variables
:class: screenshot
:::


## Next steps [slo-creation-next-steps]

Learn how to view alerts and triage SLO burn rate breaches:

* [View alerts](../../../solutions/observability/incident-management/view-alerts.md)
* [Triage SLO burn rate breaches](../../../solutions/observability/incident-management/triage-slo-burn-rate-breaches.md)

