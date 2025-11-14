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

# Import dashboards [_import_dashboards]

To move dashboards between {{product.kibana}} instances or restore dashboards from backup, use the import feature. Import works with NDJSON files that contain dashboard definitions and their dependencies.

When you import a dashboard, {{product.kibana}} also imports related objects like {{data-sources}} and visualizations. You can control whether to overwrite existing objects or create new ones with random IDs to avoid conflicts.

* **Check for existing objects**: When selected, objects are not imported when another object with the same ID already exists in this space or cluster. For example, if you import a dashboard that uses a data view which already exists, the data view is not imported and the dashboard uses the existing data view instead. You can also chose to select manually which of the imported or the existing objects are kept by selecting **Request action on conflict**.
* **Create new objects with random IDs**: All related objects are imported and are assigned a new ID to avoid conflicts.

![Import panel](/explore-analyze/images/kibana-dashboard-import-saved-object.png "")
