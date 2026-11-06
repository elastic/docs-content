---
navigation_title: Run a pattern analysis
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/run-pattern-analysis-discover.html
applies_to:
  stack: ga
  serverless: ga
type: how-to
products:
  - id: kibana
description: Group similar log messages into patterns in Discover to see common structures, filter out noise, and find unusual messages when you troubleshoot.
---

# Run a pattern analysis on your log data in Discover [run-pattern-analysis-discover]

If your logs are free-form messages, pattern analysis groups similar messages into patterns, so you can see which ones are common, filter out the noise, and focus on unusual messages while you troubleshoot. For each pattern, **Discover** shows how its messages are distributed over time in a chart, and gives example documents.

## Before you begin

- Make sure **Discover** is in classic mode. {{esql}} mode doesn't support this functionality. To switch, refer to [Switch to Discover's classic mode](switch-esql-mode.md#revert-to-classic-mode).
- You need a [Platinum or Enterprise subscription](https://www.elastic.co/subscriptions) or an active trial for Elastic Stack. Pattern analysis relies on a feature that requires it.
- **Discover** must have a [data view](../find-and-organize/data-views.md) selected that has a time field and contains a text field, and a time range that contains data.
- This example uses the [web logs sample data](/manage-data/ingest/sample-data.md). To follow along, add it and select its data view, or use your own log data.

:::{tip}
:applies_to: { serverless: preview, stack: preview 9.4+ }
In {{esql}} mode, you can [group similar messages in a query](inspect-grouped-stats.md#pattern-rendering).
:::

## Run a pattern analysis

1. Go to **Discover**.
2. Expand the data view menu, and select **Kibana Sample Data Logs**.
3. If you don't see any results, expand the time range, for example, to **Last 7 days**.
4. Select **Patterns** (or **View as** → **Patterns**, depending on your version). **Discover** groups the messages of a text field into patterns and lists them with the chart.

   :::{image} /explore-analyze/images/kibana-log-pattern-analysis-results.png
   :alt: Patterns view in Discover listing the patterns found in the log messages, with the View as menu open
   :screenshot:
   :width: 70%
   :::

5. Optional: To analyze a different text field, change the field in the field selector.
6. Optional: To calculate patterns over a longer period than the time range you set in step 3, select the {icon}`controls` **Options** button to open the **Pattern analysis settings**, and set the **Minimum time range**. A longer range improves accuracy. The list still shows the patterns for the time range you set in step 3.
7. Optional: To focus on specific messages, select one or more patterns, and then select **Filter for patterns in Discover**. To hide the messages that match them instead, select **Filter out patterns in Discover**.

**Result:** **Discover** shows the patterns in your log messages. After you filter, the table shows only the documents that match the patterns you kept, or only the ones that don't match the patterns you filtered out.

## Next steps

To find unusual behavior in a pattern, create a [categorization {{anomaly-job}}](../machine-learning/anomaly-detection/ml-configuring-categories.md#creating-categorization-jobs) from the **Patterns** view. This needs permission to create {{anomaly-jobs}}, and **Discover** doesn't show the button without it.

## Related pages

- [How to query in Discover's classic mode](use-classic-mode.md)
- [Search and filter with KQL, Lucene, and filters in Discover's classic mode](search-and-filter-classic.md)

