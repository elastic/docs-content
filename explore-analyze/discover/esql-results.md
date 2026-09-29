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

- **Rows:** [Filter from a value](#refine-esql-query-from-table), or [sort the rows you retrieved or the full data set](#_sorting). [Show more than 1,000 rows](#esql-kibana-results-table-limitations) when the table stops early.
- **Columns:** [Show the fields you want](#esql-kibana-results-table), from the fields list or with `KEEP`. The table displays at most 50 columns.
- **Time filter and chart:** [Set the time filter for the table and the chart](#_esql_and_time_series_data). Discover applies the time filter when the data has an `@timestamp` field. If the time field has another name, name it in the query.

To keep the chart or the table, [put it on a dashboard](#_edit_the_esql_visualization).

## Before you begin

- You need an {{esql}} query in **Discover** that returns rows. If you are new to that editor, start with [Get started with {{esql}} in Discover](try-esql.md).

## Filter from a value in the results table [refine-esql-query-from-table]

Hover a value in the results table, then filter for it or filter it out. Discover adds or completes a `WHERE` clause, and the table shows the matching rows.

- {icon}`plus_circle` **Filter for this** keeps that value. For example, `WHERE host.keyword == "www.elastic.co"`.
- {icon}`minus_circle` **Filter out this** excludes that value. For example, `WHERE host.keyword != "www.elastic.co"`.

:::{note}
:applies_to: { serverless:, stack: ga 9.3+ }
Up to and including version 9.2, filtering for multi-value fields isn't supported. On later versions, filtering for multi-value fields translates into `WHERE MATCH` or `WHERE NOT MATCH` clauses. For example, `WHERE MATCH(tags.keyword, "error") AND MATCH(tags.keyword, "security")`.
:::

{{esql}} mode has no filter bar, and dragging a field onto the table does not change the query.

**Result:** When you select **Filter for this** or **Filter out this**, Discover adds or completes a `WHERE` clause for that value, and the table shows the matching rows.

## Sort query results [_sorting]

Select a column name, then select the sort order. Discover reorders only the rows the query already retrieved, and the query does not change. A `LIMIT` can make that set shorter than the full data. To sort the full data set, use the [`SORT`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-sort) command:

```esql
FROM kibana_sample_data_logs
| KEEP @timestamp, bytes, geo.dest
| SORT bytes DESC
```

**Result:** A column header reorders only the rows already retrieved. `SORT` orders the full data set.

## Show specific columns in the results table [esql-kibana-results-table]

Add a field from the [fields list](discover-get-started.md#explore-fields-in-your-data) to show it as its own column. The query stays the same. Until you add fields, the table shows a **Summary** column of each result's key-value pairs. The time field is the first column when the data has `@timestamp`, or when the query names that field.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` When the query has no command such as `KEEP` or `STATS`, the time field stays the first column after you add other fields. The time field is also included in CSV exports from **Discover** and from Discover session panels on dashboards.

To hide the time field, enable [**Hide 'Time' column** (`doc_table:hideTimeColumn`)](kibana://reference/advanced-settings.md#kibana-discover-settings).

To control which fields the query returns, use the [`KEEP`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-keep) command:

```esql
FROM kibana_sample_data_logs
| KEEP @timestamp, bytes, geo.dest
```

To display all fields as separate columns, use `KEEP *`:

```esql
FROM kibana_sample_data_logs
| KEEP *
```

:::{note}
:applies_to: { serverless: ga, stack: ga 9.4 }
When a query without a command such as `KEEP` or `STATS` returns 5 or fewer columns, **Discover** shows each column individually instead of the **Summary** column.
:::

To reorder or resize columns, adjust the table density or row height, or display the table in full-screen mode, refer to [Customize the Discover view](document-explorer.md).

## Row and column limits [esql-kibana-results-table-limitations]

If you omit `LIMIT`, the table shows up to 1,000 rows. `LIMIT` can raise that to 10,000, which is as many rows as Discover displays. Aggregations still run on the full data set.

- **Column limit:** Discover displays up to 50 columns. If a query returns more than 50 columns, only the first 50 are shown.
- **CSV export:** CSV exports from Discover are also limited to 10,000 rows. Queries and aggregations still run on the full data set.

## Show the time filter and the chart [_esql_and_time_series_data]

When the data has an `@timestamp` field, the time filter applies to the table and the chart.

If the time field has another name, name it in the query with the `?_tstart` and `?_tend` parameters. For the editor behavior, refer to [Custom time parameters](../query-filter/languages/esql-kibana.md#_custom_time_parameters).

For example, the eCommerce sample data set has no `@timestamp` field. It has an `order_date` field. This query has no time filter and no chart:

```esql
FROM kibana_sample_data_ecommerce
| KEEP customer_first_name, email, products._id.keyword
```

Add the parameters on `order_date`. Discover then shows the time filter and the chart.

```esql
FROM kibana_sample_data_ecommerce
| WHERE order_date >= ?_tstart and order_date <= ?_tend
```

**Result:** The time filter sets the time range for that table and chart.

## Keep a chart or table on a dashboard [_edit_the_esql_visualization]

When the query produces a chart, change the chart type, axes, breakdown, and colors in the visualization editor next to the chart.

To put the chart on a dashboard, follow [Add Discover visualizations to dashboards](save-open-search.md#add-discover-visualization-esql).

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` To put the current table on a dashboard, follow [Save the current table to a dashboard](save-open-search.md#save-table-to-dashboard).

To reopen the query later, [save the Discover session](save-open-search.md).

## Related pages

- [Use Discover with {{esql}}](use-esql.md)
- [Analyze your data with AI](discover-get-started.md#analyze-with-ai)
- [Inspect grouped STATS results in Discover](inspect-grouped-stats.md)
- [Save a Discover session for reuse](save-open-search.md)
- [Customize the Discover view](document-explorer.md)
