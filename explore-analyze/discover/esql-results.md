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

After a query runs, you can shape what the results table shows without rewriting the query: keep or exclude rows by value, reorder them, select the columns you see, and spot where your search terms matched. This page also explains how the time filter applies to the table and the chart, and what happens when you cancel a long query.

## Before you begin

- Make sure **Discover** is in {{esql}} mode. Classic mode doesn't support this functionality. To switch, refer to [Switch to Discover's {{esql}} mode](switch-esql-mode.md#switch-discover-query-mode).
- You need an {{esql}} query that returns rows. If you're new to {{esql}} in Discover, start with [Get started with {{esql}} in Discover](try-esql.md).

## Filter from a value in the results table [refine-esql-query-from-table]

Hover over a value in the results table, then filter for it or filter it out.

- {icon}`plus_circle` **Filter for** keeps that value. For example, ``WHERE `machine.os` == "osx"``.
- {icon}`minus_circle` **Filter out** excludes that value. For example, ``WHERE `machine.os` != "osx"``.

The tooltips of these buttons read **Filter for this** or **Filter out this**, followed by the field name.

:::{image} /explore-analyze/images/kibana-discover-esql-filter-out.png
:alt: The value osx in the machine.os column, with the Filter out button available.
:screenshot:
:width: 50%
:::

:::{note}
:applies_to: { serverless: ga, stack: ga 9.3+ }
Filtering for multi-value fields translates into `WHERE MV_CONTAINS` or `WHERE NOT MV_CONTAINS` clauses. For example, ``WHERE MV_CONTAINS(`tags.keyword`, ["error", "security"]::keyword)``. If Discover can't determine the field type, it uses `MATCH` clauses instead.
:::

The query is the only place where the filter lives, so the filter shows up in the query text.

**Result:** When you select **Filter for** or **Filter out**, Discover adds or completes a `WHERE` clause for that value, and the table shows the matching rows.

:::{image} /explore-analyze/images/kibana-discover-esql-filter-where.png
:alt: An ES|QL query with a WHERE clause that excludes osx from machine.os.
:screenshot:
:width: 70%
:::

## Find similar messages in the table [find-similar-values-esql]
```{applies_to}
serverless: ga
stack: ga 9.6+
```

If one message in your results looks unusual, you can check how common it is without writing a `STATS` query that uses `CATEGORIZE`. **Discover** shows the pattern the message follows, which describes the structure that similar messages share. It also shows the other documents that match the pattern and when they occurred. You can then keep those documents in your query or filter them out.

The **Find similar values** button appears only for text fields, such as `message` or `error.message`, from a data source that has a time field. It also has these requirements:

- {applies_to}`serverless: ga` Your project type must include pattern analysis. {{es}}, Observability, and Security projects include it, except Observability projects on the Logs Essentials tier.
- {applies_to}`stack: ga 9.6+` You need a [Platinum or higher subscription](https://www.elastic.co/subscriptions) or an active trial.

1. In {{esql}} mode, run a query that returns documents. For example, run `FROM kibana_sample_data_logs` and expand the time range if the table is empty.
2. In the table, hover over a value in a text field column, such as `message`, and select **Find similar values**.
3. In the flyout, read the pattern that the message follows, the number of documents that match it, and the chart that shows when they occurred. The table in the flyout lists the matching documents. The count and the table include at most 1,000 documents. The analysis uses your query and the time filter. It ignores commands that limit, reorder, or select rows and columns, such as `LIMIT`, `SORT`, and `KEEP`.

   :::{image} /explore-analyze/images/kibana-discover-find-similar-values-esql.png
   :alt: Similar values flyout in ES|QL mode, with the pattern of a message and the chart and table of matching documents
   :screenshot:
   :width: 70%
   :::

4. Optional: To keep working with these documents, select **Open documents in Discover** to see only the documents that match the pattern. To see everything else instead, select **Filter out documents in Discover**.

**Result:** The flyout shows how common the message is and when it occurred. If you select one of the buttons in step 4, **Discover** opens a new tab, labeled **Pattern** followed by the field name, with your query plus a `WHERE` clause that keeps or excludes the matching documents. Your original tab stays as it was.

In the **Summary** column, which shows each result's key-value pairs, **Find similar values** analyzes the message of the document. For example, it uses `message`, `error.message`, or `event.original`, depending on which of these fields the document has.

In classic mode, refer to [](run-pattern-analysis-discover.md#find-similar-values-classic).

## Sort query results [_sorting]

From the menu of a column, select a sort option. The labels depend on the column type: numeric columns offer **Sort Low-High** and **Sort High-Low**, text columns offer **Sort A-Z** and **Sort Z-A**, and date columns offer **Sort Old-New** and **Sort New-Old**. Discover reorders the rows already in the table. The query stays the same, and Discover doesn't run it again. The **Summary** column doesn't offer sorting.

:::{image} /explore-analyze/images/kibana-discover-esql-sort-column.png
:alt: The menu for the bytes column, with Sort High-Low highlighted.
:screenshot:
:width: 50%
:::

**Result:** The table shows those same rows in the new order, and the query has no `SORT` command.

:::{image} /explore-analyze/images/kibana-discover-esql-sort-query.png
:alt: The ES|QL query after a column sort. The query has no SORT command.
:screenshot:
:width: 70%
:::

::::{tip}
A column sort reorders only the rows the query returned. For a `FROM` query with no `LIMIT`, that is at most 1,000 rows. To change which rows come back, add a [`SORT`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-sort) command. {{es}} orders the data, then keeps the first rows of that order. This query returns the 1,000 largest `bytes` values:

```esql
FROM kibana_sample_data_logs
| KEEP @timestamp, bytes, geo.dest
| SORT bytes DESC
```
::::

## Show specific columns in the results table [esql-kibana-results-table]

### Understand the default columns

If the query has no `KEEP`, `STATS`, or `PROMQL` command, the table shows a **Summary** column of each result's key-value pairs until you add fields. A query with one of these commands shows its result columns instead, up to the first 50 by default. The time field, which is the date field that the time filter uses, is the first column when the data has `@timestamp`, or when the query names that field.

:::{note}
:applies_to: { serverless: ga, stack: ga 9.4+ }
When a query without `KEEP`, `STATS`, or `PROMQL` returns five or fewer columns, **Discover** shows each column individually instead of the **Summary** column.
:::

{applies_to}`stack: ga` {applies_to}`serverless: unavailable` To hide the time field, enable [**Hide 'Time' column** (`doc_table:hideTimeColumn`)](kibana://reference/advanced-settings.md#kibana-discover-settings).

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` To inspect each result as an expandable tree of its fields instead of columns, set **View mode** to **JSON** in **Display options**. Refer to [View documents as JSON](document-explorer.md#document-explorer-view-mode).

### Add a column from the fields list

Add a field from the [fields list in the sidebar](explore-fields.md) to show it as its own column. The query stays the same.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` When the query has no `KEEP`, `STATS`, or `PROMQL` command, the time field stays the first column after you add other fields. CSV exports from **Discover** and from Discover session panels on dashboards also include the time field.

### Return specific fields with `KEEP`

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

### Add a calculated column with `EVAL` [esql-kibana-results-eval]

To show a value that your data doesn't store, such as a size in kilobytes, calculate it in the query with the [`EVAL`](elasticsearch://reference/query-languages/esql/commands/eval.md) command. The calculated value becomes a column in the table. It exists only in that query, so your data and any data view stay as they are. If you're used to adding a [runtime field](add-fields-to-data-views.md) in classic mode, `EVAL` serves the same purpose.

```esql
FROM kibana_sample_data_logs
| EVAL kb = bytes / 1024.0
| KEEP @timestamp, bytes, kb
```

If your query uses `KEEP`, list the new column in it, or `KEEP` removes the column.

## See highlighted matches in the results table [esql-kibana-results-highlights]

To see which words matched a full-text search, add a command or function that highlights matches to your query. **Discover** then shows each match highlighted in the results table. You don't need to change any setting.

{{es}} marks a match by wrapping it in tags. For example, it returns `The <em>Hobbit</em>`, where `<em>` and `</em>` surround the matched word. Discover reads those tags and shows the word highlighted, so the tags don't appear in the table.

Discover highlights matches for:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` The [`HIGHLIGHT`](elasticsearch://reference/query-languages/esql/commands/highlight.md) command. It writes the matches to new columns named `highlight_` plus the field name, and Discover highlights those columns. If you set your own `prefix`, `pre_tags`, or `post_tags`, the matches in the resulting columns stay highlighted.

  For example, this query returns a `highlight_title` column in which Hobbit is highlighted:

  ```esql
  ROW title = "The Hobbit"
  | HIGHLIGHT "hobbit" ON title
  | KEEP title, highlight_title
  ```

- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.5+` The [`TOP_SNIPPETS`](elasticsearch://reference/query-languages/esql/functions-operators/search-functions/top-snippets.md) function with its `highlight` option set to `true`. Discover highlights the matches in the column that holds the snippets, including when you set your own `pre_tag` and `post_tag`.

  For example, this query returns a `snippets` column in which _rabbit_ and _hole_ are highlighted:

  ```esql
  ROW chunks = ["The white rabbit disappeared down a hole."]
  | EVAL snippets = TOP_SNIPPETS(chunks, "rabbit hole", { "num_words": 0, "highlight": true })
  | KEEP snippets
  ```

## Tell whether results are approximate [esql-kibana-results-approximation]
```{applies_to}
serverless: preview
stack: preview 9.6+
```

On {{ech}}, {{ece}}, {{eck}}, and self-managed deployments, approximation requires an [Enterprise subscription](https://www.elastic.co/subscriptions). Without one, **Fast mode** is unavailable.

When {{es}} applies approximation to a query, for example because [**Fast mode**](../query-filter/languages/esql-kibana.md#esql-kibana-fast-mode-toggle) is on or the query explicitly sets [`approximation = true`](../query-filter/languages/esql-kibana.md#esql-kibana-approximation), a {icon}`bolt` badge shows next to the chart actions and in the table toolbar. Hover over the badge to see why the results are approximate. For what the badge and the extra columns mean, refer to [Interpret approximate results](../query-filter/languages/esql-kibana.md#esql-kibana-approximation-columns).

## Row and column limits [esql-kibana-results-table-limitations]

If you omit `LIMIT`, the table shows up to 1,000 rows. When a query uses `TS` with `STATS`, or `PROMQL`, the default is 10,000 rows. To show more rows, add a `LIMIT`. By default, {{es}} returns at most 10,000 rows for a query, and a higher maximum applies to queries that use `TS` with `STATS`, or `PROMQL`. Aggregations still run on the full data set. {{es}} cluster settings define these limits. Refer to [Result set size limit](elasticsearch://reference/query-languages/esql/limitations.md#esql-max-rows).

- **Column limit:** For queries that use `KEEP`, `STATS`, or `PROMQL`, Discover shows the first 50 columns by default when the query returns more.
- **Empty columns:** Discover doesn't show a column that has no value in any returned row.
- **CSV export:** A CSV report of an {{esql}} query stops at a row limit that depends on your deployment. Queries and aggregations still run on the full data set. To find the limit, refer to [](export-discover-session.md#export-discover-session-csv).

## Set the time filter for the table and the chart [_esql_and_time_series_data]

When the data has an `@timestamp` field, the time filter applies to the table and the chart.

If the time field has another name, reference it in the query with the `?_tstart` and `?_tend` parameters. These parameters hold the start and end of the time filter. For the editor behavior, refer to [Custom time parameters](../query-filter/languages/esql-kibana.md#_custom_time_parameters).

For example, the eCommerce sample data set has no `@timestamp` field. It has an `order_date` field. With this query, the time filter doesn't apply, and Discover shows no chart:

```esql
FROM kibana_sample_data_ecommerce
```

Add the parameters on `order_date`. The time filter then applies, and Discover shows the chart.

```esql
FROM kibana_sample_data_ecommerce
| WHERE order_date >= ?_tstart AND order_date <= ?_tend
| LIMIT 100
```

:::{image} /explore-analyze/images/kibana-discover-esql-order-date.png
:alt: The eCommerce sample with order_date named as the time field. The time filter and the chart are available.
:screenshot:
:::

**Result:** The time filter sets the time range for that table and chart.

## Keep the chart or the table [_edit_the_esql_visualization]

To keep the chart or the table, use one of these options:

- **Save the Discover session.** [Save and manage Discover sessions](save-open-search.md) explains the options.
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` **Save the table to a dashboard.** [Customize the table](document-explorer.md#document-explorer-customize) explains how to configure it before you [save it](use-sessions-in-dashboards.md#save-table-to-dashboard).
- **Save the chart to a dashboard.** [Change the chart type and display options](../visualize/esorql.md#_edit_and_add_from_discover) explains how to configure it before you [save it](use-sessions-in-dashboards.md#add-discover-visualization-esql).

## Cancel a query and partial results [cancel-query-in-discover]

:::{include} ../_snippets/discover-cancel-query.md
:::

:::{important}
:applies_to: { serverless: ga, stack: ga 9.1+ }
Partial results appear when an {{esql}} query times out or when you cancel it.

- The query times out. The timeout depends on your deployment and version:
  - {applies_to}`serverless: ga` In serverless projects, the timeout is fixed at 20 minutes.
  - {applies_to}`stack: ga 9.6+` The [`search:timeout`](kibana://reference/advanced-settings.md#kibana-search-settings) advanced setting defines the timeout. The default is 20 minutes (1200000 ms).
  - {applies_to}`stack: ga 9.1-9.5` The `search:timeout` advanced setting defines the timeout. The default is 10 minutes (600000 ms).
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.3+` You cancel the query.
:::

## Next steps

- To get an AI-written analysis of your results, refer to [Analyze your data with AI](analyze-discover-data-with-ai.md).
- To look inside groups of `STATS` results, refer to [Inspect grouped STATS results in Discover](inspect-grouped-stats.md).
- To keep your work, refer to [Save and manage Discover sessions](save-open-search.md).

## Related pages

- [How to query in Discover's {{esql}} mode](use-esql.md)
- [Customize the Discover view](document-explorer.md)
