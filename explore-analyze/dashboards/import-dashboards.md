---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/_import_dashboards.html
description: Import a Kibana dashboard into another space, instance, or deployment with the Dashboards API, or from an NDJSON file on earlier versions.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Import a dashboard [_import_dashboards]

Import a dashboard to recreate one that was built elsewhere in your own {{product.kibana}} space, instance, or deployment. You might import a dashboard to:

- Promote it across environments, such as from development to staging to production.
- Share it with another team or {{kib}} instance.
- Recreate it from a version-controlled or backed-up definition.

:::::{applies-switch}

::::{applies-item} {stack: preview 9.4, serverless: preview}

The [Dashboards API](create-dashboards-programmatically.md) is the main way to import a dashboard. You recreate a dashboard from its JSON definition: take the dashboard's [API-compatible JSON](sharing.md#export-dashboard-json), exported from the source dashboard or stored in version control, and send it to the Dashboards API in the target space, instance, or deployment. The API creates the dashboard, or updates it in place when you deploy it with the same ID.

For an imported dashboard to work, the objects it references, such as data views and library visualizations, must also exist in the target environment. To version-control dashboards and keep their references portable across environments, refer to [Manage dashboards as code](manage-dashboards-as-code.md).

To move a dashboard to another space within the same deployment, you don't need to export and import it. Instead, [copy it to the target space](../find-and-organize/saved-objects.md#saved-objects-copy-to-other-spaces) from the **Saved Objects** page, together with its related objects.

:::{note}
You can still [import dashboards from NDJSON files](../find-and-organize/saved-objects.md#saved-objects-import) on the **Saved Objects** page, but the Dashboards API is the recommended way to import a dashboard.
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
