---
navigation_title: Treemap charts
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Instructions and best practices for building treemap charts with Kibana Lens in Elastic.
---

# Build treemap charts with {{kib}}

Treemap charts display hierarchical data as nested rectangles, where each rectangle's size represents a quantitative value. They are ideal for showing part-to-whole relationships within hierarchies, comparing relative sizes of categories, and visualizing how data is distributed across multiple levels.

You can create treemap charts in {{kib}} using [**Lens**](../lens.md).

![Example Lens treemap charts based on sample data](/explore-analyze/images/treemap-example.png)

## Build a treemap chart

:::{include} ../../_snippets/lens-prerequisites.md
:::

To build a treemap chart:

::::::{stepper}

:::::{step} Access Lens
**Lens** is {{kib}}'s main visualization editor. You can access it:
- From a dashboard: On the **Dashboards** page, open or create the dashboard where you want to add a treemap chart, then add a new visualization.
- From the **Visualize library** page by creating a new visualization.
:::::

:::::{step} Set the visualization to Treemap
New visualizations often start as **Bar** charts.

Using the **Visualization type** dropdown, select **Treemap**.
:::::

:::::{step} Define the data to show
1. Select the {{data-source}} that contains your data.
2. Configure the [**Group by**](#group-by-settings) dimension to define how the rectangles are grouped. Add multiple **Group by** dimensions to create a hierarchy.
3. Configure the [**Metric**](#metric-settings) dimension to define the size of each rectangle.

The chart preview updates to show rectangles sized by your metric. If you added multiple **Group by** dimensions, smaller rectangles appear nested inside the top-level categories.
:::::

:::::{step} Customize the chart to follow best practices
Tweak the appearance of the chart to your needs. Consider the following best practices:

**Limit hierarchy depth**
:   Keep your treemap to 2-3 levels of hierarchy. Deeper nesting becomes difficult to read and interpret.

**Order categories by size**
:   Arrange rectangles by size (largest first) to make comparisons easier. This is the default behavior in Lens.

**Use color meaningfully**
:   Apply colors to distinguish top-level categories or to represent an additional metric (such as growth rate or status).

**Ensure readable labels**
:   Labels are automatically hidden on rectangles that are too small to fit them. If too many labels are missing, reduce the number of categories or increase the panel size.

Refer to [Treemap chart settings](#treemap-chart-settings) to find all configuration options for your treemap chart.
:::::

:::::{step} Save the chart
- If you accessed Lens from a dashboard, select **Save and return** to save the visualization and add it to that dashboard, or select **Save to library** to add the visualization to the Visualize library and reuse it later.
- If you accessed Lens from the Visualize library, select **Save**. A menu opens and lets you add the visualization to a dashboard and to the Visualize library.
:::::

::::::

## Treemap chart settings [treemap-chart-settings]

Customize your treemap chart to display exactly the information you need, formatted the way you want.

### Group by settings [group-by-settings]

The **Group by** dimension defines how rectangles are grouped. You can add up to 2 levels of grouping to create hierarchical visualizations.

**Data**
:   The **Group by** dimension supports the following functions:

    - **Top values**: Create rectangles for the most common values in a field.
      - **Field**: Select the field to group by. You can add up to 4 fields to create multi-term groups. When multiple fields are selected, each group represents a unique combination of values across those fields. You can reorder the fields by dragging them to change their priority.
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
    - **Filters**: Define custom KQL filters to create specific groups.
      - **Collapse by**: Aggregate values into a single number using `Sum`, `Average`, `Min`, or `Max`.

**Appearance**
:   - **Name**: Customize the legend label.
    - **Color mapping**: Select a color palette or assign specific colors to categories. Refer to [Assign colors to terms](../lens.md#assign-colors-to-terms) for details. Color mapping is only available on the first **Group by** dimension. Nested levels inherit colors from their parent category.

### Metric settings [metric-settings]

The **Metric** dimension defines the size of each rectangle.

**Data**
:   The value that determines rectangle size. When you drag a field onto the chart, {{kib}} suggests a function based on the field type. You can use aggregation functions like `Sum`, `Average`, `Count`, `Median`, and more, or create custom calculations with [formulas](/explore-analyze/visualize/lens.md#lens-formulas).

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
:   - **Name**: Customize the metric label displayed in tooltips and legends.
    - **Value format**: Control how numeric values are displayed (number, percent, bytes, and more).

### General layout [appearance-options]

When creating or editing a visualization, you can customize several appearance options from the {icon}`brush` **Style** or ![Legend icon](/explore-analyze/images/kibana-legend-icon.svg "") **Legend** menus.

#### Style settings

**Slice labels**
:   Control how labels appear on rectangles:
    - **Show**: Display labels on all rectangles where space permits (default).
    - **Hide**: Do not display labels on rectangles.

**Slice values**
:   Control what values appear on rectangles:
    - **Percentage**: Display the percentage of total (default).
    - **Integer**: Display the raw numeric value.
    - **Hide**: Do not display values.

    When displaying percentages, you can also configure the **Decimal places** (default: 2).

#### Legend settings

**Visibility**
:   Specify whether to automatically show the legend or hide it:
    - **Auto**: Hide the legend (default).
    - **Show**: Always show the legend.
    - **Hide**: Never show the legend.

**Width**
:   Control the width of the legend panel: **Small**, **Medium**, **Large**, or **Extra large**.

**Label truncation**
:   Toggle whether to truncate long legend labels. When enabled, set the **Line limit** to control how many lines to display before truncating (1-5, default: 1).

**Nested**
:   When using multiple **Group by** dimensions, enable this option to show the legend in a hierarchical format.

## Treemap chart examples

The following examples show various configuration options for building impactful treemap charts.

**Bytes per file extension**
:   See which file extensions consume the most bandwidth, excluding blank values:

    * Example based on: {{kib}} Sample Data Logs
    * **Group by**: `extension.keyword`
      * Top 6 values
      * Advanced: include values matching the `.+` regular expression to exclude blank values
    * **Metric**: Sum of `bytes`

![Treemap showing bytes per file extension](/explore-analyze/images/treemap-example-bytes-per-extension.png "=70%")

:::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example creates a single-level treemap where each rectangle represents a file extension and its size reflects total bandwidth consumed.

```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "treemap",                                                               <1>
  "title": "Bytes per file extension",
  "dataset": { "type": "index", "index": "kibana_sample_data_logs", "time_field": "timestamp" },
  "filters": [],
  "query": { "query": "" },
  "legend": { "size": "auto" },
  "value_display": { "mode": "absolute" },                                         <2>
  "metrics": [
    {
      "operation": "sum",
      "field": "bytes",
      "label": "Total bytes",
      "format": { "type": "number" },
      "filter": { "query": "" }
    }
  ],
  "group_by": [
    {
      "operation": "terms",
      "fields": ["extension.keyword"],
      "size": 6                                                                    <3>
    }
  ]
}'
```

1. `treemap` renders nested rectangles whose area is proportional to the metric value.
2. `absolute` displays the raw byte count on each rectangle instead of a percentage.
3. `size: 6` limits the chart to the top 6 file extensions, keeping the layout readable.

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::

**Flights by carrier and destination country**
:   Show how flight volume is distributed across airlines and their destination countries, using two hierarchy levels:

    * Example based on: {{kib}} Sample Data Flights
    * **Group by** (Level 1): `Carrier` (Top 5 values)
    * **Group by** (Level 2): `DestCountry` (Top 5 values)
    * **Metric**: Count

![Treemap showing flights by carrier and destination country](/explore-analyze/images/treemap-example-flights-carrier.png "=70%")

:::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example creates a two-level treemap: the outer rectangles represent airlines and the inner rectangles show destination countries, revealing how each carrier's flight volume is distributed geographically.

```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "treemap",
  "title": "Flights by carrier and destination country",
  "dataset": { "type": "index", "index": "kibana_sample_data_flights", "time_field": "timestamp" },
  "filters": [],
  "query": { "query": "" },
  "legend": { "size": "auto" },
  "value_display": { "mode": "absolute" },
  "metrics": [
    {
      "operation": "count",
      "label": "Flights",
      "format": { "type": "number" },
      "filter": { "query": "" }
    }
  ],
  "group_by": [
    {
      "operation": "terms",
      "fields": ["Carrier"],                                                       <1>
      "size": 5
    },
    {
      "operation": "terms",
      "fields": ["DestCountry"],                                                   <2>
      "size": 5
    }
  ]
}'
```

1. The first `group_by` entry creates the outer (parent) rectangles, one per airline carrier.
2. The second `group_by` entry nests destination countries inside each carrier, forming the two-level hierarchy.

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::

**Response status per host**
:   See which hosts handle the most traffic and how their response status breaks down:

    * Example based on: {{kib}} Sample Data Logs
    * **Group by** (Level 1): `host.keyword` (Top 3 values)
    * **Group by** (Level 2): Filters
      - "Success (2xx/3xx)": `response.keyword >= "200" AND response.keyword < "400"`
      - "Client errors (4xx)": `response.keyword >= "400" AND response.keyword < "500"`
      - "Server errors (5xx)": `response.keyword >= "500"`
    * **Metric**: Count
    * **Color**: Gradient (`#ffc7db`)

![Treemap showing response status per host](/explore-analyze/images/treemap-example-response-per-host.png "=70%")

:::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example nests KQL-based response status categories inside host rectangles, combining `terms` and `filters` groupings to show both traffic volume and health per host.

```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "treemap",
  "title": "Response status per host",
  "dataset": { "type": "index", "index": "kibana_sample_data_logs", "time_field": "timestamp" },
  "filters": [],
  "query": { "query": "" },
  "legend": { "size": "auto" },
  "value_display": { "mode": "absolute" },
  "metrics": [
    {
      "operation": "count",
      "label": "Count",
      "format": { "type": "number" },
      "filter": { "query": "" }
    }
  ],
  "group_by": [
    {
      "operation": "terms",
      "fields": ["host.keyword"],                                                  <1>
      "size": 3
    },
    {
      "operation": "filters",                                                      <2>
      "filters": [
        { "filter": { "query": "response.keyword >= \"200\" AND response.keyword < \"400\"" }, "label": "Success (2xx/3xx)" },
        { "filter": { "query": "response.keyword >= \"400\" AND response.keyword < \"500\"" }, "label": "Client errors (4xx)" },
        { "filter": { "query": "response.keyword >= \"500\"" }, "label": "Server errors (5xx)" }
      ]
    }
  ]
}'
```

1. The top-level `terms` grouping creates one outer rectangle per host, sized by total request count.
2. The nested `filters` grouping splits each host rectangle into success, client error, and server error segments using KQL queries.

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::
