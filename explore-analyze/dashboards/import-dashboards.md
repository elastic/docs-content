---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/_import_dashboards.html
description: Move a Kibana dashboard into another space or deployment by copying it, recreating it with the Dashboards API, or importing it from an NDJSON file.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Import a dashboard [_import_dashboards]

Bring a dashboard from another {{product.kibana}} space, instance, or deployment into your own.

:::::{applies-switch}

::::{applies-item} {stack: preview 9.4, serverless: preview}

Choose the approach that matches where the dashboard is coming from:

- **From another space in the same deployment**: [copy the dashboard to the target space](../find-and-organize/saved-objects.md#saved-objects-copy-to-other-spaces) from the **Saved Objects** page. The copy includes the dashboard's related objects, such as data views.
- **From another deployment, or as part of a code-based workflow**: recreate the dashboard from its JSON definition with the [Dashboards API](create-dashboards-programmatically.md). [Export the source dashboard as API-compatible JSON](sharing.md#export-dashboard-json), then send it to the API in the target deployment. To version-control dashboards and keep their references portable across environments, refer to [Manage dashboards as code](manage-dashboards-as-code.md).

:::{note}
You can still [import dashboards from NDJSON files](../find-and-organize/saved-objects.md#saved-objects-import) on the **Saved Objects** page. The approaches above are the recommended way to move dashboards across spaces and deployments.
:::

::::

::::{applies-item} {stack: ga 9.0-9.3}

Import dashboards into {{product.kibana}} from NDJSON files exported from other {{product.kibana}} instances or spaces. When you import a dashboard, you also import its related objects such as data views and visualizations, so you can migrate dashboards between environments or share them with other teams.

To import dashboards, you need:

* **All** privilege for the **Dashboard** and **Saved Objects Management** features in {{product.kibana}}
* An NDJSON file containing the dashboard and its related objects
* Access to **Stack Management** in {{product.kibana}}

You can import dashboards from the [Saved Objects](../find-and-organize/saved-objects.md) page under **Stack Management**.

When importing dashboards, you also import their related objects, such as data views and visualizations. Import options allow you to define how the import should behave with these related objects:

* **Check for existing objects**: When selected, objects are not imported when another object with the same ID already exists in this space or cluster. For example, if you import a dashboard that uses a data view which already exists, the data view is not imported and the dashboard uses the existing data view instead. You can also choose to select manually which of the imported or the existing objects are kept by selecting **Request action on conflict**.
* **Create new objects with random IDs**: All related objects are imported and are assigned a new ID to avoid conflicts.

![Import panel](/explore-analyze/images/kibana-dashboard-import-saved-object.png "")

::::

:::::
