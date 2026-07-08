---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/_import_dashboards.html
description: Import a Kibana dashboard exported from another space, instance, deployment, or project, using the Dashboards API or the Saved Objects API.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Import a dashboard [_import_dashboards]

Import a dashboard that was exported from another {{product.kibana}} space, instance, deployment, or project. How you import it depends on the format it was exported in. Refer to [Share and export dashboards](sharing.md#export-dashboards) for the export options, then use the matching import method:

- {applies_to}`stack: preview 9.4` {applies_to}`serverless: preview` **JSON**: import it with the [Dashboards API](create-dashboards-programmatically.md). This is the recommended method.
- **NDJSON**: import it with the [Saved Objects API]({{kib-apis}}group/endpoint-saved-objects), or from the **Saved Objects** page.

::::::{tab-set}

:::::{tab-item} JSON (Dashboards API)

{applies_to}`stack: preview 9.4` {applies_to}`serverless: preview` Recreate the dashboard by sending its JSON definition to the [Dashboards API](create-dashboards-programmatically.md). This is the recommended import method.

**Prerequisites**

- The dashboard's API-compatible JSON. Refer to [Share and export dashboards](sharing.md#export-dashboard-json) to produce it.
- **All** privilege for the **Dashboard** feature in {{product.kibana}}.
- A way to call the API, such as {{kib}} Dev Tools Console or an API key.

Send the JSON to the Dashboards API in the target space, instance, deployment, or project. The [JSON export flow](sharing.md#export-dashboard-json) can open a pre-populated request in {{kib}} Dev Tools Console, where you set the target space before sending it. The API creates the dashboard, or updates it in place when you send it with an existing ID.

For the imported dashboard to work, the objects it references, such as data views and library visualizations, must also exist in the target environment. To version-control dashboards and keep their references portable across environments, refer to [Manage dashboards as code](manage-dashboards-as-code.md).

:::::

:::::{tab-item} NDJSON (Saved Objects)

Import the dashboard and its related objects from an NDJSON file on the **Saved Objects** page.

**Prerequisites**

- An NDJSON file containing the dashboard and its related objects. Refer to [Share and export dashboards](sharing.md#export-dashboards) to produce it.
- **All** privilege for the **Dashboard** and **Saved Objects Management** features in {{product.kibana}}.
- Access to **Stack Management** in {{product.kibana}}.

Import the dashboard from the [Saved Objects](../find-and-organize/saved-objects.md) page under **Stack Management**. When you import a dashboard, you also import its related objects, such as data views and visualizations. Import options control how the import handles these related objects:

- **Check for existing objects**: When selected, objects are not imported when another object with the same ID already exists in this space or cluster. For example, if you import a dashboard that uses a data view which already exists, the data view is not imported and the dashboard uses the existing data view instead. You can also choose which of the imported or existing objects to keep by selecting **Request action on conflict**.
- **Create new objects with random IDs**: All related objects are imported and are assigned a new ID to avoid conflicts.

![Import panel](/explore-analyze/images/kibana-dashboard-import-saved-object.png "")

To automate the import, use the [import saved objects API]({{kib-apis}}operation/operation-post-saved-objects-import) instead.

:::::

::::::

:::{note}
To move a dashboard to another space within the same deployment, you don't need to export and import it. Instead, [copy it to the target space](../find-and-organize/saved-objects.md#saved-objects-copy-to-other-spaces) from the **Saved Objects** page, together with its related objects. To automate this, use the [copy saved objects to space API]({{kib-apis}}operation/operation-post-spaces-copy-saved-objects).
:::
