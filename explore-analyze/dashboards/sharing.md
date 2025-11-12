---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/share-the-dashboard.html
description: Share dashboards with links, reports, or exports. Generate shareable URLs with current filters and time ranges, or export dashboard configurations as NDJSON.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Sharing dashboards [share-the-dashboard]

To share a dashboard with a larger audience, click {icon}`share` **Share** in the toolbar. For detailed information about the sharing options and time ranges, refer to [Reporting and sharing](../report-and-share.md).

![getting a shareable link for a dashboard](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/bltc45bb05c1fab3e60/68826ffb4f04ad6e224c2248/share-dashboard.gif)

::::{tip}
When sharing a dashboard with a link while a panel is in maximized view, the generated link will also open the dashboard on the same maximized panel view.
::::



## Export dashboards [export-dashboards]

You can export dashboards from **Stack Management** > **Saved Objects**. To configure and start the export:

1. Select the dashboard that you want, then click **Export**.
2. Enable **Include related objects** if you want that objects associated to the selected dashboard, such as data views and visualizations, also get exported. This option is enabled by default and recommended if you plan to import that dashboard again in a different space or cluster.
3. Select **Export**.

![Option to export a dashboard](/explore-analyze/images/kibana-dashboard-export-saved-object.png "")

To automate {{kib}}, you can export dashboards as NDJSON using the [Export saved objects API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects). It is important to export dashboards with all necessary references.
