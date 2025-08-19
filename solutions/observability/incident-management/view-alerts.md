---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/view-observability-alerts.html
  - https://www.elastic.co/guide/en/serverless/current/observability-view-alerts.html
applies_to:
  stack: all
  serverless:
    observability: all
products:
  - id: observability
  - id: cloud-serverless
---

# View and manage alerts [observability-view-alerts]

::::{note}

**For Observability serverless projects**, the **Editor** role or higher is required to perform this task. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


You can track and manage alerts for your applications and SLOs from the **Alerts** page. You can filter this view by alert status or time period, or search for specific alerts using KQL. Manage your alerts by adding them to cases or viewing them within the respective UIs.

% Stateful only for the following note

::::{note}
You can centrally manage rules from the [{{kib}} Management UI](/explore-analyze/alerts-cases/alerts/create-manage-rules.md) that provides a set of built-in [rule types](/explore-analyze/alerts-cases/alerts/rule-types.md) and [connectors](/deploy-manage/manage-connectors.md) for you to use. Click **Manage Rules**.
::::

:::{image} /solutions/images/serverless-observability-alerts-view.png
:alt: Alerts page
:screenshot:
:::


## Filter alerts [observability-view-alerts-filter-alerts]

To help you get started with your analysis faster, use the KQL bar to create structured queries using [{{kib}} Query Language](/explore-analyze/query-filter/languages/kql.md).

You can use the time filter to define a specific date and time range. By default, this filter is set to search for the last 15 minutes.

You can also filter by alert status using the buttons below the KQL bar. By default, this filter is set to **Show all** alerts, but you can filter to show only active, recovered or untracked alerts.


## View alert details [observability-view-alerts-view-alert-details]

There are a few ways to inspect the details for a specific alert.

From the **Alerts** table, you can click on a specific alert to open the alert detail flyout to view a summary of the alert without leaving the page. There you’ll see the current status of the alert, its duration, and when it was last updated. To help you determine what caused the alert, you can view the expected and actual threshold values, and the rule that produced the alert.

:::{image} /solutions/images/serverless-alert-details-flyout.png
:alt: Alerts detail (APM anomaly)
:screenshot:
:::

To further inspect the rule:

* From the alert detail flyout, click **View rule details**.
* From the **Alerts** table, click the {icon}`boxes_horizontal` icon and select **View rule details**.

To view the alert in the app that triggered it:

* From the alert detail flyout, click **View in app**.
* From the **Alerts** table, click the {icon}`eye` icon.

## Understand alert statuses [observability-view-alerts-understand-statuses]

There are four common alert statuses:

`active`
:   The conditions for the rule are met. If the rule has [actions](../../../explore-analyze/alerts-cases/alerts/create-manage-rules.md#defining-rules-actions-details), {{kib}} generates notifications based on the actions' notification settings. 

`flapping`

:   The alert is switching repeatedly between active and recovered states. If the rule has actions that run when the alert status changes states, those actions are suppressed while the alert is flapping.

::::{note}  

Alert flapping is turned on by default. You can modify the criteria for changing an alert's status to the flapping state by configuring the **Alert flapping detection** settings. To do this, navigate to the **Alerts** page in the main menu, or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Next, click **Manage Rules**, then **Settings** to open the global rule settings for the space. In the **Alert flapping detection** section, modify the rules' look back window and threshold for alert status changes. For example, you can specify that the alert must change its status at least 6 times in the last 10 runs for it to become a flapping alert. 

::::

`recovered`
:   The conditions for the rule are no longer met. If the rule has [recovery actions](../../../explore-analyze/alerts-cases/alerts/create-manage-rules.md#defining-rules-actions-details), {{kib}} generates notifications based on the actions' notification settings. Recovery actions only run if the rule's conditions aren't met during the current rule execution, but were in the previous one. 


    An active alert changes to recovered if the conditions for the rule that generated it are no longer met. 

    A flapping alert changes to recovered if the conditions for the rule that generated it are no longer met, and the alert's status stabilizes before refufilling the criteria for the flapping state. For instance, say that you specify an alert must change its status at least 6 times in the last 10 runs for it to become a flapping alert. If a flapping alert only changes its status 5 times in the last 10 runs, and rule's conditions are not met during the fifth rule run, the alert's status changes from flapping to recovered. 
    
    Once a flapping alert is recovered, it cannot be changed to flapping again. Only new alerts with repeated status changes are candidates for the flapping status. 

`untracked`
:   The rule is disabled, or you’ve marked the alert as untracked. To mark the alert as untracked, go to the **Alerts** table, click the {icon}`boxes_horizontal` icon to expand the **More actions** menu, and click **Mark as untracked**. When an alert is marked as untracked, actions are no longer generated. You can choose to move active alerts to this state when you disable or delete rules.


## Customize the alerts table [observability-view-alerts-customize-the-alerts-table]

Use the toolbar buttons in the upper-left of the alerts table to customize the columns you want displayed:

* **Columns**: Reorder the columns.
* **x fields sorted**: Sort the table by one or more columns.
* **Fields**: Select the fields to display in the table.

For example, click **Fields** and choose the `Maintenance Windows` field. If an alert was affected by a maintenance window, its identifier appears in the new column. For more information about their impact on alert notifications, refer to [{{maint-windows-cap}}](/explore-analyze/alerts-cases/alerts/maintenance-windows.md).

You can also use the toolbar buttons in the upper-right to customize the display options or view the table in full-screen mode.


## Add alerts to cases [observability-view-alerts-add-alerts-to-cases]

From the **Alerts** table, you can add one or more alerts to a case. Click the {icon}`boxes_horizontal` icon to add the alert to a new or existing case. You can add an unlimited amount of alerts from any rule type.

::::{note}
Each case can have a maximum of 1,000 alerts.

::::


### Add an alert to a new case [observability-view-alerts-add-an-alert-to-a-new-case]

To add an alert to a new case:

1. Select **Add to new case**.
2. Enter a case name, add relevant tags, and include a case description.
3. Under **External incident management system**, select a connector. If you’ve previously added one, that connector displays as the default selection. Otherwise, the default setting is `No connector selected`.
4. After you’ve completed all of the required fields, click **Create case**. A notification message confirms you successfully created the case. To view the case details, click the notification link or go to the [Cases](/solutions/observability/incident-management/cases.md) page.


### Add an alert to an existing case [observability-view-alerts-add-an-alert-to-an-existing-case]

To add an alert to an existing case:

1. Select **Add to existing case**.
2. Select the case where you will attach the alert. A confirmation message displays.

## Clean up alerts [clean-up-alerts-obs]

```{applies_to}
stack: preview 9.1 
```

Manage the size of alert indices in your space by clearing out alerts that are older or infrequently accessed. You can do this by [running an alert cleanup task](../../../explore-analyze/alerts-cases/alerts/view-alerts.md#clean-up-alerts), which deletes alerts according to the criteria that you define.