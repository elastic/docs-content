---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/alerts-ui-monitor.html
  - https://www.elastic.co/guide/en/serverless/current/security-alerts-ui-monitor.html
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Monitor Elastic Security detection rule executions, view execution results and details, check rule status, and identify and help troubleshoot performance issues using the Rule Monitoring tab and Execution results tab.
---

# Monitor rule executions [alerts-ui-monitor]

Detection rules only protect your environment when they run reliably. This page helps you confirm rules are running and troubleshoot when they're not.

| You want to | Where to go |
|-----------|-------------|
| Check if a rule succeeded, failed, or has warnings | [Rule execution status](#rule-status) (Rules table) |
| Compare status across all rules | [Rule Monitoring tab](#rule-monitoring-tab) |
| Review a specific rule's run history | [Execution results](#rule-execution-logs) (rule details page) |
| Fill gaps from missed rule runs | [Fill rule execution gaps](/solutions/security/detect-and-alert/fill-rule-gaps.md) |
| Run a rule manually for a specific time range | [Run rules manually](/solutions/security/detect-and-alert/manage-detection-rules.md#manually-run-rules) |
| View rule performance metrics in a dashboard | [Detection rule monitoring dashboard](../dashboards/detection-rule-monitoring-dashboard.md) |
| Investigate missing alerts | [Troubleshoot missing alerts](../../../troubleshoot/security/detection-rules.md#troubleshoot-signals) |


## Rule execution status [rule-status]

The **Last response** column in the Rules table displays the current status of each rule, based on the most recent attempt to run:

* **Succeeded**: The rule completed its defined search. This doesn't necessarily mean it generated an alert, just that it ran without error.
* **Failed**: The rule encountered an error that prevented it from running. For example, a {{ml}} rule whose corresponding {{ml}} job wasn't running.
* **Warning**: Nothing prevented the rule from running, but it might have returned unexpected results. For example, a custom query rule tried to search an index pattern that couldn't be found in {{es}}.

For {{ml}} rules, an indicator icon {icon}`warning` also appears in this column if a required {{ml}} job isn't running. Select the icon to list the affected jobs, then select **Visit rule details page to investigate** to open the rule's details page, where you can start the {{ml}} job.


## Rule Monitoring tab [rule-monitoring-tab]

To view a summary of all rule executions (including the most recent failures, execution times, and gaps), select the **Rule Monitoring** tab on the {{rules-ui}} page. To access the tab, find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to the **Rule Monitoring** tab.

:::{image} /solutions/images/security-monitor-table.png
:alt: monitor table
:screenshot:
:::

On the **Rule Monitoring** tab, you can [sort and filter rules](../detect-and-alert/manage-detection-rules.md#sort-filter-rules) just like you can on the **Installed Rules** tab.

::::{tip}
To sort the rules list, select any column header. To sort in descending order, select the column header again.
::::

For detailed information on a rule, the alerts it generated, and associated errors, select its name in the table. This also allows you to perform the same actions available on the [**Installed Rules** tab](manage-detection-rules.md), such as modifying or deleting rules, activating or deactivating rules, exporting or importing rules, and duplicating prebuilt rules.

### Gap information

The **Rule Monitoring** tab also displays information about gaps in rule executions. Gaps are periods when a rule didn't run as scheduled.

Several columns provide gap data:

* **Last Gap (if any)**: How long the most recent gap lasted.
* **Unfilled gaps duration**: Total duration of remaining unfilled or partially filled gaps. If a rule has no gaps, the column displays a dash (`––`).
* {applies_to}`stack: ga 9.3+` **Gap fill status**: The status of the rule's gaps (`Unfilled`, `In progress`, or `Filled`).

To learn how to find and fill gaps, refer to [Fill rule execution gaps](/solutions/security/detect-and-alert/fill-rule-gaps.md).


## Execution results tab [rule-execution-logs]

From the **Execution results** tab on a rule's details page, you can review how each run performed, monitor gaps, and check manual runs. To find this tab, select the rule's name to open its details, then scroll down.

Select the tab for your deployment. **{{stack}}** **9.4** and later and **{{ecloud}} Serverless** use the first tab. **{{stack}}** **9.3** and earlier use the second tab.

::::{applies-switch}

:::{applies-item} { stack: ga 9.4+, serverless: ga }

Each detection rule execution is logged with status, timing, and how many alerts the run produced. The table helps you understand rule performance and troubleshoot failures.

You can hover over each column heading to display a tooltip about that column's data. Select a column heading to sort the table by that column.

| Column | Description |
|--------|-------------|
| **Status** | Overall status of the execution. |
| **Run type** | Whether the run was a standard scheduled execution or a [manual backfill](/solutions/security/detect-and-alert/manage-detection-rules.md#manually-run-rules) run. |
| **Timestamp** | Date and time the rule execution started. |
| **Execution duration** | How long the rule took to run. |
| **Alerts created** | Number of new alerts generated during this execution. |
| **Message** | Outcome message from the execution (including warnings or errors when applicable). |

From the table, you can use the following row actions:

* **Filter alerts by rule execution ID**: Opens the Alerts table filtered to alerts from this execution. This control is disabled when the execution created no alerts (hover to see a tooltip).
* **View details**: Opens the [execution details flyout](#execution-details-flyout) for that run.

Use these controls to filter what appears in the table:

* The **Run type** drop-down filters by rule execution type:

    * **Scheduled**: Automatic, scheduled rule executions.
    * **Manual**: Rule executions that were [started manually](/solutions/security/detect-and-alert/manage-detection-rules.md#manually-run-rules).

* The **Status** drop-down filters by rule execution status:

    * **Succeeded**: The rule completed its defined search.
    * **Failed**: The rule encountered an error that prevented it from running.
    * **Warning**: The rule ran but might have returned unexpected results.

* The date and time picker sets the time range of rule executions included in the table. This is separate from the global date and time picker at the top of the rule details page.

Additional timing, indexing, and gap details that were previously available through extra table columns and toggles are now shown in the [execution details flyout](#execution-details-flyout).

:::

:::{applies-item} { stack: ga 9.0-9.3 }

The **Execution results** tab shows the run history in this layout. Each detection rule execution is logged, including the execution type, success or failure status, any warning or error messages, how long it took to search for data, create alerts, and complete. This can help you identify and troubleshoot a rule if it isn't behaving as expected (for example, if it isn't creating alerts or takes a long time to run).


You can hover over each column heading to display a tooltip about that column's data. Select a column heading to sort the table by that column. You can select the arrow at the end of a row to expand a long warning or error message.

Use these controls to filter what's included in the table:

* The **Run type** drop-down filters by rule execution type:

    * **Scheduled**: Automatic, scheduled rule executions.
    * **Manual**: Rule executions that were [started manually](/solutions/security/detect-and-alert/manage-detection-rules.md#manually-run-rules).

* The **Status** drop-down filters by rule execution status:

    * **Succeeded**: The rule completed its defined search.
    * **Failed**: The rule encountered an error that prevented it from running.
    * **Warning**: The rule ran but might have returned unexpected results.

* The date and time picker sets the time range of rule executions included in the table. This is separate from the global date and time picker at the top of the rule details page.
* The **Source event time range** button toggles the display of data pertaining to the time range of manual runs.
* The **Show metrics columns** toggle includes more or less data in the table, pertaining to the timing of each rule execution.
* The **Actions** column allows you to show alerts generated from a given rule execution. Select the filter icon {icon}`filterInCircle` to create a global search filter based on the rule execution's ID value. This replaces any previously applied filters, changes the global date and time range to 24 hours before and after the rule execution, and displays a confirmation notification. You can revert this action by selecting **Restore previous filters** in the notification.

:::

::::


### Execution details flyout [execution-details-flyout]
```yaml {applies_to}
stack: ga 9.4+
serverless: ga
```

Additional timing, indexing, and gap details are provided in the execution details flyout. Select **View details** on a row to open a side panel. The panel shows the execution ID (copyable) and the following fields:

Message
:   Whether the run completed successfully, plus errors or warnings (for example, index or query issues). Check this field first when a run failed or shows a warning, before you review timing or alert counts.

Source event time range
:   Manual runs only. `From` and `To` bound the source events the rule searched, not the clock time when the run started. Compare this to the run timestamp in the table above: a manual run can execute now while querying events from an earlier window. Scheduled runs rely on the rule’s schedule and look-back instead. This section is most relevant when validating a [manual run](/solutions/security/detect-and-alert/manage-detection-rules.md#manually-run-rules).

Candidate alerts
:   Detections produced by the rule query before deduplication and [alert suppression](/solutions/security/detect-and-alert/alert-suppression.md). If this number is high but **Alerts created** is low, review duplicate detection, suppression settings, and exception lists to find where alerts were dropped.

Alerts created
:   Alerts written to {{es}} after deduplication and suppression. These are the alerts shown on the **Alerts** page and in downstream workflows. Use this count to judge whether the run added meaningful new issues versus noise.

Matched indices
:   How many concrete indices matched the rule’s index patterns or data view for this run. If you expected data from a new index and this is `0`, check index names, data streams, and whether the index pattern includes the right time range.

Frozen indices queried
:   How many indices on the [frozen](/manage-data/lifecycle/data-tiers.md) data tier were searched. Searching frozen data can increase latency. A non-zero value here can explain slower search times in the breakdown below.

Gap duration
:   How long execution was behind the ideal schedule for this interval (missed or delayed coverage). Non-zero values mean some event time range was not searched on schedule. Refer to [Fill rule execution gaps](/solutions/security/detect-and-alert/fill-rule-gaps.md) and consider look-back, load, or maintenance windows.

Scheduling delay
:   Latency between the scheduled start time and when the run actually began. Large delays often point to queue backlog, cluster load, or resource limits rather than a problem inside the rule query itself.

Execution duration
:   End-to-end time for this run (search plus indexing work attributed to the run). Compare it to the rule’s run interval. If runs routinely approach or exceed the interval, consider narrowing scope, optimizing queries, or scaling the cluster.

Search
:   Time in {{es}} for queries and aggregations. If this value is the largest part of the breakdown, focus on query cost, index patterns, shard count, and whether frozen indices were queried.

Indexing
:   Time spent persisting new alerts. If this value is the largest part of the breakdown, investigate alert volume per run, bulk indexing health, and {{es}} performance on alert indices.

### Gaps table

The **Execution results** tab also includes a Gaps table that shows detailed gap information for the specific rule. To learn how to use the Gaps table to find and fill gaps, refer to [Fill rule execution gaps](/solutions/security/detect-and-alert/fill-rule-gaps.md#gaps-table).

### Manual runs table

The **Execution results** tab includes a Manual runs table that tracks manual rule executions. To learn more about running rules manually and monitoring manual runs, refer to [Run rules manually](/solutions/security/detect-and-alert/manage-detection-rules.md#manually-run-rules).
