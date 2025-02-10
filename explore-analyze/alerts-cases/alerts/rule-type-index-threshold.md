---
navigation_title: "Index threshold"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/rule-type-index-threshold.html
---

# Index threshold [rule-type-index-threshold]

The index threshold rule type runs an {{es}} query. It aggregates field values from documents, compares them to threshold values, and schedules actions to run when the thresholds are met.

In **{{stack-manage-app}}** > **{{rules-ui}}**, click **Create rule**. Select the **Index threshold** rule type then fill in the name and optional tags.

## Define the conditions [_define_the_conditions]

When you create an index threshold rule, you must define the conditions for the rule to detect. For example:

:::{image} ../../../images/kibana-rule-types-index-threshold-conditions.png
:alt: Defining index threshold rule conditions in {kib}
:class: screenshot
:::

1. Specify the indices to query and a time field that will be used for the time window.
2. In the `WHEN` clause, specify how to calculate the value that is compared to the threshold. The value is calculated by aggregating a numeric field in a time window. The aggregation options are: count, average, sum, min, and max. When using count the document count is used and an aggregation field is not necessary.
3. In the `OVER` or `GROUPED OVER` clause, specify whether the aggregation is applied over all documents or split into groups using a grouping field. If grouping is used, an alert will be created for each group when it exceeds the threshold. To limit the number of alerts on high cardinality fields, you must specify the number of groups to check against the threshold. Only the top groups are checked.
4. Choose a threshold value and a comparison operator (`is above`, `is above or equals`, `is below`, `is below or equals`, or `is between`). The result of the aggregation is compared to this threshold.
5. In the `FOR THE LAST` clause, specify a time window. It determines how far back to search for documents and uses the time field set in the index clause.
6. Optionally add a KQL expression to further refine the conditions that the rule detects.
7. Set the check interval, which defines how often to evaluate the rule conditions. Generally this value should be set to a value that is smaller than the time window, to avoid gaps in detection.
8. In the advanced options, you can change the number of consecutive runs that must meet the rule conditions before an alert occurs. The default value is `1`.

If data is available and all clauses have been defined, a preview chart will render the threshold value and display a line chart showing the value for the last 30 intervals. This can provide an indication of recent values and their proximity to the threshold, and help you tune the clauses.

## Add actions [actions-index-threshold]

You can optionally send notifications when the rule conditions are met and when they are no longer met. In particular, this rule type supports:

* alert summaries
* actions that run when the threshold is met
* recovery actions that run when the rule conditions are no longer met

For each action, you must choose a connector, which provides connection information for a {{kib}} service or third party integration. For more information about all the supported connectors, go to [*Connectors*](../../../deploy-manage/manage-connectors.md).

After you select a connector, you must set the action frequency. You can choose to create a summary of alerts on each check interval or on a custom interval. For example, summarize the new, ongoing, and recovered alerts at a custom interval:

:::{image} ../../../images/kibana-rule-types-index-threshold-example-action-summary.png
:alt: UI for defining alert summary action in an index threshold rule
:class: screenshot
:::

Alternatively, you can set the action frequency such that actions run for each alert. Choose how often the action runs (at each check interval, only when the alert status changes, or at a custom action interval). You must also choose an action group, which indicates whether the action runs when the threshold is met or when the alert is recovered. Each connector supports a specific set of actions for each action group. For example:

:::{image} ../../../images/kibana-rule-types-index-threshold-example-action.png
:alt: UI for defining an action for each alert
:class: screenshot
:::

You can further refine the conditions under which actions run by specifying that actions only run when they match a KQL query or when an alert occurs within a specific time frame.

## Add action variables [action-variables-index-threshold]

The following action variables are specific to the index threshold rule. You can also specify [variables common to all rules](rule-action-variables.md).

`context.conditions`
:   A description of the threshold condition. Example: `count greater than 4`

`context.date`
:   The date, in ISO format, that the rule met the threshold condition. Example: `2020-01-01T00:00:00.000Z`.

