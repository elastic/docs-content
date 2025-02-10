---
navigation_title: "Monitor status"
---

# Create a monitor status rule [monitor-status-alert]


There are two types of monitor status rules:

* [Synthetics monitor status](../../../solutions/observability/incident-management/create-monitor-status-rule.md#monitor-status-alert-synthetics) for use with [Elastic Synthetics](../../../solutions/observability/apps/synthetic-monitoring.md).
* [8.15.0] [Uptime monitor status](../../../solutions/observability/incident-management/create-monitor-status-rule.md#monitor-status-alert-uptime) for use with the Uptime app.

    ::::{warning}
    **The Uptime app and the Uptime monitor status rule are deprecated as of version 8.15.0.**

    If you are using the Uptime monitor status rule with the Uptime app, you should migrate the Uptime monitor and the Uptime monitor status rule to Elastic Synthetics and the Synthetics monitor rule.

    If you are using the Uptime monitor status rule with a monitor created with Elastic Synthetics, you should migrate the Uptime monitor status rule to the Synthetics monitor rule. Learn how in [Migrate from the Uptime rule to the Synthetics rule](../../../solutions/observability/incident-management/create-monitor-status-rule.md#migrate-monitor-rule).

    ::::



## Synthetics monitor status [monitor-status-alert-synthetics]

Within the Synthetics UI, create a **Monitor Status** rule to receive notifications based on errors and outages.


### Filters [synthetic-monitor-filters]

The **Filter by** section controls the scope of the rule. The rule will only check monitors that match the filters defined in this section. In this example, the rule will only alert on `browser` monitors located in `Asia/Pacific - Japan`.

:::{image} ../../../images/observability-synthetic-monitor-filters.png
:alt: Filter by section of the Synthetics monitor status rule
:class: screenshot
:::


### Conditions [synthetic-monitor-conditions]

Conditions for each rule will be applied to all monitors that match the filters in the [**Filter by** section](../../../solutions/observability/incident-management/create-monitor-status-rule.md#synthetic-monitor-filters). You can choose the number of times the monitor has to be down relative to either a number of checks run or a time range in which checks were run, and the minimum number of locations the monitor must be down in.

::::{note}
Retests are included in the number of checks.

::::


The **Rule schedule** defines how often to evaluate the condition. Note that checks are queued, and they run as close to the defined value as capacity allows. For example, if a check is scheduled to run every 2 minutes, but the check takes longer than 2 minutes to run, a check will not run until the previous check has finished.

You can also set **Advanced options** such as the number of consecutive runs that must meet the rule conditions before an alert occurs.

In this example, the conditions will be met any time a `browser` monitor is down `3` of the last `5` times the monitor ran across any locations that match the filter. These conditions will be evaluated every minute, and you will only receive an alert when the conditions are met three times consecutively.

:::{image} ../../../images/observability-synthetic-monitor-conditions.png
:alt: Filters and conditions defining a Synthetics monitor status rule
:class: screenshot
:::


### Action types [synthetic-monitor-action-types]

Extend your rules by connecting them to actions that use the following supported built-in integrations.

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


After you select a connector, you must set the action frequency. You can choose to create a summary of alerts on each check interval or on a custom interval. For example, send email notifications that summarize the new, ongoing, and recovered alerts each hour:

:::{image} ../../../images/observability-synthetic-monitor-action-types-summary.png
:alt: synthetic monitor action types summary
:class: screenshot
:::

Alternatively, you can set the action frequency such that you choose how often the action runs (for example, at each check interval, only when the alert status changes, or at a custom action interval). In this case, you must also select the specific threshold condition that affects when actions run: the *Synthetics monitor status* changes or when it is *Recovered* (went from down to up).

:::{image} ../../../images/observability-synthetic-monitor-action-types-each-alert.png
:alt: synthetic monitor action types each alert
:class: screenshot
:::

You can also further refine the conditions under which actions run by specifying that actions only run when they match a KQL query or when an alert occurs within a specific time frame:

* **If alert matches query**: Enter a KQL query that defines field-value pairs or query conditions that must be met for notifications to send. The query only searches alert documents in the indices specified for the rule.
* **If alert is generated during timeframe**: Set timeframe details. Notifications are only sent if alerts are generated within the timeframe you define.

:::{image} ../../../images/observability-synthetic-monitor-action-types-more-options.png
:alt: synthetic monitor action types more options
:class: screenshot
:::


#### Action variables [synthetic-monitor-action-variables]

Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

:::{image} ../../../images/observability-synthetic-monitor-action-variables.png
:alt: synthetic monitor action variables
:class: screenshot
:::

The following variables are specific to this rule type. You an also specify [variables common to all rules](../../../explore-analyze/alerts-cases/alerts/rule-action-variables.md).

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

::::{warning}
**The Uptime app and the Uptime monitor status rule are deprecated as of version 8.15.0.**

If you are using the Uptime monitor status rule with the Uptime app, you should migrate the Uptime monitor and the Uptime monitor status rule to Elastic Synthetics and the Synthetics monitor rule.

If you are using the Uptime monitor status rule with a monitor created with Elastic Synthetics, you should migrate the Uptime monitor status rule to the Synthetics monitor rule. Learn how in [Migrate from the Uptime rule to the Synthetics rule](../../../solutions/observability/incident-management/create-monitor-status-rule.md#migrate-monitor-rule).

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

:::{image} ../../../images/observability-monitor-status-alert.png
:alt: Monitor status rule
:class: screenshot
:::

The final step when creating a rule is to select one or more actions to take when the alert is triggered.


### Action types [action-types-status]

You can extend your rules by connecting them to actions that use the following supported built-in integrations. Actions are {{kib}} services or integrations with third-party systems that run as background tasks on the {{kib}} server when rule conditions are met.

You can configure action types on the [Settings](../../../solutions/observability/apps/configure-settings.md#configure-uptime-alert-connectors) page.

:::{image} ../../../images/observability-uptime-alert-connectors.png
:alt: Uptime rule connectors
:class: screenshot
:::

After you select a connector, you must set the action frequency. You can choose to create a summary of alerts on each check interval or on a custom interval. For example, send email notifications that summarize the new, ongoing, and recovered alerts each hour:

:::{image} ../../../images/observability-action-alert-summary.png
:alt: Action frequency summary of alerts
:class: screenshot
:::

Alternatively, you can set the action frequency such that you choose how often the action runs (for example, at each check interval, only when the alert status changes, or at a custom action interval). In this case, you must also select the specific threshold condition that affects when actions run: `Uptime Down Monitor` or `Recovered`.

:::{image} ../../../images/observability-uptime-run-when-selection.png
:alt: Action frequency for each alert
:class: screenshot
:::


### Action variables [action-variables-status]

Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

:::{image} ../../../images/observability-monitor-status-alert-default-message.png
:alt: Default notification message for monitor status rules with open "Add variable" popup listing available action variables
:class: screenshot
:::


### Alert recovery [recovery-variables-status]

To receive a notification when the alert recovers, select **Run when Recovered**. Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

:::{image} ../../../images/observability-monitor-status-alert-recovery.png
:alt: Default recovery message for monitor status rules with open "Add variable" popup listing available action variables
:class: screenshot
:::


## Migrate from the Uptime rule to the Synthetics rule [migrate-monitor-rule]

If you are currently using the Uptime monitor status with a monitor created with Elastic Synthetics, you should migrate the Uptime monitor status rule to:

* If you were using the Uptime rule for **synthetic monitor *status* checks**, you can recreate similar functionality using the [Synthetics monitor rule](../../../solutions/observability/incident-management/create-monitor-status-rule.md#migrate-monitor-rule-synthetics-rule).
* If you were using the Uptime rule for **synthetic monitor *availability* checks**, there is no equivalent in the Synthetics monitor rule. Instead, you can use the [Synthetics availability SLI](../../../solutions/observability/incident-management/create-monitor-status-rule.md#migrate-monitor-rule-synthetics-sli) to create similar functionality.


### Uptime status check to Synthetics monitor rule [migrate-monitor-rule-synthetics-rule]


#### Filters [_filters]

The KQL syntax that you used in the Uptime monitor status rule is also valid in the **Filter by** section of the Synthetics monitor status rule. The Synthetics monitor status rule also offers dropdowns for several categories for easy filtering. However, you can still use KQL syntax for these categories if you prefer.


#### Conditions [_conditions]

::::{note}
If you are using the *Uptime availability condition* refer to [Uptime availability check to Synthetics availability SLI](../../../solutions/observability/incident-management/create-monitor-status-rule.md#migrate-monitor-rule-synthetics-sli).

::::


If you’re using the Uptime status check condition, you can recreate similar effects using the following Synthetics monitor status rule condition equivalents:

|  | Uptime | Synthetics equivalent |
| --- | --- | --- |
| **Number of times the monitor is down** | `ANY MONITOR IS DOWN  >=` `{{number}}` times (for example, `ANY MONITOR IS DOWN  >=` `5` times) | `IS DOWN` `{{number}}` times (for example, `IS DOWN` `5` times) |
| **Timeframe** | `WITHIN last` `{{number}}` `{time range unit}` (for example, `WITHIN last` `15` `minutes`) | `WITHIN THE LAST` `{{number}}` `{time range unit}` (for example, `WITHIN THE LAST` `15` `minutes`) |


#### Actions [_actions_5]

The default messages for the Uptime monitor status rule and Synthetics monitor status rule are different, but you can recreate similar messages using [Synthetics monitor status rule action variables](../../../solutions/observability/incident-management/create-monitor-status-rule.md#synthetic-monitor-action-variables).


### Uptime availability check to Synthetics availability SLI [migrate-monitor-rule-synthetics-sli]

SLOs allow you to set clear, measurable targets for your service performance, based on factors like availability. The [Synthetics availability SLI](../../../solutions/observability/incident-management/create-an-slo.md#synthetics-availability-sli) is a service-level indicator (SLI) based on the availability of your synthetic monitors.


#### Filters [_filters_2]

The KQL syntax that you used in the Uptime monitor status rule is also valid in the **Query filter** field of the Synthetics availability SLI.


#### Conditions [_conditions_2]

Use the following Synthetics availability SLI fields to replace the Uptime monitor status rule’s availability conditions:

|  | Uptime | Synthetics equivalent |
| --- | --- | --- |
| **Number of checks that are down relative to all checks run** | `ANY MONITOR IS UP IN <` `{{percent}}` of checks (for example, `ANY MONITOR IS UP IN <` `90%` of checks) | **Target / SLO (%)** field (for example, `90%`) |
| **Timeframe** | `WITHIN THE LAST` `{{number}}` `{time range unit}` (for example, `WITHIN THE LAST` `30` `days`) | **Time window** and **Duration** fields (for example, Time window: `Rolling`, Duration: `30 days`) |


#### Actions [_actions_6]

After creating a new SLO using the Synthetics availability SLI, you can use the SLO burn rate rule. For more information about configuring the rule, see [Create an SLO burn rate rule](../../../solutions/observability/incident-management/create-an-slo-burn-rate-rule.md).
