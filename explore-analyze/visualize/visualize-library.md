---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/visualize-library.html
  - https://www.elastic.co/guide/en/kibana/current/manage-panels.html
navigation_title: Visualize library
type: how-to
description: Create visualizations in the Visualize library and save panels to reuse them on several dashboards. Learn how to add a library panel and unlink it.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Reuse panels from the Visualize library [visualize-library]

A panel is a chart, map, or other block of content on a dashboard. The **Visualize library** is where you save panels so that several dashboards can reuse them. Use it to share one panel across dashboards, to build a visualization before you tie it to a dashboard, and to give one dashboard its own copy of a shared panel. To find the library, refer to [Open the library](#visualize-library-access).

## Before you begin [visualize-library-before-you-begin]

### Permissions [visualize-library-permissions]

The privileges you need depend on the task:

* To open the library, you need the **Read** privilege for the **Visualize library** feature in {{product.kibana}}. To create visualizations in the library, you need the **All** privilege.
* To add a library panel to a dashboard or unlink one, you need the **All** privilege for the **Dashboard** feature.
* To save a dashboard panel to the library, you need the **All** privilege for the **Dashboard** feature, plus the **All** privilege for the feature behind the panel type. Lens, Vega, and legacy visualizations belong to **Visualize library**, maps belong to **Maps**, and Discover sessions belong to **Discover**. Links panels and Markdown panels need no privilege beyond **Dashboard**.

### Library panels and dashboard panels [visualize-library-vs-dashboard-panels]

A panel is either a library panel or a dashboard panel. The difference is where {{kib}} stores it.

* **Library panels** are saved in the library. Every dashboard that uses a library panel shows the same panel, so an edit you save appears on all of them. Use a library panel when the same chart belongs on several dashboards, for example an error-rate chart that appears on both a team dashboard and an executive dashboard.

    You might also see this called a by-reference panel, because every dashboard points to the one copy in the library.
* **Dashboard panels** are saved only with the dashboard where you created them. An edit changes that dashboard and nothing else. Use a dashboard panel for a chart that only one dashboard needs. If you remove a dashboard panel, it is deleted.

    You might also see this called a by-value panel, because the dashboard holds the full definition of the panel.

You can change a panel from one kind to the other. [Save a dashboard panel to the library](#save-to-visualize-library) to share it, or [unlink a library panel](#unlink-library-panel) to give a dashboard its own copy.

### Panel types you can save to the library [visualize-library-what-you-can-save]

Unless the remarks say otherwise, a panel type in this table appears in the **Visualizations** tab and when you add a panel from the library to a dashboard.

| Panel type | Remarks |
| --- | --- |
| [Lens](lens.md) visualizations | Lens visualizations based on an {{esql}} query are not supported. The **Save to library** action isn't available for them. |
| [Maps](maps.md) |  |
| [Links](link-panels.md) panels | You can't create them directly from the library. Instead, create the panel on a dashboard, then save it to the library. |
| {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` [Markdown](text-panels.md#markdown-library-reuse) panels | Appear only when you add a panel from the library to a dashboard, not in the **Visualizations** tab. You can't create them directly from the library. Instead, create the panel on a dashboard, then save it to the library. |
| [Discover sessions](../discover/save-open-search.md#add-discover-session-from-library) | Appear only when you add a panel from the library to a dashboard, not in the **Visualizations** tab. You can't create them directly from the library. Instead, save the session in **Discover**, or create it on a dashboard and save it to the library. |
| Vega visualizations |  |
| {applies_to}`serverless: unavailable` Legacy visualizations: [aggregation-based](legacy-editors/aggregation-based.md), [TSVB](legacy-editors/tsvb.md), and [Timelion](legacy-editors/timelion.md) |  |

The library doesn't support other panel types. These panels are saved only with the dashboard they belong to.

## Open the library and create visualizations [visualize-library-manage]

In the library, you can create visualizations and manage annotation groups, which are saved sets of chart annotations.

### Open the library [visualize-library-access]

$$$visualize-library-visualizations$$$

To browse your saved visualizations or build a new one, open the library. Where you open it depends on your deployment and version.

The navigation you see depends on the solution view of your space: **Classic**, **Search**, **Observability**, or **Security**. To check the solution view of a space, refer to [Manage spaces](/deploy-manage/manage-spaces.md). In {{serverless-full}}, every project uses a solution view.

- {applies_to}`serverless: ga` On the **Dashboards** page, select the **Visualizations** tab.
- {applies_to}`stack: ga 9.4+` Open the library from one of these places:
  - In a solution view, on the **Dashboards** page, select the **Visualizations** tab.
  - In the Classic view, on the **Dashboards** page, select the **Visualizations** tab, or select **Visualize library** in the navigation menu.
- {applies_to}`stack: ga 9.0-9.3` Select **Visualize library** in the navigation menu, or search for it in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

The library opens on the list of your saved visualizations.

### Create a visualization from the library [visualize-library-create]

To build a visualization before you add it to any dashboard, create it from the library.

1. [Open the library](#visualize-library-access).
2. Select **Create visualization**.
3. Select the type of visualization to build. For the steps to build each type, refer to its page:

   * [Lens](lens.md)
   * [Maps](maps.md)
   * [Vega](custom-visualizations-with-vega.md)
   * {applies_to}`stack: ga` {applies_to}`serverless: unavailable` [Aggregation-based](legacy-editors/aggregation-based.md) and [TSVB](legacy-editors/tsvb.md): Legacy visualizations that you find on the **Legacy** tab of the dialog.

After you save the visualization, it appears in the library and you can add it to any dashboard.

You can't create links panels, Markdown panels, or Discover sessions from the library.

### Reuse annotations across charts with annotation groups [visualize-library-annotation-groups]

Annotation groups mark events such as deployments on your charts. You can reuse the same group on more than one Lens visualization. Annotation groups aren't dashboard panels. To manage them, select the **Annotation groups** tab. To create a group and add it to a chart, refer to [Add annotations](lens.md#add-annotations). When you save a change to a group, every visualization that uses the group shows it.

## Use library panels on dashboards [visualize-library-use-on-dashboards]

### Add a panel from the library to a dashboard [add-a-library-panel]

To use a library panel on another dashboard, add it from the library. The new panel stays linked to the library copy.

1. Open the dashboard and select **Edit**.
2. Open the library picker:

   - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` Select **Add** → **From library**.
   - {applies_to}`stack: ga 9.0-9.1` Select **Add from library**.

3. Select the panel to add.
4. Save the dashboard.

The panel appears on the dashboard and shows the library copy.

### Save a dashboard panel to the library [save-to-visualize-library]

To reuse a dashboard panel on other dashboards, save it to the library.

1. Open the dashboard and select **Edit**.
2. Hover over the panel, then select the {icon}`boxes_vertical` panel menu.
3. Select **Save to library**.
4. Enter a title, then select **Save**.
5. Save the dashboard.

The panel on this dashboard is now a library panel. When you save a later edit, every dashboard that uses the panel shows that edit.

### Change a library panel on one dashboard only [unlink-library-panel]

To change a library panel on one dashboard only, unlink it from the library on that dashboard.

1. Open the dashboard and select **Edit**.
2. Hover over the panel, then select the {icon}`boxes_vertical` panel menu.
3. Select **Unlink from library**.
4. Save the dashboard.

The panel is now a dashboard panel. Edits you make from now on apply to this dashboard only. The library copy and the other dashboards stay as they are.

## Related pages [visualize-library-related]

- [Create a dashboard from the {{kib}} UI](../dashboards/create-dashboard.md)
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` [Save and reuse Markdown panels across dashboards](text-panels.md#markdown-library-reuse)
- [Add a Discover session from the library](../discover/save-open-search.md#add-discover-session-from-library)
- [Add a links panel from the library](link-panels.md#add-links-panel-from-library)
