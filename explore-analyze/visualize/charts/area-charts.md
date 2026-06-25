---
navigation_title: Area charts
applies_to:
  stack: ga
  serverless: ga
description: Instructions and best practices for building area charts with Kibana Lens in Elastic.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Build area charts with {{kib}}

Area charts are line charts with the area below the line filled in with a certain color or texture. Area charts work with numeric metrics over the horizontal axis (typically time) and are ideal to display quantitative values over an interval or time period, to show trends for time series like traffic, CPU, revenue, or error rates.

You can create area charts in {{kib}} using [**Lens**](../lens.md).

![Example Lens area chart](../../images/kibana-area-chart.png)

## Build an area chart

:::{include} ../../_snippets/lens-prerequisites.md
:::

To build an area chart:

::::::{stepper}

:::::{step} Access Lens
:::{include} ../../_snippets/access-lens.md
:::
:::::

:::::{step} Set the visualization to Area
New visualizations often start as **Bar** charts.

Using the **Visualization type** dropdown, select **Area**.
:::::

:::::{step} Define the data to show
1. Select the {{data-source}} that contains your data.
2. Drag a [time field](elasticsearch://reference/elasticsearch/mapping-reference/date.md) to the **Horizontal axis** and a numeric field to the **Vertical axis**. {{kib}} automatically selects an appropriate aggregation function compatible with the selected field.

Optionally:
   - Add more numeric fields to create additional series, or drag a categorical field to the **Breakdown** settings to segment your data by a categorical field, and create multiple areas within the same chart.
   - You can click the **Add layer** icon {icon}`plus_square` to integrate additional visualizations, [annotations](../lens.md#add-annotations), or a [reference line](../lens.md#add-reference-lines).

The chart preview updates to show filled areas plotted over time. Each area represents a series, with the filled region emphasizing the volume of data.
:::::

:::::{step} Customize the chart to follow best practices
Tweak the appearance of the chart to your needs. Consider the following best practices:

**Choose the right stack mode**
:   Use **Stacked** to show contribution to a whole, **Percentage** for normalized representation of values, or **Unstacked** when absolute trends matter more than composition. For a practical use case, check how to [show composition with stacked and 100% stacked areas](#area-stacking).

**Handle gaps and noise**
:   For sparse data, configure **Missing values** and **Line interpolation** to avoid misleading gaps or sharp edges. Check the [Visualization appearance options](../lens.md#customize-visualization-appearance).

**Use color purposefully**
:   Apply colors to highlight important data or patterns. Avoid using too many colors that might distract from the data. You can also assign [consistent colors to key categories](../lens.md#assign-colors-to-terms).

**Label clearly**
:   Provide a descriptive title and axis labels that clearly communicate what the chart shows. For example, mention the metric being visualized ("Average Response Time") and reference the time period when relevant ("Dec 8-16, 2025").

Refer to [Area chart settings](#area-chart-settings) to find all configuration options for your area chart.

For panel sizing and layout guidance, refer to [Organize dashboard panels](../../dashboards/arrange-panels.md#dashboard-grid-layout).
:::::

:::::{step} Save the chart
:::{include} ../../_snippets/save-visualization.md
:::
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

4. Optionally, in the **Breakdown** settings, you can set **Rank by** to specify the dimension the top values are ranked by.

### Compare current versus previous period with time shift [area-timeshift]

In Area charts, you can enable time shift to compare different periods and identify deltas.

![Example Lens area chart compare periods](../../images/kibana-area-compare-periods.png)

1. Create an area chart with a time-based **Horizontal axis** and your main metric on **Vertical axis**, for example: `bytes`.
2. Duplicate the layer:
    * {applies_to}`serverless: ga` {applies_to}`stack: ga 9.3` Select {icon}`copy` **Duplicate layer** from the visualization editor.
    * {applies_to}`stack: ga 9.0-9.2` Open the {icon}`boxes_vertical` contextual menu of the visualization editor and select {icon}`copy` **Duplicate layer**.
3. From the duplicated layer settings, select the field defined as vertical axis to open its details. Expand its **Advanced** options and set **Time shift** to `1w` or to the time value of your choice.
   Check [Compare differences over time](../lens.md#compare-data-with-time-offsets) for more details.
4. Optionally, customize the appearance of the layer to adjust how it looks on the chart. When you duplicate a layer, {{kib}} automatically assigns a different **Series color** to the new layer. You can for example change this color, or adjust the layer's name and axis position. This name is used for the chart's legend.

::::{tip}
You can also compute the relative change using a formula, for example:
`(average(bytes) - average(bytes, shift='1w')) / average(bytes, shift='1w')`
::::

## Area chart settings [area-chart-settings]

Customize your area chart to match the information you need and how you want it displayed.

### Horizontal axis settings [horizontal-axis-settings]

**Data**
:   
    - **Functions**:
      - **Top values**: Create separate areas for the most common values in a field.
        - **Field**: Select the field to group by. You can add up to 4 fields. When multiple fields are selected, each area represents a unique combination of values across those fields. You can reorder the fields by dragging them to change their priority.
        - **Number of values**: How many top values to display. The default number of values depends on your environment:
          - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Defaults to 9.
          - {applies_to}`stack: ga 9.0-9.3` Defaults to 5.
        :::{include} ../../_snippets/lens-rank-by-options.md
        :::
        :::{include} ../../_snippets/lens-breakdown-advanced-settings.md
        :::
      - **Date histogram**: Group data points into time-based buckets (for example, hourly, daily, weekly). 
        - **Field**: Select the date field to use for the time-based grouping.
        :::{include} ../../_snippets/lens-histogram-settings.md
        :::
      - **Intervals**: Create numeric ranges for continuous data. You can define the interval granularity or specify custom ranges.
        - **Field**: Select the numeric field to create intervals from.
      - **Filters**: Allow you to segment your data based on specific conditions, creating separate areas for each filter.

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

You can split your data by a categorical field to create multiple stacked or overlapping areas. You can specify the following options:

**Data**
:   
    - **Functions**:
      - **Top values**: Create separate areas for the most common values in a field.
        - **Field**: Select the field to group by. You can add up to 4 fields. When multiple fields are selected, each area represents a unique combination of values across those fields. You can reorder the fields by dragging them to change their priority.
        - **Number of values**: How many top values to display. The default number of values depends on your environment:
          - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Defaults to 9.
          - {applies_to}`stack: ga 9.0-9.3` Defaults to 3.
        :::{include} ../../_snippets/lens-rank-by-options.md
        :::
        :::{include} ../../_snippets/lens-breakdown-advanced-settings.md
        :::
      - **Date histogram**: Group data points into time-based buckets (for example, hourly, daily, weekly). 
        - **Field**: Select the date field to use for the time-based grouping.
        :::{include} ../../_snippets/lens-histogram-settings.md
        :::
      - **Intervals**: Create numeric ranges for continuous data. You can define the interval granularity or specify custom ranges.
        - **Field**: Select the numeric field to create intervals from.
      - **Filters**: Create separate colored areas based on filter conditions.

**Appearance**
:   Allow you to customize how your breakdown data is displayed in line charts, including:

    - **Name**: It's a best practice to customize this with a meaningful title.
    - **Color mapping**: Determine how colors are assigned to your breakdown series.

### General layout [appearance-options]

When creating or editing a visualization, you can adjust the following settings.

:::{include} ../../_snippets/area-chart-style-settings.md
:::

:::{include} ../../_snippets/line-chart-legend-settings.md
:::


## Area chart examples

<!-- MAINTENANCE: the API payload examples in this section were verified
against the Visualizations API spec. To re-verify after a schema change, run:
  KIBANA_URL=… API_KEY=… python3 .github/scripts/verify-lens-api-examples.py --file area-charts.md
See .github/scripts/verify-lens-api-examples.py for full usage. -->

**Traffic by geographic region**
:   Visualizing which geographic regions generate the most traffic:
   - **Horizontal axis**: `@timestamp` (Date histogram)
   - **Vertical axis**: `records`
   - **Breakdown**: `geo.dest`
   
![Example Lens area chart geographical regions](../../images/kibana-area-geo-regions.png " =70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

Send the following request to create a stacked area chart that shows record counts broken down by geographic destination.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "xy",
  "title": "Traffic by geographic region",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto", "placement": "outside", "position": "right" },
  "axis": {},
  "layers": [
    {
      "type": "area_stacked", <1>
      "x": { "operation": "date_histogram", "field": "timestamp", "include_empty_rows": true }, <2>
      "y": [
        {
          "operation": "count",
          "empty_as_null": false,
          "label": "Records",
          "format": { "type": "number", "decimals": 0 },
          "filter": { "expression": "" }
        }
      ],
      "breakdown_by": {
        "operation": "terms",
        "fields": ["geo.dest"],
        "limit": 3, <3>
        "other_bucket": { "include_documents_without_field": false }, <4>
        "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" },
        "aggregate_first": true <5>
      },
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    }
  ],
  "styling": {
    "fitting": { "type": "none" },
    "areas": { "fill_opacity": 0.3 },
    "points": { "visibility": "visible" }
  }
}
```

1. Uses `area_stacked` to show each region's contribution to the total traffic.
2. `include_empty_rows: true` fills time buckets with no data as zero rather than leaving gaps.
3. Shows only the top 3 geographic destinations.
4. `other_bucket` groups all remaining destinations into an **Other** segment.
5. `aggregate_first: true` ranks destinations globally across the full time range, ensuring the same top 3 appear consistently in every bucket.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "xy",
  "title": "Traffic by geographic region",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto", "placement": "outside", "position": "right" },
  "axis": {},
  "layers": [
    {
      "type": "area_stacked", <1>
      "x": { "operation": "date_histogram", "field": "timestamp", "include_empty_rows": true }, <2>
      "y": [
        {
          "operation": "count",
          "empty_as_null": false,
          "label": "Records",
          "format": { "type": "number", "decimals": 0 },
          "filter": { "expression": "" }
        }
      ],
      "breakdown_by": {
        "operation": "terms",
        "fields": ["geo.dest"],
        "limit": 3, <3>
        "other_bucket": { "include_documents_without_field": false }, <4>
        "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" },
        "aggregate_first": true <5>
      },
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    }
  ],
  "styling": {
    "fitting": { "type": "none" },
    "areas": { "fill_opacity": 0.3 },
    "points": { "visibility": "visible" }
  }
}'
```

1. Uses `area_stacked` to show each region's contribution to the total traffic.
2. `include_empty_rows: true` fills time buckets with no data as zero rather than leaving gaps.
3. Shows only the top 3 geographic destinations.
4. `other_bucket` groups all remaining destinations into an **Other** segment.
5. `aggregate_first: true` ranks destinations globally across the full time range, ensuring the same top 3 appear consistently in every bucket.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

**Response code over time with annotations**

Visualizing HTTP response codes over time, highlighting the proportion of success, client error, and server error responses, with annotations for key events:

* **Horizontal axis**: `@timestamp` (Date histogram)
* **Vertical axis**: `Count of records`
* **Breakdown**:
  * **Success/Redirection**: `response.keyword >= 200 and response.keyword < 400`
  * **Client Error**: `response.keyword >= 400 and response.keyword < 500`
  * **Server Error**: `response.keyword >= 500`
* **Stacking**: `Percentage` to show the distribution relative to the total count at each point in time.
* **Annotation query**: `tags:error AND tags:security`

![Example Lens area chart response code annotations](../../images/kibana-response-code-annotations.png " =70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

Send the following request to create a percentage area chart that shows the distribution of HTTP response codes over time.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "xy",
  "title": "Response code over time",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto", "placement": "outside", "position": "bottom", "layout": { "type": "list" } },
  "axis": {},
  "layers": [
    {
      "type": "area_percentage", <1>
      "x": {
        "operation": "date_histogram",
        "field": "timestamp"
      },
      "y": [
        {
          "operation": "count",
          "empty_as_null": false,
          "label": "Count of records",
          "format": { "type": "number", "decimals": 2 },
          "filter": { "expression": "" }
        }
      ],
      "breakdown_by": {
        "operation": "filters", <2>
        "filters": [
          {
            "filter": { "expression": "response.keyword >= 200 and response.keyword < 400" },
            "label": "Success/Redirection"
          },
          {
            "filter": { "expression": "response.keyword >= 400 and response.keyword < 500" },
            "label": "Client Error"
          },
          { "filter": { "expression": "response.keyword >= 500" }, "label": "Server Error" }
        ]
      },
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    },
    {
      "type": "annotations", <3>
      "ignore_global_filters": true,
      "events": [
        {
          "type": "query",
          "label": "Event",
          "query": { "language": "kql", "expression": "tags:error AND tags:security" },
          "time_field": "timestamp",
          "color": { "type": "static", "color": "#ee72a6" },
          "visible": true,
          "icon": "asterisk"
        }
      ],
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    }
  ],
  "styling": {
    "fitting": { "type": "none" },
    "areas": { "fill_opacity": 0.3 }
  }
}
```

1. `area_percentage` normalizes each time bucket to 100% so you see the proportion of each response class, not absolute counts.
2. `filters` breakdown creates one area per KQL filter instead of splitting by field values.
3. The `annotations` layer marks events matching `tags:error AND tags:security` on the time axis with a pink asterisk.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "xy",
  "title": "Response code over time",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto", "placement": "outside", "position": "bottom", "layout": { "type": "list" } },
  "axis": {},
  "layers": [
    {
      "type": "area_percentage", <1>
      "x": {
        "operation": "date_histogram",
        "field": "timestamp"
      },
      "y": [
        {
          "operation": "count",
          "empty_as_null": false,
          "label": "Count of records",
          "format": { "type": "number", "decimals": 2 },
          "filter": { "expression": "" }
        }
      ],
      "breakdown_by": {
        "operation": "filters", <2>
        "filters": [
          {
            "filter": { "expression": "response.keyword >= 200 and response.keyword < 400" },
            "label": "Success/Redirection"
          },
          {
            "filter": { "expression": "response.keyword >= 400 and response.keyword < 500" },
            "label": "Client Error"
          },
          { "filter": { "expression": "response.keyword >= 500" }, "label": "Server Error" }
        ]
      },
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    },
    {
      "type": "annotations", <3>
      "ignore_global_filters": true,
      "events": [
        {
          "type": "query",
          "label": "Event",
          "query": { "language": "kql", "expression": "tags:error AND tags:security" },
          "time_field": "timestamp",
          "color": { "type": "static", "color": "#ee72a6" },
          "visible": true,
          "icon": "asterisk"
        }
      ],
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    }
  ],
  "styling": {
    "fitting": { "type": "none" },
    "areas": { "fill_opacity": 0.3 }
  }
}'
```

1. `area_percentage` normalizes each time bucket to 100% so you see the proportion of each response class, not absolute counts.
2. `filters` breakdown creates one area per KQL filter instead of splitting by field values.
3. The `annotations` layer marks events matching `tags:error AND tags:security` on the time axis with a pink asterisk.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::






     


