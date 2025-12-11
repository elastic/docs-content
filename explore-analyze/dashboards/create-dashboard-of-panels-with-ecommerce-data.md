---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/create-a-dashboard-of-panels-with-ecommerce-data.html
description: Step-by-step tutorial for creating a Kibana dashboard with time series visualizations to analyze eCommerce sales trends and patterns.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Create a dashboard with time series charts [create-a-dashboard-of-panels-with-ecommerce-data]

Learn how to create time series visualizations and build a dashboard that tracks trends over time. This tutorial uses eCommerce sample data to analyze sales patterns, but you can apply these techniques to any time-based data.

When you're done, you'll have a complete dashboard showing sales trends, revenue patterns, and customer behavior over time.

:::{image} /explore-analyze/images/kibana-lens_timeSeriesDataTutorialDashboard_8.3.png
:alt: Final dashboard with eCommerce sample data
:screenshot:
:::

## Add the data and create the dashboard [add-the-data-and-create-the-dashboard-advanced]

Add the sample eCommerce data, and set up the dashboard.

1. [Install the eCommerce sample data set](../index.md#gs-get-data-into-kibana).
2. Go to **Dashboards**.
3. On the **Dashboards** page, click **Create dashboard**.


## Open and set up the visualization editor [open-and-set-up-lens-advanced]

Open the visualization editor, then make sure the correct fields appear.

1. Create a visualization.
   
   * {applies_to}`stack: ga 9.2` Select **Add** > **Visualization** in the toolbar.
   * {applies_to}`stack: ga 9.0` Click **Create visualization**.

2. Make sure the **Kibana Sample Data eCommerce** {{data-source}} appears, then set the [time filter](../query-filter/filtering.md) to **Last 30 days**.

## Create visualizations with custom time intervals [custom-time-interval]

When you create visualizations with time series data, you can use the default time interval or increase and decrease the interval. For performance reasons, the visualization editor allows you to choose the minimum time interval, but not the exact time interval. The interval limit is controlled by the [`histogram:maxBars`](kibana://reference/advanced-settings.md#histogram-maxbars) setting and [time range](../query-filter/filtering.md).

To analyze the data with a custom time interval, create a bar chart that shows you how many orders were made at your store every hour:

1. From the **Available fields** list, drag **Records** to the workspace.

    The visualization editor creates a bar chart.

2. To zoom in on the data, click and drag your cursor across the bars.

   :::{image} /explore-analyze/images/kibana-lens_clickAndDragZoom_7.16.gif
   :alt: Cursor clicking and dragging across the bars to zoom in on the data
   :screenshot:
   :::

3. In the layer pane, click **Count of records**.

    1. Click **Advanced**.
    2. From the **Normalize by unit** dropdown, select **per hour**, then click **Close**.

        **Normalize by unit** converts `Count of records` into `Count of records per hour` by dividing by 24.

    3. In the **Name** field, enter `Number of orders`.
    4. Click **Close**.

4. To hide the **Horizontal axis** label, open the **Bottom Axis** menu, then select **None** from the **Axis title** dropdown.

To identify the 75th percentile of orders, add a reference line:

1. In the layer pane, click **Add layer > Reference lines**.
2. Click **Static value**.

    1. Click **Quick function**, then click **Percentile**.
    2. From the **Field** dropdown, select **total_quantity**.
    3. In the **Reference line value** field, enter `75`.

3. Configure the **Appearance** options.

    1. In the **Name** field, enter `75th`.
    2. To display the name, select **Name** from **Text decoration**.
    3. From the **Icon decoration** dropdown, select **Tag**.
    4. In the **Color** field, enter `#E7664C`.

4. Click **Close**.

   :::{image} /explore-analyze/images/kibana-lens_barChartCustomTimeInterval_8.3.png
   :alt: Orders per day
   :screenshot:
   :::

5. Click **Save and return**.

## Analyze multiple data series [add-a-data-layer-advanced]

You can create visualizations with multiple data series within the same time interval, even when the series have similar configurations with minor differences.

To analyze multiple series, create a line chart that displays the price distribution of products sold over time:

1. Create a visualization.
   
   * {applies_to}`stack: ga 9.2` Select **Add** > **Visualization** in the toolbar.
   * {applies_to}`stack: ga 9.0` Click **Create visualization** in the dashboard toolbar.

2. Open the **Visualization type** dropdown, then select **Line**.
3. From the **Available fields** list, drag **products.price** to the workspace.

Create the 95th price distribution percentile:

1. In the layer pane, click **Median of products.price**.
2. Click the **Percentile** function.
3. In the **Name** field, enter `95th`, then click **Close**.

To copy a function, you drag it to the **Add or drag-and-drop a field** area within the same group. To create the 90th percentile, duplicate the `95th` percentile:

1. Drag the **95th** field to **Add or drag-and-drop a field** for **Vertical axis**.

   :::{image} /explore-analyze/images/drag-and-drop-a-field-8.16.0.gif
   :alt: Easily duplicate the items with drag and drop
   :screenshot:
   :::

2. Click **95th [1]**, then enter `90` in the **Percentile** field.
3. In the **Name** field enter `90th`, then click **Close**.
4. To create the `50th` and `10th` percentiles, repeat the duplication steps.
5. Open the **Left Axis** menu, select **Custom** from the **Axis title** dropdown, then enter `Percentiles for product prices` in the **Axis title** field.

   :::{image} /explore-analyze/images/kibana-lens_lineChartMultipleDataSeries_7.16.png
   :alt: Percentiles for product prices chart
   :screenshot:
   :::

6. Click **Save and return**.

## Analyze multiple visualization types [add-a-data-layer]

With layers, you can analyze your data with multiple visualization types. When you create layered visualizations, match the data on the horizontal axis so that it uses the same scale.

To analyze multiple visualization types, create an area chart that displays the average order prices, then add a line chart layer that displays the number of customers.

1. Create a visualization.
   
   * {applies_to}`stack: ga 9.2` Select **Add** > **Visualization** in the toolbar.
   * {applies_to}`stack: ga 9.0` Click **Create visualization** in the dashboard toolbar.

2. From the **Available fields** list, drag **products.price** to the workspace.
3. In the layer pane, click **Median of products.price**.

    1. Click the **Average** function.
    2. In the **Name** field, enter `Average price`, then click **Close**.

4. Open the **Visualization type** dropdown, then select **Area**.

Add a layer to display the customer traffic:

1. In the layer pane, click **Add layer > Visualization > Line**.
2. From the **Available fields** list, drag **customer_id** to the **Vertical Axis** field in the second layer.
3. In the layer pane, click **Unique count of customer_id**.

    1. In the **Name** field, enter `Number of customers`.
    2. In the **Series color** field, enter `#D36086`.
    3. Click **Right** for the **Axis side**, then click **Close**.

       :::{image} /explore-analyze/images/kibana-lens_advancedTutorial_numberOfCustomers_8.5.0.png
       :alt: Number of customers area chart in Lens
       :::

4. From the **Available fields** list, drag **order_date** to the **Horizontal Axis** field in the second layer.
5. To change the position of the legend, open the **Legend** menu, then select the **Position** arrow that points up.

   :::{image} /explore-analyze/images/kibana-lens_mixedXYChart_7.16.png
   :alt: Layer visualization type menu
   :screenshot:
   :::

6. Click **Save and return**.

## Compare the change in percentage over time [percentage-stacked-area]

By default, the visualization editor displays time series data with stacked charts, which show how the different document sets change over time.

To view change over time as a percentage, create an **Area percentage** chart that displays three order categories over time:

1. Create a visualization.
   
   * {applies_to}`stack: ga 9.2` Select **Add** > **Visualization** in the toolbar.
   * {applies_to}`stack: ga 9.0` Click **Create visualization** in the dashboard toolbar.

2. From the **Available fields** list, drag **Records** to the workspace.
3. Open the **Visualization type** dropdown, then select **Area**.

For each order category, create a filter:

1. In the layer pane, click **Add or drag-and-drop a field** for **Breakdown**.
2. Click the **Filters** function.
3. Click **All records**, enter the following in the query bar, then press Return:

    * **KQL** — `category.keyword : *Clothing`
    * **Label** — `Clothing`

4. Click **Add a filter**, enter the following in the query bar, then press Return:

    * **KQL** — `category.keyword : *Shoes`
    * **Label** — `Shoes`

5. Click **Add a filter**, enter the following in the query bar, then press Return:

    * **KQL** — `category.keyword : *Accessories`
    * **Label** — `Accessories`

6. Click **Close**.
7. Open the **Legend** menu, then select the **Position** arrow that points up.

   :::{image} /explore-analyze/images/kibana-lens_areaPercentageNumberOfOrdersByCategory_8.3.png
   :alt: Prices share by category
   :screenshot:
   :::

8. Click **Save and return**.

## View the cumulative number of products sold on weekends [view-the-cumulative-number-of-products-sold-on-weekends]

To determine the number of orders made only on Saturday and Sunday, create an area chart, then add it to the dashboard.

1. Create a visualization.
   
   * {applies_to}`stack: ga 9.2` Select **Add** > **Visualization** in the toolbar.
   * {applies_to}`stack: ga 9.0` Click **Create visualization** in the dashboard toolbar.

2. Open the **Visualization type** dropdown, then select **Area**.

Configure the cumulative sum of store orders:

1. From the **Available fields** list, drag **Records** to the workspace.
2. In the layer pane, click **Count of records**.
3. Click the **Cumulative sum** function.
4. In the **Name** field, enter `Cumulative weekend orders`, then click **Close**.

Filter the results to display the data for only Saturday and Sunday:

1. In the layer pane, click **Add or drag-and-drop a field** for **Breakdown**.
2. Click the **Filters** function.
3. Click **All records**, enter the following in the query bar, then press Return:

    * **KQL** — `day_of_week : "Saturday" or day_of_week : "Sunday"`
    * **Label** — `Saturday and Sunday`

        The [KQL filter](../query-filter/languages/kql.md) displays all documents where `day_of_week` matches `Saturday` or `Sunday`.

4. Click **Close**.
5. Open the **Legend** menu, then click **Hide** next to **Visibility**.

   :::{image} /explore-analyze/images/kibana-lens_areaChartCumulativeNumberOfSalesOnWeekend_7.16.png
   :alt: Area chart with cumulative sum of orders made on the weekend
   :screenshot:
   :width: 50%
   :::

6. Click **Save and return**.

## Compare time ranges [compare-time-ranges]

With **Time shift**, you can compare the data from different time ranges. To make sure the data displays correctly, choose a multiple of the date histogram interval when you use multiple time shifts. For example, you are unable to use a **36h** time shift for one series, and a **1d** time shift for the second series if the interval is **days**.

To compare two time ranges, create a line chart that compares the sales in the current week with sales from the previous week:

1. Create a visualization.
   
   * {applies_to}`stack: ga 9.2` Select **Add** > **Visualization** in the toolbar.
   * {applies_to}`stack: ga 9.0` Click **Create visualization** in the dashboard toolbar.

2. Open the **Visualization type** dropdown, then select **Line**.
3. From the **Available fields** list, drag **Records** to the workspace.
4. To duplicate **Count of records**, drag **Count of records** to **Add or drag-and-drop a field** for **Vertical axis** in the layer pane.

To create a week-over-week comparison, shift **Count of records [1]** by one week:

1. In the layer pane, click **Count of records [1]**.
2. Click **Advanced**, select **1 week ago** from the **Time shift** dropdown, then click **Close**.

   To use custom time shifts, enter the time value and increment, then press Enter. For example, enter **1w** to use the **1 week ago** time shift.

   :::{image} /explore-analyze/images/kibana-lens_time_shift.png
   :alt: Line chart with week-over-week sales comparison
   :screenshot:
   :width: 50%
   :::

3. Click **Save and return**.

Time shifts can be used on any metric. The special shift **previous** will show the time window preceding the currently selected one in the time picker in the top right, spanning the same duration. For example, if **Last 7 days** is selected in the time picker, **previous** will show data from 14 days ago to 7 days ago. This mode can’t be used together with date histograms.

### Analyze the percent change between time ranges [compare-time-as-percent]

With **Formula**, you can analyze the percent change in your data from different time ranges.

To compare time range changes as a percent, create a bar chart that compares the sales in the current week with sales from the previous week:

1. Create a visualization.
   
   * {applies_to}`stack: ga 9.2` Select **Add** > **Visualization** in the toolbar.
   * {applies_to}`stack: ga 9.0` Click **Create visualization** in the dashboard toolbar.

2. From the **Available fields** list, drag **Records** to the workspace.
3. In the layer pane, click **Count of records**.
4. Click **Formula**, then enter `count() / count(shift='1w') - 1` in the **Formula** field.
5. In the **Name** field, enter `Percent of change`.
6. From the **Value format** dropdown, select **Percent**, then enter `0` in the **Decimals** field.
7. Click **Close**.

   :::{image} /explore-analyze/images/kibana-lens_percent_chage.png
   :alt: Bar chart with percent change in sales between the current time and the previous week
   :screenshot:
   :width: 50%
   :::

8. Click **Save and return**.

## Analyze the data in a table [view-customers-over-time-by-continents]

With tables, you can view and compare the field values, which is useful for displaying the locations of customer orders.

Create a date histogram table and group the customer count metric by category, such as the continent registered in user accounts:

1. Create a visualization.
   
   * {applies_to}`stack: ga 9.2` Select **Add** > **Visualization** in the toolbar.
   * {applies_to}`stack: ga 9.0` Click **Create visualization** in the dashboard toolbar.

2. Open the **Visualization type** dropdown, then select **Table**.
3. From the **Available fields** list, drag **customer_id** to the **Metrics** field in the layer pane.

    1. In the layer pane, click **Unique count of customer_id**.
    2. In the **Name** field, enter `Customers`, then click **Close**.

4. From the **Available fields** list, drag **order_date** to the **Rows** field in the layer pane.

    1. In the layer pane, click the **order_date**.
    2. In the **Minimum interval** field, enter **1d**.
    3. In the **Name** field, enter `Sales`, then click **Close**.


To split the metric, add columns for each continent using the **Columns** field:

1. From the **Available fields** list, drag **geoip.continent_name** to the **Split metrics by** field in the layer pane.

   :::{image} /explore-analyze/images/kibana-lens_table_over_time.png
   :alt: Date histogram table with groups for the customer count metric
   :screenshot:
   :width: 50%
   :::

2. Click **Save and return**.


## Save the dashboard [_save_the_dashboard_2]

Now that you have a complete overview of your eCommerce sales data, save the dashboard.

1. In the toolbar, click **Save**.
2. On the **Save dashboard** window, enter `eCommerce sales`.
3. Select **Store time with dashboard**.
4. Click **Save**.

:::{image} /explore-analyze/images/kibana-lens_timeSeriesDataTutorialDashboard_8.3.png
:alt: Final dashboard with eCommerce sample data
:screenshot:
:::

