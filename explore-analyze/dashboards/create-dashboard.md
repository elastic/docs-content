---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/create-dashboard.html
description: Create dashboards with visualizations, controls, and content from the library. Configure settings, organize panels, and save custom analytics views for data exploration.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Create a dashboard [create-dashboard]

1. Open the **Dashboards** page in {{kib}}.
2. Select **Create dashboard** to start with an empty dashboard.

    When you create a dashboard, you are automatically in edit mode and can make changes to the dashboard.

3. Populate your dashboard with the content that you need. You can:

    * [**Add new visualizations**](../visualize.md#panels-editors). Create a chart using [Lens](../visualize/lens.md), the default visualization editor in {{kib}}, or other visualizations such as [Maps](../visualize/maps.md).
    * [**Add existing content from the library**](../visualize/visualize-library.md). Select existing visualizations or Discover sessions that have already been configured and saved to the **Visualize Library**.
    * [**Add annotations or navigation panels**](../visualize.md#panels-editors). Make your dashboard more informative and easier to read with sections, text, and images.
    * [**Add controls**](add-controls.md). Define a set of interactive filters (options lists, range or time sliders) that you and future users of this dashboard can use to explore its data.  

4. Organize your dashboard by [organizing the various panels](arrange-panels.md).
5. Define the main settings of your dashboard from the **Settings** menu located in the toolbar.

    1. A meaningful title, description, and [tags](../find-and-organize/tags.md) allow you to find the dashboard quickly later when browsing your list of dashboards or using the {{kib}} search bar.
    2. Additional display options allow you unify the look and feel of the dashboard’s panels:

        * **Store time with dashboard** — Saves the specified time filter.
        * **Use margins between panels** — Adds a margin of space between each panel.
        * **Show panel titles** — Displays the titles in the panel headers.
        * **Sync color palettes across panels** — Applies the same color palette to all panels on the dashboard.
        * **Sync cursor across panels** — When you hover your cursor over a time series chart or a heatmap, the cursor on all other related dashboard charts automatically appears.
        * **Sync tooltips across panels** — When you hover your cursor over a **Lens** chart, the tooltips on all other related dashboard charts automatically appear.

    3. Click **Apply**.
       
       ![Change and apply dashboard settings](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt4a6e9807f1fac9f8/6750ee9cef6d5a250c229e50/dashboard-settings-8.17.0.gif "title =50%")

6. Click **Save**  to save the dashboard.
