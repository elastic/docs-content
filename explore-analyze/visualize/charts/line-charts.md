---
navigation_title: Line charts
applies_to:
  stack: ga
  serverless: ga
description: Instructions and best practices for building line charts with Kibana Lens in Elastic.
---

# Build line charts with {{kib}}

Line charts are ideal for visualizing how metrics evolve over time, spotting seasonal patterns, and detecting spikes or regressions at a glance. Use them for KPIs like response time, error rate, throughput, or utilization, and compare multiple series or previous periods on the same chart.

You can create line charts from any numeric data using aggregations (for example, `Average`, `Percentile`, `Counter rate`) or with custom [formulas](../lens.md#lens-formulas). Line charts usually show time on the x-axis, but they can also display data grouped by numbers or categories.

You can create line charts in {{kib}} using [**Lens**](../lens.md).

![Example Lens line chart](../../images/kibana-line.png)

## Build a line chart

To build a line chart:

::::::{stepper}

:::::{step} Access Lens
**Lens** is {{kib}}'s main visualization editor. You can access it:
- From a dashboard: On the **Dashboards** page, open or create the dashboard where you want to add a line chart, then add a new visualization.
- From the **Visualize library** page by creating a new visualization.
:::::

:::::{step} Set the visualization to Line
New visualizations default to **Bar**.

Using the visualization type dropdown, select **Line**.
:::::

:::::{step} Define the data to show
1. Select the {{data-source}} that contains your data.
2. Drag a time field (for example, `order_date`) to the **X-axis** to create a `Date histogram` (recommended for time series).

:::{note}
You might need to extend the time range and set the time filter to Last 30 days.
:::

3. Drag a numeric field (for example, `products_quantity`) to the **Y-axis**.

Optionally:
   - Add more numeric fields to create additional series, or drag a categorical field (for example, `geoip.city_name`) to **Break down by** to split the series.
   - Add a [reference line](../lens.md#add-reference-lines) to mark targets or SLOs.
:::::

:::::{step} Customize the chart to follow best practices
You can tweak the appearance of your chart by adjusting axes, legends, and series styles from the chart settings. Consider the following best practices:

**Use color wisely**
:   Assign colors that match your users' expectations and consider your specific context.

**Provide context**
:   Add descriptive axis titles and units to explain what the chart shows.

For layout, hierarchy, and color guidance on dashboards, check the EUI’s [Dashboard good practices](https://eui.elastic.co/docs/dataviz/dashboard-good-practices/). 
For more chart configuration options, go to the [Line chart settings](#settings) section.
:::::

:::::{step} Save the chart
- If you accessed Lens from a dashboard, select **Save and return** to save the visualization and add it to that dashboard, or select **Save to library** to add the visualization to the Visualize library.
- If you accessed Lens from the Visualize library, select **Save**. The Save menu lets you also add the visualization to a dashboard and to the Visualize library.
:::::

::::::

## Advanced line scenarios

### Compare with a previous period [line-previous-period]
Compare the current value with a prior time range using time shift to quickly see deltas.

1. Create a line series for the current value, for example: `average(response_time)`.
2. Add a second series with a time shift, for example: `average(response_time, shift='1w')`.
3. Use the legend labels to clarify “Current” versus “Previous (1w)”.

| Single series | With previous period |
|---|---|
| ![Metric over time](../../images/kibana-lens_lineChartMetricOverTime_8.4.0.png "title =70%") | ![Multiple series with previous period](../../images/kibana-lens_lineChartMultipleDataSeries_7.16.png "title =70%") |

::::{tip}
You can also compute the relative change as a separate series using a formula, for example:  
`(average(response_time) - average(response_time, shift='1w')) / average(response_time, shift='1w')`
:::: 

### Smooth noisy series with moving average [line-moving-average]
Noisy metrics (for example, per-minute throughput) can be smoothed:

1. Add a series such as `sum(bytes)`.
2. Add a second series using `moving_average(sum(bytes), window=5)`.
3. Keep both series visible (raw versus smoothed) or show only the smoothed one.

### Highlight thresholds with reference lines [line-reference-lines]
Use reference lines to indicate SLOs or alert thresholds.

1. In the chart settings, add a **Reference line** (for example, `200` ms or `0.95`).
2. Give it a label (for example, `Target` or `SLO`), choose a color, and optionally a band.

![Reference line](../../images/kibana-lens_referenceLine_7.16.png "title =70%")

### Handle gaps and missing data [line-fit-missing]
Irregular data or sparse sampling can create breaks. Use “fit missing values” to interpolate or extend:

1. Open the series settings.
2. Set **Missing values** to `Linear`, `Carry`, or `Zero`, depending on the use case.

![Fill gaps with linear fit](../../images/charts-gaps-fill-linear.png "title =70%")

### Choose the right axis and scale [line-axis]
For multi-metric charts, make sure the scale communicates intent:

- Use the **Left** axis for primary series, and enable a **Right** axis only when needed for different units.
- Use **log** scale for heavy-tailed distributions, or **percentage** mode for normalization.

| Left axis | Bottom axis |
|---|---|
| ![Left axis labeling](../../images/kibana-line-chart-left-axis-8.16.0.png "title =70%") | ![Bottom axis labeling](../../images/kibana-line-chart-bottom-axis-8.16.0.png "title =70%") |

## Line chart settings [settings]

Customize your line chart to display exactly the information you need, formatted the way you want.

### Y-axis series [y-axis-series]

**Value**
:   The metric to plot. When you drag a field onto the chart, {{kib}} suggests a function based on the field type. You can change it and use aggregation functions like `Average`, `Sum`, `Percentile`, `Counter rate`, or create custom calculations with formulas. Refer to [](/explore-analyze/visualize/lens.md#lens-formulas) for examples, or to the {icon}`documentation` **Formula reference** available from Lens.

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
:   Define the series style, including:
   - **Name**: Customize the legend label with a descriptive name.
   - **Series type**: Line or area variants, with optional stacking for area.
   - **Line/marker style**: Toggle lines, points, or both; adjust line width.
   - **Missing values**: Choose how to display gaps (Off, Linear, Carry, Zero).
   - **Color**: Select a palette or specific color per series.

### X-axis buckets [x-axis-buckets]

**Data**
:   Buckets define the x-axis. Commonly a `Date histogram` on `@timestamp`, but you can also use numeric histograms or terms (for small category counts).

**Appearance**
:   Axis title, tick density, and value formatting (for example, time format, numeric precision).

### Breakdown (split series) [breakdown-options]

**Data**
:   Split the chart into multiple series based on a categorical field. Each unique value creates its own series. You can optionally specify the following options:

   - **Number of values**: Limit to top N.
   - **Rank by**: Choose the ranking metric.
   - **Rank direction**: Ascending or descending.

   :::{include} ../../_snippets/lens-breakdown-advanced-settings.md
   :::

**Appearance**
:   Define how the series are displayed:
   - **Legend position**: Show legend and choose its placement.
   - **Color palette**: Ensure consistent colors across dashboards.

### Reference lines [reference-line-settings]
Add horizontal or vertical markers for targets, limits, or thresholds. Configure:
- **Value** (static or formula), **Label**, **Color**, and optional bands.

### General layout [appearance-options]
When creating or editing a visualization, open the {icon}`brush` panel to adjust:

- **Title and subtitle**: Add context like “Last 24 hours”.
- **Axes**: Set titles, units, scale (linear/log/percentage), and grid lines.
- **Legend**: Position and truncation.
- **Tooltip**: Synchronized tooltips are enabled by default across panels on dashboards.

## Line chart examples

**Website response time (p95) with target**
:   Monitor user experience and enforce SLO:

   * **Title**: "Response time (p95)"
   * **X-axis**: `Date histogram` on `@timestamp`
   * **Y-axis**: `percentile(response_time, percentile=95)`
     * **Format**: `Duration`
   * **Reference line**: `200` ms labeled `SLO`

   ![Response time with SLO reference line](../../images/kibana-lens_referenceLine_7.16.png "=70%")

**Requests throughput with moving average**
:   Smooth per-minute variation while preserving overall trend:

   * **Title**: "Requests per minute"
   * **X-axis**: `Date histogram`
   * **Y-axis (raw)**: `counter_rate(requests)`
   * **Y-axis (smoothed)**: `moving_average(counter_rate(requests), window=5)`
   * **Legend**: "Raw", "5-interval MA"

   ![Metric over time](../../images/kibana-lens_lineChartMetricOverTime_8.4.0.png "=70%")

**Error rate versus previous week**
:   Quickly assess regressions:

   * **Title**: "Error rate (now versus previous week)"
   * **X-axis**: `Date histogram`
   * **Series A**: `count(kql='response.code >= 500') / count()`
     * **Format**: `Percent`
   * **Series B**: `count(kql='response.code >= 500', shift='1w') / count(shift='1w')`
     * **Format**: `Percent`
   * **Legend**: "Current", "Previous (1w)"

   ![Multiple series comparison](../../images/kibana-lens_lineChartMultipleDataSeries_7.16.png "=70%")

**Throughput by top countries**
:   Break down by top N categories:

   * **Title**: "Requests per minute by country"
   * **X-axis**: `Date histogram`
   * **Y-axis**: `counter_rate(requests)`
   * **Break down by**: `geo.country`
     * **Number of values**: `10`
     * **Rank by**: `Custom` > `Count` > `Records`

   ![Multiple series by breakdown](../../images/kibana-lens_lineChartMultipleDataSeries_7.16.png "=70%")

---




