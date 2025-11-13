---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/dashboard-links.html
description: Add link panels to dashboards for navigation between dashboards or external URLs. Carry time ranges, filters, and queries to maintain exploration context.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Link panels [dashboard-links]

Link panels provide navigation between dashboards or to external websites, helping users discover related content or access supporting documentation. When linking to other dashboards, you can preserve the current time range, filters, and queries to maintain context as users navigate.

Links panels support vertical or horizontal layouts and can be saved to the Visualize Library for reuse. External links respect the [`externalUrl.policy`](kibana://reference/configuration-reference/url-drilldown-settings.md#external-url-policy) security settings.

:::{image} /explore-analyze/images/kibana-dashboard_links_panel.png
:alt: A screenshot displaying the new links panel
:screenshot:
:::

* [Add a links panel](#add-links-panel)
* [Add a links panel from the library](#add-links-panel-from-library)
* [Edit links panels](#edit-links-panel)


## Add a links panel [add-links-panel]

1. Add a new panel.

    * {applies_to}`stack: ga 9.2` Select **Add** > **New panel** in the toolbar.
    * {applies_to}`stack: ga 9.0` Click **Add panel** in the dashboard toolbar.

2. In the **Add panel** flyout, select **Links**. The **Create links panel** flyout appears and lets you add the link you want to display.
3. Choose between the panel displaying vertically or horizontally on your dashboard and add your link.
4. Specify the following:

    * **Go to** - Select **Dashboard** to link to another dashboard, or **URL** to link to an external website.
    * **Choose destination** - Use the dropdown to select another dashboard or enter an external URL.
    * **Text** - Enter text for the link, which displays in the panel.
    * **Options** - When linking to another dashboard, use the sliders to use the filters and queries from the original dashboard, use the date range from the original dashboard, or open the dashboard in a new tab. When linking to an external URL, use the sliders to open the URL in a new tab, or encode the URL.

5. Click **Add link**.
6. Select **Save to library** if you want to reuse the link in other dashboards, and then click **Save**.


## Add a links panel from the library [add-links-panel-from-library]

To add a previously saved links panel to another dashboard:

1. Open the **Add from library** flyout.

    * {applies_to}`stack: ga 9.2` Select **Add** > **From library** in the toolbar.
    * {applies_to}`stack: ga 9.0` Click **Add from library** in the dashboard toolbar.

2. Select **Links** from the **Types** dropdown and then select the Links panel you want to add.
3. Click **Save**.

## Edit links panels [edit-links-panel]

To edit links panels:

1. Hover over the panel and click ![Edit links icon](/explore-analyze/images/kibana-edit-visualization-icon.png "") to edit the link. The **Edit links panel** flyout appears.
2. Click ![Edit link icon](/explore-analyze/images/kibana-edit-link-icon.png "kibana-edit-link-icon =4%x4%") next to the link.

   :::{image} /explore-analyze/images/kibana-edit-links-panel.png
   :alt: A screenshot displaying the Edit icon next to the link
   :screenshot:
   :::

3. Edit the link as needed and then click **Update link**.
4. Click **Save**.
