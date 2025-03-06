---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/_use_and_filter_dashboards.html
---

# Exploring dashboards [_use_and_filter_dashboards]


## Search and filter your dashboard data [search-or-filter-your-data]

{{kib}} supports several ways to explore the data displayed in a dashboard more in depth:

* The **query bar**, using KQL expressions by default.
* The **time range**, that allows you to display data only for the period that you want to focus on. You can set a global time range for the entire dashboard, or specify a custom time range for each panel.
* **Controls**, that dashboard creators can add to help viewers filter on specific values.
* **Filter pills**, that you can add and combine by clicking on specific parts of the dashboard visualizations, or by defining conditions manually from the filter editor. The filter editor is a good alternative if you’re not comfortable with using KQL expressions in the main query bar.
* View the data of a panel and the requests used to build it.

This section shows the most common ways for you to filter dashboard data. For more information about {{kib}} and {{es}} filtering capabilities, refer to [](/explore-analyze/query-filter.md).


### Use filter pills [_use_filter_pills]

Use filter pills to focus in on the specific data you want.

:::{image} ../../images/kibana-dashboard_filter_pills_8.15.0.png
:alt: Filter pills
:screenshot:
:::


#### Add pills by interacting with visualizations [_add_pills_by_interacting_with_visualizations]

You can interact with some panel visualizations to explore specific data more in depth. Upon clicking, filter pills are added and applied to the entire dashboard, so that surrounding panels and visualizations also reflect your browsing.

:::{image} ../../images/add-filter-pills-8.17.gif
:alt: Browsing a chart creates a filter dynamically
:::


#### Add pills using the filter editor [_add_pills_using_the_filter_editor]

As an alternative to the main query bar, you can filter dashboard data by defining individual conditions on specific fields and values, and by combining these conditions together in a filter pill.

:::{image} ../../images/kibana-dashboard-filter-editor.png
:alt: Filter editor with 2 conditions
:::


### Filter dashboards using the KQL query bar [_filter_dashboards_using_the_kql_query_bar]

The query bar lets you build filters using [{{kib}} Query Language (KQL)](../query-filter/languages/kql.md). When typing, it dynamically suggests matching fields, operators, and values to help you get the exact results that you want.

:::{image} ../../images/kibana-dashboard-filter-kql.png
:alt: KQL filter dynamically suggesting values
:::


### Set a time range [_set_a_time_range]

The data visible in a dashboard highly depends on the time range that is applied. In a dashboard, you can select a time range that applies globally to all panels, or set a custom time range for specific panels.


#### Apply a global time range to an entire dashboard [_apply_a_global_time_range_to_an_entire_dashboard]

The global time range menu is located right next to the query bar, in the dashboard’s header. With this menu, you can select the time range to apply, and set the frequency for refreshing the dashboard data. Setting the time range is a common action in {{kib}}. Refer to [Set the time range](../query-filter/filtering.md) for more details.

:::{image} ../../images/kibana-dashboard-global-time-range.png
:alt: Time range menu with multiple time range suggestions
:::


#### Apply a custom time range to a panel [_apply_a_custom_time_range_to_a_panel]

**To apply a panel-level time range:**

1. Hover over the panel and click ![Settings icon](../../images/kibana-settings-icon-hover-action.png ""). The **Settings** flyout appears.
2. Turn on **Apply a custom time range**.
3. Enter the time range you want to view, then click **Apply**.

**To view and edit the time range applied to a specific panel:**

When a custom time range is active for a single panel, it is indicated in the panel’s header.

To edit it, click the filter. You can then adjust and apply the updated **Time range**.


### Use available controls [_use_available_controls]

Dashboard authors can [add various types of additional controls](add-controls.md) to help you filter the data that you want to visualize.


#### Filter the data with Options list controls [filter-the-data-with-options-list-controls]

Filter the data with one or more options that you select.

1. Open the Options list dropdown.
2. Select the available options.

    Selecting *Exists* returns all documents that contain an indexed value for the field.

3. Select how to filter the options.

    * To display only the data for the options you selected, select **Include**.
    * To exclude the data for the options you selected, select **Exclude**.

4. To clear the selections, click ![The icon to clear all selected options in the Options list](../../images/kibana-dashboard_controlsClearSelections_8.3.0.png "").
5. To display only the options you selected in the dropdown, click ![The icon to display only the options you have selected in the Options list](../../images/kibana-dashboard_showOnlySelectedOptions_8.3.0.png "").

:::{image} ../../images/kibana-dashboard_controlsOptionsList_8.7.0.png
:alt: Options list control
:screenshot:
:::


#### Filter the data with Range slider controls [filter-the-data-with-range-slider-controls]

Filter the data within a specified range of values.

1. On the Range slider, click a value.
2. Move the sliders to specify the values you want to display.

    The dashboard displays only the data for the range of values you specified.

3. To clear the specified values, click ![The icon to clear all specified values in the Range slider](../../images/kibana-dashboard_controlsClearSelections_8.3.0.png "").

:::{image} ../../images/kibana-dashboard_controlsRangeSlider_8.3.0.png
:alt: Range slider control
:screenshot:
:::


#### Filter the data with time slider controls [filter-the-data-with-time-slider-controls]

Filter the data within a specified range of time.

1. To view a different time range, click the time slider, then move the sliders to specify the time range you want to display.
2. To advance the time range forward, click ![The icon to advance the time range forward](../../images/kibana-dashboard_timeSliderControl_advanceForward_8.5.0.png "").
3. To advance the time range backward, click ![The icon to advance the time range backward](../../images/kibana-dashboard_timeSliderControl_advanceBackward_8.5.0.png "").
4. To animate the data changes over time, click ![The icon to clear all specified values in the Range slider](../../images/kibana-dashboard_timeSliderControl_animate_8.5.0.png "").
5. To clear the specified values, click ![The icon to clear all specified values in the Range slider](../../images/kibana-dashboard_controlsClearSelections_8.3.0.png "").

:::{image} ../../images/dashboard_timeslidercontrol_8.17.0.gif
:alt: Time slider control
:screenshot:
:::


### View the panel data and requests [download-csv]

**View the data in visualizations and the requests that collect the data:**

1. Open the panel menu and select **Inspect**.
2. View and download the panel data.

    1. Open the **View** dropdown, then click **Data**.
    2. Click **Download CSV**, then select the format type from the dropdown:

        * **Formatted CSV** — Contains human-readable dates and numbers.
        * **Unformatted** — Best used for computer use.

            When you download visualization panels with multiple layers, each layer produces a CSV file, and the file names contain the visualization and layer {{data-source}} names.

3. View the requests that collect the data.

    1. Open the **View** dropdown, then click **Requests**.
    2. From the dropdown, select the requests you want to view.
    3. To view the requests in **Console**, click **Request**, then click **Open in Console**.


**View the time range on specific panels:**

When a custom time range is active for a single panel, it is indicated in the panel’s header.

You can view it in more details and edit it by clicking the filter.


## Full screen mode and maximized panel views [_full_screen_mode_and_maximized_panel_views]

You can display dashboards in full screen mode to gain visual space and view or show visualizations without the rest of the {{kib}} interface.

:::{image} ../../images/kibana-dashboard-full-screen.png
:alt: A dashboard in full screen mode
:::

If you need to focus on a particular panel, you can maximize it by opening the panel menu and selecting **Maximize**. You can minimize it again the same way.

::::{tip}
When sharing a dashboard with a link while a panel is in maximized view, the generated link will also open the dashboard on the same maximized panel view.
::::


:::{image} ../../images/kibana-dashboard-panel-maximized.png
:alt: A maximized panel in a dashboard
:::
