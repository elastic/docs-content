---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-run-log-pattern-analysis.html
applies_to:
  stack: all
products:
  - id: cloud-serverless
---

# Run a pattern analysis on log data [observability-run-log-pattern-analysis]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


Log pattern analysis helps you find patterns in unstructured log messages and makes it easier to examine your data. When you run a pattern analysis, it performs categorization analysis on a selected field, creates categories based on the data, and then displays them together in a chart that shows the distribution of each category and an example document that matches the category. Log pattern analysis is useful when you want to examine how often different types of logs appear in your data set. It also helps you group logs in ways that go beyond what you can achieve with a terms aggregation.

Log pattern analysis works on every text field.

To run a log pattern analysis:

1. In your {{obs-serverless}} project, go to **Discover** and select the **All logs** from the **Data view** menu.
2. Apply any filters that you want.
3. If you don’t see any results, expand the time range, for example, to **Last 15 days**.
4. In the **Available fields** list, select the text field you want to analyze, then click **Run pattern analysis**.

    ![Run log pattern analysis](/solutions/images/serverless-run-log-pattern-analysis.png "")

    The results of the analysis are shown in a table:

    :::{image} /solutions/images/serverless-log-pattern-analysis.png
    :alt: Log pattern analysis of the message field
    :screenshot:
    :::

5. (Optional) Select one or more patterns, then choose to filter for (or filter out) documents that match the selected patterns. Discover only displays documents that match (or don’t match) the selected patterns. The filter options enable you to remove unimportant messages and focus on the more important, actionable data during troubleshooting.
