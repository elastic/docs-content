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

- You need a [Platinum or Enterprise subscription](https://www.elastic.co/subscriptions) or an active trial for Elastic Stack. On Elastic Cloud Serverless, `CHANGE_POINT` is available for all project types and feature tiers, including Elastic AI SOC Engine (EASE).
- To follow the example, [add the **Sample web logs** data](../index.md#gs-get-data-into-kibana).
- To analyze your own data, you need a date field and values that you can aggregate into a numeric metric. The `CHANGE_POINT` command requires at least 22 values per series.

## Find and investigate change points

In this example, you use the sample web logs data to detect changes in the average number of bytes transferred for each destination country.

1. Find **Discover** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Switch to {{esql}} mode. Refer to [Using {{esql}}](try-esql.md#tutorial-try-esql) for the available options.
3. Set the time range to **All time**, or select a range that covers at least one month of the sample data.
4. Enter the following query:

   ```esql
   FROM kibana_sample_data_logs
   | STATS avg_bytes = AVG(bytes) BY geo.dest, day = BUCKET(timestamp, 1d)
   | CHANGE_POINT avg_bytes ON day BY geo.dest
   | WHERE type IS NOT NULL
   ```

   The query calculates the average number of bytes transferred each day for every destination country, then returns the detected change points.

5. Select **Search**.

   Discover shows a separate chart for each destination country with a detected change point. The results table lists the detected changes. A lower p-value indicates a more significant change.

   :::{image} /explore-analyze/images/kibana-discover-change-point-results.png
   :alt: Discover showing change point charts and results for destination countries in the sample web logs data
   :screenshot:
   :width: 90%
   :::

6. Expand a change point in the results table. The **Overview** tab lets you inspect its chart, time, metric, type, p-value, and description.
7. From the chart actions, select **Open in a new Discover tab** to open the series in a focused time range around the detected change.

   :::{image} /explore-analyze/images/kibana-discover-change-point-overview.png
   :alt: Expanded change point with the Overview tab selected and the Open in a new Discover tab action highlighted
   :screenshot:
   :width: 60%
   :::

## Analyze your own data

For indexed data, structure your query so that it produces one numeric metric value per time bucket before calling `CHANGE_POINT`. For example, the following query analyzes changes in log volume over the selected time range:

```esql
FROM logs-*
| WHERE @timestamp <= ?_tend AND @timestamp > ?_tstart
| STATS event_count = COUNT(*) BY time_bucket = BUCKET(@timestamp, 50, ?_tstart, ?_tend)
| SORT time_bucket
| CHANGE_POINT event_count ON time_bucket
| WHERE type IS NOT NULL
```

To adapt and troubleshoot the query:

- **Use your data:** Replace the index, time field, and aggregation with values appropriate for your data.
- **Troubleshoot empty results:** If Discover shows **No change points detected**, the data either has no statistically significant change or doesn't provide the 22 values required for analysis. Widen the time range or adjust the bucket size to provide more values.
- **Inspect source documents:** For queries that read from an index, **Open in a new Discover tab** opens the source documents in a focused time range around the detected change.

## Compare change points across groups

Add fields to `BY` to analyze each unique combination as a separate series. For example, the following query analyzes the sum of transferred bytes for each host and response code in the sample web logs data:

```esql
FROM kibana_sample_data_logs
| STATS sum_bytes = SUM(bytes) BY host, response.keyword, day = BUCKET(timestamp, 1d)
| CHANGE_POINT sum_bytes ON day BY host, response.keyword
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
