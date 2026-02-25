---
navigation_title: Time series charts
applies_to:
  stack: ga
  serverless: ga
description: Instructions and best practices for building time series charts with Kibana Lens in Elastic.
---

# Build time series charts with {{kib}}

Time series charts are essential for visualizing how data changes over time. They are ideal for tracking metrics, identifying trends, and spotting anomalies in your data. With time series charts, you can monitor application performance, track business KPIs, analyze sensor data, and much more.

You can create time series charts in {{kib}} using [**Lens**](../lens.md).

![A line chart showing a metric over time](../../images/kibana-lens_lineChartMetricOverTime_8.4.0.png)

## Build a time series chart

To build a time series chart:

:::::{stepper}

::::{step} Access Lens
**Lens** is {{kib}}'s main visualization editor. You can access it:
- From a dashboard: On the **Dashboards** page, open or create the dashboard where you want to add a time series chart, then add a new visualization.
- From the **Visualize library** page by creating a new visualization.
::::

::::{step} Select a chart type
New visualizations default to creating **Bar** charts. Time series data can be effectively visualized using **Line**, **Area**, or **Bar** charts. 

Using the dropdown indicating **Bar**, select **Line**.
::::

::::{step} Define the data to show
1. Select the {{data-source}} that contains your data.
2. Define the **Horizontal axis** by dragging a time field (like `@timestamp`) to the chart. This will represent the time component of your visualization.
3. Define the **Vertical axis** by dragging a numeric field or using a count to the chart. This will represent the metric you want to track over time.
4. Optionally:
    - Add more vertical axes to display multiple metrics on the same chart.
    - [Break down](#breakdown-options) the series into multiple lines based on a categorical field.

Refer to [](#settings) to find all data configuration options for your time series chart.
::::

::::{step} Customize the chart to follow best practices
Tweak the appearance of the chart to your needs. Consider the following best practices:

**Label axes clearly**
:   Ensure your horizontal and vertical axes have descriptive labels.

**Use appropriate time intervals**
:   Choose a time interval for the horizontal axis that makes sense for your data.

**Provide context**
:   Use titles and descriptions to explain what the chart shows.

Refer to [](#settings) for a complete list of options.
::::

::::{step} Save the chart
- If you accessed Lens from a dashboard, select **Save and return** to save the visualization and add it to that dashboard, or select **Save to library** to add the visualization to the Visualize library and be able to add it to other dashboards later.
- If you accessed Lens from the Visualize library, select **Save**. A menu opens and offers you to add the visualization to a dashboard and to the Visualize library.
::::

:::::

## Time series chart settings [settings]

Customize your time series chart to display exactly the information you need, formatted the way you want.

### Horizontal axis settings [horizontal-axis-options]

**Value**
:   The time field for the horizontal axis. This is typically a field with a `date` type, like `@timestamp`. You can adjust the time interval (e.g., per second, minute, hour, day).

### Vertical axis settings [vertical-axis-options]

**Value**
:   The numeric value for the vertical axis. When you drag a field onto the chart, {{kib}} suggests a function based on the field type. You can change it and use aggregation functions like `Sum`, `Average`, `Count`, `Median`, and more, or create custom calculations with formulas. Refer to [](/explore-analyze/visualize/lens.md#lens-formulas) for examples, or to the {icon}`documentation` **Formula reference** available from Lens.

    You can add multiple vertical axes to display several metrics on the same chart.

### Breakdown settings [breakdown-options]

**Data**
:   Split your chart into multiple series based on a categorical field. Each unique value creates its own series (e.g., a separate line for each host or region). You can optionally specify the following options:

    - **Number of values**: The number of series to show.
    - **Rank by**: The dimension by which top values are ranked.

## Time series chart example

The following example shows how to build a time series chart to monitor website traffic.

**Website traffic over time**
:   Display the number of page views over time, broken down by browser type.

    * **Title**: "Website page views by browser"
    * **Horizontal axis**: `@timestamp` with an appropriate time interval.
    * **Vertical axis**: `count()` of records.
    * **Break down by**: `user_agent.browser.name`
      * **Number of values**: `5` (to show the top 5 browsers)

    ![A time series chart showing website traffic over time, broken down by browser.](../../images/kibana-lens_lineChartMultipleDataSeries_7.16.png)

