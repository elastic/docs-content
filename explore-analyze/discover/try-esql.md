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
description: Walk through your first Discover session in ES|QL. Query sample logs without a data view, filter and sort results, and keep the chart.
---

# Get started with {{esql}} in Discover [try-esql]

Elasticsearch Query Language ({{esql}}) lets you explore {{product.elasticsearch}} data in **Discover** without a [data view](discover-get-started.md#find-the-data-you-want-to-use). You write a piped query that names the data, then filter and sort it in the same editor. This tutorial walks through a first session on the sample web logs: run a query, read the table and chart, then keep what you found.

It assumes you can open {{product.kibana}} and have data in {{product.elasticsearch}}. You do not need {{esql}} experience.

By the end of this tutorial, you can:

- Open **Discover** in {{esql}} mode
- Write a piped query that selects fields, filters rows, and sorts the results
- Read the results table and the chart that Discover builds from the query
- Keep the session so you can reopen it, or add the session, table, or chart to a dashboard

## Before you begin [try-esql-prerequisites]

To follow this tutorial, you need the following:

- The `enableESQL` setting enabled in {{product.kibana}} **Advanced Settings**. It is enabled by default.
- The {{product.kibana}} sample web logs. Add them from [Add sample data](/manage-data/ingest/sample-data.md). You can use your own indices instead. Replace `kibana_sample_data_logs` in the examples with a data source you can query.

## Step 1: Open Discover in ES|QL [tutorial-try-esql]

**Discover** has two query modes. This tutorial uses {{esql}}, which does not require a data view. Classic mode uses data views with Kibana Query Language (KQL) or Lucene. For classic mode, refer to [Explore fields and data with Discover](discover-get-started.md).

1. Find **Discover** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. If the editor is not already in {{esql}} mode, switch to it from either location:

   - {icon}`code` **Query in ES|QL** (**ES|QL** or **Try ES|QL** in earlier versions) in the application menu.
   - {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` **Switch to ES|QL** in the contextual menu ({icon}`boxes_vertical`) of the active Discover tab. This affects only that tab.

   If the editor already shows an {{esql}} query, skip this step. If that tab already has a KQL or Lucene query, Discover converts it when you switch. Switching back to classic mode does not restore that query. Refer to [Revert to Discover's classic mode](switch-esql-mode.md#revert-to-classic-mode).

3. Set the time range to **Last 7 days**.

   Sample data timestamps are relative to when you installed the set. If you added the sample web logs earlier, widen the range until the table has rows.

**Result:** The query editor is in {{esql}} mode, and the time range covers the sample web logs.

## Step 2: Query the sample web logs

Start with the operating system and RAM fields from the sample web logs.

1. Copy the following query. To make queries easier to read, put each processing command on a new line.

    ```esql
    FROM kibana_sample_data_logs <1>
    | KEEP machine.os, machine.ram <2>
    ```

    1. Query the sample web logs you added earlier.
    2. Keep only the `machine.os` and `machine.ram` fields in the results table.

   :::{note}
   {{esql}} keywords are not case sensitive.
   :::

2. Select **Search** (or **▶Run** in earlier versions).

**Result:** The table lists operating systems and RAM values. Discover also draws a chart from the query.

You don't have to write the next change from memory. The editor suggests commands and fields as you type, and it includes in-app help. Refer to [Write queries with the {{esql}} editor](../query-filter/languages/esql-kibana.md#esql-kibana-get-started) for those tools, the editor search bar, and AI assistance.

If you are not sure which index or field names to use on your own data, the editor can browse data sources and fields for you. Refer to [Browse data sources and fields from the editor](browse-esql-sources.md).

## Step 3: Add a field and read the chart

Add the visit destination so you can see where the visits went. `LIMIT` sets how many rows the query returns. These examples use `LIMIT 10` to keep the table short.

1. Replace the query with the following:

    ```esql
    FROM kibana_sample_data_logs
    | KEEP machine.os, machine.ram, geo.dest
    | LIMIT 10
    ```

2. Select **Search** (or **▶Run** in earlier versions).

**Result:** The table shows 10 rows. The chart updates from the new query and breaks the data down for you.

:::{note}
When you don't use `KEEP` to retain specific fields, Discover does not break the chart down automatically. An option appears above the visualization so you can select a field.
:::

## Step 4: Sort and filter the results

Sort by RAM, and drop visits whose destination is Great Britain.

1. Replace the query with the following:

    ```esql
    FROM kibana_sample_data_logs
    | KEEP machine.os, machine.ram, geo.dest
    | SORT machine.ram desc
    | WHERE geo.dest != "GB"
    | LIMIT 10
    ```

2. Select **Search** (or **▶Run** in earlier versions).

**Result:** The table and chart no longer include rows where `geo.dest` is `GB`. The table is sorted by `machine.ram` in descending order.

You can also add a `WHERE` clause by interacting with a value in the results table. Refer to [Refine an {{esql}} query from the results table](esql-results.md#refine-esql-query-from-table). Column-header sorting only reorders the rows already retrieved. To sort the full data set, keep using `SORT` in the query. Refer to [Sort query results](esql-results.md#_sorting).

## Step 5: Save the session

To reopen this query, the columns, and the tabs later, save the Discover session.

You can also add the session or the chart to a dashboard.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` You can save the current table to a dashboard too.

Refer to [Save a Discover session for reuse](save-open-search.md).

**Result:** The session is saved, and you can reopen it or put it on a dashboard.

## Next steps

There is much more you can do with {{esql}} to explore data and investigate in **Discover**.

- [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md): Commands, functions, and operators.
- [Use Discover with ES|QL](use-esql.md): Tasks that stay in Discover when you are in {{esql}} mode.
- [Create lookup indices from Discover queries](create-lookup-indices.md): Build or edit a lookup index from a `LOOKUP JOIN` command.
- [Inspect grouped STATS results in Discover](inspect-grouped-stats.md): Expand `STATS BY` groups, inspect patterns, and filter from a group.
- [Use ES|QL in the {{kib}} UI](../query-filter/languages/esql-kibana.md): Editor tools, time parameters, AI assistance, and Fast mode.
- [Learn data exploration and visualization with Kibana](../kibana-data-exploration-learning-tutorial.md): A longer path from Discover into dashboards.

## Related pages

- [Discover](../discover.md)
- [Explore fields and data with Discover](discover-get-started.md)
- [Optimize {{esql}} query performance](elasticsearch://reference/query-languages/esql/esql-query-performance.md)
- {applies_to}`stack: ga 9.5+` [Detect change points in Discover](detect-change-points.md)
