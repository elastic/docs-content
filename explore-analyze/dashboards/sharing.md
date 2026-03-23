---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/share-the-dashboard.html
navigation_title: Share and export
description: Share Kibana dashboards using links or embeds, and export them as PDF, PNG, or CSV files.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Share and export dashboards [share-the-dashboard]

{{kib}} provides several ways to share dashboards with others and export their content:

- **[Share with a link](#share-dashboard-link)**: Copy a direct link to the dashboard.
- **[Embed in a webpage](#embed-dashboard)**: Embed an interactive dashboard as an iframe on external web pages.
- **[Export as PDF or PNG](#export-dashboard-pdf-png)**: Generate a report file of your dashboard.
- **[Download visualization data as CSV](#download-csv)**: Download the data behind individual Lens visualizations.
- **[Export dashboard configuration](#export-dashboards)**: Export the dashboard definition as an NDJSON file for backup or migration.

You can also [manage access permissions](#manage-dashboard-access) to control who can view or edit your dashboard.

To get started, click {icon}`share` **Share** in the toolbar.

:::{image} /explore-analyze/images/share-dashboard.png
:screenshot:
:width: 60%
:::

## Manage access permissions [manage-dashboard-access]
```{applies_to}
serverless:
stack: ga 9.3+
```

From the {icon}`share` **Share** dialog, you can set whether other users in the space can edit or view a dashboard you own:

- **Can edit**: Everybody in the space can edit, delete, and fully manage the dashboard.
- **Can view**: Everybody in the space can view the dashboard, but cannot edit or delete it. They can duplicate it. This read-only setting can be changed at any time by the dashboard owner or a {{kib}} administrator.

:::{include} ../_snippets/dashboard-ownership.md
:::

## Share with a link [share-dashboard-link]

Share a direct link to your dashboard so that others can access it in {{kib}}.

1. Open the dashboard, then click {icon}`share` **Share**.
2. On the **Link** tab, click **Copy link**.

The link requires authentication. To access the dashboard, users must log in to {{kib}} with an account that has the necessary permissions.

{applies_to}`stack: ga 9.1` When sharing, you can choose to use a relative or an absolute time range:

* **Relative time range**: The link shows current data. For example, if you share a "Last 7 days" view, users always see the most recent 7 days when they open the link.
* **Absolute time range** (default): The link shows a fixed time period. For example, if you share a "Last 7 days" view on January 7, 2025, the link always shows that exact week of January 1-7, 2025, regardless of when users open the link.

::::{tip}
When sharing a dashboard with a link while a panel is in maximized view, the generated link also opens the dashboard with the same panel maximized.
::::

::::{tip}
When sharing an object with unsaved changes, you get a temporary link that might break in the future, for example in case of upgrade. Save the dashboard first to get a permanent link.
::::

Anonymous users can also access the link if you have configured [Anonymous authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-authentication.md#anonymous-authentication) and your anonymous service account has the necessary privileges.

## Embed in a webpage [embed-dashboard]
```{applies_to}
stack: ga
serverless: unavailable
```

Embed a fully interactive dashboard as an iframe on an internal company website or personal web page.

1. Open the dashboard, then click {icon}`share` **Share**.
2. Go to the **Embed** tab.
3. Under **Include**, select which parts of the dashboard to display in the embedded view:
   - **Top menu**
   - **Query**
   - **Time filter**
   - **Filter bar** (enabled by default)
4. Click **Copy embed code**.
5. Paste the iframe code into your web page HTML.

<!-- TODO: add screenshot of the embed tab -->

For information about granting access to embedded dashboards, refer to [Authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/user-authentication.md).

::::{tip}
Save the dashboard before generating the embed code. Embedding a dashboard with unsaved changes may result in an embed code that does not work properly.
::::

## Export as PDF or PNG [export-dashboard-pdf-png]
```{applies_to}
stack: ga
serverless: unavailable
```

Generate and download a PDF or PNG file of your dashboard. PDF and PNG reports are a [subscription feature](https://www.elastic.co/subscriptions).

1. Open the dashboard, then click {icon}`download` **Export** in the toolbar.
2. Select **PDF** or **PNG**.
3. Optional: For PDF exports, enable **Print format** to create a printer-friendly report with multiple A4 portrait pages and two visualizations per page.
4. Click the button to generate the report.

A notification confirms that the report is queued. When it is ready, download it from the **Reporting** page under **Stack Management > Alerts and Insights > Reporting**.

:::{note}
For more information on how to configure reporting in {{kib}}, refer to [Configure reporting in {{kib}}](/deploy-manage/kibana-reporting-configuration.md).
:::

::::{note}
When you create a dashboard report that includes a data table or Discover session, the PDF includes only the visible data.
::::

{applies_to}`stack: ga 9.1+` You can also schedule recurring exports. Refer to [Automatically generate reports](../report-and-share/automating-report-generation.md) to learn more.

For general information about reporting across all {{kib}} apps, known limitations, and troubleshooting, refer to [Reporting and sharing](../report-and-share.md).

## Download visualization data as CSV [download-csv]

You can download the data displayed in individual **Lens** visualizations on your dashboard as CSV files.

1. On the dashboard, open the Lens visualization you want to export.
2. Click {icon}`download` **Export**, then select **CSV Download**.
3. The CSV file is downloaded to your machine.

::::{note}
If the visualization contains data that starts with characters that spreadsheet applications may interpret as formulas (such as `=`, `+`, `-`, or `@`), a warning is displayed.
::::

## Export dashboard configuration [export-dashboards]

Export dashboards as NDJSON files to migrate them to other {{product.kibana}} instances, back them up, or share them with other teams. You can export dashboards from **Stack Management** > **Saved Objects**. To configure and start the export:

1. Select the dashboard that you want, then click **Export**.
2. Enable **Include related objects** if you want objects associated with the selected dashboard, such as data views and visualizations, to also be exported. This option is enabled by default and recommended if you plan to import that dashboard again in a different space or cluster.
3. Select **Export**.

![Option to export a dashboard](/explore-analyze/images/kibana-dashboard-export-saved-object.png "")

To automate {{kib}}, you can export dashboards as NDJSON using the [Export saved objects API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects). It is important to export dashboards with all necessary references.
