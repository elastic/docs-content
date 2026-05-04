---
navigation_title: Lens
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/lens.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Lens [lens]

**Lens** is {{kib}}'s modern, drag‑and‑drop visualization editor designed to make data exploration fast and intuitive. It allows you to build charts and tables by dragging fields from a data view onto a workspace, while {{kib}} automatically suggests the most appropriate visualization types based on the data.

## Supported chart types [chart-types]

With Lens, you can create the following visualization types:

**Charts to show change over time**

| Visualization | Best for |
|---|---|
| [Bar](/explore-analyze/visualize/charts/bar-charts.md) | Compare values across discrete categories or show distributions with histogram buckets. |
| [Line](/explore-analyze/visualize/charts/line-charts.md) | Show how a metric changes over time or another continuous dimension. |
| [Area](/explore-analyze/visualize/charts/area-charts.md) | Show change over time while emphasizing volume or stacked proportions. |

**Charts to show part-to-whole relationships**

| Visualization | Best for |
|---|---|
| [Pie](/explore-analyze/visualize/charts/pie-charts.md) | Show how parts make up a whole with a small number of slices. |
| [Treemap](/explore-analyze/visualize/charts/treemap-charts.md) | Show hierarchical proportions across nested categories. |
| [Waffle](/explore-analyze/visualize/charts/waffle-charts.md) | Show part-to-whole as a grid of equal cells where filled cells represent proportion. |
| [Mosaic](/explore-analyze/visualize/charts/mosaic-charts.md) | Compare part-to-whole across two categorical dimensions in a tiled layout. |

**Charts to show a single value or progress**

| Visualization | Best for |
|---|---|
| [Metric](/explore-analyze/visualize/charts/metric-charts.md) | Highlight a single KPI or a small set of critical numbers. |
| [Gauge](/explore-analyze/visualize/charts/gauge-charts.md) | Show progress toward a target or status against thresholds for a single metric. |

**Additional visualizations for tabular data, spatial patterns, and text analysis.**

| Visualization | Best for |
|---|---|
| [Table](/explore-analyze/visualize/charts/tables.md) | Present precise values, rankings, or multi-metric details in a compact layout. |
| [Heat map](/explore-analyze/visualize/charts/heat-map-charts.md) | Reveal density or patterns across two dimensions using color intensity. |
| [Tag cloud](/explore-analyze/visualize/charts/tag-cloud-charts.md) | Highlight the most frequent or important terms in a dataset. |
| [Region map](/explore-analyze/visualize/charts/region-map-charts.md) | Show how values vary across geographic regions (choropleth). |

## Create visualizations [create-the-visualization-panel]

If you're unsure about the visualization type you want to use, or how you want to display the data, drag the fields you want to visualize onto the workspace, then let **Lens** choose for you.

If you already know the visualization type you want to use, and how you want to display the data, use the following process.

:::::{stepper}

::::{step} Choose the visualization type

New visualizations generally default to **Bar** or **Line** charts. You can change that manually to the visualization type that you want.

As you drag fields into the workspace or to the layer pane, Lens automatically generates alternative visualizations. To view them, click **Suggestions** at the bottom of the workspace. If a suggested visualization meets your needs, click **Save and return** to add it to the dashboard.

::::

::::{step} Choose the data you want to visualize

As you drag fields to the layer pane, Lens automatically selects an aggregation function, for example **Date histogram**, **Intervals**, or **Top values**. Click a field to learn more about its data or to edit its appearance.

::::

::::{step}  Customize the appearance of your visualization

In the Lens editor, you can customize the appearance of your visualization by clicking the **Style** icon {icon}`brush` and the **Legend** icon ![Legend icon](/explore-analyze/images/kibana-legend-icon.svg "") in the layer pane.

::::

::::{step} Save or add the visualization to a dashboard

- If you accessed Lens from a dashboard, select **Save and return** to save the visualization and add it to that dashboard, or select **Save to library** to add the visualization to the Visualize library and reuse it later.
- If you accessed Lens from the Visualize library, select **Save**. A menu opens and lets you add the visualization to a dashboard and to the Visualize library.

