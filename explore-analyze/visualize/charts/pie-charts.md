---
navigation_title: Pie charts
applies_to:
  stack: ga
  serverless: ga
description: Create pie and donut charts to illustrate relative prevalence of categorical data and display proportional relationships.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Build pie charts with {{kib}}

Pie charts display parts of a whole as slices, where each slice represents a value and its size represents its prevalence. Pie charts are ideal for illustrating the relative prevalence of categorical data, and for displaying percentage or proportional data. They work best with a **maximum of 6 slices** and when proportions are around 25%, 50%, or 75%, as these are easiest to perceive accurately. For more than 6 categories, precise comparisons, or negative values, consider using [bar charts](bar-charts.md) instead. For comparing similarly-sized proportions or displaying percentages as discrete units, consider using [waffle charts](waffle-charts.md).

You can create pie charts in {{kib}} using [**Lens**](../lens.md).

![Example Lens pie chart](../../images/kibana-lens-pie-chart.png)

## Build a pie chart

:::{include} ../../_snippets/lens-prerequisites.md
:::

To build a pie chart:

::::::{stepper}

:::::{step} Access Lens
:::{include} ../../_snippets/access-lens.md
:::
:::::

:::::{step} Set the visualization to Pie
New visualizations often start as **Bar** charts.

Using the **Visualization type** dropdown, select **Pie**.
:::::

