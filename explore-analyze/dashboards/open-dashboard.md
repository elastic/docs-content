---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/open-the-dashboard.html
description: Edit dashboard content, settings, and layout with Edit mode. Adjust panels, controls, and configurations to maintain and update visualizations for viewers.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Edit dashboards [open-the-dashboard]

To modify an existing dashboard, you need to switch to Edit mode where you can add or remove panels, adjust settings, modify controls, and reorganize the layout. Changes you make are not visible to other viewers until you save the dashboard.

This guide shows you how to open a dashboard for editing, make modifications, and save or reset your changes.

To edit a dashboard:

1. Open the **Dashboards** page in {{kib}}.
2. Locate the dashboard you want to edit.

   ::::{tip}
   When looking for a specific dashboard, you can filter them by tag or by creator, or search the list based on their name and description. Note that the creator information is only available for dashboards created on or after version 8.14.
   ::::

3. Click the dashboard name you want to open.
   The dashboard opens automatically in **Edit** mode if you have the right permissions. You can switch between edit and view modes from the toolbar.

5. Make the changes that you need to the dashboard:

    * Adjust the dashboard’s settings
    * [Add, remove, move, or edit panels](../visualize.md#panels-editors)
    * [Change the available controls](add-controls.md)

6. **Save** the dashboard.

::::{note}
Managed dashboards can’t be edited directly, but you can [duplicate](duplicate-dashboards.md) them and edit these duplicates.
::::

## Reset dashboard changes [reset-the-dashboard]

When editing a dashboard, you can revert any changes you’ve made since the last save using the **Reset** button in the toolbar.

::::{note}
Once changes are saved, you can no longer revert them in one click, and instead have to edit the dashboard manually.
::::