---
navigation_title: Inspect grouped STATS
applies_to:
  serverless: preview
  stack: preview 9.4
products:
  - id: kibana
type: how-to
description: Inspect expandable STATS groups in Discover, including patterns, sparklines, row actions, and the option to use a flat table.
---

# Inspect grouped STATS results in Discover

When your {{esql}} query uses a [`STATS BY`](elasticsearch://reference/query-languages/esql/commands/stats-by.md) clause with a single grouping field, **Discover** displays the results as expandable groups instead of a flat table. Each row represents one unique value of the grouping field. You can expand it to inspect the underlying documents without leaving the query.

## Before you begin

- You need an {{esql}} query in **Discover**. If you're new to {{esql}} in Discover, start with [Get started with {{esql}} in Discover](try-esql.md).
- Your query groups by a single field, or by a single [`CATEGORIZE`](elasticsearch://reference/query-languages/esql/functions-operators/grouping-functions/categorize.md) call. Other queries keep the standard flat results table:
  - Queries that group by more than one field, for example `BY clientip, extension.keyword`.
  - Queries that use other grouping functions, such as `BUCKET` or `TBUCKET`.
  - Queries that use [`TS_INFO`](elasticsearch://reference/query-languages/esql/commands/ts-info.md) or [`METRICS_INFO`](elasticsearch://reference/query-languages/esql/commands/metrics-info.md). Their rows describe metrics and have no documents to expand.

## View grouped results from a STATS query [esql-cascade-layout]

1. In **Discover**, in {{esql}} mode, enter a `STATS BY` query with a single grouping field. For example:

   ```esql
   FROM kibana_sample_data_logs
   | STATS Visits = COUNT(*), AvgBytes = AVG(bytes) BY geo.dest
   | SORT Visits DESC
   ```

2. Select **Search**.

   **Result:** The table lists one row per group. The results count reports the number of groups instead of the number of documents.

   :::{note}
   :applies_to: { serverless: preview, stack: preview 9.5+ }
   When searching large data sets, you can get faster, estimated results by using {icon}`bolt` **Fast mode**. Refer to [](/explore-analyze/query-filter/languages/esql-kibana.md#approximation-fast-mode).
   :::

   :::{image} /explore-analyze/images/discover-esql-cascade-overview.png
   :alt: Grouped results layout in Discover, with one row expanded to show underlying documents
   :screenshot:
   :::

3. Expand a row to inspect the underlying documents.

## Show CATEGORIZE patterns in the group titles [pattern-rendering]

When the grouping field uses [`CATEGORIZE`](elasticsearch://reference/query-languages/esql/functions-operators/grouping-functions/categorize.md), each row title shows the detected pattern with token highlighting, so you can scan repeated message structures at a glance.

```esql
FROM kibana_sample_data_logs
| STATS Count = COUNT(*) BY Pattern = CATEGORIZE(message)
| SORT Count DESC
```

::::{tip}
Pattern detection on text fields is also available outside {{esql}} from the **Patterns** view in Discover's classic mode. Refer to [](/explore-analyze/discover/run-pattern-analysis-discover.md).
::::

## Add sparklines to patterns [esql-cascade-pattern-sparkline]
```{applies_to}
serverless: preview
stack: preview 9.5
```

When the query also computes a [`SPARKLINE`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions/sparkline.md) over time, **Discover** renders an inline chart next to the row aggregates. For example, the following query categorizes log messages and renders a sparkline for each pattern:

```esql
FROM kibana_sample_data_logs
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS Count = COUNT(*),
        Sparkline = SPARKLINE(COUNT(*), @timestamp, 40, ?_tstart, ?_tend)
    BY Pattern = CATEGORIZE(message)
| SORT Count DESC
```

On larger data sets, add a [`SAMPLE`](elasticsearch://reference/query-languages/esql/commands/sample.md) command before `STATS` to keep the categorization fast, and divide `COUNT(*)` by the same sample fraction to keep the counts representative. For example, `SAMPLE 0.001` followed by `Count = COUNT(*) / 0.001`.

:::{image} /explore-analyze/images/discover-esql-cascade-pattern-sparkline.png
:alt: A grouped row showing a CATEGORIZE pattern with token highlighting and an inline sparkline
:screenshot:
:::

## Grouped row actions [grouped-row-actions]

Select the {icon}`boxes_vertical` actions button on any group row to:

- **Copy to clipboard**: copy the group's value.
- **Filter in**: append a `WHERE` clause to your query that keeps only documents matching this group.
- **Filter out**: append a `WHERE` clause that excludes documents matching this group.
- **Open in new tab**: open the documents in this group in a new Discover tab, with a query scoped to that group.

**Filter in** and **Filter out** are disabled when the grouping field isn't filterable.

## Opt out of the grouped layout [opt-out-of-the-grouped-layout]

When the grouped layout activates, the regular results table toolbar is replaced with a {icon}`flask` **Group by** button. The button shows the number of active groupings as a badge.

The grouping field is preselected from your `STATS BY` clause. From the **Group by** menu, select **none** to go back to the standard flat results table and the regular toolbar.

## Related pages

- [Use Discover with {{esql}}](use-esql.md)
- [Run a pattern analysis on your log data](run-pattern-analysis-discover.md)
- [`STATS` command reference](elasticsearch://reference/query-languages/esql/commands/stats-by.md)
- [Get faster results with approximate `STATS`](../query-filter/languages/esql-kibana.md#approximation-fast-mode)
