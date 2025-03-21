---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/view-alerts.html
---

# View alerts [view-alerts]

When the conditions of a rule are met, it creates an alert. If the rule has actions, they run at the defined frequency. For example, the rule can send email notifications for each alert at a custom interval. For an introduction to the concepts of rules, alerts, and actions, refer to [Alerting](../alerts.md).

You can manage the alerts for each rule in **{{stack-manage-app}}** > **{{rules-ui}}**. Alternatively, manage all your alerts in **{{stack-manage-app}}** > **Alerts**. [preview]

:::{image} /explore-analyze/images/kibana-stack-management-alerts-page.png
:alt: Alerts page with multiple alerts
:screenshot:
:::

::::{note}
You must have the appropriate {{kib}} {{alert-features}} and index privileges to view alerts. Refer to [Alerting security requirements](alerting-setup.md#alerting-security).

::::

## Filter alerts [filter-alerts]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::

In **{{stack-manage-app}}** > **Alerts**, you can filter the list (for example, by alert status or rule type) and customize the filter controls. To search for specific alerts, use the KQL bar to create structured queries using [{{kib}} Query Language](../../query-filter/languages/kql.md).

By default, the list contains all the alerts that you have authority to view in the selected time period except those associated with Security rules. To view alerts for Security rules, click the query menu and select **Security rule types**:

:::{image} /explore-analyze/images/kibana-stack-management-alerts-query-menu.png
:alt: The Alerts page with the query menu open
:screenshot:
:::

Alternatively, view those alerts in the [{{security-app}}](../../../solutions/security/detect-and-alert/manage-detection-alerts.md).

## View alert details [view-alert-details]

To get more information about a specific alert, open its action menu (…) and select **View alert details** in either **{{stack-manage-app}} > Alerts** or **{{rules-ui}}**. There you’ll see the current status of the alert, its duration, and when it was last updated. To help you determine what caused the alert, there is information such as the expected and actual threshold values and a summarized reason for the alert.

If an alert is affected by a maintenance window, the alert details include its identifier. For more information about their impact on alert notifications, refer to [*Maintenance windows*](maintenance-windows.md).

### Alert statuses [alert-status]

There are three common alert statuses:

`active`
:   The conditions for the rule are met and actions should be generated according to the notification settings.

`recovered`
:   The conditions for the rule are no longer met and recovery actions should be generated.

`untracked`
:   Actions are no longer generated. For example, you can choose to move active alerts to this state when you disable or delete rules.

::::{note}
An alert can also be in a "flapping" state when it is switching repeatedly between active and recovered states. This state is possible only if you have enabled alert flapping detection in **{{stack-manage-app}} > {{rules-ui}} > Settings**. For each space, you can choose a look back window and threshold that are used to determine whether alerts are flapping. For example, you can specify that the alert must change status at least 6 times in the last 10 runs. If the rule has actions that run when the alert status changes, those actions are suppressed while the alert is flapping.

::::

## Mute alerts [mute-alerts]

If an alert is active or flapping, you can mute it to temporarily suppress future actions. In both **{{stack-manage-app}} > Alerts** and **{{rules-ui}}**, you can open the action menu (…) for the appropriate alert and select **Mute**. To permanently suppress actions for an alert, open the actions menu and select **Mark as untracked**.

To affect the behavior of the rule rather than individual alerts, check out [Snooze and disable rules](create-manage-rules.md#controlling-rules).
