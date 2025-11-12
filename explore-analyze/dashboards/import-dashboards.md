---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/_import_dashboards.html
description: Import dashboards with related objects from saved object files. Configure import behavior for data views, visualizations, and handle object conflicts during migration.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Import a dashboard [_import_dashboards]

You can import dashboards from the [Saved Objects](../find-and-organize/saved-objects.md) page under **Stack Management**.

When importing dashboards, you also import their related objects, such as data views and visualizations. Import options allow you to define how the import should behave with these related objects.

* **Check for existing objects**: When selected, objects are not imported when another object with the same ID already exists in this space or cluster. For example, if you import a dashboard that uses a data view which already exists, the data view is not imported and the dashboard uses the existing data view instead. You can also chose to select manually which of the imported or the existing objects are kept by selecting **Request action on conflict**.
* **Create new objects with random IDs**: All related objects are imported and are assigned a new ID to avoid conflicts.

![Import panel](/explore-analyze/images/kibana-dashboard-import-saved-object.png "")
