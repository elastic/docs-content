---
navigation_title: Monitor Status
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-status-alert.html
  - https://www.elastic.co/guide/en/serverless/current/observability-monitor-status-alert.html
products:
  - id: observability
  - id: cloud-serverless
---


# Create a synthetic monitor status rule [observability-monitor-status-alert]


Within the Synthetics UI, create a **Monitor Status** rule to receive notifications based on errors and outages.

1. To access this page, go to **Synthetics** → **Overview**.
2. At the top of the page, click **Alerts and rules** → **Monitor status rule** → **Create status rule**.

## Filters [observability-monitor-status-alert-filters]

The **Filter by** section controls the scope of the rule. The rule will only check monitors that match the filters defined in this section. In this example, the rule will only alert on `browser` monitors located in `Asia/Pacific - Japan`.

:::{image} /solutions/images/serverless-synthetic-monitor-filters.png
:alt: Filter by section of the Synthetics monitor status rule
:screenshot:
:::


## Conditions [observability-monitor-status-alert-conditions]

Conditions for each rule will be applied to all monitors that match the filters in the [**Filter by** section](/solutions/observability/incident-management/create-monitor-status-rule.md#observability-monitor-status-alert-filters). You can choose the number of times the monitor has to be down relative to either a number of checks run or a time range in which checks were run, and the minimum number of locations the monitor must be down in.

::::{note}
Retests are included in the number of checks.

::::


The **Rule schedule** defines how often to evaluate the condition. Note that checks are queued, and they run as close to the defined value as capacity allows. For example, if a check is scheduled to run every 2 minutes, but the check takes longer than 2 minutes to run, a check will not run until the previous check has finished.

You can also set **Advanced options** such as the number of consecutive runs that must meet the rule conditions before an alert occurs.

In this example, the conditions will be met any time a `browser` monitor is down `3` of the last `5` times the monitor ran across any locations that match the filter. These conditions will be evaluated every minute, and you will only receive an alert when the conditions are met three times consecutively.

:::{image} /solutions/images/serverless-synthetic-monitor-conditions.png
:alt: Filters and conditions defining a Synthetics monitor status rule
:screenshot:
:::


## Action types [observability-monitor-status-alert-action-types]

Extend your rules by connecting them to actions that use the following supported built-in integrations.

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


After you select a connector, you must set the action frequency. You can choose to create a summary of alerts on each check interval or on a custom interval. For example, send email notifications that summarize the new, ongoing, and recovered alerts each hour:

:::{image} /solutions/images/serverless-synthetic-monitor-action-types-summary.png
:alt: synthetic monitor action types summary
:screenshot:
:::

Alternatively, you can set the action frequency such that you choose how often the action runs (for example, at each check interval, only when the alert status changes, or at a custom action interval). In this case, you must also select the specific threshold condition that affects when actions run: the *Synthetics monitor status* changes or when it is *Recovered* (went from down to up).

:::{image} /solutions/images/serverless-synthetic-monitor-action-types-each-alert.png
:alt: synthetic monitor action types each alert
:screenshot:
:::

You can also further refine the conditions under which actions run by specifying that actions only run when they match a KQL query or when an alert occurs within a specific time frame:

* **If alert matches query**: Enter a KQL query that defines field-value pairs or query conditions that must be met for notifications to send. The query only searches alert documents in the indices specified for the rule.
* **If alert is generated during timeframe**: Set timeframe details. Notifications are only sent if alerts are generated within the timeframe you define.

:::{image} /solutions/images/serverless-synthetic-monitor-action-types-more-options.png
:alt: synthetic monitor action types more options
:screenshot:
:::


#### Action variables [observability-monitor-status-alert-action-variables]

Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

:::{image} /solutions/images/serverless-synthetic-monitor-action-variables.png
:alt: synthetic monitor action variables
:screenshot:
:::

The following variables are specific to this rule type. You an also specify [variables common to all rules](/explore-analyze/alerting/alerts/rule-action-variables.md).

`context.checkedAt`
:   Timestamp of the monitor run.

`context.hostName`
:   Hostname of the location from which the check is performed.

`context.lastErrorMessage`
:   Monitor last error message.

`context.locationId`
:   Location id from which the check is performed.

`context.locationName`
:   Location name from which the check is performed.

`context.locationNames`
:   Location names from which the checks are performed.

`context.message`
:   A generated message summarizing the status of monitors currently down.

`context.monitorId`
:   ID of the monitor.

`context.monitorName`
:   Name of the monitor.

`context.monitorTags`
:   Tags associated with the monitor.

`context.monitorType`
:   Type (for example, HTTP/TCP) of the monitor.

`context.monitorUrl`
:   URL of the monitor.

`context.reason`
:   A concise description of the reason for the alert.

`context.recoveryReason`
:   A concise description of the reason for the recovery.

`context.status`
:   Monitor status (for example, "down").

`context.viewInAppUrl`
:   Open alert details and context in Synthetics app.


## Uptime monitor status [monitor-status-alert-uptime]

```{applies_to}
stack: deprecated 8.15.0
serverless: unavailable
```

::::{warning}
**The Uptime app and the Uptime monitor status rule are deprecated as of version 8.15.0.**

If you are using the Uptime monitor status rule with the Uptime app, you should migrate the Uptime monitor and the Uptime monitor status rule to Elastic Synthetics and the Synthetics monitor rule.

If you are using the Uptime monitor status rule with a monitor created with Elastic Synthetics, you should migrate the Uptime monitor status rule to the Synthetics monitor rule. Learn how in [Migrate from the Uptime rule to the Synthetics rule](/solutions/observability/incident-management/create-monitor-status-rule.md#migrate-monitor-rule).

::::


Within the {{uptime-app}}, create a **Monitor Status** rule to receive notifications based on errors and outages.

1. To access this page, go to **{{observability}}** → **Uptime**.
2. At the top of the page, click **Alerts and rules** → **Create rule**.
3. Select **Monitor status rule**.

::::{tip}
If you already have a query in the overview page search bar, it’s populated here.

::::



### Conditions [status-alert-conditions]

You can specify the following thresholds for your rule.

|     |     |
| --- | --- |
| **Status check** | Receive alerts when a monitor goes down a specified number oftimes within a time range (seconds, minutes, hours, or days). |
| **Availability** | Receive alerts when a monitor goes below a specified availabilitythreshold within a time range (days, weeks, months, or years). |

Let’s create a rule for any monitor that shows `Down` more than three times in 10 minutes.

This rule covers all the monitors you have running. You can use a query to specify specific monitors, and you can also have different conditions for each one.

:::{image} /solutions/images/observability-monitor-status-alert.png
:alt: Monitor status rule
:screenshot:
:::

The final step when creating a rule is to select one or more actions to take when the alert is triggered.


### Action types [action-types-status]

You can extend your rules by connecting them to actions that use the following supported built-in integrations. Actions are {{kib}} services or integrations with third-party systems that run as background tasks on the {{kib}} server when rule conditions are met.

You can configure action types on the [Settings](/solutions/observability/uptime/configure-settings.md#configure-uptime-alert-connectors) page.

:::{image} /solutions/images/observability-uptime-alert-connectors.png
:alt: Uptime rule connectors
:screenshot:
:::

After you select a connector, you must set the action frequency. You can choose to create a summary of alerts on each check interval or on a custom interval. For example, send email notifications that summarize the new, ongoing, and recovered alerts each hour:

:::{image} /solutions/images/observability-action-alert-summary.png
:alt: Action frequency summary of alerts
:screenshot:
:::

Alternatively, you can set the action frequency such that you choose how often the action runs (for example, at each check interval, only when the alert status changes, or at a custom action interval). In this case, you must also select the specific threshold condition that affects when actions run: `Uptime Down Monitor` or `Recovered`.

:::{image} /solutions/images/observability-uptime-run-when-selection.png
:alt: Action frequency for each alert
:screenshot:
:::


### Action variables [action-variables-status]

Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

:::{image} /solutions/images/observability-monitor-status-alert-default-message.png
:alt: Default notification message for monitor status rules with open "Add variable" popup listing available action variables
:screenshot:
:::


### Alert recovery [recovery-variables-status]

To receive a notification when the alert recovers, select **Run when Recovered**. Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

:::{image} /solutions/images/observability-monitor-status-alert-recovery.png
:alt: Default recovery message for monitor status rules with open "Add variable" popup listing available action variables
:screenshot:
:::


## Migrate from the Uptime rule to the Synthetics rule [migrate-monitor-rule]

If you are currently using the Uptime monitor status with a monitor created with Elastic Synthetics, you should migrate the Uptime monitor status rule to:

* If you were using the Uptime rule for **synthetic monitor *status* checks**, you can recreate similar functionality using the [Synthetics monitor rule](/solutions/observability/incident-management/create-monitor-status-rule.md#migrate-monitor-rule-synthetics-rule).
* If you were using the Uptime rule for **synthetic monitor *availability* checks**, there is no equivalent in the Synthetics monitor rule. Instead, you can use the [Synthetics availability SLI](/solutions/observability/incident-management/create-monitor-status-rule.md#migrate-monitor-rule-synthetics-sli) to create similar functionality.


### Uptime status check to Synthetics monitor rule [migrate-monitor-rule-synthetics-rule]


#### Filters [monitor-status-alert-checks-filters]

The KQL syntax that you used in the Uptime monitor status rule is also valid in the **Filter by** section of the Synthetics monitor status rule. The Synthetics monitor status rule also offers dropdowns for several categories for easy filtering. However, you can still use KQL syntax for these categories if you prefer.


#### Conditions [monitor-status-alert-checks-conditions]

::::{note}
If you are using the *Uptime availability condition* refer to [Uptime availability check to Synthetics availability SLI](/solutions/observability/incident-management/create-monitor-status-rule.md#migrate-monitor-rule-synthetics-sli).

::::


If you’re using the Uptime status check condition, you can recreate similar effects using the following Synthetics monitor status rule condition equivalents:

|  | Uptime | Synthetics equivalent |
| --- | --- | --- |
| **Number of times the monitor is down** | `ANY MONITOR IS DOWN  >=` `{{number}}` times (for example, `ANY MONITOR IS DOWN  >=` `5` times) | `IS DOWN` `{{number}}` times (for example, `IS DOWN` `5` times) |
| **Timeframe** | `WITHIN last` `{{number}}` `{time range unit}` (for example, `WITHIN last` `15` `minutes`) | `WITHIN THE LAST` `{{number}}` `{time range unit}` (for example, `WITHIN THE LAST` `15` `minutes`) |


#### Actions [monitor-status-alert-checks-actions]

The default messages for the Uptime monitor status rule and Synthetics monitor status rule are different, but you can recreate similar messages using [Synthetics monitor status rule action variables](/solutions/observability/incident-management/create-monitor-status-rule.md#observability-monitor-status-alert-action-variables).


### Uptime availability check to Synthetics availability SLI [migrate-monitor-rule-synthetics-sli]

SLOs allow you to set clear, measurable targets for your service performance, based on factors like availability. The [Synthetics availability SLI](/solutions/observability/incident-management/create-an-slo.md#synthetics-availability-sli) is a service-level indicator (SLI) based on the availability of your synthetic monitors.


#### Filters [monitor-status-alert-checks-filters-uptime]

The KQL syntax that you used in the Uptime monitor status rule is also valid in the **Query filter** field of the Synthetics availability SLI.


#### Conditions [monitor-status-alert-checks-conditions-uptime]

Use the following Synthetics availability SLI fields to replace the Uptime monitor status rule’s availability conditions:

|  | Uptime | Synthetics equivalent |
| --- | --- | --- |
| **Number of checks that are down relative to all checks run** | `ANY MONITOR IS UP IN <` `{{percent}}` of checks (for example, `ANY MONITOR IS UP IN <` `90%` of checks) | **Target / SLO (%)** field (for example, `90%`) |
| **Timeframe** | `WITHIN THE LAST` `{{number}}` `{time range unit}` (for example, `WITHIN THE LAST` `30` `days`) | **Time window** and **Duration** fields (for example, Time window: `Rolling`, Duration: `30 days`) |


#### Actions [monitor-status-alert-checks-actions-uptime]

After creating a new SLO using the Synthetics availability SLI, you can use the SLO burn rate rule. For more information about configuring the rule, see [Create an SLO burn rate rule](/solutions/observability/incident-management/create-an-slo-burn-rate-rule.md).