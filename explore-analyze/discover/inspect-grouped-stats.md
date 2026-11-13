---
navigation_title: Inspect grouped STATS
applies_to:
  serverless: preview
  stack: preview 9.4
products:
  - id: kibana
type: how-to
description: See the documents behind each STATS group in Discover, including CATEGORIZE patterns, sparklines, and row actions.
---

# Inspect grouped STATS results in Discover

If you group results with [`STATS BY`](elasticsearch://reference/query-languages/esql/commands/stats-by.md), you can look inside each group to see the documents behind a count or an average. When a query groups by one field, **Discover** shows each group as a row that you can expand, instead of a flat table with one row per group. Each row stands for one unique value of the grouping field, which is the field after `BY`.

## Before you begin

- Make sure **Discover** is in {{esql}} mode. Classic mode doesn't support this functionality. To switch, refer to [Switch to Discover's {{esql}} mode](switch-esql-mode.md#switch-discover-query-mode).
- If you're new to {{esql}} in Discover, start with [Get started with {{esql}} in Discover](try-esql.md).
- To get expandable groups, your query needs to group by a single field, or by a single [`CATEGORIZE`](elasticsearch://reference/query-languages/esql/functions-operators/grouping-functions/categorize.md) call on a field. If your query has more than one `STATS` command, **Discover** uses the last one. The `CATEGORIZE` function requires a [Platinum or Enterprise subscription](https://www.elastic.co/subscriptions) or an active trial.
- These queries keep the standard flat results table:
  - Queries that group by more than one field, for example `BY clientip, extension.keyword`.
  - Queries that use other grouping functions, such as `BUCKET` or `TBUCKET`, or that nest a function inside `CATEGORIZE`.
  - Queries where a later `KEEP` command drops the grouping field.
  - Queries whose data source is a subquery.
  - {applies_to}`serverless: preview` {applies_to}`stack: preview 9.5+` Queries that use [`TS_INFO`](elasticsearch://reference/query-languages/esql/commands/ts-info.md) or [`METRICS_INFO`](elasticsearch://reference/query-languages/esql/commands/metrics-info.md). Their rows describe metrics and have no documents to expand.

## View grouped results from a STATS query [esql-cascade-layout]

1. In **Discover**, in {{esql}} mode, enter a `STATS BY` query with a single grouping field. For example:

   ```esql
   FROM kibana_sample_data_logs
   | STATS Visits = COUNT(*), AvgBytes = AVG(bytes) BY geo.dest
   | SORT Visits DESC
   ```

2. Select **Search**.

   **Result:** The table lists one row per group. The results count reports the number of groups instead of the number of documents.

   :::{image} /explore-analyze/images/discover-esql-cascade-overview.png
   :alt: Grouped results layout in Discover, with one row expanded to show underlying documents
   :screenshot:
   :::

3. Expand a row to inspect the underlying documents.

:::{note}
:applies_to: { serverless: preview, stack: preview 9.5+ }
On large data sets, you can get faster, estimated results by turning on {icon}`bolt` **Fast mode**. Refer to [](/explore-analyze/query-filter/languages/esql-kibana.md#approximation-fast-mode).
:::

## Show CATEGORIZE patterns in the group titles [pattern-rendering]

When the grouping field uses [`CATEGORIZE`](elasticsearch://reference/query-languages/esql/functions-operators/grouping-functions/categorize.md), each row title shows a detected pattern, which is a group of similar messages, with the changing words highlighted. This helps you scan repeated message structures at a glance.

```esql
FROM kibana_sample_data_logs
| STATS Count = COUNT(*) BY Pattern = CATEGORIZE(message)
| SORT Count DESC
```

::::{tip}
To run a pattern analysis without writing a query, refer to [](/explore-analyze/discover/run-pattern-analysis-discover.md).
::::

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` To check how common one message is without grouping your results, refer to [](esql-results.md#find-similar-values-esql).

## Add sparklines to patterns [esql-cascade-pattern-sparkline]
```{applies_to}
serverless: preview
stack: preview 9.5
```

When the query also computes a [`SPARKLINE`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions/sparkline.md) over time, **Discover** renders a sparkline, which is a small trend chart, next to the row aggregates. For example, the following query categorizes log messages and renders a sparkline for each pattern:

```esql
FROM kibana_sample_data_logs
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS Count = COUNT(*),
        Sparkline = SPARKLINE(COUNT(*), @timestamp, 40, ?_tstart, ?_tend)
    BY Pattern = CATEGORIZE(message)
| SORT Count DESC
```

On larger data sets, add a [`SAMPLE`](elasticsearch://reference/query-languages/esql/commands/sample.md) command before `STATS` to keep the categorization fast. Because `SAMPLE 0.001` keeps about one document in a thousand, divide `COUNT(*)` by the same fraction, `Count = COUNT(*) / 0.001`, so the counts stay representative.

:::{image} /explore-analyze/images/discover-esql-cascade-pattern-sparkline.png
:alt: A grouped row showing a CATEGORIZE pattern with token highlighting and an inline sparkline
:screenshot:
:::

## Act on a grouped row [grouped-row-actions]

Select the {icon}`boxes_vertical` actions button on any group row to:

- **Copy to clipboard**: Copy the group's value.
- **Filter in**: Add a `WHERE` clause before the `STATS` command that keeps only documents matching this group.
- **Filter out**: Add a `WHERE` clause before the `STATS` command that excludes documents matching this group.
- **Open in new tab**: Open the documents in this group in a new Discover tab, with a query scoped to that group.

If the grouping field isn't filterable, **Filter in** and **Filter out** are unavailable.

## Opt out of grouped results [opt-out-of-the-grouped-layout]

If you prefer the flat results table, you can switch grouped results off. When grouped results are active, Discover replaces the regular results table toolbar with a **Group by** button that carries a {icon}`flask` badge and shows the number of active groupings. Discover preselects the grouping field from your `STATS BY` clause. To go back to the flat results table and the regular toolbar, open the **Group by** menu and select **none**. The **Group by** button stays in the toolbar of the flat table. To bring the grouping back, open the menu again and select the grouping field.

## Related pages

- [How to query in Discover's {{esql}} mode](use-esql.md)
- [Run a pattern analysis on your log data](run-pattern-analysis-discover.md)
- [`STATS` command reference](elasticsearch://reference/query-languages/esql/commands/stats-by.md)
- [Get faster results with approximate `STATS`](../query-filter/languages/esql-kibana.md#approximation-fast-mode)
