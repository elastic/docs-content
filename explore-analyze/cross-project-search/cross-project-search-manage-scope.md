---
applies_to:
  stack: unavailable
  serverless: preview
type: overview
products:
  - id: cloud-serverless
  - id: kibana
navigation_title: "CPS scope in project apps"
description: Learn how to manage cross-project search scope from your project apps using the scope selector, tag filters, query-level overrides, and space defaults.
---

# Managing {{cps}} scope in your project apps

When [{{cps}} ({{cps-init}})](/explore-analyze/cross-project-search.md) is enabled and projects are linked, searches initiated from your project's apps run across all linked projects by default. {{kib}} provides several ways to narrow or change this scope:

* **Space default**: Admins [configure a default scope for each space](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope), which applies when you start a new session.
* **Session scope**: Use the [{{cps-init}} scope selector](#cps-in-kibana) in the project's header to change which projects are searched during your session.
* **Stored scope**: Some features use the [scope selector](#cps-in-kibana) to set a project routing value that is saved with a specific resource, such as a dashboard. The stored scope applies every time that resource runs or opens, independent of the session scope.
* **Query-level override**: Use project routing or qualified index expressions in individual queries to target specific projects.

## {{cps-cap}} scope selector [cps-in-kibana]

The **{{cps-cap}} ({{cps-init}}) scope** selector ({icon}`cross_project_search`) lets you choose which linked projects to include. It appears in the project header, or on the resource you are creating or editing.

The scope selector lists all linked projects, narrowed by any active [tag filters](#cps-picker-tag-filters). The origin project always appears first, labeled **This project**. Each project row shows the project name, project type icon, and any assigned [tags](/explore-analyze/cross-project-search/cross-project-search-tags.md).

From the scope selector, you can:

* [Toggle individual projects on or off](#cps-picker-include-exclude) to include or exclude them from searches.
* [Filter the project list by tags](#cps-picker-tag-filters) to find and select projects based on metadata or custom tags.

The footer displays the count of included and excluded projects.

The scope selector is not editable in every app. Some apps display it as **read-only**, meaning the app uses the space default scope but you cannot change it. In read-only mode, filter badges are visible but you cannot create, edit, or remove filters. Other apps show it as **unavailable**, meaning the app searches only the current project. Refer to [{{cps-cap}} availability by app](#cps-availability) for details.

When the current selection matches the [space default](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope), the scope selector displays a **Using space defaults** indicator. When you change the selection, the indicator disappears. To restore the space default at any time, select **Revert to space defaults** in the scope selector. Changes you make in the project header or on a resource do not change the space default.

The scope selector also provides shortcuts to admin settings. Select **Adjust space defaults** to open the space's {{cps-init}} scope configuration, or **Manage cross-project search** to open the [{{cps-init}} management page](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md).

### Session scope vs. stored scope

Sometimes, you might want to change which projects are included in your results as you work. Other times, you want to set the project scope and persist it with a resource to keep inputs consistent. Session scope and stored scope are how apps make that happen. The behavior follows the app.

Most apps use **session scope**. Session scope is which projects are searched while you work. You set it with the scope selector in the project header. Your selection is preserved as you navigate between apps that support the selector. Starting a new session resets to the space default. Session scope is used by most apps.

Some apps use **stored scope**. Stored scope is saved with a resource and applies every time that resource runs or opens. Some apps, such as [Dashboards](/explore-analyze/dashboards.md), save a snapshot of the scope currently set in the header selector.

In apps where you write queries, you can still [override that scope at the query level](#cps-query-overrides).

Refer to the [availability table](#cps-availability) for how each app uses scope.

### Include and exclude projects [cps-picker-include-exclude]

Each project row has a toggle switch that includes or excludes it from searches. You can also use the context menu on any project row for quick actions:

* **Include only this project**: Excludes all other projects currently shown in the list.
* **Exclude only this project**: Includes all other projects currently shown in the list except this one.

You can also select all projects currently shown in the list by clicking **Include all visible**.

The scope selector prevents you from excluding every project. The toggle on the last included project is deactivated, so at least one project is always included.

If your current selection results in zero included projects, the scope selector displays a warning.

### Filter projects by tag [cps-picker-tag-filters]

You can narrow the project list in the scope selector by creating tag filters. Tag filters let you find and select projects based on [predefined and custom project tags](/explore-analyze/cross-project-search/cross-project-search-tags.md). Predefined tags include `_type`, `_region`, and `_csp`. You can also filter on [custom tags](/deploy-manage/deploy/elastic-cloud/project-settings.md#project-tags) that you define in the {{ecloud}} UI.

:::{note}
When you use a filter by custom tags, [changing the custom tags](/deploy-manage/deploy/elastic-cloud/project-settings.md#project-tags) on a project can include or exclude that project from your selected scope without the scope being edited.
:::

To add a tag filter:

1. Open the scope selector and select **Add project tag filter**.
2. Choose a tag from the **Select a tag** dropdown.
3. Choose an operator. The default operator is **is**.
4. If the operator requires a value, choose one or more values from the **Select a value** dropdown.
5. Select **Apply** ({icon}`check`) to add the filter.

When multiple filters are active, they are combined with AND logic: a project must match all filters to appear in the list.

#### Manage tag filters

Active filters appear as badges below the filter form. You can:

* Select a filter badge to edit its tag, operator, or value.
* Invert a filter to switch between include and exclude logic.
* Turn off a filter without removing it.
* Remove a filter to delete it.

To remove all active filters at once, select **Clear project tag filters** in the scope selector.

#### Quick-filter from project tags

You can create a filter directly from a project's tags. Select the tag count badge on a project row to open a popover listing that project's tags, then select a tag to create a filter for it.

### How newly linked projects affect your scope [cps-picker-new-projects]
How newly linked projects affect your scope depends on your app.

In most cases, your scope is saved as a [project routing expression](/explore-analyze/cross-project-search/cross-project-search-project-routing.md), not a fixed list, so it also applies to projects that are linked later:

* Projects that match your active tag filters are included automatically.
* Excluding a project individually affects only that project.

To keep future projects out of your scope, use a tag filter rather than excluding projects one by one.

## Override {{cps}} scope at the query level [cps-query-overrides]

In apps where you write queries, you can define a different {{cps}} scope than the one set in the header's scope selector or the [space-level default](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope). This is useful when you want a specific query or dashboard panel to search a different set of projects.

There are two main mechanisms:

* **[Project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md)**: Use a `project_routing` parameter to limit which projects a query runs against. In {{esql}}, use [`SET project_routing`](/explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-cps) at the beginning of your query. `SET project_routing` overrides the space default, the header selection, and any dashboard-stored scope for that query. Project routing is evaluated before query execution, so excluded projects are never queried.
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
| **Agent Builder** | Not available | ES\|QL |
| **Dashboards** | Editable | Per-panel overrides using ES\|QL visualizations or Maps layer routing. Dashboards can also [store a {{cps}} scope](/explore-analyze/dashboards/using.md#dashboard-cps-scope). Dashboard controls, such as **Options list** controls, suggest values from all projects in the selected {{cps-init}} scope. |
| **Dev Tools / Console** | Not available | Full {{cps-init}} through raw API requests, including ES\|QL. The [{{product.painless}} execute API](/explore-analyze/cross-project-search.md#cps-painless-scripting) resolves index names differently. |
| **Discover** | Editable | ES\|QL |
| **Lens visualizations** | Editable | ES\|QL visualizations[^cps-badge] |
| **Maps** | Editable | Layer-level [project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) for vector layers and joins |
| **{{ml-app}} AIOps Labs** | Editable | Not available |
| **{{ml-app}} {{data-viz}}** | Editable | ES\|QL |
| **{{rules-ui}} and alerts** | Read-only | ES\|QL rules support `SET project_routing`. For non-{{esql}} rules that use index patterns, you can use [qualified index expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions) to scope the rule to specific projects.|
| **Streams** | Not available | ES\|QL |
| **Vega** | Editable | Project routing in Vega specs |

The header's {{cps-init}} scope selector is not available in other apps, including Transforms, Canvas, and object listing pages.

[^cps-badge]: When a visualization panel uses a query-level override, it displays a **Custom CPS scope** badge on dashboards to indicate that it uses a different scope than the {{cps-init}} scope selector.

### {{cps-cap}} availability in Elastic {{observability}} apps [cps-availability-observability]

{{observability}} apps have limited {{cps-init}} support. The scope selector is not available in {{observability}} apps, and most apps remain scoped to the origin project. The following table shows how each {{observability}} app behaves with {{cps-init}}:

::::{include} /solutions/_snippets/cps-obs-compatibility.md
::::

For specific app details, refer to [{{cps-cap}} in {{observability}}](/solutions/observability/cross-project-search.md).

### {{cps-cap}} availability in {{elastic-sec}} apps [cps-availability-security]

:::{include} /explore-analyze/cross-project-search/_snippets/cps-availability-security-apps.md
:::

## Related pages

* [{{cps-cap}} overview](/explore-analyze/cross-project-search.md)
* [Project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md)
* [How search works in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-search.md)
* [Configure {{cps}} access and scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md)
* [ES\|QL in {{kib}}](/explore-analyze/query-filter/languages/esql-kibana.md)
* [Query across Serverless projects with ES\|QL](elasticsearch://reference/query-languages/esql/esql-cross-serverless-projects.md)
