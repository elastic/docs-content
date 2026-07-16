:::{dropdown} Legend
You can customize the way the legend is displayed and the data it shows. Select ![Legend icon](/explore-analyze/images/kibana-legend-icon.svg "") to open the **Legend** panel.

Use **Visibility** and **Position** to control where the legend appears.

For legends positioned outside the chart on the left or right, use **Width** to set the legend size.

**Layout** {applies_to}`stack: ga 9.4` {applies_to}`serverless: ga`
:   For legends positioned outside the chart at the top or bottom, choose how series labels are arranged:

    - **List**: A compact layout that flows series labels to fit the available space. List is the default for new charts when the legend is at the top or bottom.
    - **Grid**: A table-style layout that aligns series labels and statistics into rows and columns.

    Existing visualizations retain their layout until you change it.

**Statistics**
:   When every chart layer uses a non-categorical horizontal axis, such as a date, time, or numeric axis, select one or more statistics to show for each series:

    - **Average**: Average of all values
    - **Median**: Median value
    - **Minimum**: Minimum value
    - **Maximum**: Maximum value
    - **Range**: Difference between the minimum and maximum values
    - **Last value**: Last value
    - **Last non-null value**: Last value that isn't null
    - **First value**: First value
    - **First non-null value**: First value that isn't null
    - **Difference**: Difference between the first and last values
    - **Difference %**: Percentage difference between the first and last values
    - **Sum**: Sum of all values
    - **Count**: Number of values
    - **Distinct count**: Number of distinct values
    - **Variance**: Variance of all values
    - **Std deviation**: Standard deviation of all values
    - **Current or last value**: Value of the data point under the pointer, or the last value when the pointer isn't over a data point

    All statistics use the aggregated data points shown for the selected time range, not the original documents from {{es}}. After you select a statistic that uses the **Grid** layout, you can add a **Series header** above the legend entries.


**Label truncation**
:   For legends positioned inside the chart, outside on the side, or outside at the top or bottom with the **Grid** layout, choose whether to truncate long series labels and set the maximum number of lines for each label.
:::
