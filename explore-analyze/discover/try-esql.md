---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/try-esql.html
navigation_title: Get started with ES|QL
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: tutorial
description: Query data in Discover with ES|QL, shape the table and chart, group rows, and save or share the results.
---

# Get started with {{esql}} in Discover [try-esql]

In this tutorial you query data in **Discover** with Elasticsearch Query Language ({{esql}}). The query names the data and decides which rows appear in the table and the chart. You filter, sort, and group those rows, then keep the results.

You do not need a [data view](discover-get-started.md#find-the-data-you-want-to-use), and you do not need {{esql}} experience. For the rest of Discover, refer to [Explore fields and data with Discover](discover-get-started.md). For the language itself, refer to the [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md).

By the end of this tutorial, you can:

- Query a data source from **Discover**
- Add a field with the editor's suggestions
- Filter and sort the rows the table and chart show
- Group those rows with an aggregation
- Narrow the results to one value, or save the session so you can reopen it

## Before you begin [try-esql-prerequisites]

To follow this tutorial, you need the following:

- The `enableESQL` setting enabled in {{product.kibana}} **Advanced Settings**. It is enabled by default.
- The {{product.kibana}} sample web logs. Add them from [Add sample data](/manage-data/ingest/sample-data.md). You can use your own indices instead. Replace `kibana_sample_data_logs` in the examples with a data source you can query.

## Step 1: Query a data source [tutorial-try-esql]

Name the data in the query. `FROM` reads an index, a data stream, or an alias. This tutorial uses the sample web logs. If your data is a time series data stream, use [`TS`](elasticsearch://reference/query-languages/esql/commands/ts.md) instead.

{applies_to}`serverless: preview` {applies_to}`stack: preview 9.4` If the data is PromQL, use [`PROMQL`](elasticsearch://reference/query-languages/esql/commands/promql.md).

To name a different kind of data, refer to [source commands](elasticsearch://reference/query-languages/esql/esql-commands.md#esql-source-commands).

1. Find **Discover** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. If the editor is not already in {{esql}} mode, switch to it from either location:

   - {icon}`code` **Query in ES|QL** (**ES|QL** or **Try ES|QL** in earlier versions) in the application menu.
   - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` **Switch to ES|QL** in the contextual menu ({icon}`boxes_vertical`) of the active Discover tab. This affects only that tab.

   If the editor already shows an {{esql}} query, skip this step. If the tab already has a KQL or Lucene query, Discover converts it when you switch. Switching back to classic mode does not restore that query. Refer to [Revert to Discover's classic mode](switch-esql-mode.md#revert-to-classic-mode).

3. Set the time range to **Last 7 days**.

   Sample data timestamps are relative to when you installed the set. If you added the sample web logs earlier, widen the range until the table has rows.

4. Copy the following query. `from` and `FROM` are the same command.

    On your own data, replace `kibana_sample_data_logs` with a source you can query. If you do not know the name, [browse data sources from the editor](browse-esql-sources.md).

    ```esql
    FROM kibana_sample_data_logs <1>
    | KEEP machine.os, machine.ram <2>
    ```

    1. Query the sample web logs you added earlier.
    2. Show only `machine.os` and `machine.ram` as columns. The query selects the columns, not a data view.

    {applies_to}`serverless: preview` {applies_to}`stack: preview 9.5+` You can describe this query instead of copying it. In the editor search bar, select **Natural language**, for example `operating system and RAM from the sample web logs`. Refer to [Generate a full query from natural language](../query-filter/languages/esql-kibana.md#esql-kibana-quick-search-nl).

5. Select **Search** (or **▶Run** in earlier versions).

   {applies_to}`serverless: preview` {applies_to}`stack: preview 9.5+` If the editor underlines the query, select **Fix with AI** on the error. Refer to [Fix query errors with AI](../query-filter/languages/esql-kibana.md#esql-kibana-ai-fix).

**Result:** The table lists operating systems and RAM values. The chart shows those documents over the time range.

## Step 2: Add a field with the editor

Add the destination so you can see where the visits went. The same visits stay in the table, with a `geo.dest` column.

Type `geo.dest` on the `KEEP` line and select it from the suggestions. Autocomplete offers the field name as you type. Refer to [Autocomplete and in-app help](../query-filter/languages/esql-kibana.md#esql-kibana-autocomplete). You can also copy the query.

1. Copy this query if you did not add the field yourself.

    ```esql
    FROM kibana_sample_data_logs
    | KEEP machine.os, machine.ram, geo.dest
    ```

2. Select **Search** (or **▶Run** in earlier versions).

**Result:** The table includes a `geo.dest` column.

## Step 3: Filter and sort the rows

Drop visits to Great Britain, and show the 10 rows with the most RAM. `WHERE` removes those visits from the table and the chart. `SORT` orders the full result first, so `LIMIT 10` keeps the highest RAM values rather than any 10 rows.

If you type the query on one line, select {icon}`line_break` **Prettify query** to put each command on its own line. Refer to [Query formatting](../query-filter/languages/esql-kibana.md#_make_your_query_readable).

{applies_to}`serverless: preview` {applies_to}`stack: preview 9.3+` You can open the editor search bar and type a KQL filter instead of writing `WHERE`. The editor inserts a `WHERE KQL()` command. Refer to [Build {{esql}} queries from KQL syntax](../query-filter/languages/esql-kibana.md#esql-kibana-quick-search).

1. Copy the following query.

    ```esql
    FROM kibana_sample_data_logs
    | KEEP machine.os, machine.ram, geo.dest
    | WHERE geo.dest != "GB"
    | SORT machine.ram desc
    | LIMIT 10
    ```

2. Select **Search** (or **▶Run** in earlier versions).

**Result:** The table and chart no longer include visits to Great Britain. The table lists 10 rows, sorted by RAM in descending order.

A column header reorders only the rows already retrieved. `SORT` is what orders the full data set. Refer to [Sort query results](esql-results.md#_sorting).

## Step 4: Group the rows

Count the visits for each destination. `STATS` turns the visits into one row per destination, and the chart shows those counts.

{applies_to}`serverless: preview` {applies_to}`stack: preview 9.5+` You can generate that pipe instead of typing it. Add `// count visits by destination`, then press {kbd}`cmd+J` (Mac) or {kbd}`ctrl+J` (Windows/Linux). Refer to [Generate {{esql}} from a comment](../query-filter/languages/esql-kibana.md#esql-kibana-ai-comment).

1. Copy the following query.

    ```esql
    FROM kibana_sample_data_logs
    | STATS visits = COUNT(*) BY geo.dest
    | SORT visits desc
    ```

2. Select **Search** (or **▶Run** in earlier versions).

**Result:** The table lists one row per destination and a visit count. Discover draws the chart from those aggregated rows.

To see the visits inside a destination, open the group. Refer to [Inspect grouped STATS results in Discover](inspect-grouped-stats.md). To count another value, such as total bytes, refer to the [`STATS` command reference](elasticsearch://reference/query-languages/esql/commands/stats-by.md). If this aggregation is slow on your data, refer to [Optimize {{esql}} query performance](elasticsearch://reference/query-languages/esql/esql-query-performance.md).

## Step 5: Use the results

Narrow these counts, ask what they mean, or save them. The query is:

```esql
FROM kibana_sample_data_logs
| STATS visits = COUNT(*) BY geo.dest
| SORT visits desc
```

To stay on one destination, filter from that value in the results table. Discover adds a `WHERE` clause for you. Refer to [Refine an {{esql}} query from the results table](esql-results.md#refine-esql-query-from-table).

{applies_to}`serverless: preview` {applies_to}`stack: preview 9.5` To ask what the pattern means, select **AI Agent** in the {{kib}} header. The agent uses this query and these rows. Refer to [Analyze your data with AI](discover-get-started.md#analyze-with-ai).

Select **Save** in the application menu to reopen this query later. To share it, or to put the chart or the table on a dashboard, follow [Save a Discover session for reuse](save-open-search.md) and [Share your Discover session](discover-get-started.md#share-your-findings).

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` You can save the current table to a dashboard too.

**Result:** After you save, you can reopen this query. You can also share it.

## Next steps

- [Use Discover with ES|QL](use-esql.md): Switch modes, browse data sources, work with results, and add variable controls.
- [Create lookup indices from Discover queries](create-lookup-indices.md): Build or edit a lookup index from a `LOOKUP JOIN` command.
- [Inspect grouped STATS results in Discover](inspect-grouped-stats.md): Expand `STATS BY` groups, inspect patterns, and filter from a group.
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` [Detect change points in Discover](detect-change-points.md): Find a spike, dip, or shift in a time series.
- [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md): Commands, functions, and operators, when you want more than this session.
- [Use ES|QL in the {{kib}} UI](../query-filter/languages/esql-kibana.md): Editor tools, time parameters, AI assistance, and Fast mode.
- [Learn data exploration and visualization with Kibana](../kibana-data-exploration-learning-tutorial.md): A longer path from Discover into dashboards.

## Related pages

- [Discover](../discover.md)
- [Explore fields and data with Discover](discover-get-started.md)
- [Optimize {{esql}} query performance](elasticsearch://reference/query-languages/esql/esql-query-performance.md)
