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
:alt: Time filter showing presets and controls for custom ranges, settings, and saving presets
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

A rounding unit makes a range start or end at the edge of a day, month, or year. For example, `-1y/M` starts at the beginning of the month one year ago, and the time filter adds **(rounded)** after the label. For more examples, refer to [Round a range to whole days, months, or years](#round-relative-time-ranges).

The time filter can also give you the text for a range:

- To open the syntax reference, select **Discover allowed formats and shorthands**.
- To get the text equivalent of a range without typing it, select **Custom range** and configure the range. The **Shorthand** field shows the corresponding text, which you can copy and paste into the time filter whenever you need the same range again.

Optionally, you can:

- Open {icon}`gear` **Settings** to configure automatic refresh and time display:

    - Turn **Refresh every** on or off and set the refresh interval.
    - Review **Time format and zone**, and select **Advanced settings** to change the time zone if you have access.
    - Turn **Round relative time ranges** on or off to [round relative ranges automatically](#round-relative-time-ranges).
    - Under **Absolute time range**, select whether timestamps show **Minutes**, **Seconds**, or **Milliseconds**.

- Save the current range as a preset for later reuse with {icon}`save`, or select **Save as preset** when applying a range from the **Calendar** or **Custom range** panels. Saving a preset also applies the range, and saved ranges appear under **Presets**. User-created presets are personal to your user profile, and you can save up to 40. To delete a user-created preset, point to it under **Presets** and select {icon}`trash` **Delete preset**. Ranges from the [**Time filter quick ranges**](kibana://reference/advanced-settings.md#timepicker-quickranges) advanced setting stay in the list under the label configured for each range and cannot be deleted.

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

### Round a range to whole days, months, or years [round-relative-time-ranges]
```{applies_to}
stack: preview 9.5+
serverless: preview
```

With rounding, a relative range starts or ends at the edge of a day, month, or year instead of at an exact time. For example, if it's October 8, 2026 at 13:09, a range that reaches back one year starts at a different point depending on how you round it. You can enter each of these values directly in the time filter, and a single value runs from that point to now.

| You enter | The range starts at |
| --- | --- |
| `-1y` | October 8, 2025, 13:09 |
| `-1y/d` | October 8, 2025, 00:00 |
| `-1y/M` | October 1, 2025, 00:00 |
| `-1y/y` | January 1, 2025, 00:00 |

#### Round the start or end of a range

Adding `/` and a rounding unit after an offset moves a start back to the beginning of that unit and an end forward to the end of it. The time filter accepts these rounding units:

| Unit | Rounds to |
| --- | --- |
| `s` | Second |
| `m` | Minute |
| `h` | Hour |
| `d` | Day |
| `w` | Week |
| `M` | Month |
| `y` | Year |

Rounding units are case-sensitive: `m` is the minute and `M` is the month. The time filter doesn't accept words such as `/mo` or `/month`, so `-1y/M` is how you start at the beginning of the month one year ago.

With `to` between a start and an end, you round both edges. If it's October 8, 2026, these ranges cover:

| You enter | The range covers |
| --- | --- |
| `-7d/d to -1d/d` | The last 7 full days, from October 1 at 00:00 through October 7 at 23:59 |
| `-1y/M to -1y/M` | The whole month one year ago, October 2025 in this example |

#### Round every relative range automatically

With **Round relative time ranges** turned on, the time filter rounds relative ranges for you, so you don't type a rounding unit each time. The setting is off by default. To turn it on, select {icon}`gear` **Settings** in the time filter.

When the setting is on, the time filter adds a rounding unit to each start or end that is a single offset from now and has no rounding unit. For example, `-7d` becomes `-7d/h`, so the range starts at the beginning of the hour instead of at the exact time. A rounding unit that you typed stays as it is, so `-7d/M` doesn't change. The unit that the time filter adds depends on the unit of the offset:

| Offset unit | Rounds to | Example |
| --- | --- | --- |
| Milliseconds, seconds, or minutes | Seconds | `-15m` becomes `-15m/s` |
| Hours | Minutes | `-1h` becomes `-1h/m` |
| Days | Hours | `-7d` becomes `-7d/h` |
| Weeks, months, or years | Days | `-1y` becomes `-1y/d` |

A start or end without an offset, such as `now`, stays as it is.

#### Find out why a range says (rounded)

If a range label says **(rounded)**, the start or end has an offset and a rounding unit. You typed the unit, or the **Round relative time ranges** setting added it. The time filter shows the suffix after the label on the time filter button and in the **Presets** and **Recent** lists. The label describes the offset, not the rounded start. For example, `-1y` shows Last 1 year, and `-1y/y` shows Last 1 year (rounded) even though it starts on January 1 of last year.

Whether the suffix appears depends on the range behind each entry:

- In **Presets**, an entry shows the suffix only if its own range has an offset and a rounding unit.
- In **Recent**, an entry shows the suffix if it was saved with a rounding unit. With **Round relative time ranges** on, the time filter saves the ranges you apply with the added rounding unit.
- On the time filter button, a preset that has no rounding unit shows the suffix after you select it if the setting is on.

A range that covers one whole period, such as Today (`now/d`) or Yesterday (`-1d/d to -1d/d`), doesn't get the suffix because its label already says so. To qualify, the start and end must be identical and the rounding unit must match the offset unit. A range such as `-1y/M to -1y/M` still gets the suffix, because its rounding unit differs from its offset unit.

## Additional filters [autocomplete-suggestions]

Structured filters are a more interactive way to create {{es}} queries, and are commonly used when building dashboards that are shared by multiple analysts. Each filter can be disabled, inverted, or pinned across all apps. Each of the structured filters is combined with AND logic on the rest of the query.

![Add filter popup](/explore-analyze/images/kibana-add-filter-popup.png "")