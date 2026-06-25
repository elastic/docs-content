---
navigation_title: Tables
applies_to:
  stack: ga
  serverless: ga
description: Instructions and best practices for building tables with {{kib}} Lens in Elastic.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Build tables with {{kib}} [build-tables-with-kibana]

Tables are versatile visualizations that display your data in rows and columns, making them ideal for detailed data analysis and comparison. They're perfect for displaying multiple metrics side-by-side, showing individual records, or creating pivot tables that summarize data across different dimensions.

Tables work with any type of data: numeric values, strings, dates, and more. You can organize data using rows, add metrics to analyze, and optionally split metrics into separate columns to create pivot-style views. Tables offer extensive customization options including sorting, filtering, formatting, and coloring.

You can create tables in {{kib}} using [**Lens**](../lens.md).


![A table visualization in {{kib}}](/explore-analyze/images/table-charts.png)

## Build a table

:::{include} ../../_snippets/lens-prerequisites.md
:::

To build a table:

:::::{stepper}

::::{step} Access Lens
:::{include} ../../_snippets/access-lens.md
:::
::::

::::{step} Set the visualization to Table
New visualizations default to creating **Bar** charts. 

Using the dropdown indicating **Bar**, select **Table**.
::::

::::{step} Define the data to show
1. Select the {{data-source}} that contains your data.
2. Define your table structure by dragging fields and defining functions for one or more of these dimensions:
    - **Metrics**: The values to display in columns. You can use aggregation functions like `Sum`, `Average`, and `Count`, or create custom calculations with formulas.
    - **Rows** (optional): Fields that create the rows of your table. Each unique value becomes a row. You can use functions like **Top values**, **Date histogram**, **Intervals**, or **Filters** to organize your rows. You can add multiple fields as rows to create hierarchical groupings and break down the data more granularly.
    - **Split metrics by** (optional): Break metrics into separate columns based on a categorical field, creating a pivot table view.
3. Optionally, customize individual columns by clicking on any dimension in the layer pane to configure formatting, alignment, coloring, and more.

The table preview updates to show your metrics as columns. If you added row dimensions, each unique value creates a separate row. If you added a **Split metrics by** dimension, metrics are broken into multiple columns by category.

