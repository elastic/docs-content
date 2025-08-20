---
navigation_title: SLO burn rate
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/slo-burn-rate-alert.html
  - https://www.elastic.co/guide/en/serverless/current/observability-create-slo-burn-rate-alert-rule.html
products:
  - id: observability
  - id: cloud-serverless
---

# Create an SLO burn rate rule [observability-create-slo-burn-rate-alert-rule]

% Stateful only for the important admonition below?

::::{important}

**For Observability serverless projects**, The **Editor** role or higher is required to create SLOs. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

**For Elastic Stack**, to create and manage SLOs, you need an [appropriate license](https://www.elastic.co/subscriptions), an {{es}} cluster with both `transform` and `ingest` [node roles](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#node-roles) present, and [SLO access](/solutions/observability/incident-management/configure-service-level-objective-slo-access.md) must be configured.

::::


Create an SLO burn rate rule to get alerts when the burn rate is too high over a defined threshold for two different lookback periods: a long period and a short period that is 1/12th of the long period. For example, if your long lookback period is one hour, your short lookback period is five minutes.

Choose which SLO to monitor and then define multiple burn rate windows with appropriate severity. For each period, the burn rate is computed as the error rate divided by the error budget. When the burn rates for both periods surpass the threshold, an alert is triggered. Add actions to raise alerts via services or third-party integrations e.g. mail, Slack, Jira.

:::{image} /solutions/images/serverless-slo-alerts-create-rule.png
:alt: Create rule for failed transaction rate threshold
:screenshot:
:::

::::{tip}
These steps show how to use the **Alerts** UI. You can also create an SLO burn rate rule directly from **Observability** → **SLOs**. Click the more options icon (![More options](/solutions/images/serverless-boxesVertical.svg "")) to the right of the SLO you want to add a burn rate rule for, and select **![Bell](/solutions/images/serverless-bell.svg "") Create new alert rule** from the menu.

When you use the UI to create an SLO, a default SLO burn rate alert rule is created automatically. The burn rate rule will use the default configuration and no connector. You must configure a connector if you want to receive alerts for SLO breaches.

::::


To create an SLO burn rate rule:

1. In Observability UI, go to **Alerts**.
2. Select **Manage Rules** from the **Alerts** page, and select **Create rule**.
3. Enter a **Name** for your rule, and any optional **Tags** for more granular reporting (leave blank if unsure).
4. Select **SLO burn rate** from the **Select rule type** list.
5. Select the **SLO** you want to monitor.
6. Define multiple burn rate windows for each **Action Group** (defaults to 4 windows but you can edit):

    * **Lookback (hours)**: Enter the lookback period for this window. A shorter period equal to 1/12th of this period will be used for faster recovery.
    * **Burn rate threshold**: Enter a burn rate for this window.
    * **Action Group**: Select a severity for this window.

7. Define the interval to check the rule e.g. check every 1 minute.
8. (Optional) Set up **Actions**.
9. **Save** your rule.


## Add actions [observability-create-slo-burn-rate-alert-rule-add-actions]

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

With the **Run when** menu you can choose if an action runs for a specific severity (critical, high, medium, low), or when the alert is recovered. For example, you can add a corresponding action for each severity you want an alert for, and also for when the alert recovers.

:::{image} /solutions/images/serverless-slo-action-frequency.png
:alt: Choose between severity or recovered
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

`context.burnRateThreshold`
:   The burn rate threshold value.

`context.grouping` {applies_to}`stack: ga 9.1`
:   The object containing groups that are reporting data.

`context.longWindow`
:   The window duration with the associated burn rate value.

`context.reason`
:   A concise description of the reason for the alert.

`context.shortWindow`
:   The window duration with the associated burn rate value.

`context.sloId`
:   The SLO unique identifier.

`context.sloInstanceId`
:   The SLO instance ID.

`context.sloName`
:   The SLO name.

`context.timestamp`
:   A timestamp of when the alert was detected.

`context.viewInAppUrl`
:   The url to the SLO details page to help with further investigation.

:::::



## Next steps [observability-create-slo-burn-rate-alert-rule-next-steps]

Learn how to view alerts and triage SLO burn rate breaches:

* [View alerts](/solutions/observability/incident-management/view-alerts.md)
* [SLO burn rate breaches](/solutions/observability/incident-management/triage-slo-burn-rate-breaches.md)