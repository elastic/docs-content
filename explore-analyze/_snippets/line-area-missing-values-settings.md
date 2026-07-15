::::{dropdown} Missing values
Use **Missing values** to control how gaps appear in area and line charts. Missing values include empty buckets and metrics that return `null` because of their operation or data.

:::{note}
This setting is available when **Include empty rows** is enabled or when a metric produces a null bucket. For example, a moving average can produce null buckets.

This setting isn't available for percentage area charts or charts created from ES|QL queries.
:::

- **Hide**: Don't show gaps in the data.

  ![Hide missing values](/explore-analyze/images/charts-gaps-fill-hide.png "Hide missing values =50%")

- **Zero**: Connect the data points before and after each gap to zero.

  ![Fill gaps to zero](/explore-analyze/images/charts-gaps-fill-zero.png "Fill gaps to zero =50%")

- **Linear**: Connect the data points before and after each gap with a straight line.

  ![Fill gaps with a direct line](/explore-analyze/images/charts-gaps-fill-linear.png "Fill gaps with a direct line =50%")

- **Last**: Fill each gap with a horizontal or vertical line from the last available data point.

  ![Fill gaps with a straight line from last known data point](/explore-analyze/images/charts-gaps-fill-last.png "Fill gaps with a straight line from last known data point =50%")

- **Next**: Fill each gap with a horizontal or vertical line from the next available data point.

  ![Fill gaps with a straight line from next known data point](/explore-analyze/images/charts-gaps-fill-next.png "Fill gaps with a straight line from next known data point =50%")

**End values**
:   Choose how to extend a series to the edge of the chart:

    - **Hide**: Don't extend the series.
    - **Zero**: Extend the series as zero.
    - **Nearest**: Extend the series using its first or last value.

**Show as dotted line**
:   Show the lines used to fill gaps as dotted lines.
::::
