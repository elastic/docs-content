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

2. Drag a time-based field to the **Horizontal axis** and numeric field to the **Vertical axis**. Click the axes fields and check which functions Kibana suggests based on the field type. You can change it and use aggregation functions like Date histogram, Intervals, Filters, Top values, and more, or create custom calculations with formulas. Refer to [](/explore-analyze/visualize/lens.md#lens-formulas) for examples, or to the {icon}`documentation` **Formula reference** available from Lens.

3. Optionally, you can use the **Breakdown** settings to segment your data by a categorical field, creating multiple areas within the same chart. For example, to break down CPU usage by host, show request counts by service or endpoint, or visualize error rates by environment or region.
:::::

:::::{step} Customize the chart to follow best practices
Tweak the appearance of the chart to your needs. Consider the following best practices:

**Choose the right stack mode**
:   Use **Stacked** to show contribution to a whole, **Percentage** for normalized share, or **Unstacked** when absolute trends matter more than composition. For a practical use case, check how to [show composition with stacked and 100% stacked areas](#area-stacking).

**Handle gaps and noise**
:   For sparse data, configure **Missing values** and **Line interpolation** to avoid misleading gaps or sharp edges. Check the [Visualization appearance options](../lens.md#customize-visualization-appearance).

**Use color purposefully**
:   Apply colors to highlight important data or patterns. Avoid using too many colors that might distract from the data. You can also assign [consistent colors to key categories](../lens.md#assign-colors-to-terms).

**Label clearly**
:   Provide a descriptive title and axis labels that clearly communicate what the chart shows. For example, mention the metric being visualized ("Average Response Time") and reference the time period when relevant ("Dec 8-16, 2025").

Refer to [Area chart settings](#area-chart-settings) to find all configuration options for your area chart.  
:::::

:::::{step} Save the chart
- If you accessed Lens from a dashboard, select **Save and return** to save the visualization and add it to that dashboard, or select **Save to library** to add the visualization to the Visualize library and reuse it later.
- If you accessed Lens from the Visualize library, select **Save**. A menu opens and offers you to add the visualization to a dashboard and to the Visualize library.
:::::

::::::

## Advanced area scenarios

### Show composition with stacked and 100% stacked areas [area-stacking]

Use stacking to show how categories contribute to a total over time.

1. Create an area chart with a time-based **Horizontal axis**.
2. Break down the series by a categorical field, for example, `agent.keyword`, `response.keyword`.
   You can set the area chart stack mode to:
   - **Stacked** — Show cumulative totals and category contributions.

     ![Example Lens area chart stacked mode](../../images/kibana-area-stacked.png " =70%")

   - **Percentage (100%)** — Normalizes each timestamp to 100% to emphasize shares rather than magnitudes.

     ![Example Lens area chart percentage mode](../../images/kibana-area-percentage.png " =70%")

4. Optionally, in the **Beakdown** settings, you can set **Rank by** to specify the dimension the top values are ranked by.

### Compare current versus previous period with time shift [area-timeshift]

In Area charts, you can enable time shift to compare different periods and identify deltas.

![Example Lens area chart compare periods](../../images/kibana-area-compare-periods.png)

1. Create an area chart with a time-based **Horizontal axis** and your main metric on the **Vertical axis**, for example, `bytes`.
2. From the three-dot menu in the upper-left of the layer panel, select **Duplicate layer**.
3. From the duplicated layer, open the **Advanced** of the **Vertical axis** and set **Time shift** to `1w`. 
   Check also [Compare differences over time](../lens.md#compare-data-with-time-offsets) for more details.
4. Use a different color and set **Stacking** to **None** so areas overlay rather than stack.
5. Update the legend to show “Current” and “Previous”.

::::{tip}
You can also compute the relative change using a formula, for example:  
`(average(bytes) - average(bytes, shift='1w')) / average(bytes, shift='1w')`
:::: 

## Area chart settings [area-chart-settings]

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
:   To represent the metrics or values you want to visualize, you can use quick functions like Average, Count, Percentile, Counter rate, or create custom calculations with formulas. Refer to [](/explore-analyze/visualize/lens.md#lens-formulas) for examples.

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

**Traffic by geographic region**
:   Visualizing which geographic regions generate the most traffic:
   - **Horizontal axis**: `@timestamp` (Date histogram)
   - **Vertical axis**: `records`
   - **Breakdown**: `geo.dest`
   
   ![Example Lens area chart geographical regions](../../images/kibana-area-geo-regions.png " =70%")

**Response code over time with annotations**

:   Visualizing HTTP response codes over time, highlighting the proportion of success, client error, and server error responses, with annotations for key events: 

* **Horizontal axis**: `@timestamp` (Date histogram)
* **Vertical axis**: `Count of records`
  * **Breakdown**: 
    * **Success/Redirection**`response.keyword >= 200 and response.keyword < 400`
    * **Client Error**`response.keyword >= 400 and response.keyword < 500`
    * **Server Error**`response.keyword >= 500`
  * **Stacking**: `Percentage` to show the distribution relative to the total count at each point in time.
    * **Annotation Query**: `tags:error AND tags:security`

   ![Example Lens area chart response code annotations](../../images/kibana-response-code-annotations.png " =70%")






     


