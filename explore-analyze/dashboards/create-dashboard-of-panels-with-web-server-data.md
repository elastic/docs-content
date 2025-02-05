---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/create-a-dashboard-of-panels-with-web-server-data.html
---

# Create a simple dashboard to monitor website logs [create-a-dashboard-of-panels-with-web-server-data]

Learn the most common ways to create a dashboard from your own data. The tutorial will use sample data from the perspective of an analyst looking at website logs, but this type of dashboard works on any type of data.

When you’re done, you’ll have a complete overview of the sample web logs data.

:::{image} ../../images/kibana-lens_logsDashboard_8.4.0.png
:alt: Logs dashboard
:class: screenshot
:::

Before you begin, you should be familiar with the [*{{kib}} concepts*](../overview/kibana-quickstart.md).


## Add the data and create the dashboard [add-the-data-and-create-the-dashboard]

Add the sample web logs data, and create and set up the dashboard.

1. [Install the web logs sample data set](../overview/kibana-quickstart.md#gs-get-data-into-kibana).
2. Go to **Dashboards**.
3. Click **Create dashboard**.
4. Set the [time filter](../query-filter/filtering.md) to **Last 90 days**.


## Open the visualization editor and get familiar with the data [open-and-set-up-lens]

Open the visualization editor, then make sure the correct fields appear.

1. On the dashboard, click **Create visualization**.
2. Make sure the **{{kib}} Sample Data Logs** {{data-source}} appears.

    :::{image} ../../images/kibana-lens_dataViewDropDown_8.4.0.png
    :alt: Data view dropdown
    :class: screenshot
    :::


To create the visualizations in this tutorial, you’ll use the following fields:

* **Records**
* **timestamp**
* **bytes**
* **clientip**
* **referer.keyword**

Click a field name to view more details, such as its top values and distribution.

:::{image} https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt25c7a05e0f5daaa3/671966b9b1d3dd705a2ae650/tutorial-field-more-info.gif
:alt: Clicking a field name to view more details
:class: screenshot
:::


## Create your first visualization [view-the-number-of-website-visitors]

Pick a field you want to analyze, such as **clientip**. To analyze only the **clientip** field, use the **Metric** visualization to display the field as a number.

The only number function that you can use with **clientip** is **Unique count**, also referred to as cardinality, which approximates the number of unique values.

1. Open the **Visualization type** dropdown, then select **Metric**.

    :::{image} images/visualization-type-dropdown-8.16.0.png
    :alt: Visualization type dropdown
    :class: screenshot
    :::

2. From the **Available fields** list, drag **clientip** to the workspace or layer pane.

    :::{image} images/tutorial-unique-count-of-client-ip-8.16.0.png
    :alt: Metric visualization of the clientip field
    :class: screenshot
    :::

    In the layer pane, **Unique count of clientip** appears because the editor automatically applies the **Unique count** function to the **clientip** field. **Unique count** is the only numeric function that works with IP addresses.

3. In the layer pane, click **Unique count of clientip**.

    1. In the **Name** field, enter `Unique visitors`.
    2. Click **Close**.

4. Click **Save and return**.


## View a metric over time [mixed-multiaxis]

There are two shortcuts you can use to view metrics over time. When you drag a numeric field to the workspace, the visualization editor adds the default time field from the {{data-source}}. When you use the **Date histogram** function, you can replace the time field by dragging the field to the workspace.

To visualize the **bytes** field over time:

1. On the dashboard, click **Create visualization**.
2. From the **Available fields** list, drag **bytes** to the workspace.

    The visualization editor creates a bar chart with the **timestamp** and **Median of bytes** fields.

3. To zoom in on the data, click and drag your cursor across the bars.

    :::{image} ../../images/kibana-lens_end_to_end_3_1_1.gif
    :alt: Zoom in on the data
    :class: screenshot
    :::


To emphasize the change in **Median of bytes** over time, change the visualization type to **Line** with one of the following options:

* In the **Suggestions**, click the line chart.
* In the editor toolbar, open the **Visualization type** dropdown, then select **Line**.
* In the layer pane, open the **Layer visualization type** menu, then click **Line**.

To increase the minimum time interval:

1. In the layer pane, click **timestamp**.
2. Change the **Minimum interval** to **1d**, then click **Close**.

    You can increase and decrease the minimum interval, but you are unable to decrease the interval below the configured [**Advanced Settings**](https://www.elastic.co/guide/en/kibana/current/advanced-options.html).


To save space on the dashboard, hide the axis labels.

1. Open the **Left axis** menu, then select **None** from the **Axis title** dropdown.

    :::{image} images/line-chart-left-axis-8.16.0.png
    :alt: Left axis menu
    :class: screenshot
    :::

2. Open the **Bottom axis** menu, then select **None** from the **Axis title** dropdown.

    :::{image} images/line-chart-bottom-axis-8.16.0.png
    :alt: Bottom axis menu
    :class: screenshot
    :::

3. Click **Save and return**

Since you removed the axis labels, add a panel title:

1. Hover over the panel and click ![Settings icon](../../images/kibana-settings-icon-hover-action.png ""). The **Settings** flyout appears.
2. In the **Title** field, enter `Median of bytes`, then click **Apply**.

    :::{image} ../../images/kibana-lens_lineChartMetricOverTime_8.4.0.png
    :alt: Line chart that displays metric data over time
    :class: screenshot
    :::



## View the top values of a field [view-the-distribution-of-visitors-by-operating-system]

Create a visualization that displays the most frequent values of **request.keyword** on your website, ranked by the unique visitors. To create the visualization, use **Top values of request.keyword** ranked by **Unique count of clientip**, instead of being ranked by **Count of records**.

The **Top values** function ranks the unique values of a field by another function. The values are the most frequent when ranked by a **Count** function, and the largest when ranked by the **Sum** function.

1. On the dashboard, click **Create visualization**.
2. From the **Available fields** list, drag **clientip** to the **Vertical axis** field in the layer pane.

    The visualization editor automatically applies the **Unique count** function. If you drag **clientip** to the workspace, the editor adds the field to the incorrect axis.

3. Drag **request.keyword** to the workspace.

    :::{image} images/tutorial-top-values-of-field-8.16.0.png
    :alt: Vertical bar chart with top values of request.keyword by most unique visitors
    :class: screenshot
    :::

    When you drag a text or IP address field to the workspace, the editor adds the **Top values** function ranked by **Count of records** to show the most frequent values.


The chart labels are unable to display because the **request.keyword** field contains long text fields. You could use one of the **Suggestions**, but the suggestions also have issues with long text. The best way to display long text fields is with the **Table** visualization.

1. Open the **Visualization type** dropdown, then select **Table**.

    :::{image} images/table-with-request-keyword-and-client-ip-8.16.0.png
    :alt: Table with top values of request.keyword by most unique visitors
    :class: screenshot
    :::

2. In the layer pane, click **Top 5 values of request.keyword**.

    1. In the **Number of values** field, enter `10`.
    2. In the **Name** field, enter `Page URL`.
    3. Click **Close**.

        :::{image} ../../images/kibana-lens_tableTopFieldValues_7.16.png
        :alt: Table that displays the top field values
        :class: screenshot
        :::

3. Click **Save and return**.

    Since the table columns are labeled, you do not need to add a panel title.



## Compare a subset of documents to all documents [custom-ranges]

Create a proportional visualization that helps you determine if your users transfer more bytes from documents under 10KB versus documents over 10Kb.

1. On the dashboard, click **Create visualization**.
2. From the **Available fields** list, drag **bytes** to the **Vertical axis** field in the layer pane.
3. In the layer pane, click **Median of bytes**.
4. Click the **Sum** quick function, then click **Close**.
5. From the **Available fields** list, drag **bytes** to the **Breakdown** field in the layer pane.

To select documents based on the number range of a field, use the **Intervals** function. When the ranges are non numeric, or the query requires multiple clauses, you could use the **Filters** function.

Specify the file size ranges:

1. In the layer pane, click **bytes**.
2. Click **Create custom ranges**, enter the following in the **Ranges** field, then press Return:

    * **Ranges** — `0` → `10240`
    * **Label** — `Below 10KB`

3. Click **Add range**, enter the following, then press Return:

    * **Ranges** — `10240` → `+∞`
    * **Label** — `Above 10KB`

        :::{image} ../../images/kibana-lens_end_to_end_6_1.png
        :alt: Custom ranges configuration
        :class: screenshot
        :::

4. From the **Value format** dropdown, select **Bytes (1024)**, then click **Close**.

To display the values as a percentage of the sum of all values, use the **Pie** chart.

1. Open the **Visualization Type** dropdown, then select **Pie**.

    :::{image} ../../images/kibana-lens_pieChartCompareSubsetOfDocs_7.16.png
    :alt: Pie chart that compares a subset of documents to all documents
    :class: screenshot
    :::

2. Click **Save and return**.

Add a panel title:

1. Hover over the panel and click ![Settings icon](../../images/kibana-settings-icon-hover-action.png ""). The **Settings** flyout appears.
2. In the **Title** field, enter `Sum of bytes from large requests`, then click **Apply**.


## View the distribution of a number field [histogram]

The distribution of a number can help you find patterns. For example, you can analyze the website traffic per hour to find the best time for routine maintenance.

1. On the dashboard, click **Create visualization**.
2. From the **Available fields** list, drag **bytes** to **Vertical axis** field in the layer pane.
3. In the layer pane, click **Median of bytes**.

    1. Click the **Sum** quick function.
    2. In the **Name** field, enter `Transferred bytes`.
    3. From the **Value format** dropdown, select **Bytes (1024)**, then click **Close**.

4. From the **Available fields** list, drag **hour_of_day** to **Horizontal axis** field in the layer pane.
5. In the layer pane, click **hour_of_day**, then slide the **Intervals granularity** slider until the horizontal axis displays hourly intervals.

    :::{image} ../../images/kibana-lens_barChartDistributionOfNumberField_7.16.png
    :alt: Bar chart that displays the distribution of a number field
    :class: screenshot
    :::

6. Click **Save and return**.

Add a panel title:

1. Hover over the panel and click ![Settings icon](../../images/kibana-settings-icon-hover-action.png ""). The **Settings** flyout appears.
2. In the **Title** field, enter `Website traffic`, then click **Apply**.


## Create a multi-level chart [treemap]

**Table** and **Proportion** visualizations support multiple functions. For example, to create visualizations that break down the data by website traffic sources and user geography, apply the **Filters** and **Top values** functions.

1. On the dashboard, click **Create visualization**.
2. Open the **Visualization type** dropdown, then select **Treemap**.
3. From the **Available fields** list, drag **Records** to the **Size by** field in the layer pane.
4. In the layer pane, click **Add or drag-and-drop a field** for **Group by**.

Create a filter for each website traffic source:

1. Click **Filters**.
2. Click **All records**, enter the following in the query bar, then press Return:

    * **KQL** — `referer : *facebook.com*`
    * **Label** — `Facebook`

3. Click **Add a filter**, enter the following in the query bar, then press Return:

    * **KQL** — `referer : *twitter.com*`
    * **Label** — `Twitter`

4. Click **Add a filter**, enter the following in the query bar, then press Return:

    * **KQL** — `NOT referer : *twitter.com* OR NOT referer: *facebook.com*`
    * **Label** — `Other`

5. Click **Close**.

Add the user geography grouping:

1. From the **Available fields** list, drag **geo.srcdest** to the workspace.
2. To change the **Group by** order, drag **Top 3 values of geo.srcdest** in the layer pane so that appears first.

    :::{image} ../../images/kibana-lens_end_to_end_7_2.png
    :alt: Treemap visualization
    :class: screenshot
    :::


Remove the documents that do not match the filter criteria:

1. In the layer pane, click **Top 3 values of geo.srcdest**.
2. Click **Advanced**, deselect **Group other values as "Other"**, then click **Close**.

    :::{image} ../../images/kibana-lens_treemapMultiLevelChart_7.16.png
    :alt: Treemap visualization
    :class: screenshot
    :::

3. Click **Save and return**.

Add a panel title:

1. Hover over the panel and click ![Settings icon](../../images/kibana-settings-icon-hover-action.png ""). The **Settings** flyout appears.
2. In the **Title** field, enter `Page views by location and referrer`, then click **Apply**.


## Arrange the dashboard panels [arrange-the-lens-panels]

Resize and move the panels so they all appear on the dashboard without scrolling.

Decrease the size of the following panels, then move the panels to the first row:

* **Unique visitors**
* **Median of bytes**
* **Sum of bytes from large requests**
* **Website traffic**

    :::{image} ../../images/kibana-lens_logsDashboard_8.4.0.png
    :alt: Logs dashboard
    :class: screenshot
    :::



## Save the dashboard [_save_the_dashboard]

Now that you have a complete overview of your web server data, save the dashboard.

1. In the toolbar, click **Save**.
2. On the **Save dashboard** window, enter `Logs dashboard` in the **Title** field.
3. Select **Store time with dashboard**.
4. Click **Save**. You will be identified as the **creator** of the dashboard. If you or another user edit the dashboard, you can also view the **last editor** when checking the dashboard information.

:::{image} ../../images/kibana-dashboard-creator-editor.png
:alt: Information panel of a dashboard showing its creator and last editor
:::
