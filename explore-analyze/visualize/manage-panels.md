---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/manage-panels.html
description: Save panels to Visualize Library for reuse across dashboards or save locally. Configure panel options, manage sharing, and control visualization updates.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Manage panels [manage-panels]

When creating a panel, you can choose to add it to a dashboard, or to save it to the Visualize Library so it can be added to multiple dashboards later.

There are also some common options that you can configure on the various types of panels to make a dashboard easier to navigate and analyze.


### Save to the Visualize Library [save-to-visualize-library] 

To use a panel on multiple dashboards, you can save it to the **Visualize Library**. Any updates made to a shared panel are replicated to all dashboards where the panel is added.

If you created the panel from a dashboard:

1. In the editor, click **Save to library**.
2. Enter the **Title** and add any applicable [**Tags**](../find-and-organize/tags.md).
3. Select **Add to Dashboards after saving** to add the panel to your dashboard at the same time.
4. Click **Save and return**.

If you created the panel from the **Visualize Library**:

1. In the editor, click **Save**.
2. On the **Save** window, enter the **Title**.
3. Choose one of the following options:

    * To save the panel to a dashboard and the **Visualize Library**, select **Add to library**, add any applicable [**Tags**](../find-and-organize/tags.md), then click **Save and go to Dashboard**.
    * To save the panel only to the **Visualize Library**, select **None**, add any applicable [**Tags**](../find-and-organize/tags.md), then click **Save and add to library**.


To add unsaved dashboard panels to the **Visualize Library**:

1. Open the panel menu and select **Save to library**.
2. Enter the panel title, then click **Save**.


### Save to the dashboard [save-to-the-dashboard] 

Return to the dashboard and add the panel without specifying the save options or adding the panel to the **Visualize Library**.

If you created the panel from a dashboard:

1. In the editor, click **Save and return**.
2. Add an optional title to the panel.

    1. In the panel header, click **No Title**.
    2. On the **Panel settings** window, select **Show title**.
    3. Enter the **Title**, then click **Save**.


If you created the panel from the **Visualize Library**:

1. Click **Save**.
2. On the **Save** window, add a **Title** to name the visualization.
3. Choose one of the following options:

    * If you want to add the panel to an existing dashboard, select **Existing**, select the dashboard from the dropdown, then click **Save and go to Dashboard**.
    * If you want to add the panel to a new dashboard, select **New**, then click **Save and go to Dashboard**.


## Link to Discover [explore-the-underlying-documents]

You can add interactions to panels that allow you to open and explore the data in **Discover**. To use the interactions, the panel must use only one data view.

There are three types of **Discover** interactions you can add to dashboard panels:

* **Panel interactions** — Opens panel data in **Discover**, including the dashboard-level filters, but not the panel-level filters.

    To enable panel interactions, configure [`xpack.discoverEnhanced.actions.exploreDataInContextMenu.enabled`](kibana://reference/configuration-reference/general-settings.md#settings-explore-data-in-context) in kibana.yml. If you are using 7.13.0 and earlier, panel interactions are enabled by default.

    To use panel interactions, open the panel menu and click **Explore underlying data**.

* **Series data interactions** — Opens the series data in **Discover**.

    To enable series data interactions, configure [`xpack.discoverEnhanced.actions.exploreDataInChart.enabled`](kibana://reference/configuration-reference/general-settings.md#settings-explore-data-in-chart) in kibana.yml. If you are using 7.13.0 and earlier, data series interactions are enabled by default.

    To use series data interactions, click a data series in the panel.

* **Discover session interactions** — Opens [saved Discover session](../discover.md#save-your-search) data in **Discover**.

    To use saved Discover session interactions, open the panel menu and click **View Discover session**.



## Edit panels [edit-panels]

To make changes to the panel, use the panel menu options.

1. In the toolbar, click **Edit**.
2. Open the panel menu, then use the following options:

    * **Edit visualization** — Opens the editor so you can make changes to the panel.

        To make changes without changing the original version, open the panel menu and click **Unlink from library**.

    * **Convert to Lens** — Opens **TSVB** and aggregation-based visualizations in **Lens**.
    * **Settings** — Opens the **Settings** window to change the **title**, **description**, and **time range**.
    * **Remove** — Removes the panel from the dashboard.

        If you want to use the panel later, make sure that you save the panel to the **Visualize Library**.



