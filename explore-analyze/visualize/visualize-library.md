---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/visualize-library.html
  - https://www.elastic.co/guide/en/kibana/current/manage-panels.html
navigation_title: Visualize library
description: Save a panel to the Visualize library to reuse it on several dashboards. Learn how library panels differ from dashboard panels and how to unlink one.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Reuse panels from the Visualize library [visualize-library]

The **Visualize library** is where you build a visualization before you tie it to a dashboard, and where you keep panels that you want to use on more than one dashboard. Depending on your version and navigation, you open it as a **Visualizations** tab on the **Dashboards** page or as a separate **Visualize library** page.

## Library panels and dashboard panels [visualize-library-vs-dashboard-panels]

A panel is either a library panel or a dashboard panel. The difference is where {{kib}} stores it.

* **Library panels** are saved in the library. Every dashboard that uses a library panel shows the same panel, so an edit you save appears on all of them. Use a library panel when the same chart belongs on several dashboards, for example an error-rate chart that appears on both a team dashboard and an executive dashboard.
* **Dashboard panels** are saved only with the dashboard where you created them. An edit changes that dashboard and nothing else. Use a dashboard panel for a chart that only one dashboard needs. If you remove a dashboard panel, it is deleted.

You can change a panel from one kind to the other. Save a dashboard panel to the library to share it, or unlink a library panel to give a dashboard its own copy.

## Panel types you can save to the library [visualize-library-what-you-can-save]

Unless the remarks say otherwise, a panel type in this table appears in the **Visualizations** tab and when you add a panel from the library to a dashboard.

| Panel type | Remarks |
| --- | --- |
| [Lens](lens.md) visualizations | Lens visualizations based on an {{esql}} query are not supported. |
| [Maps](maps.md) |  |
| [Links](link-panels.md) panels | You can't create them directly from the library. Instead, create the panel on a dashboard, then save it to the library. |
| {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` [Markdown](text-panels.md#markdown-library-reuse) panels | Appear only when you add a panel from the library to a dashboard, not in the **Visualizations** tab. You can't create them directly from the library. Instead, create the panel on a dashboard, then save it to the library. |
| [Discover sessions](../discover/save-open-search.md#add-discover-session-from-library) | Appear only when you add a panel from the library to a dashboard, not in the **Visualizations** tab. You can't create them directly from the library. Instead, save the session in **Discover**, then add it from the library. |
| Vega visualizations |  |
| Legacy visualizations: [aggregation-based](legacy-editors/aggregation-based.md), [TSVB](legacy-editors/tsvb.md), and [Timelion](legacy-editors/timelion.md) |  |
| Any other panel type | Not supported by the library. These panels are saved only with the dashboard they belong to. |

## Open the library [visualize-library-access]

$$$visualize-library-visualizations$$$

Where you open the library depends on your deployment and version.

- {applies_to}`serverless: ga` On the **Dashboards** page, select the **Visualizations** tab.
- {applies_to}`stack: ga 9.4` Open the library from one of these places:
  - In a solution view, on the **Dashboards** page, select the **Visualizations** tab.
  - In the Classic view, on the **Dashboards** page, select the **Visualizations** tab, or select **Visualize library** in the navigation menu.
- {applies_to}`stack: ga 9.0-9.3` Select **Visualize library** in the navigation menu, or search for it in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

## Save a dashboard panel to the library [save-to-visualize-library]

To reuse a dashboard panel, save it to the library. Panel actions are in the panel menu {icon}`boxes_vertical`, which appears when you hover over a panel.

1. Open the dashboard and select **Edit**.
2. Hover over the panel, then select the {icon}`boxes_vertical` panel menu.
3. Select **Save to library**.
4. Enter a title, then select **Save**.

The panel on this dashboard is now a library panel. When you save a later edit, every dashboard that uses the panel shows that edit.

## Add a panel from the library to a dashboard [add-a-library-panel]

To use a library panel on another dashboard, add it from the library. The new panel stays linked to the library copy.

1. Open the dashboard and select **Edit**.
2. Open the library picker:

   - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2` Select **Add**, then **From library**.
   - {applies_to}`stack: ga 9.0-9.1` Select **Add from library**.

3. Select the panel to add.

The panel appears on the dashboard and shows the library copy.

## Change a library panel on one dashboard only [unlink-library-panel]

To change a library panel on one dashboard only, unlink it from the library on that dashboard.

1. Open the dashboard and select **Edit**.
2. Hover over the panel, then select the {icon}`boxes_vertical` panel menu.
3. Select **Unlink from library**.

The panel is now a dashboard panel. Edits you make from now on apply to this dashboard only. The library copy and the other dashboards stay as they are.

## Annotation groups [visualize-library-annotation-groups]

Annotation groups mark events such as deployments on your charts. You can reuse the same group on more than one Lens visualization. Annotation groups are not dashboard panels. To manage them, select the **Annotation groups** tab. To create a group and add it to a chart, refer to [Add annotations](lens.md#add-annotations). When you save a change to a group, every visualization that uses the group shows it.

## Related pages [visualize-library-related]

- [Create a dashboard from the {{kib}} UI](../dashboards/create-dashboard.md)
- [Save and reuse Markdown panels across dashboards](text-panels.md#markdown-library-reuse)
- [Add a Discover session from the library](../discover/save-open-search.md#add-discover-session-from-library)
- [Add a links panel from the library](link-panels.md#add-links-panel-from-library)
