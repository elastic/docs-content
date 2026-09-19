---
navigation_title: Use Discover with ES|QL
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: overview
description: Use ES|QL in Discover to browse data sources, work with the results table, add variable controls, and switch back to classic mode.
---

# Use Discover with ES|QL

After you [get started with Discover using {{esql}}](try-esql.md), these jobs stay in **Discover**. They are specific to {{esql}} mode. For the editor itself, time parameters, AI assistance, and Fast mode, refer to [Use {{esql}} in the {{kib}} UI](../query-filter/languages/esql-kibana.md).

You can:

- [Browse data sources and fields from the editor](#discover-esql-resource-browsers)
- [Work with the results table](#esql-kibana-results-table)
- [Create lookup indices from Discover queries](create-lookup-indices.md)
- [Inspect grouped STATS results in Discover](inspect-grouped-stats.md)
- [Add variable controls to your queries](#add-variable-control)
- [Keep a chart or table on a dashboard](#_edit_the_esql_visualization)
- [Switch to {{esql}} or back to classic mode](#switch-discover-query-mode)

## Switch to ES|QL or classic mode [switch-discover-query-mode]

**Discover** has two query modes: {{esql}}, and classic mode (data views with KQL or Lucene).

To switch to {{esql}}:

- {icon}`code` **Query in ES|QL** (**ES|QL** or **Try ES|QL** in earlier versions) in the application menu.
- {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` **Switch to ES|QL** in the contextual menu ({icon}`boxes_vertical`) of the active Discover tab. This affects only that tab.

If you've entered a KQL or Lucene query in classic mode, Discover converts it to {{esql}}.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` Active filters from the filter bar are also converted to {{esql}} `WHERE` clauses where possible. Filters that can't be converted, such as scripted filters, are dropped.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` Discover remembers your last used query mode. The next time you open a new Discover session, it opens in the mode you last used.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` By default, Discover derives your starting query from your data sources. Administrators can set a different starting query for the space with the [**Default ES|QL query** (`discover:defaultEsqlQuery`)](kibana://reference/advanced-settings.md#kibana-discover-settings) setting. This setting doesn't apply after you edit the query or switch query modes.

### Revert to Discover's classic mode [revert-to-classic-mode]

You can go back to the classic data view and KQL mode in Discover at any time. When you switch from {{esql}} mode to classic mode, your {{esql}} query is lost.

:::::{applies-switch}

::::{applies-item} {serverless:, stack: ga 9.4+ }
1. Open the Discover tab that you want to switch to classic mode.

2. Switch the active tab from either location:

   - From the tab's contextual menu ({icon}`boxes_vertical`), select **Switch to classic**.
   - From the application menu, select **Switch to Classic**.

   This affects only the active Discover tab.

:::{tip}
The contextual menu **Switch to classic** option only appears for the currently active tab. To see it for another tab, you must load that tab first.
:::
::::

::::{applies-item} stack: ga 9.2-9.3
From the application menu, select **Switch to classic**. This only affects your current Discover tab.
::::

::::{applies-item} stack: ga 9.0-9.1
From the application menu, select **Switch to classic**.
::::

:::::

## Browse data sources and fields from the editor [discover-esql-resource-browsers]
```{applies_to}
stack: ga 9.4
serverless: ga
```

When you write a query, the {{esql}} editor includes two interactive browsers that help you find available data sources and field names:

- **Data source browser**: lists the data sources of the following types that you can query: **Alias**, [**External data**](elasticsearch://reference/query-languages/esql/esql-data-federation.md), **Index**, **Integration**, **Lookup Index**, **Stream**, and **Timeseries**. The browser supports multi-select: you can add or remove several sources in one session, and sources already present in your query appear preselected. Selections are inserted into the `FROM` or `TS` command and existing sources stay preserved. When the query starts with `TS`, only time series data sources are listed.
- **Fields browser**: lists fields for the data sources currently in your query and lets you insert one field at a time at the cursor position.

:::{note}
:applies_to: {stack: preview 9.4.0, serverless: preview}
[{{esql}} views](elasticsearch://reference/query-languages/esql/esql-views.md) aren't shown in the data source browser but they're visible through the autocomplete menu suggestions.
:::

You can open either browser from:

- **The autocomplete menu**: select **Browse data sources** (or **Browse indices** in earlier versions) when editing a `FROM` or `TS` command, or **Browse fields** when editing a position that accepts a field name (for example, after `KEEP`, `WHERE`, or `SORT`).
- **The data source badge**: the first `FROM` or `TS` keyword in the query is rendered as a clickable badge. Select it to open the data source browser.

Both browsers operate on the main query only and don't apply to subqueries.

## Work with the results table [esql-kibana-results-table]

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

### Sort query results [_sorting]

To sort on one of the columns, select the column name you want to sort on and select the sort order. This performs client-side sorting and only sorts the rows that were retrieved by the query, which might not be the full dataset because of the (implicit) limit. To sort the full data set, use the [`SORT`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-sort) command:

```esql
FROM kibana_sample_data_logs
| KEEP @timestamp, bytes, geo.dest
| SORT bytes DESC
```

## ES|QL and time series data [_esql_and_time_series_data]

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

## Keep a chart or table on a dashboard [_edit_the_esql_visualization]

When your query produces a chart, you can change the chart type, axes, breakdown, colors, and displayed information from the visualization editor next to the chart. If you're not sure which route to go, check one of the suggestions available in the visualization editor.

You can keep what you found without saving the Discover session:

- To put the chart on a dashboard, select {icon}`app_dashboard` **Save visualization to dashboard** next to the chart (or {icon}`save` **Save visualization** in earlier versions). Refer to [Add Discover visualizations to dashboards](save-open-search.md#add-discover-visualization-esql).
- {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` To put the current table on a dashboard, select {icon}`app_dashboard` **Save table to dashboard**. Refer to [Save the current table to a dashboard](save-open-search.md#save-table-to-dashboard).

To reopen the same query, columns, tabs, and controls later, [save the Discover session](save-open-search.md).

## Add variable controls to your Discover queries [add-variable-control]
```{applies_to}
stack: preview 9.2
serverless: preview
```

Variable controls help you make your queries more dynamic instead of having to maintain several versions of almost identical queries.

![Variable control in Discover](/explore-analyze/images/variable-control-discover.png " =75%")

You can add them from your Discover {{esql}} query.

:::{include} ../_snippets/variable-control-procedure.md
:::

:::{include} ../_snippets/variable-control-examples.md
:::

### Allow multi-value selections for {{esql}}-based variable controls [esql-multi-values-controls]
```{applies_to}
stack: preview 9.3
serverless: preview
```

:::{include} ../_snippets/multi-value-esql-controls.md
:::

#### Edit a variable control

Once a control is active for your query, you can still edit it by hovering over it and by selecting the {icon}`pencil` **Edit** option that appears.

You can edit all the options described in [](#add-variable-control).

When you save your edits, the control is updated for your query.

### Import a Discover query along with its controls into a dashboard [import-discover-query-with-controls]

:::{include} ../_snippets/import-discover-query-controls-into-dashboard.md
:::

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

## Related pages

- [Get started with Discover using {{esql}}](try-esql.md)
- [Create lookup indices from Discover queries](create-lookup-indices.md)
- [Inspect grouped STATS results in Discover](inspect-grouped-stats.md)
- [Save a Discover session for reuse](save-open-search.md)
- [Use {{esql}} in the {{kib}} UI](../query-filter/languages/esql-kibana.md)
- [Lens visualizations using {{esql}} queries](../visualize/esorql.md)
