---
description: Create visualizations with aggregation-based editor for multi-level splits and non-time series data. Access classic Kibana chart types with plugin extensibility.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Aggregation-based [add-aggregation-based-visualization-panels]

Aggregation-based visualizations are the core {{kib}} panels, and are not optimized for a specific use case.

With aggregation-based visualizations, you can:

* Split charts up to three aggregation levels, which is more than **Lens** and **TSVB**
* Create visualization with non-time series data
* Use a [Discover session](../../discover/save-open-search.md) as an input
* Sort data tables and use the summary row and percentage column features
* Assign colors to data series
* Extend features with plugins

Aggregation-based visualizations include the following limitations:

* Limited styling options
* Math is unsupported
* Multiple indices is unsupported


## Types of aggregation-based visualizations [types-of-visualizations]

{{kib}} supports the following types of aggregation-based visualizations.

|     |     |
| --- | --- |
| **Area**: Displays data points, connected by a line, where the area between the line and axes are shaded.Use area charts to compare two or more categories over time, and display the magnitude of trends. | ![Area chart](/explore-analyze/images/kibana-area.png "") |
| **Data table**: Displays your aggregation results in a tabular format. Use data tables to display server configuration details, track counts, min,or max values for a specific field, and monitor the status of key services. | ![Data table](/explore-analyze/images/kibana-data_table.png "") |
| **Gauge**: Displays your data along a scale that changes color according to where your data falls on the expected scale. Use the gauge to show how metricvalues relate to reference threshold values, or determine how a specified field is performing versus how it is expected to perform. | ![Gauge](/explore-analyze/images/kibana-gauge.png "") |
| **Goal**: Displays how your metric progresses toward a fixed goal. Use the goal to display an easy to read visual of the status of your goal progression. | ![Goal](/explore-analyze/images/kibana-goal.png "") |
| **Heat map**: Displays graphical representations of data where the individual values are represented by colors. Use heat maps when your data set includescategorical data. For example, use a heat map to see the flights of origin countries compared to destination countries using the sample flight data. | ![Heat map](/explore-analyze/images/kibana-heat_map.png "") |
| **Horizontal Bar**: Displays bars side-by-side where each bar represents a category. Use bar charts to compare data across alarge number of categories, display data that includes categories with negative values, and easily identifythe categories that represent the highest and lowest values. {{kib}} also supports vertical bar charts. | ![Bar chart](/explore-analyze/images/kibana-bar.png "") |
| **Line**: Displays data points that are connected by a line. Use line charts to visualize a sequence of values, discovertrends over time, and forecast future values. | ![Line chart](/explore-analyze/images/kibana-line.png "") |
| **Metric**: Displays a single numeric value for an aggregation. Use the metric visualization when you have a numeric value that is powerful enough to tella story about your data. | ![Metric](/explore-analyze/images/kibana-metric.png "") |
| **Pie**: Displays slices that represent a data category, where the slice size is proportional to the quantity it represents.Use pie charts to show comparisons between multiple categories, illustrate the dominance of one category over others,and show percentage or proportional data. | ![Pie chart](/explore-analyze/images/kibana-pie.png "") |
| **Tag cloud**: Graphical representations of how frequently a word appears in the source text. Use tag clouds to easily produce a summary of large documents andcreate visual art for a specific topic. | ![Tag cloud](/explore-analyze/images/kibana-tag_cloud.png "") |


## Create an aggregation-based visualization panel [create-aggregation-based-panel]

Choose the type of visualization you want to create, then use the editor to configure the options.

1. On the dashboard, click **All types > Aggregation based**.

    1. Select the visualization type you want to create.
    2. Select the data source you want to visualize.

       ::::{note}
       There is no performance impact on the data source you select. For example, saved Discover sessions perform the same as {{data-sources}}.
       ::::

2. Add the [aggregations](../supported-chart-types.md#aggregation-reference) you want to visualize using the editor, then click **Update**.

   ::::{note}
   For the **Date Histogram** to use an **auto interval**, the date field must match the primary time field of the {{data-source}}.
   ::::

3. To change the order, drag and drop the aggregations in the editor.

    ![Option to change the order of aggregations](/explore-analyze/images/kibana-bar-chart-tutorial-3.png "")

4. To customize the series colors, click the series in the legend, then select the color you want to use.

    ![Color picker](/explore-analyze/images/kibana-aggregation-based-color-picker.png "")



## Try it: Create an aggregation-based bar chart [try-it-aggregation-based-panel]

You collected data from your web server, and you want to visualize and analyze the data on a dashboard. To create a dashboard panel of the data, create a bar chart that displays the top five log traffic sources for every three hours.


### Add the data and create the dashboard [_add_the_data_and_create_the_dashboard]

Add the sample web logs data that you’ll use to create the bar chart, then create the dashboard.

1. [Install the web logs sample data set](../../index.md#gs-get-data-into-kibana).
2. Go to **Dashboards**.
3. On the **Dashboards** page, click **Create dashboard**.


### Open and set up the aggregation-based bar chart [_open_and_set_up_the_aggregation_based_bar_chart]

Open the **Aggregation based** editor and change the time range.

1. On the dashboard, click **All types > Aggregation based**, select **Vertical bar**, then select **Kibana Sample Data Logs**.
2. Make sure the [time filter](../../query-filter/filtering.md) is **Last 7 days**.


### Create the bar chart [tutorial-configure-the-bar-chart]

To create the bar chart, add a [bucket aggregation](../supported-chart-types.md#bucket-aggregations), then add the terms sub-aggregation to display the top values.

1. Add a **Buckets** aggregation.

    1. Click **Add**, then select **X-axis**.
    2. From the **Aggregation** dropdown, select **Date Histogram**.
    3. Click **Update**.

        ![Bar chart with sample logs data](/explore-analyze/images/kibana-aggBased_barChartTutorial1_8.4.png "")

2. To show the top five log traffic sources, add a sub-bucket aggregation.

    1. Click **Add**, then select **Split series**.

       ::::{tip}
       Aggregation-based panels support a maximum of three **Split series**.
       ::::

    2. From the **Sub aggregation** dropdown, select **Terms**.
    3. From the **Field** dropdown, select **geo.src**.
    4. Click **Update**.
       ![Bar chart with sample logs data](/explore-analyze/images/kibana-aggBased_barChartTutorial2_8.4.png "")



## Open and edit aggregation-based visualizations in Lens [edit-agg-based-visualizations-in-lens]

When you open aggregation-based visualizations in **Lens**, all configuration options appear in the **Lens** visualization editor.

You can open the following aggregation-based visualizations in **Lens**:

* Area
* Data table
* Gauge
* Goal
* Heat map
* Horizontal bar
* Line
* Metric
* Pie
* Vertical bar

To get started, click **Edit visualization in Lens** in the toolbar.

For more information, check out [Create visualizations with Lens](../lens.md).


### Save and add the panel [save-the-aggregation-based-panel]

Save the panel to the **Visualize Library** and add it to the dashboard, or add it to the dashboard without saving.

To save the panel to the **Visualize Library**:

1. Click **Save to library**.
2. Enter the **Title** and add any applicable [**Tags**](../../find-and-organize/tags.md).
3. Make sure that **Add to Dashboard after saving** is selected.
4. Click **Save and return**.

To save the panel to the dashboard:

1. Click **Save and return**.
2. Add an optional title to the panel.

    1. In the panel header, click **No Title**.
    2. On the **Panel settings** window, select **Show title**.
    3. Enter the **Title**, then click **Save**.


