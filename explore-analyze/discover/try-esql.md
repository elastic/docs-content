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
description: Learn how ES|QL commands change the results you see in Discover, by building one query step by step on the sample web logs.
---

# Get started with {{esql}} in Discover [try-esql]

In this tutorial, you explore the {{kib}} sample web logs in **Discover** with Elasticsearch Query Language ({{esql}}). You build one query, one command at a time, and see how each command changes the results in the table and the chart.

You do not need a [data view](discover-get-started.md#find-the-data-you-want-to-use), and you do not need {{esql}} experience. For the rest of Discover, refer to [Explore fields and data with Discover](discover-get-started.md). For the language itself, refer to the [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md).

By the end of this tutorial, you'll know the main elements of your query and how they shape the results you see in **Discover**.

## Before you begin [try-esql-prerequisites]

To follow this tutorial, you need the following:

- The `enableESQL` setting enabled in {{product.kibana}} **Advanced Settings**. It is enabled by default.
- The {{product.kibana}} sample web logs. Add them from [Add sample data](/manage-data/ingest/sample-data.md). You can use your own indices instead. Replace `kibana_sample_data_logs` in the examples with a data source you can query.

## Query a data source [tutorial-try-esql]

In {{esql}} mode, the query decides which data you explore. There is no data view to select like in classic mode. Instead, the first command of every query names the data source, and the table and the chart show what that source returns.

This first command is a [source command](elasticsearch://reference/query-languages/esql/esql-commands.md#esql-source-commands). 
- [`FROM`](elasticsearch://reference/query-languages/esql/commands/from.md) is {{esql}}'s generic source command. It takes the names of the sources to read, for example an index or a data stream. You can list several names or match them with a wildcard, such as `FROM logs-*`.
- Other source commands serve specific cases. For example, [`TS`](elasticsearch://reference/query-languages/esql/commands/ts.md) queries time series data streams, and [`PROMQL`](elasticsearch://reference/query-languages/esql/commands/promql.md) runs a PromQL query. 

Command names are not case-sensitive, so `from` and `FROM` are the same.

1. Open **Discover** from the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. If the editor is not in {{esql}} mode yet, switch to it. Refer to [Switch between {{esql}} and classic mode](switch-esql-mode.md#switch-discover-query-mode).
3. Set the time filter to the 7 days before you installed the sample data. If you installed it today, select **Last 7 days**. Otherwise, [set a custom range](/explore-analyze/query-filter/filtering.md#set-time-filter) that ends on the installation date.

   The sample web logs have an `@timestamp` field, so Discover connects the results to it. The time filter keeps only the results in the range you pick, and the chart shows how they spread over that range.

   :::{tip}
   If your time field has a name other than `@timestamp`, you can name it in the query to bind it to the time filter. If your data has no time field, Discover shows no time filter and no chart. Refer to [Set the time filter for the table and the chart](esql-results.md#_esql_and_time_series_data).
   :::

4. Enter the following query in the editor:

   ```esql
   FROM kibana_sample_data_logs
   ```

   To query your own data, replace `kibana_sample_data_logs` with the name of your source. If you do not know the name, [browse the data sources from the editor](browse-esql-sources.md).

5. Select **Search** (or **▶Run** in earlier versions).

**Result:** The table lists up to 1,000 results by default, with the time and a **Summary** of each result. The chart shows how the results spread over the 7 days.

:::{image} /explore-analyze/images/kibana-discover-try-esql-from.png
:alt: Discover in ES|QL mode with the query FROM kibana_sample_data_logs, a histogram of results over time, and a table with @timestamp and Summary columns
:screenshot:
:width: 90%
:::

## Choose the columns to show in the table

Each result has dozens of fields, but the table shows only the time and a **Summary** by default. To answer a question, you usually need a few specific fields as their own columns. In this step, you keep four fields: the response size, the destination, the operating system, and the response code.

An {{esql}} query is a chain of commands separated by pipes (`|`). Each command after the source command takes the results of the previous command, changes them, and passes them on. Commands run in the order you write them.

[`KEEP`](elasticsearch://reference/query-languages/esql/commands/keep.md) is one of these processing commands. It keeps only the columns you list, in that order. It does not remove any results. Because the query now decides which columns exist, Discover also replaces the chart of results over time with a chart based on these columns.

1. Add a `KEEP` line to the query:

   ```esql
   FROM kibana_sample_data_logs
   | KEEP bytes, geo.dest, machine.os, response.keyword
   ```

   As you enter a field name, the editor suggests matching fields. Select a suggestion to insert it. Refer to [Autocomplete and in-app help](../query-filter/languages/esql-kibana.md#esql-kibana-autocomplete).

2. Select **Search**.

**Result:** The table shows four columns: `bytes`, `geo.dest`, `machine.os`, and `response.keyword`. The number of results stays the same, and the chart now uses the columns you kept.

You can also add a column from the fields list, without changing the query. Refer to [Show specific columns in the results table](esql-results.md#esql-kibana-results-table).

## Filter the results

Filtering keeps only the results you care about. In this step, you exclude the results whose destination is Great Britain.

[`WHERE`](elasticsearch://reference/query-languages/esql/commands/where.md) keeps only the results that match a condition. A condition compares a field with a value, with [operators](elasticsearch://reference/query-languages/esql/functions-operators/operators.md) such as `==`, `!=`, `>`, or `<`. You can combine conditions with `AND` and `OR`. Put text values in double quotes.

Because `WHERE` removes results, it changes both the table and the chart.

1. Add a `WHERE` line to the query:

   ```esql
   FROM kibana_sample_data_logs
   | KEEP bytes, geo.dest, machine.os, response.keyword
   | WHERE geo.dest != "GB"
   ```

   The `!=` operator keeps every result whose destination is not `GB`.

2. Select **Search**.

**Result:** The results with `GB` as destination are gone from the table. The chart updates too, because it uses the same results as the table.

You can also filter from the table. Hover a value, then select **Filter for this** or **Filter out this**, and Discover writes the `WHERE` line for you. Refer to [Filter from a value in the results table](esql-results.md#refine-esql-query-from-table).

## Find the top results

Sorting and limiting bring the most relevant results to the top, such as the largest responses. In this step, you list the 10 results with the highest `bytes` value.

[`SORT`](elasticsearch://reference/query-languages/esql/commands/sort.md) orders the results by a field, in ascending (`asc`) or descending (`desc`) order. [`LIMIT`](elasticsearch://reference/query-languages/esql/commands/limit.md) keeps only the first results. Because commands run in order, `SORT` followed by `LIMIT 10` returns the top 10. Without `SORT`, `LIMIT 10` returns any 10 results.

A query without `LIMIT` returns at most 1,000 results.

1. Add `SORT` and `LIMIT` lines to the query:

   ```esql
   FROM kibana_sample_data_logs
   | KEEP bytes, geo.dest, machine.os, response.keyword
   | WHERE geo.dest != "GB"
   | SORT bytes desc
   | LIMIT 10
   ```

2. Select **Search**.

**Result:** The table lists 10 results, starting with the highest `bytes` value.

Sorting from a column header in the table is different. It reorders only the results already in the table, and it does not change which results the query returns. Refer to [Sort query results](esql-results.md#_sorting).

## Count the results by group

So far, each row in the table is one result. To find out which destinations come up most often, you need one row per destination, with a count. In this step, you count the results for each destination.

[`STATS`](elasticsearch://reference/query-languages/esql/commands/stats-by.md) aggregates the results. An [aggregation function](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md), such as `COUNT`, `AVG`, or `SUM`, computes a value, and `BY` sets the groups. In `STATS count = COUNT(*) BY geo.dest`, `COUNT(*)` counts the results in each group, `count =` names the new column, and `BY geo.dest` makes one group per destination.

After `STATS`, each row is a group, not a single result. Only the columns that `STATS` creates remain, in this query `count` and `geo.dest`. That is why the query no longer needs `KEEP` or `LIMIT`, and why `SORT` now uses `count`. The `WHERE` line stays before `STATS`, so the counts still exclude Great Britain.

1. Replace the query with the following one:

   ```esql
   FROM kibana_sample_data_logs
   | WHERE geo.dest != "GB"
   | STATS count = COUNT(*) BY geo.dest
   | SORT count desc
   ```

2. Select **Search**.

**Result:** The table lists one row per destination with its count, starting with the highest. The chart shows the same counts.

`STATS` can compute several values at once, or group results by time to show a trend. Refer to the [`STATS` command](elasticsearch://reference/query-languages/esql/commands/stats-by.md). To look at the results behind each destination, refer to [Inspect grouped STATS results in Discover](inspect-grouped-stats.md).

## Save your exploration

Your query holds your whole exploration. Save it as a Discover session to come back to it, share it, or build on it later.

A Discover session saves the query, not a copy of the results. When you open the session again, Discover runs the query again, so the results reflect the current data.

1. Select **Save** in the application menu.
2. Enter a **Title**, for example `Results by destination`.

   To reopen the session with the same time range, turn on **Store time with Discover session**.

3. Select **Save**.

**Result:** The session is saved, and you can open it again later.

To share the session, refer to [Share your Discover session](discover-get-started.md#share-your-findings). To add the chart or the table to a dashboard, refer to [Keep a chart or table on a dashboard](esql-results.md#_edit_the_esql_visualization).

## Next steps

- [Use Discover with {{esql}}](use-esql.md): The other {{esql}} tasks in Discover, including variable controls.
- [Create lookup indices from Discover queries](create-lookup-indices.md): Add fields from a lookup index with `LOOKUP JOIN`.
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` [Detect change points in Discover](detect-change-points.md): Find a spike, dip, or shift in a time series.
- [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md): Commands, functions, and operators beyond this session.
- [Use {{esql}} in the {{kib}} UI](../query-filter/languages/esql-kibana.md): Editor tools, time parameters, AI assistance, and Fast mode.
- [Learn data exploration and visualization with Kibana](../kibana-data-exploration-learning-tutorial.md): A longer path from Discover into dashboards.

## Related pages

- [Discover](../discover.md)
- [Explore fields and data with Discover](discover-get-started.md)
- [Optimize {{esql}} query performance](elasticsearch://reference/query-languages/esql/esql-query-performance.md)
