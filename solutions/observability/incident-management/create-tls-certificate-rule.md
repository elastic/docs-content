---
navigation_title: TLS certificate
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/tls-certificate-alert.html
applies_to:
  stack: ga
  serverless: unavailable 
products:
  - id: observability
---

# Create a TLS certificate rule [tls-certificate-alert]


In {{kib}}, you can create a rule that notifies you when one or more of your monitors has a TLS certificate expiring within a specified threshold, or when it exceeds an age limit.

There are two types of TLS certificate rule:

* [Synthetics TLS certificate rule](#tls-rule-synthetics) for use with [Elastic Synthetics](/solutions/observability/synthetics/index.md).
* [Uptime TLS rule](#tls-rule-uptime) for use with the {{uptime-app}}.

  :::{admonition} Deprecated in 8.15.0
  Uptime was deprecated in 8.15.0. Use Synthetics instead.
  :::


## Synthetics TLS certificate rule [tls-rule-synthetics]

Within the Synthetics UI, create a **TLS certificate** rule to receive notifications based on errors and outages.


### Conditions [tls-rule-synthetics-conditions]

You can specify the following thresholds for your rule:

|     |     |
| --- | --- |
| **Expiration threshold** | The `HAS A CERTIFICATE EXPIRING WITHIN DAYS` condition specifies when you are notifiedabout certificates that are approaching expiration dates. |
| **Age limit** | The `OR OLDER THAN DAYS` condition specifies when you are notified about certificatesthat have been valid for too long. |

The **Rule schedule** defines how often to evaluate the condition.

You can also set **Advanced options** such as the number of consecutive runs that must meet the rule conditions before an alert occurs.

In this example, the conditions are met when any of the TLS certificates on sites we’re monitoring is expiring within 30 days or is older than 730 days. These conditions are evaluated every 6 hours, and you will only receive an alert when the conditions are met three times consecutively.

:::{image} /solutions/images/observability-tls-rule-synthetics-conditions.png
:alt: Conditions and advanced options defining a Synthetics TLS certificate rule
:screenshot:
:::


### Action types [tls-rule-synthetics-action-types]

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

:::{image} /solutions/images/observability-tls-rule-synthetics-action-types-summary.png
:alt: tls rule synthetics action types summary
:screenshot:
:::

Alternatively, you can set the action frequency such that you choose how often the action runs (for example, at each check interval, only when the alert status changes, or at a custom action interval). In this case, you must also select the specific threshold condition that affects when actions run: the *Synthetics TLS certificate* changes or when it is *Recovered* (went from down to up).

:::{image} /solutions/images/observability-tls-rule-synthetics-action-types-each-alert.png
:alt: tls rule synthetics action types each alert
:screenshot:
:::

You can also further refine the conditions under which actions run by specifying that actions only run when they match a KQL query or when an alert occurs within a specific time frame:

* **If alert matches query**: Enter a KQL query that defines field-value pairs or query conditions that must be met for notifications to send. The query only searches alert documents in the indices specified for the rule.
* **If alert is generated during timeframe**: Set timeframe details. Notifications are only sent if alerts are generated within the timeframe you define.

:::{image} /solutions/images/observability-tls-rule-synthetics-action-types-more-options.png
:alt: tls rule synthetics action types more options
:screenshot:
:::


#### Action variables [tls-rule-synthetics-action-variables]

Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

:::{image} /solutions/images/observability-tls-rule-synthetics-action-variables.png
:alt: tls rule synthetics action variables
:screenshot:
:::

The following variables are specific to this rule type. You an also specify [variables common to all rules](/explore-analyze/alerts-cases/alerts/rule-action-variables.md).

`context.checkedAt`
:   Timestamp of the monitor run.

`context.hostName`
:   Hostname of the location from which the check is performed.

`context.labels`
:   Labels associated with the monitor.

`context.lastErrorMessage`
:   Monitor last error message.

`context.lastErrorStack`
:   Monitor last error stack trace.

`context.locationId`
:   Location ID from which the check is performed.

`context.locationName`
:   Location name from which the check is performed.

`context.locationNames`
:   Location names from which the checks are performed.

`context.monitorType`
:   Type (for example, HTTP/TCP) of the monitor.

`context.monitorUrl`
:   URL of the monitor.

`context.reason`
:   A concise description of the reason for the alert.

`context.recoveryReason`
:   A concise description of the reason for the recovery.

`context.serviceName`
:   Service name associated with the monitor.

`context.status`
:   Monitor status (for example, "down").

`context.viewInAppUrl`
:   Open alert details and context in Synthetics app.


## Uptime TLS rule [tls-rule-uptime]

```{applies_to}
stack: deprecated 8.15.0
serverless: unavailable
```

::::{admonition} Deprecated in 8.15.0.
:class: warning

Use [Synthetic monitoring](/solutions/observability/synthetics/index.md) instead of the {{uptime-app}}.
::::


Within the {{uptime-app}}, create a **TLS certificate** rule to receive notifications based on errors and outages.


### Filters [tls-rule-uptime-filters]

The **Filter by** section controls the scope of the rule. The rule will only check monitors that match the filters defined in this section.


### Conditions [tls-alert-conditions]

You can specify the following thresholds for your rule:

|     |     |
| --- | --- |
| **Expiration threshold** | The `HAS A CERTIFICATE EXPIRING WITHIN DAYS` threshold specifies when you are notifiedabout certificates that are approaching expiration dates. |
| **Age limit** | The `OR OLDER THAN DAYS` threshold specifies when you are notified about certificatesthat have been valid for too long. |

In this example, the conditions are met when any of the TLS certificates on sites we’re monitoring is expiring within 30 days or is older than 730 days. These conditions are evaluated every 6 hours, and you will only receive an alert when the conditions are met three times consecutively.

:::{image} /solutions/images/observability-tls-rule-uptime-conditions.png
:alt: Monitor status rule
:screenshot:
:::


### Action types [action-types-certs]

Extend your rules by connecting them to actions that use the following supported built-in integrations. Actions are {{kib}} services or integrations with third-party systems that run as background tasks on the {{kib}} server when rule conditions are met.

You can configure action types on the [Settings](/solutions/observability/uptime/configure-settings.md#configure-uptime-alert-connectors) page.

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

:::{image} /solutions/images/observability-tls-rule-uptime-action-types-summary.png
:alt: tls rule uptime action types summary
:screenshot:
:::

Alternatively, you can set the action frequency such that you choose how often the action runs (for example, at each check interval, only when the alert status changes, or at a custom action interval). In this case, you must also select the specific threshold condition that affects when actions run: *Uptime TLS Alert* or *Recovered* (went from down to up).

:::{image} /solutions/images/observability-tls-rule-uptime-action-types-each-alert.png
:alt: tls rule uptime action types each alert
:screenshot:
:::

You can also further refine the conditions under which actions run by specifying that actions only run when they match a KQL query or when an alert occurs within a specific time frame:

* **If alert matches query**: Enter a KQL query that defines field-value pairs or query conditions that must be met for notifications to send. The query only searches alert documents in the indices specified for the rule.
* **If alert is generated during timeframe**: Set timeframe details. Notifications are only sent if alerts are generated within the timeframe you define.

:::{image} /solutions/images/observability-tls-rule-uptime-action-types-more-options.png
:alt: tls rule uptime action types more options
:screenshot:
:::


#### Action variables [action-variables-certs]

Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

:::{image} /solutions/images/observability-tls-rule-uptime-default-message.png
:alt: Default notification message for TLS rules with open "Add variable" popup listing available action variables
:screenshot:
:::

The following variables are specific to this rule type. You an also specify [variables common to all rules](/explore-analyze/alerts-cases/alerts/rule-action-variables.md).

`context.agingCommonNameAndDate`
:   The common names and expiration date/time of the detected certs.

`context.agingCount`
:   The number of detected certs that are becoming too old.

`context.alertDetailsUrl`
:   Link to the alert troubleshooting view for further context and details. This will be an empty string if the `server.publicBaseUrl` is not configured.

`context.count`
:   The number of certs detected by the alert executor.

`context.currentTriggerStarted`
:   Timestamp indicating when the current trigger state began, if alert is triggered.

`context.expiringCommonNameAndDate`
:   The common names and expiration date/time of the detected certs.

`context.expiringCount`
:   The number of expiring certs detected by the alert.

`context.firstCheckedAt`
:   Timestamp indicating when this alert first checked.

`context.firstTriggeredAt`
:   Timestamp indicating when the alert first triggered.

`context.isTriggered`
:   Flag indicating if the alert is currently triggering.

`context.lastCheckedAt`
:   Timestamp indicating the alert’s most recent check time.

`context.lastResolvedAt`
:   Timestamp indicating the most recent resolution time for this alert.

`context.lastTriggeredAt`
:   Timestamp indicating the alert’s most recent trigger time.
