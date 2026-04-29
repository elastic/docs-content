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
    3. {applies_to}`stack: ga 9.5` {applies_to}`serverless: ga` In **Add to dashboard**, select **Existing** to add the session as a panel on a dashboard you choose, **New** to add it to a brand-new dashboard, or **None** to save the session to the library.
2. Select **Save**.
3. To reload your search results in **Discover**, select **Open** in the application menu, and select the saved Discover session.

If the saved Discover session is associated with a different {{data-source}} than is currently selected, opening the saved Discover session changes the selected {{data-source}}. The query language used for the saved Discover session is also automatically selected.



## Duplicate a Discover session [_duplicate_a_discover_session]

To duplicate an existing Discover session as a new one, the workflow depends on the version you're using.

::::{applies-switch}

:::{applies-item} { stack: ga 9.4+, serverless: ga }
1. In **Discover**, open the Discover session that you want to duplicate.
2. In the application menu, open the menu next to **Save** and select **Save as**. The **Save Discover session** modal opens.
3. Enter a **Title** for the new session, and optionally a **Description** and [**Tags**](../find-and-organize/tags.md).
4. {applies_to}`stack: ga 9.5` {applies_to}`serverless: ga` Optionally, in **Add to dashboard**, add the new session to a dashboard at the same time as you save it. For details, refer to [Add the session to a dashboard when saving it from Discover](#save-discover-session-with-add-to-dashboard).
5. Select **Save**.
:::

:::{applies-item} { stack: ga 9.0-9.3 }
1. In **Discover**, open the Discover session that you want to duplicate.
2. In the application menu, select **Save**.
3. Give the session a new name.
4. Turn on **Save as new Discover session**.
5. Select **Save**.
:::

::::


## Use Discover sessions in dashboards [_add_search_results_to_a_dashboard]

You can add different pieces of a Discover session to a dashboard:

- [The visualization](#add-discover-visualization-to-dashboard)
- [The data table](#save-table-to-dashboard), that contains the results of a particular query
- [The entire Discover session](#add-full-discover-session-to-dashboard), that lets you choose which tab to display when you set up the panel on the dashboard

### Add the Discover visualization to a dashboard [add-discover-visualization-to-dashboard]

When a query in Discover produces a chart, you can save that chart as a visualization panel on a new or existing dashboard, without saving the Discover session itself. The exact flow depends on the query mode you're using in Discover.

To use either workflow, you need permission to view and create dashboards.

#### In {{esql}} mode [add-discover-visualization-esql]

1. In Discover, run an {{esql}} query that produces a chart.
2. Next to the chart, select {icon}`app_dashboard` **Save visualization to dashboard** (or {icon}`save` **Save visualization** in versions earlier than 9.4).
3. Enter a title for the panel, and optionally a description.
4. In **Add to dashboard**, select **New** to create a dashboard, or **Existing** to choose one from the list.
5. Select **Save and go to dashboard**.

:::{note}
:applies_to: stack: ga 9.0-9.2
In these versions, if your {{esql}} query defines [variable controls](try-esql.md#add-variable-control), they aren't added to the dashboard when using this method. To preserve them, use the [Import a Discover query along with its controls into a dashboard](try-esql.md#import-discover-query-with-controls) workflow instead.
:::

#### In classic mode [add-discover-visualization-classic]

In classic mode there's no direct save button next to the chart. Instead, you open the chart in **Lens**, edit it as needed, and save from there.

The {icon}`app_lens` **Edit visualization** button only appears when the {{data-source}} you're querying is time-based and its time field can be visualized. If those conditions aren't met, the chart isn't shown and the button isn't available.

1. In Discover, run a query that produces a chart.
2. Next to the chart, select {icon}`app_lens` **Edit visualization**. The chart opens in **Lens**, prefilled with your current query and time range.
3. In Lens, adjust the visualization as needed.
4. Select **Save** in the Lens application menu.
5. Enter a **Title** for the panel, and optionally a **Description**.
6. In **Add to dashboard**, select **New** to create a dashboard, or **Existing** to choose one from the list.
7. Select **Save and go to dashboard**.

### Add the Discover table to a dashboard [save-table-to-dashboard]
```{applies_to}
stack: ga 9.4
serverless: ga
```

Save the current view of the documents table to a new or existing dashboard without first saving the Discover session to the library. The resulting panel stores its configuration with the dashboard, so later changes to the Discover session don't affect the panel.

To use this option, you need permission to view and create dashboards. The button isn't available when Discover is opened from another application, such as when editing a session panel from a dashboard.

1. In the documents table toolbar, select {icon}`app_dashboard` **Save table to dashboard**.
2. Enter a title for the panel, and optionally a description.
3. In **Add to dashboard**, select **New** to create a dashboard, or **Existing** to choose one from the list.
4. Select **Save and go to dashboard**.

### Add an entire Discover session to a dashboard [add-full-discover-session-to-dashboard]

A full Discover session panel retains the session's tabs, columns, sort order, and other settings, and can display a single tab as a data table. If the session has multiple tabs, you can [choose which tab the panel displays](#discover-session-choose-tab).

There are several ways to add a full session as a panel:

- [Add a saved session from the dashboard library](#add-discover-session-from-library)
- {applies_to}`stack: ga 9.4` {applies_to}`serverless: ga` [Create a **Discover session** panel from the dashboard's **Add** menu](#add-ad-hoc-discover-session-panel)
- {applies_to}`stack: ga 9.5` {applies_to}`serverless: ga` [Save the session from Discover with a relevant **Add to dashboard** option selected](#save-discover-session-with-add-to-dashboard)
- {applies_to}`stack: ga 9.4` {applies_to}`serverless: ga` [Save Discover panel edits initiated from a dashboard as a new session](#discover-session-save-as-from-dashboard)

#### Add a saved session from the dashboard library [add-discover-session-from-library]

Use this method to add a session that's already saved to the library.

1. Save the Discover session following the steps in [Save a Discover session](#_save_a_discover_session).
2. Go to **Dashboards**.
3. Open or create the dashboard, then switch to **Edit** mode if necessary.
4. Depending on the version you're using, select **Add from library**, or **Add** > **From library**.
5. From the **Types** dropdown, select **Discover session**.
6. Select the Discover session that you want to add, then select **X** to close the list.

#### Create a Discover session from the dashboard [add-ad-hoc-discover-session-panel]
```{applies_to}
stack: ga 9.4
serverless: ga
```

Create a single-tab Discover session directly on a dashboard, without first saving it to the library. The session is stored with the dashboard and isn't saved to the library.

To use this option, you need permission to access Discover, and the dashboard must be in **Edit** mode.

1. On the dashboard, select **Add panel** > **New panel**.
2. In the **Visualizations** group, select {icon}`app_discover` **Discover session**. Discover opens in embedded editor mode.
3. Configure the session: enter a query, adjust columns, sort, and other view settings as needed.
4. Select **Save and return** in the application menu to add the configured panel to the dashboard.

#### Add a session to a dashboard when saving it from Discover [save-discover-session-with-add-to-dashboard]
```{applies_to}
stack: ga 9.5
serverless: ga
```

You can add a Discover session directly to a dashboard when saving it for the first time, as described in [](#_save_a_discover_session).

#### Save panel edits as a new Discover session [discover-session-save-as-from-dashboard]
```{applies_to}
stack: ga 9.4
serverless: ga
```

When editing a Discover session panel from a dashboard, you can save your changes as a new Discover session, instead of updating the panel in place. This works whether the panel was added from the library or created directly on the dashboard.

1. On the dashboard, hover over the panel and select {icon}`pencil` **Edit Discover session configuration**. Discover opens in embedded editor mode.
2. Make your changes in **Discover**.
3. In the application menu, open the menu next to **Save and return** and select **Save as**.
4. In the **Save Discover session** modal, enter a **Title** for the new session, and optionally a **Description** and [**Tags**](../find-and-organize/tags.md).
5. In **Add to dashboard**, choose where to display the new session:

   - **Existing**: Add the new session to a dashboard you select.

     - If you select the dashboard the panel came from, the original panel is updated in place to reference the new session, in the same position. If the replaced panel was linked to the library, you can still find it unchanged in the library. If the panel wasn't linked to the library, it is lost and replaced by the newly saved session.
     - If you select a different dashboard, the original panel is unchanged, and the new session is added as a separate panel on the dashboard you selected.

   - **New**: Save the session and add it as a panel on a new dashboard. The original panel is unchanged.
   - **None**: Save the session to the library only, without adding it to a dashboard. The original panel is unchanged.

6. Select **Save and add to library** (when **None** is selected) or **Save and go to dashboard** (when **Existing** or **New** is selected).

After saving, you go to the new session in **Discover** when you selected **None**, or to the corresponding dashboard when you selected **Existing** or **New**.

#### Choose which tab a session panel displays [discover-session-choose-tab]
```{applies_to}
stack: ga 9.4
serverless: ga
```

A Discover session panel displays one tab at a time. When the underlying session has multiple tabs, you can change which tab the panel shows.

1. On the dashboard, open the panel menu and select **Edit**.
2. From the tab selector, select the tab you want to display.

   :::{image} /explore-analyze/images/discover-session-tab-selector.png
   :alt: Tab selector showing the list of available tabs for a Discover session panel
   :width: 50%
   :screenshot:
   :::

3. Select **Apply**.
