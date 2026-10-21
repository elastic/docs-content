---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/open-the-dashboard.html
description: Open and edit an existing Kibana dashboard to modify its panels, settings, and controls.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Edit a dashboard [open-the-dashboard]

Open an existing dashboard in {{product.kibana}} to modify its visualizations, add or remove panels, adjust settings, or change filtering controls. When you have the appropriate permissions, dashboards automatically open in **Edit** mode, allowing you to make changes immediately.

## Requirements [edit-dashboard-requirements]

To edit a dashboard, you need the **All** privilege for the **Dashboard** feature in {{product.kibana}}.

::::{note}
Managed dashboards created by integrations can't be edited directly, but you can [duplicate](duplicate-dashboards.md) them and edit the duplicates.
::::

## Edit an existing dashboard [edit-dashboard-steps]

1. Open the **Dashboards** page in {{product.kibana}}.
2. Locate the dashboard you want to edit.

   ::::{tip}
   When looking for a specific dashboard, you can filter them by tag or by creator, or search the list based on their name and description. The creator information is only available for dashboards created on or after version 8.14.
   ::::

3. Click the dashboard name you want to open.
   The dashboard opens automatically in **Edit** mode if you have the right permissions. You can switch between edit and view modes from the application menu.

5. Make the changes that you need to the dashboard:

    * Adjust the dashboard’s settings
    * [Add, remove, move, or edit panels](../visualize.md#panels-editors)
    * [Change the available controls](../visualize/dashboard-controls.md)

6. **Save** the dashboard.

## Undo and redo dashboard changes [undo-redo-dashboard]
```{applies_to}
serverless: ga
stack: ga 9.6+
```

If you move a panel or change a setting by mistake while you edit a dashboard, you can step back through your changes one at a time, and step forward again if you change your mind. Changes that you don't undo stay in place.

To go back one change, click **Undo** {icon}`undo` in the application menu, or press {kbd}`cmd+z` (Mac) / {kbd}`ctrl+z` (Windows and Linux). To bring back a change that you undid, click **Redo** {icon}`redo`, or press {kbd}`cmd+y` (Mac) / {kbd}`ctrl+y` (Windows and Linux).

Undo and redo behave as follows:

* The history covers your current editing session. It keeps about the 100 most recent changes, and it clears when you leave the dashboard.
* If you undo a change and then make a new one, you can no longer redo the changes that you undid.
* **Undo** and **Redo** are unavailable while the dashboard loads data or while a panel editor is open.
* The keyboard shortcuts don't work while the cursor is in an input field.

To discard all unsaved changes at once, use [Reset changes](#reset-the-dashboard) instead.

## Reset dashboard changes [reset-the-dashboard]

When editing a dashboard, you can revert any changes you’ve made since the last save using the **Reset**/**Reset changes** button.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` To step back through your changes one at a time instead, refer to [Undo and redo dashboard changes](#undo-redo-dashboard).

::::{note}
Once changes are saved, you can no longer revert them in one click, and instead have to edit the dashboard manually.
::::