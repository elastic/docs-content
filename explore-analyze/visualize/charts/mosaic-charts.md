---
navigation_title: Mosaic charts
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Instructions and best practices for building mosaic charts with Kibana Lens in Elastic.
---

# Build mosaic charts with {{kib}}

Mosaic charts display the relationship between two categorical variables as a grid of rectangles, where both the width and height of each rectangle represent proportions of the data. They are ideal for visualizing how categories combine, showing conditional distributions, and exploring relationships between two dimensions. They work best with a moderate number of categories in each dimension (2-8 each).

You can create mosaic charts in {{kib}} using [**Lens**](../lens.md).

![Example Lens mosaic chart showing response status by operating system](/explore-analyze/images/mosaic-chart-example.png)

## Build a mosaic chart

:::{include} ../../_snippets/lens-prerequisites.md
:::

To build a mosaic chart:

::::::{stepper}

:::::{step} Access Lens
**Lens** is {{kib}}'s main visualization editor. You can access it:
- From a dashboard: On the **Dashboards** page, open or create the dashboard where you want to add a mosaic chart, then add a new visualization.
- From the **Visualize library** page by creating a new visualization.
:::::

:::::{step} Set the visualization to Mosaic
New visualizations often start as **Bar** charts.

Using the **Visualization type** dropdown, select **Mosaic**.
:::::

