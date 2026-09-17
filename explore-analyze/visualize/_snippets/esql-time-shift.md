To compare the current period with a previous period of the same duration, compute both windows in one [`STATS`](elasticsearch://reference/query-languages/esql/commands/stats-by.md) command. Use a per-aggregation `WHERE` filter for each window.

This example uses the {{kib}} [sample web logs](/manage-data/ingest/sample-data.md). It compares the last 7 days with the 7 days before that, per host. Add that data set if you don't have it yet. Sample data timestamps are relative to when you installed the data set.

To create the visualization:

1. Open a dashboard and add a new {{esql}} visualization:

    * {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` Select **Add** in the application menu, then select **Visualization (query)** or **New panel** → **{{esql}}** under **Visualizations**, depending on your {{kib}} version.
    * {applies_to}`stack: ga 9.0-9.1` Select **Add panel** in the application menu, then select **{{esql}}**.

2. Set the [time filter](/explore-analyze/query-filter/filtering.md) to the last 15 days so both 7-day windows have data.

3. Enter the following query:

    ```esql
    FROM kibana_sample_data_logs
    | EVAL current_start = ?_tend - 7 days, previous_start = ?_tend - 14 days <1>
    | STATS
        current_count = COUNT(*) WHERE @timestamp >= current_start AND @timestamp <= ?_tend, <2>
        previous_count = COUNT(*) WHERE @timestamp >= previous_start AND @timestamp < current_start
      BY host.keyword
    | EVAL pct_diff = CASE( <3>
        previous_count > 0,
        ROUND(100.0 * TO_DOUBLE(current_count - previous_count) / previous_count, 1),
        null
      )
    | SORT ABS(pct_diff) DESC
    ```

    1. Bound both windows from the end of the time filter. `?_tend` stays in sync with the dashboard time filter.
    2. Count events in each window in a single pass. Refer to [`STATS` with `WHERE`](elasticsearch://reference/query-languages/esql/commands/stats-by.md).
    3. Compute the percent change. `CASE` returns `null` when the previous window has no events.

4. Run the query. A visualization appears with one row per host. If {{kib}} suggests a different visualization type, select **Table** from the visualization type dropdown.

5. Select **Apply and close** to save the visualization to your dashboard.

To use your own data, change the `FROM` source and the `BY` grouping field. If your time field isn't `@timestamp`, replace `@timestamp` in the `STATS` filters. To apply the dashboard time filter to a custom time field, add a `WHERE` clause with `?_tstart` and `?_tend`. Refer to [Filter by time](/explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-time-filter).

To compare a different duration or offset, change the two `EVAL` time spans. For the last hour versus the same hour a week ago, set `current_start` to `?_tend - 1 hour` and `previous_start` to `?_tend - 7 days - 1 hour`. Set the time filter to cover both windows.

To set **Time shift** in the point-and-click editor, refer to [Compare differences over time](/explore-analyze/visualize/lens.md#compare-data-with-time-offsets).
