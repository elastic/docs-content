---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/kibana-concepts-analysts.html
  - https://www.elastic.co/guide/en/kibana/current/set-time-filter.html
---

# Filtering in Kibana

$$$_finding_your_apps_and_objects$$$

This page describes the common ways Kibana offers in most apps for filtering data and refining your initial search queries.

Some apps provide more options, such as [Dashboards](../dashboards.md).

## Time filter [set-time-filter]

Display data within a specified time range when your index contains time-based events, and a time-field is configured for the selected [{{data-source}}](../find-and-organize/data-views.md). The default time range is 15 minutes, but you can customize it in [Advanced Settings](kibana://reference/advanced-settings.md).

1. Click ![calendar icon](/explore-analyze/images/kibana-time-filter-icon.png "calendar icon =7%x7%").
2. Choose one of the following:

    * **Quick select**. Set a time based on the last or next number of seconds, minutes, hours, or other time unit.
    * **Commonly used**. Select a time range from options such as **Last 15 minutes**, **Today**, and **Week to date**.
    * **Recently used date ranges**. Use a previously selected data range.
    * **Refresh every**. Specify an automatic refresh rate.

:::{image} /explore-analyze/images/kibana-time-filter.png
:alt: Time filter menu
:width: 300px
:::

3. To set start and end times, click the bar next to the time filter. In the popup, select **Absolute**, **Relative** or **Now**, then specify the required options.

:::{image} /explore-analyze/images/kibana-time-relative.png
:alt: Time filter showing relative time
:width: 350px
:::

The global time filter limits the time range of data displayed. In most cases, the time filter applies to the time field in the data view, but some apps allow you to use a different time field.

Using the time filter, you can configure a refresh rate to periodically resubmit your searches.

To manually resubmit a search, click the **Refresh** button. This is useful when you use Kibana to view the underlying data.

## Additional filters [autocomplete-suggestions]

Structured filters are a more interactive way to create {{es}} queries, and are commonly used when building dashboards that are shared by multiple analysts. Each filter can be disabled, inverted, or pinned across all apps. Each of the structured filters is combined with AND logic on the rest of the query.

![Add filter popup](/explore-analyze/images/kibana-add-filter-popup.png "")