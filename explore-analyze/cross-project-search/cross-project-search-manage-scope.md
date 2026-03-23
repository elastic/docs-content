---
applies_to:
  stack: unavailable
  serverless: preview
type: overview
products:
  - id: cloud-serverless
  - id: kibana
navigation_title: "Manage CPS scope"
description: Learn how to manage cross-project search scope from your project apps using the scope selector, query-level overrides, and space defaults.
---

# Managing {{cps}} scope in your project apps [cps-manage-scope]

When [{{cps}}](/explore-analyze/cross-project-search.md) is enabled and projects are linked, searches run across all linked projects by default. {{kib}} provides several ways to narrow or change this scope:

* **Space default**: Admins [configure a default scope per space](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope), which applies when you start a new session.
* **Session scope**: Use the header's scope selector to change which projects are searched during your session.
* **Query-level override**: Use project routing or qualified index expressions in individual queries to target specific projects.

## {{cps-cap}} scope selector [cps-in-kibana]

A **{{cps-cap}}** ({{cps-init}}) **scope selector** appears in the header of your project. It controls which linked projects your searches include.

With the {{cps-init}} scope selector, you can select:

* **This project**: Searches only the origin project.
* **All projects**: Searches the origin project and all linked projects.

:::{tip}
The scope selector also lists the aliases of all [linked projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md), which is useful when you need to reference them in queries or index patterns.
:::

The scope selector is not editable in every app. Some apps display it as **read-only**, meaning the app uses the space default scope but you cannot change it. Other apps show it as **unavailable**, meaning the app searches only the local project. Refer to [{{cps-cap}} availability by app](#cps-availability) for details.

When you change the scope during a session, your selection is preserved as you navigate between apps. Admins can configure a [default {{cps}} scope for each space](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope), which is used when you start a new session.

## Override {{cps}} scope at the query level [cps-query-overrides]

In apps where you write queries, you can define a different {{cps}} scope than the one set in the header's scope selector or the [space-level default](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope). This is useful when you want a specific query or dashboard panel to search a different set of projects.

There are two main mechanisms:

* **[Project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md)**: Use a `project_routing` parameter to limit which projects a query runs against. In {{esql}}, use [`SET project_routing`](/explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-cps) at the beginning of your query. Project routing is evaluated before query execution, so excluded projects are never queried.
* **[Qualified index expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions)**: Prefix an index name with a project alias to target a specific project, for example `my_project:logs-*`. Qualified expressions work in index patterns and query source commands.

For example, to search only a specific linked project from Discover, start your {{esql}} query with:

```esql
SET project_routing="_alias:my-project";
FROM logs-*
| LIMIT 100
```

## {{cps-cap}} availability by app [cps-availability]

Not all apps support {{cps}}. The following table shows which apps support the {{cps-init}} scope selector and query-level overrides. Any app with an ES\|QL editor supports [`SET project_routing`](/explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-cps) and [qualified index expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions) in `FROM` commands.

| App | {{cps-init}} scope selector | Query-level overrides |
| --- | --- | --- |
| **Discover** | Editable | ES\|QL |
| **Dashboards** | Editable | Per-panel overrides using ES\|QL visualizations or Maps layer routing. Dashboards can also [store a {{cps}} scope](/explore-analyze/dashboards/using.md#dashboard-cps-scope). |
| **Lens visualizations** | Editable | ES\|QL visualizations [^cps-badge] |
| **Maps** | Editable | Layer-level [project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) for vector layers and joins |
| **Vega** | Editable | Project routing in Vega specs |
| **{{rules-ui}} and alerts** | Read-only | ES\|QL rules support `SET project_routing`. For non-{{esql}} rules that use index patterns, you can use [qualified index expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions) to scope the rule to specific projects.|
| **Dev Tools / Console** | Not available | Full CPS through raw API requests, including ES\|QL |
| **{{ml-app}} Data Visualizer** | Not available | ES\|QL |
| **Streams** | Not available | ES\|QL |
| **Agent Builder** | Not available | ES\|QL |

The header's {{cps-init}} scope selector is not available in other apps, including Transforms, Canvas, and object listing pages.

[^cps-badge]: When a visualization panel uses a query-level override, it displays a **Custom CPS scope** badge on dashboards to indicate that it uses a different scope than the {{cps-init}} scope selector.

## Related pages

* [{{cps-cap}} overview](/explore-analyze/cross-project-search.md)
* [Project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md)
* [How search works in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-search.md)
* [Configure {{cps}} access and scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md)
* [ES\|QL in {{kib}}](/explore-analyze/query-filter/languages/esql-kibana.md)
* [Query across Serverless projects with ES\|QL](elasticsearch://reference/query-languages/esql/esql-cross-serverless-projects.md)
