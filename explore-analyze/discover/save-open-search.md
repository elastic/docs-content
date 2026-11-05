---
navigation_title: Save and manage sessions
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/save-open-search.html
applies_to:
  stack: ga
  serverless: ga
type: how-to
products:
  - id: kibana
description: Save a Discover session to reuse its queries, filters, and view, then reopen, find, and duplicate it.
---

# Save and manage Discover sessions [save-open-search]

When an exploration is worth coming back to, save it as a Discover session. A saved session preserves your queries, filters, column selections, and view configurations, so you can reopen it later, share it, add it to dashboards, or use it as a foundation for building visualizations.

## Requirements [save-search-requirements]

To save searches, you need **Create** and **Edit** permissions for the {{saved-objects-app}} feature in {{product.kibana}}. If you don't have these permissions, the **Save** button won't be visible. For more information, refer to [Read-only access](#discover-read-only-access).


### Read-only access [discover-read-only-access]

If you don’t have sufficient privileges to save Discover sessions, the following indicator is displayed and the **Save** button is not visible. For more information, refer to [Granting access to {{kib}}](elasticsearch://reference/elasticsearch/roles.md).

:::{image} /explore-analyze/images/kibana-read-only-badge.png
:alt: Example of Discover's read only access indicator in the {{product.kibana}} header
:screenshot:
:::

## Save a Discover session [_save_a_discover_session]

1. Once you’ve created a view worth saving, select **Save** in the application menu. A dialog with several options opens:
    1. Enter a **Title** for the session, and optionally a **Description** and [**Tags**](../find-and-organize/tags.md).
    2. If the session is time-based, turn on **Store time with Discover session** to save the current time filter and refresh interval with it.
    3. {applies_to}`stack: ga 9.5` {applies_to}`serverless: ga` In **Add to dashboard**, choose whether to also add the session as a panel on a dashboard. Select **New** to create a dashboard, **Existing** to choose one, or **None** to skip. The session is saved to the library in all cases.
2. Select **Save**.
3. To reload your results later, refer to [Open a saved Discover session](#open-discover-session).

A Discover session stores the following elements for each of its tabs:

- The query mode ({{esql}} or Classic)
- The query text and filters
- The {{data-source}}
- If you turned on **Store time with Discover session**, the selected time filter and refresh interval
- The current view of **Discover**, including the document table layout, the chart, and any {{esql}} [variable controls](esql-variable-controls.md)
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` The **JSON** view of the document table, including how each tree is displayed. Refer to [View documents as JSON](document-explorer.md#document-explorer-view-mode).
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.6+` The {icon}`bolt` **Fast mode** setting in {{esql}} mode. Refer to [Use Fast mode](/explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-fast-mode-toggle).

## Open a saved Discover session [open-discover-session]

To go back to a session you saved, or to find one that a teammate saved, open it from **Discover**.

1. In the application menu, select **Open session**. The **Open Discover session** flyout lists the saved sessions.
2. To find a session, enter part of its title in the search box, filter the list by tag, or sort it by selecting a column header such as **Title**.
3. Select the session.

**Result:** The session opens in **Discover**. If it uses a different {{data-source}} than the one currently selected, **Discover** switches to it. The query language that the session used is also selected automatically.

To rename, delete, or otherwise manage your saved sessions, select **Manage Discover sessions** in the flyout. The button opens the [{{saved-objects-app}}](../find-and-organize/saved-objects.md) page, filtered to Discover sessions. It appears if you have access to that page.

## Duplicate a Discover session [_duplicate_a_discover_session]

To duplicate an existing Discover session as a new one, the workflow depends on the version you're using.

::::{applies-switch}

:::{applies-item} { stack: ga 9.4+, serverless: ga }
1. In **Discover**, open the Discover session that you want to duplicate.
2. In the application menu, from the menu next to **Save**, select **Save as**. The **Save Discover session** dialog opens.
3. Enter a **Title** for the new session, and optionally a **Description** and [**Tags**](../find-and-organize/tags.md).
4. {applies_to}`stack: ga 9.5` {applies_to}`serverless: ga` In **Add to dashboard**, choose whether to also add the session as a panel on a dashboard. Select **New** to create a dashboard, **Existing** to choose one, or **None** to skip. The session is saved to the library in all cases.
5. Select **Save**.
:::

:::{applies-item} { stack: ga 9.0-9.3 }
1. In **Discover**, open the Discover session that you want to duplicate.
2. In the application menu, select **Save**.
3. Enter a new name for the session.
4. Turn on **Save as new Discover session**.
5. Select **Save**.
:::

::::

## Related pages [save-open-search-related]

- [How Discover works](discover-get-started.md)
- [Export Discover session results](export-discover-session.md)
- [Use Discover sessions in dashboards](use-sessions-in-dashboards.md)
- [Query your data in Discover with {{esql}}](use-esql.md)