::::

:::::

## Create visualizations with the API [create-visualizations-with-the-api]

```{applies_to}
stack: preview 9.4+
serverless: preview
```

You can create and manage Lens visualizations programmatically using the [Visualizations API](https://elastic.github.io/dashboards-api-spec/#tag/Visualizations). This is useful for managing visualizations as code, automating their lifecycle, or building tooling around Lens charts.

:::{note}
The Visualizations API is in technical preview and may change in future releases.
:::

The following chart-type pages include **Create this chart using the API** dropdowns with example payloads you can use directly:

- [Bar charts](/explore-analyze/visualize/charts/bar-charts.md)
- [Line charts](/explore-analyze/visualize/charts/line-charts.md)
- [Area charts](/explore-analyze/visualize/charts/area-charts.md)
- [Pie charts](/explore-analyze/visualize/charts/pie-charts.md)
- [Treemap charts](/explore-analyze/visualize/charts/treemap-charts.md)
- [Waffle charts](/explore-analyze/visualize/charts/waffle-charts.md)
- [Mosaic charts](/explore-analyze/visualize/charts/mosaic-charts.md)
- [Metric charts](/explore-analyze/visualize/charts/metric-charts.md)
- [Gauge charts](/explore-analyze/visualize/charts/gauge-charts.md)
- [Table](/explore-analyze/visualize/charts/tables.md)
- [Heat map charts](/explore-analyze/visualize/charts/heat-map-charts.md)
- [Tag cloud charts](/explore-analyze/visualize/charts/tag-cloud-charts.md)
- [Region map charts](/explore-analyze/visualize/charts/region-map-charts.md)

## Add annotations [add-annotations]

Annotations highlight specific points or ranges on a chart. For example, you can call attention to a deployment, an outage, or any event that may have affected your data.

Annotations appear as a layer in the Lens editor. They can be:

- **Point annotations**: mark a specific timestamp.
- **Range annotations**: mark a time interval.

Annotations can use a static timestamp you define, or reference events from an {{product.elasticsearch}} index.

For step-by-step instructions, refer to [Add annotations to visualizations](/explore-analyze/visualize/annotations.md).

## Add reference lines [add-reference-lines]

Reference lines mark a threshold, target, or baseline directly on a chart to give viewers immediate context without needing to scan a separate legend or tooltip.

A reference line can use:

- A **static value** you set manually.
- A **dynamic value** computed from the data in the chart, such as the average, maximum, or 95th percentile.

For step-by-step instructions, refer to [Add reference lines to visualizations](/explore-analyze/visualize/reference-lines.md).

## Formulas and functions [formulas]

Use the formula editor to combine multiple metrics, apply math operations, and compute derived values directly inside a Lens visualization.

For step-by-step instructions and examples, refer to [Formulas](/explore-analyze/visualize/lens-formulas.md).

## Frequently asked questions [lens-faq]

### How do I change how the data is displayed? [change-the-data]

With Lens, you make changes to the visualization by editing the dimensions, which are the components of the chart. The **Layer pane** shows the dimensions of a visualization and where they map to in the chart.

All dimension names that appear in the **Layer pane** correspond to a chart component. The number of dimensions and their names differ between visualization types.

For example, bar chart dimensions are **Vertical axis**, **Horizontal axis**, and **Break down by**, while metric chart dimensions are **Primary metric**, **Secondary metric**, **Maximum value**, and **Breakdown by**.

For detailed information about what each dimension does and when to use it, refer to the relevant chart type documentation.

### How do I add more splits or breakdowns? [add-a-split]

To add more splits or breakdowns, click **Add or drag-and-drop a field** in the **Break down by** dimension. Multiple breakdowns display as a small multiple chart.

### How do I change the aggregation type? [change-the-aggregation-type]

To change the aggregation type, use the dimension editor. To open the dimension editor, click the dimension badge in the **Layer pane**.

### How do I add formulas or math? [add-a-formula]

To add formulas or math operations to a Lens visualization, click on an existing metric in the **Layer pane**, then select **Formula** from the function list. Enter your formula in the formula editor. Refer to [Formulas](/explore-analyze/visualize/lens-formulas.md) for more details.

### How do I format numbers in tooltips and axes? [change-the-number-format]

To change number formatting, click on the metric dimension to open the dimension editor, then expand **Display options** and open the **Value format** menu.

### How do I add color? [color-mapping]

To add color to your visualization:

- In the **Layer pane**, click the dimension you want to color.
- Expand the **Color** section in the dimension editor, then choose how you want to apply color: by **Value**, **Gradient**, or **Fixed value**.

### How do I change the color of a single bar or line? [change-the-color-of-a-bar-or-line]

To change the color of a single bar or line, open the dimension editor for the metric, expand **Color**, and select **Fixed value**. Choose a color from the palette.

### How do I zoom into a time range on a chart? [zoom-in]

To zoom into a time range on a chart, drag to select the range directly on the chart. This updates the time picker. To zoom back out, click **Reset zoom** or use the time picker.

### How do I visualize a mix of index patterns? [visualization-mix-index-patterns]

To visualize a mix of index patterns, use the **Add layer** option and select a different data source for each layer.

### How do I compare two time periods? [how-do-i-compare-two-time-periods]

To compare two time periods in a Lens chart, click **Add layer** and select **Add a new visualization layer**. In the second layer, choose **Date histogram** for the time dimension and set the **Time shift** option to the period you want to compare. For example, set **Time shift** to **1 week ago** to compare the current period against the previous week.

### How do I change the formatting of a date? [how-do-i-change-the-formatting-of-a-date]

To change the formatting of a date, click on the date dimension in the **Layer pane** to open the dimension editor. Expand **Display options** and open the **Value format** menu to select a date format.

### How do I calculate the percentage of a total? [percentage-of-total]

To calculate a percentage of the total, use the formula editor. Select or create a metric dimension, then click **Formula** and enter an expression such as `count() / overall_sum(count()) * 100`.

### Why is my field not visible? [field-is-not-visible]

If a field does not appear in the field list, it is likely one of the following:

- The field type is not supported by Lens.
- The field is not mapped in your data view.
- The field has no data in the selected time range.

Try expanding the time range or checking the data view to confirm the field is indexed.

### Why is my field greyed out? [field-is-greyed-out]

A greyed-out field means it is not compatible with the current visualization type or the aggregation function you have selected. Switch to a compatible visualization type or change the aggregation function to enable the field.

### How do I make date histogram bars fill the entire time range? [date-histogram-bars-fill-the-entire-time-range]

To make date histogram bars fill the entire time range, add a date histogram field to the **Horizontal axis** dimension and set the granularity to **Auto**. Bars fill the available range based on the data and the interval.

### How do I change the starting value of a range? [change-the-starting-value-of-a-range]

To change the starting value of a range, open the dimension editor for the **Intervals** dimension and set a custom minimum value in the **Range start** field.

### How do I filter the data for a single layer? [filter-the-data-for-a-single-layer]

To apply a filter to a single layer without affecting other layers or the dashboard, open the **Layer options** menu and select **Add layer filter**. Define the filter in the KQL or Lucene editor that appears.

### How do I apply a reduction function to a date histogram? [apply-a-reduction]

To apply a reduction function such as **Sum**, **Average**, or **Max** to a date histogram, use the formula editor and wrap the aggregation in an **Overall** function. For example, `overall_sum(sum(bytes))` sums all values across the entire time range instead of showing them per interval.

### Why are my results different from Discover? [why-are-my-results-different-from-discover]

Differences between Lens and Discover results occur because Lens applies aggregations to summarize data, while Discover shows individual documents. For example, a **Count** metric in Lens may differ from the document count shown in Discover if filters or data view settings differ between the two views.

### How do I add a threshold line? [add-threshold]

To add a threshold line to a chart, add a **Reference line** layer and set it to a static or dynamic value. Refer to [Add reference lines to visualizations](/explore-analyze/visualize/reference-lines.md).

### How do I sort my data? [sort-the-data]

To sort data in a Lens visualization, click on the dimension you want to sort by in the **Layer pane**, then expand **Display options** and choose the sort direction.

For tables, click the column header to sort by that column in the rendered table.

### What limitations exist for tables? [limitations-for-tables]

Tables created in Lens have the following limitations:

- You can add at most 10 metrics and 10 dimensions.
- Sorting is limited to one column at a time.
- Table pagination is not available inside the Lens editor; it becomes available after you add the table to a dashboard.

### Why can't I add more columns or breakdowns? [why-cant-I-add-more-columns-or-breakdowns]

Each visualization type in Lens has a fixed set of dimensions. Once you fill all available dimension slots, the **Add** option becomes unavailable. To add more breakdowns or columns, either remove an existing dimension or switch to a visualization type that supports more dimensions.

### What does 'Missing values' mean? [missing-values]

**Missing values** appear in charts when data exists for some time intervals or category buckets but not others. By default, Lens shows gaps where no data is present. To change this behavior, open the **Layer options** menu and set the **Missing values** option to **Zero** or **Linear interpolation**, depending on the chart type.

### How do I share or export a visualization? [share-or-export-a-visualization]

To share or export a Lens visualization:

- If the visualization is on a dashboard, use the dashboard sharing options.
- If the visualization is in the Visualize library, open it and use the **Share** menu in the top navigation bar.

For more details, refer to [Reporting and sharing](/explore-analyze/report-and-share.md).

### How do I add an axis title? [add-an-axis-title]

To add or edit an axis title in Lens, click the **Style** icon {icon}`brush` in the **Layer pane** to open the style panel. Look for the **Axis titles** section and toggle or edit the axis label text.

### How do I use the time shift option? [time-shift]

The **Time shift** option offsets a metric backward in time, letting you compare the current period against a previous one in the same chart. To use it, click on the metric dimension in the **Layer pane**, then expand **Advanced options** and set the **Time shift** value. For example, entering **7d** shows the metric as it was seven days ago.

### How do I display long labels? [display-long-labels]

For long axis labels, Lens automatically truncates text that exceeds the available display area. To see the full label, hover over a truncated label to reveal the tooltip with the complete text.

### How do I visualize multiple metrics with different scales on the same chart? [multiple-metrics-different-scales]

To visualize multiple metrics with different scales on the same chart, use **Multiple chart layers** and assign each metric to a separate y-axis. Click **Add layer**, then configure the metric for that layer. To move a metric to a secondary axis, open its dimension editor and change the **Axis side** setting from **Left** to **Right**.

### How do I change the axis scale? [axis-scale]

To change the axis scale in Lens, open the **Style** panel by clicking the **Style** icon {icon}`brush` in the **Layer pane** and look for the **Axis scale** option. You can switch between **Linear** and **Log** scales for the y-axis.

### How do I show only the top N results? [how-do-i-show-only-the-top-n-results]

To show only the top N results in a visualization, click the dimension that you want to limit in the **Layer pane**. In the dimension editor, change the aggregation to **Top values** and set the **Number of values** to the count you need.

### How do I test my visualization formula? [how-do-i-test-my-visualization-formula]

To test a formula, open the formula editor by clicking **Formula** in the dimension editor. Lens validates the formula in real time and shows an inline error if the syntax is invalid. Review the formula preview at the bottom of the editor to confirm the computed values look correct.

### How do I create a ratio or rate? [create-a-ratio-or-rate]

To create a ratio or rate in Lens, use the formula editor. Click a metric dimension, select **Formula**, and divide one aggregation by another. For example, to compute the error rate, enter `count(kql='status:error') / count()`. Multiply by 100 to express the result as a percentage.

### How do I create a rolling average? [create-a-rolling-average]

To create a rolling average, use the formula editor and wrap a metric in the **Moving average** function. For example, `moving_average(sum(bytes), window=7)` computes the seven-period rolling average of the sum of bytes. You can adjust the window size to control how many periods are included in each average.
