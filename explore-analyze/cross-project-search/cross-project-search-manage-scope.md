---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: cloud-serverless
  - id: kibana
navigation_title: "Manage CPS scope"
description: Learn how to manage cross-project search scope from your project apps using the scope selector, query-level overrides, and space defaults.
---

# Manage {{cps}} scope in your project apps [cps-manage-scope]

When [{{cps}}](/explore-analyze/cross-project-search.md) is enabled and projects are linked, you can control which linked projects are included in your searches. {{kib}} provides several ways to manage this scope, from a global selector in the header to query-level overrides.

## {{cps-cap}} scope selector [cps-in-kibana]

A **{{cps-cap}}** ({{cps-init}}) **scope selector** appears in the header of your project. It controls which linked projects your searches include.

With the {{cps-init}} scope selector, you can select:

* **This project**: Searches only the origin project.
* **All projects**: Searches the origin project and all linked projects.

:::{tip}
The scope selector also lists the aliases of all [linked projects](/explore-analyze/cross-project-search/cross-project-search-link-projects.md), which is useful when you need to reference them in queries or index patterns.
:::

The scope selector is not editable in every app. Some apps display it as read-only, and others show it as unavailable. Refer to [{{cps-cap}} availability by app](#cps-availability) for details.

When you change the scope during a session, your selection is preserved as you navigate between apps. Admins can configure a [default {{cps}} scope for each space](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope), which is used when you start a new session.

## Override {{cps}} scope at the query level [cps-query-overrides]

In apps where you write queries, you can define a different {{cps}} scope than the one set in the header's scope selector or the [space-level default](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope). This is useful when you want a specific query or dashboard panel to search a different set of projects.

There are two main mechanisms:

* **[Project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md)**: Use a `project_routing` parameter to limit which projects a query runs against. In {{esql}}, use [`SET project_routing`](/explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-cps) at the beginning of your query. Project routing is evaluated before query execution, so excluded projects are never queried.
* **[Qualified index expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions)**: Prefix an index name with a project alias to target a specific project, for example `my_project:logs-*`. Use `_origin:logs-*` to target only the current project. Qualified expressions work in index patterns and query source commands.

When a visualization panel uses a query-level override, it displays a **Custom CPS scope** badge on dashboards to indicate that it uses a different scope than the {{cps-init}} scope selector.

## {{cps-cap}} availability by app [cps-availability]

Not all apps support {{cps}}. The following table shows which apps support the {{cps-init}} scope selector and query-level overrides:

| App | {{cps-init}} scope selector | Query-level overrides |
| --- | --- | --- |
| **Discover** | Editable | {{esql}} [`SET project_routing`](/explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-cps) and [qualified expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions) in `FROM` |
| **Dashboards** | Editable | Per-panel overrides via {{esql}} or Maps layer routing. Dashboards can also [store a {{cps}} scope](/explore-analyze/dashboards/using.md#dashboard-cps-scope). |
| **Lens** | Editable | {{esql}} [`SET project_routing`](/explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-cps) and [qualified expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions) in `FROM` |
| **Maps** | Editable | Layer-level [project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) for vector layers and joins |
| **Vega** | Editable | Project routing in Vega specs |
| **{{rules-ui}} and alerts** | Read-only | {{esql}} rules support [`SET project_routing`](/explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-cps). Other rules use the [space-level {{cps}} scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope). |

The header's {{cps-init}} scope selector is not available in other apps, including Transforms, {{ml-app}}, Canvas, and object listing pages.
