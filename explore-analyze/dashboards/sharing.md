---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/share-the-dashboard.html
---

# Sharing [share-the-dashboard]

To share a dashboard with a larger audience, click **Share** in the toolbar. For detailed information about the sharing options, refer to [Reporting](../report-and-share.md).

:::{image} https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt9428300b184af4c6/6763173de7201118db0315a7/share-dashboard-copy-link.gif
:alt: getting a shareable link for a dashboard
:::

::::{tip}
When sharing a dashboard with a link while a panel is in maximized view, the generated link will also open the dashboard on the same maximized panel view.
::::



## Export dashboards [export-dashboards]

You can export dashboards from **Stack Management** > **Saved Objects**. To configure and start the export:

1. Select the dashboard that you want, then click **Export**.
2. Enable **Include related objects** if you want that objects associated to the selected dashboard, such as data views and visualizations, also get exported. This option is enabled by default and recommended if you plan to import that dashboard again in a different space or cluster.
3. Select **Export**.

![Option to export a dashboard](../../images/kibana-dashboard-export-saved-object.png "")

To automate {{kib}}, you can export dashboards as NDJSON using the [Export saved objects API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects). It is important to export dashboards with all necessary references.
