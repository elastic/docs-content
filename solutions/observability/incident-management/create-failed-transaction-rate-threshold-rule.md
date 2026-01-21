---
navigation_title: Failed transaction rate threshold
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-failed-transaction-rate-threshold-rule.html
  - https://www.elastic.co/guide/en/serverless/current/observability-create-failed-transaction-rate-threshold-alert-rule.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Create a failed transaction rate threshold rule [observability-create-failed-transaction-rate-threshold-alert-rule]


::::{note}

**For Observability serverless projects**, the **Editor** role or higher is required to create failed transaction rate threshold rules. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


You can create a failed transaction rate threshold rule to alert you when the rate of transaction errors in a service exceeds a defined threshold. Threshold rules can be set at different levels: environment, service, transaction type, and/or transaction name. Add actions to raise alerts via services or third-party integrations e.g. mail, Slack, Jira.

:::{image} /solutions/images/serverless-alerts-create-rule-failed-transaction-rate.png
:alt: Create rule for failed transaction rate threshold alert
:screenshot:
:::

::::{tip}
These steps show how to use the **Alerts** UI. You can also create a failed transaction rate threshold rule directly from any page within **Applications**. Click the **Alerts and rules** button, and select **Create threshold rule** and then **Failed transaction rate**. When you create a rule this way, the **Name** and **Tags** fields will be prepopulated but you can still change these.

::::


To create your failed transaction rate threshold rule:

1. From the Observability UI, go to **Alerts**.
2. Select **Manage Rules** from the **Alerts** page, and select **Create rule**.
3. Enter a **Name** for your rule, and any optional **Tags** for more granular reporting (leave blank if unsure).
4. Select the **Failed transaction rate threshold** rule type from the APM use case.
5. Select the appropriate **Service**, **Type**, **Environment** and **Name** (or leave **ALL** to include all options). Alternatively, you can select **Use KQL Filter** and enter a KQL expression to limit the scope of your rule.
6. Enter a fail rate in the **Is Above** (defaults to 30%).
7. Define the period to be assessed in **For the last** (defaults to last 5 minutes).
8. Choose how to **Group alerts by**. Every unique value will create an alert.
9. Define the interval to check the rule (for example, check every 1 minute).
10. (Optional) Set up **Actions**.
11. **Save** your rule.


## Add actions [observability-create-failed-transaction-rate-threshold-alert-rule-add-actions]

You can extend your rules with actions that interact with third-party systems, write to logs or indices, or send user notifications. You can add an action to a rule at any time. You can create rules without adding actions, and you can also define multiple actions for a single rule.

To add actions to rules, you must first create a connector for that service (for example, an email or external incident management system), which you can then use for different rules, each with their own action frequency.

:::::{dropdown} Connector types
Connectors provide a central place to store connection information for services and integrations with third party systems. The following connectors are available when defining actions for alerting rules:

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


For more information on creating connectors, refer to [Connectors](/deploy-manage/manage-connectors.md).

:::::


:::::{dropdown} Action frequency
After you select a connector, you must set the action frequency. You can choose to create a **Summary of alerts** on each check interval or on a custom interval. For example, you can send email notifications that summarize the new, ongoing, and recovered alerts every twelve hours.

Alternatively, you can set the action frequency to **For each alert** and specify the conditions each alert must meet for the action to run. For example, you can send an email only when the alert status changes to critical.

:::{image} /solutions/images/serverless-alert-action-frequency.png
:alt: Configure when a rule is triggered
:screenshot:
:::

With the **Run when** menu you can choose if an action runs when the threshold for an alert is reached, or when the alert is recovered. For example, you can add a corresponding action for each state to ensure you are alerted when the rule is triggered and also when it recovers.

:::{image} /solutions/images/serverless-alert-apm-action-frequency-recovered.png
:alt: Choose between threshold met or recovered
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

`context.environment`
:   The transaction type the alert is created for.

`context.grouping` {applies_to}`stack: ga 9.1`
:   The object containing groups that are reporting data.

`context.interval`
:   The length and unit of time period where the alert conditions were met.

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

:::::



## Example [create-failed-transaction-rate-threshold-example]

The failed transaction rate threshold alert triggers when the number of transaction errors in a service exceeds a defined threshold.

Before continuing, identify the service name, environment name, and transaction type that you’d like to create a failed transaction rate threshold rule for.

This guide will create an alert for an error group ID based on the following criteria:

* Service: `{your_service.name}`
* Transaction: `{your_transaction.name}`
* Environment: `{your_service.environment}`
* Error rate is above 30% for the last five minutes
* Group alerts by `service.name` and `service.environment`
* Check every 1 minute
* Send the alert via email to the site reliability team

From any page in **Applications**, select **Alerts and rules** → **Create threshold rule** → **Failed transaction rate**. Change the name of the alert (if you wish), but do not edit the tags.

Based on the criteria above, define the following rule details:

* **Service**: `{your_service.name}`
* **Type**: `{your_transaction.name}`
* **Environment**: `{your_service.environment}`
* **Is above:** `30%`
* **For the last:** `5 minutes`
* **Group alerts by:** `service.name` `service.environment`
* **Check every:** `1 minute`

Next, select the **Email** connector and click **Create a connector**. Fill out the required details: sender, host, port, etc., and select **Save**.

A default message is provided as a starting point for your alert. You can use the Mustache template syntax (`{{variable}}`) to pass additional alert values at the time a condition is detected to an action. A list of available variables can be accessed by clicking the Add variable icon ![Add variable](/solutions/images/serverless-indexOpen.svg "").

Select **Save**. The alert has been created and is now active!