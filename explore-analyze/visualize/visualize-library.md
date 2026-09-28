---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/visualize-library.html
  - https://www.elastic.co/guide/en/kibana/current/manage-panels.html
navigation_title: Visualize library
description: Save a panel once and reuse it on other dashboards. Saved edits appear on every dashboard that uses the panel. Unlink a panel to change one dashboard only.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: how-to
---

# Reuse panels from the Visualize library [visualize-library]

Save a panel to the **Visualize library** when you want the same panel on more than one dashboard. The panel stays linked to that library copy. When you save an edit, every dashboard that uses the panel shows the change. Unlink the panel when one dashboard needs a different copy.

## Before you begin [visualize-library-requirements]

You need the **All** privilege for the **Dashboard** feature in {{product.kibana}}.

## What you can save [visualize-library-what-you-can-save]

You can save a panel to the library and add that same panel to other dashboards.

| Panel | Where you find it again |
| --- | --- |
| [Lens](lens.md) visualizations, aggregation-based visualizations, TSVB, Timelion, Vega, [maps](maps.md), and [links](link-panels.md) panels | **Visualizations** tab, and **From library** when you add a panel |
| Markdown panels | {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` **From library** when you add a panel. Markdown panels are not listed on the **Visualizations** tab. Refer to [Save and reuse Markdown panels across dashboards](text-panels.md#markdown-library-reuse). |
| Discover sessions | [Save the session in Discover](../discover/save-open-search.md#_save_a_discover_session), then [add it from the library](../discover/save-open-search.md#add-discover-session-from-library). Discover sessions are not listed on the **Visualizations** tab. |

A [custom panel](custom-panels.md) is saved with its dashboard. You cannot save it to the library.

## Open the library [visualize-library-access]

Where you open the library depends on your version and navigation.

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` On the **Dashboards** page, select **Visualizations** or **Annotation groups**.
- {applies_to}`serverless: ga` **Visualize library** is not in the navigation menu.
- {applies_to}`stack: ga 9.4+` **Visualize library** is not in the navigation menu in a [solution view](/deploy-manage/manage-spaces.md). In the **Classic** view, **Visualize library** stays in the navigation menu.
- {applies_to}`stack: ga 9.0-9.3` Open **Visualize library** from the navigation menu.

You can also search for **Visualize library** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

$$$visualize-library-visualizations$$$

Select **Create visualization** to build a new chart in the library. To save that chart to the library, follow the save steps for the editor you opened. For Lens, refer to [Save and add the panel](lens.md#save-the-lens-panel).

## Save a panel that is already on a dashboard [save-to-visualize-library]

Save a panel from a dashboard when you want to add it to other dashboards later.

1. Open the dashboard and select **Edit**.
2. Open the panel menu and select **Save to library**.
3. Enter a title, then select **Save**.

The panel on this dashboard is now linked to the library. When you save a later edit, every dashboard that uses the panel shows that edit.

## Add a library panel to a dashboard [add-a-library-panel]

Add a panel you already saved. The new panel stays linked to the library.

On a dashboard you are editing, open the library picker:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` Select **Add**, then **From library**.
- {applies_to}`stack: ga 9.0-9.1` Select **Add from library**.

Select the panel. It appears on this dashboard and stays linked to the library. Add the same panel to a second dashboard. Both dashboards show the library copy. After you save an edit on one dashboard, the other dashboard shows that edit.

## Change one dashboard only [save-to-the-dashboard]

Unlink a panel when this dashboard needs its own copy. The library copy stays as it is, and later edits on this dashboard stay here.

1. Open the dashboard and select **Edit**.
2. Open the panel menu and select **Unlink from library**.

To keep a new panel on this dashboard only, add the panel and save the dashboard. Do not select **Save to library**. The panel is stored with the dashboard.

**Remove** deletes a panel that exists only on this dashboard. If the panel is linked, **Remove** takes it off this dashboard and leaves the library copy in place. Select **Edit**, open the panel menu, and select **Remove**.

## Annotation groups [visualize-library-annotation-groups]

**Annotation groups** mark events on a chart, such as a deployment, and you can reuse one group on more than one visualization. They are not dashboard panels. Open them from the **Annotation groups** tab. To create a group and add it to a Lens chart, refer to [Add annotations](lens.md#add-annotations). Changes you save to a group show on every visualization that uses it.

## Related pages [visualize-library-related]

- [Create a dashboard from the {{kib}} UI](../dashboards/create-dashboard.md)
- [Save and reuse Markdown panels across dashboards](text-panels.md#markdown-library-reuse)
- [Add a Discover session from the library](../discover/save-open-search.md#add-discover-session-from-library)
- [Add a links panel from the library](link-panels.md#add-links-panel-from-library)
- [Change panel settings](../dashboards/arrange-panels.md#panel-settings)
- [Open panel data in Discover](../dashboards/drilldowns.md#open-panel-data-in-discover)
