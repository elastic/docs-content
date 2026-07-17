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
- {{esql}} must be enabled in {{kib}}.
- To analyze your own data, you need a date field and values that you can aggregate into a numeric metric. The `CHANGE_POINT` command requires at least 22 values per series.

## Find and investigate change points

In this example, you use a query that simulates a change point, so you can explore the results without loading sample data.

1. Find **Discover** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Switch to {{esql}} mode. Refer to [Using {{esql}}](try-esql.md#tutorial-try-esql) for the available options.
3. Set the time range to **Last 24 hours**.
4. Enter the following query:

   ```esql
   ROW hour_offset = [24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]
   | MV_EXPAND hour_offset
   | EVAL time_bucket = TO_DATETIME(TO_LONG(NOW()) - TO_LONG(hour_offset) * 3600000)
   | EVAL request_count = CASE(hour_offset >= 12, 10, 100)
   | SORT time_bucket
   | CHANGE_POINT request_count ON time_bucket
   | WHERE type IS NOT NULL
   ```

   The query creates 25 hourly values, increases `request_count` from 10 to 100 midway through the series, and returns the detected step change. Because it generates timestamps relative to the current time, you can run it at any time without installing sample data.

5. Select **Search**.

   Discover replaces the usual visualization with a chart that shows the sharp increase from 10 to 100. The results table contains one `step_change` result. A lower p-value indicates a more significant change.

   :::{image} /explore-analyze/images/kibana-discover-change-point-results.png
   :alt: Discover chart showing the simulated increase from 10 to 100 and one step change result
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

Add `BY` to analyze each group as a separate series. For example, the following query analyzes log volume for each host:

```esql
FROM logs-*
| WHERE @timestamp <= ?_tend AND @timestamp > ?_tstart
| STATS event_count = COUNT(*) BY host.name, time_bucket = BUCKET(@timestamp, 50, ?_tstart, ?_tend)
| SORT host.name, time_bucket
| CHANGE_POINT event_count ON time_bucket BY host.name
| WHERE type IS NOT NULL
```

Discover displays a separate chart for each group that contains a detected change point. Use the chart grid to compare where each series changed.

::::{dropdown} Example
The following query simulates change points for two services, so you can preview grouped results without loading sample data:

```esql
ROW hour_offset = [24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0], service = ["checkout","search"]
| MV_EXPAND hour_offset
| MV_EXPAND service
| EVAL time_bucket = TO_DATETIME(TO_LONG(NOW()) - TO_LONG(hour_offset) * 3600000)
| EVAL request_count = CASE(service == "checkout", CASE(hour_offset >= 12, 10, 100), CASE(hour_offset >= 8, 20, 80))
| SORT service, time_bucket
| CHANGE_POINT request_count ON time_bucket BY service
| WHERE type IS NOT NULL
```

:::{image} /explore-analyze/images/kibana-discover-grouped-change-points.png
:alt: Discover showing separate change point charts and results for the checkout and search services
:screenshot:
:width: 90%
:::
::::

## Next steps

- Save the Discover session to preserve the query and time range.
- Use the chart actions to inspect the visualization or attach it to an existing case.

## Related pages

- [Using {{esql}} in Discover](try-esql.md)
- [`CHANGE_POINT` command reference](elasticsearch://reference/query-languages/esql/commands/change-point.md)
- [Detect change points in AIOps Labs](../machine-learning/machine-learning-in-kibana/xpack-ml-aiops.md#change-point-detection)
