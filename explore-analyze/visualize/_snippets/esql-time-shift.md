Point-and-click visualizations use a **Time shift** to compare the current window with an earlier window of the same duration. In an {{esql}} query, compute both windows in one [`STATS`](elasticsearch://reference/query-languages/esql/commands/stats-by.md) command. Use a per-aggregation `WHERE` filter for each window.

The dashboard [time filter](/explore-analyze/query-filter/filtering.md) always applies to {{esql}} visualizations. Set it so both windows fall inside the selected range. Point-and-click **Time shift** fetches the offset range even when that range sits outside the time filter.

This example uses the {{kib}} [sample web logs](/manage-data/ingest/sample-data.md) data. It compares the last 7 days with the 7 days before that, per host.

To follow the example, [add the **Sample web logs** data](/manage-data/ingest/sample-data.md). Sample data timestamps are relative to when you installed the data set. If you installed it recently, set the time filter to **Last 15 days** so both 7-day windows have data.

To create the visualization:

1. Open a dashboard and add a new {{esql}} visualization:

    * {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` Select **Add** in the application menu, then select **Visualization (query)** or **New panel** → **{{esql}}** under **Visualizations**, depending on your {{kib}} version.
    * {applies_to}`stack: ga 9.0-9.1` Select **Add panel** in the application menu, then select **{{esql}}**.

2. Enter the following query:

    ```esql
    FROM kibana_sample_data_logs
    | EVAL current_start = ?_tend - 7 days, prior_start = ?_tend - 14 days <1>
    | STATS
        current_count = COUNT(*) WHERE @timestamp >= current_start, <2>
        prior_count = COUNT(*) WHERE @timestamp >= prior_start AND @timestamp < current_start
      BY host.keyword
    | EVAL pct_diff = CASE( <3>
        prior_count > 0,
        ROUND(100.0 * TO_DOUBLE(current_count - prior_count) / prior_count, 1),
        null
      )
    | SORT ABS(pct_diff) DESC
    ```

    1. Bound both windows from the end of the time filter. `?_tend` stays in sync with the dashboard time filter.
    2. Count events in each window in a single pass. Refer to [`STATS` with `WHERE`](elasticsearch://reference/query-languages/esql/commands/stats-by.md).
    3. Compute the percent change. `CASE` returns `null` when the earlier window has no events.

3. Run the query. A visualization appears with one row per host. If {{kib}} suggests a different visualization type, select **Table** from the visualization type dropdown.

4. Select **Apply and close** to save the visualization to your dashboard.

You now have current and prior counts, plus a percent difference, for each host. To use your own data, change the `FROM` source and the `BY` grouping field.

To compare a different duration or offset, change the two `EVAL` time spans. For the last hour versus the same hour a week ago, set `current_start` to `?_tend - 1 hour` and `prior_start` to `?_tend - 7 days - 1 hour`. Keep the time filter wide enough to include both windows.

For the point-and-click **Time shift** control, refer to [Compare differences over time](/explore-analyze/visualize/lens.md#compare-data-with-time-offsets).
