---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/duplicate-dashboards.html
description: Duplicate an existing Kibana dashboard to create a copy that you can customize independently without affecting the original.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Duplicate a dashboard [duplicate-dashboards]

Create a copy of an existing dashboard in {{product.kibana}} to customize it independently without affecting the original. This is particularly useful when you want to create variations of a dashboard for different teams or use cases, or when you need to edit a managed dashboard that comes from an integration.

## Requirements [duplicate-dashboard-requirements]

To duplicate a dashboard, you need:

* **All** privilege for the **Dashboard** feature in {{product.kibana}}

## Duplicate a dashboard [duplicate-dashboard-steps]

1. Open the dashboard you want to duplicate.
2. Exit the edit mode, and click **Duplicate** in the toolbar.
3. In the **Duplicate dashboard** window, enter a title and optional description and tags.
4. Click **Save**.

You will be redirected to the duplicated dashboard.

To duplicate a managed dashboard, follow the instructions above or click the **Managed** badge in the toolbar. Then click **Duplicate** in the dialog that appears.

:::{image} /explore-analyze/images/kibana-managed-dashboard-popover-8.16.0.png
:alt: Managed badge dialog with Duplicate button
:screenshot:
:width: 50%
:::

