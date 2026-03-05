---
navigation_title: Fill rule execution gaps
applies_to:
  stack: ga
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Find and fill gaps in Elastic Security detection rule executions manually or automatically to ensure continuous threat monitoring and avoid missed alerts.
---

# Fill rule execution gaps [fill-rule-gaps]

Gaps are periods when a detection rule didn't run as scheduled. They can be caused by various disruptions, including system updates, resource constraints, or simply turning off a rule. Addressing gaps is essential for maintaining consistent detection coverage and avoiding missed alerts.

This page explains how to find gaps and fill them, either manually or automatically.

## Find gaps [find-gaps]

You can find gaps from two locations:

* **Rule Monitoring tab**: Provides an overview of gaps across all rules
* **Gaps table**: Shows detailed gap information for a specific rule

### Rule Monitoring tab [rule-monitoring-tab-gaps]

From the **Rule Monitoring** tab on the {{rules-ui}} page, you can get an overview of existing gaps and their status. The total number of rules with gaps is tracked in the panel above the Rules table.

::::{applies-switch}

:::{applies-item} { "stack": "ga 9.3+"}
The panel displays:
* **Rules with gaps**: The number of rules with gaps (left metric) and the number of rules with all gaps filled (right metric). Shows data from the last 90 days.
:::

:::{applies-item} { "stack": "ga 9.1-9.2" }
The panel displays:
* **Time filter**: Select a time range for viewing gap data.
* **Total rules with gaps**: The number of rules with unfilled gaps (left metric) and rules with gaps being filled (right metric) within the selected time range.
* **Only rules with unfilled gaps**: Filters the Rules table to only display rules with unfilled gaps (excludes rules with gaps currently being filled).
:::

:::{applies-item} { "stack": "ga =9.0" }
The panel displays:
* **Time filter**: Select a time range for viewing gap data.
* **Total rules with gaps**: The number of rules with unfilled or partially filled gaps within the selected time range.
* **Only rules with gaps**: Filters the Rules table to only display rules with unfilled or partially filled gaps.
:::

::::

Within the Rules table, several columns provide additional gap data:

* **Last Gap (if any)**: Shows how long the most recent gap for a particular rule lasted.
* **Unfilled gaps duration**: Shows whether a rule still has gaps and provides a total sum of the remaining unfilled or partially filled gaps. The total can change based on the time range you select (data on gaps older than 90 days is not retained). If a rule has no gaps, the column displays a dash (`––`).
* {applies_to}`stack: ga 9.3+` **Gap fill status**: Shows the status of the rule's gaps (`Unfilled`, `In progress`, or `Filled`).

    ::::{tip}
    :applies_to:{stack: ga 9.3+}
    Use the **Gap fill status** filter in the Rules table to find rules with a specific gap status.
    ::::

### Gaps table [gaps-table]

```{applies_to}
stack: preview =9.0, ga 9.1+
```

The Gaps table on a rule's **Execution results** tab provides detailed information about that rule's gaps. Use it to assess the scope and severity of gaps for a specific rule.

To access the Gaps table, select a rule's name to open its details, then scroll to the **Execution results** tab.

{applies_to}`stack: ga 9.3+` To fill all gaps for the rule at once, select **Fill all gaps**.

:::{image} /solutions/images/security-gaps-table.png
:alt: Gaps table on the rule execution results tab
:screenshot:
:::

The Gaps table has the following columns:

