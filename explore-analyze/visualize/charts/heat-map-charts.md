---
navigation_title: Heat map charts
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Instructions and best practices for building heat map charts with Kibana Lens in Elastic.
---

# Build heat map charts with {{kib}}

Heat map charts display data as a grid of colored cells, where each cell's color represents the magnitude of a value. They are ideal for visualizing patterns across two categorical or temporal dimensions, identifying correlations, and spotting anomalies in large datasets.

You can create heat map charts in {{kib}} using [**Lens**](../lens.md).

![Example Lens heat map chart representing temperatures in various cities](/explore-analyze/images/heat-map-chart-example.png)

## Build a heat map chart

:::{include} ../../_snippets/lens-prerequisites.md
:::

To build a heat map chart:

::::::{stepper}

:::::{step} Access Lens
**Lens** is {{kib}}'s main visualization editor. You can access it:
- From a dashboard: On the **Dashboards** page, open or create the dashboard where you want to add a heat map chart, then add a new visualization.
- From the **Visualize library** page by creating a new visualization.
:::::

:::::{step} Set the visualization to Heat map
New visualizations often start as **Bar** charts.

Using the **Visualization type** dropdown, select **Heat map**.
:::::

:::::{step} Define the data to show
1. Select the {{data-source}} that contains your data.
2. Configure the [**Horizontal axis**](#horizontal-axis-settings) dimension to define the columns of the heat map.
3. Configure the [**Cell value**](#cell-value-settings) dimension to define the metric that determines cell colors.

Optionally:
   - Configure the [**Vertical axis**](#vertical-axis-settings) dimension to define the rows of the heat map. Without a vertical axis, the heat map displays a single row of colored cells.

The chart preview updates to show a grid of colored cells. Cell colors represent the magnitude of the metric value. If the grid appears empty, verify that the axes have data for the current time range.
:::::

:::::{step} Customize the chart to follow best practices
Tweak the appearance of the chart to your needs. Consider the following best practices:

**Choose appropriate dimensions**
:   Select dimensions that have a reasonable number of distinct values. Too many values create unreadable grids with tiny cells.

**Use sequential color palettes**
:   For data that ranges from low to high, use a sequential palette (light to dark). Reserve diverging palettes for data with a meaningful midpoint.

**Consider data density**
:   If cells are too small to read, reduce the number of buckets or use a larger time interval on your axes.

**Order categories meaningfully**
:   For categorical axes, order values logically (alphabetically, by frequency, or by a natural ordering like days of the week). Use the **Sort order** [style setting](#appearance-options) to control how axis values are sorted.

Refer to [Heat map chart settings](#heat-map-chart-settings) to find all configuration options for your heat map chart.

For panel sizing and layout guidance, refer to [Organize dashboard panels](../../dashboards/arrange-panels.md#dashboard-grid-layout).
:::::

:::::{step} Save the chart
- If you accessed Lens from a dashboard, select **Save and return** to save the visualization and add it to that dashboard, or select **Save to library** to add the visualization to the Visualize library and reuse it later.
- If you accessed Lens from the Visualize library, select **Save**. A menu opens and offers you to add the visualization to a dashboard and to the Visualize library.
:::::

::::::

## Advanced heat map chart scenarios

### Highlight anomalies with custom color ranges [anomaly-colors]

You can configure custom color ranges on the **Cell value** dimension to emphasize unusual values, making outliers immediately visible.

1. Create a **Heat map** chart with your dimensions configured.
2. Select the **Cell value** dimension to open its settings.
3. In the **Color palette** configuration, select **Custom** to define your own color ranges:
   - Normal range: Neutral colors (blues, grays)
   - Anomalous range: Attention-grabbing colors (red, orange)

![Example Lens heat map chart showing error rates per day for various errors](/explore-analyze/images/heat-map-chart-example-server-errors.png)

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example tracks 404 and 503 error activity over time. Named filter rows isolate each error type, and absolute count thresholds drive the color — gray for normal, yellow for elevated, red for high — so anomalous periods stand out immediately.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "heatmap",
  "title": "Error rates per day",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "visible", "position": "right" },
  "axis": { "x": { "scale": "ordinal" }, "y": {} },
  "styling": { "cells": { "labels": { "visible": true } } },
  "x": {
    "operation": "date_histogram",
    "field": "@timestamp",
    "suggested_interval": "auto",
    "use_original_time_range": false,
    "include_empty_rows": true,
    "drop_partial_intervals": false
  },
  "y": {
    "operation": "filters", <1>
    "label": "Errors",
    "filters": [
      { "filter": { "expression": "\"response.keyword\" : \"404\"" }, "label": "Client errors" },
      { "filter": { "expression": "\"response.keyword\" : \"503\"" }, "label": "Server errors" }
    ]
  },
  "metric": {
    "operation": "formula", <2>
    "formula": "count()",
    "format": { "type": "number", "decimals": 0, "suffix": "%", "compact": false },
    "color": {
      "type": "dynamic", <3>
      "range": "absolute",
      "steps": [
        { "color": "#c2cbdb", "gte": 0, "lt": 5 },
        { "color": "#EAAE01", "gte": 5, "lt": 10 },
        { "color": "#F6726A", "gte": 10, "lte": null }
      ]
    }
  },
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "@timestamp"
  }
}
```

1. The `filters` grouping on the vertical axis creates two named rows — "Client errors" (404s) and "Server errors" (503s) — isolating each error type so every cell represents one error type in one time bucket.
2. The `formula` metric counts matching documents with `count()` and appends a `%` suffix to the display format, presenting counts in a percentage-like style without computing an actual ratio.
3. The `dynamic` color uses absolute count thresholds: gray for 0–4 errors, yellow for 5–9, and red for 10 or more, flagging time buckets with elevated error activity at a glance.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "heatmap",
  "title": "Error rates per day",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "visible", "position": "right" },
  "axis": { "x": { "scale": "ordinal" }, "y": {} },
  "styling": { "cells": { "labels": { "visible": true } } },
  "x": {
    "operation": "date_histogram",
    "field": "@timestamp",
    "suggested_interval": "auto",
    "use_original_time_range": false,
    "include_empty_rows": true,
    "drop_partial_intervals": false
  },
  "y": {
    "operation": "filters", <1>
    "label": "Errors",
    "filters": [
      { "filter": { "expression": "\"response.keyword\" : \"404\"" }, "label": "Client errors" },
      { "filter": { "expression": "\"response.keyword\" : \"503\"" }, "label": "Server errors" }
    ]
  },
  "metric": {
    "operation": "formula", <2>
    "formula": "count()",
    "format": { "type": "number", "decimals": 0, "suffix": "%", "compact": false },
    "color": {
      "type": "dynamic", <3>
      "range": "absolute",
      "steps": [
        { "color": "#c2cbdb", "gte": 0, "lt": 5 },
        { "color": "#EAAE01", "gte": 5, "lt": 10 },
        { "color": "#F6726A", "gte": 10, "lte": null }
      ]
    }
  },
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "@timestamp"
  }
}'
```

1. The `filters` grouping on the vertical axis creates two named rows — "Client errors" (404s) and "Server errors" (503s) — isolating each error type so every cell represents one error type in one time bucket.
2. The `formula` metric counts matching documents with `count()` and appends a `%` suffix to the display format, presenting counts in a percentage-like style without computing an actual ratio.
3. The `dynamic` color uses absolute count thresholds: gray for 0–4 errors, yellow for 5–9, and red for 10 or more, flagging time buckets with elevated error activity at a glance.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

## Heat map chart settings [heat-map-chart-settings]

Customize your heat map chart to display exactly the information you need, formatted the way you want.

### Horizontal axis settings [horizontal-axis-settings]

The **Horizontal axis** dimension defines the columns of the heat map.

**Data**
:   The **Horizontal axis** dimension supports the following functions:

    - **Top values**: Create columns for the most common values in a field.
      - **Field**: Select the field to group by. You can add up to 4 fields to create multi-term columns. When multiple fields are selected, each column represents a unique combination of values across those fields. You can reorder the fields by dragging them to change their priority.
      - **Number of values**: How many top values to display. The default number of values depends on your environment:
        - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Defaults to 9.
        - {applies_to}`stack: ga 9.0-9.3` Defaults to 5.
      :::{include} ../../_snippets/lens-rank-by-options.md
      :::
      :::{include} ../../_snippets/lens-breakdown-advanced-settings.md
      :::
    - **Date histogram**: Group data into time-based buckets.
      - **Field**: Select the date field to use for the time-based grouping.
      :::{include} ../../_snippets/lens-histogram-settings.md
      :::
    - **Intervals**: Create numeric ranges for continuous data.
      - **Field**: Select the numeric field to create intervals from.
      - **Include empty rows**: Include intervals with no matching documents.

**Appearance**
:   - **Name**: Customize the axis label.

### Vertical axis settings [vertical-axis-settings]

The **Vertical axis** dimension defines the rows of the heat map.

**Data**
:   The **Vertical axis** dimension supports the same functions as the horizontal axis:

    - **Top values**: Create rows for the most common values in a field.
      - **Field**: Select the field to group by. You can add up to 4 fields to create multi-term rows. When multiple fields are selected, each row represents a unique combination of values across those fields. You can reorder the fields by dragging them to change their priority.
      - **Number of values**: How many top values to display. The default number of values depends on your environment:
        - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Defaults to 9.
        - {applies_to}`stack: ga 9.0-9.3` Defaults to 3.
      :::{include} ../../_snippets/lens-rank-by-options.md
      :::
      :::{include} ../../_snippets/lens-breakdown-advanced-settings.md
      :::
    - **Date histogram**: Group data into time-based buckets.
      - **Field**: Select the date field to use for the time-based grouping.
      :::{include} ../../_snippets/lens-histogram-settings.md
      :::
    - **Intervals**: Create numeric ranges for continuous data.
      - **Field**: Select the numeric field to create intervals from.
      - **Include empty rows**: Include intervals with no matching documents.

**Appearance**
:   - **Name**: Customize the axis label.

### Cell value settings [cell-value-settings]

The **Cell value** dimension defines the metric that determines cell colors.

**Data**
:   The value that determines cell color intensity. When you drag a field onto the chart, {{kib}} suggests a function based on the field type. You can use aggregation functions like `Sum`, `Average`, `Count`, `Median`, and more, or create custom calculations with [formulas](/explore-analyze/visualize/lens.md#lens-formulas).

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
:   - **Name**: Customize the metric label displayed in tooltips.
    - **Value format**: Control how numeric values are displayed (number, percent, bytes, and more).
    - **Color palette**: Configure the color palette that maps cell values to colors. The default palette is **Temperature**. You can select a different palette, reverse the color direction, and define custom color ranges with specific value-to-color mappings.

### General layout [appearance-options]

When creating or editing a visualization, you can customize several appearance options from the {icon}`brush` **Style** or ![Legend icon](/explore-analyze/images/kibana-legend-icon.svg "") **Legend** menus.

#### Style settings

**Titles and text**

**Value labels**
:   Control whether cell values are displayed as text inside each cell:
    - **Hide**: Do not display values in cells (default).
    - **Show, if able**: Display the metric value inside each cell when there is enough space. Cells that are too small to fit the text will not show a label.

**Vertical axis**

**Axis title**
:   Show or hide the vertical axis title. When visible, you can enter a custom title or use the default field name.

**Tick labels**
:   Toggle whether to show or hide the tick labels on the vertical axis.

**Sort order** {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4`
:   Control the sort order of the vertical axis values:
    - **Unsorted**: Use the default sort order (default).
      
      {applies_to}`stack: ga 9.5` {applies_to}`serverless: ga` When the vertical axis uses numeric data, descending numeric order is used. Axes that use other data types, such as strings, are unaffected: their rows appear in the order the data is returned. You can still set the sort order manually.
   
    - **Ascending**: Sort values in ascending order. Automatically detects whether to use numeric or alphabetical sorting based on the data type.
    - **Descending**: Sort values in descending order. Automatically detects whether to use numeric or alphabetical sorting based on the data type.

**Horizontal axis**

**Axis title**
:   Show or hide the horizontal axis title. When visible, you can enter a custom title or use the default field name.

**Tick labels**
:   Toggle whether to show or hide the tick labels on the horizontal axis.

**Sort order** {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4`
:   Control the sort order of the horizontal axis values. Not available for time-based horizontal axes.
    - **Unsorted**: Use the default sort order (default).
    - **Ascending**: Sort values in ascending order. Automatically detects whether to use numeric or alphabetical sorting based on the data type.
    - **Descending**: Sort values in descending order. Automatically detects whether to use numeric or alphabetical sorting based on the data type.

**Orientation**
:   Control the orientation of horizontal axis tick labels. Only available when **Tick labels** is enabled.
    - **Horizontal**: Labels are displayed horizontally (default).
    - **Vertical**: Labels are rotated 90 degrees.
    - **Angled**: Labels are displayed at a 45-degree angle.

#### Legend settings

**Visibility**
:   Show or hide the legend:
    - **Show**: Display the legend (default).
    - **Hide**: Do not display the legend.

**Width**
:   Control the width of the legend panel. Options include **Small**, **Medium**, **Large**, and **Extra large**.

**Label truncation**
:   Toggle whether to truncate long legend labels. When enabled, set the **Line limit** to control the maximum number of lines for each label (defaults to 1).

## Heat map chart examples

<!-- MAINTENANCE: the API payload examples in this section were verified
against the Visualizations API spec. To re-verify after a schema change, run:
  KIBANA_URL=… API_KEY=… python3 .github/scripts/verify-lens-api-examples.py --file heat-map-charts.md
See .github/scripts/verify-lens-api-examples.py for full usage. -->

The following examples show various configuration options for building impactful heat map charts.

**Request volume by day and hour**
:   Visualize when your website receives the most traffic using a runtime field that extracts the hour of the day (0-23) from `@timestamp`:

    * Example based on: {{kib}} Sample Data Logs
    * **Horizontal axis**: `@timestamp` (Date histogram, daily)
    * **Vertical axis**: `hour_of_day` (Top 24 values, "Aggregate by this dimension first" active, ranked by descending alphabetical order)
    * **Cell value**: Count
    * **Color palette**: Cool (sequential)

![Heat map showing request volume by hour and day](/explore-analyze/images/heat-map-example-request-volume.png "=70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example builds a day-by-hour traffic grid using a runtime field (`hour_of_day`) on the vertical axis to reveal peak activity patterns across the week.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "heatmap",
  "title": "Request volume by day and hour",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "size": "auto" },
  "axis": { "x": { "scale": "temporal" }, "y": {} },
  "x": { "operation": "date_histogram", "field": "timestamp" },
  "y": {
    "operation": "terms",
    "fields": ["hour_of_day"], <1>
    "limit": 24, <2>
    "other_bucket": { "include_documents_without_field": false },
    "rank_by": { "type": "alphabetical", "direction": "desc" }
  },
  "metric": {
    "operation": "count",
    "empty_as_null": true,
    "color": {
      "type": "legacy_dynamic", <3>
      "palette": "cool",
      "range": "percentage",
      "shift": true,
      "steps": [
        { "color": "#cee1ff", "gte": 0, "lt": 20 },
        { "color": "#b5d2ff", "gte": 20, "lt": 40 },
        { "color": "#9bc2ff", "gte": 40, "lt": 60 },
        { "color": "#80b2ff", "gte": 60, "lt": 80 },
        { "color": "#61a2ff", "gte": 80, "lte": null }
      ]
    }
  },
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  }
}
```

1. `hour_of_day` is a runtime field that extracts the hour (0–23) from `@timestamp`, creating one row per hour.
2. `limit: 24` ensures all 24 hours appear on the vertical axis. Combined with alphabetical descending sort, hours are ordered 23 → 0 for a top-to-bottom timeline feel.
3. The `legacy_dynamic` coloring with the `cool` palette and `range: "percentage"` distributes the blue gradient proportionally across the actual value range, so the lightest blue always marks the quietest hours and the darkest blue the busiest.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "heatmap",
  "title": "Request volume by day and hour",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "size": "auto" },
  "axis": { "x": { "scale": "temporal" }, "y": {} },
  "x": { "operation": "date_histogram", "field": "timestamp" },
  "y": {
    "operation": "terms",
    "fields": ["hour_of_day"], <1>
    "limit": 24, <2>
    "other_bucket": { "include_documents_without_field": false },
    "rank_by": { "type": "alphabetical", "direction": "desc" }
  },
  "metric": {
    "operation": "count",
    "empty_as_null": true,
    "color": {
      "type": "legacy_dynamic", <3>
      "palette": "cool",
      "range": "percentage",
      "shift": true,
      "steps": [
        { "color": "#cee1ff", "gte": 0, "lt": 20 },
        { "color": "#b5d2ff", "gte": 20, "lt": 40 },
        { "color": "#9bc2ff", "gte": 40, "lt": 60 },
        { "color": "#80b2ff", "gte": 60, "lt": 80 },
        { "color": "#61a2ff", "gte": 80, "lte": null }
      ]
    }
  },
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  }
}'
```

1. `hour_of_day` is a runtime field that extracts the hour (0–23) from `@timestamp`, creating one row per hour.
2. `limit: 24` ensures all 24 hours appear on the vertical axis. Combined with alphabetical descending sort, hours are ordered 23 → 0 for a top-to-bottom timeline feel.
3. The `legacy_dynamic` coloring with the `cool` palette and `range: "percentage"` distributes the blue gradient proportionally across the actual value range, so the lightest blue always marks the quietest hours and the darkest blue the busiest.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

**Sales performance by product and region**
:   Compare product sales across geographic regions:

    * Example based on: {{kib}} Sample Data eCommerce
    * **Horizontal axis**: `geoip.city_name` (Top 10 values)
    * **Vertical axis**: `category.keyword` (Top values)
    * **Cell value**: `Sum(taxful_total_price)`
    * **Color palette**: Positive (sequential)

![Heat map showing sales performance by product and region](/explore-analyze/images/heat-map-example-sales-performance.png "=70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example uses two `terms` dimensions (city and product category) to create a category-versus-region grid, with cell color representing total revenue.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "heatmap",
  "title": "Sales performance by product and region",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "size": "auto" },
  "axis": { "x": { "scale": "ordinal" }, "y": {} },
  "x": {
    "operation": "terms",
    "fields": ["geoip.city_name"], <1>
    "limit": 10
  },
  "y": {
    "operation": "terms",
    "fields": ["category.keyword"], <2>
    "limit": 5
  },
  "metric": {
    "operation": "sum", <3>
    "field": "taxful_total_price",
    "label": "Revenue",
    "empty_as_null": true,
    "color": {
      "type": "legacy_dynamic",
      "palette": "positive",
      "range": "percentage",
      "shift": true,
      "steps": [
        { "color": "#d4efe6", "gte": 0, "lt": 20 },
        { "color": "#b1e4d1", "gte": 20, "lt": 40 },
        { "color": "#8cd9bb", "gte": 40, "lt": 60 },
        { "color": "#62cea6", "gte": 60, "lt": 80 },
        { "color": "#24c292", "gte": 80, "lte": null }
      ]
    }
  },
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_ecommerce",
    "time_field": "order_date"
  }
}
```

1. Cities on the horizontal axis create one column per location, making geographic performance quick to scan.
2. Product categories on the vertical axis form the rows, so each cell shows revenue for one category in one city.
3. `sum` of `taxful_total_price` colors cells by total revenue rather than document count.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "heatmap",
  "title": "Sales performance by product and region",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "size": "auto" },
  "axis": { "x": { "scale": "ordinal" }, "y": {} },
  "x": {
    "operation": "terms",
    "fields": ["geoip.city_name"], <1>
    "limit": 10
  },
  "y": {
    "operation": "terms",
    "fields": ["category.keyword"], <2>
    "limit": 5
  },
  "metric": {
    "operation": "sum", <3>
    "field": "taxful_total_price",
    "label": "Revenue",
    "empty_as_null": true,
    "color": {
      "type": "legacy_dynamic",
      "palette": "positive",
      "range": "percentage",
      "shift": true,
      "steps": [
        { "color": "#d4efe6", "gte": 0, "lt": 20 },
        { "color": "#b1e4d1", "gte": 20, "lt": 40 },
        { "color": "#8cd9bb", "gte": 40, "lt": 60 },
        { "color": "#62cea6", "gte": 60, "lt": 80 },
        { "color": "#24c292", "gte": 80, "lte": null }
      ]
    }
  },
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_ecommerce",
    "time_field": "order_date"
  }
}'
```

1. Cities on the horizontal axis create one column per location, making geographic performance quick to scan.
2. Product categories on the vertical axis form the rows, so each cell shows revenue for one category in one city.
3. `sum` of `taxful_total_price` colors cells by total revenue rather than document count.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::
