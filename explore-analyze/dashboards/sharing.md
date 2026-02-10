---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/share-the-dashboard.html
description: Share Kibana dashboards with your team using links, embeds, or by exporting them as NDJSON files for import into other environments.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Sharing dashboards [share-the-dashboard]

Share your dashboards with team members and stakeholders using shareable links, embeds, or file exports. You can also manage permissions to control who can view or edit a dashboard. Kibana provides multiple sharing options to fit different collaboration needs, from quick URL sharing to exporting complete dashboard configurations for migration between environments.
To share a dashboard with a larger audience, click {icon}`share` **Share** in the toolbar.

:::{image} /explore-analyze/images/share-dashboard.png
:screenshot:
:width: 60%
:::

## Manage access of other users on your dashboard
```{applies_to}
serverless:
stack: ga 9.3+
```

From the icon {icon}`share`, you can set whether other users in the space can edit or view a dashboard you own:

- **Can edit**: Everybody in the space can edit, delete, and fully manage the dashboard.
- **Can view**: Everybody in the space can view the dashboard, but cannot edit or delete it. They can duplicate it. This read-only setting can be changed at any time by the dashboard owner or a {{kib}} administrator. 

By default, the dashboard owner is the dashboard creator. This cannot be changed and is not currently visible in the UI. However, in some cases the creator and owner can be different users. For example, if user A creates a dashboard and user B exports and re-imports it in the same space (overwriting the existing dashboard), the creator becomes user B while user A remains the owner.

::::{note}
{{kib}} administrators always have write access to all dashboards.
::::

## Share a dashboard [share-dashboard-link]

You can share your dashboards in several ways:
- [Share with a direct link](../report-and-share.md#share-a-direct-link)
- {applies_to}`serverless: unavailable` [Embed a dashboard outside of {{kib}}](../report-and-share.md#embed-code)

For detailed information about the sharing options and time ranges, refer to [Reporting and sharing](../report-and-share.md).

::::{tip}
When sharing a dashboard with a link while a panel is in maximized view, the generated link will also open the dashboard on the same maximized panel view.
::::

## Export dashboards [export-dashboards]

Export dashboards as NDJSON files to migrate them to other {{product.kibana}} instances, back them up, or share them with other teams. You can export dashboards from **Stack Management** > **Saved Objects**. To configure and start the export:

1. Select the dashboard that you want, then click **Export**.
2. Enable **Include related objects** if you want that objects associated to the selected dashboard, such as data views and visualizations, also get exported. This option is enabled by default and recommended if you plan to import that dashboard again in a different space or cluster.
3. Select **Export**.

![Option to export a dashboard](/explore-analyze/images/kibana-dashboard-export-saved-object.png "")

To automate {{kib}}, you can export dashboards as NDJSON using the [Export saved objects API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects). It is important to export dashboards with all necessary references.
