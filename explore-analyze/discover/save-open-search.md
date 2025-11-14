---
navigation_title: Save a search for reuse
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/save-open-search.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Preserve exploration work with saved Discover sessions that store queries, filters, column selections, and data views. Reuse explorations, share with teams, or add to dashboards.
---

# Save and reuse Discover searches [save-open-search]

After configuring a search with specific queries, filters, and column selections, you can save your work as a Discover session. This lets you reopen the exact view later, share it with team members, or add the results to a dashboard. Saved sessions preserve all aspects of your exploration for future use.

**Technical summary**: Click **Save** in the toolbar, name your session, and optionally store time range and tags. Saved sessions preserve query text, filters, selected {{data-source}}, columns, sort order, and document table configuration.

**Prerequisites:**

* You need privileges to save Discover sessions (refer to [Granting access to {{product.kibana}}](elasticsearch://reference/elasticsearch/roles.md))
* If a read-only indicator appears, you can view but not save sessions

## Read-only access [discover-read-only-access]

If you don't have sufficient privileges to save Discover sessions, the following indicator is displayed and the **Save** button is not visible.

:::{image} /explore-analyze/images/kibana-read-only-badge.png
:alt: Example of Discover's read only access indicator in Kibana's header
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
