---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/try-esql.html
navigation_title: Get started with ES|QL
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: tutorial
description: Query data in Discover with ES|QL, shape the table and chart, group rows, and save or share the results.
---

# Get started with {{esql}} in Discover [try-esql]

In this tutorial you query data in **Discover** with Elasticsearch Query Language ({{esql}}). The query names the data and decides which rows appear in the table and the chart. You filter, sort, and group those rows, then keep the results.

You do not need a [data view](discover-get-started.md#find-the-data-you-want-to-use), and you do not need {{esql}} experience. For the rest of Discover, refer to [Explore fields and data with Discover](discover-get-started.md). For the language itself, refer to the [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md) and [Use {{esql}} in the {{kib}} UI](../query-filter/languages/esql-kibana.md).

By the end of this tutorial, you can:

- Query a data source from **Discover**
- Add a field with the editor's suggestions
- Filter and sort the rows the table and chart show
- Group those rows with an aggregation
- Investigate from a result, or save and share the session

## Before you begin [try-esql-prerequisites]

To follow this tutorial, you need the following:

- The `enableESQL` setting enabled in {{product.kibana}} **Advanced Settings**. It is enabled by default.
- The {{product.kibana}} sample web logs. Add them from [Add sample data](/manage-data/ingest/sample-data.md). You can use your own indices instead. Replace `kibana_sample_data_logs` in the examples with a data source you can query.

## Step 1: Query a data source [tutorial-try-esql]

A source command retrieves the data. `FROM` names the indices, data streams, or aliases to query.

This tutorial uses {{esql}} mode. Classic mode uses data views with Kibana Query Language (KQL) or Lucene.

1. Find **Discover** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. If the editor is not already in {{esql}} mode, switch to it from either location:

   - {icon}`code` **Query in ES|QL** (**ES|QL** or **Try ES|QL** in earlier versions) in the application menu.
   - {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` **Switch to ES|QL** in the contextual menu ({icon}`boxes_vertical`) of the active Discover tab. This affects only that tab.

   If the editor already shows an {{esql}} query, skip this step.

3. Set the time range to **Last 7 days**.

   Sample data timestamps are relative to when you installed the set. If you added the sample web logs earlier, widen the range until the table has rows.

4. Copy the following query. To make queries easier to read, put each processing command on a new line.

    ```esql
    FROM kibana_sample_data_logs <1>
    | KEEP machine.os, machine.ram <2>
    ```

    1. Query the sample web logs you added earlier.
    2. Keep only the `machine.os` and `machine.ram` fields in the results table.

   :::{note}
   {{esql}} keywords are not case sensitive.
   :::

5. Select **Search** (or **▶Run** in earlier versions).

If that tab already has a KQL or Lucene query, Discover converts it when you switch. Switching back to classic mode does not restore that query. Refer to [Revert to Discover's classic mode](switch-esql-mode.md#revert-to-classic-mode).

**Result:** The table lists operating systems and RAM values. The chart shows those documents over the time range.

Other source commands fit other kinds of data. [`TS`](elasticsearch://reference/query-languages/esql/commands/ts.md) queries time series data streams.

{applies_to}`stack: preview 9.4` {applies_to}`serverless: preview` [`PROMQL`](elasticsearch://reference/query-languages/esql/commands/promql.md) queries time series data with PromQL syntax.

These commands are summarized in [Query structure](../query-filter/languages/esql-kibana.md#esql-kibana-query-bar). If you are not sure which names to use on your own data, refer to [Browse data sources and fields from the editor](browse-esql-sources.md).

## Step 2: Add a field with the editor

The editor suggests commands and fields as you type, so you can change the query without writing the next line from memory.

1. In the `KEEP` line, add `geo.dest` after `machine.ram`. As you type, select the field from the suggestions.

2. Select **Search** (or **▶Run** in earlier versions).

**Result:** The table includes a destination column.

The editor also includes in-app help. Refer to [Write queries with the {{esql}} editor](../query-filter/languages/esql-kibana.md#esql-kibana-get-started) for those tools, the editor search bar, and AI assistance.

## Step 3: Filter and sort the rows

Each processing command changes the rows Discover shows. `WHERE` drops rows from the table and the chart. `SORT` orders the full result. `LIMIT` shortens the table for this example.

1. Replace the query with the following:

    ```esql
    FROM kibana_sample_data_logs
    | KEEP machine.os, machine.ram, geo.dest
    | WHERE geo.dest != "GB"
    | SORT machine.ram desc
    | LIMIT 10
    ```

2. Select **Search** (or **▶Run** in earlier versions).

**Result:** The table and chart no longer include visits to Great Britain. The table lists 10 rows, sorted by RAM in descending order.

A column header reorders only the rows already retrieved. To sort the full data set, keep `SORT` in the query. Refer to [Sort query results](esql-results.md#_sorting).

## Step 4: Group the rows

`STATS` replaces the document rows with one row per group. The chart shows those aggregated values.

1. Replace the query with the following:

    ```esql
    FROM kibana_sample_data_logs
    | STATS visits = COUNT(*) BY geo.dest
    | SORT visits desc
    ```

2. Select **Search** (or **▶Run** in earlier versions).

**Result:** The table lists one row per destination and a visit count. Discover draws the chart from those aggregated rows.

Expanding a group is covered in [Inspect grouped STATS results in Discover](inspect-grouped-stats.md). For other aggregation functions, refer to the [`STATS` command reference](elasticsearch://reference/query-languages/esql/commands/stats-by.md).

## Step 5: Use the results

You can continue from a value in the table, or keep the query.

To investigate one value, filter from it in the results table. Refer to [Refine an {{esql}} query from the results table](esql-results.md#refine-esql-query-from-table).

To reopen this query, the columns, and the tabs later, select **Save** in the application menu. You can share the session, or add the session, the chart, or the table to a dashboard.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` You can save the current table to a dashboard too.

The steps are in [Save a Discover session for reuse](save-open-search.md) and [Share your Discover session](discover-get-started.md#share-your-findings).

**Result:** You can continue from a result, reopen the session, or share it.

## Next steps

- [Use Discover with ES|QL](use-esql.md): Switch modes, browse data sources, work with results, and add variable controls.
- [Create lookup indices from Discover queries](create-lookup-indices.md): Build or edit a lookup index from a `LOOKUP JOIN` command.
- [Inspect grouped STATS results in Discover](inspect-grouped-stats.md): Expand `STATS BY` groups, inspect patterns, and filter from a group.
- [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md): Commands, functions, and operators, when you want more than this session.
- [Use ES|QL in the {{kib}} UI](../query-filter/languages/esql-kibana.md): Editor tools, time parameters, AI assistance, and Fast mode.
- [Learn data exploration and visualization with Kibana](../kibana-data-exploration-learning-tutorial.md): A longer path from Discover into dashboards.

## Related pages

- [Discover](../discover.md)
- [Explore fields and data with Discover](discover-get-started.md)
- [Optimize {{esql}} query performance](elasticsearch://reference/query-languages/esql/esql-query-performance.md)
- {applies_to}`stack: ga 9.5+` [Detect change points in Discover](detect-change-points.md)