:::::{step} Define the data to show
1. Select the {{data-source}} that contains your data.
2. Configure the [**Horizontal axis**](#horizontal-axis-settings) dimension to define the columns. The width of each column represents the proportion of data in that category.
3. Configure the [**Vertical axis**](#vertical-axis-settings) dimension to define the rows within each column. The height of each rectangle represents the proportion within that column.
4. Configure the [**Metric**](#metric-settings) dimension to define the value used to calculate rectangle sizes. This defaults to **Count**.

The chart preview updates to show a grid of rectangles. Column widths represent the proportion of each horizontal category, and rectangle heights within each column show the distribution of vertical categories.
:::::

:::::{step} Customize the chart to follow best practices
Tweak the appearance of the chart to your needs. Consider the following best practices:

**Limit categories**
:   Keep both dimensions to a maximum of 6-8 categories each. More categories create tiny rectangles that are hard to read.

**Ensure balanced proportions**
:   Mosaic charts work best when categories have roughly comparable sizes. If one category dominates (for example, one host handling 90% of traffic), the other columns become too narrow to read. In that case, consider using a [bar chart](bar-charts.md) instead.

**Order categories meaningfully**
:   Arrange categories in a logical order (by size, alphabetically, or by a natural order) to make patterns easier to identify.

**Use color for the vertical dimension**
:   Colors typically represent the vertical axis categories, making it easier to track how each category appears across columns.

Refer to [Mosaic chart settings](#mosaic-chart-settings) to find all configuration options for your mosaic chart.
:::::

:::::{step} Save the chart
- If you accessed Lens from a dashboard, select **Save and return** to save the visualization and add it to that dashboard, or select **Save to library** to add the visualization to the Visualize library and reuse it later.
- If you accessed Lens from the Visualize library, select **Save**. A menu opens and lets you add the visualization to a dashboard and to the Visualize library.
:::::

::::::

## Mosaic chart settings [mosaic-chart-settings]

Customize your mosaic chart to display exactly the information you need, formatted the way you want.

### Horizontal axis settings [horizontal-axis-settings]

The **Horizontal axis** dimension defines the columns of the mosaic. Column widths represent the proportion of each category.

**Data**
:   The **Horizontal axis** dimension supports the following functions:

    - **Top values**: Create columns for the most common values in a field.
      - **Field**: Select the field to group by. You can add up to 4 fields to create multi-term columns. When multiple fields are selected, each column represents a unique combination of values across those fields. You can reorder the fields by dragging them to change their priority.
      - **Number of values**: How many categories to display.
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
    - **Filters**: Define custom KQL filters to create specific columns.
      - **Collapse by**: Aggregate values into a single number using `Sum`, `Average`, `Min`, or `Max`.

**Appearance**
:   - **Name**: Customize the axis label.
    - **Value format**: Control how numeric values are displayed (number, percent, bytes, and more).

### Vertical axis settings [vertical-axis-settings]

The **Vertical axis** dimension defines the rows within each column. Rectangle heights represent the proportion of each category within the column.

**Data**
:   The **Vertical axis** dimension supports the following functions:

    - **Top values**: Create rows for the most common values in a field.
      - **Field**: Select the field to group by. You can add up to 4 fields to create multi-term rows. When multiple fields are selected, each row represents a unique combination of values across those fields. You can reorder the fields by dragging them to change their priority.
      - **Number of values**: How many categories to display.
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
    - **Filters**: Define custom KQL filters to create specific rows.
      - **Collapse by**: Aggregate values into a single number using `Sum`, `Average`, `Min`, or `Max`.

**Appearance**
:   - **Name**: Customize the axis label.
    - **Color mapping**: Select a color palette or assign specific colors to categories. Refer to [Assign colors to terms](../lens.md#assign-colors-to-terms) for details.

### Metric settings [metric-settings]

The **Metric** dimension defines the value used to calculate rectangle sizes. In mosaic charts, this is typically **Count**.

**Data**
:   The value that determines rectangle proportions. You can use aggregation functions like `Count` or `Sum`, or create custom calculations with [formulas](/explore-analyze/visualize/lens.md#lens-formulas).

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
:   - **Name**: Customize the metric label displayed in tooltips and legends.
    - **Value format**: Control how numeric values are displayed (number, percent, bytes, and more).

    :::{note}
    Mosaic charts do not support multiple metrics. Each cell represents a single count or aggregated value.
    :::

### General layout [appearance-options]

When creating or editing a visualization, you can customize several appearance options from the {icon}`brush` **Style** or ![Legend icon](/explore-analyze/images/kibana-legend-icon.svg "") **Legend** menus.

#### Style settings

**Slice values**
:   Control what values appear on rectangles:
    - **Percentage**: Display the percentage of total (default).
    - **Integer**: Display the raw numeric value.
    - **Hide**: Do not display values.

    When displaying percentages, you can also configure the **Decimal places** (default: 2).

#### Legend settings

**Visibility**
:   Specify whether to automatically show the legend or hide it:
    - **Auto**: Show the legend when there are multiple categories.
    - **Show**: Always show the legend.
    - **Hide**: Never show the legend (default).

**Width**
:   Control the width of the legend panel: **Small**, **Medium** (default), **Large**, or **Extra large**.

**Nested**
:   When using both horizontal and vertical axes, enable this option to show the legend in a hierarchical format.

**Label truncation**
:   Toggle whether to truncate long legend labels. When enabled, set the **Line limit** to control how many lines to display before truncating (1-5, default: 1).

## Mosaic chart examples

The following examples show various configuration options for building impactful mosaic charts.

**Response status by operating system**
:   Visualize how response status categories vary across operating systems:

    * Example based on: {{kib}} Sample Data Logs
    * **Horizontal axis**: `machine.os.keyword` (Top 5 values)
    * **Vertical axis**: **Filters**
      - "Success (2xx/3xx)": `response.keyword >= "200" AND response.keyword < "400"`
      - "Client errors (4xx)": `response.keyword >= "400" AND response.keyword < "500"`
      - "Server errors (5xx)": `response.keyword >= "500"`
    * **Metric**: Count
    * **Color mapping**: Green for success, yellow for client errors, red for server errors

![Mosaic chart showing response status by operating system](/explore-analyze/images/mosaic-example-response-by-os.png "=70%")

**Product categories by continent**
:   Show how product preferences vary across regions:

    * Example based on: {{kib}} Sample Data eCommerce
    * **Horizontal axis**: `geoip.continent_name` (Top values)
    * **Vertical axis**: `category.keyword` (Top 5 values)
    * **Metric**: Count

![Mosaic chart showing product categories by continent](/explore-analyze/images/mosaic-example-category-by-continent.png "=70%")