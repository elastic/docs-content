---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/reports.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
description: View and manage generated reports for saved searches, dashboards, and visualizations. Download CSV reports from Discover and track reporting history.
---

# Reports [reports]

The {{reports-app}} management page displays a history of generated reports from Discover searches, dashboards, and visualizations. From this page, you can download completed reports, view report details, or delete old reports to manage storage.

{{reports-app}} are typically generated as CSV files for Discover searches or PDFs for dashboards and visualizations. The management interface shows report status, creation time, and file size.

:::{image} /explore-analyze/images/serverless-reports-management.png
:alt: {{reports-app}}
:screenshot:
:::

You can download or view details about the report by clicking the icons in the actions menu.

To delete one or more reports, select their checkboxes then click **Delete reports**.
