# Set the time range [set-time-filter]

Display data within a specified time range when your index contains time-based events, and a time-field is configured for the selected [{{data-source}}](../../../explore-analyze/find-and-organize/data-views.md). The default time range is 15 minutes, but you can customize it in [Advanced Settings](https://www.elastic.co/guide/en/kibana/current/advanced-options.html).

1. Click ![calendar icon](../../../images/kibana-time-filter-icon.png "").
2. Choose one of the following:

    * **Quick select**. Set a time based on the last or next number of seconds, minutes, hours, or other time unit.
    * **Commonly used**. Select a time range from options such as **Last 15 minutes**, **Today**, and **Week to date**.
    * **Recently used date ranges**. Use a previously selected data range.
    * **Refresh every**. Specify an automatic refresh rate.

        :::{image} ../../../images/kibana-time-filter.png
        :alt: Time filter menu
        :class: screenshot
        :::

3. To set start and end times, click the bar next to the time filter. In the popup, select **Absolute**, **Relative** or **Now**, then specify the required options.

    :::{image} ../../../images/kibana-time-relative.png
    :alt: Time filter showing relative time
    :class: screenshot
    :::


