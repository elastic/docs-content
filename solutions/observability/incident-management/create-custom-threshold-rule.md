---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/custom-threshold-alert.html
  - https://www.elastic.co/guide/en/serverless/current/observability-create-custom-threshold-alert-rule.html

navigation_title: "Custom threshold"
---

# Create a custom threshold rule [observability-create-custom-threshold-alert-rule]


::::{note}

**For Observability serverless projects**, the **Editor** role or higher is required to create a custom threshold rule. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


Create a custom threshold rule to trigger an alert when an {{obs-serverless}} data type reaches or exceeds a given value.

1. To access this page, select **Alerts** from the main navigation.
2. Click **Manage Rules** → **Create rule**.
3. Under **Select rule type**, select **Custom threshold**.

:::{image} /solutions/images/serverless-custom-threshold-rule.png
:alt: Rule details (custom threshold)
:screenshot:
:::


## Define rule data [custom-threshold-scope]

Specify the following settings to define the data the rule applies to:

* **Select a data view:** Click the data view field to search for and select a data view that points to the indices or data streams that you’re creating a rule for. You can also create a *new* data view by clicking **Create a data view**. Refer to [Create a data view](/explore-analyze/find-and-organize/data-views.md) for more on creating data views.
* **Define query filter (optional):** Use a query filter to narrow down the data that the rule applies to. For example, set a query filter to a specific host name using the query filter `host.name:host-1` to only apply the rule to that host.


## Set rule conditions [custom-threshold-rule-conditions]

Set the conditions for the rule to detect using aggregations, an equation, and a threshold.


### Set aggregations [custom-threshold-aggregation]

Aggregations summarize your data to make it easier to analyze. Set any of the following aggregation types to gather data to create your rule: `Average`, `Max`, `Min`, `Cardinality`, `Count`, `Sum,` `Percentile`, or `Rate`. For more information about these options, refer to [Aggregation options](/solutions/observability/incident-management/aggregation-options.md).

For example, to gather the total number of log documents with a log level of `warn`:

1. Set the **Aggregation** to **Count**, and set the **KQL Filter** to `log.level: "warn"`.
2. Set the threshold to `IS ABOVE 100` to trigger an alert when the number of log documents with a log level of `warn` reaches 100.


### Set the equation and threshold [custom-threshold-equation]

Set an equation using your aggregations. Based on the results of your equation, set a threshold to define when to trigger an alert. The equations use basic math or boolean logic. Refer to the following examples for possible use cases.


### Basic math equation [custom-threshold-math-equation]

Add, subtract, multiply, or divide your aggregations to define conditions for alerting.

**Example:** Set an equation and threshold to trigger an alert when a metric is above a threshold. For this example, we’ll use average CPU usage—the percentage of CPU time spent in states other than `idle` or `IOWait` normalized by the number of CPU cores—and trigger an alert when CPU usage is above a specific percentage. To do this, set the following aggregations, equation, and threshold:

1. Set the following aggregations:

    * **Aggregation A:** Average `system.cpu.user.pct`
    * **Aggregation B:** Average `system.cpu.system.pct`
    * **Aggregation C:** Max `system.cpu.cores`.

2. Set the equation to `(A + B) / C * 100`
3. Set the threshold to `IS ABOVE 95` to alert when CPU usage is above 95%.


### Boolean logic [custom-threshold-boolean-equation]

Use conditional operators and comparison operators with you aggregations to define conditions for alerting.

**Example:** Set an equation and threshold to trigger an alert when the number of stateful pods differs from the number of desired pods. For this example, we’ll use `kubernetes.statefulset.ready` and `kubernetes.statefulset.desired`, and trigger an alert when their values differ. To do this, set the following aggregations, equation, and threshold:

1. Set the following aggregations:

    * **Aggregation A:** Sum `kubernetes.statefulset.ready`
    * **Aggregation B:** Sum `kubernetes.statefulset.desired`

2. Set the equation to `A == B ? 1 : 0`. If A and B are equal, the result is `1`. If they’re not equal, the result is `0`.
3. Set the threshold to `IS BELOW 1` to trigger an alert when the result is `0` and the field values do not match.


## Preview chart [custom-threshold-chart-preview]

The preview chart provides a visualization of how many entries match your configuration. The shaded area shows the threshold you’ve set.

If you use the **Group alerts by** option, the maximum bar size will be 3. It will only show the top 3 fields.


## Group alerts by (optional) [custom-threshold-group-by]

Set one or more **group alerts by** fields for custom threshold rules to perform a composite aggregation against the selected fields. When any of these groups match the selected rule conditions, an alert is triggered *per group*.

When you select multiple groupings, the group name is separated by commas.

For example, if you group alerts by the `host.name` and `host.architecture` fields, and there are two hosts (`Host A` and `Host B`) and two architectures (`Architecture A` and `Architecture B`), the composite aggregation forms multiple groups.

If the `Host A, Architecture A` group matches the rule conditions, but the `Host B, Architecture B` group doesn’t, one alert is triggered for `Host A, Architecture A`.

If you select one field—for example, `host.name`—and `Host A` matches the conditions but `Host B` doesn’t, one alert is triggered for `Host A`. If both groups match the conditions, alerts are triggered for both groups.


## Trigger "no data" alerts (optional) [observability-create-custom-threshold-alert-rule-trigger-no-data-alerts-optional]

Optionally configure the rule to trigger an alert when:

