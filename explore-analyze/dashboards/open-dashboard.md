---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/open-the-dashboard.html
---

# Edit a dashboard [open-the-dashboard]

1. Open the **Dashboards** page in {{kib}}.
2. Locate the dashboard you want to edit.

   ::::{tip}
   When looking for a specific dashboard, you can filter them by tag or by creator, or search the list based on their name and description. Note that the creator information is only available for dashboards created on or after version 8.14.
   ::::

3. Click the dashboard **Title** you want to open.
4. Make sure that you are in **Edit** mode to be able to make changes to the dashboard. You can switch between **Edit** and **View** modes from the toolbar.
   ![Switch between Edit and View modes](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt619b284e92c2be27/6750f3a512a5eae780936fe3/switch-to-view-mode-8.17.0.gif)

5. Make the changes that you need to the dashboard:

    * Adjust the dashboard’s settings
    * [Add, remove, move, or edit panels](../visualize.md#panels-editors)
    * [Change the available controls](add-controls.md)

6. **Save** the dashboard. You automatically switch to **View** mode upon saving.

::::{note}
Managed dashboards can’t be edited directly, but you can [duplicate](duplicate-dashboards.md) them and edit these duplicates.
::::


## Reset dashboard changes [reset-the-dashboard]

When editing a dashboard, you can revert any changes you’ve made since the last save using **Reset dashboards**.

::::{note}
Once changes are saved, you can no longer revert them in one click, and instead have to edit the dashboard manually.
::::


1. In the toolbar, click **Reset**.
2. On the **Reset dashboard?** window, click **Reset dashboard**.
   ![Reset dashboard to revert unsaved changes](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blte0c08bede75b3874/6750f5566cdeea14b273b048/reset-dashboard-8.17.0.gif)
