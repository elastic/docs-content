---
navigation_title: Waffle charts
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Instructions and best practices for building waffle charts with Kibana Lens in Elastic.
---

# Build waffle charts with {{kib}}

Waffle charts display data as a 10x10 grid of small squares, where each square represents 1% of the whole. They are ideal for showing percentages, visualizing survey results, and making proportions intuitive by representing data as discrete units. They work best with fewer than 10 categories.

Like [pie charts](pie-charts.md), waffle charts show part-to-whole relationships. However, waffle charts make it easier to compare similarly-sized proportions (for example, 23% vs. 27%) because areas in a grid are easier to distinguish than angles in a circle. Choose a pie chart when you have a small number of slices (2-4) with clearly different sizes, or when you want to use a donut layout.

You can create waffle charts in {{kib}} using [**Lens**](../lens.md).

![Example Lens waffle charts showing response status breakdown and OS distribution](/explore-analyze/images/waffle-chart-example.png)

## Build a waffle chart

:::{include} ../../_snippets/lens-prerequisites.md
:::

To build a waffle chart:

::::::{stepper}

:::::{step} Access Lens
**Lens** is {{kib}}'s main visualization editor. You can access it:
- From a dashboard: On the **Dashboards** page, open or create the dashboard where you want to add a waffle chart, then add a new visualization.
- From the **Visualize library** page by creating a new visualization.
:::::

:::::{step} Set the visualization to Waffle
New visualizations often start as **Bar** charts.

Using the **Visualization type** dropdown, select **Waffle**.
:::::

