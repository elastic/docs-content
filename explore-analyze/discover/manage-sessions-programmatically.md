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

If you keep your {{kib}} content in version control or deploy it from a pipeline, you can create and manage Discover sessions from code instead of saving each one by hand in **Discover**. The Discover sessions API covers the sessions themselves. The Dashboards API and the data views APIs cover what sessions connect to: the dashboards that show a session, and the saved data views that a session tab can use as its data source.

| API | When to use it | What you get |
|---|---|---|
| [Discover sessions API](#discover-sessions-api) | Keeping sessions in version control and deploying them from CI/CD | Saved Discover session |
| [Dashboards API](#sessions-on-dashboards) | Showing a session on a dashboard that you also manage as code | Dashboard with a Discover session panel |
| [Data views v2 API](#sessions-and-data-views) | Creating a saved data view that a session tab can use as its data source | Data view |

## Discover sessions API [discover-sessions-api]

To get a definition to start from, [export a session as JSON](export-discover-session.md#export-discover-session-json). If you have access to **Dev Tools**, **Open in Console** opens {{kib}} Dev Tools with a request that creates the session from that JSON.

Refer to the [Discover sessions API reference]({{kib-apis}}group/endpoint-discover-sessions) for the request schema, the data sources that a tab can use, authentication, spaces, and an example request that you can run as is.

## Show a session on a dashboard [sessions-on-dashboards]

A dashboard that you manage with the [Dashboards API](../dashboards/create-dashboards-programmatically.md#dashboards-api) can include Discover sessions. Add a `discover_session` panel to the dashboard definition and set it up in one of two ways:

- **Link a saved session:** Set `ref_id` to the ID of a saved session. Several dashboards can then share the session, and a change to the session shows on every panel that links it.
- **Define the tab in the panel:** Describe the tab inside the dashboard definition. The tab is stored with the dashboard and doesn't create a saved session, so the dashboard stays self-contained.

For the other panel options, such as choosing which tab a linked session shows, refer to the [Dashboards API reference](https://elastic.github.io/dashboards-api-spec/dashboards#tag/Dashboards). To add a session to a dashboard without writing API requests, refer to [Use Discover sessions in dashboards](use-sessions-in-dashboards.md).

## Use data views in sessions [sessions-and-data-views]

A tab that references a saved data view by ID only works in an environment where a data view with that ID exists. {{esql}} tabs and tabs that define their data view inline don't depend on anything else in the target environment.

Create the data views before the sessions that reference them, with the [Data views v2 API]({{kib-apis}}group/endpoint-data-views-v2). For more on keeping references consistent between environments, refer to [Manage data views from code](../find-and-organize/data-views.md#data-views-from-code) and [Keep references portable across environments](../dashboards/manage-dashboards-as-code.md#dashboards-as-code-portability).

## Next steps

- [Create dashboards programmatically](../dashboards/create-dashboards-programmatically.md): Build the dashboards that show your sessions.

## Related pages

- [Save and manage Discover sessions](save-open-search.md)
- [Use Discover sessions in dashboards](use-sessions-in-dashboards.md)
- [Manage dashboards as code](../dashboards/manage-dashboards-as-code.md)
- [{{kib}} data views](../find-and-organize/data-views.md)
