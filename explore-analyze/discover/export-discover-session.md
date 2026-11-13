---
navigation_title: Export a session
applies_to:
  serverless: ga
  stack: ga
type: how-to
products:
  - id: kibana
description: Export Discover results as a CSV file for a spreadsheet, or export a session definition as JSON to inspect it or manage it as code.
---

# Export results and sessions from Discover

If you want to analyze results in a spreadsheet or another tool, export them from **Discover** as a CSV file. If you want to keep a session definition in a file, for example in version control, export the session as JSON.

## Before you begin

- To export results as CSV, run a query that returns results in **Discover**.
- To generate a CSV report, you need the **Generate CSV reports** privilege, in the **Reporting** sub-feature of the **Discover** feature. The **All** privilege for **Discover** includes it by default. For more information, refer to [Permissions](../report-and-share.md#permissions).
- To export a session as JSON, open **Discover**. To open the JSON in **Console**, you also need access to **Dev Tools**.

## Export Discover session results as CSV [export-discover-session-csv]

To analyze the rows of a session in a spreadsheet or another tool, export them as a CSV file.

1. Look for the CSV export action in the actions available in the application menu. Depending on your version, this action can be called **Export** → **CSV**, **Export tab results** → **CSV**, or **Export** → **Tab results as CSV**, and can be nested under {icon}`ellipsis` **More** or {icon}`share` **Share**.
2. In the export flyout, select **Generate CSV**.

**Result:** {{kib}} queues a CSV report of the results of the current tab. To download the file when it's ready, refer to [Manually generate reports](../report-and-share.md#manually-generate-reports).

If a cell in the CSV file shows a dash or stays empty, the result has no value for that field. Refer to [What a dash or `(null)` in your results means](inspect-documents.md#missing-values-in-results).

### Row and file size limits [export-csv-limits]

Your CSV file might not contain every row of your results. The export stops at the first limit that it reaches, either a number of rows or a file size.

::::{applies-switch}

:::{applies-item} serverless: ga
* **{{esql}} mode:** 250 MB or the row limit, whichever comes first. The {{kib}} limit is 100,000 rows. The row limit is the lower value of the {{kib}} limit and the {{es}} cap on the rows that an {{esql}} query returns, which is 10,000 by default, so most queries stop at 10,000 rows. For queries that start with `TS` or `PROMQL`, the {{es}} cap is 10,000,000 rows, so the {{kib}} limit of 100,000 rows applies instead. A `LIMIT` in your query can lower the row limit. The generated report doesn't include a warning when it reaches the row limit. Refer to [Result set size limit](elasticsearch://reference/query-languages/esql/limitations.md#esql-max-rows).
* **Classic mode:** 100,000 rows or 250 MB, whichever comes first. When the results reach the row limit, the report completes with a warning.

You can't change the limits in either mode.
:::

:::{applies-item} stack: ga 9.3+
* **{{esql}} mode:** 10,000 rows or 250 MB by default, whichever comes first. The {{kib}} limit is 10,000 rows by default. The row limit is the lower value of the {{kib}} limit and the {{es}} cap on the rows that an {{esql}} query returns, which is also 10,000 by default. For queries that start with `TS` or `PROMQL`, the {{es}} cap is 10,000,000 rows, so only the {{kib}} limit applies. A `LIMIT` in your query can lower the row limit. The generated report doesn't include a warning when it reaches the row limit. Refer to [Result set size limit](elasticsearch://reference/query-languages/esql/limitations.md#esql-max-rows).
* **Classic mode:** 10,000 rows or 250 MB by default, whichever comes first. When the results reach the row limit, the export flyout warns you before you generate the report, and the report completes with a warning.

In self-managed and {{ech}} deployments, you can change the {{kib}} limits with the `xpack.reporting.csv.maxRows` and `xpack.reporting.csv.maxSizeBytes` settings. Higher limits can affect performance. In {{esql}} mode, you can also raise the {{es}} cap with the `esql.query.result_truncation_max_size` cluster setting. Refer to [Reporting settings](kibana://reference/configuration-reference/reporting-settings.md).
:::

:::{applies-item} stack: ga 9.0-9.2
* **{{esql}} mode:** 10,000 rows or 250 MB by default, whichever comes first. The row limit is the {{es}} cap on the rows that an {{esql}} query returns. A `LIMIT` in your query can lower it. In 9.2, for queries that start with `TS`, the {{es}} cap is 10,000,000 rows, so the file size limit usually comes first. The generated report doesn't include a warning when it reaches the row limit. Refer to [Result set size limit](elasticsearch://reference/query-languages/esql/limitations.md#esql-max-rows).
* **Classic mode:** 250 MB by default. There is no row limit.

In self-managed and {{ech}} deployments, you can change the file size limit with the `xpack.reporting.csv.maxSizeBytes` setting. In {{esql}} mode, you can change the row limit with the `esql.query.result_truncation_max_size` cluster setting. Refer to [Reporting settings](kibana://reference/configuration-reference/reporting-settings.md).
:::

::::

If you need more rows than the limit allows, use filters to create several smaller reports, or query {{es}} directly.

An export can also time out or return incomplete data for reasons unrelated to these limits, such as slow storage, an unavailable shard, or high network latency. For the common causes, refer to [CSV report limitations](../report-and-share.md#csv-limitations).

To generate the same export automatically on a schedule, refer to [Automatically generate reports](../report-and-share/automating-report-generation.md).

{applies_to}`serverless: unavailable` You can also trigger the export from a script or {{watcher}} by [creating a POST URL](../report-and-share/automating-report-generation.md#create-a-post-url).

## Export a Discover session as JSON [export-discover-session-json]
```{applies_to}
serverless: preview
stack: preview 9.6+
```

To inspect a session's definition, or to use it as the starting point for managing the session as code, export it as JSON. For each tab you include, the file contains the query, the filters, the {{data-source}}, and the current view, including the columns and the chart, but not the query results. To export rows, refer to [Export Discover session results as CSV](#export-discover-session-csv).

1. In **Discover**, in the application menu, select **More** → **Export** → **Export JSON**.
2. Set what the JSON includes:

   - To include every open tab, leave **Export only the current tab** off. Turn it on to include only the tab you are viewing.
   - If the session is not saved, turn on **Include current time settings** to include the current time filter and refresh interval. The setting is off by default.
   - If the session is saved, **Include current time settings** is not available. The JSON includes the current time filter and refresh interval only when you saved the session with **Store time with Discover session**.

3. Review the JSON. If {{kib}} removed a property that it can't include, the flyout lists it under **Unsupported properties were removed**. Select **Show details** to see what was removed. If the flyout shows **Unable to export** and an error, select **Retry**.
4. Copy, download, or open the JSON:

   - Select **Copy to clipboard** to copy it.
   - Select **Open in Console** to open {{kib}} Dev Tools with a request that contains the JSON. This option is available if you have access to **Dev Tools**.
   - Select **Download JSON** to save the file. The file name is the session title. For an unsaved session, the file is named `Untitled Discover session.json`.

**Result:** You have the JSON of the session, as a copy, as a request in **Console**, or as a file.

## Next steps

- [Use Discover sessions in dashboards](use-sessions-in-dashboards.md): Keep the results next to your other panels instead of exporting them.

## Related pages

- [Save and manage Discover sessions](save-open-search.md)
- [Reporting and sharing](../report-and-share.md)