* there is no data, or
* a group that was previously detected stops reporting data.

To do this, select **Alert me if there’s no data**.

The behavior of the alert depends on whether any **group alerts by** fields are specified:

* **No "group alerts by" fields**: (Default) A "no data" alert is triggered if the condition fails to report data over the expected time period, or the rule fails to query {{es}}. This alert means that something is wrong and there is not enough data to evaluate the related threshold.
* **Has "group alerts by" fields**: If a previously detected group stops reporting data, a "no data" alert is triggered for the missing group.

    For example, consider a scenario where `host.name` is the **group alerts by** field for CPU usage above 80%. The first time the rule runs, two hosts report data: `host-1` and `host-2`. The second time the rule runs, `host-1` does not report any data, so a "no data" alert is triggered for `host-1`. When the rule runs again, if `host-1` starts reporting data again, there are a couple possible scenarios:

    * If `host-1` reports data for CPU usage and it is above the threshold of 80%, no new alert is triggered. Instead the existing alert changes from "no data" to a triggered alert that breaches the threshold. Keep in mind that no notifications are sent in this case because there is still an ongoing issue.
    * If `host-1` reports CPU usage below the threshold of 80%, the alert status is changed to recovered.


::::{note}
**How to untrack decommissioned hosts**

If a host (for example, `host-1`) is decommissioned, you probably no longer want to see "no data" alerts about it. To mark an alert as untracked: Go to the Alerts table, click the ![More actions](/solutions/images/serverless-boxesHorizontal.svg "") icon to expand the "More actions" menu, and click *Mark as untracked*.

::::



## Add actions [observability-create-custom-threshold-alert-rule-add-actions]

You can extend your rules with actions that interact with third-party systems, write to logs or indices, or send user notifications. You can add an action to a rule at any time. You can create rules without adding actions, and you can also define multiple actions for a single rule.

To add actions to rules, you must first create a connector for that service (for example, an email or external incident management system), which you can then use for different rules, each with their own action frequency.

:::::{dropdown} Connector types
Connectors provide a central place to store connection information for services and integrations with third party systems. The following connectors are available when defining actions for alerting rules:

* [Cases](https://www.elastic.co/guide/en/kibana/current/cases-action-type.html)
* [D3 Security](https://www.elastic.co/guide/en/kibana/current/d3security-action-type.html)
* [Email](https://www.elastic.co/guide/en/kibana/current/email-action-type.html)
* [{{ibm-r}}](https://www.elastic.co/guide/en/kibana/current/resilient-action-type.html)
* [Index](https://www.elastic.co/guide/en/kibana/current/index-action-type.html)
* [Jira](https://www.elastic.co/guide/en/kibana/current/jira-action-type.html)
* [Microsoft Teams](https://www.elastic.co/guide/en/kibana/current/teams-action-type.html)
* [Observability AI Assistant](https://www.elastic.co/guide/en/kibana/current/obs-ai-assistant-action-type.html)
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


For more information on creating connectors, refer to [Connectors](/deploy-manage/manage-connectors.md).

:::::


:::::{dropdown} Action frequency
After you select a connector, you must set the action frequency. You can choose to create a summary of alerts on each check interval or on a custom interval. Alternatively, you can set the action frequency such that you choose how often the action runs (for example, at each check interval, only when the alert status changes, or at a custom action interval). In this case, you must also select the specific threshold condition that affects when actions run: `Alert`, `No Data`, or `Recovered`.

:::{image} /solutions/images/serverless-custom-threshold-run-when.png
:alt: Configure when a rule is triggered
:screenshot:
:::

You can also further refine the conditions under which actions run by specifying that actions only run when they match a KQL query or when an alert occurs within a specific time frame:

* **If alert matches query**: Enter a KQL query that defines field-value pairs or query conditions that must be met for notifications to send. The query only searches alert documents in the indices specified for the rule.
* **If alert is generated during timeframe**: Set timeframe details. Notifications are only sent if alerts are generated within the timeframe you define.

:::{image} /solutions/images/serverless-logs-threshold-conditional-alert.png
:alt: Configure a conditional alert
:screenshot:
:::

:::::


:::::{dropdown} Action variables
Use the default notification message or customize it. You can add more context to the message by clicking the Add variable icon ![Add variable](/solutions/images/serverless-indexOpen.svg "") and selecting from a list of available variables.

:::{image} /solutions/images/serverless-action-variables-popup.png
:alt: Action variables list
:screenshot:
:::

The following variables are specific to this rule type. You can also specify [variables common to all rules](/explore-analyze/alerts-cases/alerts/rule-action-variables.md).

`context.alertDetailsUrl`
:   Link to the alert troubleshooting view for further context and details. This will be an empty string if the `server.publicBaseUrl` is not configured.

`context.cloud`
:   The cloud object defined by ECS if available in the source.

`context.container`
:   The container object defined by ECS if available in the source.

`context.group`
:   The object containing groups that are reporting data.

`context.host`
:   The host object defined by ECS if available in the source.

`context.labels`
:   List of labels associated with the entity where this alert triggered.

`context.orchestrator`
:   The orchestrator object defined by ECS if available in the source.

`context.reason`
:   A concise description of the reason for the alert.

`context.tags`
:   List of tags associated with the entity where this alert triggered.

`context.timestamp`
:   A timestamp of when the alert was detected.

`context.value`
:   List of the condition values.

`context.viewInAppUrl`
:   Link to the alert source.

:::::