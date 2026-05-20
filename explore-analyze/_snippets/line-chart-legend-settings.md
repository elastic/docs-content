:::{dropdown} Legend
You can customize the way the legend is displayed and the data it shows. Click ![Legend icon](/explore-analyze/images/kibana-legend-icon.svg "") to open the **Legend** panel.
    
With the **Visibility**, **Position**, and **Width** options, you can adjust the way the legend appears in or next to the visualization.

**Layout** {applies_to}`stack: ga 9.4` {applies_to}`serverless: ga`
:   For legends positioned outside the chart at the top or bottom, choose how series labels are arranged:

    - **List**: A compact layout that flows series labels to fit the available space. List is the default for new charts when the legend is at the top or bottom.
    - **Grid**: A table-style layout that aligns series labels and statistics into rows and columns.

    Visualizations created before this setting was introduced keep their previous layout until you change it.

**Statistics**
:   To make your legends as informative as possible, you can show some additional statistics. All statistics are computed based on the selected time range and the aggregated data points shown in the chart, rather than the original data coming from Elasticsearch. For example, if the metric plotted in the chart is Median(system.memory) and the time range is last 24 hours, when you show the Max statistic in the Legend, the value that shows corresponds to the Max[Median(system.memory)] for the last 24 hours.

  - **Average**: Average value considering all data points in the chart.
  - **Median**: Median value considering all data points in the chart.
  - **Minimum**: Minimum value considering all data points in the chart.
  - **Maximum**: Maximum value considering all data points in the chart.
  - **Range**: Difference between min and max values.
  - **Last value**: Last value considering all data points in the chart.
  - **Last non-null value**: Last non-null value.


**Label truncation**
:   For legends positioned inside the chart, outside on the side, or outside at the top or bottom with the **Grid** layout, choose whether to truncate long series labels and set the maximum number of lines for each label.
:::