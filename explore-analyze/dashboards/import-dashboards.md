---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/_import_dashboards.html
description: Import dashboards and their related objects into Kibana from NDJSON files using the Saved Objects interface.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Import a dashboard [_import_dashboards]

Import dashboards into {{product.kibana}} from NDJSON files exported from other {{product.kibana}} instances or spaces. When you import a dashboard, you also import its related objects such as data views and visualizations, making it easy to migrate dashboards between environments or share them with other teams.

## Requirements [import-dashboard-requirements]

To import dashboards, you need:

* **Create** and **Edit** permissions for the **Dashboard** and **Saved Objects** features in {{product.kibana}}
* An NDJSON file containing the dashboard and its related objects
* Access to **Stack Management** in {{product.kibana}}

## Import a dashboard [import-dashboard-steps]

You can import dashboards from the [Saved Objects](../find-and-organize/saved-objects.md) page under **Stack Management**.

When importing dashboards, you also import their related objects, such as data views and visualizations. Import options allow you to define how the import should behave with these related objects:

* **Check for existing objects**: When selected, objects are not imported when another object with the same ID already exists in this space or cluster. For example, if you import a dashboard that uses a data view which already exists, the data view is not imported and the dashboard uses the existing data view instead. You can also chose to select manually which of the imported or the existing objects are kept by selecting **Request action on conflict**.
* **Create new objects with random IDs**: All related objects are imported and are assigned a new ID to avoid conflicts.

![Import panel](/explore-analyze/images/kibana-dashboard-import-saved-object.png "")
