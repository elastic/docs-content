---
navigation_title: "Pattern analysis"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/run-pattern-analysis-discover.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Detect patterns in unstructured logs with Discover's pattern analysis. Categorize log messages, identify common structures, and filter out noise during troubleshooting.
---

# Analyze log patterns in Discover [run-pattern-analysis-discover]

When troubleshooting with unstructured log data, manually identifying patterns is time-consuming. Pattern analysis automatically categorizes log messages to help you find common structures and filter out noise during investigation. This guide shows you how to run pattern analysis in Discover.

**Technical summary**: Open the **Patterns** tab in Discover, select a text field for analysis, adjust the minimum time range if needed, and filter or exclude patterns to focus on actionable data.

**Prerequisites:**

* You need a {{data-source}} with text fields containing log data
* Pattern analysis works on any text field in your data
* This example uses the [sample web logs data](../index.md#gs-get-data-into-kibana), or you can use your own data

1. Go to **Discover**.
2. Expand the {{data-source}} dropdown, and select **{{kib}} Sample Data Logs**.
3. If you don’t see any results, expand the time range, for example, to **Last 15 days**.
4. Click the **Patterns** tab next to **Documents** and **Field statistics**. The pattern analysis starts. The results are displayed under the chart. You can change the analyzed field by using the field selector. In the **Pattern analysis menu**, you can change the **Minimum time range**. This option enables you to widen the time range for calculating patterns which improves accuracy. The patterns, however, are still displayed by the time range you selected in step 3.

:::{image} /explore-analyze/images/kibana-log-pattern-analysis-results.png
:alt: Log pattern analysis results in Discover.
:screenshot:
:::

5. (optional) Apply filters to one or more patterns. **Discover** only displays documents that match the selected patterns. Additionally, you can remove selected patterns from **Discover**, resulting in the display of only those documents that don’t match the selected pattern. These options enable you to remove unimportant messages and focus on the more important, actionable data during troubleshooting. You can also create a categorization {{anomaly-job}} directly from the **Patterns** tab to find anomalous behavior in the selected pattern.

