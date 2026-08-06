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

# Managing {{cps}} scope in your project apps [cps-manage-scope]

When [{{cps}} ({{cps-init}})](/explore-analyze/cross-project-search.md) is enabled and projects are linked, searches initiated from your project's apps run across all linked projects by default. {{kib}} provides several ways to narrow or change this scope:

* **Space default**: Admins [configure a default scope for each space](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope), which applies when you start a new session.
* **Session scope**: Use the [{{cps-init}} scope selector](#cps-in-kibana) in the project's header to change which projects are searched during your session.
* **Query-level override**: Use project routing or qualified index expressions in individual queries to target specific projects.

## {{cps-cap}} scope selector [cps-in-kibana]

The **{{cps-cap}} ({{cps-init}}) scope** selector ({icon}`cross_project_search`) in your project's header lets you control which linked projects your searches include.

<!-- TODO: screenshot of the scope selector open, showing the project list with toggles and tag filter area -->

The scope selector lists all linked projects in alphabetical order. The origin project always appears first, labeled **This project**. Each project row shows the project name, project type icon, and any assigned [tags](/explore-analyze/cross-project-search/cross-project-search-tags.md).

From the scope selector, you can:

* Toggle individual projects on or off to include or exclude them from searches.
* [Filter the project list by tags](#cps-picker-tag-filters) to find and select projects based on metadata or custom tags.
* Use the context menu on a project row to **Include only this project** or **Exclude only this project**.
* Use the **Include all visible** action in the footer to include all projects that match the current filters.

The footer displays the count of included and excluded projects.

The scope selector is not editable in every app. Some apps display it as **read-only**, meaning the app uses the space default scope but you cannot change it. In read-only mode, filter badges are visible but you cannot create, edit, or remove filters. Other apps show it as **unavailable**, meaning the app searches only the current project. Refer to [{{cps-cap}} availability by app](#cps-availability) for details.

When your scope matches the [space default](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope), the scope selector displays a **Using space defaults** indicator. When you change the scope during a session, the indicator disappears and your selection is preserved as you navigate between apps. Starting a new session resets to the space default.

### Filter projects by tag [cps-picker-tag-filters]

You can narrow the project list in the scope selector by creating tag filters. Tag filters let you find and select projects based on [predefined tags](/explore-analyze/cross-project-search/cross-project-search-tags.md) like `_type`, `_region`, and `_csp`, or custom tags that you define in the {{ecloud}} UI.

To add a tag filter:

1. Open the scope selector and select **Add project tag filter**.
2. Choose a tag from the **Select a tag** dropdown.
3. Choose an operator. The default operator is **is**.
4. If the operator requires a value, choose one or more values from the **Select a value** dropdown.
5. Select **Apply** to add the filter.

<!-- TODO: verify the exact button label for applying a filter -->

The following filter operators are available:

| Operator | Description |
| --- | --- |
| **is** | Matches projects where the tag equals the specified value. |
| **is not** | Matches projects where the tag does not equal the specified value. |
| **is one of** | Matches projects where the tag equals any of the specified values. |
| **is not one of** | Matches projects where the tag does not equal any of the specified values. |
| **exists** | Matches projects that have the tag, regardless of value. No value selector is shown. |
| **does not exist** | Matches projects that do not have the tag. No value selector is shown. |

When multiple filters are active, they are combined with AND logic: a project must match all filters to appear in the list.

#### Manage tag filters

Active filters appear as badges below the filter form. You can:

* Select a filter badge to edit its tag, operator, or value.
* Invert a filter to switch between include and exclude logic.
* Enable or disable a filter without removing it.
* Remove a filter to delete it.

#### Quick-filter from project tags

You can create a filter directly from a project's tags. Select the tag count badge on a project row to open a popover listing that project's tags, then select a tag to create a filter for it.

### Include and exclude projects [cps-picker-include-exclude]

You can control which projects are included in your searches independently of tag filters. Each project row has a toggle switch that includes or excludes it.

You can also use the context menu on any project row for quick actions:

* **Include only this project**: Excludes all other visible projects.
* **Exclude only this project**: Includes all other visible projects except this one.

The scope selector prevents you from excluding every project. The toggle on the last included project is disabled, so at least one project is always included.

If your combination of tag filters and project toggles results in zero included projects, the scope selector displays a warning.

<!-- TODO: verify the exact warning text -->

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
