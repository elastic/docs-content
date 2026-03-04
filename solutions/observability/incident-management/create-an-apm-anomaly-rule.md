---
navigation_title: APM anomaly
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-anomaly-rule.html
  - https://www.elastic.co/guide/en/serverless/current/observability-create-anomaly-alert-rule.html
products:
  - id: observability
  - id: cloud-serverless
---

# Create an APM anomaly rule [observability-create-anomaly-alert-rule]

::::{important}
To use the APM Anomaly rule, you have to enable [machine learning](/solutions/observability/apm/machine-learning.md#observability-apm-integrate-with-machine-learning-enable-anomaly-detection), which requires an [appropriate license](https://www.elastic.co/subscriptions).

::::

::::{note}

For Observability serverless projects, the **Editor** role or higher is required to create anomaly rules. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


You can create an anomaly rule to alert you when either the latency, throughput, or failed transaction rate of a service is abnormal. Anomaly rules can be set at different levels: environment, service, and/or transaction type. Add actions to raise alerts via services or third-party integrations (for example, send an email or create a Jira issue).

:::{image} /solutions/images/serverless-alerts-create-apm-anomaly.png
:alt: Create rule for APM anomaly alert
:screenshot:
:::

::::{tip}
These steps show how to use the **Alerts** UI. You can also create an anomaly rule directly from any page within **Applications**. Click the **Alerts and rules** button, and select **Create anomaly rule**. When you create a rule this way, the **Name** and **Tags** fields will be prepopulated but you can still change these.

::::


To create your anomaly rule:

1. In Observability UI, go to **Alerts**.
2. Select **Manage Rules** from the **Alerts** page, and select **Create rule**.
3. Enter a **Name** for your rule, and any optional **Tags** for more granular reporting (leave blank if unsure).
4. Select the **APM Anomaly** rule type.
5. Select the appropriate **Service**, **Type**, and **Environment** (or leave **ALL** to include all options).
6. Select the desired severity (critical, major, minor, warning) from **Has anomaly with severity**.
7. Define the interval to check the rule (for example, check every 1 minute).
8. (Optional) Set up **Actions**.
9. **Save** your rule.


## Add actions [observability-create-anomaly-alert-rule-add-actions]

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

The following variables are specific to this rule type. You can also specify [variables common to all rules](/explore-analyze/alerting/alerts/rule-action-variables.md).

`context.alertDetailsUrl`
:   Link to the alert troubleshooting view for further context and details. This will be an empty string if the `server.publicBaseUrl` is not configured.

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

:::::