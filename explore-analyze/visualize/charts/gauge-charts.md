---
navigation_title: Gauge charts
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
description: Create gauge charts to monitor KPIs and track progress toward goals with visual range context.
---

# Build gauge charts with {{kib}}

Gauge charts display a single value within a defined range, showing how close the value is to a target or threshold. They are ideal for monitoring KPIs, tracking progress toward goals, and highlighting when values fall within acceptable, warning, or critical ranges. Unlike [metric charts](metric-charts.md) that display raw values, gauge charts add range context with known minimum and maximum boundaries.

You can create gauge charts in {{kib}} using [**Lens**](../lens.md).

![Example Lens gauge chart showing RAM consumption averages](/explore-analyze/images/gauge-chart-example.png)

## Build a gauge chart

:::{include} ../../_snippets/lens-prerequisites.md
:::

To build a gauge chart:

::::::{stepper}

:::::{step} Access Lens
:::{include} ../../_snippets/access-lens.md
:::
:::::

:::::{step} Set the visualization to Gauge
New visualizations often start as **Bar** charts.

Using the **Visualization type** dropdown, select **Gauge**.
:::::

:::::{step} Define the data to show
1. Select the {{data-source}} that contains your data.
2. Configure the [**Metric**](#metric-settings) dimension to define the value displayed on the gauge.

Optionally:
   - Configure the [**Minimum value**](#minimum-value-settings) dimension to set the lower bound of the gauge range.
   - Configure the [**Maximum value**](#maximum-value-settings) dimension to set the upper bound of the gauge range.
   - Configure the [**Goal**](#goal-settings) dimension to display a target marker on the gauge.

Each of these optional dimensions can be set as a static number, computed dynamically from your data using an aggregation, or defined with a [formula](/explore-analyze/visualize/lens.md#lens-formulas).

The chart preview updates to show a gauge with your metric value positioned within the range. If the gauge appears empty, verify that the selected field contains numeric data for the current time range.
:::::

:::::{step} Customize the chart to follow best practices
Tweak the appearance of the chart to your needs. Consider the following best practices:

**Set meaningful bounds**
:   Define the minimum and maximum values that make sense for your metric. A CPU usage gauge should range from 0 to 100, while a sales target might range from 0 to your quarterly goal.

**Use color bands for thresholds**
:   Configure color ranges to indicate performance levels. Use green for acceptable values, yellow for warning, and red for critical thresholds.

**Choose the right shape**
:   Select a gauge shape that fits your dashboard layout. Use **Arc** shapes for traditional gauge appearance, or **Linear** for a more compact horizontal or vertical display.

**Add context with titles**
:   Provide clear titles that explain what the gauge measures and what the target value represents.

Refer to [Gauge chart settings](#gauge-chart-settings) to find all configuration options for your gauge chart.

For panel sizing and layout guidance, refer to [Organize dashboard panels](../../dashboards/arrange-panels.md#dashboard-grid-layout).
:::::

:::::{step} Save the chart
:::{include} ../../_snippets/save-visualization.md
:::
:::::

::::::

## Advanced gauge chart scenarios

### Create a goal-tracking gauge [goal-tracking]

Use a gauge to track progress toward a specific target, such as monthly sales goals or project completion percentage.

1. Create a **Gauge** chart and select your {{data-source}}.
2. Configure the **Metric** dimension with your progress value (for example, `Sum(sales_amount)`).
3. Configure the **Minimum value** dimension as a static value of `0`.
4. Configure the **Maximum value** dimension as a static value matching your target (for example, `100000` for a $100K sales goal).
5. Configure the **Goal** dimension as a static value matching your target to display a goal marker on the gauge.
6. Select the **Metric** dimension, enable **Band colors**, and configure **Color mapping** with bands to show progress levels.

![Example Lens gauge chart showing yearly sales goal](/explore-analyze/images/gauge-chart-scenario-goal.png "=75%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: "ga 9.5+, preview =9.4", serverless: ga }

This example creates a horizontal bullet gauge that sums order revenue from the eCommerce sample data, providing a quick view of progress toward a sales goal.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "gauge",
  "title": "Yearly sales goal",
  "filters": [],
  "query": { "expression": "" },
  "styling": {
    "shape": { "type": "bullet", "orientation": "horizontal" } <1>
  },
  "metric": {
    "operation": "sum", <2>
    "field": "products.taxful_price",
    "empty_as_null": true,
    "label": "Yearly sales",
    "max": { "operation": "static_value", "value": 1500000 }, <3>
    "goal": { "operation": "static_value", "value": 1000000 },
    "title": { "visible": true },
    "ticks": { "visible": true, "mode": "bands" },
    "color": {
      "type": "dynamic",
      "range": "absolute",
      "steps": [
        { "gte": 0, "lt": 750000, "color": "#f6726a" },
        { "gte": 750000, "lt": 1000000, "color": "#aee8d2" },
        { "gte": 1000000, "color": "#24c292" }
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

1. `bullet` with `orientation: "horizontal"` renders a compact linear bar gauge, ideal for placing multiple KPIs in a row.
2. `sum` of `products.taxful_price` tracks cumulative revenue as the gauge metric.
3. `max` sets the upper bound of the scale (1.5M) and `goal` places a target marker at 1M, so progress toward the goal is immediately visible. The three `steps` color bands turn the bar red below 750K, light green approaching the goal, and green once it's reached.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "gauge",
  "title": "Yearly sales goal",
  "filters": [],
  "query": { "expression": "" },
  "styling": {
    "shape": { "type": "bullet", "orientation": "horizontal" } <1>
  },
  "metric": {
    "operation": "sum", <2>
    "field": "products.taxful_price",
    "empty_as_null": true,
    "label": "Yearly sales",
    "max": { "operation": "static_value", "value": 1500000 }, <3>
    "goal": { "operation": "static_value", "value": 1000000 },
    "title": { "visible": true },
    "ticks": { "visible": true, "mode": "bands" },
    "color": {
      "type": "dynamic",
      "range": "absolute",
      "steps": [
        { "gte": 0, "lt": 750000, "color": "#f6726a" },
        { "gte": 750000, "lt": 1000000, "color": "#aee8d2" },
        { "gte": 1000000, "color": "#24c292" }
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

1. `bullet` with `orientation: "horizontal"` renders a compact linear bar gauge, ideal for placing multiple KPIs in a row.
2. `sum` of `products.taxful_price` tracks cumulative revenue as the gauge metric.
3. `max` sets the upper bound of the scale (1.5M) and `goal` places a target marker at 1M, so progress toward the goal is immediately visible. The three `steps` color bands turn the bar red below 750K, light green approaching the goal, and green once it's reached.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

### Configure color bands for thresholds [color-bands]

Color bands help users quickly understand whether a value is within acceptable ranges.

1. Create a **Gauge** chart with your metric configured.
2. Select the **Metric** dimension to open its settings.
3. Enable **Band colors**.
4. In **Color mapping**, select a color palette (or use the default **Status** palette) and adjust the band boundaries and colors.
5. Optionally, enable **Ticks on bands** to display tick marks at the band boundaries on the gauge scale.

#### Example: Server health monitoring

This example shows a gauge with server response time and color-coded health indicators.

| Band | Range | Color | Meaning |
|------|-------|-------|---------|
| Healthy | 0-200ms | Green | Normal response times |
| Warning | 200-500ms | Light green | Elevated response times |
| Critical | 500ms+ | Red | Unacceptable performance |

![Example Lens gauge chart showing average response time in milliseconds](/explore-analyze/images/gauge-chart-scenario-thresholds.png "=50%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: "ga 9.5+, preview =9.4", serverless: ga }

This example creates a gauge with three color-coded threshold bands so the arc turns green, yellow, or red depending on the average byte count.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "gauge",
  "title": "Server response time",
  "filters": [],
  "query": { "expression": "" },
  "styling": { "shape": { "type": "bullet", "orientation": "horizontal" } },
  "metric": {
    "operation": "median",
    "field": "memory",
    "label": "Average response time - last hour",
    "format": { "type": "duration", "from": "microseconds", "to": "asMilliseconds" },
    "min": { "operation": "static_value", "value": 0 },
    "max": { "operation": "formula", "formula": "1000000" },
    "title": { "visible": true },
    "ticks": { "visible": true, "mode": "bands" },
    "color": { <1>
      "type": "dynamic",
      "range": "absolute",
      "steps": [ <2>
        { "color": "#24c292", "gte": 0, "lt": 200000 },
        { "color": "#aee8d2", "gte": 200000, "lt": 500000 },
        { "color": "#f6726a", "gte": 500000 }
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

1. `color.type: "dynamic"` applies color bands based on the metric value, giving instant visual feedback on health status.
2. Each `steps` entry defines a range and color: green for healthy (0–200ms), light green for warning (200–500ms), and red for critical (500ms+). The `duration` format converts raw microsecond values to human-readable milliseconds.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "gauge",
  "title": "Server response time",
  "filters": [],
  "query": { "expression": "" },
  "styling": { "shape": { "type": "bullet", "orientation": "horizontal" } },
  "metric": {
    "operation": "median",
    "field": "memory",
    "label": "Average response time - last hour",
    "format": { "type": "duration", "from": "microseconds", "to": "asMilliseconds" },
    "min": { "operation": "static_value", "value": 0 },
    "max": { "operation": "formula", "formula": "1000000" },
    "title": { "visible": true },
    "ticks": { "visible": true, "mode": "bands" },
    "color": { <1>
      "type": "dynamic",
      "range": "absolute",
      "steps": [ <2>
        { "color": "#24c292", "gte": 0, "lt": 200000 },
        { "color": "#aee8d2", "gte": 200000, "lt": 500000 },
        { "color": "#f6726a", "gte": 500000 }
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

1. `color.type: "dynamic"` applies color bands based on the metric value, giving instant visual feedback on health status.
2. Each `steps` entry defines a range and color: green for healthy (0–200ms), light green for warning (200–500ms), and red for critical (500ms+). The `duration` format converts raw microsecond values to human-readable milliseconds.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

### Use dynamic bounds and goals [dynamic-bounds]

Instead of entering fixed static values, you can use fields from your data to set the minimum, maximum, or goal dynamically using aggregations.

1. Create a **Gauge** chart with your metric configured.
2. In the **Maximum value** dimension, select a field and aggregation that represents the upper bound (for example, `Max(quota)` for a quota-based gauge).
3. Optionally, do the same for **Minimum value** (for example, `Min(baseline)`) or **Goal** (for example, `Average(target)`).

This approach is useful when bounds or targets vary by category, time period, or user. You can also use formulas to define dynamic bounds or goals. Refer to [Lens formulas](/explore-analyze/visualize/lens.md#lens-formulas) for more details.

## Gauge chart settings [gauge-chart-settings]

Customize your gauge chart to display exactly the information you need, formatted the way you want.

### Metric settings [metric-settings]

The **Metric** dimension defines the main value displayed on the gauge.

**Data**
:   The value that the gauge displays. When you drag a field onto the chart, {{kib}} suggests a function based on the field type. You can use aggregation functions like `Sum`, `Average`, `Count`, `Median`, `Last value`, and more, or create custom calculations with [formulas](/explore-analyze/visualize/lens.md#lens-formulas).

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
:   - **Name**: Customize the metric label displayed in the gauge.
    - **Value format**: Control how numeric values are displayed (number, percent, bytes, and more).
    - **Band colors**: Toggle to enable colored bands on the gauge. When enabled, the following options appear:
      - **Color mapping**: Configure the color palette and define color stops for the bands. The default palette is **Status** with 4 color steps.
      - **Ticks on bands**: Toggle to place tick marks at band boundaries instead of distributing them evenly along the gauge scale.

### Minimum value settings [minimum-value-settings]

The **Minimum value** dimension defines the lower bound of the gauge range.

**Data**
:   Set a static value, use a field with an aggregation like `Min`, or create a custom calculation with a [formula](/explore-analyze/visualize/lens.md#lens-formulas). When adding this dimension, you can enter a fixed number directly (static value) or select a field to compute the minimum dynamically. If not configured, the gauge infers a minimum from the data.

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

    :::{note}
    The minimum value must be less than the maximum value. If the minimum is greater than or equal to the maximum, the gauge displays an error.
    :::

**Appearance**
:   - **Name**: Customize the label for the minimum value.

### Maximum value settings [maximum-value-settings]

The **Maximum value** dimension defines the upper bound of the gauge range.

**Data**
:   Set a static value, use a field with an aggregation like `Max`, or create a custom calculation with a [formula](/explore-analyze/visualize/lens.md#lens-formulas). When adding this dimension, you can enter a fixed number directly (static value) or select a field to compute the maximum dynamically. If not configured, the gauge infers a maximum from the data.

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
:   - **Name**: Customize the label for the maximum value.

### Goal settings [goal-settings]

The **Goal** dimension displays a target marker on the gauge, providing a visual reference point for the metric value.

**Data**
:   Set a static value, use a field with an aggregation, or create a custom calculation with a [formula](/explore-analyze/visualize/lens.md#lens-formulas). When adding this dimension, you can enter a fixed number directly (static value) or select a field to compute the goal dynamically. The goal marker appears as a line or indicator on the gauge scale.

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
:   - **Name**: Customize the label for the goal value.

### General layout [appearance-options]

When creating or editing a visualization, you can customize several appearance options from the {icon}`brush` **Style** menu.

#### Style settings

**Shape**
:   Choose the gauge shape:
    - **Linear**: A bar gauge, displayed horizontally (default) or vertically. Select **Horizontal** or **Vertical** orientation after choosing this shape.
    - **Minor arc**: A partial circle arc.
    - **Major arc**: A larger circular arc.
    - **Circle**: A full 360-degree gauge.

**Titles and text**

**Title**
:   Control the gauge title:
    - **Auto**: Display the metric name automatically (default).
    - **Custom**: Enter a custom title.
    - **None**: Hide the title.

**Subtitle**
:   Add an optional subtitle for additional context:
    - **Custom**: Enter a custom subtitle.
    - **None**: No subtitle (default).

## Gauge chart examples

<!-- MAINTENANCE: the API payload examples in this section were verified
against the Visualizations API spec. To re-verify after a schema change, run:
  KIBANA_URL=… API_KEY=… python3 .github/scripts/verify-lens-api-examples.py --file gauge-charts.md
See .github/scripts/verify-lens-api-examples.py for full usage. -->

The following examples show various configuration options for building impactful gauge charts.

**CPU usage monitoring**
:   Monitor system CPU usage with threshold-based coloring:

    * Example based on: {{kib}} Sample Data Logs
    * **Metric**: Formula `average(machine.ram)/20000000000` formatted as percent
    * **Maximum**: Formula `max(machine.ram)/32211000000`
    * **Shape**: Semi-circle
    * **Color bands**: 0–50% (green), 50–75% (yellow), 75%+ (red)

![Example Lens gauge chart showing average CPU usage in percent](/explore-analyze/images/gauge-chart-example-cpu.png "=50%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: "ga 9.5+, preview =9.4", serverless: ga }

This example creates a CPU-monitoring gauge with green/yellow/red threshold bands, using `machine.ram` from the logs sample data as a proxy for a CPU-like metric.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "gauge",
  "title": "CPU usage",
  "filters": [],
  "query": { "expression": "" },
  "styling": { "shape": { "type": "semi_circle" } },
  "metric": {
    "operation": "formula", <1>
    "formula": "average(machine.ram)/20000000000",
    "label": "CPU usage",
    "format": { "type": "percent", "decimals": 2, "compact": false },
    "max": { "operation": "formula", "formula": "max(machine.ram)/32211000000" },
    "title": { "visible": true },
    "ticks": { "visible": true, "mode": "bands" },
    "color": {
      "type": "dynamic",
      "range": "percentage",
      "steps": [ <2>
        { "gte": 0, "lt": 50, "color": "#24c292" },
        { "gte": 50, "lt": 75, "color": "#EAAE01" },
        { "gte": 75, "color": "#f6726a" }
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

1. `formula` computes the ratio of average RAM to a reference value, producing a 0–1 ratio formatted as a percentage. Replace with your actual CPU metric field (for example, `average(system.cpu.total.pct)`).
2. `range: "percentage"` maps the color thresholds proportionally across the gauge's 0–100% scale: green below 50%, yellow between 50–75%, and red above 75%.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "gauge",
  "title": "CPU usage",
  "filters": [],
  "query": { "expression": "" },
  "styling": { "shape": { "type": "semi_circle" } },
  "metric": {
    "operation": "formula", <1>
    "formula": "average(machine.ram)/20000000000",
    "label": "CPU usage",
    "format": { "type": "percent", "decimals": 2, "compact": false },
    "max": { "operation": "formula", "formula": "max(machine.ram)/32211000000" },
    "title": { "visible": true },
    "ticks": { "visible": true, "mode": "bands" },
    "color": {
      "type": "dynamic",
      "range": "percentage",
      "steps": [ <2>
        { "gte": 0, "lt": 50, "color": "#24c292" },
        { "gte": 50, "lt": 75, "color": "#EAAE01" },
        { "gte": 75, "color": "#f6726a" }
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

1. `formula` computes the ratio of average RAM to a reference value, producing a 0–1 ratio formatted as a percentage. Replace with your actual CPU metric field (for example, `average(system.cpu.total.pct)`).
2. `range: "percentage"` maps the color thresholds proportionally across the gauge's 0–100% scale: green below 50%, yellow between 50–75%, and red above 75%.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

**Disk space utilization**
:   Display disk space usage as a percentage of capacity:

    * Example based on: {{kib}} Sample Data Logs
    * **Metric**: Formula `average(machine.ram)/29000000000` formatted as percent
    * **Maximum**: Formula `max(machine.ram)/32211000000`
    * **Shape**: Circle
    * **Color bands**: 0–60% (green), 60–80% (yellow), 80%+ (red)

![Example Lens gauge chart showing disk space utilization in percent](/explore-analyze/images/gauge-chart-example-disk-space.png "=50%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: "ga 9.5+, preview =9.4", serverless: ga }

This example creates a full-circle disk utilization gauge with color bands that shift from green to red as usage increases, using `machine.ram` from the logs sample data as a proxy.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "gauge",
  "title": "Disk space utilization",
  "filters": [],
  "query": { "expression": "" },
  "styling": {
    "shape": { "type": "circle" } <1>
  },
  "metric": {
    "operation": "formula",
    "formula": "average(machine.ram)/29000000000", <2>
    "label": "Disk space utilization",
    "format": { "type": "percent", "decimals": 2, "compact": false },
    "max": { "operation": "formula", "formula": "max(machine.ram)/32211000000" },
    "title": { "visible": true },
    "ticks": { "visible": true, "mode": "bands" },
    "color": {
      "type": "dynamic",
      "range": "percentage",
      "steps": [ <3>
        { "gte": 0, "lt": 60, "color": "#24c292" },
        { "gte": 60, "lt": 80, "color": "#EAAE01" },
        { "gte": 80, "color": "#f6726a" }
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

1. `circle` draws a full 360-degree gauge, which works well for utilization percentages where the full range is always visible.
2. The `formula` divides average RAM by a reference capacity value to produce a 0–1 ratio formatted as percent. Replace with your actual disk metric (for example, `sum(system.filesystem.used.bytes) / sum(system.filesystem.total.bytes)`).
3. The `percentage` range maps thresholds proportionally: green below 60%, yellow between 60–80%, and red above 80%, so the gauge turns red only when disk usage becomes critical.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "gauge",
  "title": "Disk space utilization",
  "filters": [],
  "query": { "expression": "" },
  "styling": {
    "shape": { "type": "circle" } <1>
  },
  "metric": {
    "operation": "formula",
    "formula": "average(machine.ram)/29000000000", <2>
    "label": "Disk space utilization",
    "format": { "type": "percent", "decimals": 2, "compact": false },
    "max": { "operation": "formula", "formula": "max(machine.ram)/32211000000" },
    "title": { "visible": true },
    "ticks": { "visible": true, "mode": "bands" },
    "color": {
      "type": "dynamic",
      "range": "percentage",
      "steps": [ <3>
        { "gte": 0, "lt": 60, "color": "#24c292" },
        { "gte": 60, "lt": 80, "color": "#EAAE01" },
        { "gte": 80, "color": "#f6726a" }
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

1. `circle` draws a full 360-degree gauge, which works well for utilization percentages where the full range is always visible.
2. The `formula` divides average RAM by a reference capacity value to produce a 0–1 ratio formatted as percent. Replace with your actual disk metric (for example, `sum(system.filesystem.used.bytes) / sum(system.filesystem.total.bytes)`).
3. The `percentage` range maps thresholds proportionally: green below 60%, yellow between 60–80%, and red above 80%, so the gauge turns red only when disk usage becomes critical.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::
