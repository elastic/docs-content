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
description: Group similar log messages into patterns in Discover, or check how common one message is, to filter out noise and find unusual messages.
---

# Run a pattern analysis on your log data in Discover [run-pattern-analysis-discover]

If your logs are free-form messages, pattern analysis groups similar messages into patterns, so you can see which ones are common, filter out the noise, and focus on unusual messages while you troubleshoot. For each pattern, **Discover** shows how its messages are distributed over time in a chart, and gives example documents.

## Before you begin

- Make sure **Discover** is in classic mode. {{esql}} mode doesn't have the **Patterns** view. To switch, refer to [Switch to Discover's classic mode](switch-esql-mode.md#revert-to-classic-mode).
- {applies_to}`serverless: ga` Pattern analysis is available in {{es}}, Observability, and Security projects, except Observability projects on the Logs Essentials tier.
- {applies_to}`stack: ga` You need a [Platinum or higher subscription](https://www.elastic.co/subscriptions) or an active trial. Pattern analysis relies on a feature that requires it.
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

## Find similar messages in the table [find-similar-values-classic]
```{applies_to}
serverless: ga
stack: ga 9.6+
```

If one message in your results looks unusual, you can check how common it is without running a pattern analysis on the whole list first. **Discover** shows the pattern the message follows, the other documents that match it, and when they occurred. You can then open those documents or filter them out.

The **Find similar values** button appears only for text fields in a data view that has a time field. It has the same subscription and project requirements as pattern analysis. Refer to [Before you begin](#before-you-begin).

1. In classic mode, run a query that returns log messages. For example, select **Kibana Sample Data Logs** and expand the time range if the table is empty.
2. In the table, hover over a value in a text field column, such as `message`, and select **Find similar values**.
3. In the flyout, read the pattern that the message follows, the number of documents that match it, and the chart that shows when they occurred. The table in the flyout lists the matching documents. The analysis uses the query, filters, and time range of your table.

   :::{image} /explore-analyze/images/kibana-discover-find-similar-values-classic.png
   :alt: Similar values flyout in classic mode, with the pattern of a message, the chart and table of matching documents, and the sampling button
   :screenshot:
   :width: 70%
   :::

4. Optional: To trade speed against accuracy, select the sampling button at the top of the flyout. It reads **Auto sampling** by default, which sets the share of documents to analyze for you. To choose the share yourself, set **Random sampling** to **On - manual**, enter a **Sampling percentage** between 0.001 and 50, and select **Apply**. A lower percentage is faster but less accurate. To analyze every document, set **Random sampling** to **Off**.
5. Optional: To keep working with these documents, select **Open documents in Discover** to see only the documents that match the pattern. To see everything else instead, select **Filter out documents in Discover**.

**Result:** The flyout shows how common the message is and when it occurred. If you select one of the buttons in step 5, **Discover** opens a new tab, labeled **Pattern** followed by the field name, with your query and filters plus a filter that keeps or excludes the matching documents. Your original tab stays as it was.

In the **Summary** column, which gives an overview of each result, **Find similar values** analyzes the message of the document. For example, it uses `message`, `error.message`, or `event.original`, depending on which of these fields the document has.

In {{esql}} mode, refer to [](esql-results.md#find-similar-values-esql).

## Next steps

To find unusual behavior in a pattern, create a [categorization {{anomaly-job}}](../machine-learning/anomaly-detection/ml-configuring-categories.md#creating-categorization-jobs) from the **Patterns** view. This needs permission to create {{anomaly-jobs}}, and **Discover** doesn't show the button without it.

## Related pages

- [How to query in Discover's classic mode](use-classic-mode.md)
- [Search and filter with KQL, Lucene, and filters in Discover's classic mode](search-and-filter-classic.md)

