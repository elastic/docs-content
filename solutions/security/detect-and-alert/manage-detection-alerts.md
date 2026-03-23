---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/alerts-ui-manage.html
  - https://www.elastic.co/guide/en/serverless/current/security-alerts-manage.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Filter, triage, and take actions on detection alerts from the Alerts page.
---

# Manage detection alerts [security-alerts-manage]

The Alerts page is your central hub for triaging and investigating detection alerts. Filter alerts to focus on what matters, change statuses to track progress, and take actions to investigate or respond.

:::{agent-skill}
:url: https://github.com/elastic/agent-skills/tree/main/skills/security/alert-triage
:::

:::{image} /solutions/images/security-alert-page.png
:alt: Alerts page overview
:screenshot:
:::


## Quick reference [quick-reference]

| Task | How to do it |
|------|--------------|
| View alert details | Click the **View details** icon {icon}`expand` in the Alerts table |
| Filter by rule | Use KQL: `kibana.alert.rule.name: "Rule Name"` |
| Filter by time | Use the date/time picker (default: last 24 hours) |
| Change alert status | Click the **More actions** icon {icon}`boxes_horizontal` > select status, or use bulk selection |
| Add to case | Click the **More actions** icon {icon}`boxes_horizontal` > **Add to case** |
| Investigate in Timeline | Click **Investigate in timeline** icon {icon}`timeline` |
| Add exception | Click the **More actions** icon {icon}`boxes_horizontal` > **Add exception** |


## Filter alerts [detection-view-and-filter-alerts]

