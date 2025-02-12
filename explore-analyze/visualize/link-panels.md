---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/dashboard-links.html
---

# Link panels [dashboard-links]

You can use **Links** panels to create links to other dashboards or external websites. When creating links to other dashboards, you have the option to carry the time range, query, and filters to apply over to the linked dashboard. Links to external websites follow the [`externalUrl.policy`](https://www.elastic.co/guide/en/kibana/current/url-drilldown-settings-kb.html#external-URL-policy) settings. **Links** panels support vertical and horizontal layouts and may be saved to the **Library** for use in other dashboards.

:::{image} ../../images/kibana-dashboard_links_panel.png
:alt: A screenshot displaying the new links panel
:class: screenshot
:::

* [Add a links panel](#add-links-panel)
* [Add a links panel from the library](#add-links-panel-from-library)
* [Edit links panels](#edit-links-panel)


## Add a links panel [add-links-panel]

To add a links panel to your dashboard:

1. From your dashboard, select **Add panel**.
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

1. From your dashboard, select **Add from library**.
2. In the **Add from library** flyout, select **Links** from the **Types** dropdown and then select the Links panel you want to add.
3. Click **Save**.


## Edit links panels [edit-links-panel]

To edit links panels:

1. Hover over the panel and click ![Edit links icon](../../images/kibana-edit-visualization-icon.png "") to edit the link. The **Edit links panel** flyout appears.
2. Click ![Edit link icon](../../images/kibana-edit-link-icon.png "") next to the link.

   :::{image} ../../images/kibana-edit-links-panel.png
   :alt: A screenshot displaying the Edit icon next to the link
   :class: screenshot
   :::

3. Edit the link as needed and then click **Update link**.
4. Click **Save**.