See [](#settings) for all configuration options for your table.
::::

::::{step} Customize the table to follow best practices
Tweak the appearance of the table to your needs. Consider the following best practices:

**Make it scannable**
:   Use consistent formatting and alignment. For example, you can right-align numbers for easier comparison, and left-align text for readability.

**Use color purposefully**
:   Apply color to values or cells to highlight important data or patterns. Avoid using too many colors that might distract from the data.

**Add context with summary rows**
:   Use summary rows to show totals, averages, or other aggregate values that help users understand the overall picture.

**Enable interactivity**
:   Turn on **Directly filter on click** to let users click on values to filter the dashboard or drill down into data.

**Control density**
:   Adjust table density based on your use case. Use **Compact** for fitting more rows, **Expanded** for better readability.

Refer to [](#settings) for a complete list of options.

For panel sizing and layout guidance, refer to [Organize dashboard panels](../../dashboards/arrange-panels.md#dashboard-grid-layout).
::::

::::{step} Save the table
:::{include} ../../_snippets/save-visualization.md
:::
::::

:::::

## Advanced table scenarios

### Create pivot tables

Tables can display data in a pivot-style format by using the **Split metrics by** dimension. This creates separate columns for each unique value of the split field, which is great for comparing metrics across different categories.

To create a pivot table:

1. Create a **Table** visualization.
2. Add a dimension to **Rows**.
3. Add one or more metrics.
4. Drag a categorical field to **Split metrics by** to create separate columns for each unique value.

For example, you could show visits per date in rows, split by the top 3 HTTP response codes, and add various metrics such as the number of unique visitors, total bytes, or the percentage of successful requests. This creates a pivot table showing the various metrics for each response code.

![Example of a table in Lens using the Split metrics by functionality](../../images/lens-table-breakdown-by-example.png)

Refer to [Analyze the data in a table](../../dashboards/create-dashboard-of-panels-with-ecommerce-data.md#view-customers-over-time-by-continents) for a detailed example.

### Use formulas in tables

Tables support Lens formulas, which let you create calculated columns with custom logic. You can use formulas to:

* Calculate percentages or ratios between metrics
* Compare current values to time-shifted values
* Apply mathematical operations across multiple fields
* Create conditional calculations

To add a formula to a table:

1. In the **Metrics** dimension, select **Add a field**.
2. Select **Formula** from the function list.
3. Enter your formula using the available functions and fields.
4. Customize the column name and formatting.

Refer to [](/explore-analyze/visualize/lens.md#lens-formulas) for formula examples, including time-shifting comparisons and mathematical operations, and the {icon}`documentation` **Formula reference** available from Lens.

### Use emojis in tables [esql-table-emojis]

:::{include} ../_snippets/emoji-table-esql.md
:::


## Table settings [settings]

Customize your table to display exactly the information you need, formatted the way you want.

### Metrics settings [metrics-options]

**Value**
:   The metrics to display in your table columns. When you drag a field onto the table, {{kib}} suggests a function based on the field type. You can change it and use aggregation functions like `Sum`, `Average`, `Count`, `Median`, and more, or create custom calculations with formulas. 

    Each metric becomes its own column in the table. If you use [**Split metrics by**](#columns-options), each metric is further split into multiple columns.

    Refer to [](/explore-analyze/visualize/lens.md#lens-formulas) for examples, or to the {icon}`documentation` **Formula reference** available from Lens.

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
:   Define the formatting and behavior of each metric column, including:
    
    - **Name**: The column header label. By default, the chart uses the function or formula name. It's a best practice to customize this with a meaningful title.
    
    :::{include} ../../_snippets/lens-tables-column-appearance-settings.md
    :::
    
    - **Summary row**: Add a row at the bottom of the table showing an aggregate value for this column. You can choose the aggregation function (`Sum`, `Average`, `Min`, `Max`, `Count`) and customize the **Summary label**.

### Rows settings [rows-options]

**Data**
:   Define which fields create the rows of your table. Drag a field to the **Rows** dimension, and {{kib}} suggests an appropriate function based on the field type. 

    - **Functions**:
      - **Top values**: Show the most common values of a categorical field. Configure the number of values to display, ranking criteria, and sort direction.
        - **Field**: Select the field to group by. You can add up to 4 fields. When multiple fields are selected, each row represents a unique combination of values across those fields. You can reorder the fields by dragging them to change their priority.
        - **Number of values**: How many top values to display. The default number of values depends on your environment:
          - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Defaults to 9.
          - {applies_to}`stack: ga 9.0-9.3` Defaults to 5.
        :::{include} ../../_snippets/lens-rank-by-options.md
        :::
        :::{include} ../../_snippets/lens-breakdown-advanced-settings.md
        :::
      - **Date histogram**: Group data by time intervals. Configure the time interval and how to handle date formatting.
        - **Field**: Select the date field to use for the time-based grouping.
        :::{include} ../../_snippets/lens-histogram-settings.md
        :::
      - **Intervals**: Create numeric ranges for continuous data. Useful for grouping numeric fields into buckets. You can define the interval granularity or specify custom ranges.
        - **Field**: Select the numeric field to create intervals from.
        :::{dropdown} How does interval granularity work?
        Interval granularity divides the field into evenly spaced intervals based on the minimum and maximum values for the field.
        
        The size of the interval is a "nice" value. When the granularity of the slider changes, the interval stays the same when the “nice” interval is the same. The minimum granularity is 1, and the maximum value is histogram:maxBars. To change the maximum granularity, go to Advanced settings.
        
        Intervals are incremented by 10, 5 or 2. For example, an interval can be `100` or `0.2`.
        :::
      - **Filters**: Define custom KQL filters to create specific row groups. Each filter creates one row in the table.

    - **Collapse by**: Aggregate rows that share the same value for this field into a single row, combining their metrics (for example, sum or average for each group). This is useful when you want to display a consolidated result for grouped values instead of individual rows.

    

**Appearance**
:   - **Name**: Customize the column header label for the row dimension.
    :::{include} ../../_snippets/lens-tables-column-appearance-settings.md
    :::
    - **Directly filter on click**: Make the values in this column clickable, so clicking a value adds a filter to your visualization or dashboard for that value. This interactivity is helpful for quickly drilling down into data.

### Split metrics by settings [columns-options]

**Data**
:   Optionally split your metrics into separate columns based on a categorical field. This creates a pivot table view where each unique value of the split field becomes its own column. This is useful for comparing the same metric across different categories side by side.

    - **Functions**:
      - **Top values**: Show the most common values of a categorical field. Configure the number of values to display, ranking criteria, and sort direction.
        - **Field**: Select the field to group by. You can add up to 4 fields. When multiple fields are selected, each column group represents a unique combination of values across those fields. You can reorder the fields by dragging them to change their priority.
        - **Number of values**: How many top values to display. The default number of values depends on your environment:
          - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Defaults to 9.
          - {applies_to}`stack: ga 9.0-9.3` Defaults to 3.
        :::{include} ../../_snippets/lens-rank-by-options.md
        :::
        :::{include} ../../_snippets/lens-breakdown-advanced-settings.md
        :::
      - **Date histogram**: Group data by time intervals. Configure the time interval and how to handle date formatting.
        - **Field**: Select the date field to use for the time-based grouping.
        :::{include} ../../_snippets/lens-histogram-settings.md
        :::
      - **Intervals**: Create numeric ranges for continuous data. Useful for grouping numeric fields into buckets. You can define the interval granularity or specify custom ranges.
        - **Field**: Select the numeric field to create intervals from.
        :::{dropdown} How does interval granularity work?
        Interval granularity divides the field into evenly spaced intervals based on the minimum and maximum values for the field.
        
        The size of the interval is a "nice" value. When the granularity of the slider changes, the interval stays the same when the “nice” interval is the same. The minimum granularity is 1, and the maximum value is histogram:maxBars. To change the maximum granularity, go to Advanced settings.
        
        Intervals are incremented by 10, 5 or 2. For example, an interval can be `100` or `0.2`.
        :::
      - **Filters**: Define custom KQL filters to create specific column groups. Each filter creates one column in the table. 

**Appearance**
:   - **Name**: Customize the split dimension. This name is not used on the table.


### General table settings [appearance-options]

When creating or editing a table visualization, you can customize several appearance options. To do that, look for the {icon}`brush` icon.

**Density** {applies_to}`stack: ga 9.1` {applies_to}`serverless: ga`
:   Control how much space each row occupies. Choose between:
    - **Compact**: Minimal spacing, fits more rows in less space
    - **Normal**: Balanced spacing (default)
    - **Expanded**: More generous spacing for improved readability

**Max header cell lines**
:   Set the maximum number of lines that column headers can span. When header text is longer than this setting, it is truncated with an ellipsis. Use `Auto` to let {{kib}} determine the appropriate height, or set a specific number like `1`, `2`, or `3`.

**Body cell lines**
:   Set the number of lines that body cells display. When cell content exceeds this limit, it is truncated with an ellipsis. Use `Auto` to automatically adjust based on content, or set a specific number like `1`, `2`, or `3` for consistent row heights. Setting this to `1` creates more compact tables, while higher values allow more content to be visible.

**Paginate table**
:   Toggle pagination on or off. When enabled:
    - The table displays a limited number of rows per page.
    - Navigation controls appear at the bottom of the table when the table contains at least 10 items. By default, 10 rows appear per page. Users of the dashboard will be able to select a different number.
    - This is helpful for tables with many rows to improve performance and readability.
    
    When disabled, all rows appear in a scrollable view (up to the maximum returned by the query).

**Show row numbers** {applies_to}`stack: ga 9.4` {applies_to}`serverless: ga`
:   Toggle a leading column that numbers each row in the table. Turned on by default for new tables, and turned off by default for tables that were saved before this option was introduced. When pagination is turned on, numbering restarts at `1` on each page.

## Table examples

<!-- MAINTENANCE: the API payload examples in this section were verified
against the Visualizations API spec. To re-verify after a schema change, run:
  KIBANA_URL=… API_KEY=… python3 .github/scripts/verify-lens-api-examples.py --file tables.md
See .github/scripts/verify-lens-api-examples.py for full usage. -->

The following examples show various configuration options you can use for building effective tables.

**Top pages by unique visitors**
:   Display the most visited pages on your website with the number of unique visitors:

    * **Rows**: `request.keyword` field using **Top values** function
      * **Number of values**: `5`
      * **Advanced**: Group remaining values as "Other"
    * **Metrics**: `clientip` field using **Unique count** function
      * **Value format**: `Number`
      * **Text alignment**: `Right`

![Table showing top pages by unique visitors](../../images/kibana-table-with-request-keyword-and-client-ip-8.16.0.png "=70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

Send the following request to create a table that displays the top 5 request pages ranked by unique visitor count.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "data_table",
  "title": "Top pages by unique visitors",
  "filters": [],
  "query": { "expression": "" },
  "rows": [
    {
      "operation": "terms", <1>
      "fields": ["request.keyword"],
      "limit": 5,
      "other_bucket": { "include_documents_without_field": false }
    }
  ],
  "metrics": [
    {
      "operation": "unique_count", <2>
      "field": "clientip",
      "label": "Unique visitors",
      "format": { "type": "number" },
      "filter": { "expression": "" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": { "density": { "mode": "default" } }
}
```

1. Uses `terms` on `request.keyword` to create one row per top page, limited to 5.
2. Counts unique values of `clientip` to measure distinct visitors per page.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "data_table",
  "title": "Top pages by unique visitors",
  "filters": [],
  "query": { "expression": "" },
  "rows": [
    {
      "operation": "terms", <1>
      "fields": ["request.keyword"],
      "limit": 5,
      "other_bucket": { "include_documents_without_field": false }
    }
  ],
  "metrics": [
    {
      "operation": "unique_count", <2>
      "field": "clientip",
      "label": "Unique visitors",
      "format": { "type": "number" },
      "filter": { "expression": "" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": { "density": { "mode": "default" } }
}'
```

1. Uses `terms` on `request.keyword` to create one row per top page, limited to 5.
2. Counts unique values of `clientip` to measure distinct visitors per page.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

**Sales by date and continent (pivot table)**
:   Create a pivot table showing customer counts across different continents over time:

    * **Rows**: `order_date` field using **Date histogram** function
      * **Minimum interval**: `1d`
      * **Name**: `Sales per day`
    * **Metrics**: `customer_id` field using **Unique count** function
    * **Split metrics by**: `geoip.continent_name` field using **Top values** set to `3`
      * **Advanced**: Group remaining values as "Other"

![Table showing customers over time by continent](../../images/kibana-lens_table_over_time.png "=70%")

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

Send the following request to create a pivot table that shows unique customer counts per day, split into columns by the top 3 continents.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "data_table",
  "title": "Sales by date and continent",
  "filters": [],
  "query": { "expression": "" },
  "rows": [
    {
      "operation": "date_histogram", <1>
      "field": "order_date",
      "suggested_interval": "1d",
      "label": "Sales per day"
    }
  ],
  "metrics": [
    {
      "operation": "unique_count", <2>
      "field": "customer_id",
      "label": "Unique customers",
      "format": { "type": "number", "decimals": 0 },
      "filter": { "expression": "" }
    }
  ],
  "split_metrics_by": [ <3>
    {
      "operation": "terms",
      "fields": ["geoip.continent_name"],
      "limit": 3,
      "other_bucket": { "include_documents_without_field": false }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_ecommerce",
    "time_field": "order_date"
  },
  "styling": { "density": { "mode": "default" } }
}
```

1. Groups rows by `order_date` using a date histogram.
2. Counts unique `customer_id` values as the table metric.
3. Splits the metric into separate columns for the top 3 continents.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "data_table",
  "title": "Sales by date and continent",
  "filters": [],
  "query": { "expression": "" },
  "rows": [
    {
      "operation": "date_histogram", <1>
      "field": "order_date",
      "suggested_interval": "1d",
      "label": "Sales per day"
    }
  ],
  "metrics": [
    {
      "operation": "unique_count", <2>
      "field": "customer_id",
      "label": "Unique customers",
      "format": { "type": "number", "decimals": 0 },
      "filter": { "expression": "" }
    }
  ],
  "split_metrics_by": [ <3>
    {
      "operation": "terms",
      "fields": ["geoip.continent_name"],
      "limit": 3,
      "other_bucket": { "include_documents_without_field": false }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_ecommerce",
    "time_field": "order_date"
  },
  "styling": { "density": { "mode": "default" } }
}'
```

1. Groups rows by `order_date` using a date histogram.
2. Counts unique `customer_id` values as the table metric.
3. Splits the metric into separate columns for the top 3 continents.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

**Document comparison with custom ranges**
:   Compare metrics across custom-defined ranges:

    * **Rows**: `bytes` field using **Intervals** function
      * **Ranges**: 
        * `0` → `10240`, labeled `Below 10KB`
        * `10240` → `+∞`, labeled `Above 10KB`
      * **Name**: `File size`
    * **Metrics**: `bytes` field using **Sum** function
      * **Name**: `Total bytes transferred`
      * **Value format**: `Bytes`
      * **Text alignment**: `Right`
    * **Additional styling**:
      * **Color by value**: Dynamic coloring to highlight ranges with higher byte transfers

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

Send the following request to create a table that compares total bytes transferred across custom-defined file size ranges.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "data_table",
  "title": "Document comparison with custom ranges",
  "filters": [],
  "query": { "expression": "" },
  "rows": [
    {
      "operation": "range", <1>
      "field": "bytes",
      "ranges": [
        { "lte": 10240, "label": "Below 10KB" },
        { "gt": 10240, "label": "Above 10KB" }
      ], <2>
      "label": "File size"
    }
  ],
  "metrics": [
    {
      "operation": "sum", <3>
      "field": "bytes",
      "label": "Total bytes transferred",
      "format": { "type": "bytes" },
      "alignment": "right",
      "color": { "type": "auto" },
      "apply_color_to": "value",
      "filter": { "expression": "" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": { "density": { "mode": "default" } }
}
```

1. Uses a `range` operation to create custom row buckets from the `bytes` field.
2. Defines two ranges, each with a label: documents up to 10 KB (`Below 10KB`) and documents above 10 KB (`Above 10KB`).
3. The `sum` metric sums the `bytes` field within each range, right-aligns the column, and applies dynamic `auto` coloring to highlight ranges with higher byte transfers.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "data_table",
  "title": "Document comparison with custom ranges",
  "filters": [],
  "query": { "expression": "" },
  "rows": [
    {
      "operation": "range", <1>
      "field": "bytes",
      "ranges": [
        { "lte": 10240, "label": "Below 10KB" },
        { "gt": 10240, "label": "Above 10KB" }
      ], <2>
      "label": "File size"
    }
  ],
  "metrics": [
    {
      "operation": "sum", <3>
      "field": "bytes",
      "label": "Total bytes transferred",
      "format": { "type": "bytes" },
      "alignment": "right",
      "color": { "type": "auto" },
      "apply_color_to": "value",
      "filter": { "expression": "" }
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_logs",
    "time_field": "timestamp"
  },
  "styling": { "density": { "mode": "default" } }
}'
```

1. Uses a `range` operation to create custom row buckets from the `bytes` field.
2. Defines two ranges, each with a label: documents up to 10 KB (`Below 10KB`) and documents above 10 KB (`Above 10KB`).
3. The `sum` metric sums the `bytes` field within each range, right-aligns the column, and applies dynamic `auto` coloring to highlight ranges with higher byte transfers.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::

**Weekly sales with percentage change**
:   Show week-over-week sales trends with calculated percentage changes:

    * **Rows**: `order_date` field using **Date histogram** function
      * **Minimum interval**: `1w`
      * **Name**: `Week`
    * **Metrics** (two columns):
      1. `Records` using **Count** function
         * **Name**: `Orders this week`
         * **Value format**: `Number`, 0 decimals
      2. **Formula**: `count() / count(shift='1w') - 1`
         * **Name**: `Change from last week`
         * **Value format**: `Percent`, 2 decimals
         * **Text alignment**: `Right`

:::::::{dropdown} Create this chart using the API
:applies_to: { stack: preview 9.4, serverless: preview }

Send the following request to create a table that shows weekly order counts alongside a formula-based percentage change column.


:::::{tab-set}

::::{tab-item} Console
:sync: api-console
```console
POST kbn://api/visualizations
{
  "type": "data_table",
  "title": "Weekly sales with percentage change",
  "filters": [],
  "query": { "expression": "" },
  "rows": [
    {
      "operation": "date_histogram", <1>
      "field": "order_date",
      "suggested_interval": "1w",
      "label": "Week"
    }
  ],
  "metrics": [
    {
      "operation": "count",
      "label": "Orders this week",
      "format": { "type": "number", "decimals": 0 },
      "filter": { "expression": "" }
    },
    {
      "operation": "formula", <2>
      "formula": "count() / count(shift='1w') - 1", <3>
      "label": "Change from last week",
      "format": { "type": "percent", "decimals": 2 },
      "alignment": "right"
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_ecommerce",
    "time_field": "order_date"
  },
  "styling": { "density": { "mode": "default" } }
}
```

1. Groups rows by `order_date` with a weekly date histogram.
2. Uses a `formula` metric to compute a calculated column. Formula metrics must not include a `filter` field — omitting it is required for time shift to work correctly.
3. Divides the current week's count by the previous week's count and subtracts 1 to get the percentage change.

::::

::::{tab-item} curl
:sync: api-curl
```bash
curl -X POST "${KIBANA_URL}/api/visualizations" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "data_table",
  "title": "Weekly sales with percentage change",
  "filters": [],
  "query": { "expression": "" },
  "rows": [
    {
      "operation": "date_histogram", <1>
      "field": "order_date",
      "suggested_interval": "1w",
      "label": "Week"
    }
  ],
  "metrics": [
    {
      "operation": "count",
      "label": "Orders this week",
      "format": { "type": "number", "decimals": 0 },
      "filter": { "expression": "" }
    },
    {
      "operation": "formula", <2>
      "formula": "count() / count(shift='1w') - 1", <3>
      "label": "Change from last week",
      "format": { "type": "percent", "decimals": 2 },
      "alignment": "right"
    }
  ],
  "data_source": {
    "type": "data_view_spec",
    "index_pattern": "kibana_sample_data_ecommerce",
    "time_field": "order_date"
  },
  "styling": { "density": { "mode": "default" } }
}'
```

1. Groups rows by `order_date` with a weekly date histogram.
2. Uses a `formula` metric to compute a calculated column. Formula metrics must not include a `filter` field — omitting it is required for time shift to work correctly.
3. Divides the current week's count by the previous week's count and subtracts 1 to get the percentage change.

::::

:::::

For more information, refer to the [Visualizations API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations).
:::::::