| Filter method | Description |
|---------------|-------------|
| KQL search | Enter queries like `kibana.alert.rule.name: "SSH from the Internet"`. Autocomplete is available for `.alerts-security.alerts-*` indices. |
| Date/time picker | Set a specific time range (default: last 24 hours). |
| Drop-down controls | Filter by status, severity, user, host, or [custom fields](#drop-down-filter-controls). |
| Additional filters | Include [building block alerts](/solutions/security/detect-and-alert/about-building-block-rules.md) or show only indicator match rule alerts. |
| Visualization section | Group and visualize alerts by field. Refer to [Visualize detection alerts](/solutions/security/detect-and-alert/visualize-detection-alerts.md). |

### Inline actions

Hover over any value in the Alerts table to see inline actions. Click the expand icon for more options:

| Action | Description |
|--------|-------------|
| Filter for value | Add the value as a filter |
| Filter out value | Exclude the value |
| Show top *x* | View most common values |
| Add to timeline | Add the field value to Timeline for investigation |
| Copy to clipboard | Copy the value |

:::{image} /solutions/images/security-inline-actions-menu.png
:alt: Inline additional actions menu
:screenshot:
:::

### View rule-specific alerts

Go to **Rules** > **Detection rules (SIEM)**, then select a rule name. The rule details page shows all alerts from that rule, including alerts from previous rule revisions.


## Edit drop-down filter controls [drop-down-filter-controls]

Customize the filter controls above the Alerts table. By default, you can filter by **Status**, **Severity**, **User**, and **Host**.

:::{image} /solutions/images/security-alert-page-dropdown-controls.png
:alt: Alerts page with drop-down controls highlighted
:screenshot:
:::

| Action | How to do it |
|--------|--------------|
| Edit controls | Click {icon}`boxes_horizontal` next to controls > **Edit Controls** |
| Reorder | Drag controls by their handle |
| Remove | Hover over control > click **Remove control** |
| Add | Click **Add Controls** (maximum 4) |
| Save changes | Click **Save pending changes** |

::::{note}
- The **Status** control cannot be removed.
- Changes are saved in your browser's local storage, not your user profile.
::::


## Group alerts [group-alerts]

Group alerts by up to three fields, such as rule name, host, user, source IP, or custom fields. Groups nest in the order you select them.

:::{image} /solutions/images/security-group-alerts.png
:alt: Alerts table with Group alerts by drop-down
:screenshot:
:::

| Action | How to do it |
|--------|--------------|
| Group alerts | Click **Group alerts by** > select field(s) |
| Expand a group | Click the group name or expand icon |
| Bulk action on group | Click **Take actions** menu on the group row |


## Customize the Alerts table [customize-the-alerts-table]

### Toolbar options

| Button | Function |
|--------|----------|
| Columns | Reorder columns |
| Sort fields | Sort by one or more columns |
| Fields | Add or remove fields (including [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md)) |
| Full screen | Expand table to full screen |

:::{image} /solutions/images/security-alert-table-toolbar-buttons.png
:alt: Alerts table with toolbar buttons highlighted
:screenshot:
:::

### View modes

| Mode | Description |
|------|-------------|
| Grid view | Traditional table with columns for each field. Click the expand icon in the **Reason** column to see rendered alert details. |
| Event rendered view | Descriptive event flow showing relevant context. |

:::{image} /solutions/images/security-event-rendered-view.png
:alt: Alerts table with the Event rendered view enabled
:screenshot:
:::


## Take actions on an alert [alert-actions]

Access actions from the **More actions** (**…**) menu in the Alerts table, or from **Take action** in the alert details flyout.

| Action | Description |
|--------|-------------|
| [Change status](#detection-alert-status) | Mark as open, acknowledged, or closed |
| [Add to case](/explore-analyze/cases/attach-objects-to-cases.md) | Attach alert to a new or existing case |
| {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` [Run a workflow from an alert](#run-workflow-from-alert) | Run an Elastic workflow for on-demand response or investigation |
| [Add rule exception](#add-exception-from-alerts) | Prevent rule from generating similar alerts |
| [Add {{elastic-endpoint}} exception](/solutions/security/detect-and-alert/add-manage-exceptions.md#endpoint-rule-exceptions) | Prevent {{elastic-endpoint}} alerts for specific conditions |
| [Apply alert tags](#apply-alert-tags) | Categorize alerts for filtering |
| [Assign users](#assign-users-to-alerts) | Assign analysts to investigate |
| [Investigate in Timeline](#signals-to-timelines) | Open alert in Timeline for analysis |
| [Analyze process tree](/solutions/security/investigate/visual-event-analyzer.md) | Visualize process relationships |
| [Isolate host](/solutions/security/endpoint-response-actions/isolate-host.md) | Isolate the alert's host from the network |
| [Run Osquery](/solutions/security/investigate/run-osquery-from-alerts.md) | Query the host for additional context |
| [Response actions](/solutions/security/endpoint-response-actions.md) | Execute response actions on the host |

### Change alert status [detection-alert-status]

Alert statuses track investigation progress:

| Status | Meaning |
|--------|---------|
| Open | Needs investigation (default view) |
| Acknowledged | Under active investigation |
| Closed | Resolved |

**To change status:**

| Scope | How to do it |
|-------|--------------|
| Single alert | **More actions** icon {icon}`boxes_horizontal` > select status |
| Multiple alerts | Select alerts > **Selected *x* alerts** > select status |
| Grouped alerts | **Take actions** menu on group row > select status |
| From flyout | **Take action** > select status |

:::{image} /solutions/images/security-alert-change-status.png
:alt: Bulk action menu with multiple alerts selected
:screenshot:
:::

#### Closing reasons
```yaml {applies_to}
stack: ga 9.2
serverless: ga
```

When closing alerts, you can specify a reason:

| Reason | Use when |
|--------|----------|
| Close without reason | No specific categorization needed |
| Duplicate | Alert duplicates another alert |
| False positive | Normal activity, not a security issue |
| True positive | Real incident that's been resolved |
| Benign positive | Real activity but acceptable/not actionable |
| Other | Other reasons |

::::{tip}
:applies_to: {stack: ga 9.4+, serverless: ga}
You can add your own closing reason options by updating the `securitySolution:alertCloseReasons` advanced setting. Refer to [Add custom alert closing reasons](/solutions/security/get-started/configure-advanced-settings.md#custom-alert-closing-reasons) for more information.
::::

The closing reason is stored in `kibana.alert.workflow_reason` and can be used for filtering. Reopening an alert removes this field.

### Run a workflow from an alert [run-workflow-from-alert]
```yaml {applies_to}
stack: ga 9.4+
serverless: ga
```

You can run an [Elastic workflow](/explore-analyze/workflows.md) directly from an alert to trigger an on-demand response or investigation. To use this feature, make sure you meet the [workflows prerequisites](/explore-analyze/workflows/get-started.md#workflows-prerequisites).

To run a workflow on an individual alert, do one of the following:

* In the Alerts table, click **More actions** ({icon}`boxes_vertical`) in an alert's row, then click **Run workflow**. Use the search bar to select a workflow, then click **Run workflow**.
* In an alert's details flyout, click **Take action → Run workflow**. Use the search bar to select a workflow, then click **Run workflow**.

::::{note}
You can select only enabled workflows.
::::

To run a workflow on multiple alerts, select the alerts, then click **Selected *x* alerts** at the upper-left above the table. Click **Run workflow**, select a workflow, then click **Run workflow**.

### Apply alert tags [apply-alert-tags]

Tags help organize alerts into filterable categories.

| Task | How to do it |
|------|--------------|
| Tag single alert | **More actions** icon {icon}`boxes_horizontal` > **Apply alert tags** |
| Tag multiple alerts | Select alerts > **Selected *x* alerts** > **Apply alert tags** |
| Tag from flyout | **Take action** > **Apply alert tags** |
| Filter by tag | KQL: `kibana.alert.workflow_tags: "False Positive"` |
| Show tags column | **Fields** > add `kibana.alert.workflow_tags` |
| Manage tag options | [Configure `securitySolution:alertTags`](/solutions/security/get-started/configure-advanced-settings.md#manage-alert-tags) |


### Assign users to alerts [assign-users-to-alerts]

Assign analysts to alerts they should investigate.

::::{important}
Users are not notified when assigned or unassigned.
::::

| Task | How to do it |
|------|--------------|
| Assign to single alert | **More actions** icon {icon}`boxes_horizontal` > **Assign alert** > select users |
| Assign to multiple alerts | Select alerts > **Selected *x* alerts** > **Assign alert** |
| Assign from flyout | **Take action** > **Assign alert**, or click the assign icon at top |
| Unassign all users | **More actions** icon {icon}`boxes_horizontal` > **Unassign alert** |
| Show assignees column | **Fields** > add `kibana.alert.workflow_assignee_ids` |
| Filter by assignee | Click **Assignees** filter above table |

:::{image} /solutions/images/security-alert-assigned-alerts.png
:alt: Alert assignees in the Alerts table
:screenshot:
:::


### Add rule exception [add-exception-from-alerts]

Create an [exception](/solutions/security/detect-and-alert/rule-exceptions.md) to prevent a rule from generating similar alerts.

| Location | How to do it |
|----------|--------------|
| Alerts table | **More actions** icon {icon}`boxes_horizontal` > **Add exception** |
| Alert details flyout | **Take action** > **Add rule exception** |


### Investigate in Timeline [signals-to-timelines]

| Scope | How to do it |
|-------|--------------|
| Single alert | Click **Investigate in timeline** button in table, or **Take action** > **Investigate in timeline** |
| Multiple alerts | Select alerts (up to 2,000) > **Selected *x* alerts** > **Investigate in timeline** |

:::{image} /solutions/images/security-timeline-button.png
:alt: Investigate in timeline button
:screenshot:
:::

::::{tip}
For [threshold rule](/solutions/security/detect-and-alert/using-the-rule-ui.md) alerts, Timeline shows all matching events, not only those that crossed the threshold.
::::

If the rule uses a Timeline template, dropzone query values are replaced with the alert's actual field values.


## Clean up alerts [clean-up-alerts-sec]

```{applies_to}
stack: ga 9.4+, preview 9.1-9.3
serverless: ga
```

Manage the size of alert indices in your space by clearing out alerts that are older or infrequently accessed. You can do this by [running an alert cleanup task](../../../explore-analyze/alerting/kibana-alerting-v1/view-alerts-v1.md#clean-up-alerts), which deletes alerts according to the criteria that you define.