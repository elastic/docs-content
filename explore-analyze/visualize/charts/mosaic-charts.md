---
navigation_title: Mosaic charts
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
description: Create mosaic charts to visualize relationships between two categorical variables and explore conditional distributions.
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
:::{include} ../../_snippets/access-lens.md
:::
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

For panel sizing and layout guidance, refer to [Organize dashboard panels](../../dashboards/arrange-panels.md#dashboard-grid-layout).
:::::

:::::{step} Save the chart
:::{include} ../../_snippets/save-visualization.md
:::
:::::

::::::

## Mosaic chart settings [mosaic-chart-settings]

Customize your mosaic chart to display exactly the information you need, formatted the way you want.

### Horizontal axis settings [horizontal-axis-settings]

The **Horizontal axis** dimension defines the columns of the mosaic. Column widths represent the proportion of each category. In the API, this corresponds to `group_breakdown_by`.

**Data**
:   The **Horizontal axis** dimension supports the following functions:

    - **Top values**: Create columns for the most common values in a field.
      - **Field**: Select the field to group by. You can add up to 4 fields to create multi-term columns. When multiple fields are selected, each column represents a unique combination of values across those fields. You can reorder the fields by dragging them to change their priority.
      - **Number of values**: How many categories to display. The default number of values depends on your environment:
        - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Defaults to 9.
        - {applies_to}`stack: ga 9.0-9.3` Defaults to 5.
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

The **Vertical axis** dimension defines the rows within each column. Rectangle heights represent the proportion of each category within the column. In the API, this corresponds to `group_by`, and color mapping is configured here.

**Data**
:   The **Vertical axis** dimension supports the following functions:

    - **Top values**: Create rows for the most common values in a field.
      - **Field**: Select the field to group by. You can add up to 4 fields to create multi-term rows. When multiple fields are selected, each row represents a unique combination of values across those fields. You can reorder the fields by dragging them to change their priority.
      - **Number of values**: How many categories to display. The default number of values depends on your environment:
        - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Defaults to 9.
        - {applies_to}`stack: ga 9.0-9.3` Defaults to 3.
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

<!-- MAINTENANCE: the API payload examples in this section were verified
against the Visualizations API spec. To re-verify after a schema change, run:
  KIBANA_URL=… API_KEY=… python3 .github/scripts/verify-lens-api-examples.py --file mosaic-charts.md
See .github/scripts/verify-lens-api-examples.py for full usage. -->

The following examples show various configuration options for building impactful mosaic charts.

**Response status by operating system**
:   Visualize how response status categories vary across operating systems:

    * Example based on: {{kib}} Sample Data Logs
    * **Horizontal axis** (columns): `machine.os.keyword` (Top 5 values)
    * **Vertical axis** (rows): **Filters**
      - "Success (2xx/3xx)": `response.keyword >= "200" AND response.keyword < "400"`
      - "Client errors (4xx)": `response.keyword >= "400" AND response.keyword < "500"`
      - "Server errors (5xx)": `response.keyword >= "500"`
    * **Metric**: Count
    * **Color mapping**: Teal for success, pink for client errors, red for server errors

![Mosaic chart showing response status by operating system](/explore-analyze/images/mosaic-example-response-by-os.png "=70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example creates a mosaic chart where column widths represent OS popularity and the colored rows within each column show the proportion of success, client error, and server error responses.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "mosaic", <1>
  "title": "Response status by operating system",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto", "nested": false },
  "metric": { "operation": "count", "empty_as_null": true },
  "group_by": [ <2>
    {
      "operation": "filters",
      "filters": [
        {
          "filter": { "expression": "response.keyword >= \"200\" AND response.keyword < \"400\"" },
          "label": "Success (2xx/3xx)"
        },
        {
          "filter": { "expression": "response.keyword >= \"400\" AND response.keyword < \"500\"" },
          "label": "Client errors (4xx)"
        },
        {
          "filter": { "expression": "response.keyword >= \"500\"" },
          "label": "Server errors (5xx)"
        }
      ],
      "color": {
        "mode": "categorical",
        "palette": "default",
        "mapping": [
          { "values": ["Success (2xx/3xx)"], "color": { "type": "from_palette", "palette": "default", "index": 0 } },
          { "values": ["Client errors (4xx)"], "color": { "type": "from_palette", "palette": "default", "index": 8 } },
          { "values": ["Server errors (5xx)"], "color": { "type": "from_palette", "palette": "default", "index": 6 } }
        ]
      }
    }
  ],
  "group_breakdown_by": [ <3>
    {
      "operation": "terms",
      "fields": ["machine.os.keyword"],
      "limit": 5,
      "other_bucket": { "include_documents_without_field": false },
      "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": { "values": { "visible": true, "mode": "percentage" } }
}
```

1. `mosaic` renders a grid where both column width and row height encode proportions, making distribution comparisons clear across two dimensions.
2. `group_by` defines the vertical axis (rows). Using `filters` here creates three named rows — one per response status category — each colored from the `mapping` so success, client errors, and server errors are immediately distinguishable.
3. `group_breakdown_by` defines the horizontal axis (columns). Each OS becomes a column whose width reflects its share of total traffic.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "mosaic", <1>
  "title": "Response status by operating system",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto", "nested": false },
  "metric": { "operation": "count", "empty_as_null": true },
  "group_by": [ <2>
    {
      "operation": "filters",
      "filters": [
        {
          "filter": { "expression": "response.keyword >= \"200\" AND response.keyword < \"400\"" },
          "label": "Success (2xx/3xx)"
        },
        {
          "filter": { "expression": "response.keyword >= \"400\" AND response.keyword < \"500\"" },
          "label": "Client errors (4xx)"
        },
        {
          "filter": { "expression": "response.keyword >= \"500\"" },
          "label": "Server errors (5xx)"
        }
      ],
      "color": {
        "mode": "categorical",
        "palette": "default",
        "mapping": [
          { "values": ["Success (2xx/3xx)"], "color": { "type": "from_palette", "palette": "default", "index": 0 } },
          { "values": ["Client errors (4xx)"], "color": { "type": "from_palette", "palette": "default", "index": 8 } },
          { "values": ["Server errors (5xx)"], "color": { "type": "from_palette", "palette": "default", "index": 6 } }
        ]
      }
    }
  ],
  "group_breakdown_by": [ <3>
    {
      "operation": "terms",
      "fields": ["machine.os.keyword"],
      "limit": 5,
      "other_bucket": { "include_documents_without_field": false },
      "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": { "values": { "visible": true, "mode": "percentage" } }
}'
```

1. `mosaic` renders a grid where both column width and row height encode proportions, making distribution comparisons clear across two dimensions.
2. `group_by` defines the vertical axis (rows). Using `filters` here creates three named rows — one per response status category — each colored from the `mapping` so success, client errors, and server errors are immediately distinguishable.
3. `group_breakdown_by` defines the horizontal axis (columns). Each OS becomes a column whose width reflects its share of total traffic.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

**Product categories by continent**
:   Show how product preferences vary across regions:

    * Example based on: {{kib}} Sample Data eCommerce
    * **Horizontal axis** (columns): `geoip.continent_name` (Top values)
    * **Vertical axis** (rows): `category.keyword` (Top 9 values)
    * **Metric**: Count

![Mosaic chart showing product categories by continent](/explore-analyze/images/mosaic-example-category-by-continent.png "=70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example uses `terms` on both axes to compare product category preferences across continents, revealing how shopping behavior varies by region.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "mosaic",
  "title": "Product categories by continent",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto", "nested": false },
  "metric": { "operation": "count", "empty_as_null": true },
  "group_by": [
    {
      "operation": "terms",
      "fields": ["category.keyword"], <1>
      "limit": 9,
      "other_bucket": { "include_documents_without_field": false },
      "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" },
      "color": { "mode": "categorical", "palette": "default", "mapping": [] }
    }
  ],
  "group_breakdown_by": [
    {
      "operation": "terms",
      "fields": ["geoip.continent_name"], <2>
      "limit": 9,
      "other_bucket": { "include_documents_without_field": false },
      "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_ecommerce",
    "time_field": "order_date"
  },
  "styling": { "values": { "visible": true, "mode": "percentage" } }
}
```

1. `category.keyword` on the vertical axis (`group_by`) creates one row per product category. The `color` mapping assigns a distinct palette color to each category, making each category trackable across columns.
2. `geoip.continent_name` on the horizontal axis (`group_breakdown_by`) creates one column per continent, with width proportional to order volume from that region.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "mosaic",
  "title": "Product categories by continent",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto", "nested": false },
  "metric": { "operation": "count", "empty_as_null": true },
  "group_by": [
    {
      "operation": "terms",
      "fields": ["category.keyword"], <1>
      "limit": 9,
      "other_bucket": { "include_documents_without_field": false },
      "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" },
      "color": { "mode": "categorical", "palette": "default", "mapping": [] }
    }
  ],
  "group_breakdown_by": [
    {
      "operation": "terms",
      "fields": ["geoip.continent_name"], <2>
      "limit": 9,
      "other_bucket": { "include_documents_without_field": false },
      "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_ecommerce",
    "time_field": "order_date"
  },
  "styling": { "values": { "visible": true, "mode": "percentage" } }
}'
```

1. `category.keyword` on the vertical axis (`group_by`) creates one row per product category. The `color` mapping assigns a distinct palette color to each category, making each category trackable across columns.
2. `geoip.continent_name` on the horizontal axis (`group_breakdown_by`) creates one column per continent, with width proportional to order volume from that region.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::
