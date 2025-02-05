---
navigation_title: Save a search for reuse
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/save-open-search.html
---

# Discover sessions: Save a search for reuse [save-open-search]

A saved Discover session is a convenient way to reuse a search that you’ve created in **Discover**. Discover sessions are good for saving a configured view of Discover to use later or adding search results to a dashboard, and can also serve as a foundation for building visualizations.


## Read-only access [discover-read-only-access]

If you don’t have sufficient privileges to save Discover sessions, the following indicator is displayed and the **Save** button is not visible. For more information, refer to [Granting access to {{kib}}](../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md).

:::{image} ../../images/kibana-read-only-badge.png
:alt: Example of Discover's read only access indicator in Kibana's header
:class: screenshot
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
