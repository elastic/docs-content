---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/run-pattern-analysis-discover.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Detect patterns in unstructured data with pattern analysis in Discover. Categorize log messages, identify common structures, and filter noise during troubleshooting.
---

# Run a pattern analysis on your log data [run-pattern-analysis-discover]

Pattern analysis in **Discover** helps you find patterns in unstructured log messages by performing categorization analysis on text fields. It creates categories based on message structures, displays their distribution in a chart, and provides example documents for each pattern. This makes it easier to identify common log patterns, filter out noise, and focus on anomalous messages during troubleshooting.

:::{tip}
:applies_to: { stack: preview 9.4, serverless: preview }
You can also detect patterns from {{esql}}:

- {applies_to}`{ stack: preview 9.4, serverless: preview }` Use the [`CATEGORIZE`](elasticsearch://reference/query-languages/esql/functions-operators/grouping-functions/categorize.md) grouping function to render the results as expandable groups with row actions. Refer to [](/explore-analyze/discover/try-esql.md#esql-cascade-layout).
- {applies_to}`{ stack: preview 9.5, serverless: preview }` Add a [`SPARKLINE`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions/sparkline.md) aggregation to display an inline trend for each pattern. Refer to [Add sparklines to patterns](/explore-analyze/discover/try-esql.md#esql-cascade-pattern-sparkline).
:::

Pattern analysis works on any text field. This example uses the [sample web logs data](../index.md#gs-get-data-into-kibana), or you can use your own log data.

1. Go to **Discover**.
2. Expand the {{data-source}} dropdown, and select **Kibana Sample Data Logs**.
3. If you don’t see any results, expand the time range, for example, to **Last 15 days**.
4. Click the **Patterns** tab next to **Documents** and **Field statistics**. The pattern analysis starts. The results are displayed under the chart. You can change the analyzed field by using the field selector. In the **Pattern analysis menu**, you can change the **Minimum time range**. This option enables you to widen the time range for calculating patterns which improves accuracy. The patterns, however, are still displayed by the time range you selected in step 3.

:::{image} /explore-analyze/images/kibana-log-pattern-analysis-results.png
:alt: Log pattern analysis results in Discover.
:screenshot:
:::

5. (optional) Apply filters to one or more patterns. **Discover** only displays documents that match the selected patterns. Additionally, you can remove selected patterns from **Discover**, resulting in the display of only those documents that don’t match the selected pattern. These options enable you to remove unimportant messages and focus on the more important, actionable data during troubleshooting. You can also create a categorization {{anomaly-job}} directly from the **Patterns** tab to find anomalous behavior in the selected pattern.

