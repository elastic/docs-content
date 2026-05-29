---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/share-the-dashboard.html
description: Share Kibana dashboards with your team using links or embeds, and export them as PDF, PNG, CSV, JSON, or NDJSON files.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Share and export dashboards [share-the-dashboard]

{{kib}} provides several ways to share and export dashboards:

- [Share with a link](#share-dashboard-link): Copy a direct link to the dashboard.
- [Embed in a webpage](#embed-dashboard): Embed an interactive dashboard as an iframe on external web pages.
- [Export as PDF or PNG](#export-dashboard-pdf-png): Generate a report file of your dashboard.
- [Download visualization data as CSV](#download-csv): Download the data behind individual visualizations.
- [Export dashboard configuration](#export-dashboards): Export as JSON for the dashboards API, or as NDJSON for bulk moves and backups.

You can also [set whether other users of your space can edit dashboards you own](#manage-dashboard-access).

:::{image} /explore-analyze/images/share-dashboard.png
:screenshot:
:width: 40%
:::

## Share with a link [share-dashboard-link]

Share a direct link to your dashboard so that others can access it in {{kib}}.

1. Open the dashboard, then select {icon}`share` **Share**.
2. On the **Link** tab, select **Copy link**.

The link requires authentication. To access the dashboard, users must log in to {{kib}} with an account that has the necessary permissions. Anonymous users can also access the link if you have configured [Anonymous authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-authentication.md#anonymous-authentication) and your anonymous service account has the necessary privileges.

If the dashboard has unsaved changes, you get a temporary link that might break later, for example after an upgrade. Save the dashboard first to get a permanent link. If you share a link while a panel is maximized, the link reopens the dashboard with that same panel maximized.

{applies_to}`stack: ga 9.1` {applies_to}`serverless: ga` When sharing, you can choose to use a relative or an absolute time range:

* **Relative time range** (default): The link shows current data. For example, if you share a "Last 7 days" view, users always see the most recent 7 days when they open the link.
* **Absolute time range**: The link shows a fixed time period. For example, if you share a "Last 7 days" view on January 7, 2025, the link always shows that exact week of January 1-7, 2025, regardless of when users open the link.

## Embed in a webpage [embed-dashboard]
```{applies_to}
stack: ga
serverless: unavailable
```

Embed a fully interactive dashboard as an iframe on an internal company website or personal web page.

1. Open the dashboard, then select {icon}`share` **Share**.
2. Go to the **Embed** tab.
3. Under **Include**, select which parts of the dashboard to display in the embedded view:
   - **Top menu**
   - **Query**
   - **Time filter**
   - **Filter bar** (enabled by default)
4. Select **Copy embed code**.
5. Paste the iframe code into your web page HTML.

For information about granting access to embedded dashboards, refer to [Authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/user-authentication.md).

::::{tip}
Save the dashboard before generating the embed code. Embedding a dashboard with unsaved changes might result in an embed code that does not work properly.
::::

## Export as PDF or PNG [export-dashboard-pdf-png]
```{applies_to}
stack: ga
serverless: unavailable
```

Generate and download a PDF or PNG file of your dashboard. PDF and PNG reports are a [subscription feature](https://www.elastic.co/subscriptions).

1. Open the dashboard, then select {icon}`download` **Export** in the application menu.
2. Choose the PDF or PNG option.
3. Optional: For PDF exports, enable **Print format** to create a printer-friendly report with multiple A4 portrait pages and two visualizations per page.
4. Select **Export PDF** or **Export PNG** to generate the report.

A notification confirms that the report is queued. When it is ready, download it from the **Reporting** page under **Stack Management** → **Alerts and Insights** → **Reporting**. If the report contains a data table or Discover session, the PDF includes only the visible data.

{applies_to}`stack: ga 9.1+` You can also schedule recurring exports. Refer to [Automatically generate reports](../report-and-share/automating-report-generation.md) to learn more.

For general information about reporting across all {{kib}} apps, [how to configure reporting](/deploy-manage/kibana-reporting-configuration.md), known limitations, and troubleshooting, refer to [Reporting and sharing](../report-and-share.md).

## Download visualization data as CSV [download-csv]

You can download the data displayed in a visualization on your dashboard as a CSV file. The option is available for chart and table visualizations that expose tabular data, typically those created with **Lens**. It does not appear on panel types such as **Markdown**, **Image**, **Link**, or **Maps**.

1. Open the panel menu of the visualization, then select **Download CSV**.
2. The CSV file is downloaded to your machine.

::::{note}
If the visualization contains data that starts with characters that spreadsheet applications might interpret as formulas (such as `=`, `+`, `-`, or `@`), a warning is displayed.
::::

## Export dashboard configuration [export-dashboards]

You can export a dashboard from {{kib}} in two formats. The JSON format is the modern way to export and recreate dashboards through the {{kib}} dashboards API, and is intended to replace the saved-objects-based NDJSON export. While JSON is in technical preview and limited to one dashboard at a time, NDJSON remains the right choice for bulk operations and cross-space moves.

| Format | Use it to | What it includes |
|---|---|---|
| [JSON](#export-dashboard-json) {applies_to}`stack: preview 9.4` {applies_to}`serverless: preview` | Manage a single dashboard as code, version-control it, recreate it through the dashboards API, or inspect its state. | One dashboard, with the panel types and properties that the dashboards API supports. Any panel types and properties not supported by the API are listed in the export flyout and removed from the export. |
| [NDJSON](#export-ndjson) | Move dashboards between spaces or clusters, back them up, or share them in bulk. | The selected dashboards along with their related objects, such as data views and visualizations. Supports exporting multiple dashboards at once. |

### Export as dashboards API-compatible JSON [export-dashboard-json]
```{applies_to}
stack: preview 9.4
serverless: preview
```

Export the JSON source of a dashboard in a format that the {{kib}} dashboards API can consume. Use this option when you want to inspect the state of a dashboard, save it to a file, or send it to the API to recreate the dashboard in another space or instance.

1. Open the dashboard you want to export.
2. From the application menu, select {icon}`download` **Export** → **Export JSON**.
3. In the flyout, review the JSON source. If a panel type or property is not yet supported by the dashboards API, it is removed from the export and listed under **Unsupported properties were removed**. Expand **Show details** to see what was removed.
4. Choose how to use the JSON source:

   * Select **Copy to clipboard** to copy the JSON.
   * Select **Open in Console** to open {{kib}} Dev Tools Console with a Create dashboard API request pre-populated with the JSON source. This option is available if you have access to **Dev Tools**.
   * Select **Download JSON** to save the JSON source to a file.

### Export as NDJSON saved objects [export-ndjson]

Export dashboards as NDJSON files to migrate them to other {{kib}} instances, back them up, or share them with other teams. You can export dashboards from **Stack Management** → **Saved Objects**. To configure and start the export:

1. Select the dashboard that you want, then select **Export**.
2. Enable **Include related objects** if you want objects associated with the selected dashboard, such as data views and visualizations, to also be exported. This option is enabled by default and recommended if you plan to import that dashboard again in a different space or cluster.
3. Select **Export**.

To automate {{kib}}, you can export dashboards as NDJSON using the [Export saved objects API]({{kib-apis}}group/endpoint-saved-objects). It is important to export dashboards with all necessary references.

## Set edit permissions [manage-dashboard-access]
```{applies_to}
serverless: ga
stack: ga 9.3+
```

From the {icon}`share` **Share** dialog, you can choose whether others in the space can edit your dashboard, or only view it:

- **Can edit**: Everybody in the space can edit, delete, and fully manage the dashboard.
- **Can view**: Everybody in the space can view the dashboard, but cannot edit or delete it. They can duplicate it. This read-only setting can be changed at any time by the dashboard owner or a {{kib}} administrator.

:::{include} ../_snippets/dashboard-ownership.md
:::