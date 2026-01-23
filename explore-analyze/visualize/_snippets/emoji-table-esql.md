When you build a table with {{esql}}, query results can include emoji characters, which means you can use them in your visualizations. Combined with `EVAL` and `CASE` functions, this opens up options like mapping values to colored status indicators (🟢, 🟠, 🔴), adding visual labels, or highlighting specific categories.

This example uses the {{kib}} sample web logs data to build a status table that shows the success rate per host, with a colored status indicator.

:::{image} /explore-analyze/images/esql-table-emoji.png
:alt: Table visualization showing success rate per host with emoji status indicators
:screenshot:
:::

Before you begin, ensure you have the sample web logs data installed. In {{kib}}, go to **{{integrations}}** and search for **Sample data**. On the **Sample data** page, expand the **Other sample data sets** section and add **Sample web logs**.

To create the visualization:

1. Open a dashboard and add a new {{esql}} visualization:

    * {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` Select **Add** > **New panel** in the toolbar, then choose **{{esql}}** under **Visualizations**.
    * {applies_to}`stack: ga 9.0-9.1` Click **Add panel** in the dashboard toolbar, then choose **{{esql}}**.

2. Enter the following query:

    ```esql
    FROM kibana_sample_data_logs
    | EVAL is_success = CASE(response >= "200" AND response < "300", 1, 0) <1>
    | STATS 
        total_requests = COUNT(*),
        successful_requests = SUM(is_success)
      BY host.keyword <2>
    | EVAL success_rate = ROUND(successful_requests * 100.0 / total_requests, 1) <3>
    | EVAL status = CASE( <4>
        success_rate >= 92, "🟢",
        success_rate >= 90, "🟠",
        "🔴"
      )
    | KEEP host.keyword, status, success_rate, successful_requests, total_requests <5>
    | SORT success_rate DESC
    ```

    1. Create a binary flag: 1 for successful responses (2xx), 0 otherwise.
    2. Group by host and use `SUM` to count successes.
    3. Calculate the success rate as a percentage.
    4. Map the success rate to emoji indicators based on thresholds.
    5. Select and order the columns for the table output.

3. Run the query. A visualization appears with one row per host and an emoji status column. If {{kib}} suggests a different visualization type, select **Table** from the visualization type dropdown.

4. Optionally, configure the table appearance in the visualization settings:
   - To reorder columns, rearrange the metrics in the **Metrics** section.
   - To rename a column, select the metric and update its **Name** in the appearance options.

5. Select **Apply and close** to save the visualization to your dashboard.

6. Optionally, once the panel is saved, select the panel title to give it a meaningful name like `Status per host`.

Emojis aren't limited to tables. Because they're part of the query results, you can use them in any visualization type that displays text fields, such as bar charts with emoji labels or metric panels with status indicators.

Once you have your visualization working, you can add [controls](../dashboards/add-controls.md#add-variable-control) to filter by host or time range, use [LOOKUP JOIN](elasticsearch://reference/query-languages/esql/esql-lookup-join.md) to enrich your data with metadata from other indices, or create [alerts](../alerts-cases/alerts/rule-type-es-query.md) based on the same query to get notified when status changes.