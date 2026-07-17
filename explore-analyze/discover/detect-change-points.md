---
navigation_title: Detect change points
applies_to:
  stack: ga 9.5+
  serverless: ga
products:
  - id: kibana
type: how-to
description: Detect statistically significant changes in time series data with an ES|QL query in Discover, then investigate each change point in context.
---

# Detect change points in Discover [detect-change-points-discover]

Use an {{esql}} [`CHANGE_POINT`](elasticsearch://reference/query-languages/esql/commands/change-point.md) query in **Discover** to find statistically significant changes in time series data, such as spikes, dips, and shifts in distribution or trend. Discover charts each analyzed series, marks detected changes, and keeps the results table available for investigation.

## Before you begin

- You need an [appropriate subscription](https://www.elastic.co/subscriptions) or a trial license.
- You need time series data with a date field and values that you can aggregate into a metric. The `CHANGE_POINT` command requires at least 22 values per series.
- {{esql}} must be enabled in {{kib}}. To try the example in this guide, [install the sample web logs](../index.md#gs-get-data-into-kibana).

## Find and investigate change points

1. Find **Discover** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Switch to {{esql}} mode. Refer to [Using {{esql}}](try-esql.md#tutorial-try-esql) for the available options.
3. Set the time range to a seven-day period that contains data. For newly installed sample data, use **Last 7 days**. If that range has no data, select an earlier absolute range or reinstall the sample data to refresh its timestamps.
4. Enter the following query:

   ```esql
   FROM kibana_sample_data_logs
   | WHERE @timestamp <= ?_tend AND @timestamp > ?_tstart
   | STATS event_count = COUNT(*) BY time_bucket = BUCKET(@timestamp, 50, ?_tstart, ?_tend)
   | CHANGE_POINT event_count ON time_bucket
   | WHERE type IS NOT NULL
   ```

   The query counts events in 50 time buckets, analyzes the count for changes, and returns only detected change points. For your own data, replace the index, time field, and aggregation.

5. Select **Search**.

   When the query detects a change point, Discover replaces the usual visualization with a chart of the analyzed series and marks each change. The results table remains available. A lower p-value indicates a more significant change.

   If Discover shows **No change points detected**, the data either has no statistically significant change or doesn't provide the 22 values required for analysis. Widen the time range or adjust the bucket size to provide more values.

6. Expand a change point in the results table, then select **Overview** to inspect its chart, time, metric, type, p-value, and description.
7. From the chart actions, select **Open in a new Discover tab** to inspect the source documents around the change point. The new tab is filtered to a focused time range around the detected change.

## Compare change points across groups

Add `BY` to analyze each group as a separate series. For example, the following query analyzes event counts for each operating system:

```esql
FROM kibana_sample_data_logs
| WHERE @timestamp <= ?_tend AND @timestamp > ?_tstart
| STATS event_count = COUNT(*) BY machine.os, time_bucket = BUCKET(@timestamp, 50, ?_tstart, ?_tend)
| CHANGE_POINT event_count ON time_bucket BY machine.os
| WHERE type IS NOT NULL
```

Discover displays a separate chart for each group that contains a detected change point. Use the chart grid to compare where each series changed.

## Next steps

- Save the Discover session to preserve the query and time range.
- Use the chart actions to inspect the visualization or attach it to an existing case.

## Related pages

- [Using {{esql}} in Discover](try-esql.md)
- [`CHANGE_POINT` command reference](elasticsearch://reference/query-languages/esql/commands/change-point.md)
- [Detect change points in AIOps Labs](../machine-learning/machine-learning-in-kibana/xpack-ml-aiops.md#change-point-detection)
