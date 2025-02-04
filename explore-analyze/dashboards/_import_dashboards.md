---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/_import_dashboards.html
---

# Import dashboards [_import_dashboards]

You can import dashboards from the **Saved Objects*** page under ***Stack Management**. Refer to [Manage saved objects](../find-and-organize/saved-objects.md).

When importing dashboards, you also import their related objects, such as data views and visualizations. Import options allow you to define how the import should behave with these related objects.

* **Check for existing objects***: When selected, objects are not imported when another object with the same ID already exists in this space or cluster. For example, if you import a dashboard that uses a data view which already exists, the data view is not imported and the dashboard uses the existing data view instead. You can also chose to select manually which of the imported or the existing objects are kept by selecting ***Request action on conflict**.
* **Create new objects with random IDs**: All related objects are imported and are assigned a new ID to avoid conflicts.

![Import panel](../../images/kibana-dashboard-import-saved-object.png "")
