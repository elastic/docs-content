---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-aiops-analyze-spikes.html
---

# Analyze log spikes and drops [observability-aiops-analyze-spikes]

{{obs-serverless}} provides built-in log rate analysis capabilities, based on advanced statistical methods, to help you find and investigate the causes of unusual spikes or drops in log rates.

To analyze log spikes and drops:

1. In your {{obs-serverless}} project, go to **Machine learning** → **Log rate analysis**.
2. Choose a data view or saved search to access the log data you want to analyze.
3. In the histogram chart, click a spike (or drop) and then run the analysis.

    :::{image} ../../../images/serverless-log-rate-histogram.png
    :alt: Histogram showing log spikes and drops
    :class: screenshot
    :::

    When the analysis runs, it identifies statistically significant field-value combinations that contribute to the spike or drop, and then displays them in a table:

    :::{image} ../../../images/serverless-log-rate-analysis-results.png
    :alt: Histogram showing log spikes and drops
    :class: screenshot
    :::

    Notice that you can optionally turn on **Smart grouping** to summarize the results into groups. You can also click **Filter fields** to remove fields that are not relevant.

    The table shows an indicator of the level of impact and a sparkline showing the shape of the impact in the chart.

4. Select a row to display the impact of the field on the histogram chart.
5. From the **Actions** menu in the table, you can choose to view the field in **Discover**, view it in [Log Pattern Analysis](#log-pattern-analysis), or copy the table row information to the clipboard as a query filter.

To pin a table row, click the row, then move the cursor to the histogram chart. It displays a tooltip with exact count values for the pinned field which enables closer investigation.

Brushes in the chart show the baseline time range and the deviation in the analyzed data. You can move the brushes to redefine both the baseline and the deviation and rerun the analysis with the modified values.


## Log pattern analysis [log-pattern-analysis]

Use log pattern analysis to find patterns in unstructured log messages and examine your data. When you run a log pattern analysis, it performs categorization analysis on a selected field, creates categories based on the data, and then displays them together in a chart. The chart shows the distribution of each category and an example document that matches the category. Log pattern analysis is useful when you want to examine how often different types of logs appear in your data set. It also helps you group logs in ways that go beyond what you can achieve with a terms aggregation.

To run log pattern analysis:

1. Follow the steps under [Analyze log spikes and drops]() to run a log rate analysis.
2. From the **Actions** menu, choose **View in Log Pattern Analysis**.
3. Select a category field and optionally apply any filters that you want.
4. Click **Run pattern analysis**.

    The results of the analysis are shown in a table:

    :::{image} ../../../images/serverless-log-pattern-analysis.png
    :alt: Log pattern analysis of the message field
    :class: screenshot
    :::

5. From the **Actions** menu, click the plus (or minus) icon to open **Discover** and show (or filter out) the given category there, which helps you to further examine your log messages.
