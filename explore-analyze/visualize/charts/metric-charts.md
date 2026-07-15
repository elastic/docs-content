---
navigation_title: Metric charts
applies_to:
  stack: ga
  serverless: ga
description: Create metric charts to highlight important KPIs with dynamic coloring and trend indicators on dashboards.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Build metric charts with {{kib}} [build-metric-charts-with-kibana]

Metric charts make important single values stand out on a dashboard. They're perfect for highlighting KPIs such as error rates or SLOs, and for making them understandable at a glance with dynamic coloring or trend indicators.

They work with any numeric data: plain numbers, percentages, or calculations like a count, sum, or average. You can get this numeric data from numeric fields stored in your {{es}} documents, or from aggregation functions and formulas that you can apply to any type of field. <br>
You can also display strings by using the `Last value` aggregation function that picks up the last document, sorted by timestamp, in the current time frame.


You can create metric charts in {{kib}} using [**Lens**](../lens.md).

![Metric chart representing an SLO with different layouts](../../images/metric-chart.png)

## Build a metric chart

:::{include} ../../_snippets/lens-prerequisites.md
:::

To build a metric chart:

:::::{stepper}

::::{step} Access Lens
:::{include} ../../_snippets/access-lens.md
:::
::::

::::{step} Set the visualization to Metric
New visualizations default to creating **Bar** charts. 

Using the dropdown indicating **Bar**, select **Metric**.
::::

