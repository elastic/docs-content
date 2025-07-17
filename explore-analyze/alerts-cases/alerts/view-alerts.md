---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/view-alerts.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# View and manage alerts [view-alerts]

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

## Clean up alerts [clean-up-alerts]

```{applies_to}
stack: preview 9.1 
serverless: preview
```

Manage the size of alert indices in your space by clearing out alerts that are older or infrequently accessed. You can do this by running an alert cleanup task, which deletes alerts according to the criteria that you define.

:::{note}
The alert cleanup task permanently deletes alerts in your `.alert-*` indices. Make sure to take regular snapshots of your cluster to back up your alert data in case you ever need to restore it.
:::

### Prerequisites [clean-up-alerts-reqs]

* To run the alert cleanup task, your role must have `All` privileges for the **Alert deletion feature**. When setting your role’s Kibana privileges, go to **Management > Rule Settings**, enable **Customize sub-feature privileges**, then select `All` for the **Alert deletion** feature.
* Alerts in your space must be older than a day. The minimum threshold for the alert cleanup task is one day.  

### Run the alert cleanup task [run-alert-clean-up-task]

Remove old or rarely-accessed alerts in your space by running an alert cleanup task, which deletes alerts according to the criteria that you define. Alerts that are attached to cases are not deleted. 

1. Open the **Rules** page by going to **Stack Management > Alerts and Insights > Rules** in the main menu or using the global search field.
2. Click **Settings** to open the settings for all rules in the space.
3. In the **Clean up alert history** section, click **Clean up**.
4. Define criteria for the alert cleanup task. You can choose to delete alerts that are active or inactive and meet a certain age.

   :::{tip}
   At the bottom of the modal, you can find a preview of the number of alerts that will be deleted according to the criteria that you define.
   :::

   * **Active alerts**: Choose to delete alerts that haven't had their status changed since they were initially generated and are older than the threshold that you specify. 
   
      For example, if you specify two years as the threshold, the cleanup task will delete alerts that were generated more than two years ago and have never had their status changed.  

   * **Inactive alerts**: Choose to delete alerts that have had their statuses changed since they were initially created and are older than the threshold that you specify. Inactive alerts have had their status changed to recovered, closed, acknowledged, or untracked. 

      For example, if you specify two years, the cleanup task will delete alerts that have had their status changed to recovered, closed, acknowledged, or untracked more than two years ago.

5. Enter **Delete** to verify that you want to run the alert cleanup task, then click **Run cleanup task**.  

A message confirming that the alert cleanup task has started running appears. This information is also provided at the top of the alert cleanup modal in the **Last cleanup task: details** field. Note the field doesn't display in the modal until an alert cleanup task is run.