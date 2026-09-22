---
navigation_title: Work with results
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: how-to
description: Filter and sort ES|QL results in Discover, select columns, and turn on the time picker for a time field other than @timestamp.
---

# Work with {{esql}} results in Discover

After you run an {{esql}} query, filter it from a value in the results table or sort the rows you retrieved. You can also select which columns to show. If the time picker or the chart is missing, point the query at a different time field.

## Before you begin

- You need an {{esql}} query in **Discover** that returns rows. If you are new to that editor, start with [Get started with {{esql}} in Discover](try-esql.md).

## Refine an {{esql}} query from the results table [refine-esql-query-from-table]

Certain interactions with the results table of your {{esql}} query in Discover apply additional filters to your query. When hovering over a value cell, contextual options appear:

- Selecting {icon}`plus_circle` **Filter for this** adds or completes the `WHERE` command of the query to specifically look for the selected value. For example, `WHERE host.keyword == "www.elastic.co"`.
- Selecting {icon}`minus_circle` **Filter out this** adds or completes the `WHERE` command of the query to specifically exclude the selected value. For example, `WHERE host.keyword != "www.elastic.co"`.

:::{note}
:applies_to: { serverless:, stack: ga 9.3+ }
Up to and including version 9.2, filtering for multi-value fields isn't supported. On later versions, filtering for multi-value fields translates into `WHERE MATCH` or `WHERE NOT MATCH` clauses. For example, `WHERE MATCH(tags.keyword, "error") AND MATCH(tags.keyword, "security")`.
:::

Other interactions with the results table do not update the query, such as dragging fields onto the table or sorting the table in a specific order.

:::{tip}
:applies_to: {"stack": "preview 9.5", "serverless": "preview"}
You can also have an AI agent analyze your {{esql}} results, render a chart of the main finding, and suggest drill-down queries. Refer to [Analyze your data with AI](/explore-analyze/discover/discover-get-started.md#analyze-with-ai).
:::

**Result:** **Filter for this** or **Filter out this** updates the query.

## Sort query results [_sorting]

To sort on one of the columns, select the column name you want to sort on and select the sort order. This performs client-side sorting and only sorts the rows that were retrieved by the query, which might not be the full dataset because of the (implicit) limit. To sort the full data set, use the [`SORT`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-sort) command:

```esql
FROM kibana_sample_data_logs
| KEEP @timestamp, bytes, geo.dest
| SORT bytes DESC
```

**Result:** A column header reorders only the rows already retrieved. `SORT` orders the full data set.

## Show specific columns in the results table [esql-kibana-results-table]

By default, the results table shows the `@timestamp` field and a **Summary** column that lists each result's key-value pairs. To customize the visible columns without changing the query, [add fields from the fields list](discover-get-started.md#explore-fields-in-your-data).

{applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` When the query doesn't contain transformational commands such as `KEEP` or `STATS`, the time field remains the first column after you add other fields. The time field is also included in CSV exports from **Discover** and from Discover session panels on dashboards.

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
:applies_to: { stack: ga 9.4, serverless: ga }
When a query without transformational commands (such as `KEEP` or `STATS`) returns 5 or fewer columns, **Discover** shows each column individually instead of the **Summary** column.
:::

Omitting the `LIMIT` command, the results table defaults to up to 1,000 rows. Using `LIMIT`, you can increase the limit to up to 10,000 rows.

Depending on your query, **Discover** provides additional ways to display and organize the results table:

- {applies_to}`{ stack: preview 9.4, serverless: preview }` A `STATS BY` query with a single grouping field displays expandable groups. Refer to [Inspect grouped STATS results in Discover](inspect-grouped-stats.md).
- {applies_to}`{ stack: preview 9.5, serverless: preview }` A `STATS` or `INLINE STATS` query that includes a [`SPARKLINE`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions/sparkline.md) aggregation displays inline charts. To add sparklines to categorized patterns, refer to [Add sparklines to patterns](inspect-grouped-stats.md#esql-cascade-pattern-sparkline).

To reorder or resize columns, adjust the table density or row height, or display the table in full-screen mode, refer to [Customize the Discover view](document-explorer.md).

### Limitations [esql-kibana-results-table-limitations]

- **Row limit:** Discover displays up to 10,000 rows. This limit only applies to the number of rows that are retrieved by the query and displayed in Discover. Any query or aggregation runs on the full data set.
- **Column limit:** Discover displays up to 50 columns. If a query returns more than 50 columns, only the first 50 are shown.
- **CSV export:** CSV exports from Discover are also limited to 10,000 rows. Queries and aggregations still run on the full data set.
- **No data filtering UI:** The data filtering UI is not available when Discover is in {{esql}} mode. Use the [`WHERE`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-where) command instead.

  {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` When you switch from classic mode to {{esql}} mode, active filters from the filter bar are converted to `WHERE` clauses where possible, so they aren't lost. Filters that can't be converted are dropped.

## Show the time picker and chart for a time field other than @timestamp [_esql_and_time_series_data]

By default, ES|QL identifies time series data when an index contains a `@timestamp` field. This enables the time range selector and visualization options for your query.

If your index doesn't have an explicit `@timestamp` field, but has a different time field, you can still enable the time range selector and visualization options by calling the `?_tstart` and `?_tend` parameters in your query. For the editor behavior, refer to [Custom time parameters](../query-filter/languages/esql-kibana.md#_custom_time_parameters).

For example, the eCommerce sample data set doesn't have a `@timestamp` field, but has an `order_date` field.

By default, when querying this data set, time series capabilities aren't active. No visualization is generated and the time picker is unavailable.

```esql
FROM kibana_sample_data_ecommerce
| KEEP customer_first_name, email, products._id.keyword
```

While still querying the same data set, by adding the `?_tstart` and `?_tend` parameters based on the `order_date` field, **Discover** enables time series capabilities.

```esql
FROM kibana_sample_data_ecommerce
| WHERE order_date >= ?_tstart and order_date <= ?_tend
```

**Result:** The time picker and the chart are available for that query.

## Keep a chart or table on a dashboard [_edit_the_esql_visualization]

When your query produces a chart, you can change the chart type, axes, breakdown, colors, and displayed information from the visualization editor next to the chart. If you're not sure which route to go, check one of the suggestions available in the visualization editor.

You can keep what you found without saving the Discover session:

- To put the chart on a dashboard, select {icon}`app_dashboard` **Save visualization to dashboard** next to the chart (or {icon}`save` **Save visualization** in earlier versions). Refer to [Add Discover visualizations to dashboards](save-open-search.md#add-discover-visualization-esql).
- {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` To put the current table on a dashboard, select {icon}`app_dashboard` **Save table to dashboard**. Refer to [Save the current table to a dashboard](save-open-search.md#save-table-to-dashboard).

To reopen the same query, columns, tabs, and controls later, [save the Discover session](save-open-search.md).

## Related pages

- [Use Discover with {{esql}}](use-esql.md)
- [Inspect grouped STATS results in Discover](inspect-grouped-stats.md)
- [Save a Discover session for reuse](save-open-search.md)
- [Customize the Discover view](document-explorer.md)
