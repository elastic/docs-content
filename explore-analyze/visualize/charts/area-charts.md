---
navigation_title: Area charts
applies_to:
  stack: ga
  serverless: ga
description: Instructions and best practices for building area charts with Kibana Lens in Elastic.
---

# Build area charts with {{kib}}

Area charts are line charts with the area below the line filled in with a certain color or texture. Area charts work with numeric metrics over the horizontal axis (typically time) and are ideal to display quantitative values over an interval or time period, to show trends for time series like traffic, CPU, revenue, or error rates.

You can create area charts in {{kib}} using [**Lens**](../lens.md).

![Example Lens area chart](../../images/kibana-area-chart.png)

## Build an area chart

To build an area chart:

::::::{stepper}

:::::{step} Access Lens
**Lens** is {{kib}}'s main visualization editor. You can access it:
- From a dashboard: On the **Dashboards** page, open or create the dashboard where you want to add an area chart, then add a new visualization.
- From the **Visualize library** page by creating a new visualization.
:::::

:::::{step} Set the visualization to Area
New visualizations often start as **Bar** charts.

Using the **Visualization type** dropdown, select **Area**.
:::::

:::::{step} Define the data to show
1. Select the {{data-source}} that contains your data.

2. Drag a time-based field to the **Horizontal axis** and numeric field to the **Vertical axis**. You can use aggregation functions like `Date histograms` and `Filters`, or create custom calculations with [formulas](../lens.md#lens-formulas).

Optionally, you can add more numeric fields to create additional series, or drag a categorical field to **Break down** to split the series.
:::::

:::::{step} Customize the chart to follow best practices
Tweak the appearance of the chart to your needs. Consider the following best practices:

**Choose the right stack mode**
:   Use **Stacked** to show contribution to a whole, **Percentage** for normalized share, or **Unstacked** when absolute trends matter more than composition.

**Handle gaps and noise**
:   For sparse data, configure **Missing values** and **Line interpolation** to avoid misleading gaps or sharp edges. See [Visualization appearance options](../lens.md#customize-visualization-appearance).

**Use color purposefully**
:   Apply colors to highlight important data or patterns. Avoid using too many colors that might distract from the data. You can also assign [consistent colors to key categories](../lens.md#assign-colors-to-terms).

**Label clearly**
:   Provide a descriptive title and axis labels so users can interpret trends quickly.

Refer to [Area chart settings](#settings) to find all configuration options for your area chart.
:::::

:::::{step} Save the chart
- If you accessed Lens from a dashboard, select **Save and return** to save the visualization and add it to that dashboard, or select **Save to library** to add the visualization to the Visualize library and reuse it later.
- If you accessed Lens from the Visualize library, select **Save**. A menu opens and offers you to add the visualization to a dashboard and to the Visualize library.
:::::

::::::

## Advanced area scenarios

### Show composition with stacked and 100% stacked areas [area-stacking]

Use stacking to show how categories contribute to a total over time.

1. Create an **Area** visualization with a time-based **Horizontal axis**.
2. Break down the series by a categorical field, for example, `agent.keyword`, `response.keyword`.
   You can set the area chart stack mode to:
   - **Stacked** — Show cumulative totals and category contributions.

     ![Example Lens area chart stacked mode](../../images/kibana-area-stacked.png)

   - **Percentage (100%)** — Normalizes each timestamp to 100% to emphasize shares rather than magnitudes.

     ![Example Lens area chart percentage mode](../../images/kibana-area-percentage.png)

4. Optionally set **Rank by** for the breakdown dimension to control stacking order.

### Compare current vs previous period with time shift [area-timeshift]

Overlay a shifted series to compare different periods.

1. Create an **Area** visualization with a time-based **X-axis** and your main metric on **Y-axis** (for example, `sum(bytes)` or `average(transaction.duration.us)`).
2. Duplicate the series (Actions menu > **Duplicate**), or add a new series with the same metric.
3. In the duplicated series, open **Advanced** and set **Time shift** to a value like `1w`, `1d`, or `1M`. See [Compare differences over time](../lens.md#compare-data-with-time-offsets).
4. Use a distinct color and set **Stacking** to **None** so lines overlay rather than stack.

## Area chart settings [settings]

Customize your area chart to match the information you need and how you want it displayed.

### Horizontal axis settings [horizontal-axis-settings]

**Data**
:   **Functions**: Allow you to group your data. For example, you can use `Date histogram` to group data points into time-based buckets, or `Filters` to divide values into predefined subsets.
:   **Fields**: Determine which field from your data will be used for the horizontal axis.
:   **Minimum interval**: Determine the smallest time bucket that your data will be grouped into (for example, seconds, minutes, hours, days).

**Appearance**
:   **Name**: By default, the chart uses the function or formula as title. It's a best practice to customize this with a meaningful title.

### Vertical axis settings [vertical-axis-settings]

**Data**
:   To represent the metrics or values you want to visualize, you can use quick functions like `Average`, `Count`, `Percentile`, `Counter rate`, or create custom calculations with formulas. Refer to [](/explore-analyze/visualize/lens.md#lens-formulas) for examples, or to the {icon}`documentation` **Formula reference** available from Lens.

    :::{include} ../../_snippets/area-vertical-axis-advanced-settings.md
    :::

**Appearance**
:   Configure series-level options, including:
   - **Name**: Customize the series label.
   - **Value format**: Control how numeric values are displayed on your vertical axis and in tooltips.
   - **Series color**: Determine the color of your data series in the visualization.
   - **Axis side**: Determine which side of the chart the vertical axis appears on.

### Breakdown settings [breakdown-settings]

You can optionally split your series by a categorical field to create multiple stacked or overlapping areas. 

## Area chart examples

The following examples show practical configurations for common time series questions.

**Website traffic with YoY comparison**
::   Visualize weekly page views and compare to last year:
   - **Title**: "Weekly page views (YoY)"
   - **X-axis**: `@timestamp` (Date histogram, weekly)
   - **Y-axis**: `count()`
   - Add a second series: `count(shift='1y')`
   - Set **Stacking** to **None** for both series
   - Set distinct colors; optionally choose **Smooth** interpolation
   - Use legend statistics like **Max**, **Average**, and **Last value** for quick insights

**CPU utilization by service (stacked)**
::   Show how services contribute to overall CPU:
   - **Title**: "CPU utilization by service"
   - **X-axis**: `@timestamp` (Date histogram)
   - **Y-axis**: `average(system.cpu.total.pct)`; set **Value format** to `Percent`
   - **Break down by**: `service.name`
   - **Stacking**: **Stacked** or **Percentage (100%)** to show shares
   - Configure **Missing values** to **Linear** to avoid visual gaps; consider **Smooth** lines

**Error rate over time, stacked by outcome**
::   Monitor error rate composition:
   - **Title**: "Error rate by outcome"
   - **X-axis**: `@timestamp` (Date histogram)
   - **Primary series (formula)**:
     ```
     count(kql='event.dataset : \"apm*\" and event.outcome : failure') /
     count(kql='event.dataset : \"apm*\"')
     ```
     Set **Value format** to `Percent`
   - **Break down by**: `service.name` (to see which services contribute to failures)
   - **Stacking**: **None** for pure error rate trend, or **Stacked** when breaking down the numerator by `event.outcome` (success/failure) for composition
   - Add a **Reference line** at `0.05` (5%) as target/SLO

**95th percentile latency by service (overlapping series)**
::   Compare high-percentile latency across services:
   - **Title**: "p95 latency by service"
   - **X-axis**: `@timestamp`
   - Add one series per service (or use a breakdown on `service.name` with top N):
     - **Y-axis**: `percentile(transaction.duration.us, percentile=95)`
   - **Stacking**: **None** (overlapping, not additive)
   - Use **Legend** to show **Max**, **Median**, and **Last value**

**Revenue vs forecast with cumulative totals**
::   Track performance against plan:
   - **Title**: "Revenue vs forecast (MTD)"
   - **X-axis**: `@timestamp` (Date histogram, daily)
   - **Actuals series**:
     ```
     cumulative_sum(sum(sales.revenue))
     ```
   - **Forecast series**:
     ```
     cumulative_sum(sum(sales.revenue_forecast))
     ```
   - **Stacking**: **None**
   - Consider **Step** interpolation for clarity and add **Annotations** for major promotions or releases

**Inbound network rate (moving average)**
::   Smooth short-term spikes:
   - **Title**: "Inbound network rate (5m MA)"
   - **X-axis**: `@timestamp`
   - **Y-axis (formula)**:
     ```
     moving_average(rate(sum(system.network.in.bytes))), window=5
     ```
   - Set **Value format** to `Bytes`
   - **Stacking**: **None**


