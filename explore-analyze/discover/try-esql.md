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
description: Learn how ES|QL commands change the documents, columns, and groups you see in Discover.
---

# Get started with {{esql}} in Discover [try-esql]

In this tutorial you query the sample web logs in **Discover** with Elasticsearch Query Language ({{esql}}). You start from the documents, then turn them into one row per destination. Each command changes what the table and the chart show.

You do not need a [data view](discover-get-started.md#find-the-data-you-want-to-use), and you do not need {{esql}} experience. For the rest of Discover, refer to [Explore fields and data with Discover](discover-get-started.md). For the language itself, refer to the [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md).

By the end of this tutorial, you'll know the main elements of your query and how they shape the results you see in **Discover**.

## Before you begin [try-esql-prerequisites]

To follow this tutorial, you need the following:

- The `enableESQL` setting enabled in {{product.kibana}} **Advanced Settings**. It is enabled by default.
- The {{product.kibana}} sample web logs. Add them from [Add sample data](/manage-data/ingest/sample-data.md). You can use your own indices instead. Replace `kibana_sample_data_logs` in the examples with a data source you can query.

## Name the data [tutorial-try-esql]

The query starts by naming the data. Discover then lists those documents in the table and draws the chart from them.

`FROM` is the source command for an index, a data stream, or an alias. `from` and `FROM` are the same command. Other source commands exist for specific kinds of data. Use [`TS`](elasticsearch://reference/query-languages/esql/commands/ts.md) for a time series data stream, or [`PROMQL`](elasticsearch://reference/query-languages/esql/commands/promql.md) to query with PromQL.

The sample web logs include `@timestamp`, so Discover uses that field for the time filter and the chart. The range you set is the range the table and the chart use. If the data has no `@timestamp` field, the time filter and the chart stay hidden until the query names another time field. Refer to [Set the time filter for the table and the chart](esql-results.md#_esql_and_time_series_data).

1. Find **Discover** in the navigation menu, or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. If the editor is not already in {{esql}} mode, switch to it. Refer to [Switch between {{esql}} and classic mode](switch-esql-mode.md#switch-discover-query-mode).
3. Set the time range to **Last 7 days**.

   Sample data timestamps are relative to when you installed the set. If you added the sample web logs earlier, widen the range until the table has rows.

4. Copy this query.

   On your own data, replace `kibana_sample_data_logs` with a source you can query. If you do not know the name, [browse data sources from the editor](browse-esql-sources.md).

   ```esql
   FROM kibana_sample_data_logs
   ```

5. Select **Search** (or **▶Run** in earlier versions).

**Result:** The table lists the documents. The time field is the first column, and the other fields are in the **Summary** column. The chart shows those documents over the time range.

## Choose the columns

`KEEP` names the columns you want. The same documents stay in the table, and the chart still shows them over the time range.

To add a field yourself, enter its name on the `KEEP` line and select it from the suggestions. Refer to [Autocomplete and in-app help](../query-filter/languages/esql-kibana.md#esql-kibana-autocomplete).

1. Copy this query.

   ```esql
   FROM kibana_sample_data_logs
   | KEEP machine.os, machine.ram, geo.dest
   ```

2. Select **Search**.

**Result:** The table shows `machine.os`, `machine.ram`, and `geo.dest` instead of the **Summary** column.

## Filter the rows

`WHERE` removes documents that do not match. Those visits leave the table and the chart. Put string values in double quotes.

1. Copy this query.

   ```esql
   FROM kibana_sample_data_logs
   | KEEP machine.os, machine.ram, geo.dest
   | WHERE geo.dest != "GB"
   ```

2. Select **Search**.

**Result:** Visits to Great Britain are gone from the table and the chart.

To write this filter in KQL instead, refer to [Build {{esql}} queries from KQL syntax](../query-filter/languages/esql-kibana.md#esql-kibana-quick-search).

## Choose which rows, and how many

`SORT` orders the visits that are still in the result. `LIMIT` then keeps the first rows of that order. This query sorts by RAM and keeps the 10 highest values. Without `SORT`, `LIMIT 10` would keep any 10 visits.

1. Copy this query.

   ```esql
   FROM kibana_sample_data_logs
   | KEEP machine.os, machine.ram, geo.dest
   | WHERE geo.dest != "GB"
   | SORT machine.ram desc
   | LIMIT 10
   ```

2. Select **Search**.

**Result:** The table lists 10 visits, with the highest RAM first.

A column sort reorders only the rows already in the table. It does not change which rows the query returns. Refer to [Sort query results](esql-results.md#_sorting).

## Turn the visits into groups

`STATS` replaces the documents with one row per group. The columns come from the aggregation, so this query no longer uses `KEEP` or `LIMIT`. The `WHERE` stays, and the counts are the visits that are not to Great Britain. Discover draws the chart from these rows.

`COUNT(*)` counts the visits. `BY geo.dest` makes one row per destination.

1. Copy this query.

   ```esql
   FROM kibana_sample_data_logs
   | WHERE geo.dest != "GB"
   | STATS visits = COUNT(*) BY geo.dest
   | SORT visits desc
   ```

2. Select **Search**.

**Result:** The table lists one row per destination and a visit count. The chart shows those counts.

To see the visits inside a destination, open the group. Refer to [Inspect grouped STATS results in Discover](inspect-grouped-stats.md). To calculate something other than a count, refer to the [`STATS` command](elasticsearch://reference/query-languages/esql/commands/stats-by.md).

## Keep the result

You can stay on one destination, or save the session so you can reopen this query.

Hover a value in the `geo.dest` column and select **Filter for this**. Discover adds a `WHERE` clause for that value. If you filter for `US`, the query is:

```esql
FROM kibana_sample_data_logs
| WHERE geo.dest != "GB"
| STATS visits = COUNT(*) BY geo.dest
| SORT visits desc
| WHERE geo.dest == "US"
```

**Result:** The table shows that destination only.

Select **Save** in the application menu to reopen this query later. Refer to [Save a Discover session for reuse](save-open-search.md). To share the session, refer to [Share your Discover session](discover-get-started.md#share-your-findings). To put the chart or the table on a dashboard, refer to [Keep a chart or table on a dashboard](esql-results.md#_edit_the_esql_visualization).

To ask what these counts mean, refer to [Analyze your data with AI](discover-get-started.md#analyze-with-ai).

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