| Column | Description |
|---|---|
| Status | The current state of the gap: `Filled`, `Partially filled`, or `Unfilled`. |
| Detected at | When the gap was first discovered. |
| Manual fill tasks | The status of the manual run filling the gap. For details, refer to the [Manual runs table](/solutions/security/detect-and-alert/manage-detection-rules.md#manual-runs-table). |
| Event time covered | How much progress the manual run has made filling the gap. |
| Range | When the gap started and ended. |
| Total gap duration | How long the gap lasted. |
| Actions | Available actions: **Fill gap** (starts a manual run) or **Fill remaining gap** (fills the leftover portion of a partially filled gap). |

::::{note}
If you stop a manual run before it finishes filling a gap, the gap's status changes to `Partially filled`. To fill the remaining gap, select **Fill remaining gap** or [manually run](/solutions/security/detect-and-alert/manage-detection-rules.md#manually-run-rules) the rule over the gap's time frame.
::::


## Fill gaps manually [fill-gaps-manually]

You can manually fill gaps in two ways:

* **For a specific rule**: Use the **Fill gap** action in the rule's [Gaps table](#gaps-table).
* **For multiple rules**: Use the **Fill gaps** bulk action from the Rules table.

### Fill gaps for multiple rules [bulk-fill-gaps]

```{applies_to}
stack: ga 9.1+
```

From the Rules table, fill gaps for multiple rules using the **Fill gaps** bulk action.

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the Rules table, select the **Rule Monitoring** tab, then do one of the following:

    * Fill rules with unfilled or partially filled gaps: Select the appropriate rules or all rules on the page, then select **Bulk actions** > **Fill gaps**.
    * Only fill rules with unfilled gaps: Filter for rules with unfilled gaps:
       - {applies_to}`stack: ga 9.3+` Use the **Gap fill status** filter in the Rules table to find rules with the `Unfilled` gap status, then select **Bulk actions** > **Fill gaps**.
       - {applies_to}`stack: ga 9.1-9.2` In the panel above the table, select the **Only rules with unfilled gaps** filter to show only rules with unfilled gaps (excludes rules with gaps currently being filled). Select the appropriate rules, then select **Bulk actions** > **Fill gaps**.

3. Specify when to start and end the manual run that fills the gaps.
4. Select **Schedule gap fills**. The rule runs over unfilled gaps in the selected time range.

After scheduling the manual run, track gap fill progress by checking the **Total rules with gaps** field in the panel above the Rules table. The left metric shows remaining rules with unfilled gaps; the right metric shows rules currently having their gaps filled.

You can also check gap fill progress for individual rules by opening their details page and viewing the [Gaps table](#gaps-table) on the **Execution results** tab.


## Fill gaps automatically [fill-gaps-automatically]

```{applies_to}
stack: ga 9.3+
```

::::{note}
Automatic gap fill requires the appropriate subscription. Refer to the subscription page for [{{ecloud}}](https://www.elastic.co/subscriptions/cloud) and [{{stack}}/self-managed](https://www.elastic.co/subscriptions) for feature availability.
::::

When enabled, the automatic gap fill feature runs a job every two minutes to check for new and existing gaps, then schedules tasks to fill them.

### Enable automatic gap fill

1. On the {{rules-ui}} page, select **Settings** (above the Rules table).
2. In the **Auto gap fill settings** section, turn on the toggle.

::::{tip}
The **Auto gap fill status** field (in the panel above the Rules table) shows whether automatic gap fill is on or off. Select the field value to access the settings.
::::

### Monitor automatic gap fill

Details about the automatic gap fill job and scheduled tasks are captured in the gap fill scheduler logs. Access the logs by selecting **Gap fill scheduler** in the **Auto gap fill settings** section.

In the scheduler logs table, expand rows to learn more about gaps discovered and tasks scheduled each time the job ran. Key details include:

* When each job ran to check for gaps
* The number of gaps detected and rules affected
* The number of gap fill tasks scheduled
* Task status:
    * **Success**: Gap fill tasks were successfully scheduled. Check log details to see if any rules were not processed.
    * **Error**: Some gap fill tasks were not scheduled or failed to run. Check log details for more information.
    * **Task skipped**: Gap fill tasks were scheduled but did not run (rules may have been disabled or the maximum task limit was reached).
    * **No gaps**: No gaps were detected; no tasks were scheduled.


## Troubleshoot gaps

Refer to the [Troubleshoot gaps](../../../troubleshoot/security/detection-rules.md#troubleshoot-gaps) section for strategies on avoiding and resolving gaps.
