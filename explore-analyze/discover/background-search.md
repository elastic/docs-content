---
navigation_title: "Run queries in the background"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/search-sessions.html
applies_to:
  stack: preview 9.2
  serverless: unavailable
products:
  - id: kibana
description: Send long-running queries to run in the background with background searches from Discover and Dashboards. Continue working while queries complete and access results later.
---

# Run Discover and Dashboards queries in the background [background-search]

Send long-running searches to run asynchronously while you continue working in {{product.kibana}}. Access your completed searches later from **Discover** or **Dashboards**, and manage all background searches from the toolbar.

::::{important} - Background search replaces Search sessions

Background search is a feature introduced in version 9.2. It replaces the deprecated **Search sessions** feature.
If you have been using search sessions and upgrade to 9.2, your search sessions aren't lost and become background searches.
::::

## Requirements [background-search-requirements]

To use background searches, you need:

* **Read** permissions for the **Discover** or **Dashboard** features in {{product.kibana}}
* A {{data-source}} configured with data in {{product.elasticsearch}}

![Send search to background](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/bltee31dcf0d3917c75/68ecf412e5bae49d65a286ff/background-search.gif " =75%")


## Enable background searches

This feature is disabled by default. You can enable background searches in versions 9.2 and later, or search sessions in versions 9.1 and earlier, by setting [`data.search.sessions.enabled`](kibana://reference/configuration-reference/search-sessions-settings.md) to `true` in the [`kibana.yml`](/deploy-manage/stack-settings.md) configuration file.

:::{note} - Exception for search sessions users
If you upgrade to version 9.2 or later with search sessions enabled in the version you upgrade from, background searches are automatically enabled.
:::

## Usage requirements [_requirements]

The background searches that you run are personal and only visible by you. To use this feature, you must have the following minimum permissions:

:::::{tab-set}
:group: background search

::::{tab-item} 9.2 and later
:sync: 92
To send searches to the background, and to view and interact with the list of background searches from **Discover** and **Dashboards** apps, you must have permissions for **Discover** and **Dashboard**, and for the [Background search subfeature](../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#kibana-feature-privileges).
::::

::::{tab-item} 9.1 and earlier
:sync: 91
In versions 9.1 and earlier, this feature is named **Search sessions**.
* To save a session, you must have permissions for **Discover** and **Dashboard**, and the [Search sessions subfeature](../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#kibana-feature-privileges).
* To view and restore a saved session, you must have access to {{stack-manage-app}}.
::::

:::::

## Send a search to the background

You can send a search to the background only after it starts running. Until then, the **Send to background** button is disabled.

1. Write or edit the query.

1. Select {icon}`play` **Run** (or {icon}`refresh` **Refresh** if you already ran the query at least once) to start executing the query. At this point, the {icon}`background_task` **Send to background** button becomes available.

1. Select {icon}`background_task` **Send to background**. The search is sent to the background and added to the queue of background searches.

You can resume your other tasks, for example start a new search, navigate to a different application, or close the browser. Once the search has completed, a notification informs you and lets you access the search to view its results.

Background searches expire after 7 days. Beyond that period, you must run the search again. You can change this default value by editing the [`data.search.sessions.defaultExpiration`](kibana://reference/configuration-reference/search-sessions-settings.md) setting.

## Reopen or manage background searches

From the list of background searches, you can reopen and edit any searches, but also extend their validity period or delete them to keep only searches that you care about.

1. Open your list of background searches using one of the following methods:
   - Once a background search is sent to the background, a notification appears to inform you, with a link to open the list of background searches.
   - If you miss the notification or need to access this list at any time, go to **Discover** or **Dashboards** and select the {icon}`background_task` **Background searches** button in the toolbar. This option is only available from version 9.2.

     :::{tip}
     From **Discover**, you can only view Discover background searches. And from **Dashboards**, you can only see Dashboards background searches.
     :::
   - Open the **Background Search** management page in {{kib}}.

1. Find the background search that you want to interact with using the search or status filter options.
   - To open it to view its results and continue your explorations, select its name. Relative dates are converted to absolute dates.
   - To rename it, select the {icon}`boxes_horizontal` **More actions** button, then select {icon}`pencil` **Edit name**. By default, background searches get default names that indicate their execution date and time.
   - To extend its current expiration date by another 7 days, select the {icon}`boxes_horizontal` More actions button, then select **Extend**.
   - To delete it, select the {icon}`boxes_horizontal` More actions button, then select {icon}`trash` **Delete**.


## Background search limitations in dashboards [_limitations]

Some visualization features do not fully support background searches. When you restore a dashboard, panels with unsupported features won’t load immediately, but instead send out additional data requests, which can take a while to complete. The **Your background search is still running** warning appears. You can either wait for these additional requests to complete or come back to the dashboard later when all data requests have finished.

A panel on a dashboard can behave like this if one of the following features is used:

**Lens**

* A **top values** dimension with an enabled **Group other values as "Other"** setting. This is configurable in the **Advanced** section of the dimension.
* An **intervals** dimension.

**Aggregation-based** visualizations

* A **terms** aggregation with an enabled **Group other values in separate bucket** setting.
* A **histogram** aggregation.

**Maps**

* Layers using joins, blended layers, or tracks layers.