:::::{step} Define the data to show
1. Select the {{data-source}} that contains your data.
2. Configure the [**Slice by**](#slice-by-settings) dimension to define how the pie is divided into slices. Drag a categorical field to create slices based on its values.
3. Configure the [**Metric**](#metric-settings) dimension to define the size of each slice. This determines the numerical value that each slice represents. {{kib}} automatically selects an appropriate aggregation function compatible with the selected field.

Optionally:
   - Add additional **Slice by** dimensions to create nested slices (a multi-level or sunburst-style chart).
   - Enable [**Multiple metrics**](#multiple-metrics) in the layer settings to compare different measures within the same chart.

The chart preview updates to show a pie divided into slices. Each slice represents a category value, and its size reflects the metric proportion. If you added multiple **Slice by** dimensions, inner and outer rings appear to show the hierarchy.
:::::

:::::{step} Customize the chart to follow best practices
Tweak the appearance of the chart to your needs. Consider the following best practices:

**Limit the number of slices**
:   Keep your pie chart to a maximum of 6 slices. If you have more categories, consider [grouping smaller values into an "Other" category](#other-category) or using a different visualization type.

**Order slices meaningfully**
:   The largest slice should start at the 12 o'clock position and proceed clockwise in descending order. For categories with a natural order (such as satisfaction ratings), follow that order instead.

**Use color purposefully**
:   Apply colors to highlight important data or patterns. Use the [color mapping feature](../lens.md#assign-colors-to-terms) to assign consistent colors to key categories across your dashboards.

**Consider using a donut**
:   The empty center of donut charts provides space to display additional information, such as a total or key metric. Refer to [Create a donut chart](#donut-chart) for instructions.

**Label clearly**
:   Keep labels inside or close to slices when possible. For charts with many small slices or long labels, use the legend instead.

Refer to [Pie chart settings](#pie-chart-settings) to find all configuration options for your pie chart.

For panel sizing and layout guidance, refer to [Organize dashboard panels](../../dashboards/arrange-panels.md#dashboard-grid-layout).
:::::

:::::{step} Save the chart
:::{include} ../../_snippets/save-visualization.md
:::
:::::

::::::

## Advanced pie chart scenarios

### Create a donut chart [donut-chart]

Donut charts are pie charts with a hollow center. The empty space can provide a visual focal point and space for displaying related information.

1. Create a **Pie** chart visualization.
2. Configure your **Slice by** and **Metric** dimensions.
3. Select {icon}`brush` **Style**.
4. In **Appearance**, set **Donut hole** to **Small**, **Medium**, or **Large** depending on how much center space you want.

![Setting the donut hole size in Pie chart Style settings](/explore-analyze/images/pie-chart-donut.png "50%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example creates a donut chart sliced by the top 5 log tag values, with raw counts shown inside each slice.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "pie", <1>
  "title": "Logs per type",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "visible", "nested": false },
  "metrics": [{ "operation": "count", "empty_as_null": true }],
  "group_by": [
    {
      "operation": "terms",
      "fields": ["tags.keyword"],
      "limit": 5,
      "other_bucket": { "include_documents_without_field": false },
      "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" },
      "color": {
        "mode": "categorical",
        "palette": "default",
        "mapping": [ <2>
          { "values": ["success"], "color": { "type": "from_palette", "palette": "default", "index": 0 } },
          { "values": ["error"],   "color": { "type": "from_palette", "palette": "default", "index": 6 } },
          { "values": ["info"],    "color": { "type": "from_palette", "palette": "default", "index": 3 } },
          { "values": ["warning"], "color": { "type": "from_palette", "palette": "default", "index": 9 } },
          { "values": ["security"],"color": { "type": "from_palette", "palette": "default", "index": 4 } }
        ]
      }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "donut_hole": "m", <3>
    "labels": { "visible": true, "position": "inside" },
    "values": { "visible": true, "mode": "absolute" }
  }
}
```

1. `pie` creates a pie or donut chart. The `donut_hole` style setting controls the size of the center hole.
2. `color.mapping` pins each tag value to a specific palette index so colors stay consistent even when data changes.
3. `donut_hole: "m"` hollows out the center of the pie. Valid values are `"s"` (small), `"m"` (medium), and `"l"` (large).

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "pie", <1>
  "title": "Logs per type",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "visible", "nested": false },
  "metrics": [{ "operation": "count", "empty_as_null": true }],
  "group_by": [
    {
      "operation": "terms",
      "fields": ["tags.keyword"],
      "limit": 5,
      "other_bucket": { "include_documents_without_field": false },
      "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" },
      "color": {
        "mode": "categorical",
        "palette": "default",
        "mapping": [ <2>
          { "values": ["success"], "color": { "type": "from_palette", "palette": "default", "index": 0 } },
          { "values": ["error"],   "color": { "type": "from_palette", "palette": "default", "index": 6 } },
          { "values": ["info"],    "color": { "type": "from_palette", "palette": "default", "index": 3 } },
          { "values": ["warning"], "color": { "type": "from_palette", "palette": "default", "index": 9 } },
          { "values": ["security"],"color": { "type": "from_palette", "palette": "default", "index": 4 } }
        ]
      }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "donut_hole": "m", <3>
    "labels": { "visible": true, "position": "inside" },
    "values": { "visible": true, "mode": "absolute" }
  }
}'
```

1. `pie` creates a pie or donut chart. The `donut_hole` style setting controls the size of the center hole.
2. `color.mapping` pins each tag value to a specific palette index so colors stay consistent even when data changes.
3. `donut_hole: "m"` hollows out the center of the pie. Valid values are `"s"` (small), `"m"` (medium), and `"l"` (large).

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

### Compare multiple metrics in a pie chart [multiple-metrics]

By default, pie charts use a single metric with **Slice by** to split that metric by values in a categorical field. The **Multiple metrics** option lets you take a different approach: each slice represents a distinct metric you define, rather than values from your data.

This is useful when:

* You want to compare metrics that apply different filters to the same aggregation
* You need to show custom-defined categories that don't exist as values in a field
* You want to compare different calculations or formulas side by side

#### Example: Server resource consumption

This example uses the **Kibana Sample Data Logs** data set and groups requests by file extension to approximate resource usage: `.zip` files map to processing time, `.gz` files map to bandwidth, and `.rpm` files map to memory usage.

1. Create a **Pie** chart and remove any existing **Slice by** dimension.
2. Open the layer settings:
   * {applies_to}`serverless: ga` {applies_to}`stack: ga 9.3` Select {icon}`gear` **Settings**/**Layer settings**.
   * {applies_to}`stack: ga 9.0-9.2` Select {icon}`boxes_vertical`, then select **Layer settings**.
3. Select **Multiple metrics**, then close the layer settings menu.
4. Add metrics for each resource type:

   | Slice | Metric configuration | Filter |
   |-------|---------------------|--------|
   | Processing time | `Count of records` | `extension: zip` |
   | Bandwidth | `Count of records` | `extension: gz` |
   | Memory usage | `Count of records` | `extension: rpm` |

   For each metric, select the **Metric** dimension, set the function to **Count**, add a KQL filter in the **Advanced** section, and customize the **Name** to display meaningful labels.

5. Assign a custom color to each metric by selecting the metric and choosing a **Series color**.

![Pie chart with three slices showing different server resource metrics](/explore-analyze/images/pie-chart-multiple-metrics-example.png)

This example demonstrates the core value of multiple metrics: using KQL filters on each metric to compare distinct categories. Unlike **Slice by**, which splits a single metric by category values, multiple metrics lets you define completely custom groupings — even those that don't exist as a field in your data.

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example uses multiple metrics mode (no `group_by`) where each metric counts documents matching a specific file extension, with each metric assigned a static color.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "pie",
  "title": "Server resource consumption",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto", "nested": false },
  "metrics": [ <1>
    {
      "operation": "count",
      "empty_as_null": true,
      "label": "Processing time", <2>
      "filter": { "expression": "extension: zip", "language": "kql" },
      "color": { "type": "static", "color": "#eaae01" }
    },
    {
      "operation": "count",
      "empty_as_null": true,
      "label": "Bandwidth",
      "filter": { "expression": "extension: gz", "language": "kql" },
      "color": { "type": "static", "color": "#61a2ff" }
    },
    {
      "operation": "count",
      "empty_as_null": true,
      "label": "Memory usage",
      "filter": { "expression": "extension: rpm", "language": "kql" },
      "color": { "type": "static", "color": "#16c5c0" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "labels": { "visible": true, "position": "outside" },
    "values": { "visible": true, "mode": "percentage" }
  }
}
```

1. Three entries in `metrics` without a `group_by` activates multiple-metrics mode, where each metric becomes its own slice.
2. Each metric uses a `filter` to scope its count to a specific file extension, and a `color` with `type: "static"` to pin it to a specific hex color regardless of palette.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "pie",
  "title": "Server resource consumption",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto", "nested": false },
  "metrics": [ <1>
    {
      "operation": "count",
      "empty_as_null": true,
      "label": "Processing time", <2>
      "filter": { "expression": "extension: zip", "language": "kql" },
      "color": { "type": "static", "color": "#eaae01" }
    },
    {
      "operation": "count",
      "empty_as_null": true,
      "label": "Bandwidth",
      "filter": { "expression": "extension: gz", "language": "kql" },
      "color": { "type": "static", "color": "#61a2ff" }
    },
    {
      "operation": "count",
      "empty_as_null": true,
      "label": "Memory usage",
      "filter": { "expression": "extension: rpm", "language": "kql" },
      "color": { "type": "static", "color": "#16c5c0" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "labels": { "visible": true, "position": "outside" },
    "values": { "visible": true, "mode": "percentage" }
  }
}'
```

1. Three entries in `metrics` without a `group_by` activates multiple-metrics mode, where each metric becomes its own slice.
2. Each metric uses a `filter` to scope its count to a specific file extension, and a `color` with `type: "static"` to pin it to a specific hex color regardless of palette.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

### Group smaller values into a single slice [other-category]

When you have many categories with small values, you can group them into an "Other" category to simplify the visualization.

1. In the **Slice by** configuration, select the field.
2. Use **Top values** to limit the number of slices displayed.
3. Expand **Advanced**.
4. Enable **Group other values as "Other"** to combine remaining values into a single slice.

:::{tip}
Be careful when using "Other," as it could end up being the largest category, which might obscure the meaning of your chart. Consider whether a bar chart might be more appropriate for data with many categories.
:::

#### Example: Top hosts with remaining grouped as "Other"

This example uses the **Kibana Sample Data Logs** data set. If you haven't installed it yet, refer to [Sample data](/manage-data/ingest/sample-data.md) for instructions.

1. Create a **Pie** chart using the **Kibana Sample Data Logs** {{data-source}}.
2. In the **Slice by** dimension, select `host.keyword` with **Top values** set to **3**.
3. Expand **Advanced** and make sure that the **Group other values as "Other"** option is active.
4. Set the **Metric** to the **Count** function.

The resulting chart shows the 3 most common hosts, with all remaining hosts combined into a single "Other" slice. This keeps the chart readable while still accounting for the full data set.

![Pie chart showing top 3 hosts with remaining hosts grouped as Other](/explore-analyze/images/pie-chart-group-as-other.png)

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example shows the top 3 hosts as individual slices and groups all remaining hosts into an "Other" slice using the `other_bucket` option.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "pie",
  "title": "Top hosts with Other",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto", "nested": false },
  "metrics": [{ "operation": "count", "empty_as_null": true }],
  "group_by": [
    {
      "operation": "terms",
      "fields": ["host.keyword"],
      "limit": 3, <1>
      "other_bucket": { "include_documents_without_field": true } <2>
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "labels": { "visible": true, "position": "inside" },
    "values": { "visible": true, "mode": "percentage" }
  }
}
```

1. `limit: 3` limits the chart to the top 3 hosts by count.
2. `other_bucket` groups every remaining host into a single "Other" slice, including documents that lack the field entirely.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "pie",
  "title": "Top hosts with Other",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto", "nested": false },
  "metrics": [{ "operation": "count", "empty_as_null": true }],
  "group_by": [
    {
      "operation": "terms",
      "fields": ["host.keyword"],
      "limit": 3, <1>
      "other_bucket": { "include_documents_without_field": true } <2>
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "labels": { "visible": true, "position": "inside" },
    "values": { "visible": true, "mode": "percentage" }
  }
}'
```

1. `limit: 3` limits the chart to the top 3 hosts by count.
2. `other_bucket` groups every remaining host into a single "Other" slice, including documents that lack the field entirely.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

## Pie chart settings [pie-chart-settings]

Customize your pie chart to display exactly the information you need, formatted the way you want.

### Slice by settings [slice-by-settings]

The **Slice by** dimension defines how your pie is divided into segments. You can add up to 3 levels of slicing to create hierarchical visualizations.

**Data**
:   The **Slice by** dimension supports the following functions:

    - **Top values**: Create slices for the most common values in a field.
      - **Field**: Select the field to group by. You can add up to 4 fields to create multi-term slices. When multiple fields are selected, each slice represents a unique combination of values across those fields. You can reorder the fields by dragging them to change their priority.
      - **Number of values**: How many top values to display. The default number of values depends on your environment:
        - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Defaults to 9.
        - {applies_to}`stack: ga 9.0-9.3` Defaults to 5.
      :::{include} ../../_snippets/lens-rank-by-options.md
      :::
      - **Collapse by**: Aggregate values into a single number using `Sum`, `Average`, `Min`, or `Max`.
      :::{include} ../../_snippets/lens-breakdown-advanced-settings.md
      :::
    - **Date histogram**: Group data into time-based buckets (useful for showing time-based composition). Configure the time interval and how to handle date formatting.
      - **Field**: Select the date field to use for the time-based grouping.
      :::{include} ../../_snippets/lens-histogram-settings.md
      :::
      - **Collapse by**: Aggregate values into a single number using `Sum`, `Average`, `Min`, or `Max`.
    - **Intervals**: Create numeric ranges for continuous data. Useful for grouping numeric fields into buckets. You can define the interval granularity or specify custom ranges.
      - **Field**: Select the numeric field to create intervals from.
      - **Include empty rows**: Include intervals with no matching documents. On by default.
      - **Collapse by**: Aggregate values into a single number using `Sum`, `Average`, `Min`, or `Max`.
      :::{dropdown} How does interval granularity work?
      Interval granularity divides the field into evenly spaced intervals based on the minimum and maximum values for the field.
      
      The size of the interval is a "nice" value. When the granularity of the slider changes, the interval stays the same when the "nice" interval is the same. The minimum granularity is 1, and the maximum value is histogram:maxBars. To change the maximum granularity, go to Advanced settings.
      
      Intervals are incremented by 10, 5 or 2. For example, an interval can be `100` or `0.2`.
      :::
    - **Filters**: Define custom KQL filters to create specific slices. Each filter creates one slice in the chart.
      - **Collapse by**: Aggregate values into a single number using `Sum`, `Average`, `Min`, or `Max`.

**Appearance**
:   Configure slice-level options:
    - **Name**: Customize the legend label.
    - **Color mapping**: Select a color palette or assign specific colors to categories. Refer to [Assign colors to terms](../lens.md#assign-colors-to-terms) for details.

### Metric settings [metric-settings]

The **Metric** dimension defines the size of each slice.

**Data**
:   The main value that appears prominently in your chart. When you drag a field onto the chart, {{kib}} suggests a function based on the field type. You can change it and use aggregation functions like `Sum`, `Average`, `Count`, `Median`, and more, or create custom calculations with formulas. Refer to [](/explore-analyze/visualize/lens.md#lens-formulas) for examples, or to the {icon}`documentation` **Formula reference** available from Lens.

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
:   - **Name**: Customize the metric label displayed in tooltips and legends.
    - **Value format**: Control how numeric values are displayed (number, percent, bytes, and more).
    - **Series color**: When using multiple metrics without a **Slice by** dimension, use this option to assign a specific color to each metric.

### General layout [appearance-options]

When creating or editing a visualization, you can customize several appearance options from the {icon}`brush` **Style** or ![Legend icon](/explore-analyze/images/kibana-legend-icon.svg "") **Legend** menus.

#### Style settings

**Appearance**
:   Control the main visual aspects of the pie chart.

    **Donut hole**
    :   Transform your pie chart into a donut by adding a center hole:
        - **None**: Standard pie chart with no hole (default).
        - **Small**: Small center hole.
        - **Medium**: Medium center hole.
        - **Large**: Large center hole for emphasis or to display additional information.

**Titles and text**
:   Control slice labels and values.

    **Slice labels**
    :   Control how labels appear on the slices:
        - **Hide**: Do not display labels on slices.
        - **Inside**: Display labels inside the slices.
        - **Auto**: Automatically position labels for optimal readability (default).

    **Slice values**
    :   Control what values appear on the slices (when labels are visible):
        - **Hide**: Do not display values.
        - **Integer**: Display the raw numeric value.
        - **Percentage**: Display the percentage of the total.

          When displaying percentages, you can also configure the **Decimal places** (0-10) for precision.

#### Legend settings

Configure elements of your pie chart's legend:

**Visibility**
:   Specify whether to automatically show the legend or hide it:
    - **Auto**: Show the legend when there are multiple slices (default).
    - **Show**: Always show the legend.
    - **Hide**: Never show the legend.

**Nested**
:   When using multiple **Slice by** dimensions, enable this option to show the legend in a hierarchical format that reflects the slice hierarchy.

**Label truncation**
:   Choose whether to truncate long legend labels, and set a limit for how many lines to display.

**Width**
:   Set the width of the legend.

## Pie chart examples

<!-- MAINTENANCE: the API payload examples in this section were verified
against the Visualizations API spec. To re-verify after a schema change, run:
  KIBANA_URL=… API_KEY=… python3 .github/scripts/verify-lens-api-examples.py --file pie-charts.md
See .github/scripts/verify-lens-api-examples.py for full usage. -->

The following examples show various configuration options for building impactful pie charts.

**Website traffic by source**
:   Visualize the distribution of traffic sources to your website:

    * Example based on: Kibana Sample Data Logs
    * Configuration: [**Multiple metrics**](#multiple-metrics)
    * **Metrics**: 4 metrics based on formulas
        * `count(kql='referer : *elastic*')`, named "Elastic website"
        * `count(kql='referer : *twitter*')`, named "Twitter/X"
        * `count(kql='referer : *facebook*')`, named "Facebook"
        * `count(kql='referer : *nytimes*')`, named "NY Times"
    * **Style**: Donut with medium hole
    * **Legend**: Show

![Donut chart with traffic by sources](/explore-analyze/images/pie-chart-example-traffic-by-source.png "=60%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example uses formula-based metrics to count visits from specific referrer domains, producing one slice per traffic source without a `group_by` dimension.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "pie",
  "title": "Website traffic by source",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "visible", "nested": false },
  "metrics": [
    {
      "operation": "formula", <1>
      "formula": "count(kql='referer : *elastic*')", <2>
      "label": "Elastic website",
      "color": { "type": "auto" }
    },
    {
      "operation": "formula",
      "formula": "count(kql='referer : *facebook*')",
      "label": "Facebook",
      "color": { "type": "auto" }
    },
    {
      "operation": "formula",
      "formula": "count(kql='referer:*twitter*')",
      "label": "Twitter/X",
      "color": { "type": "auto" }
    },
    {
      "operation": "formula",
      "formula": "count(kql='referer : *nytimes*')",
      "label": "NY Times",
      "color": { "type": "auto" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "donut_hole": "m",
    "labels": { "visible": true, "position": "outside" },
    "values": { "visible": true, "mode": "percentage" }
  }
}
```

1. `formula` lets each metric apply its own KQL filter, creating slices that represent custom-defined categories.
2. The `kql` parameter inside `count()` filters documents to only those whose `referer` field matches the given pattern.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "pie",
  "title": "Website traffic by source",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "visible", "nested": false },
  "metrics": [
    {
      "operation": "formula", <1>
      "formula": "count(kql='referer : *elastic*')", <2>
      "label": "Elastic website",
      "color": { "type": "auto" }
    },
    {
      "operation": "formula",
      "formula": "count(kql='referer : *facebook*')",
      "label": "Facebook",
      "color": { "type": "auto" }
    },
    {
      "operation": "formula",
      "formula": "count(kql='referer:*twitter*')",
      "label": "Twitter/X",
      "color": { "type": "auto" }
    },
    {
      "operation": "formula",
      "formula": "count(kql='referer : *nytimes*')",
      "label": "NY Times",
      "color": { "type": "auto" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "donut_hole": "m",
    "labels": { "visible": true, "position": "outside" },
    "values": { "visible": true, "mode": "percentage" }
  }
}'
```

1. `formula` lets each metric apply its own KQL filter, creating slices that represent custom-defined categories.
2. The `kql` parameter inside `count()` filters documents to only those whose `referer` field matches the given pattern.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

**Revenue distribution by product category**
:   Show how revenue is distributed across product categories:

    * Example based on: Kibana Sample Data eCommerce
    * **Slice by**: `category.keyword` (Top values, 6)
    * **Metric**: Sum of `taxful_total_price`
    * **Style**: Pie (no donut hole)

![Pie chart with revenue by product category](/explore-analyze/images/pie-chart-example-revenue-by-product-category.png "=60%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example creates a pie chart that sums revenue per product category from the eCommerce sample data, showing each category's share of total revenue.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "pie",
  "title": "Revenue distribution by product category",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto", "nested": false },
  "metrics": [
    {
      "operation": "sum", <1>
      "field": "taxful_total_price",
      "empty_as_null": true
    }
  ],
  "group_by": [
    {
      "operation": "terms",
      "fields": ["category.keyword"], <2>
      "limit": 6,
      "other_bucket": { "include_documents_without_field": false },
      "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" },
      "color": { "mode": "categorical", "palette": "default", "mapping": [] }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_ecommerce",
    "time_field": "order_date"
  },
  "styling": {
    "labels": { "visible": true, "position": "outside" },
    "values": { "visible": true, "mode": "percentage" }
  }
}
```

1. `sum` on `taxful_total_price` sizes each slice by total revenue rather than document count.
2. `category.keyword` splits the pie by product category, with each of the top 6 categories becoming its own slice.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "pie",
  "title": "Revenue distribution by product category",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto", "nested": false },
  "metrics": [
    {
      "operation": "sum", <1>
      "field": "taxful_total_price",
      "empty_as_null": true
    }
  ],
  "group_by": [
    {
      "operation": "terms",
      "fields": ["category.keyword"], <2>
      "limit": 6,
      "other_bucket": { "include_documents_without_field": false },
      "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" },
      "color": { "mode": "categorical", "palette": "default", "mapping": [] }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_ecommerce",
    "time_field": "order_date"
  },
  "styling": {
    "labels": { "visible": true, "position": "outside" },
    "values": { "visible": true, "mode": "percentage" }
  }
}'
```

1. `sum` on `taxful_total_price` sizes each slice by total revenue rather than document count.
2. `category.keyword` splits the pie by product category, with each of the top 6 categories becoming its own slice.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

**Error distribution by type**
:   Display the proportion of different error types in your application:

    * Example based on: Kibana Sample Data Logs
    * **Slice by**: `error.type` using **Filters**:
      - "Client Error": `response.keyword >= "400" AND response.keyword < "500"`
      - "Server Error": `response.keyword >= "500"`
      - "Success": `response.keyword >= "200" AND response.keyword < "400"`
    * **Metric**: `Count of records`
    * **Style**: Donut with large hole
    * **Color mapping**: Red for client errors, yellow for server errors, green for success

![Donut chart with distribution of errors by type](/explore-analyze/images/pie-chart-example-response-distribution.png "=60%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example uses the `filters` grouping operation to define custom slices based on HTTP response code ranges, rather than relying on field values directly.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "pie",
  "title": "Error distribution by type",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto", "nested": false },
  "metrics": [
    {
      "operation": "count",
      "empty_as_null": true
    }
  ],
  "group_by": [
    {
      "operation": "filters", <1>
      "filters": [
        {
          "filter": { "expression": "response.keyword >= \"400\" AND response.keyword < \"500\"" },
          "label": "Client Error"
        },
        { "filter": { "expression": "response.keyword >= \"500\"" }, "label": "Server Error" },
        {
          "filter": { "expression": "response.keyword >= \"200\" AND response.keyword < \"400\"" },
          "label": "Success"
        }
      ],
      "color": {
        "mode": "categorical",
        "palette": "default",
        "mapping": [
          { "values": ["Client Error"], "color": { "type": "color_code", "value": "#CC5642" } },
          { "values": ["Server Error"], "color": { "type": "color_code", "value": "#D6BF57" } },
          { "values": ["Success"],      "color": { "type": "color_code", "value": "#209280" } }
        ]
      }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "donut_hole": "l",
    "labels": { "visible": true, "position": "inside" },
    "values": { "visible": true, "mode": "percentage" }
  }
}
```

1. `filters` creates one slice per KQL query, letting you define arbitrary categories such as "Client Error" (4xx), "Server Error" (5xx), and "Success" (2xx/3xx). The `color` mapping assigns explicit hex colors to each category — red for client errors, yellow for server errors, green for success.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "pie",
  "title": "Error distribution by type",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto", "nested": false },
  "metrics": [
    {
      "operation": "count",
      "empty_as_null": true
    }
  ],
  "group_by": [
    {
      "operation": "filters", <1>
      "filters": [
        {
          "filter": { "expression": "response.keyword >= \"400\" AND response.keyword < \"500\"" },
          "label": "Client Error"
        },
        { "filter": { "expression": "response.keyword >= \"500\"" }, "label": "Server Error" },
        {
          "filter": { "expression": "response.keyword >= \"200\" AND response.keyword < \"400\"" },
          "label": "Success"
        }
      ],
      "color": {
        "mode": "categorical",
        "palette": "default",
        "mapping": [
          { "values": ["Client Error"], "color": { "type": "color_code", "value": "#CC5642" } },
          { "values": ["Server Error"], "color": { "type": "color_code", "value": "#D6BF57" } },
          { "values": ["Success"],      "color": { "type": "color_code", "value": "#209280" } }
        ]
      }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "donut_hole": "l",
    "labels": { "visible": true, "position": "inside" },
    "values": { "visible": true, "mode": "percentage" }
  }
}'
```

1. `filters` creates one slice per KQL query, letting you define arbitrary categories such as "Client Error" (4xx), "Server Error" (5xx), and "Success" (2xx/3xx). The `color` mapping assigns explicit hex colors to each category — red for client errors, yellow for server errors, green for success.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::
