---
navigation_title: Save a search for reuse
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/save-open-search.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Save Discover sessions to reuse searches, queries, and configured views. Add saved searches to dashboards or use them as a foundation for building visualizations.
---

# Save a search for reuse [save-open-search]

Saved **Discover** sessions preserve your queries, filters, column selections, and view configurations for reuse. Save sessions to return to specific data explorations, share search results with team members, add searches to dashboards, or use them as a foundation for building visualizations. This guide shows how to save, reopen, duplicate, and manage Discover sessions.

## Requirements [save-search-requirements]

To save searches, you need **Create** and **Edit** permissions for the {{saved-objects-app}} feature in {{product.kibana}}. If you don't have these permissions, the **Save** button won't be visible. For more information, refer to [Read-only access](#discover-read-only-access).


### Read-only access [discover-read-only-access]

If you don’t have sufficient privileges to save Discover sessions, the following indicator is displayed and the **Save** button is not visible. For more information, refer to [Granting access to {{kib}}](elasticsearch://reference/elasticsearch/roles.md).

:::{image} /explore-analyze/images/kibana-read-only-badge.png
:alt: Example of Discover's read only access indicator in the {{product.kibana}} header
:screenshot:
:::


## Save a Discover session [_save_a_discover_session]

By default, a Discover session stores the query text, filters, and current view of **Discover**, including the columns and sort order in the document table, and the {{data-source}}.

1. Once you’ve created a view worth saving, select **Save** in the application menu. A modal with several options opens:
    1. Enter a **Title** for the session, and optionally a **Description** and [**Tags**](../find-and-organize/tags.md).
    2. If the session is time-based, turn on **Store time with Discover session** to save the current time filter and refresh interval with it.
    3. {applies_to}`stack: ga 9.4` {applies_to}`serverless: ga` Under **Add to dashboard**, select **Existing** to add the session as a panel on a dashboard you choose, **New** to add it to a brand-new dashboard, or **None** to save the session to the library only.
2. Select **Save**.
3. To reload your search results in **Discover**, select **Open** in the application menu, and select the saved Discover session.

If the saved Discover session is associated with a different {{data-source}} than is currently selected, opening the saved Discover session changes the selected {{data-source}}. The query language used for the saved Discover session is also automatically selected.



## Duplicate a Discover session [_duplicate_a_discover_session]

1. In **Discover**, open the Discover session that you want to duplicate.
2. In the application menu, click **Save**.
3. Give the session a new name.
4. Turn on **Save as new Discover session**.
5. Click **Save**.


## Add search results to a dashboard [_add_search_results_to_a_dashboard]

1. Go to **Dashboards**.
2. Open or create the dashboard, then click **Edit**.
3. Click **Add from library**.
4. From the **Types** dropdown, select **Discover session**.
5. Select the Discover session that you want to add, then click **X** to close the list.

### Choose which tab to display [discover-session-choose-tab]
```{applies_to}
stack: ga 9.4
serverless: ga
```

If the Discover session contains multiple tabs, you can choose which tab the panel displays.

1. Open the panel menu and select **Edit**.
2. From the tab selector, select the tab you want to display.

   :::{image} /explore-analyze/images/discover-session-tab-selector.png
   :alt: Tab selector showing the list of available tabs for a Discover session panel
   :screenshot:
   :::

3. Select **Apply**.

### Save edits as a new Discover session [discover-session-save-as-from-dashboard]
```{applies_to}
stack: ga 9.4
serverless: ga
```

When editing a Discover session panel from a dashboard, you can save your changes as a new Discover session instead of updating the panel. This works whether the panel was added from the library or created directly on the dashboard.

1. From the dashboard, hover over the panel and select {icon}`pencil` **Edit Discover session configuration**.
2. Make your changes in **Discover**.
3. In the application menu, open the menu next to **Save and return** and select **Save as**.
4. In the **Save Discover session** modal, enter a **Title** for the new session, and optionally a **Description** and [**Tags**](../find-and-organize/tags.md).
5. In **Add to dashboard**, choose where to display the new session:

   - **Existing**: Add the new session to a dashboard you select.

     - If you select the dashboard the panel came from, the original panel is updated in place to reference the new session, in the same position. If the replaced panel was linked to the library, you can still find it unchanged in the library. If the panel wasn't linked to the library, it is lost and replaced by the newly saved session.
     - If you select a different dashboard, the original panel is unchanged, and the new session is added as a separate panel on the dashboard you selected.

   - **New**: Save the session and add it as a panel on a new dashboard. The original panel is unchanged.
   - **None**: Save the session to the library only, without adding it to a dashboard. The original panel is unchanged.

6. Select **Save and add to library** (when **None** is selected) or **Save and go to Dashboard** (when **Existing** or **New** is selected).

Upon saving, you navigate to the new session in **Discover** when you selected **None**, or to the corresponding dashboard when you selected **Existing** or **New**.