`context.group`
:   The name of the action group associated with the threshold condition. Example: `threshold met`.

`context.message`
:   A preconstructed message for the rule. Example:<br> `rule 'kibana sites - high egress' is active for group 'threshold met':`<br> `- Value: 42`<br> `- Conditions Met: count greater than 4 over 5m`<br> `- Timestamp: 2020-01-01T00:00:00.000Z`

`context.title`
:   A preconstructed title for the rule. Example: `rule kibana sites - high egress met threshold`.

`context.value`
:   The value for the rule that met the threshold condition.

## Example [_example]

In this example, you will use the {{kib}} [sample weblog data set](https://www.elastic.co/guide/en/kibana/current/get-started.html) to set up and tune the conditions on an index threshold rule. For this example, you want to detect when any of the top four sites serve more than 420,000 bytes over a 24 hour period.

1. Go to **{{stack-manage-app}} > {{rules-ui}}** and click **Create rule**.
2. Select the **Index threshold** rule type.

    1. Provide a rule name.
    2. Select an index. Click **Index**, and set **Indices to query** to `kibana_sample_data_logs`. Set the **Time field** to `@timestamp`.
       :::{image} ../../../images/kibana-rule-types-index-threshold-example-index.png
       :alt: Choosing an index
       :class: screenshot
       :::

    3. To detect the number of bytes served during the time window, click **When** and select `sum` as the aggregation, and `bytes` as the field to aggregate.
       :::{image} ../../../images/kibana-rule-types-index-threshold-example-aggregation.png
       :alt: Choosing the aggregation
       :class: screenshot
       :::

    4. To detect the four sites that have the most traffic, click **Over** and select `top`, enter `4`, and select `host.keyword` as the field.
       :::{image} ../../../images/kibana-rule-types-index-threshold-example-grouping.png
       :alt: Choosing the groups
       :class: screenshot
       :::

    5. To trigger the rule when any of the top four sites exceeds 420,000 bytes over a 24 hour period, select `is above` and enter `420000`. Then click **For the last**, enter `24`, and select `hours`.
       :::{image} ../../../images/kibana-rule-types-index-threshold-example-threshold.png
       :alt: Setting the threshold
       :class: screenshot
       :::

    6. Schedule the rule to check every four hours.
       :::{image} ../../../images/kibana-rule-types-index-threshold-example-preview.png
       :alt: Setting the check interval
       :class: screenshot
       :::

        The preview chart will render showing the 24 hour sum of bytes at 4 hours intervals for the past 120 hours (the last 30 intervals).

    7. Change the time window and observe the effect it has on the chart. Compare a 24 window to a 12 hour window. Notice the variability in the sum of bytes, due to different traffic levels during the day compared to at night. This variability would result in noisy rules, so the 24 hour window is better. The preview chart can help you find the right values for your rule.
    8. Define the actions for your rule.

        You can add one or more actions to your rule to generate notifications when its conditions are met and when they are no longer met. For each action, you must select a connector, set the action frequency, and compose the notification details. For example, add an action that uses a server log connector to write an entry to the Kibana server log:
       :::{image} ../../../images/kibana-rule-types-index-threshold-example-action.png
       :alt: Add an action to the rule
       :class: screenshot
       :::

        The unique action variables that you can use in the notification are listed in [Add action variables](#action-variables-index-threshold). For more information, refer to [Actions](create-manage-rules.md#defining-rules-actions-details) and [*Connectors*](../../../deploy-manage/manage-connectors.md).

    9. Save the rule.

3. Find the rule and view its details in **{{stack-manage-app}} > {{rules-ui}}**. For example, you can see the status of the rule and its alerts:
   :::{image} ../../../images/kibana-rule-types-index-threshold-example-alerts.png
   :alt: View the list of alerts for the rule
   :class: screenshot
   :::

4. Delete or disable this example rule when it’s no longer useful. In the detailed rule view, select **Delete rule** from the actions menu.
