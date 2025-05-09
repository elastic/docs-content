---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/search-sessions.html
---

# Run a search session in the background [search-sessions]

::::{admonition} Deprecated and disabled by default
Search Sessions are deprecated. They are disabled by default and will be removed in a future version. You can enable search sessions again by setting [`data.search.sessions.enabled`](kibana://reference/configuration-reference/search-sessions-settings.md) to `true` in the [`kibana.yml`](/deploy-manage/stack-settings.md) configuration file.
::::


Sometimes you might need to search through large amounts of data, no matter how long the search takes. Consider a threat hunting scenario, where you need to search through years of data. You can save a long-running search, so {{kib}} processes your request in the background, and you can continue your work.

Save your search session from **Discover** or **Dashboard**, and when your session is complete, view and manage it in **Stack Management**. Search sessions are [enabled by default](kibana://reference/configuration-reference/search-sessions-settings.md).

:::{image} /explore-analyze/images/kibana-search-session.png
:alt: Search Session indicator displaying the current state of the search
:screenshot:
:::


## Requirements [_requirements]

* To save a session, you must have permissions for **Discover** and **Dashboard**, and the [search sessions subfeature](../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#kibana-feature-privileges).
* To view and restore a saved session, you must have access to **Stack Management**.


## Example: Save a search session [_example_save_a_search_session]

You’re trying to understand a trend you see on a dashboard. You need to look at several years of data, currently in [cold storage](../../manage-data/lifecycle/data-tiers.md#cold-tier), but you don’t have time to wait. You want {{kib}} to continue working in the background, so tomorrow you can open your browser and pick up where you left off.

1. Load your dashboard.
   Your search session begins automatically. The icon after the dashboard title displays the current state of the search session. A clock icon indicates the search session is in progress. A checkmark indicates that the search session is complete.

2. To continue a search in the background, click the clock icon, and then click **Save session**.

   ![Search Session indicator displaying the current state of the search](/explore-analyze/images/kibana-search-session-awhile.png "title =50%")
   
   Once you save a search session, you can start a new search, navigate to a different application, or close the browser.

3. To view your saved search sessions, go to the **Search Sessions** management page using the navigation menu or the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md). For a saved or completed session, you can also open this view from the search sessions popup.
   ![Search Sessions management view with actions for inspecting](/explore-analyze/images/kibana-search-sessions-menu.png "")

4. Use the edit menu in **Search Sessions** to:

    * **Inspect** the queries and filters that makeup the session.
    * **Edit the name** of a session.
    * **Extend** the expiration of a completed session.
    * **Delete** a session.

5. To restore a search session, click its name in the **Search Sessions** view.

    You’re returned to the place from where you started the search session. The data is the same, but behaves differently:

    * Relative dates are converted to absolute dates.
    * Panning and zooming is disabled for maps.
    * Changing a filter, query, or drilldown starts a new search session, which can be slow.



## Limitations [_limitations]

Some visualization features do not fully support background search sessions. When you restore a dashboard, panels with unsupported features won’t load immediately, but instead send out additional data requests, which can take a while to complete. The **Your search session is still running** warning appears. You can either wait for these additional requests to complete or come back to the dashboard later when all data requests have finished.

A panel on a dashboard can behave like this if one of the following features is used:

**Lens**

* A **top values** dimension with an enabled **Group other values as "Other"** setting. This is configurable in the **Advanced** section of the dimension.
* An **intervals** dimension.

**Aggregation-based** visualizations

* A **terms** aggregation with an enabled **Group other values in separate bucket** setting.
* A **histogram** aggregation.

**Maps**

* Layers using joins, blended layers, or tracks layers.
