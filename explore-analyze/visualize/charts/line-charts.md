---
navigation_title: Line charts
applies_to:
  stack: ga
  serverless: ga
description: Create line charts to visualize how metrics evolve over time, spot seasonal patterns, and detect spikes or regressions.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Build line charts with {{kib}}

Line charts are ideal for visualizing how metrics evolve over time, spotting seasonal patterns, and detecting spikes or regressions at a glance. Use them for KPIs like response time, error rate, throughput, or utilization, and compare multiple series or previous periods on the same chart. You can create line charts from any numeric data using aggregations (for example, `Average`, `Percentile`, `Counter rate`) or with custom [formulas](../lens.md#lens-formulas).

You can create line charts in {{kib}} using [**Lens**](../lens.md).

![Example Lens line chart](../../images/kibana-line-new.png)

## Build a line chart

:::{include} ../../_snippets/lens-prerequisites.md
:::

To build a line chart:

::::::{stepper}

:::::{step} Access Lens
:::{include} ../../_snippets/access-lens.md
:::
:::::

:::::{step} Set the visualization to Line
Make sure that the visualization type is set to **Line**.

{applies_to}`stack: ga 9.4` {applies_to}`serverless: ga` When you drag a date or time field (such as `@timestamp`) onto an empty workspace, **Line** is automatically selected.
:::::

:::::{step} Define the data to show
1. Select the {{data-source}} that contains your data.
2. Drag a [time field](elasticsearch://reference/elasticsearch/mapping-reference/date.md) to the **Horizontal axis** and a numeric field to the **Vertical axis**. {{kib}} automatically selects an appropriate aggregation function compatible with the selected field.

Optionally:
   - Add more numeric fields to create additional series, or drag a categorical field to **Break down by** to split the series.
   - You can click the **Add layer** icon {icon}`plus_square` to integrate additional visualizations, [annotations](../lens.md#add-annotations), or a [reference line](../lens.md#add-reference-lines).

The chart preview updates to show one or more lines plotted over time. Each line represents a series, and data points are connected to show trends.
:::::

:::::{step} Customize the chart to follow best practices
You can tweak the appearance of your chart by adjusting axes, legends, and series styles from the chart settings. Consider the following best practices:

**Use color wisely**
:   Assign colors that match your users' expectations and consider your specific context. 

    {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Lens automatically applies the **Elastic (line optimized)** palette to line charts, which reorders colors for better contrast between adjacent series. You can override this by manually selecting a different palette.

**Provide context**
:   Add a legend and descriptive axis titles, or remove them for obvious axes.

For more chart configuration options, go to the [Line chart settings](#settings) section.

For panel sizing and layout guidance, refer to [Organize dashboard panels](../../dashboards/arrange-panels.md#dashboard-grid-layout).
:::::

:::::{step} Save the chart
:::{include} ../../_snippets/save-visualization.md
:::
:::::

::::::

## Advanced line scenarios

### Compare current versus previous period with time shift [line-previous-period]

In line charts, you can enable time shift to compare the current value with a prior time range and identify deltas.

![Example Lens line chart current previous](../../images/kibana-line-current-previous.png "=75%")

1. Create a line chart with a time-based **Horizontal axis** and your main metric on **Vertical axis**, for example: `bytes`.
2. Duplicate the layer:
    * {applies_to}`serverless: ga` {applies_to}`stack: ga 9.3` Select {icon}`copy` **Duplicate layer** from the visualization editor.
    * {applies_to}`stack: ga 9.0-9.2` Open the {icon}`boxes_vertical` contextual menu of the visualization editor and select {icon}`copy` **Duplicate layer**.
3. From the duplicated layer settings, select the field defined as vertical axis to open its details. Expand its **Advanced** options and set **Time shift** to `1w` or to the time value of your choice.
   Check [Compare differences over time](../lens.md#compare-data-with-time-offsets) for more details.
4. Optionally, customize the appearance of the layer to adjust how it looks on the chart. When you duplicate a layer, {{kib}} automatically assigns a different **Series color** to the new layer. You can for example change this color, or adjust the layer's name and axis position. This name is used for the chart's legend.

::::{tip}
You can also compute the relative change by defining the axis data with a [formula](/explore-analyze/visualize/lens.md#lens-formulas), for example:
`(average(bytes) - average(bytes, shift='1w')) / average(bytes, shift='1w')`
::::

### Highlight thresholds with reference lines [line-reference-lines]

Use reference lines to indicate important thresholds, such as SLOs or alert limits.

![Example Lens line chart reference lines](../../images/kibana-line-reference-lines.png "=75%")

1. In the chart settings, add a static value reference line to mark your target or threshold visually.
2. Use the **Text decoration** setting to provide a name, for example, `Target` or `SLO`, choose a color, and optionally a band.

## Line chart settings [settings]

Customize your line chart to display exactly the information you need, formatted the way you want.

### Horizontal axis settings [horizontal-axis-settings]

**Data**
:   
    - **Functions**:
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
:   **Name**: By default, the chart uses the function or formula as title. It's a best practice to customize this with a meaningful title.

### Vertical axis settings [vertical-axis-settings]

**Data**
:   To represent the metrics or values you want to visualize, you can use quick functions like `Average`, `Count`, `Percentile`, `Counter rate`, or create custom calculations with formulas. Refer to [](/explore-analyze/visualize/lens.md#lens-formulas) for examples, or to the {icon}`documentation` **Formula reference** available from Lens.

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
   - **Name**: Customize the legend label with a descriptive name.
   - **Value format**: Control how numeric values are displayed on the vertical axis of your visualization.
   - **Series color**: Select a palette or specific color per series.
   - **Axis side**: Control where axis labels and tick marks appear.

### Breakdown settings [breakdown-settings]

Breakdown functions segment your data into multiple lines on the same chart, with each line representing a different value of a categorical field. You can specify the following options:

**Data**
:   
    - **Functions**:
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
:   Allow you to customize how your breakdown data is displayed in line charts, including:

    - **Name**: It's a best practice to customize this with a meaningful title.
    - **Value format**: Control how numeric values are displayed in your visualization.
    - **Color mapping**: Determine how colors are assigned to your breakdown series.

### General layout [appearance-options]

When creating or editing a visualization, you can adjust the following settings.

:::{include} ../../_snippets/line-chart-style-settings.md
:::

:::{include} ../../_snippets/xy-chart-legend-settings.md
:::

## Line chart examples

<!-- MAINTENANCE: the API payload examples in this section were verified
against the Visualizations API spec. To re-verify after a schema change, run:
  KIBANA_URL=… API_KEY=… python3 .github/scripts/verify-lens-api-examples.py --file line-charts.md
See .github/scripts/verify-lens-api-examples.py for full usage. -->

**Average RAM per host**
:   Monitoring the average of RAM over time for the first four hosts:

1. Drag `@timestamp` to the **Horizontal axis** and set the following settings: 
   * **Functions**: `Date histogram`
   * **Minimum interval**: `Hour`
2. Drag `machine.ram` to the **Vertical axis** and set the following settings:
   * **Functions**: : `Moving average`
   * **Value format**: `Bytes`
3. In the **Breakdwon** panel, set the following settings:
   * **Functions**: `Top values`
   * **Fields**: `host.keyword`   
   * **Number of values**: `4`
4. Save your chart.

![Average RAM per host](../../images/kibana-lens-average-ram-host.png "=70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

Send the following request to create a line chart that plots the moving average of RAM, broken down by the top 4 hosts.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "xy",
  "title": "Average RAM per host",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "visible", "placement": "outside", "position": "bottom" },
  "axis": {},
  "layers": [
    {
      "type": "line",
      "x": {
        "operation": "date_histogram",
        "field": "timestamp",
        "suggested_interval": "1h"
      },
      "y": [
        {
          "operation": "moving_average", <1>
          "of": {
            "operation": "average",
            "field": "machine.ram",
            "format": { "type": "bytes", "decimals": 0 },
            "filter": { "expression": "" }
          },
          "label": "Moving average of RAM",
          "format": { "type": "bytes", "decimals": 0 },
          "filter": { "expression": "" },
          "color": {
            "type": "static",
            "color": "#6092c0"
          }
        }
      ],
      "breakdown_by": { <2>
        "operation": "terms",
        "fields": ["host.keyword"],
        "limit": 4,
        "rank_by": { "type": "alphabetical", "direction": "asc" } <3>
      },
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    }
  ],
  "styling": {
    "fitting": { "type": "linear" }
  }
}
```

1. `moving_average` over the `average` of `machine.ram` smooths out spikes and produces a trend line. `decimals: 0` keeps the byte labels clean.
2. `breakdown_by` splits the chart into one line per host, limited to the top 4 values of `host.keyword`.
3. `rank_by: "alphabetical"` is required here because `moving_average` is a pipeline aggregation and cannot be used to sort breakdown buckets.

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
  "title": "Average RAM per host",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "visible", "placement": "outside", "position": "bottom" },
  "axis": {},
  "layers": [
    {
      "type": "line",
      "x": {
        "operation": "date_histogram",
        "field": "timestamp",
        "suggested_interval": "1h"
      },
      "y": [
        {
          "operation": "moving_average", <1>
          "of": {
            "operation": "average",
            "field": "machine.ram",
            "format": { "type": "bytes", "decimals": 0 },
            "filter": { "expression": "" }
          },
          "label": "Moving average of RAM",
          "format": { "type": "bytes", "decimals": 0 },
          "filter": { "expression": "" },
          "color": {
            "type": "static",
            "color": "#6092c0"
          }
        }
      ],
      "breakdown_by": { <2>
        "operation": "terms",
        "fields": ["host.keyword"],
        "limit": 4,
        "rank_by": { "type": "alphabetical", "direction": "asc" } <3>
      },
      "data_source": {
        "type": "data_view_spec",
        "index_pattern": "kibana_sample_data_logs",
        "time_field": "timestamp"
      }
    }
  ],
  "styling": {
    "fitting": { "type": "linear" }
  }
}'
```

1. `moving_average` over the `average` of `machine.ram` smooths out spikes and produces a trend line. `decimals: 0` keeps the byte labels clean.
2. `breakdown_by` splits the chart into one line per host, limited to the top 4 values of `host.keyword`.
3. `rank_by: "alphabetical"` is required here because `moving_average` is a pipeline aggregation and cannot be used to sort breakdown buckets.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

**Unique IPs over time**
:   Visualize the number of unique client IPs throughout the day to identify traffic patterns and peak usage periods:

1. Drag `timestamp` to the **Horizontal axis** and set **Functions** to `Date histogram` with **Minimum interval** set to `Hour`.
2. Drag `clientip` to the **Vertical axis** and set the following settings:
   * **Functions**: `Unique count`
   * **Value format**: `Number`
   * **Decimals**: `0`
3. In the **Visual options**, set **Missing values** to `Linear` to connect gaps in the line.
4. Save your chart.

![Unique IPs throughout the day](../../images/kibana-lens-unique-ip-throughout-day.png "=70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

Send the following request to create a line chart that plots the unique count of client IPs over time, with linear interpolation for missing values.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "xy",
  "title": "Unique IPs over time",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto" },
  "axis": {},
  "layers": [
    {
      "type": "line",
      "x": {
        "operation": "date_histogram",
        "field": "timestamp",
        "suggested_interval": "1h" <1>
      },
      "y": [
        {
          "operation": "unique_count", <2>
          "field": "clientip",
          "label": "Unique IPs",
          "format": {
            "type": "number",
            "decimals": 0
          },
          "filter": { "expression": "" }
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
    "fitting": {
      "type": "linear" <3>
    }
  }
}
```

1. `suggested_interval: "1h"` sets the date histogram to bucket by hour.
2. `unique_count` on `clientip` counts distinct IP addresses per time bucket, tracking unique visitors rather than total requests.
3. `fitting.type: "linear"` connects data points across empty buckets with a straight line instead of leaving gaps.

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
  "title": "Unique IPs over time",
  "filters": [],
  "query": { "expression": "" },
  "legend": { "visibility": "auto" },
  "axis": {},
  "layers": [
    {
      "type": "line",
      "x": {
        "operation": "date_histogram",
        "field": "timestamp",
        "suggested_interval": "1h" <1>
      },
      "y": [
        {
          "operation": "unique_count", <2>
          "field": "clientip",
          "label": "Unique IPs",
          "format": {
            "type": "number",
            "decimals": 0
          },
          "filter": { "expression": "" }
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
    "fitting": {
      "type": "linear" <3>
    }
  }
}'
```

1. `suggested_interval: "1h"` sets the date histogram to bucket by hour.
2. `unique_count` on `clientip` counts distinct IP addresses per time bucket, tracking unique visitors rather than total requests.
3. `fitting.type: "linear"` connects data points across empty buckets with a straight line instead of leaving gaps.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

---