::::{step} Define the data to show
1. Select the {{data-source}} that contains your data.
2. Define the **Primary metric** by dragging a field from the fields list to the chart. {{kib}} automatically selects an appropriate aggregation function like Sum, Average, or Count based on the field type. This is the only setting that your metric chart requires to display something.
3. Optionally:
    - Add a [secondary metric](#secondary-metric-options). You can use this secondary metric as a comparison value or as a trend indicator to show how the primary metric evolves over time.
    - Specify a [maximum value](#max-value-options).
    - [Break down](#breakdown-options) the metric into multiple tiles based on another dimension. 

The chart preview updates to show a large numeric value. If you added a secondary metric, it appears below the primary value. If you added a breakdown dimension, separate tiles appear for each category.

See [](#settings) for all data configuration options for your metric chart.
::::

::::{step} Customize the chart to follow best practices
Tweak the appearance of the chart to your needs. Consider the following best practices:

**Use color wisely**
:   Assign colors that match your users' expectations and consider your specific context.

**Format for readability**
:   Round to an appropriate precision. Showing 1.2M is clearer than 1,234,567.89 for high-level metrics, but use more precision when small changes matter.

**Provide context**
:   Use titles and subtitles to explain what the metric shows. "45,234" is a number, but "Active Users" as a title gives it meaning, and "Last 24 hours" as a subtitle makes it unambiguous.

Refer to [](#settings) for a complete list of options.

For panel sizing and layout guidance, refer to [Organize dashboard panels](../../dashboards/arrange-panels.md#dashboard-grid-layout).
::::

::::{step} Save the chart
:::{include} ../../_snippets/save-visualization.md
:::
::::

:::::

## Advanced metric scenarios

### Show trends in Metric charts [metric-trends]
```{applies_to}
stack: ga 9.1
serverless: ga
```

When creating **Metric** visualizations with numeric data, you can add trend indicators that compare your primary metric to a secondary value. This feature displays colored badges with directional arrows to help you quickly identify whether values are increasing, decreasing, or staying the same.

| Without trend | With trend |
|--------|-------|
| ![Secondary metric before comparison](../../images/secondary_metric_before_compare.png "title =70%") | ![Secondary metric after comparison](../../images/secondary_metric_after_compare.png "title =70%") |

To add trend indicators to your metric visualization:

1. Create a **Metric** visualization with a numeric primary metric.
2. Add a secondary metric that represents the comparison value.

    ::::{tip}
    Use the `shift` parameter in formulas to compare current values against historical data. For example, if your primary metric is counting orders (based on an `order_id` field) for the current week, you can use the `count(order_id, shift='1w')` formula to compare this week's count of orders to last week's count.
    ::::

3. In the secondary metric configuration, look for the **Color by value** option. The possible choices are:
   * **None**: No trend indicators (default)
   * **Static**: Shows the secondary metric as a badge with a fixed color that you select
   * **Dynamic**: Enables both color coding and directional icons based on the comparison

4. Select **Dynamic** coloring. More options appear.

   ![Dynamic coloring options for secondary metrics](../../images/metric-secondary-dynamic-coloring.png "=70%")

5. Choose a **Color palette** that matches how you'd like to represent the comparison.

6. Configure the **Display** option:
   * **Icon**: Shows only directional arrows: ↑ for increase, ↓ for decrease, = for no change
   * **Value**: Shows only the secondary metric value
   * **Both**: Shows both the icon and value (default)

7. The secondary metric does not automatically compare with the primary metric. Define the value for **Compare to**:
   * **Static value**: Compares against a fixed baseline value that you specify
   * **Primary metric**: Compares the secondary metric directly against the primary metric by displaying the result of `Primary metric - Secondary metric`. This option is only available when the primary metric is numeric. 
   
     When you select this option, the secondary metric is automatically updated:

       * The secondary metric label changes to **Difference**. You can edit this label.
       * If you chose a **Display** option that shows a value, the secondary metric value is automatically updated to show the difference compared to the primary metric.

8. Apply your changes. 

The metric visualization now shows the secondary metric as a comparison with a trend indicator.

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

Send the following request to create a metric that counts unique orders for the current period and compares the result to the previous week using a time-shifted formula.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "metric",
  "title": "Total orders with trend",
  "metrics": [
    {
      "type": "primary",
      "operation": "unique_count",
      "field": "order_id",
      "empty_as_null": true,
      "label": "Total orders",
      "subtitle": "Weekly",
      "color": { "type": "auto" }
    },
    {
      "type": "secondary",
      "operation": "formula",
      "formula": "count(order_id,shift='1w')", <1>
      "label": "Compared to previous week",
      "compare": { <2>
        "to": "primary",
        "palette": "compare_to",
        "icon": true,
        "value": true
      },
      "color": { "type": "none" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_ecommerce",
    "time_field": "order_date"
  },
  "styling": {
    "primary": { "position": "bottom", "labels": { "alignment": "left" }, "value": { "sizing": "auto", "alignment": "right" } },
    "secondary": {
      "label": { "visible": true, "placement": "before" },
      "value": { "alignment": "right" }
    }
  }
}
```

1. `shift='1w'` runs the same count offset by one week, providing the comparison baseline.
2. `compare.to: "primary"` displays the *difference* between primary and secondary instead of the raw secondary value. `palette: "compare_to"` colors the badge green for increases and red for decreases. `icon: true` adds a directional arrow.

:::{note}
When `compare.to: "primary"` is first applied, Kibana sets the secondary metric **Label** to **Auto**, which displays **Difference**. To use a custom label, select the secondary metric in the Lens editor, set **Label** to **Custom**, and type your text. Once saved, the custom label is stored in the `label` field of the payload and preserved in exports.
:::

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "metric",
  "title": "Total orders with trend",
  "metrics": [
    {
      "type": "primary",
      "operation": "unique_count",
      "field": "order_id",
      "empty_as_null": true,
      "label": "Total orders",
      "subtitle": "Weekly",
      "color": { "type": "auto" }
    },
    {
      "type": "secondary",
      "operation": "formula",
      "formula": "count(order_id,shift='\''1w'\'')", <1>
      "label": "Compared to previous week",
      "compare": { <2>
        "to": "primary",
        "palette": "compare_to",
        "icon": true,
        "value": true
      },
      "color": { "type": "none" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_ecommerce",
    "time_field": "order_date"
  },
  "styling": {
    "primary": { "position": "bottom", "labels": { "alignment": "left" }, "value": { "sizing": "auto", "alignment": "right" } },
    "secondary": {
      "label": { "visible": true, "placement": "before" },
      "value": { "alignment": "right" }
    }
  }
}'
```

1. `shift='1w'` runs the same count offset by one week, providing the comparison baseline.
2. `compare.to: "primary"` displays the *difference* between primary and secondary instead of the raw secondary value. `palette: "compare_to"` colors the badge green for increases and red for decreases. `icon: true` adds a directional arrow.

:::{note}
When `compare.to: "primary"` is first applied, Kibana sets the secondary metric **Label** to **Auto**, which displays **Difference**. To use a custom label, select the secondary metric in the Lens editor, set **Label** to **Custom**, and type your text. Once saved, the custom label is stored in the `label` field of the payload and preserved in exports.
:::

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

### Show progress by setting a maximum value [metric-progress]

When creating **Metric** visualizations with numeric data, you can specify a maximum value to show progress toward a goal or capacity limit. When combined with the **Bar** background chart option, this displays a progress bar that visually represents how close your current metric is to reaching the maximum value.

| Without progress | With progress |
|--------|-------|
| ![Metric before showing progress](../../images/metric-no-max.png "title =70%") | ![Metric showing progress](../../images/metric-max.png "title =70%") |

To add a progress bar to your metric visualization:

1. Create a **Metric** visualization with a numeric primary metric.

2. Optionally, [customize the appearance of the metric](#primary-metric-options). For example, add dynamic coloring to the primary metric to change colors based on progress: red when below 50%, yellow between 50-80%, and green above 80%. The progress bar will reflect this configuration once you set up a maximum value.

3. Add a maximum value that represents your goal or upper limit. The [maximum value](#max-value-options) can be a static value, a function, or a formula based on your data.

   ![Metric maximum value option](../../images/metric-maximum-value.png "title =70%")

4. Configure the **Primary metric** appearance to show the progress bar. Depending on the configuration of the primary metric, Lens might automatically set this option for you. If not, complete these steps:
   1. In the primary metric configuration, set the **Background chart** or **Supporting visualization** type to **Bar**. The name of this option depends on the version you're using.
   3. Optionally, change the orientation of the progress bar as needed.

5. Apply your changes.

The metric visualization now shows a progress bar indicating how close the current value is to the maximum.

::::{tip}
You can combine progress bars with secondary metrics to show both progress toward a goal and trends over time. To do this, add both a maximum value and a secondary metric to your visualization.
::::

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example creates a metric that shows the current count of users against a target of 2,500, with a progress bar and a weekly comparison badge.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "metric",
  "title": "Quarterly net new users",
  "filters": [],
  "query": { "expression": "" },
  "metrics": [
    {
      "type": "primary",
      "operation": "formula",
      "formula": "count()",
      "label": "Quarterly net new users",
      "subtitle": "Target: 2500",
      "background_chart": { <1>
        "type": "bar",
        "max_value": { "operation": "formula", "formula": "2500" } <2>
      },
      "color": { <3>
        "type": "dynamic",
        "range": "absolute",
        "steps": [
          { "lt": 1000, "color": "#f6726a" },
          { "gte": 1000, "lt": 2000, "color": "#fcd883" },
          { "gte": 2000, "color": "#24c292" }
        ]
      }
    },
    {
      "type": "secondary",
      "operation": "formula",
      "formula": "count(shift='1w')",
      "label": "Since last week",
      "compare": { "to": "primary", "palette": "compare_to", "icon": true, "value": true },
      "color": { "type": "none" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "primary": { "position": "top", "labels": { "alignment": "left" }, "value": { "sizing": "auto", "alignment": "left" } },
    "secondary": { "label": { "visible": true, "placement": "before" }, "value": { "alignment": "left" } }
  }
}
```

1. `background_chart.type: "bar"` renders a horizontal progress bar behind the metric value.
2. `max_value` with `formula: "2500"` sets the target. The bar fills proportionally as the metric approaches this value. You can also use `operation: "static_value", value: 2500` for a plain number.
3. `dynamic` color with `absolute` thresholds changes the tile color as the metric progresses — red below 1,000, yellow between 1,000 and 2,000, and green at or above 2,000.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "metric",
  "title": "Quarterly net new users",
  "filters": [],
  "query": { "expression": "" },
  "metrics": [
    {
      "type": "primary",
      "operation": "formula",
      "formula": "count()",
      "label": "Quarterly net new users",
      "subtitle": "Target: 2500",
      "background_chart": { <1>
        "type": "bar",
        "max_value": { "operation": "formula", "formula": "2500" } <2>
      },
      "color": { <3>
        "type": "dynamic",
        "range": "absolute",
        "steps": [
          { "lt": 1000, "color": "#f6726a" },
          { "gte": 1000, "lt": 2000, "color": "#fcd883" },
          { "gte": 2000, "color": "#24c292" }
        ]
      }
    },
    {
      "type": "secondary",
      "operation": "formula",
      "formula": "count(shift='\''1w'\'')",
      "label": "Since last week",
      "compare": { "to": "primary", "palette": "compare_to", "icon": true, "value": true },
      "color": { "type": "none" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "primary": { "position": "top", "labels": { "alignment": "left" }, "value": { "sizing": "auto", "alignment": "left" } },
    "secondary": { "label": { "visible": true, "placement": "before" }, "value": { "alignment": "left" } }
  }
}'
```

1. `background_chart.type: "bar"` renders a horizontal progress bar behind the metric value.
2. `max_value` with `formula: "2500"` sets the target. The bar fills proportionally as the metric approaches this value. You can also use `operation: "static_value", value: 2500` for a plain number.
3. `dynamic` color with `absolute` thresholds changes the tile color as the metric progresses — red below 1,000, yellow between 1,000 and 2,000, and green at or above 2,000.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

## Metric chart settings [settings]

Customize your metric chart to display exactly the information you need, formatted the way you want.

### Primary metric settings [primary-metric-options]

**Value**
:   The main numeric value that appears prominently in your chart. When you drag a field onto the chart, {{kib}} suggests a function based on the field type. You can change it and use aggregation functions like `Sum`, `Average`, `Count`, `Median`, and more, or create custom calculations with formulas. Refer to [](/explore-analyze/visualize/lens.md#lens-formulas) for examples, or to the {icon}`documentation` **Formula reference** available from Lens.

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
:   Define the formatting of the primary metric, including:
    - **Name**: By default, the chart uses the function or formula as title. It's a best practice to customize this with a meaningful title.
    - **Value format**: Choose to display the metric as number, percent, bytes, bits, duration, or with a custom format that you can define.
    - **Icon decoration**: Add an icon to the top right corner of the chart.
    - **Background chart** or supporting visualization **Type** (depending on your version): Options include:
      - **None**: Show a unified background.    
      - **Line**: Show a light line chart in the background.
      - **Bar**: Show a progress bar that represents the current value of the chart measured against the [Maximum value](#max-value-options) defined for the chart.
    - **Bar orientation**: Options include **Vertical** and **Horizontal**.
    - **Color mode** or **Color by value** (depending on your version): Apply colors to the chart. Choose between **Static** for a unique color and **Dynamic** for using different colors based on the metric's value. By default, the color applies to the chart's background. 
      - **Static**: The color always remains the same and is independent from the metric's value.
        - **Color**: Pick a color and its opacity.
      - **Dynamic**: Define colors to apply to the chart based on the value of the primary metric.
        - **Dynamic color mapping**: Use the color palette to define custom color ranges.

### Secondary metric settings [secondary-metric-options]

**Value**
:   An optional additional value that provides context or enables comparisons. Common uses include:
    * Time-shifted values to show trends (for example, last week's sales compared to this week)
    * Different aggregations on the same data (for example, showing both average and median response times)
    * Related metrics for context (for example, showing total count alongside an average)

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
:   Define the formatting of the secondary metric, including:
    - **Name**: By default, the chart uses the function or formula as title. It's a best practice to customize this with a meaningful title.
    - **Value format**: Choose to display the metric as number, percent, bytes, bits, duration, or with a custom format that you can define.
    - **Label**: Define the label displayed next to the secondary metric. By default, the **Name** shows. You can instead show a **Custom** value or hide it by selecting **None**.
    - **Label position**: Choose to show the label **Before** or **After** the metric.
    - **Color by value**: Apply colors to the chart. Choose between **None**, **Static** for a unique color and **Dynamic** for using different colors based on the metric's value. This option allows you to use the secondary metric as a comparison point to highlight trends. Refer to [](#metric-trends) for more details.

### Maximum value settings [max-value-options]

**Value**
:   An optional reference value that defines the upper bound for your metric. Specifying a maximum lets you show a progress bar in your metric chart. The progress is represented by your primary metric's value on a scale of 0 to the defined maximum value. This option is useful for showing progress toward goals or capacity limits.

    :::{note}
    If a progress bar doesn't show after setting a maximum value, manually set the primary metric's **Background chart** option to **Bar**.
    :::

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
:   Define the formatting of the maximum value, including:
    - **Name**: It's a best practice to customize this with a readable title.

### Breakdown settings [breakdown-options]

**Data**
:   Split your metric into multiple tiles based on a categorical field. Each unique value creates its own tile, allowing you to compare metrics across regions, products, time periods, or any other dimensions. It supports the following functions:

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
:   Define the formatting of the broken down view of the metric, including:
    - **Name**: It's a best practice to customize this with a meaningful title.
    - **Layout columns**: The number of columns used to lay out the various tiles of your metric chart.


### General layout settings [appearance-options]
```{applies_to}
stack: ga 9.2
serverless: ga
```
When creating or editing a visualization, you can customize several appearance options. To do that, look for the {icon}`brush` icon.

**Style template** {applies_to}`stack: ga 9.5` {applies_to}`serverless: ga`
:   Apply a preset that sets the position and alignment of the primary metric, title, and secondary value in one step. Choose between:

    - **Top**: Primary value and title at the top, secondary value below. All elements are left-aligned.
    - **Middle**: Title at the top, primary value centered, secondary value below. All elements are center-aligned.
    - **Bottom**: Title at the top, secondary and primary values at the bottom. The primary and secondary values are right-aligned. New metric visualizations use this template by default.
    - **Custom**: Keep your individual appearance settings. Select **Custom**, then adjust each control independently in the **Details** section. Lens switches to **Custom** automatically when your settings no longer match any preset.

    The detailed appearance controls described in the next section are grouped under a **Details** accordion. Select **Details** to expand the section and adjust individual settings, or select a different template to apply its preset values to all styling settings at once.

**Primary metric**
:   Define the formatting of the primary metric in terms of **Position**, **Alignment**, and **Font size**.

    - **Position**: Choose the vertical placement of the primary metric value within the tile:
      - **Top**: Places the value at the top of the tile.
      - **Bottom**: Places the value at the bottom of the tile. This is the default.
      - {applies_to}`stack: ga 9.4` **Middle**: Centers the value vertically within the tile.

**Title and subtitle**
:   Enter a subtitle and define the relevant settings:
    - **Alignment**
    - {applies_to}`stack: ga 9.2-9.3` **Font weight**

**Secondary metric**
:   Define the **Alignment** of the secondary metric.

**Other**
:   Configure the icon and layout:
    - **Icon decoration**: Add an icon to the metric chart.
    - **Icon position**: Select **Left** or **Right**.
    - {applies_to}`stack: ga 9.5` {applies_to}`serverless: ga` **Density**: Select **Compact** to use the previous layout, or **Default** to increase padding and spacing and use a larger font. New metric charts use **Default**. Charts saved before this option was introduced use **Compact** until you change the setting.


## Metric chart examples

<!-- MAINTENANCE: the API payload examples in this section were verified
against the Visualizations API spec. To re-verify after a schema change, run:
  KIBANA_URL=… API_KEY=… python3 .github/scripts/verify-lens-api-examples.py --file metric-charts.md
See .github/scripts/verify-lens-api-examples.py for full usage. -->

The following examples show various configuration options that you can use for building impactful metrics.

**Ratio of successful requests**
:   Display the percentage of successful requests on a monitoring dashboard:

    * **Title**: "Successful requests (2xx)"
    * **Primary metric**: `count(kql='response.keyword >= "200" and response.keyword < "300"') / count(response.keyword)`
      * **Value format**: `Percent`
      * **Color mode** or **Color by value**: `Dynamic` (green when above 95%, yellow between 75% and 95%, red when below)
      * **Background chart** or **Supporting visualization**: "Line" to show evolution over time
    * **Secondary metric**: `0.95` formula
      * **Value format**: `Percent`
      * **Label**: Custom, set to `Target:`

![Metric with below target successful request percentage](../../images/metric-example-successful-requests-rate.png "=70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example creates a metric that calculates the ratio of successful HTTP requests using a formula with a KQL filter, and adds a fixed target value as a secondary metric.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "metric",
  "title": "Successful requests (2xx)",
  "filters": [],
  "query": { "expression": "" },
  "metrics": [
    {
      "type": "primary",
      "operation": "formula",
      "formula": "count(kql=response.keyword >= \"200\" and response.keyword < \"300\") / count(response.keyword)", <1>
      "label": "Successful requests (2xx)",
      "format": { "type": "percent", "decimals": 1, "compact": true },
      "background_chart": { "type": "trend" }, <2>
      "color": { <3>
        "type": "dynamic",
        "range": "absolute",
        "steps": [
          { "lt": 0.75, "color": "#f6726a" },
          { "gte": 0.75, "lt": 0.95, "color": "#fcd883" },
          { "gte": 0.95, "color": "#24c292" }
        ]
      },
      "apply_color_to": "background" <4>
    },
    {
      "type": "secondary",
      "operation": "formula",
      "formula": "0.95", <5>
      "format": { "type": "percent", "decimals": 2 },
      "label": "Target:",
      "color": { "type": "none" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "primary": { "position": "top", "labels": { "alignment": "left" }, "value": { "sizing": "auto", "alignment": "left" } },
    "secondary": { "label": { "visible": true, "placement": "before" }, "value": { "alignment": "right" } }
  }
}
```

1. `response.keyword` is stored as a string in the sample data, so the comparison values must be quoted.
2. `background_chart.type: "trend"` renders a sparkline in the background showing how the metric evolves over time.
3. `dynamic` color with `absolute` thresholds applies different colors based on the metric value — red below 75%, yellow between 75% and 95%, green at or above 95%.
4. `apply_color_to: "background"` colors the tile background rather than the number itself.
5. The secondary metric displays a fixed 95% target for comparison.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "metric",
  "title": "Successful requests (2xx)",
  "filters": [],
  "query": { "expression": "" },
  "metrics": [
    {
      "type": "primary",
      "operation": "formula",
      "formula": "count(kql='''response.keyword >= \"200\" and response.keyword < \"300\"''') / count(response.keyword)", <1>
      "label": "Successful requests (2xx)",
      "format": { "type": "percent", "decimals": 1, "compact": true },
      "background_chart": { "type": "trend" }, <2>
      "color": { <3>
        "type": "dynamic",
        "range": "absolute",
        "steps": [
          { "lt": 0.75, "color": "#f6726a" },
          { "gte": 0.75, "lt": 0.95, "color": "#fcd883" },
          { "gte": 0.95, "color": "#24c292" }
        ]
      },
      "apply_color_to": "background" <4>
    },
    {
      "type": "secondary",
      "operation": "formula",
      "formula": "0.95", <5>
      "format": { "type": "percent", "decimals": 2 },
      "label": "Target:",
      "color": { "type": "none" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "primary": { "position": "top", "labels": { "alignment": "left" }, "value": { "sizing": "auto", "alignment": "left" } },
    "secondary": { "label": { "visible": true, "placement": "before" }, "value": { "alignment": "right" } }
  }
}'
```

1. `response.keyword` is stored as a string in the sample data, so the comparison values must be quoted.
2. `background_chart.type: "trend"` renders a sparkline in the background showing how the metric evolves over time.
3. `dynamic` color with `absolute` thresholds applies different colors based on the metric value — red below 75%, yellow between 75% and 95%, green at or above 95%.
4. `apply_color_to: "background"` colors the tile background rather than the number itself.
5. The secondary metric displays a fixed 95% target for comparison.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

**Ratio of successful requests per origin**
:   This example builds on the previous one to display the percentage of successful requests for the 10 countries with the most incoming requests on a monitoring dashboard:

    * **Title**: "Successful requests per origin"
    * **Primary metric**: `count(kql='response.keyword >= "200" and response.keyword < "300"') / count(response.keyword)`
      * **Value format**: `Percent`
      * **Color mode** or **Color by value**: `Dynamic`. Green when above 95%, yellow between 75% and 95%, red when below
      * **Background chart** or **Supporting visualization**: "Line" to show evolution over time
    * **Secondary metric**: `0.95` formula
      * **Label**: Custom, set to `Target:`
      * **Value format**: `Percent`
    * **Break down by**: `geo.dest`
      * **Number of values**: `10`
      * **Rank by**: `Custom` > `Count` > `Records` to get countries generating most requests

![Metric with below target successful request percentage](../../images/metric-example-successful-requests-rate-top-countries.png "=70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example builds on the previous one by adding a breakdown that splits the success rate into one tile per destination country.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "metric",
  "title": "Successful requests per origin",
  "filters": [],
  "query": { "expression": "" },
  "metrics": [
    {
      "type": "primary",
      "operation": "formula",
      "formula": "count(kql=response.keyword >= \"200\" and response.keyword < \"300\") / count(response.keyword)",
      "label": "Successful requests (2xx)",
      "format": { "type": "percent", "decimals": 1, "compact": true },
      "background_chart": { "type": "trend" },
      "color": {
        "type": "dynamic",
        "range": "absolute",
        "steps": [
          { "lt": 0.75, "color": "#f6726a" },
          { "gte": 0.75, "lt": 0.95, "color": "#fcd883" },
          { "gte": 0.95, "color": "#24c292" }
        ]
      },
      "apply_color_to": "background"
    },
    {
      "type": "secondary",
      "operation": "formula",
      "formula": "0.95",
      "format": { "type": "percent", "decimals": 2 },
      "label": "Target:",
      "color": { "type": "none" }
    }
  ],
  "breakdown_by": { <1>
    "operation": "terms",
    "fields": ["geo.dest"],
    "limit": 10, <2>
    "rank_by": { "type": "custom", "operation": "count", "field": "___records___", "direction": "desc" }, <3>
    "columns": 5 <4>
  },
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "primary": { "position": "top", "labels": { "alignment": "left" }, "value": { "sizing": "auto", "alignment": "left" } },
    "secondary": { "label": { "visible": true, "placement": "before" }, "value": { "alignment": "right" } }
  }
}
```

1. `breakdown_by` splits the metric into separate tiles, one per destination country.
2. Shows the top 10 countries by document count.
3. `rank_by` with `field: "___records___"` ranks tiles by document count, ensuring the countries with the most traffic appear first.
4. `columns: 5` arranges the tiles in a 5-column grid.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "metric",
  "title": "Successful requests per origin",
  "filters": [],
  "query": { "expression": "" },
  "metrics": [
    {
      "type": "primary",
      "operation": "formula",
      "formula": "count(kql='''response.keyword >= \"200\" and response.keyword < \"300\"''') / count(response.keyword)",
      "label": "Successful requests (2xx)",
      "format": { "type": "percent", "decimals": 1, "compact": true },
      "background_chart": { "type": "trend" },
      "color": {
        "type": "dynamic",
        "range": "absolute",
        "steps": [
          { "lt": 0.75, "color": "#f6726a" },
          { "gte": 0.75, "lt": 0.95, "color": "#fcd883" },
          { "gte": 0.95, "color": "#24c292" }
        ]
      },
      "apply_color_to": "background"
    },
    {
      "type": "secondary",
      "operation": "formula",
      "formula": "0.95",
      "format": { "type": "percent", "decimals": 2 },
      "label": "Target:",
      "color": { "type": "none" }
    }
  ],
  "breakdown_by": { <1>
    "operation": "terms",
    "fields": ["geo.dest"],
    "limit": 10, <2>
    "rank_by": { "type": "custom", "operation": "count", "field": "___records___", "direction": "desc" }, <3>
    "columns": 5 <4>
  },
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "primary": { "position": "top", "labels": { "alignment": "left" }, "value": { "sizing": "auto", "alignment": "left" } },
    "secondary": { "label": { "visible": true, "placement": "before" }, "value": { "alignment": "right" } }
  }
}'
```

1. `breakdown_by` splits the metric into separate tiles, one per destination country.
2. Shows the top 10 countries by document count.
3. `rank_by` with `field: "___records___"` ranks tiles by document count, ensuring the countries with the most traffic appear first.
4. `columns: 5` arranges the tiles in a 5-column grid.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

**Website traffic with trend**
:   Monitor current traffic and show whether it's increasing or decreasing compared to the previous period:

    * **Title**: "Weekly page views"
    * **Primary metric**: `count()` (current week's page views)
    * **Secondary metric**: `count(shift='1w')` (previous week's page views)
      * **Color mode** or **Color by value**: Dynamic coloring
      * **Compare to**: Primary metric
      * **Display**: Both icon and value
      * **Label**: "Compared to previous week"
      * **Color palette**: Green for increases (more traffic is positive)

![Metric showing weekly visits with weekly comparison trend](../../images/metric-website-views-weekly-trend-example.png "=70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

This example creates a metric that counts page views and compares the current value to the previous week using a time-shifted formula.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "metric",
  "title": "Weekly page views",
  "filters": [],
  "query": { "expression": "" },
  "metrics": [
    {
      "type": "primary",
      "operation": "count",
      "empty_as_null": true,
      "label": "Page views",
      "format": { <1>
        "type": "number",
        "decimals": 0,
        "compact": true
      }
    },
    {
      "type": "secondary", <2>
      "operation": "formula",
      "formula": "count(shift='1w')", <3>
      "label": "Compared to previous week",
      "compare": { <4>
        "to": "primary",
        "palette": "compare_to",
        "icon": true,
        "value": true
      },
      "color": { "type": "none" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "primary": { "position": "top", "labels": { "alignment": "left" }, "value": { "sizing": "auto", "alignment": "left" } },
    "secondary": {
      "label": { "visible": true, "placement": "before" },
      "value": { "alignment": "right" }
    }
  }
}
```

1. `compact: true` displays large numbers in abbreviated form (for example, 1.2K).
2. The secondary metric appears below the primary value as a comparison badge.
3. `shift='1w'` runs the same count query offset by one week.
4. `compare.to: "primary"` displays the difference from the primary rather than the raw secondary value. `palette: "compare_to"` colors the badge green for increases and red for decreases. `icon: true` adds a directional arrow (↑ or ↓).

:::{note}
When `compare.to: "primary"` is first applied, Kibana sets the secondary metric **Label** to **Auto**, which displays **Difference**. To use a custom label, select the secondary metric in the Lens editor, set **Label** to **Custom**, and type your text. Once saved, the custom label is stored in the `label` field of the payload and preserved in exports.
:::

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "metric",
  "title": "Weekly page views",
  "filters": [],
  "query": { "expression": "" },
  "metrics": [
    {
      "type": "primary",
      "operation": "count",
      "empty_as_null": true,
      "label": "Page views",
      "format": { <1>
        "type": "number",
        "decimals": 0,
        "compact": true
      }
    },
    {
      "type": "secondary", <2>
      "operation": "formula",
      "formula": "count(shift='\''1w'\'')", <3>
      "label": "Compared to previous week",
      "compare": { <4>
        "to": "primary",
        "palette": "compare_to",
        "icon": true,
        "value": true
      },
      "color": { "type": "none" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": {
    "primary": { "position": "top", "labels": { "alignment": "left" }, "value": { "sizing": "auto", "alignment": "left" } },
    "secondary": {
      "label": { "visible": true, "placement": "before" },
      "value": { "alignment": "right" }
    }
  }
}'
```

1. `compact: true` displays large numbers in abbreviated form (for example, 1.2K).
2. The secondary metric appears below the primary value as a comparison badge.
3. `shift='1w'` runs the same count query offset by one week.
4. `compare.to: "primary"` displays the difference from the primary rather than the raw secondary value. `palette: "compare_to"` colors the badge green for increases and red for decreases. `icon: true` adds a directional arrow (↑ or ↓).

:::{note}
When `compare.to: "primary"` is first applied, Kibana sets the secondary metric **Label** to **Auto**, which displays **Difference**. To use a custom label, select the secondary metric in the Lens editor, set **Label** to **Custom**, and type your text. Once saved, the custom label is stored in the `label` field of the payload and preserved in exports.
:::

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::