:::::{step} Define the data to show
1. Select the {{data-source}} that contains your data.
2. Configure the [**Group by**](#group-by-settings) dimension to define the categories. Each category is displayed as a colored section of the waffle.
3. Configure the [**Metric**](#metric-settings) dimension to define the value for each category. This determines how many squares each category occupies.

Optionally:
   - Enable [**Multiple metrics**](#percentage-completion) in the layer settings to define each category as a separate metric.

The chart preview updates to show a grid of colored squares. Each color represents a category, and the number of squares reflects its proportion of the total.
:::::

:::::{step} Customize the chart to follow best practices
Tweak the appearance of the chart to your needs. Consider the following best practices:

**Limit categories**
:   Keep your waffle chart to a maximum of 6-8 categories. More categories make the chart difficult to read.

**Use intuitive colors**
:   Assign colors that have semantic meaning when possible (for example, green for success, red for errors). Use the [color mapping feature](../lens.md#assign-colors-to-terms) for consistent coloring.

**Order categories meaningfully**
:   Arrange categories from largest to smallest or in a natural order (such as satisfaction ratings from low to high).

Refer to [Waffle chart settings](#waffle-chart-settings) to find all configuration options for your waffle chart.
:::::

:::::{step} Save the chart
- If you accessed Lens from a dashboard, select **Save and return** to save the visualization and add it to that dashboard, or select **Save to library** to add the visualization to the Visualize library and reuse it later.
- If you accessed Lens from the Visualize library, select **Save**. A menu opens and lets you add the visualization to a dashboard and to the Visualize library.
:::::

::::::

## Advanced waffle chart scenarios

### Show percentage completion with multiple metrics [percentage-completion]

You can use **Multiple metrics** to show progress toward a goal, with filled squares for completed work and empty squares for remaining work.

#### Example: Revenue progress toward a sales target

This example uses the **Kibana Sample Data eCommerce** data set. If you haven't installed it yet, refer to [Sample data](/manage-data/ingest/sample-data.md) for instructions.

1. Create a **Waffle** chart using the **Kibana Sample Data eCommerce** {{data-source}}.
2. Open **Layer settings**:
   * {applies_to}`serverless: ga` {applies_to}`stack: ga 9.3` Select {icon}`app_management` **Layer settings**.
   * {applies_to}`stack: ga 9.0-9.2` Select {icon}`boxes_horizontal`, then select **Layer settings**.
3. Select **Multiple metrics**, then close the layer settings.
4. Add two metrics:
   - **Revenue earned**: Set to `Sum` of `taxful_total_price`. Name it "Revenue earned" and assign a green color.
   - **Remaining to goal**: Set to a [formula](/explore-analyze/visualize/lens.md#lens-formulas): `500000 - sum(taxful_total_price)`. Name it "Remaining to goal" and assign a gray color.
5. The chart shows how close revenue is to the $500,000 target. Each green square represents 1% of the goal achieved.

![Waffle chart showing revenue progress toward a sales target](/explore-analyze/images/waffle-scenario-completion.png "=70%")

## Waffle chart settings [waffle-chart-settings]

Customize your waffle chart to display exactly the information you need, formatted the way you want.

### Group by settings [group-by-settings]

The **Group by** dimension defines how the waffle is divided into colored sections. Waffle charts support a single **Group by** dimension.

**Data**
:   The **Group by** dimension supports the following functions:

    - **Top values**: Create sections for the most common values in a field.
      - **Field**: Select the field to group by. You can add up to 4 fields to create multi-term sections. When multiple fields are selected, each section represents a unique combination of values across those fields. You can reorder the fields by dragging them to change their priority.
      - **Number of values**: How many top values to display.
      :::{include} ../../_snippets/lens-rank-by-options.md
      :::
      - **Collapse by**: Aggregate values into a single number using `Sum`, `Average`, `Min`, or `Max`.
      :::{include} ../../_snippets/lens-breakdown-advanced-settings.md
      :::
    - **Date histogram**: Group data into time-based buckets.
      - **Field**: Select the date field to use for the time-based grouping.
      :::{include} ../../_snippets/lens-histogram-settings.md
      :::
      - **Collapse by**: Aggregate values into a single number using `Sum`, `Average`, `Min`, or `Max`.
    - **Intervals**: Create numeric ranges for continuous data.
      - **Field**: Select the numeric field to create intervals from.
      - **Include empty rows**: Include intervals with no matching documents.
      - **Collapse by**: Aggregate values into a single number using `Sum`, `Average`, `Min`, or `Max`.
    - **Filters**: Define custom KQL filters to create specific sections.
      - **Collapse by**: Aggregate values into a single number using `Sum`, `Average`, `Min`, or `Max`.

**Appearance**
:   - **Name**: Customize the legend label.
    - **Color mapping**: Select a color palette or assign specific colors to categories. Refer to [Assign colors to terms](../lens.md#assign-colors-to-terms) for details.

### Metric settings [metric-settings]

The **Metric** dimension defines the value for each category, determining how many squares each section occupies.

**Data**
:   The value that determines how many squares each category fills. When you drag a field onto the chart, {{kib}} suggests a function based on the field type. You can use aggregation functions like `Sum`, `Average`, `Count`, `Median`, and more, or create custom calculations with [formulas](/explore-analyze/visualize/lens.md#lens-formulas).

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
:   - **Name**: Customize the metric label displayed in tooltips and legends.
    - **Value format**: Control how numeric values are displayed (number, percent, bytes, and more).
    - **Series color**: When using multiple metrics without a **Group by** dimension, assign a specific color to each metric.

### General layout [appearance-options]

When creating or editing a visualization, you can customize the legend from the ![Legend icon](/explore-analyze/images/kibana-legend-icon.svg "") **Legend** menu.

:::{note}
Waffle charts do not have configurable style settings. The chart automatically displays labels and percentages on each section.
:::

#### Legend settings

**Visibility**
:   Specify whether to automatically show the legend or hide it:
    - **Auto**: Show the legend when there are multiple categories.
    - **Show**: Always show the legend (default).
    - **Hide**: Never show the legend.

**Width**
:   Control the width of the legend panel: **Small**, **Medium** (default), **Large**, or **Extra large**.

**Show value**
:   Toggle whether to display the numeric value alongside each legend entry. This is enabled by default.

**Label truncation**
:   Toggle whether to truncate long legend labels. When enabled, set the **Line limit** to control how many lines to display before truncating (1-5, default: 1).

## Waffle chart examples

The following examples show various configuration options for building impactful waffle charts.

**Response status breakdown**
:   Visualize the proportion of successful and failed HTTP requests at a glance:

    * Example based on: {{kib}} Sample Data Logs
    * **Group by**: Filters
      - "Success (2xx/3xx)": `response.keyword >= "200" AND response.keyword < "400"`
      - "Client errors (4xx)": `response.keyword >= "400" AND response.keyword < "500"`
      - "Server errors (5xx)": `response.keyword >= "500"`
    * **Metric**: Count
    * **Color mapping**: Green for success, yellow for client errors, red for server errors

![Waffle chart showing response status breakdown](/explore-analyze/images/waffle-example-response-status.png "=70%")

**OS distribution**
:   Show the distribution of operating systems used by your website visitors:

    * Example based on: {{kib}} Sample Data Logs
    * **Group by**: `machine.os.keyword` (Top 5 values)
    * **Metric**: Count

![Waffle chart showing OS distribution](/explore-analyze/images/waffle-example-os.png "=70%")