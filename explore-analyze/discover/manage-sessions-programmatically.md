---
navigation_title: Manage programmatically
description: Create and manage Discover sessions from code with the Discover sessions API, and see how it works with the Dashboards API and the data views APIs.
applies_to:
  serverless: ga
  stack: ga 9.6+
products:
  - id: kibana
type: overview
---

# Manage Discover sessions programmatically [manage-discover-sessions-programmatically]

If you keep your {{kib}} content in version control or deploy it from a pipeline, you can create and manage Discover sessions from code instead of saving each one by hand in **Discover**. The Discover sessions API covers the sessions themselves. Two other APIs cover what sessions connect to: the Dashboards API, to show a session on a dashboard, and the data views APIs, for the saved data views that a session tab can refer to.

| API | When to use it | What you get |
|---|---|---|
| [Discover sessions API](#discover-sessions-api) | Keeping sessions in version control and deploying them from CI/CD | Saved Discover session |
| [Dashboards API](#sessions-on-dashboards) | Showing a session on a dashboard that you also manage as code | Dashboard with a Discover session panel |
| [Data views v2 API](#sessions-and-data-views) | Creating a saved data view that a session tab can refer to | Data view |

## Discover sessions API [discover-sessions-api]

The Discover sessions API, available at `/api/discover_sessions`, lets you create, read, search, update, and delete saved Discover sessions outside the {{kib}} UI. You describe a session as JSON: a title and one or more tabs, each with its own data source, query, filters, and table and chart settings. You can then store session definitions in version control and deploy them through automated pipelines.

Use the Discover sessions API when you need to:

- Deploy the same sessions to several spaces or environments from a CI/CD pipeline
- Track session definitions in version control, next to the rest of your configuration
- Create or update sessions from your own tooling

A `PUT` request with an ID that you provide creates the session if it doesn't exist and fully replaces it if it does, so you can run the same request in every environment.

To get a definition to start from, [export a session as JSON](export-discover-session.md#export-discover-session-json). If you have access to **Dev Tools**, **Open in Console** opens {{kib}} Dev Tools with a request that creates the session from that JSON.

Refer to the [Discover sessions API reference]({{kib-apis}}group/endpoint-discover-sessions) for the request schema, tab types, and authentication requirements.

## Show a session on a dashboard [sessions-on-dashboards]

A dashboard that you manage with the [Dashboards API](../dashboards/create-dashboards-programmatically.md#dashboards-api) can include Discover sessions. Add a `discover_session` panel to the dashboard definition and set it up in one of two ways:

- **Link a saved session:** Set `ref_id` to the ID of a saved session. The panel shows the first tab of the session, or the tab that you set in `selected_tab_id`. You can also override table settings, such as column order or row height, for this panel only.
- **Define the tab in the panel:** Describe the tab inside the dashboard definition. The tab is stored with the dashboard and doesn't create a saved session, so the dashboard stays self-contained.

Linking suits a session that several dashboards share, because a change to the session shows on every panel that links it.

For the panel schema, refer to the [Dashboards API reference](https://elastic.github.io/dashboards-api-spec/dashboards#tag/Dashboards). To add a session to a dashboard from the UI, refer to [Use Discover sessions in dashboards](use-sessions-in-dashboards.md).

## Use data views in sessions [sessions-and-data-views]

Each tab in a session gets its data in one of three ways, which you set with `data_source.type`:

- `esql`: The tab runs an {{esql}} query and doesn't use a data view.
- `data_view_reference`: The tab uses an existing data view, which you reference by its ID.
- `data_view_spec`: The tab defines its own data view inline, with an index pattern and, optionally, a time field.

{{esql}} tabs and tabs with an inline data view don't depend on anything else in the target environment. A tab that references a data view only works there if a data view with the same ID exists.

Create data views before the sessions that reference them. To create data views with the IDs that your sessions reference, use the [Data views v2 API]({{kib-apis}}group/endpoint-data-views-v2). A `PUT` request creates the data view with the ID in the path, or replaces its definition if it exists. The earlier [Data views API]({{kib-apis}}group/endpoint-data-views) remains available for partial updates and for managing individual fields.

For more on keeping references consistent between environments, refer to [Manage data views from code](../find-and-organize/data-views.md#data-views-from-code) and [Keep references portable across environments](../dashboards/manage-dashboards-as-code.md#dashboards-as-code-portability).

## Next steps

- [Create dashboards programmatically](../dashboards/create-dashboards-programmatically.md): Build the dashboards that show your sessions.

## Related pages

- [Save and manage Discover sessions](save-open-search.md)
- [Use Discover sessions in dashboards](use-sessions-in-dashboards.md)
- [Manage dashboards as code](../dashboards/manage-dashboards-as-code.md)
- [{{kib}} data views](../find-and-organize/data-views.md)
