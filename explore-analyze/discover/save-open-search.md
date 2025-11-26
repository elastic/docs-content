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


## Read-only access [discover-read-only-access]

If you don’t have sufficient privileges to save Discover sessions, the following indicator is displayed and the **Save** button is not visible. For more information, refer to [Granting access to {{kib}}](elasticsearch://reference/elasticsearch/roles.md).

:::{image} /explore-analyze/images/kibana-read-only-badge.png
:alt: Example of Discover's read only access indicator in the {{product.kibana}} header
:screenshot:
:::


## Save a Discover session [_save_a_discover_session]

By default, a Discover session stores the query text, filters, and current view of **Discover**, including the columns and sort order in the document table, and the {{data-source}}.

1. Once you’ve created a view worth saving, click **Save** in the toolbar.
2. Enter a name for the session.
3. Optionally store [tags](../find-and-organize/tags.md) and the time range with the session.
4. Click **Save**.
5. To reload your search results in **Discover**, click **Open** in the toolbar, and select the saved Discover session.

If the saved Discover session is associated with a different {{data-source}} than is currently selected, opening the saved Discover session changes the selected {{data-source}}. The query language used for the saved Discover session is also automatically selected.



## Duplicate a Discover session [_duplicate_a_discover_session]

1. In **Discover**, open the Discover session that you want to duplicate.
2. In the toolbar, click **Save**.
3. Give the session a new name.
4. Turn on **Save as new Discover session**.
5. Click **Save**.


## Add search results to a dashboard [_add_search_results_to_a_dashboard]

1. Go to **Dashboards**.
2. Open or create the dashboard, then click **Edit**.
3. Click **Add from library**.
4. From the **Types** dropdown, select **Discover session**.
5. Select the Discover session that you want to add, then click **X** to close the list.
