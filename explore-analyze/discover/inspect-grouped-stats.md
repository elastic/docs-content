---
navigation_title: Inspect grouped STATS
applies_to:
  stack: preview 9.4
  serverless: preview
products:
  - id: kibana
type: how-to
description: Inspect expandable STATS groups in Discover, including patterns, sparklines, row actions, and the option to use a flat table.
---

# Inspect grouped STATS results in Discover

When your {{esql}} query uses a [`STATS BY`](elasticsearch://reference/query-languages/esql/commands/stats-by.md) clause with a single grouping field, **Discover** displays the results as expandable groups instead of a flat table. Each row represents one unique value of the grouping field. You can expand it to inspect the underlying documents without leaving the query.

## Before you begin

- You need an {{esql}} query in **Discover**. If you are new to that editor, start with [Get started with Discover using {{esql}}](try-esql.md).
- The grouped layout activates when the `BY` clause contains a single field reference or a single [`CATEGORIZE`](elasticsearch://reference/query-languages/esql/functions-operators/grouping-functions/categorize.md) call. Other grouping functions like `BUCKET` or `TBUCKET`, and queries that group by more than one field (for example, `BY clientip, extension`), keep the standard flat results table. Queries that use [`TS_INFO`](elasticsearch://reference/query-languages/esql/commands/ts-info.md) or [`METRICS_INFO`](elasticsearch://reference/query-languages/esql/commands/metrics-info.md) also keep the flat results table, because those commands return synthetic metric-metadata rows that have no underlying documents to expand.

## View grouped results from a STATS query [esql-cascade-layout]

1. In **Discover**, in {{esql}} mode, enter a `STATS BY` query with a single grouping field. For example:

   ```esql
   FROM kibana_sample_data_logs
   | STATS Count = COUNT(*) BY Pattern = CATEGORIZE(message)
   | SORT Count DESC
   ```

2. Select **Search**.

   **Result:** The table lists one row per group. The results count above the table reports the number of groups instead of the number of documents.

   :::{note}
   :applies_to: {"stack": "preview 9.5", "serverless": "preview"}
   When searching large datasets, you can get faster, estimated results by using {icon}`bolt` **Fast mode**. Refer to [](/explore-analyze/query-filter/languages/esql-kibana.md#approximation-fast-mode).
   :::

   :::{image} /explore-analyze/images/discover-esql-cascade-overview.png
   :alt: Grouped results layout in Discover, with one row expanded to show underlying documents
   :screenshot:
   :::

3. Expand a row to inspect the underlying documents.

## Pattern rendering

When the grouping field uses [`CATEGORIZE`](elasticsearch://reference/query-languages/esql/functions-operators/grouping-functions/categorize.md), each row title shows the detected pattern with token highlighting, so you can scan repeated message structures at a glance.

::::{tip}
Pattern detection on text fields is also available outside {{esql}} from the **Patterns** view in Discover's classic mode. Refer to [](/explore-analyze/discover/run-pattern-analysis-discover.md).
::::

## Add sparklines to patterns [esql-cascade-pattern-sparkline]
```{applies_to}
stack: preview 9.5
serverless: preview
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

## Grouped row actions

Select the {icon}`boxes_vertical` actions button on any group row to:

- **Copy to clipboard**: copy the group's value.
- **Filter in**: append a `WHERE` clause to your query that keeps only documents matching this group.
- **Filter out**: append a `WHERE` clause that excludes documents matching this group.
- **Open in new tab**: open the documents in this group in a new Discover tab, with a query scoped to that group.

**Filter in** and **Filter out** aren't available when the grouping field is not filterable.

## Opt out of the grouped layout

When the grouped layout activates, the regular results table toolbar is replaced with a {icon}`flask` **Group by** button. The button shows the number of active groupings as a badge.

The grouping field is preselected from your `STATS BY` clause. Open the **Group by** menu and select **none** to fall back to the standard flat results table and bring back the regular toolbar.

## Related pages

- [Use Discover with ES|QL](use-esql.md)
- [Run a pattern analysis on your log data](run-pattern-analysis-discover.md)
- [`STATS` command reference](elasticsearch://reference/query-languages/esql/commands/stats-by.md)
- [Get faster results with approximate `STATS`](../query-filter/languages/esql-kibana.md#approximation-fast-mode)
