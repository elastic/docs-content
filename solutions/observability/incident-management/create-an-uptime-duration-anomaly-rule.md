---
navigation_title: "Uptime duration anomaly"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/duration-anomaly-alert.html
---



# Create an uptime duration anomaly rule [duration-anomaly-alert]


Within the {{uptime-app}}, create an **Uptime duration anomaly** rule to receive notifications based on the response durations for all of the geographic locations of each monitor. When a monitor runs for an unusual amount of time, at a particular time, an anomaly is recorded and highlighted on the [Monitor duration](../apps/inspect-uptime-duration-anomalies.md) chart.


## Conditions [duration-alert-conditions]

For each rule, you can configure which severity level triggers the alert. The default level is `critical`.

The *anomaly score* is a value from `0` to `100`, which indicates the significance of the anomaly compared to previously seen anomalies. The highly anomalous values are shown in red and the low scored values are indicated in blue.

|     |     |
| --- | --- |
| **warning** | Score `0` and above. |
| **minor** | Score `25` and above. |
| **major** | Score `50` and above. |
| **critical** | Score `75` and above. |

:::{image} ../../../images/observability-response-durations-alert.png
:alt: Uptime response duration rule
:class: screenshot
:::


## Action types [action-types-duration]

Extend your rules by connecting them to actions that use the following supported built-in integrations. Actions are {{kib}} services or integrations with third-party systems that run as background tasks on the {{kib}} server when rule conditions are met.

You can configure action types on the [Settings](../apps/configure-settings.md#configure-uptime-alert-connectors) page.

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


After you select a connector, you must set the action frequency. You can choose to create a summary of alerts on each check interval or on a custom interval. For example, send email notifications that summarize the new, ongoing, and recovered alerts every twelve hours:

:::{image} ../../../images/observability-duration-anomaly-alert-summary.png
:alt: Action types
:class: screenshot
:::

Alternatively, you can set the action frequency such that you choose how often the action runs (for example, at each check interval, only when the alert status changes, or at a custom action interval). In this case, you must also select the specific threshold condition that affects when actions run: `Uptime Duration Anomaly` or `Recovered`.

:::{image} ../../../images/observability-duration-anomaly-run-when-selection.png
:alt: Configure when a rule is triggered
:class: screenshot
:::


## Action variables [action-variables-duration]

Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

:::{image} ../../../images/observability-duration-anomaly-alert-default-message.png
:alt: Default notification message for Uptime duration anomaly rules with open "Add variable" popup listing available action variables
:class: screenshot
:::


## Alert recovery [recovery-variables-duration]

To receive a notification when the alert recovers, select **Run when Recovered**. Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

:::{image} ../../../images/observability-duration-anomaly-alert-recovery.png
:alt: Default recovery message for Uptime duration anomaly rules with open "Add variable" popup listing available action variables
:class: screenshot
:::

