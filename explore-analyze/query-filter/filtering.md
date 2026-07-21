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
1. Open the time filter.
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

When you enter the time range as text, the time filter interprets a single value as a range relative to now, such as `3 days ago`. To set the start and end explicitly, enter `to` or `until` between two values, such as `yesterday to today`. You can enter and combine any of the following formats:

| Format | Examples |
| --- | --- |
| Relative time | `-15m`, `last 5 minutes`, `past 5 min`, `next 2 weeks`, `2 hours from now`. You can spell out time units or abbreviate them, for example `m`, `min`, or `minutes`. |
| Named ranges | `today`, `yesterday`, `tomorrow`, `this week`, `this month until now`, `last month`, `next year`. The mnemonics `td`, `yd`, and `tmr` stand for today, yesterday, and tomorrow. |
| Absolute time | `Dec 1, 2025, 00:00` (default format), `2025-12-01` (ISO 8601), `Fri, 1 Dec 2025 00:00:00 GMT` (RFC 2822), `12/1/2025` (month/day/year), `1760665383890` (Unix timestamp in seconds or milliseconds). For example, you can paste a date or timestamp copied from a document or a log entry directly into the input. |
| Date math | `now-15m`, `now/w`, and other [date math](elasticsearch://reference/elasticsearch/rest-apis/common-options.md#date-math) expressions. |
| Preset labels | `Last 24 hours` or any other range listed under **Presets**. |

The picker can also give you the text for a range:

- To open the syntax reference, select **Discover allowed formats and shorthands**.
- To get the text equivalent of a range without typing it, select **Custom range** and configure the range. The **Shorthand** field shows the corresponding text, which you can copy and paste into the time filter whenever you need the same range again.

Optionally, you can:

- Open {icon}`gear` **Settings** to configure automatic refresh and time display:

    - Turn **Refresh every** on or off and set the refresh interval.
    - Review **Time format and zone**, and select **Advanced settings** to change the time zone if you have access.
    - Turn **Round relative time ranges** on or off.
    - Under **Absolute time range**, select whether timestamps show **Minutes**, **Seconds**, or **Milliseconds**.

- Save the current range as a preset for later reuse with {icon}`save`, or select **Save as preset** when applying a range from the **Calendar** or **Custom range** panels. Saving a preset also applies the range, and saved ranges appear under **Presets**. Presets are personal to your user profile, and you can save up to 40. To delete one, point to it under **Presets** and select {icon}`trash` **Delete preset**.

- Step through time with the buttons next to the time range: **Previous** and **Next** shift the range backward or forward by its own duration, and **Zoom out** and **Zoom in** widen or narrow it.
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