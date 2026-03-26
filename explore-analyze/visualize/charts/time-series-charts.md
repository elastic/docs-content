---
navigation_title: Time series charts
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Instructions and best practices for building time series charts with Kibana Lens in Elastic.
---

# Build time series charts with {{kib}}

Time series charts help you track how metrics change over time so you can spot trends, seasonality, and anomalies. In Lens, time series visualizations are typically built with **Line**, **Area**, or **Bar** charts, depending on whether you want to emphasize precise trend lines, cumulative volume, or period-over-period comparison.

You can create time series charts in {{kib}} using [**Lens**](../lens.md).

![Example Lens line chart](/explore-analyze/images/kibana-line-new.png)

## Build a time series chart

:::{include} ../../_snippets/lens-prerequisites.md
:::

To build a time series chart:

:::::::{stepper}

::::::{step} Access Lens
**Lens** is {{kib}}'s main visualization editor. You can access it:
- From a dashboard: On the **Dashboards** page, open or create the dashboard where you want to add a time series chart, then add a new visualization.
- From the **Visualize library** page by creating a new visualization.
::::::

::::::{step} Set the visualization type
New visualizations often start as **Bar** charts.

Using the **Visualization type** dropdown, select **Line**, **Area**, or **Bar**.
::::::

::::::{step} Define the data to show
1. Select the {{data-source}} that contains your data.
2. Configure the [**Horizontal axis**](#horizontal-axis-settings) with a date field using **Date histogram**.
3. Configure the [**Vertical axis**](#vertical-axis-settings) with the metric you want to track over time.

Optionally:
   - Configure [**Breakdown**](#breakdown-settings) to split the chart into series (for example, by host, service, region, or status).
   - Add a second metric or duplicate a layer with a [time shift](../lens.md#compare-data-with-time-offsets) to compare current versus previous periods.

The chart preview updates to show one or more time-based series.
::::::

::::::{step} Customize the chart to follow best practices
Tweak the appearance of your chart to improve interpretation. Consider the following best practices:

**Use an interval that matches the question**
:   Use shorter intervals for incident analysis and longer intervals for strategic trend reporting.

**Compare like with like**
:   Keep consistent units and aggregation logic when comparing series or periods.

**Handle sparse data explicitly**
:   If your data has gaps, choose an appropriate missing-values behavior so the chart doesn't imply false continuity.

**Keep legends informative but concise**
:   Use clear series names and only add statistics that support the decision being made.

Refer to [Time series chart settings](#time-series-chart-settings) for all configuration options relevant to time series charts.
::::::

::::::{step} Save the chart
- If you accessed Lens from a dashboard, select **Save and return** to save the visualization and add it to that dashboard, or select **Save to library** to add the visualization to the Visualize library and reuse it later.
- If you accessed Lens from the Visualize library, select **Save**. A menu opens and lets you add the visualization to a dashboard and to the Visualize library.
::::::

:::::::

## Time series chart settings [time-series-chart-settings]

Use these settings to control how data is bucketed over time and how each series is displayed.

### Horizontal axis settings [horizontal-axis-settings]

The horizontal axis defines your timeline.

**Data**
:   - **Date histogram**: Buckets documents into regular time intervals.
      - **Field**: Select the date field to use as the timeline.
      :::{include} ../../_snippets/lens-histogram-settings.md
      :::
    - **Filters**: Create fixed comparison series (for example, production vs staging) on the same timeline.

**Appearance**
:   - **Name**: Set a clear axis label that describes the time context.

### Vertical axis settings [vertical-axis-settings]

The vertical axis defines the value tracked over time.

**Data**
:   Use aggregation functions like `Average`, `Sum`, `Count`, `Max`, `Percentile`, and `Counter rate`, or build custom calculations with [formulas](../lens.md#lens-formulas).

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
:   - **Name**: Use descriptive metric names in legends and tooltips.
    - **Value format**: Match the unit to the data (for example, percent, bytes, duration, currency).
    - **Series color**: Keep colors consistent for repeat dashboards.

### Breakdown settings [breakdown-settings]

Breakdown lets you split a metric into multiple series over the same timeline.

**Data**
:   - **Top values**: Split by the most common values of a field.
      - **Field**: Select the categorical field to split by.
      - **Number of values**: Limit to the top categories to preserve readability.
      :::{include} ../../_snippets/lens-rank-by-options.md
      :::
      :::{include} ../../_snippets/lens-breakdown-advanced-settings.md
      :::
    - **Filters**: Create manually defined series with KQL.

**Appearance**
:   - **Name**: Set readable series labels.
    - **Color mapping**: Use stable mappings so a category keeps the same color across charts.

### General layout

Use chart-level options to control readability.

#### Style settings

- For **Line** and **Area** charts, configure interpolation, missing-values behavior, and point visibility.
- For **Area** charts, tune fill opacity to keep overlapping series readable.
- For **Bar** charts, choose orientation and spacing that match your labels and panel size.

#### Legend settings

- **Visibility**: Auto, show, or hide.
- **Position** and **Width**: Balance chart area with scanability.
- **Label truncation**: Limit wrapping for long labels.
- **Statistics**: For time series charts, you can add values like **Average**, **Min**, **Max**, **Last value**, and **Difference**.

## Time series chart examples

**Traffic trend with previous-week comparison**
:   Compare this week to last week to detect regressions quickly:

    * Example based on: {{kib}} Sample Data Logs
    * **Visualization type**: Line
    * **Horizontal axis**: `@timestamp` with `Date histogram`
    * **Vertical axis**: `Count`
    * **Breakdown**: `response.keyword` (Top values: 5)
    * **Comparison**: Duplicate the layer and set **Time shift** to `1w`

![Time series line chart with period comparison](/explore-analyze/images/kibana-line-current-previous.png "=70%")

**Hourly revenue with anomaly threshold**
:   Monitor revenue changes and highlight a warning threshold:

    * Example based on: {{kib}} Sample Data eCommerce
    * **Visualization type**: Area
    * **Horizontal axis**: `order_date` with `Date histogram` (hourly)
    * **Vertical axis**: `Sum(taxful_total_price)`
    * **Reference line**: Static threshold for expected minimum revenue

![Time series chart with reference lines](/explore-analyze/images/kibana-line-reference-lines.png "=70%")
