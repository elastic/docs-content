---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/alerts-ui-monitor.html
  - https://www.elastic.co/guide/en/serverless/current/security-alerts-ui-monitor.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Monitor rule executions [alerts-ui-monitor]

Several tools can help you gain insight into the performance of your detection rules:

* [Rule Monitoring tab](#rule-monitoring-tab) — The current state of all detection rules and their most recent executions. Go to the **Rule Monitoring** tab to get an overview of which rules are running, how long they’re taking, and if they’re having any trouble.
* [Execution results](#rule-execution-logs) — Historical data for a single detection rule’s executions over time. Consult the execution results to understand how a particular rule is running and whether it’s creating the alerts you expect.
* [Detection rule monitoring dashboard](../dashboards/detection-rule-monitoring-dashboard.md) — Visualizations to help you monitor the overall health and performance of {{elastic-sec}}'s detection rules. Consult this dashboard for a high-level view of whether your rules are running successfully and how long they’re taking to run, search data, and create alerts.

Refer to the [Troubleshoot missing alerts](../../../troubleshoot/security/detection-rules.md#troubleshoot-signals) section for strategies on adjusting rules if they aren’t creating the expected alerts.


## Rule Monitoring tab [rule-monitoring-tab]

To view a summary of all rule executions (including the most recent failures, execution times, and gaps in rule executions), select the **Rule Monitoring** tab on the **Rules** page. To access the tab, find **Detection rules (SIEM)** in the navigation menu or look for “Detection rules (SIEM)” using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to the **Rule Monitoring** tab.

:::{image} /solutions/images/security-monitor-table.png
:alt: monitor table
:screenshot:
:::

On the **Rule Monitoring** tab, you can [sort and filter rules](../detect-and-alert/manage-detection-rules.md#sort-filter-rules) just like you can on the **Installed Rules** tab.

::::{tip}
To sort the rules list, click any column header. To sort in descending order, click the column header again.
::::


For detailed information on a rule, the alerts it generated, and associated errors, click on its name in the table. This also allows you to perform the same actions that are available on the [**Installed Rules** tab](manage-detection-rules.md), such as modifying or deleting rules, activating or deactivating rules, exporting or importing rules, and duplicating prebuilt rules.

For information about rule execution gaps (which are periods of time when a rule didn't run), use the panel above the table. The panel contains the following:

* **Time filter**: Allows you to select a time range for viewing gap data. 
* **Total rules with gaps:** Provides metrics for rules with gaps:
  
  * {applies_to}`stack: ga 9.1+` Tells you the number of rules with unfilled gaps (left metric) and the number of rules with gaps being filled (right metric). 
  * {applies_to}`stack: ga =9.0` Tells you how many rules have unfilled or partially filled gaps within the selected time range. 

* {applies_to}`stack: ga 9.1+` **Only rules with unfilled gaps**: Filters the Rules table to only display rules with unfilled gaps. Note that the filter excludes rules with gaps that are being filled.   
* {applies_to}`stack: ga =9.0` **Only rules with gaps**: Filters the Rules table to only display rules with unfilled or partially filled gaps.

Within the Rules table, the **Last Gap (if any)** column conveys how long the most recent gap for a rule lasted. The **Unfilled gaps duration** column shows whether a rule still has gaps and provides a total sum of the remaining unfilled or partially filled gaps. The total sum can change based on the time range that you select in the panel above the table. If a rule has no gaps, the columns display a dash (`––`). 

::::{tip}
For a detailed view of a rule's gaps, go to the **Execution results** tab and check the [Gaps table](/solutions/security/detect-and-alert/monitor-rule-executions.md#gaps-table).
::::

## Execution results tab [rule-execution-logs]

From the **Execution results** tab, you can access the rule’s execution log, monitor and address gaps in a rule's execution schedule, and check manual runs for the rule. To find the tab, click the rule's name to open its details, then scroll down.

### Execution log table [execution-log-table]

Each detection rule execution is logged, including the execution type, the execution’s success or failure, any warning or error messages, how long it took to search for data, create alerts, and complete. This can help you troubleshoot a particular rule if it isn’t behaving as expected (for example, if it isn’t creating alerts or takes a long time to run).

:::{image} /solutions/images/security-rule-execution-logs.png
:alt: Execution log table on the rule execution results tab
:screenshot:
:::

You can hover over each column heading to display a tooltip about that column’s data. Click a column heading to sort the table by that column. Within the Execution log table, you can click the arrow at the end of a row to expand a long warning or error message.

Use these controls to filter what’s included in the logs table:

* The **Run type** drop-down filters the table by rule execution type:

    * **Scheduled**: Automatic, scheduled rule executions.
    * **Manual**: Rule executions that were [started manually](manage-detection-rules.md#manually-run-rules).

* The **Status** drop-down filters the table by rule execution status:

    * **Succeeded**: The rule completed its defined search. This doesn’t necessarily mean it generated an alert, just that it ran without error.
    * **Failed**: The rule encountered an error that prevented it from running. For example, a {{ml}} rule whose corresponding {{ml}} job wasn’t running.
    * **Warning**: Nothing prevented the rule from running, but it might have returned unexpected results. For example, a custom query rule tried to search an index pattern that couldn’t be found in {{es}}.

* The date and time picker sets the time range of rule executions included in the table. This is separate from the global date and time picker at the top of the rule details page.
* The **Source event time range** button toggles the display of data pertaining to the time range of manual runs.
* The **Show metrics columns** toggle includes more or less data in the table, pertaining to the timing of each rule execution.
* The **Actions** column allows you to show alerts generated from a given rule execution. Click the filter icon (![Filter icon](/solutions/images/security-filter-icon.png "title =20x20")) to create a global search filter based on the rule execution’s ID value. This replaces any previously applied filters, changes the global date and time range to 24 hours before and after the rule execution, and displays a confirmation notification. You can revert this action by clicking **Restore previous filters** in the notification.


### Gaps table [gaps-table]

```{applies_to}
   stack: preview 9.0, ga 9.1
```

Gaps in rule executions are periods of time where a rule didn’t run. They can be caused by various disruptions, including system updates, rule failures, or simply turning off a rule. Addressing gaps is essential for maintaining consistent coverage and avoiding missed alerts.

::::{tip}
Refer to the [Troubleshoot gaps](../../../troubleshoot/security/detection-rules.md#troubleshoot-gaps) section for strategies for avoiding gaps.
::::

Use the information in the Gaps table to assess the scope and severity of rule execution gaps. To control what's shown in the table, you can filter the table by gap status, select a time range for viewing gap data, and sort multiple columns. In {{stack}} 9.1 and Serverless, fill all gaps for the current rule by clicking **Fill all gaps** in the Gaps table. 

::::{note}
:applies_to: stack: ga 9.1+
From the Rules table, fill gaps for multiple rules with the [**Fill gaps** bulk action](/solutions/security/detect-and-alert/manage-detection-rules.md#bulk-fill-gaps-multiple-rules).
::::

:::{image} /solutions/images/security-gaps-table.png
:alt: Gaps table on the rule execution results tab
:screenshot:
:::

The Gaps table has the following columns:

* **Status**: The current state of the gap. It can be `Filled`, `Partially filled`, or `Unfilled`.
* **Detected at**: The date and time the gap was first discovered.
* **Manual fill tasks**: The status of the manual run that’s filling the gap. For more details about the manual run, refer to its entry in the [Manual runs table](/solutions/security/detect-and-alert/monitor-rule-executions.md#manual-runs-table).
* **Event time covered**: How much progress the manual run has made filling the gap.

    ::::{note}
    If you stop a manual run that's hasn't finished filling a gap, the gap’s status will be set to `Partially filled`. To fill the remaining gap, you can select the **Fill remaining gap** action or [manually run](/solutions/security/detect-and-alert/manage-detection-rules.md#manually-run-rules) the rule over the gap's time frame.
    ::::

* **Range**: When the gap started and ended.
* **Total gap duration**: How long the gap lasted.
* **Actions**: The actions that you can take for the gap. They can be **Fill gap** (starts a manual run to fill the gap) or **Fill remaining gap** (starts a manual run that fills the leftover portion of the gap).


### Manual runs table [manual-runs-table]

You can [manually run](/solutions/security/detect-and-alert/manage-detection-rules.md#manually-run-rules) enabled rules for a specified period of time to deliberately test them, provide additional rule coverage, or fill gaps in rule executions. Each manual run can produce multiple rule executions, depending on the time range of the run and the rule's execution schedule.

::::{note}
Manual runs are executed with low priority and limited concurrency, meaning they might take longer to complete. This can be especially apparent for rules requiring multiple executions.
::::

The Manual runs table tracks manual rule executions and provides important details such as:

* The total number of rule executions that the manual run will produce and how many are failing, pending, running, and completed.
* When the manual run started and the time range that it will cover.

    ::::{note}
    To stop an active run, go to the appropriate row in the table and click **Stop run** in the **Actions** column. Completed rule executions for each manual run are logged in the Execution log table.
    ::::

* The status of each manual run:

    * `Pending`: The rule is not yet running.
    * `Running`: The rule is executing during the time range you specified. Some rule types, such as indicator match rules, can take longer to run.
    * `Error`: The rule's configuration is preventing it from running correctly. For example, the rule's conditions cannot be validated.

:::{image} /solutions/images/security-manual-rule-run-table.png
:alt: Manual rule runs table on the rule execution results tab
:screenshot:
:::


