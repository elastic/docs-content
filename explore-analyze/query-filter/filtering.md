---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/kibana-concepts-analysts.html
  - https://www.elastic.co/guide/en/kibana/current/set-time-filter.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Filtering in Kibana

$$$_finding_your_apps_and_objects$$$

This page describes the common ways Kibana offers in most apps for filtering data and refining your initial search queries.

Some apps provide more options, such as [Dashboards](../dashboards.md).

## Time filter [set-time-filter]

Display data within a specified time range when your index contains time-based events, and a time-field is configured for the selected [{{data-source}}](../find-and-organize/data-views.md). The default time range is 15 minutes, but you can customize it in [Advanced Settings](kibana://reference/advanced-settings.md).

:::::{applies-switch}
::::{applies-item} { stack: preview 9.5+, serverless: preview }
1. Select the time range control.
2. Set the time range in one of the following ways:

    * For a common range, such as today or the last 15 minutes, select it under **Presets**.
    * To reuse a range that you selected earlier, select **Recent**.
    * If you know the range, enter it directly, such as `last 5 minutes` or `-12d to now`, then press **Enter**.
    * To select start and end dates from a calendar, select **Calendar**, select the dates, then select **Apply**.
    * To configure the start and end separately, select **Custom range**, set each one as **Relative**, **Absolute**, or **Now**, then select **Apply**.

:::{image} /explore-analyze/images/kibana-date-range-picker.png
:alt: Date range picker showing presets and controls for custom ranges, settings, and saving presets
:screenshot:
:width: 250px
:::

3. Open {icon}`gear` **Settings** to configure automatic refresh and time display:

    * Turn **Refresh every** on or off and set the refresh interval.
    * Review **Time format and zone**, and select **Advanced settings** to change the time zone if you have access.
    * Turn **Round relative time ranges** on or off.
    * Under **Absolute time range**, select whether timestamps show **Minutes**, **Seconds**, or **Milliseconds**.

4. Save the current range as a preset and apply it with {icon}`save`. Saved ranges appear under **Presets**.

:::{note}
The new picker doesn't support auto-refresh-only views. In those views, the time control and auto-refresh aren't available.
:::
::::

::::{applies-item} { stack: ga 9.0-9.4 }
1. Open the {icon}`calendar` time filter.
2. Select one of the following:

    * **Quick select**. Set a time based on the last or next number of seconds, minutes, hours, or other time unit.
    * **Commonly used**. Select a time range from options such as **Last 15 minutes**, **Today**, and **Week to date**.
    * **Recently used date ranges**. Use a previously selected date range.
    * **Refresh every**. Specify an automatic refresh rate.

:::{image} /explore-analyze/images/kibana-time-filter.png
:alt: Time filter menu
:screenshot:
:width: 200px
:::

3. To set start and end times, select the bar next to the time filter. In the popup, select **Absolute**, **Relative**, or **Now**, then specify the required options.
::::
:::::

The global time filter limits the time range of data displayed. In most cases, the time filter applies to the time field in the data view, but some apps allow you to use a different time field.

Using the time filter, you can configure a refresh rate to periodically resubmit your searches.

To manually resubmit a search, click the **Refresh** button. This is useful when you use Kibana to view the underlying data.

## Additional filters [autocomplete-suggestions]

Structured filters are a more interactive way to create {{es}} queries, and are commonly used when building dashboards that are shared by multiple analysts. Each filter can be disabled, inverted, or pinned across all apps. Each of the structured filters is combined with AND logic on the rest of the query.

![Add filter popup](/explore-analyze/images/kibana-add-filter-popup.png "")