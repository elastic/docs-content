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
description: Learn how ES|QL commands change the results you see in Discover by building one query step by step on the sample web logs.
---

# Get started with {{esql}} in Discover [try-esql]

In this tutorial, you explore the {{kib}} sample web logs in **Discover** with Elasticsearch Query Language ({{esql}}). You build one query step by step and see how each command changes the results in the table and the chart.

You don't need a [data view](discover-get-started.md#find-the-data-you-want-to-use), and you don't need {{esql}} experience. For the rest of Discover, refer to [Explore fields and data with Discover](discover-get-started.md). For the language itself, refer to the [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md).

By the end of this tutorial, you'll know the main elements of your query and how they shape the results you see in **Discover**. You'll practice how to:

- Query a data source with `FROM`.
- Keep only the columns you need with `KEEP`.
- Filter the results with `WHERE`.
- Find the top results with `SORT` and `LIMIT`.
- Count the results by group with `STATS`.
- Save your query as a Discover session.

## Before you begin [try-esql-prerequisites]

To follow this tutorial, you need the following:

- {{esql}} enabled in {{kib}}. It's enabled by default. On {{stack}} deployments, an administrator can turn it off with the `enableESQL` advanced setting.
- The {{kib}} sample web logs. Add them from [Add sample data](/manage-data/ingest/sample-data.md). You can use your own indices instead. Replace `kibana_sample_data_logs` in the examples with a data source you can query, and replace the field names in later steps with fields from your data.
- To help you go faster with what you learn in this tutorial, or to go further once you know the basics, the {{esql}} editor offers several tools. It suggests commands, fields, and values as you type, and its in-app help shows the syntax of each command. Depending on your version and setup, you can also browse data sources and fields, start a query from a KQL search, or have AI write or fix a query. This tutorial has you write each command yourself so that you learn what it does. Refer to [Write queries with the {{esql}} editor](../query-filter/languages/esql-kibana.md#esql-kibana-get-started).

## Step 1: Query a data source [tutorial-try-esql]

In {{esql}} mode, the query decides which data you explore. There is no data view to select as in classic mode. Instead, the first command of every query names the data source, and the table and the chart show what that source returns.

This first command is a [source command](elasticsearch://reference/query-languages/esql/esql-commands.md#esql-source-commands):

- [`FROM`](elasticsearch://reference/query-languages/esql/commands/from.md) is the generic {{esql}} source command. It takes the names of the sources to read, for example, an index or a data stream. You can list several names or match them with a wildcard, such as `FROM logs-*`.
- Other source commands serve specific cases. For example, [`TS`](elasticsearch://reference/query-languages/esql/commands/ts.md) queries time series data streams, and [`PROMQL`](elasticsearch://reference/query-languages/esql/commands/promql.md) runs a Prometheus Query Language (PromQL) query.

Command names aren't case-sensitive, so `from` and `FROM` are the same.

1. Open **Discover** from the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. If the editor isn't in {{esql}} mode yet, select **Query in ES|QL** (**Try ES|QL** in earlier versions) in the application menu. For other ways to switch, refer to [Switch between {{esql}} and classic mode](switch-esql-mode.md#switch-discover-query-mode).
3. Set the time filter to the seven days before you installed the sample data. {{kib}} sets the sample timestamps relative to the day you install the data. If you installed it today, select **Last 7 days**. Otherwise, [set a custom range](/explore-analyze/query-filter/filtering.md#set-time-filter) that ends on the installation date.

   The sample web logs have an `@timestamp` field, so Discover uses it for the time filter and the chart over time. The time filter keeps only the results in the range you select, and the chart shows how they spread over that range.

   :::{tip}
   If you use your own data and it has no `@timestamp` field, refer to [Set the time filter for the table and the chart](esql-results.md#_esql_and_time_series_data).
   :::

4. Enter the following query in the editor:

   ```esql
   FROM kibana_sample_data_logs
   ```

   To query your own data, replace `kibana_sample_data_logs` with the name of your source. If you don't know the name, [browse the data sources from the editor](browse-esql-sources.md).

5. Select **Search** (or **▶Run** in earlier versions).

**Result:** The table lists up to 1,000 results by default, with the time and a **Summary** of each result. The chart shows how the results spread over those seven days. It counts all the matching results in the time range, not only the 1,000 rows in the table. If the table is empty, widen the time range.

:::{image} /explore-analyze/images/kibana-discover-try-esql-from.png
:alt: Discover in ES|QL mode with the query FROM kibana_sample_data_logs, a histogram of results over time, and a table with @timestamp and Summary columns
:screenshot:
:width: 90%
:::

The table isn't the end of your exploration. To look at one result in detail, select {icon}`maximize` **View details** (**Toggle dialog with details** in earlier versions) on its row. The flyout lists all its fields, and you can filter the results from any of its values. Refer to [Explore individual result or document details in depth](discover-get-started.md#look-inside-a-document).

## Step 2: Keep only the columns you need [try-esql-columns]

Each result has dozens of fields, but the table shows only the time and a **Summary** by default. To answer a question, you usually need a few specific fields as their own columns. In this step, you keep four fields: the response size, the destination country, the operating system, and the response code.

An {{esql}} query is a chain of commands separated by pipes (`|`). Each command after the source command takes the results of the previous command, changes them, and passes them on. Commands run in the order you write them.

Commands after the source command are processing commands. [`KEEP`](elasticsearch://reference/query-languages/esql/commands/keep.md) is one of them. It keeps only the columns you list, in that order. It doesn't remove any results.

Once `KEEP` sets the columns, Discover builds a chart from them instead of the chart over time. The two charts use different rows. The chart over time uses every matching result in the time range. A chart built from your columns uses only the rows that the query returns, so at most 1,000 by default.

1. Add a `KEEP` line to the query:

   ```esql
   FROM kibana_sample_data_logs
   | KEEP bytes, geo.dest, machine.os, response.keyword
   ```

   As you enter a field name, the editor suggests matching fields. Select a suggestion to insert it. Refer to [Autocomplete and in-app help](../query-filter/languages/esql-kibana.md#esql-kibana-autocomplete).

2. Select **Search**.

**Result:** The table shows four columns: `bytes`, `geo.dest`, `machine.os`, and `response.keyword`. The number of results stays the same, and Discover now picks a chart that fits the columns you kept, such as `bytes` by `geo.dest`. The time filter still applies, even though `@timestamp` is no longer a column.

:::{image} /explore-analyze/images/kibana-discover-try-esql-keep.png
:alt: Discover with a KEEP query on bytes, geo.dest, machine.os, and response.keyword, a chart of bytes by destination, and a table with those four columns
:screenshot:
:width: 90%
:::

You can also add a column from the fields list. This changes only the table, not the query, so the chart keeps showing the results over time. It works well for a quick look at a field. Use `KEEP` when the columns are part of your question, because they're saved with the query, for example, in a Discover session or on a dashboard. Refer to [Show specific columns in the results table](esql-results.md#esql-kibana-results-table).

## Step 3: Filter the results [try-esql-filter]

Filtering keeps only the results you care about. In this step, you exclude the results whose destination is the United Kingdom (`GB`).

[`WHERE`](elasticsearch://reference/query-languages/esql/commands/where.md) keeps only the results that match a condition. A condition uses an [operator](elasticsearch://reference/query-languages/esql/functions-operators/operators.md), such as `==`, `!=`, `>`, or `<`, to compare a field with a value. You can combine conditions with `AND` and `OR`. Put text values in double quotation marks.

Because `WHERE` removes results, it changes both the table and the chart.

1. Add a `WHERE` line to the query:

   ```esql
   FROM kibana_sample_data_logs
   | KEEP bytes, geo.dest, machine.os, response.keyword
   | WHERE geo.dest != "GB"
   ```

   The `!=` operator keeps every result whose destination isn't `GB`.

2. Select **Search**.

**Result:** The results with `GB` as their destination are gone from the table and from the chart. The result count stays at 1,000 because of the default limit, but no `geo.dest` value is `GB`.

You can also filter from the table, so you don't need to enter the field name and value. Hover over a value, then select **Filter for this** or **Filter out this**, and Discover writes the `WHERE` line for you. Refer to [Filter from a value in the results table](esql-results.md#refine-esql-query-from-table).

## Step 4: Find the top results [try-esql-top-results]

Sorting and limiting bring the results you want to the top, such as the largest responses. In this step, you list the 10 results with the highest `bytes` value.

[`SORT`](elasticsearch://reference/query-languages/esql/commands/sort.md) orders the results by a field, in ascending (`asc`) or descending (`desc`) order. [`LIMIT`](elasticsearch://reference/query-languages/esql/commands/limit.md) keeps only the first results. Because commands run in order, `SORT` followed by `LIMIT 10` returns the top 10. Without `SORT`, `LIMIT 10` returns any 10 results. `LIMIT` also replaces the default limit of 1,000 results.

1. Add `SORT` and `LIMIT` lines to the query:

   ```esql
   FROM kibana_sample_data_logs
   | KEEP bytes, geo.dest, machine.os, response.keyword
   | WHERE geo.dest != "GB"
   | SORT bytes desc
   | LIMIT 10
   ```

2. Select **Search**.

**Result:** The table lists 10 results, starting with the highest `bytes` value. The chart now reflects only these 10 results.

:::{image} /explore-analyze/images/kibana-discover-try-esql-sort-limit.png
:alt: Discover with a query that sorts by bytes in descending order and limits to 10, a chart of bytes by destination for those results, and a table with 10 results
:screenshot:
:width: 90%
:::

Sorting from a column header in the table is different. It reorders only the results already in the table, and it doesn't change which results the query returns. Refer to [Sort query results](esql-results.md#_sorting).

## Step 5: Count the results by group [try-esql-count-by-group]

So far, each row in the table is one result. To find out which destinations appear most often, you need one row per destination, with a count. In this step, you count the results for each destination.

[`STATS`](elasticsearch://reference/query-languages/esql/commands/stats-by.md) aggregates the results. An [aggregation function](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md), such as `COUNT`, `AVG`, or `SUM`, computes a value, and `BY` sets the groups. In `STATS count = COUNT(*) BY geo.dest`, `COUNT(*)` counts the results in each group, and `BY geo.dest` makes one group per destination. `count =` names the new column, which is separate from the `COUNT` function.

After `STATS`, each row is a group, not a single result. The query returns only the new `count` column and the `BY` column, `geo.dest`. That's why the query no longer needs `KEEP`, and why `SORT` now uses `count`. The query also drops `LIMIT 10`, so the table lists every destination instead of the first 10. The `WHERE` line stays before `STATS`, so the counts still exclude the United Kingdom.

1. Replace the query with the following one:

   ```esql
   FROM kibana_sample_data_logs
   | WHERE geo.dest != "GB"
   | STATS count = COUNT(*) BY geo.dest
   | SORT count desc
   ```

2. Select **Search**.

**Result:** The table shows each destination as a group with its count, starting with the highest. The counts include every matching result in the time range, because the default limit applies to the rows the query returns, which are now the groups. The chart shows the same counts. You can expand a group to see the results behind it.

:::{image} /explore-analyze/images/kibana-discover-try-esql-stats.png
:alt: Discover with a STATS query that counts results by destination, a chart of counts by destination, and a table of groups with one group expanded to show its results
:screenshot:
:width: 90%
:::

`STATS` can compute several values at once, or group results by time to show a trend. Refer to the [`STATS` command](elasticsearch://reference/query-languages/esql/commands/stats-by.md). To look at the results behind a group, refer to [Inspect grouped STATS results in Discover](inspect-grouped-stats.md).

## Step 6: Save your exploration [try-esql-save]

Your query holds your whole exploration. Save it as a Discover session to come back to it, share it, or build on it later.

A Discover session saves the query, not a copy of the results. When you open the session again, Discover runs the query again, so the results reflect the current data.

1. Select **Save** in the application menu.
2. In the **Title** field, enter a name, for example `Results by destination`.

   To reopen the session with the same time range, turn on **Store time with Discover session**.

3. Select **Save**.

**Result:** Discover saves the session. To reopen it later, select **Open session** in the application menu, then select the session.

To share the session, refer to [Share your Discover session](discover-get-started.md#share-your-findings). To add the chart or the table to a dashboard, refer to [Keep the chart or the table](esql-results.md#_edit_the_esql_visualization).

## Next steps

- [Use Discover with {{esql}}](use-esql.md): Explore the other {{esql}} tasks in Discover, including variable controls.
- [Create lookup indices from Discover queries](create-lookup-indices.md): Add fields from a lookup index with `LOOKUP JOIN`.
- [Detect change points in Discover](detect-change-points.md): Find a spike, dip, or shift in a time series.
- [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md): Look up commands, functions, and operators beyond this tutorial.
- [Use {{esql}} in the {{kib}} UI](../query-filter/languages/esql-kibana.md): Use editor tools, time parameters, AI assistance, and Fast mode.
- [Learn data exploration and visualization with Kibana](../kibana-data-exploration-learning-tutorial.md): Follow a longer path from Discover into dashboards.

## Related pages

- [Discover](../discover.md)
- [Explore fields and data with Discover](discover-get-started.md)
- [Optimize {{esql}} query performance](elasticsearch://reference/query-languages/esql/esql-query-performance.md)
