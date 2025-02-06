# Create and manage rules [observability-create-manage-rules]

::::{admonition} Required role
:class: note

The **Editor** role or higher is required to create and manage rules for alerting. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


Alerting enables you to define *rules*, which detect complex conditions within different apps and trigger actions when those conditions are met. Alerting provides a set of built-in connectors and rules for you to use.


## Observability rules [observability-create-manage-rules-observability-rules]

Learn more about Observability rules and how to create them:

| Rule type | Name | Detects when…​ |
| --- | --- | --- |
| AIOps | [Anomaly detection](../../../solutions/observability/incident-management/create-an-apm-anomaly-rule.md) | Anomalies match specific conditions. |
| APM | [APM anomaly](../../../solutions/observability/incident-management/create-an-apm-anomaly-rule.md) | The latency, throughput, or failed transaction rate of a service is abnormal. |
| Observability | [Custom threshold](../../../solutions/observability/incident-management/create-an-apm-anomaly-rule.md) | An Observability data type reaches or exceeds a given value. |
| Stack | [{{es}} query](../../../solutions/observability/incident-management/create-an-elasticsearch-query-rule.md) | Matches are found during the latest query run. |
| APM | [Error count threshold](../../../solutions/observability/incident-management/create-an-error-count-threshold-rule.md) | The number of errors in a service exceeds a defined threshold. |
| APM | [Failed transaction rate threshold](../../../solutions/observability/incident-management/create-failed-transaction-rate-threshold-rule.md) | The rate of transaction errors in a service exceeds a defined threshold. |
| Metrics | [Inventory](../../../solutions/observability/incident-management/create-an-inventory-rule.md) | The infrastructure inventory exceeds a defined threshold. |
| APM | [Latency threshold](../../../solutions/observability/incident-management/create-latency-threshold-rule.md) | The latency of a specific transaction type in a service exceeds a defined threshold. |
| SLO | [SLO burn rate rule](../../../solutions/observability/incident-management/create-an-slo-burn-rate-rule.md) | The burn rate is above a defined threshold. |


## Creating rules and alerts [observability-create-manage-rules-creating-rules-and-alerts]

You start by defining the rule and how often it should be evaluated. You can extend these rules by adding an appropriate action (for example, send an email or create an issue) to be triggered when the rule conditions are met. These actions are defined within each rule and implemented by the appropriate connector for that action e.g. Slack, Jira. You can create any rules from scratch using the **Manage Rules** page, or you can create specific rule types from their respective UIs and benefit from some of the details being pre-filled (for example, Name and Tags).

* For APM alert types, you can select **Alerts and rules** and create rules directly from the **Services***, ***Traces**, and **Dependencies** UIs.
* For SLO alert types, from the **SLOs** page open the **More actions*** menu ![action menu](../../../images/serverless-boxesHorizontal.svg "") for an SLO and select ***Create new alert rule**. Alternatively, when you create a new SLO, the **Create new SLO burn rate alert rule** checkbox is enabled by default and will prompt you to [Create SLO burn rate rule](../../../solutions/observability/incident-management/create-an-slo-burn-rate-rule.md) upon saving the SLO.

After a rule is created, you can open the **More actions** menu ![More actions](../../../images/serverless-boxesHorizontal.svg "") and select **Edit rule** to check or change the definition, and/or add or modify actions.

:::{image} ../../../images/serverless-alerts-edit-rule.png
:alt: Edit rule (failed transaction rate)
:class: screenshot
:::

From the action menu you can also:

* Disable or delete rule
* Clone rule
* Snooze rule notifications
* Run rule (without waiting for next scheduled check)
* Update API keys


## View rule details [observability-create-manage-rules-view-rule-details]

Click on an individual rule on the **{{rules-app}}** page to view details including the rule name, status, definition, execution history, related alerts, and more.

:::{image} ../../../images/serverless-alerts-detail-apm-anomaly.png
:alt: Rule details (APM anomaly)
:class: screenshot
:::

A rule can have one of the following responses:

`failed`
:   The rule ran with errors.

`succeeded`
:   The rule ran without errors.

`warning`
:   The rule ran with some non-critical errors.


## Snooze and disable rules [observability-create-manage-rules-snooze-and-disable-rules]

The rule listing enables you to quickly snooze, disable, enable, or delete individual rules.

When you snooze a rule, the rule checks continue to run on a schedule but the alert will not trigger any actions. You can snooze for a specified period of time, indefinitely, or schedule single or recurring downtimes.

When a rule is in a snoozed state, you can cancel or change the duration of this state.

To temporarily suppress notifications for *all* rules, create a [maintenance window](../../../explore-analyze/alerts-cases/alerts/maintenance-windows.md).


## Import and export rules [observability-create-manage-rules-import-and-export-rules]

To import and export rules, use [{{saved-objects-app}}](../../../explore-analyze/find-and-organize.md).

Rules are disabled on export. You are prompted to re-enable the rule on successful import.
