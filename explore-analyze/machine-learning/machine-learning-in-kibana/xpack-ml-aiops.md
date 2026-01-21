---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/xpack-ml-aiops.html
  - https://www.elastic.co/guide/en/serverless/current/observability-machine-learning.html
  - https://www.elastic.co/guide/en/serverless/current/observability-aiops-analyze-spikes.html
  - https://www.elastic.co/guide/en/serverless/current/observability-aiops-detect-change-points.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
---

# AIOps Labs [xpack-ml-aiops]

AIOps Labs is a part of {{ml-app}} in {{kib}} which provides features that use advanced statistical methods to help you interpret your data and its behavior.

## Log rate analysis [log-rate-analysis]

Log rate analysis uses advanced statistical methods to identify reasons for increases or decreases in log rates and displays the statistically significant data in a tabular format. It makes it easy to find and investigate causes of unusual spikes or drops by using the analysis workflow view. Examine the histogram chart of the log rates for a given {{data-source}}, and find the reason behind a particular change possibly in millions of log events across multiple fields and values.

You can find log rate analysis embedded in multiple applications. In {{kib}}, you can find it under **{{ml-app}}** > **AIOps Labs** or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Here, you can select the {{data-source}} or saved Discover session that you want to analyze.

:::{image} /explore-analyze/images/kibana-ml-log-rate-analysis-before.png
:alt: Log event histogram chart
:screenshot:
:::

Select a spike or drop in the log event histogram chart to start the analysis. It identifies statistically significant field-value combinations that contribute to the spike or drop and displays them in a table. The table also shows an indicator of the level of impact and a sparkline showing the shape of the impact in the chart. Hovering over a row displays the impact on the histogram chart in more detail. You can inspect a field in **Discover**, further investigate in **Log pattern analysis**, or copy the table row information as a query filter to the clipboard by selecting the corresponding option under the **Actions** column. You can also pin a table row by clicking on it then move the cursor to the histogram chart. It displays a tooltip with exact count values for the pinned field which enables closer investigation.

Brushes in the chart show the baseline time range and the deviation in the analyzed data. You can move the brushes to redefine both the baseline and the deviation and rerun the analysis with the modified values.

% :::{image} /explore-analyze/images/kibana-ml-log-rate-analysis.png
% :alt: Log rate spike explained
% :screenshot:
% :::

## Log pattern analysis [log-pattern-analysis]

Log pattern analysis helps you to find patterns in unstructured log messages and makes it easier to examine your data. It performs categorization analysis on a selected field of a {{data-source}}, creates categories based on the data and displays them together with a chart that shows the distribution of each category and an example document that matches the category.

You can find log pattern analysis under **{{ml-app}}** > **AIOps Labs** or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Here, you can select the {{data-source}} or saved Discover session that you want to analyze, or in **Discover** as an available action for any text field.

:::{image} /explore-analyze/images/kibana-ml-log-pattern-analysis.png
:alt: Log pattern analysis UI
:screenshot:
:::

Select a field for categorization and optionally apply any filters that you want, then start the analysis. The analysis uses the same algorithms as a {{ml}} categorization job. The results of the analysis are shown in a table that makes it possible to open **Discover** and show or filter out the given category there, which helps you to further examine your log messages.

## Change point detection [change-point-detection]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::

Change point detection uses the [change point aggregation](elasticsearch://reference/aggregations/search-aggregations-change-point-aggregation.md) to detect distribution changes, trend changes, and other statistically significant change points in a metric of your time series data.

You can find change point detection under **{{ml-app}}** > **AIOps Labs** or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Here, you can select the {{data-source}} or saved Discover session that you want to analyze.

:::{image} /explore-analyze/images/kibana-ml-change-point-detection.png
:alt: Change point detection UI
:screenshot:
:::

Select a function and a metric field, then pick a date range to start detecting change points in the defined range. Optionally, you can split the data by a field. If the cardinality of the split field exceeds 10,000, then only the first 10,000, sorted by document count, are analyzed. You can configure a maximum of 6 combinations of a function applied to a metric field, partitioned by a split field to identify change points.

When a change point is detected, a row displays basic information including the timestamp of the change point, a preview chart, the type of change point, its p-value, the name and value of the split field. You can further examine the selected change point in a detailed view. A chart visualizes the identified change point within the analyzed time window, making the interpretation easier. If the analysis is split by a field, a separate chart is shown for every partition that has a detected change point. The chart displays the type of change point, its value, and the timestamp of the bucket where the change point has been detected. The corresponding `p-value` indicates the magnitude of the change; lower values indicate more significant changes. You can use the change point type selector to filter the results by specific types of change points.

:::{image} /explore-analyze/images/kibana-ml-change-point-detection-selected.png
:alt: Selected change points
:screenshot:
:::

You can attach change point charts to a dashboard or a case by using the context menu. If the split field is selected, you can either select specific charts (partitions) or set the maximum number of top change points to plot. It’s possible to preserve the applied time range or use the time bound from the page date picker. You can also add or edit change point charts directly from the **Dashboard** app.
