---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/_import_dashboards.html
description: Import a dashboard exported from another Kibana space, instance, deployment, or project, using the Dashboards app, the Dashboards API, or Saved Objects.
type: how-to
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Import a dashboard [_import_dashboards]

Import a dashboard that was exported from another {{product.kibana}} space, instance, deployment, or project. How you import it depends on the format it was exported in. Refer to [](sharing.md#export-dashboards) for the export options, then use the matching import method:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` **JSON**: import it with **Import dashboard** in the **Dashboards** app.
- {applies_to}`stack: ga 9.5+, preview =9.4` {applies_to}`serverless: ga` **JSON**: import it with the [Dashboards API](create-dashboards-programmatically.md). This is the recommended method.
- **NDJSON**: import it with the [Saved Objects API]({{kib-apis}}group/endpoint-saved-objects), or from the **Saved Objects** page.

::::::{tab-set}

:::::{tab-item} JSON (Dashboards app)

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` Recreate a dashboard from its JSON file without writing an API request. {{kib}} checks the file as soon as you select it, so you can see what it removes and what the dashboard depends on before you import.

**Prerequisites**

- A dashboard JSON file of 1 MB or less, created with **Export JSON**. Refer to [](sharing.md#export-dashboard-json) to produce it.
- **All** privilege for the **Dashboard** feature in {{product.kibana}}. Without it, **Import dashboard** doesn't appear.

**Import the file**

1. Go to **Dashboards**.
2. From the application menu, select **Import dashboard**.
3. In the **Import dashboard** flyout, select your file under **Select a JSON file**. {{kib}} checks the file right away.
4. Review any messages in the flyout. If {{kib}} shows an error, select a different file. If it shows a warning, review it before you continue.
5. Select **Import**.

{{kib}} creates a new dashboard, closes the flyout, shows a confirmation message, and refreshes the list of dashboards so the new dashboard appears. It never updates an existing dashboard, so importing the same file again creates another dashboard.

**Messages after you select a file**

- **The selected file is too large. The maximum size is 1 MB.** Select a smaller file. **Import** stays unavailable.
- **The selected file does not contain valid JSON.** Select a different file. **Import** stays unavailable.
- **The file could not be imported.** {{kib}} can't validate the file, for example because it isn't a full dashboard definition created with **Export JSON**. **Import** stays unavailable.
- **Unsupported properties were removed.** The file includes panel types or properties that the Dashboards API doesn't support. {{kib}} leaves them out of the imported dashboard. Select **Show details** to see what it removed. **Import** stays available.
- **Review import warnings.** The file references related items, such as data views, tags, or library visualizations. {{kib}} imports only the dashboard. Select **Show details** to see each item's type and ID, and make sure these items exist in the space or cluster where you import. This warning also lists any removed properties. **Import** stays available.

:::::

:::::{tab-item} JSON (Dashboards API)

{applies_to}`stack: ga 9.5+, preview =9.4` {applies_to}`serverless: ga` Recreate the dashboard by sending its JSON definition to the [Dashboards API](create-dashboards-programmatically.md). This is the recommended import method.

**Prerequisites**

- The dashboard's API-compatible JSON. Refer to [](sharing.md#export-dashboard-json) to produce it.
- **All** privilege for the **Dashboard** feature in {{product.kibana}}.
- A way to call the API, such as {{kib}} Dev Tools Console or an API key.

Send the JSON to the Dashboards API in the target space, instance, deployment, or project. The [JSON export flow](sharing.md#export-dashboard-json) can open a pre-populated request in {{kib}} Dev Tools Console, where you set the target space before sending it. The API creates the dashboard, or updates it in place when you send it with an existing ID.

For the imported dashboard to work, the objects it references, such as data views and library visualizations, must also exist in the target environment. To version-control dashboards and keep their references portable across environments, refer to [Manage dashboards as code](manage-dashboards-as-code.md).

:::::

:::::{tab-item} NDJSON (Saved Objects)

Import the dashboard and its related objects from an NDJSON file on the **Saved Objects** page.

**Prerequisites**

- An NDJSON file containing the dashboard and its related objects. Refer to [](sharing.md#export-dashboards) to produce it.
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
