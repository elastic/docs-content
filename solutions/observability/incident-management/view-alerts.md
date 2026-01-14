---
navigation_title: View and manage alerts
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

# View and manage alerts in Elastic Observability [observability-view-alerts]

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

## Review related alerts [observability-view-alerts-find-related-alerts]
```{applies_to}
stack: ga 9.1 
```

Check related alerts to find other alerts that might be related to the same incident. You can add these alerts to a case and investigate them as a group instead of analyzing them individually.

To find related alerts, go to the **Related alerts** tab from an alert's details page. Within the table, alerts are ordered from most to least relevant. To only view alerts that were created around the same time as the current alert (+/- 30 minutes), apply the **Triggered around the same time** filter.

The relevancy of alerts is determined by how closely they match the current alert and other similiarites that they might share:

1. Alerts in the space are filtered down to only include alerts that were created about one day before or after the current alert. 
2. Data from the new subset of alerts is compared against the current alert to identify matching values and similarities. Data such as the time at which alerts were generated or recovered, tags added to the alerts, group values, and more are evaluated.
3. Alerts are scored based on how closely they match the current alert. Alerts with a score above a certain threshold are considered relevant and are included in the list of related alerts.


## Understand alert statuses [observability-view-alerts-understand-statuses]

There are four common alert statuses:

`active`
:   The conditions for the rule are met. If the rule has [actions](../../../explore-analyze/alerts-cases/alerts/create-manage-rules.md#defining-rules-actions-details), {{kib}} generates notifications based on the actions' notification settings. 

`flapping`

:   The alert switched repeatedly between active and recovered states. If actions are configured to run when its status changes, they are suppressed. Refer to [Configure alert flapping](/explore-analyze/alerts-cases/alerts/create-manage-rules.md#defining-rules-flapping-details) to learn more about configuring alert flapping for rules.

`recovered`
:   The conditions for the rule are no longer met. If the rule has [recovery actions](../../../explore-analyze/alerts-cases/alerts/create-manage-rules.md#defining-rules-actions-details), {{kib}} generates notifications based on the actions' notification settings. Recovery actions only run if the rule's conditions aren't met during the current rule execution, but were in the previous one. 


    An active alert changes to recovered if the conditions for the rule that generated it are no longer met. 

    A flapping alert changes to recovered when the rule's conditions are unmet for a specific number of consecutive runs. This number is determined by the **Alert status change threshold** setting, which you can configure under the **Alert flapping detection** settings.
    
    For example, if the threshold requires an alert to change status at least 6 times in the last 10 runs to be considered flapping, then to recover, the rule's conditions must remain unmet for 6 consecutive runs. If the rule's conditions are met at any point during this recovery period, the count of consecutive unmet runs will reset, requiring the alert to remain unmet for an additional 6 consecutive runs to finally be reported as recovered.

    Once a flapping alert is recovered, it cannot be changed to flapping again. Only new alerts with repeated status changes are candidates for the flapping status. 

`untracked`
:   The rule is disabled, or you’ve marked the alert as untracked. To mark the alert as untracked, go to the **Alerts** table, click the {icon}`boxes_horizontal` icon to expand the **More actions** menu, and click **Mark as untracked**. When an alert is marked as untracked, actions are no longer generated and the alert's status can no longer be changed. You can choose to move active alerts to this state when you disable or delete rules.

## Apply and filter alert tags [observability-view-alerts-tag-alerts]

Use alert tags to organize related alerts into categories that you can filter and group. For example, use the `Production` alert tag to label a group of alerts as notifications from your production environment. Search for tags by entering the `kibana.alert.workflow_tags : "Production"` query into the KQL bar. Alternatively, use the Alert table’s drop-down filters to filter for tagged alerts.

::::{tip}
To display alert tags in the Alerts table, click **Fields**, then add the `kibana.alert.workflow_tags` field. 
::::

To apply or remove alert tags on individual alerts:

1. Go to the Alerts table, click the **More actions** menu ({icon}`boxes_vertical`) in an alert’s row, then click **Edit tags**. 
2. In the flyout, do one of the following:
   
    * **Apply a new tag**: Enter a new tag into the search bar, then select the **Add _tag name_ as a tag** or click enter on your keyboard to apply your changes.
    * **Remove existing tags**: Click the tag that you want to remove. To remove all tags from the alert, click **Select none**.
        ::::{important}
        Removing tags from an alert permanently deletes them. 
        ::::

3. Click **Save selection** to apply your changes to the alert. 

To apply or remove alert tags on multiple alerts, select the alerts you want to change, then click **Selected *x* alerts** at the upper-left above the table. Click **Edit alert tags**, select or unselect tags, then click **Save selection**.

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