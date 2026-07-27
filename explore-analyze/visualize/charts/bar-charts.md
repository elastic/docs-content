---
navigation_title: Bar charts
applies_to:
  stack: ga
  serverless: ga
description: Create bar charts to compare values across categories, display distributions, and show rankings side by side.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Build bar charts with {{kib}}

Bar charts are one of the most versatile and widely used visualizations for comparing values across categories. They're perfect for showing distributions, rankings, and comparisons, making complex data understandable at a glance.

They work with any type of data: numeric values, counts, averages, or calculations. You can compare sales by region, track errors by service, analyze user engagement by feature, or rank products by revenue. Using bar charts, you can display data horizontally or vertically, stacked to show part-to-whole relationships, or grouped to compare multiple metrics side by side.

You can create bar charts in {{kib}} using [**Lens**](../lens.md).

![Bar chart showing sales by category with different layouts](../../images/stacked-bar-chart.png)

## Build a bar chart

:::{include} ../../_snippets/lens-prerequisites.md
:::

To build a bar chart:

:::::{stepper}

::::{step} Access Lens
:::{include} ../../_snippets/access-lens.md
:::
::::

::::{step} Set the visualization to Bar
Make sure that the visualization type is set to **Bar**.

::::

::::{step} Define the data to show
1. Select the {{data-source}} that contains your data.
2. Set the **Horizontal axis** to define categories for your data. This is typically a dimension like a category field, date histogram, or terms aggregation. This setting creates the individual bars.
3. Set the **Vertical axis** to define the numerical values or quantities being measured. They're what determine the height or length of your bars. 
4. Optionally:
    - Add a [**Break down by**](#breakdown-options) dimension to split each bar into segments, creating stacked or grouped bar charts.
    - Add multiple metrics to compare different measures side by side.
    - Add layers to your chart to integrate additional visualizations, [annotations](../lens.md#add-annotations), or a [reference line](../lens.md#add-reference-lines).
    - Configure the axis settings to customize scale, labels, and gridlines.

The chart preview updates to show bars representing your data. If you added a breakdown dimension, bars are segmented or grouped by category.

Refer to [](#settings) for all data configuration options for your bar chart.
::::

::::{step} Customize the chart to follow best practices
Tweak the appearance of the chart to your needs. Consider the following best practices:

**Select appropriate orientation**
:   Use vertical bars for time-based data and horizontal bars when category labels are long or you have many categories to display.

**Use color strategically**
:   Apply colors to distinguish between categories or highlight important values. Use consistent color schemes across related dashboards.

**Keep it focused**
:   Avoid cluttering with too many bars or categories. If you have more than 10-15 categories, consider filtering to show top values or using a different visualization type.

**Label clearly**
:   Use descriptive axis labels and titles. Add value labels when exact numbers are important.

**Sort meaningfully**
:   Sort bars by value (ascending or descending) to make comparisons easier, or keep them in alphabetical/chronological order when the sequence matters.

Refer to [](#settings) for a complete list of options.

For panel sizing and layout guidance, refer to [Organize dashboard panels](../../dashboards/arrange-panels.md#dashboard-grid-layout).
::::

::::{step} Save the chart
:::{include} ../../_snippets/save-visualization.md
:::
::::

:::::

## Advanced bar chart scenarios

### Create stacked bar charts [stacked-bars]

Stacked bar charts show how different components contribute to a total value. Each bar is divided into colored segments representing different categories, allowing you to view both the total and the breakdown.

Stacked bar charts work best when:
- You want to show part-to-whole relationships
- The total value is meaningful
- You have 2-7 segments per bar, more can become hard to read
- The segments don't vary wildly in size

To create a stacked bar chart:

1. Create a **Bar** visualization and set it to **Stacked**.
   :::{tip}
   You can also set it to **Percentage** for a stacked display but as percentages of the total instead, allowing you to compare proportions even when absolute values differ greatly.
   :::
2. Add the main metric you want to visualize to the vertical axis.
3. Add a dimension to the horizontal axis to create the bars.
4. Add a dimension to **Break down by** to split each bar into stacked segments, recognizable with varying colors.

![Bar chart with stacking](../../images/stacked-bar-chart.png "=70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: "ga 9.5+, preview =9.4", serverless: ga }

This example creates a stacked bar chart that counts log entries over time and breaks them down by HTTP response code.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "xy",
  "title": "Stacked bar chart",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "visible", "placement": "outside", "position": "right" },
  "axis": {},
  "layers": [
    {
      "type": "bar_stacked", <1>
      "x": { "operation": "date_histogram", "field": "timestamp" },
      "y": [
        {
          "operation": "count",
          "empty_as_null": true,
          "format": { "type": "number" }
        }
      ],
      "breakdown_by": { <2>
        "operation": "terms",
        "fields": ["response.keyword"],
        "limit": 3,
        "other_bucket": { "include_documents_without_field": false }, <3>
        "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" }
      },
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    }
  ],
  "styling": {
    "fitting": { "type": "none" }
  }
}
```

1. `bar_stacked` renders bars with colored segments stacked on top of each other, showing both the total and the contribution of each category.
2. `breakdown_by` splits each bar into segments by the top 3 HTTP response codes, ranked by document count.
3. `other_bucket` groups any remaining response codes beyond the top 3 into an **Other** segment.

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
  "title": "Stacked bar chart",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "visible", "placement": "outside", "position": "right" },
  "axis": {},
  "layers": [
    {
      "type": "bar_stacked", <1>
      "x": { "operation": "date_histogram", "field": "timestamp" },
      "y": [
        {
          "operation": "count",
          "empty_as_null": true,
          "format": { "type": "number" }
        }
      ],
      "breakdown_by": { <2>
        "operation": "terms",
        "fields": ["response.keyword"],
        "limit": 3,
        "other_bucket": { "include_documents_without_field": false }, <3>
        "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" }
      },
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    }
  ],
  "styling": {
    "fitting": { "type": "none" }
  }
}'
```

1. `bar_stacked` renders bars with colored segments stacked on top of each other, showing both the total and the contribution of each category.
2. `breakdown_by` splits each bar into segments by the top 3 HTTP response codes, ranked by document count.
3. `other_bucket` groups any remaining response codes beyond the top 3 into an **Other** segment.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

### Create unstacked (side-by-side) bar charts [grouped-bars]

Unstacked bar charts display multiple bars side by side for each category, allowing you to compare different metrics or time periods.

Use unstacked bar charts when:
- You need to compare 2-4 metrics across categories
- Direct comparison between metrics is more important than viewing totals
- The metrics have similar scales

To create an unstacked bar chart:

1. Create a **Bar** chart visualization and set it to **Unstacked**
2. Add the main metric you want to visualize to the vertical axis.
3. Add a dimension to the horizontal axis.
4. Add a dimension to **Break down by** to split each bar into different bars that show next to each other, recognizable with varying colors.

![Bar chart without stacking showing breakdown](../../images/unstacked-bar-chart.png "=70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: "ga 9.5+, preview =9.4", serverless: ga }

This example creates an unstacked bar chart where each breakdown category renders as a separate bar placed side by side, making individual values straightforward to compare.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "xy",
  "title": "Unstacked bar chart",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "visible", "placement": "outside", "position": "right" },
  "axis": {},
  "layers": [
    {
      "type": "bar", <1>
      "x": { "operation": "date_histogram", "field": "timestamp" },
      "y": [
        {
          "operation": "count",
          "empty_as_null": true,
          "format": { "type": "number" }
        }
      ],
      "breakdown_by": { <2>
        "operation": "terms",
        "fields": ["response.keyword"],
        "limit": 3,
        "other_bucket": { "include_documents_without_field": false },
        "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" }
      },
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    }
  ],
  "styling": {
    "fitting": { "type": "none" }
  }
}
```

1. `bar` (instead of `bar_stacked`) places each category's bar side by side for direct comparison.
2. `breakdown_by` creates a separate bar for each of the top 3 HTTP response codes within every time bucket.

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
  "title": "Unstacked bar chart",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "visible", "placement": "outside", "position": "right" },
  "axis": {},
  "layers": [
    {
      "type": "bar", <1>
      "x": { "operation": "date_histogram", "field": "timestamp" },
      "y": [
        {
          "operation": "count",
          "empty_as_null": true,
          "format": { "type": "number" }
        }
      ],
      "breakdown_by": { <2>
        "operation": "terms",
        "fields": ["response.keyword"],
        "limit": 3,
        "other_bucket": { "include_documents_without_field": false },
        "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" }
      },
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    }
  ],
  "styling": {
    "fitting": { "type": "none" }
  }
}'
```

1. `bar` (instead of `bar_stacked`) places each category's bar side by side for direct comparison.
2. `breakdown_by` creates a separate bar for each of the top 3 HTTP response codes within every time bucket.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

## Bar chart settings [settings]

Customize your bar chart to display exactly the information you need, formatted the way you want.

### Horizontal axis settings [horizontal-axis-options]

**Data**
:   The dimension that creates your individual bars. It supports the following functions:

    :::{include} ../../_snippets/lens-bucket-top-values.md
    :::
      :::{include} ../../_snippets/lens-rank-by-options.md
      :::
      :::{include} ../../_snippets/lens-breakdown-advanced-settings.md
      :::
    :::{include} ../../_snippets/lens-bucket-date-histogram.md
    :::
      :::{include} ../../_snippets/lens-histogram-settings.md
      :::
    :::{include} ../../_snippets/lens-bucket-intervals.md
    :::
    :::{include} ../../_snippets/lens-bucket-filters.md
    :::

**Appearance**
:   Define the formatting of the horizontal axis, including:
    - **Name**: Customize the axis label to describe what the bars represent.
    - **Value format**: Select to display values as number, percent, bytes, bits, duration, or with a custom format.

### Vertical axis settings [vertical-axis-options]

**Data**
:   The metric that determines the height of your bars. When you drag a field onto the vertical axis, {{kib}} suggests a function based on the field type. You can change it and use aggregation functions like `Sum`, `Average`, `Count`, `Median`, `Min`, `Max`, and more, or create custom calculations with formulas. Refer to [](/explore-analyze/visualize/lens.md#lens-formulas) for examples, or to the {icon}`documentation` **Formula reference** available from Lens.

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
:   Define the formatting of the vertical axis, including:
    - **Name**: By default, the chart uses the function or formula as the axis label. It's a best practice to customize this with a meaningful title.
    - **Value format**: Select to display values as number, percent, bytes, bits, duration, or with a custom format.
    - **Series color**: Assign a specific color to bars. This option isn't available when the **Breakdown** option is defined for the chart, because it's the color mapping of that option that is then taken into account.
    - **Axis side**: Choose to display the vertical axis on the left or right side of the graph. By default, the axis displays on the left. 

### Breakdown settings [breakdown-options]

**Data**
:   Split your bars into segments or groups based on another dimension. Each unique value creates its own segment or bar, allowing you to show composition or compare metrics across multiple dimensions. It supports the following functions:

    :::{include} ../../_snippets/lens-bucket-top-values.md
    :::
      :::{include} ../../_snippets/lens-rank-by-options.md
      :::
      :::{include} ../../_snippets/lens-breakdown-advanced-settings.md
      :::
    :::{include} ../../_snippets/lens-bucket-date-histogram.md
    :::
      :::{include} ../../_snippets/lens-histogram-settings.md
      :::
    :::{include} ../../_snippets/lens-bucket-intervals.md
    :::
    :::{include} ../../_snippets/lens-bucket-filters.md
    :::

    :::{include} ../../_snippets/lens-collapse-by.md
    :::

**Appearance**
:   Define the formatting of the breakdown, including:
    - **Name**: Customize the legend label.
    - **Value format**: Select to display values as number, percent, bytes, bits, duration, or with a custom format.
    - **Color mapping**: Select a color palette or assign specific colors to categories.

### General layout [appearance-options]

When creating or editing a visualization, you can customize several appearance options from the {icon}`brush` **Style** or ![Legend icon](/explore-analyze/images/kibana-legend-icon.svg "") **Legend** menus.

#### Style settings

**Appearance**
:   Select the bar orientation. It can be **Horizontal** or **Vertical**.

**Titles and text**
:    Specify to hide or show bar values on bar charts:
    - **Hide**: Removes the numeric value from the bars entirely. Only the bar height represents the magnitude. 
    - **Show, if able**: Attempts to draw the value inside each bar, but the label will only render when there’s enough vertical space to keep text legible; crowded bars will not have labels. 
    
    Your selection applies to the entire chart layer, so you can turn labels on for quick KPI-style charts or keep them off for dense histograms.

**Left axis**
:   Left-axis controls for Lens bar charts let you tune how the vertical scale looks and behaves. Key options are:
    - **Title**: Set the label that appears under the axis (for example, "Date"). You can hide the label entirely if the layout is tight. 
    - **Gridlines**: Toggles vertical guide lines across the chart, which help compare bar positions against the axis scale.
    - **Tick labels**: Show or hide the textual values beneath the ticks. When visible, the orientation picker lets you rotate them (horizontal, angled, vertical) to avoid overlap on dense timelines.
    - **Orientation**: Set the placement of the axis title. It can be **Horizontal**, **Vertical**, or **Angled**.
    - **Axis scale**: Select linear (default), log, or square-root scaling.
    - **Bounds & rounding**: Manually clamp the axis to a min/max or let Lens round to nice intervals. For numeric histograms this also controls whether “nice” bucket labels are used.

    :::{note}
    **Left axis** and **Bottom axis** options can interchange depending on the orientation you selected for the bar chart.
    :::

**Bottom axis**
:   Bottom-axis controls for Lens bar charts let you tune how the horizontal scale looks and behaves. Key options are:
    - **Title**: Set the label that appears under the axis (for example, "Date"). You can hide the label entirely if the layout is tight. 
    - **Gridlines**: Toggles vertical guide lines across the chart, which help compare bar positions against the axis scale.
    - **Tick labels**: Show or hide the textual values beneath the ticks. When visible, the orientation picker lets you rotate them (horizontal, angled, vertical) to avoid overlap on dense timelines.
    - **Show partial data markers**: Highlights buckets at the edges of the time range that only contain partial data—useful for time-based bar charts so viewers know the first/last bucket might be incomplete.
    - **Show current time marker**: Draws a vertical marker for “now” on time charts, so you can see how recent the latest bar is.


#### Legend settings

:::{include} ../../_snippets/xy-chart-legend-settings.md
:::

## Bar chart examples

<!-- MAINTENANCE: the API payload examples in this section were verified
against the Visualizations API spec. To re-verify after a schema change, run:
  KIBANA_URL=… API_KEY=… python3 .github/scripts/verify-lens-api-examples.py --file bar-charts.md
See .github/scripts/verify-lens-api-examples.py for full usage. -->

The following examples show various configuration options that you can use for building impactful bar charts.


**Weekly website traffic per region**
:   Track website visits over time, broken down by traffic source:

    * **Title**: "Weekly website traffic per region"
    * **Vertical axis**: `count()`
      * **Name**: "Page Views"
      * **Value format**: `Number`
    * **Horizontal axis**: `date_histogram(timestamp, interval='1w')`
      * **Name**: "Week"
    * **Break down by**: `geo.dest`
      * **Number of values**: `9`
    * **Layout**: `Stacked`
    * **Legend**: Right side, showing regions

![Stacked bar chart showing traffic per week broken down per region](/explore-analyze/images/weekly-website-traffic-per-region.png "=70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: "ga 9.5+, preview =9.4", serverless: ga }

This example creates a stacked bar chart that tracks page views over time with a custom metric label and breaks them down by the top 9 destination regions.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "xy",
  "title": "Weekly website traffic per region",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto" },
  "axis": {},
  "layers": [
    {
      "type": "bar_stacked",
      "x": { "operation": "date_histogram", "field": "timestamp", "suggested_interval": "1w" }, <1>
      "y": [
        {
          "operation": "count",
          "label": "Page Views", <2>
          "format": { "type": "number" },
          "filter": { "expression": "" }
        }
      ],
      "breakdown_by": {
        "operation": "terms",
        "fields": ["geo.dest"],
        "limit": 9, <3>
        "other_bucket": { "include_documents_without_field": false }, <4>
        "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" }
      },
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    }
  ],
  "styling": { "fitting": { "type": "none" } }
}
```

1. `suggested_interval: "1w"` sets each bar to represent one week of data.
2. `label` overrides the default axis label so the vertical axis reads "Page Views" instead of "Count."
3. `limit: 9` shows the top 9 regions, giving a broader geographic breakdown than the default 5.
4. `other_bucket` groups remaining regions into an **Other** segment so the total is always accounted for.

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
  "title": "Weekly website traffic per region",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto" },
  "axis": {},
  "layers": [
    {
      "type": "bar_stacked",
      "x": { "operation": "date_histogram", "field": "timestamp", "suggested_interval": "1w" }, <1>
      "y": [
        {
          "operation": "count",
          "label": "Page Views", <2>
          "format": { "type": "number" },
          "filter": { "expression": "" }
        }
      ],
      "breakdown_by": {
        "operation": "terms",
        "fields": ["geo.dest"],
        "limit": 9, <3>
        "other_bucket": { "include_documents_without_field": false }, <4>
        "rank_by": { "type": "metric", "metric_index": 0, "direction": "desc" }
      },
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    }
  ],
  "styling": { "fitting": { "type": "none" } }
}'
```

1. `suggested_interval: "1w"` sets each bar to represent one week of data.
2. `label` overrides the default axis label so the vertical axis reads "Page Views" instead of "Count."
3. `limit: 9` shows the top 9 regions, giving a broader geographic breakdown than the default 5.
4. `other_bucket` groups remaining regions into an **Other** segment so the total is always accounted for.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

**Request error rate per host (with threshold)**
:   Monitor error rates across hosts with a target threshold line:

    * **Title**: "Request error rate per host"
    * **Vertical axis**: `count(kql='response.keyword > "300"') / count()`
      * **Name**: "Error rate"
      * **Value format**: `Percent`
    * **Horizontal axis**: `terms(service.name)`
      * **Name**: "Hosts"
      * **Number of values**: `4`
      * **Rank by**: Alphabetical
    * **Reference line**: Value `0,10` (10% threshold)
      * **Label**: "Maximum acceptable error rate"
      * **Color**: Red, dashed line
    * **Layout**: Horizontal orientation (for better service name readability)

![Bar chart with reference line showing traffic per week broken down per region](/explore-analyze/images/request-error-rate-per-host.png "=70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: "ga 9.5+, preview =9.4", serverless: ga }

This example creates a horizontal bar chart with a formula-based metric and a reference line layer that marks the acceptable error threshold.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "xy",
  "title": "Request error rate per host",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto" },
  "axis": {},
  "layers": [
    {
      "type": "bar_horizontal", <1>
      "x": {
        "operation": "terms",
        "fields": ["host.keyword"],
        "limit": 4,
        "label": "Hosts",
        "rank_by": { "type": "alphabetical", "direction": "asc" } <2>
      },
      "y": [
        {
          "operation": "formula", <3>
          "formula": "count(kql='response.keyword > \"300\"') / count()",
          "label": "Error rate",
          "format": { "type": "percent" },
          "filter": { "expression": "" }
        }
      ],
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    },
    {
      "type": "reference_lines", <4>
      "thresholds": [
        {
          "operation": "static_value",
          "value": 0.1,
          "format": { "type": "percent" },
          "label": "Maximum acceptable error rate",
          "color": { "type": "static", "color": "#BD271E" },
          "stroke_dash": "dashed",
          "text": { "visible": true }
        }
      ],
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    }
  ],
  "styling": { "fitting": { "type": "none" } }
}
```

1. `bar_horizontal` renders bars horizontally, giving more room for long host names.
2. `rank_by: "alphabetical"` sorts the hosts alphabetically so the order is consistent regardless of error rate.
3. `formula` computes the error rate as the ratio of responses above 300 to total requests. `response.keyword` is stored as a string in the sample data.
4. A `reference_lines` layer draws a threshold at 10% so hosts exceeding it are immediately visible. `stroke_dash: "dashed"` and `color` mark it red and dashed. `text.visible: true` displays the label on the line.

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
  "title": "Request error rate per host",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto" },
  "axis": {},
  "layers": [
    {
      "type": "bar_horizontal", <1>
      "x": {
        "operation": "terms",
        "fields": ["host.keyword"],
        "limit": 4,
        "label": "Hosts",
        "rank_by": { "type": "alphabetical", "direction": "asc" } <2>
      },
      "y": [
        {
          "operation": "formula", <3>
          "formula": "count(kql='response.keyword > \"300\"') / count()",
          "label": "Error rate",
          "format": { "type": "percent" },
          "filter": { "expression": "" }
        }
      ],
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    },
    {
      "type": "reference_lines", <4>
      "thresholds": [
        {
          "operation": "static_value",
          "value": 0.1,
          "format": { "type": "percent" },
          "label": "Maximum acceptable error rate",
          "color": { "type": "static", "color": "#BD271E" },
          "stroke_dash": "dashed",
          "text": { "visible": true }
        }
      ],
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    }
  ],
  "styling": { "fitting": { "type": "none" } }
}'
```

1. `bar_horizontal` renders bars horizontally, giving more room for long host names.
2. `rank_by: "alphabetical"` sorts the hosts alphabetically so the order is consistent regardless of error rate.
3. `formula` computes the error rate as the ratio of responses above 300 to total requests. `response.keyword` is stored as a string in the sample data.
4. A `reference_lines` layer draws a threshold at 10% so hosts exceeding it are immediately visible. `stroke_dash: "dashed"` and `color` mark it red and dashed. `text.visible: true` displays the label on the line.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::
