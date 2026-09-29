---
navigation_title: Work with results
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: how-to
description: Filter and sort ES|QL results in Discover, select columns, and turn on the time filter for a time field other than @timestamp.
---

# Work with {{esql}} results in Discover

After an {{esql}} query runs in **Discover**, the results table shows what that query returned. You can filter the rows, sort them, and show the fields you want. You can also set the time filter, and the table and the chart use that time range.

- **Rows:** [Filter from a value](#refine-esql-query-from-table), or [sort the rows in the table, or change which rows come back](#_sorting). [Show more than 1,000 rows](#esql-kibana-results-table-limitations) with `LIMIT`.
- **Columns:** [Show the fields you want](#esql-kibana-results-table), from the fields list or with `KEEP`. The table displays at most 50 columns.
- **Time filter and chart:** [Set the time filter for the table and the chart](#_esql_and_time_series_data). Discover applies the time filter when the data has an `@timestamp` field. If the time field has another name, name it in the query.

To keep the chart or the table, [put it on a dashboard](#_edit_the_esql_visualization).

## Before you begin

- You need an {{esql}} query in **Discover** that returns rows. If you are new to that editor, start with [Get started with {{esql}} in Discover](try-esql.md).

## Filter from a value in the results table [refine-esql-query-from-table]

Hover over a value in the results table, then filter for it or filter it out.

- {icon}`plus_circle` **Filter for this** keeps that value. For example, `WHERE host.keyword == "www.elastic.co"`.
- {icon}`minus_circle` **Filter out this** excludes that value. For example, `WHERE host.keyword != "www.elastic.co"`.

  :::{image} /explore-analyze/images/kibana-discover-esql-filter-out.png
  :alt: The value ios in the machine.os column, with Filter out this available.
  :screenshot:
  :width: 50%
  :::

:::{note}
:applies_to: { serverless: ga, stack: ga 9.3+ }
Filtering for multi-value fields translates into `WHERE MATCH` or `WHERE NOT MATCH` clauses. For example, `WHERE MATCH(tags.keyword, "error") AND MATCH(tags.keyword, "security")`.
:::

{{esql}} mode has no filter bar, and dragging a field onto the table doesn't change the query.

**Result:** When you select **Filter for this** or **Filter out this**, Discover adds or completes a `WHERE` clause for that value, and the table shows the matching rows.

:::{image} /explore-analyze/images/kibana-discover-esql-filter-where.png
:alt: An ES|QL query with a WHERE clause that excludes ios from machine.os.
:screenshot:
:width: 70%
:::

## Sort query results [_sorting]

From the menu of a column, select **Sort High-Low** or **Sort Low-High**. Discover reorders the rows already in the table. The query stays the same, and Discover doesn't run it again.

:::{image} /explore-analyze/images/kibana-discover-esql-sort-column.png
:alt: The menu for the bytes column, with Sort High-Low highlighted.
:screenshot:
:width: 50%
:::

**Result:** The table shows those same rows in the new order. The query doesn't change.

:::{image} /explore-analyze/images/kibana-discover-esql-sort-query.png
:alt: The ES|QL query after a column sort. The query has no SORT command.
:screenshot:
:width: 70%
:::

::::{tip}
A column sort reorders only the rows the query returned. With no `LIMIT`, that is at most 1,000 rows. To change which rows come back, add a [`SORT`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-sort) command. {{es}} orders the data, then keeps the first rows of that order. This query returns the 1,000 largest `bytes` values:

```esql
FROM kibana_sample_data_logs
| KEEP @timestamp, bytes, geo.dest
| SORT bytes DESC
```
::::

## Show specific columns in the results table [esql-kibana-results-table]

### The Summary column and the time field

Until you add fields, the table shows a **Summary** column of each result's key-value pairs. The time field is the first column when the data has `@timestamp`, or when the query names that field.

:::{note}
:applies_to: { serverless: ga, stack: ga 9.4+ }
When a query without a command such as `KEEP` or `STATS` returns five or fewer columns, **Discover** shows each column individually instead of the **Summary** column.
:::

To hide the time field, enable [**Hide 'Time' column** (`doc_table:hideTimeColumn`)](kibana://reference/advanced-settings.md#kibana-discover-settings).

### Add a column from the fields list

Add a field from the [fields list](discover-get-started.md#explore-fields-in-your-data) to show it as its own column. The query stays the same.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` When the query has no command such as `KEEP` or `STATS`, the time field stays the first column after you add other fields. The time field is also included in CSV exports from **Discover** and from Discover session panels on dashboards.

### Return specific fields with KEEP

To control which fields the query returns, use the [`KEEP`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-keep) command:

```esql
FROM kibana_sample_data_logs
| KEEP bytes, geo.dest, machine.os, response.keyword
```

:::{image} /explore-analyze/images/kibana-discover-esql-keep-time-filter.png
:alt: A KEEP query that omits @timestamp. The time filter is set, and the chart and table use that range.
:screenshot:
:::

To display all fields as separate columns, use `KEEP *`:

```esql
FROM kibana_sample_data_logs
| KEEP *
```

## Row and column limits [esql-kibana-results-table-limitations]

If you omit `LIMIT`, the table shows up to 1,000 rows. `LIMIT` can raise that to 10,000, which is as many rows as Discover displays. Aggregations still run on the full data set.

- **Column limit:** Discover displays up to 50 columns. If a query returns more than 50 columns, only the first 50 are shown.
- **CSV export:** CSV exports from Discover are also limited to 10,000 rows. Queries and aggregations still run on the full data set.

## Set the time filter for the table and the chart [_esql_and_time_series_data]

When the data has an `@timestamp` field, the time filter applies to the table and the chart.

If the time field has another name, name it in the query with the `?_tstart` and `?_tend` parameters. For the editor behavior, refer to [Custom time parameters](../query-filter/languages/esql-kibana.md#_custom_time_parameters).

For example, the eCommerce sample data set has no `@timestamp` field. It has an `order_date` field. With this query, the time filter doesn't apply, and Discover shows no chart:

```esql
FROM kibana_sample_data_ecommerce
```

Add the parameters on `order_date`. The time filter then applies, and Discover shows the chart.

```esql
FROM kibana_sample_data_ecommerce
| WHERE order_date >= ?_tstart AND order_date <= ?_tend
```

:::{image} /explore-analyze/images/kibana-discover-esql-order-date.png
:alt: The eCommerce sample with order_date named as the time field. The time filter and the chart are available.
:screenshot:
:::

**Result:** The time filter sets the time range for that table and chart.

## Keep a chart or table on a dashboard [_edit_the_esql_visualization]

To keep the chart or the table, use one of these options:

- **Save the Discover session.** [Save a Discover session for reuse](save-open-search.md) explains the options.
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` **Save the table to a dashboard.** [Customize the table](document-explorer.md#document-explorer-customize) explains how to configure it before you [save it](save-open-search.md#save-table-to-dashboard).
- **Save the chart to a dashboard.** [Change the chart type and display options](../visualize/esorql.md#_edit_and_add_from_discover) explains how to configure it before you [save it](save-open-search.md#add-discover-visualization-esql).

## Related pages

- [Use Discover with {{esql}}](use-esql.md)
- [Analyze your data with AI](discover-get-started.md#analyze-with-ai)
- [Inspect grouped STATS results in Discover](inspect-grouped-stats.md)
- [Save a Discover session for reuse](save-open-search.md)
- [Customize the Discover view](document-explorer.md)
