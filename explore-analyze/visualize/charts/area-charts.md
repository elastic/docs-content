---
navigation_title: Area charts
applies_to:
  stack: ga
  serverless: ga
description: Instructions and best practices for building area charts with Kibana Lens in Elastic.
---

# Build area charts with {{kib}}

Area charts are line charts with the area below the line filled in with a certain colour or texture. Area charts work with numeric metrics over the horizontal axis (typically time) and are ideal to display quantitative values over an interval or time period, to show trends for time series like traffic, CPU, revenue, or error rates.

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

1. Create an **Area** visualization with a time-based **X-axis**.
2. Break down the series by a categorical field (for example, `event.outcome`, `response.status_code`, or `service.name`).
3. In the series appearance options, set **Stacking** to:
   - **Stacked** — Shows cumulative totals and category contributions.
   - **Percentage (100%)** — Normalizes each timestamp to 100% to emphasize shares rather than magnitudes.
4. Optionally set **Order by** for the breakdown dimension to control stacking order.

### Compare current vs previous period with time shift [area-timeshift]
Overlay a shifted series to compare different periods.

1. Create an **Area** visualization with a time-based **X-axis** and your main metric on **Y-axis** (for example, `sum(bytes)` or `average(transaction.duration.us)`).
2. Duplicate the series (Actions menu > **Duplicate**), or add a new series with the same metric.
3. In the duplicated series, open **Advanced** and set **Time shift** to a value like `1w`, `1d`, or `1M`. See [Compare differences over time](../lens.md#compare-data-with-time-offsets).
4. Use a distinct color and set **Stacking** to **None** so lines overlay rather than stack.

### Smooth curves and handle missing values [area-missing-values]
Configure how lines connect and how gaps are displayed to avoid misleading visuals.

1. In the editor toolbar, open **Appearance**.
2. Choose **Line interpolation**: **Straight** (default), **Smooth**, or **Step**.
3. Configure **Missing values** to **Hide**, **Zero**, **Linear**, **Last**, or **Next**. See [Visualization appearance options](../lens.md#customize-visualization-appearance).
4. Optionally enable **Show as dotted line** when filling gaps to distinguish inferred segments.

### Create rolling metrics (moving average, cumulative sum) [area-rolling-metrics]
Derive smoother or aggregated trends with formulas.

- Moving average of a metric:
  ```
  moving_average(average(system.cpu.total.pct), window=5)
  ```
- Cumulative sum for a running total:
  ```
  cumulative_sum(sum(orders.count))
  ```

Add these as additional series or replace the base metric. Remember to set **Value format** appropriately (for example, `Percent`).

### Highlight targets with reference lines and annotations [area-reference-annotations]
Add context with thresholds and events.

1. Add **Reference lines** for thresholds (for example, p75 latency SLO): see [Add reference lines](../lens.md#add-reference-lines).
2. Add **Annotations** to mark deployments, incidents, or business events: see [Add annotations](../lens.md#add-annotations).

## Area chart settings [settings]

Customize your area chart to match the information you need and how you want it displayed.

### Y-axis metric [y-axis-options]

**Value**
::   The numeric aggregation or formula plotted as the filled line. Common choices include `Sum`, `Average`, `Percentile`, `Count`, `Rate`, or a **Formula** combining multiple aggregations. See [Use formulas to perform math](../lens.md#lens-formulas).

**Appearance**
::   Configure series-level options, including:
   - **Name**: Customize the series label.
   - **Color by value**: Apply static or dynamic coloring. When using breakdowns, consider [Assign colors to terms](../lens.md#assign-colors-to-terms).
   - **Stacking**: Choose **None**, **Stacked**, or **Percentage (100%)**.
   - **Line interpolation**: **Straight**, **Smooth**, or **Step**.
   - **Missing values**: **Hide**, **Zero**, **Linear**, **Last**, **Next**. See [Visualization appearance options](../lens.md#customize-visualization-appearance).
   - **Area opacity**: Set the fill transparency to balance readability across overlapping series.

### X-axis settings [x-axis-options]

**Data**
::   The horizontal axis, commonly a **Date histogram** over `@timestamp`. You can change the time interval or normalize by unit when needed. See [Frequently asked questions](../lens.md#lens-faq).

**Appearance**
::   Configure axis title, bounds, tick labels, and orientation in the toolbar. See [Customize the visualization display](../lens.md#configure-the-visualization-components).

### Breakdown settings [breakdown-options]

**Data**
::   Split your series by a categorical field to create multiple stacked or overlapping areas (for example, per service, status code, or region). You can optionally specify:
   - **Number of values**: Limit the number of categories shown; extra categories can be grouped as **Other**.
   - **Order by** and **Direction**: Control ranking and display order.
   - **Collapse by**: Aggregate values across categories when needed.

   :::{include} ../../_snippets/lens-breakdown-advanced-settings.md
   :::

**Appearance**
::   Define legend behavior and label truncation. See [Customize the visualization legend](../lens.md#customize-visualization-legend).

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


