---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/legacy-editors.html
---

# Legacy editors [legacy-editors]

## Aggregation-based [add-aggregation-based-visualization-panels]

Aggregation-based visualizations are the core {{kib}} panels, and are not optimized for a specific use case.

With aggregation-based visualizations, you can:

* Split charts up to three aggregation levels, which is more than **Lens** and **TSVB**
* Create visualization with non-time series data
* Use a [Discover session](../discover/save-open-search.md) as an input
* Sort data tables and use the summary row and percentage column features
* Assign colors to data series
* Extend features with plugins

Aggregation-based visualizations include the following limitations:

* Limited styling options
* Math is unsupported
* Multiple indices is unsupported


#### Types of aggregation-based visualizations [types-of-visualizations]

{{kib}} supports the following types of aggregation-based visualizations.

|     |     |
| --- | --- |
| **Area**: Displays data points, connected by a line, where the area between the line and axes are shaded.Use area charts to compare two or more categories over time, and display the magnitude of trends. | ![Area chart](../../images/kibana-area.png "") |
| **Data table**: Displays your aggregation results in a tabular format. Use data tables to display server configuration details, track counts, min,or max values for a specific field, and monitor the status of key services. | ![Data table](../../images/kibana-data_table.png "") |
| **Gauge**: Displays your data along a scale that changes color according to where your data falls on the expected scale. Use the gauge to show how metricvalues relate to reference threshold values, or determine how a specified field is performing versus how it is expected to perform. | ![Gauge](../../images/kibana-gauge.png "") |
| **Goal**: Displays how your metric progresses toward a fixed goal. Use the goal to display an easy to read visual of the status of your goal progression. | ![Goal](../../images/kibana-goal.png "") |
| **Heat map**: Displays graphical representations of data where the individual values are represented by colors. Use heat maps when your data set includescategorical data. For example, use a heat map to see the flights of origin countries compared to destination countries using the sample flight data. | ![Heat map](../../images/kibana-heat_map.png "") |
| **Horizontal Bar**: Displays bars side-by-side where each bar represents a category. Use bar charts to compare data across alarge number of categories, display data that includes categories with negative values, and easily identifythe categories that represent the highest and lowest values. {{kib}} also supports vertical bar charts. | ![Bar chart](../../images/kibana-bar.png "") |
| **Line**: Displays data points that are connected by a line. Use line charts to visualize a sequence of values, discovertrends over time, and forecast future values. | ![Line chart](../../images/kibana-line.png "") |
| **Metric**: Displays a single numeric value for an aggregation. Use the metric visualization when you have a numeric value that is powerful enough to tella story about your data. | ![Metric](../../images/kibana-metric.png "") |
| **Pie**: Displays slices that represent a data category, where the slice size is proportional to the quantity it represents.Use pie charts to show comparisons between multiple categories, illustrate the dominance of one category over others,and show percentage or proportional data. | ![Pie chart](../../images/kibana-pie.png "") |
| **Tag cloud**: Graphical representations of how frequently a word appears in the source text. Use tag clouds to easily produce a summary of large documents andcreate visual art for a specific topic. | ![Tag cloud](../../images/kibana-tag_cloud.png "") |


#### Create an aggregation-based visualization panel [create-aggregation-based-panel]

Choose the type of visualization you want to create, then use the editor to configure the options.

1. On the dashboard, click **All types > Aggregation based**.

    1. Select the visualization type you want to create.
    2. Select the data source you want to visualize.

        ::::{note}
        There is no performance impact on the data source you select. For example, saved Discover sessions perform the same as {{data-sources}}.
        ::::

2. Add the [aggregations](supported-chart-types.md#aggregation-reference) you want to visualize using the editor, then click **Update**.

    ::::{note}
    For the **Date Histogram** to use an **auto interval**, the date field must match the primary time field of the {{data-source}}.
    ::::

3. To change the order, drag and drop the aggregations in the editor.

    ![Option to change the order of aggregations](../../images/kibana-bar-chart-tutorial-3.png "")

4. To customize the series colors, click the series in the legend, then select the color you want to use.

    ![Color picker](../../images/kibana-aggregation-based-color-picker.png "")



#### Try it: Create an aggregation-based bar chart [try-it-aggregation-based-panel]

You collected data from your web server, and you want to visualize and analyze the data on a dashboard. To create a dashboard panel of the data, create a bar chart that displays the top five log traffic sources for every three hours.


##### Add the data and create the dashboard [_add_the_data_and_create_the_dashboard]

Add the sample web logs data that you’ll use to create the bar chart, then create the dashboard.

1. [Install the web logs sample data set](../overview/kibana-quickstart.md#gs-get-data-into-kibana).
2. Go to **Dashboards**.
3. On the **Dashboards** page, click **Create dashboard**.


##### Open and set up the aggregation-based bar chart [_open_and_set_up_the_aggregation_based_bar_chart]

Open the **Aggregation based** editor and change the time range.

1. On the dashboard, click **All types > Aggregation based**, select **Vertical bar**, then select **Kibana Sample Data Logs**.
2. Make sure the [time filter](../query-filter/filtering.md) is **Last 7 days**.


##### Create the bar chart [tutorial-configure-the-bar-chart]

To create the bar chart, add a [bucket aggregation](supported-chart-types.md#bucket-aggregations), then add the terms sub-aggregation to display the top values.

1. Add a **Buckets** aggregation.

    1. Click **Add**, then select **X-axis**.
    2. From the **Aggregation** dropdown, select **Date Histogram**.
    3. Click **Update**.

        ![Bar chart with sample logs data](../../images/kibana-aggBased_barChartTutorial1_8.4.png "")

2. To show the top five log traffic sources, add a sub-bucket aggregation.

    1. Click **Add**, then select **Split series**.

        ::::{tip}
        Aggregation-based panels support a maximum of three **Split series**.
        ::::

    2. From the **Sub aggregation** dropdown, select **Terms**.
    3. From the **Field** dropdown, select **geo.src**.
    4. Click **Update**.

        ![Bar chart with sample logs data](../../images/kibana-aggBased_barChartTutorial2_8.4.png "")



#### Open and edit aggregation-based visualizations in Lens [edit-agg-based-visualizations-in-lens]

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

For more information, check out [Create visualizations with Lens](lens.md).


##### Save and add the panel [save-the-aggregation-based-panel]

Save the panel to the **Visualize Library** and add it to the dashboard, or add it to the dashboard without saving.

To save the panel to the **Visualize Library**:

1. Click **Save to library**.
2. Enter the **Title** and add any applicable [**Tags**](../find-and-organize/tags.md).
3. Make sure that **Add to Dashboard after saving** is selected.
4. Click **Save and return**.

To save the panel to the dashboard:

1. Click **Save and return**.
2. Add an optional title to the panel.

    1. In the panel header, click **No Title**.
    2. On the **Panel settings** window, select **Show title**.
    3. Enter the **Title**, then click **Save**.



## TSVB [tsvb-panel]

**TSVB** is a set of visualization types that you configure and display on dashboards.

With **TSVB**, you can:

* Combine an infinite number of [aggregations](supported-chart-types.md#aggregation-reference) to display your data.
* Annotate time series data with timestamped events from an {{es}} index.
* View the data in several types of visualizations, including charts, data tables, and markdown panels.
* Display multiple [data views](../find-and-organize/data-views.md) in each visualization.
* Use custom functions and some math on aggregations.
* Customize the data with labels and colors.

:::{image} ../../images/kibana-tsvb-screenshot.png
:alt: TSVB overview
:class: screenshot
:::


#### Open and set up TSVB [tsvb-data-view-mode]

Open **TSVB**, then configure the required settings. You can create **TSVB** visualizations with only {{data-sources}}, or {{es}} index strings.

When you use only {{data-sources}}, you are able to:

* Create visualizations with runtime fields
* Add URL drilldowns
* Add interactive filters for time series visualizations
* Improve performance

::::{important}
:name: tsvb-index-patterns-mode

Creating **TSVB** visualizations with an {{es}} index string is deprecated and will be removed in a future release. By default, you create **TSVB** visualizations with only {{data-sources}}. To use an {{es}} index string, contact your administrator, or go to [Advanced Settings](https://www.elastic.co/guide/en/kibana/current/advanced-options.html) and set `metrics:allowStringIndices` to `true`.
::::


1. On the dashboard, click **Select type**, then select **TSVB**.
2. In **TSVB**, click **Panel options**, then specify the **Data** settings.
3. Open the **Data view mode** options next to the **Data view** dropdown.
4. Select **Use only {{kib}} {data-sources}**.
5. From the **Data view** dropdown, select the {{data-source}}, then select the **Time field** and **Interval**.
6. Select a **Drop last bucket** option.

    By default, **TSVB** drops the last bucket because the time filter intersects the time range of the last bucket. To view the partial data, select **No**.

7. To view a filtered set of documents, enter [KQL filters](../query-filter/languages/kql.md) in the **Panel filter** field.


#### Configure the series [tsvb-function-reference]

Each **TSVB** visualization shares the same options to create a **Series**. Each series can be thought of as a separate {{es}} aggregation. The **Options** control the styling and {{es}} options, and are inherited from **Panel options**. When you have separate options for each series, you can compare different {{es}} indices, and view two time ranges from the same index.

To configure the value of each series, select the function, then configure the function inputs. Only the last function is displayed.

1. From the **Aggregation** dropdown, select the function for the series. **TSVB** provides you with shortcuts for some frequently-used functions:

    **Filter Ratio**
    :   Returns a percent value by calculating a metric on two sets of documents. For example, calculate the error rate as a percentage of the overall events over time.

    **Counter Rate**
    :   Used when dealing with monotonically increasing counters. Shortcut for **Max**, **Derivative**, and **Positive Only**.

    **Positive Only**
    :   Removes any negative values from the results, which can be used as a post-processing step after a derivative.

    **Series Agg**
    :   Applies a function to all of the **Group by** series to reduce the values to a single number. This function must always be the last metric in the series. For example, if the **Time Series** visualization shows 10 series, the sum **Series Agg** calculates the sum of all 10 bars and outputs a single Y value per X value. This is often confused with the overall sum function, which outputs a single Y value per unique series.

    **Math**
    :   For each series, apply simple and advanced calculations. Only use **Math** for the last function in a series.

2. To display each group separately, select one of the following options from the **Group by** dropdown:

    * **Filters** — Groups the data into the specified filters. To differentiate the groups, assign a color to each filter.
    * **Terms** — Displays the top values of the field. The color is only configurable in the **Time Series** chart. To configure, click **Options**, then select an option from the **Split color theme** dropdown.

3. Click **Options**, then configure the inputs for the function. For example, to use a different field format, make a selection from the **Data formatter** dropdown.


#### TSVB visualization options [configure-the-visualizations]

The configuration options differ for each **TSVB** visualization.


##### Time Series [tsvb-time-series]

By default, the y-axis displays the full range of data, including zero. To automatically scale the y-axis from the minimum to maximum values of the data, click **Data > Options > Fill**, then enter `0` in the **Fill** field. You can add annotations to the x-axis based on timestamped documents in a separate {{es}} index.


##### All chart types except Time Series [all-chart-types-except-time-series]

The **Data timerange mode** dropdown in **Panel options** controls the timespan that **TSVB** uses to match documents. **Last value** is unable to match all documents, only the specific interval. **Entire timerange** matches all documents specified in the time filter.


##### Metric, Top N, and Gauge [metric-topn-gauge]

**Color rules** in **Panel options** contains conditional coloring based on the values.


##### Top N and Table [topn-table]

When you click a series, **TSVB** applies a filter based on the series name. To change this behavior, click **Panel options**, then specify a URL in the **Item URL** field, which opens a URL instead of applying a filter on click.


##### Markdown [tsvb-markdown]

The **Markdown** visualization supports Markdown with Handlebar (mustache) syntax to insert dynamic data, and supports custom CSS.


#### Open and edit TSVB visualizations in Lens [edit-visualizations-in-lens]

When you open **TSVB** visualizations in **Lens**, all configuration options and annotations appear in the **Lens** visualization editor.

You can open the following **TSVB** visualizations in **Lens**:

* Time Series
* Metric
* Top N
* Gauge
* Table

To get started, click **Edit visualization in Lens** in the toolbar.

For more information, check out [Create visualizations with Lens](lens.md).


#### View the visualization data requests [view-data-and-requests-tsvb]

View the requests that collect the visualization data.

1. In the toolbar, click **Inspect**.
2. From the **Request** dropdown, select the series you want to view.


#### Save and add the panel [save-the-tsvb-panel]

Save the panel to the **Visualize Library** and add it to the dashboard, or add it to the dashboard without saving.

To save the panel to the **Visualize Library**:

1. Click **Save to library**.
2. Enter the **Title** and add any applicable [**Tags**](../find-and-organize/tags.md).
3. Make sure that **Add to Dashboard after saving** is selected.
4. Click **Save and return**.

To save the panel to the dashboard:

1. Click **Save and return**.
2. Add an optional title to the panel.

    1. In the panel header, click **No Title**.
    2. On the **Panel settings** window, select **Show title**.
    3. Enter the **Title**, then click **Save**.



#### Frequently asked questions [tsvb-faq]

For answers to frequently asked **TSVB** question, review the following.

::::{dropdown} **How do I create dashboard drilldowns for Top N and Table visualizations?**
:name: how-do-i-create-dashboard-drilldowns

You can create dashboard drilldowns that include the specified time range for **Top N** and **Table** visualizations.

1. Open the dashboard that you want to link to, then copy the URL.
2. Open the dashboard with the **Top N** and **Table** visualization panel, then click **Edit** in the toolbar.
3. Open the **Top N** or **Table** panel menu, then select **Edit visualization**.
4. Click **Panel options**.
5. In the **Item URL** field, enter the URL.

    For example `dashboards#/view/f193ca90-c9f4-11eb-b038-dd3270053a27`.

6. Click **Save and return**.
7. In the toolbar, click **Save as**, then make sure **Store time with dashboard** is deselected.

::::


::::{dropdown} **How do I base drilldown URLs on my data?**
:name: how-do-i-base-drilldowns-on-data

You can build drilldown URLs dynamically with your visualization data.

Do this by adding the `{{key}}` placeholder to your URL

For example `https://example.org/{{key}}`

This instructs TSVB to substitute the value from your visualization wherever it sees `{{key}}`.

If your data contain reserved or invalid URL characters such as "#" or "&", you should apply a transform to URL-encode the key like this `{{encodeURIComponent key}}`. If you are dynamically constructing a drilldown to another location in Kibana (for example, clicking a table row takes to you a value-scoped Discover session), you will likely want to Rison-encode your key as it may contain invalid Rison characters. ([Rison](https://github.com/Nanonid/rison#rison---compact-data-in-uris) is the serialization format many parts of Kibana use to store information in their URL.)

For example: `discover#/view/0ac50180-82d9-11ec-9f4a-55de56b00cc0?_a=(filters:!((query:(match_phrase:(foo.keyword:{{rison key}})))))`

If both conditions apply, you can cover all cases by applying both transforms: `{{encodeURIComponent (rison key)}}`.

Technical note: TSVB uses [Handlebars](https://handlebarsjs.com/) to perform these interpolations. `rison` and `encodeURIComponent` are custom Handlebars helpers provided by Kibana.

::::


::::{dropdown} **Why is my TSVB visualization missing data?**
:name: why-is-my-tsvb-visualiztion-missing-data

It depends, but most often there are two causes:

* For **Time series** visualizations with a derivative function, the time interval can be too small. Derivatives require sequential values.
* For all other **TSVB** visualizations, the cause is probably the **Data timerange mode**, which is controlled by **Panel options > Data timerange mode > Entire time range**. By default, **TSVB** displays the last whole bucket. For example, if the time filter is set to **Last 24 hours**, and the current time is 9:41, **TSVB** displays only the last 10 minutes — from 9:30 to 9:40.

::::


::::{dropdown} **How do I calculate the difference between two data series?**
:name: how-do-i-calculate-the-difference-between-two-data-series

Performing math across data series is unsupported in **TSVB**. To calculate the difference between two data series, use [**Timelion**](#timelion) or [**Vega**](custom-visualizations-with-vega.md).

::::


::::{dropdown} **How do I compare the current versus previous month?**
:name: how-do-i-compare-the-current-versus-previous-month

**TSVB** can display two series with time offsets, but it can’t perform math across series. To add a time offset:

1. Click **Clone Series**, then choose a color for the new series.

    :::{image} ../../images/kibana-tsvb_clone_series.png
    :alt: Clone Series action
    :class: screenshot
    :::

2. Click **Options**, then enter the offset value in the **Offset series time by** field.

::::


::::{dropdown} **How do I calculate a month over month change?**
:name: how-do-i-calculate-a-month-over-month-change

The ability to calculate a month over month change is not fully supported in **TSVB**, but there is a special case that is supported *if* the time filter is set to 3 months or more *and* the **Interval** is `1m`. Use the **Derivative** to get the absolute monthly change. To convert to a percent, add the **Math** function with the `params.current / (params.current - params.derivative)` formula, then select **Percent** from the **Data Formatter** dropdown.

For other types of month over month calculations, use [**Timelion**](#timelion) or [**Vega**](custom-visualizations-with-vega.md).

::::


::::{dropdown} **How do I calculate the duration between the start and end of an event?**
:name: calculate-duration-start-end

Calculating the duration between the start and end of an event is unsupported in **TSVB** because **TSVB** requires correlation between different time periods. **TSVB** requires that the duration is pre-calculated.

::::



## Timelion [timelion]

To use **Timelion**, you define a graph by chaining functions together, using the **Timelion**-specific syntax. The syntax enables some features that classical point series charts don’t offer, such as pulling data from different indices or data sources into one graph.

**Timelion** is driven by a simple expression language that you use to:

* Retrieve time series data from one or more indices
* Perform math across two or more time series
* Visualize the results

![Timelion](../../images/kibana-timelion.png "")


#### Timelion expressions [_timelion_expressions]

Timelion functions always start with a dot, followed by the function name, followed by parentheses containing all the parameters to the function.

The `.es` (or `.elasticsearch` if you are a fan of typing long words) function gathers data from {{es}} and draws it over time. By default the .es function will just count the number of documents, resulting in a graph showing the amount of documents over time.


#### Function parameters [_function_parameters]

Functions can have multiple parameters, and so does the `.es` function. Each parameter has a name, that you can use inside the parentheses to set its value. The parameters also have an order, which is shown by the autocompletion or the documentation (using the Docs button in the top menu).

If you don’t specify the parameter name, timelion assigns the values to the parameters in the order, they are listed in the documentation.

The fist parameter of the .es function is the parameter q (for query), which is a Query String used to filter the data for this series. You can also explicitly reference this parameter by its name, and I would always recommend doing so as soon as you are passing more than one parameter to the function. The following two expressions are thus equivalent:

Multiple parameters are separated by a comma. The .es function has another parameter called index, that can be used to specify a {{data-source}} for this series, so the query won’t be executed against all indexes (or whatever you changed the setting to).

If the value of your parameter contains spaces or commas you have to put the value in single or double quotes. You can omit these quotes otherwise.


##### .yaxis() function [customize-data-series-y-axis]

{{kib}} supports many y-axis scales and ranges for your data series.

The `.yaxis()` function supports the following parameters:

* **yaxis** — The numbered y-axis to plot the series on. For example, use `.yaxis(2)` to display a second y-axis.
* **min** — The minimum value for the y-axis range.
* **max** — The maximum value for the y-axis range.
* **position** — The location of the units. Values include `left` or `right`.
* **label** — The label for the axis.
* **color** — The color of the axis label.
* **units** — The function to use for formatting the y-axis labels. Values include `bits`, `bits/s`, `bytes`, `bytes/s`, `currency(:ISO 4217 currency code)`, `percent`, and `custom(:prefix:suffix)`.
* **tickDecimals** — The tick decimal precision.

Example:

```text
.es(index= kibana_sample_data_logs,
    timefield='@timestamp',
    metric='avg:bytes')
  .label('Average Bytes for request')
  .title('Memory consumption over time in bytes').yaxis(1,units=bytes,position=left), <1>
.es(index= kibana_sample_data_logs,
    timefield='@timestamp',
    metric=avg:machine.ram)
  .label('Average Machine RAM amount').yaxis(2,units=bytes,position=right) <2>
```

1. `.yaxis(1,units=bytes,position=left)` — Specifies the first y-axis for the first data series, and changes the units on the left.
2. `.yaxis(2,units=bytes,position=left)` — Specifies the second y-axis for the second data series, and changes the units on the right.



### Tutorial: Create visualizations with Timelion [_tutorial_create_visualizations_with_timelion]

You collected data from your operating system using Metricbeat, and you want to visualize and analyze the data on a dashboard. To create panels of the data, use **Timelion** to create a time series visualization,


#### Add the data and create the dashboard [_add_the_data_and_create_the_dashboard_2]

Set up Metricbeat, then create the dashboard.

1. To set up Metricbeat, go to [Metricbeat quick start: installation and configuration](https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-installation-configuration.html)
2. Go to **Dashboards**.
3. On the **Dashboards** page, click **Create dashboard**.


#### Open and set up Timelion [_open_and_set_up_timelion]

Open **Timelion** and change the time range.

1. On the dashboard, click **All types > Aggregation based**, then select **Timelion**.
2. Make sure the [time filter](../query-filter/filtering.md) is **Last 7 days**.


#### Create a time series visualization [timelion-tutorial-create-time-series-visualizations]

To compare the real-time percentage of CPU time spent in user space to the results offset by one hour, create a time series visualization.


##### Define the functions [define-the-functions]

To track the real-time percentage of CPU, enter the following in the **Timelion Expression** field, then click **Update**:

```text
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='avg:system.cpu.user.pct')
```


##### Compare the data [compare-the-data]

To compare two data sets, add another series, and offset the data back by one hour, then click **Update**:

```text
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='avg:system.cpu.user.pct'),
.es(offset=-1h,
    index=metricbeat-*,
    timefield='@timestamp',
    metric='avg:system.cpu.user.pct')
```


##### Add label names [add-label-names]

To easily distinguish between the two data sets, add label names, then click **Update**:

```text
.es(offset=-1h,index=metricbeat-*,
    timefield='@timestamp',
    metric='avg:system.cpu.user.pct').label('last hour'),
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='avg:system.cpu.user.pct').label('current hour')
```


##### Add a title [add-a-title]

To make is easier for unfamiliar users to understand the purpose of the visualization, add a title, then click **Update**:

```text
.es(offset=-1h,
    index=metricbeat-*,
    timefield='@timestamp',
    metric='avg:system.cpu.user.pct')
  .label('last hour'),
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='avg:system.cpu.user.pct')
  .label('current hour')
  .title('CPU usage over time')
```


##### Change the appearance of the chart lines [change-the-chart-type]

To differentiate between the current hour and the last hour, change the appearance of the chart lines, then click **Update**:

```text
.es(offset=-1h,
    index=metricbeat-*,
    timefield='@timestamp',
    metric='avg:system.cpu.user.pct')
  .label('last hour')
  .lines(fill=1,width=0.5),
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='avg:system.cpu.user.pct')
  .label('current hour')
  .title('CPU usage over time')
```


##### Change the line colors [change-the-line-colors]

**Timelion** supports standard color names, hexadecimal values, or a color schema for grouped data.

To make the first data series stand out, change the line colors, then click **Update**:

```text
.es(offset=-1h,
    index=metricbeat-*,
    timefield='@timestamp',
    metric='avg:system.cpu.user.pct')
  .label('last hour')
  .lines(fill=1,width=0.5)
  .color(gray),
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='avg:system.cpu.user.pct')
  .label('current hour')
  .title('CPU usage over time')
  .color(#1E90FF)
```


##### Adjust the legend [make-adjustments-to-the-legend]

Move the legend to the north west position  with two columns, then click **Update**:

```text
.es(offset=-1h,
    index=metricbeat-*,
    timefield='@timestamp',
    metric='avg:system.cpu.user.pct')
  .label('last hour')
  .lines(fill=1,width=0.5)
  .color(gray),
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='avg:system.cpu.user.pct')
  .label('current hour')
  .title('CPU usage over time')
  .color(#1E90FF)
  .legend(columns=2, position=nw)
```

:::{image} ../../images/kibana-timelion-customize04.png
:alt: Final time series visualization
:class: screenshot
:::

 


##### Save and add the panel [save-the-timelion-panel]

Save the panel to the **Visualize Library** and add it to the dashboard, or add it to the dashboard without saving.

To save the panel to the **Visualize Library**:

1. Click **Save to library**.
2. Enter the **Title** and add any applicable [**Tags**](../find-and-organize/tags.md).
3. Make sure that **Add to Dashboard after saving** is selected.
4. Click **Save and return**.

To save the panel to the dashboard:

1. Click **Save and return**.
2. Add an optional title to the panel.

    1. In the panel header, click **No Title**.
    2. On the **Panel settings** window, select **Show title**.
    3. Enter the **Title**, then click **Save**.



### Visualize the inbound and outbound network traffic [timelion-tutorial-create-visualizations-with-mathematical-functions]

To create a visualization for inbound and outbound network traffic, use mathematical functions.


#### Define the functions [mathematical-functions-define-functions]

To start tracking the inbound and outbound network traffic, enter the following in the **Timelion Expression** field, then click **Update**:

```text
.es(index=metricbeat*,
    timefield=@timestamp,
    metric=max:system.network.in.bytes)
```


#### Plot the rate of change [mathematical-functions-plot-change]

To easily monitor the inbound traffic, plots the change in values over time, then click **Update**:

```text
.es(index=metricbeat*,
    timefield=@timestamp,
    metric=max:system.network.in.bytes)
  .derivative()
```

Add a similar calculation for outbound traffic, then click **Update**:

```text
.es(index=metricbeat*,
    timefield=@timestamp,
    metric=max:system.network.in.bytes)
  .derivative(),
.es(index=metricbeat*,
    timefield=@timestamp,
    metric=max:system.network.out.bytes)
  .derivative()
  .multiply(-1) <1>
```

1. `.multiply(-1)` converts the outbound network traffic to a negative value since the outbound network traffic is leaving your machine. `.multiply()` multiplies the data series by a number, the result of a data series, or a list of data series.



#### Change the data metric [mathematical-functions-convert-data]

To make the data easier to analyze, change the data metric from `bytes` to `megabytes`, then click **Update**:

```text
.es(index=metricbeat*,
    timefield=@timestamp,
    metric=max:system.network.in.bytes)
  .derivative()
  .divide(1048576),
.es(index=metricbeat*,
    timefield=@timestamp,
    metric=max:system.network.out.bytes)
  .derivative()
  .multiply(-1)
  .divide(1048576) <1>
```

1. `.divide()` accepts the same input as `.multiply()`, then divides the data series by the defined divisor.



#### Customize and format the visualization [mathematical-functions-add-labels]

Customize and format the visualization using the following functions, then click **Update**:

```text
.es(index=metricbeat*,
    timefield=@timestamp,
    metric=max:system.network.in.bytes)
  .derivative()
  .divide(1048576)
  .lines(fill=2, width=1)
  .color(green)
  .label("Inbound traffic")
  .title("Network traffic (MB/s)"),
.es(index=metricbeat*,
    timefield=@timestamp,
    metric=max:system.network.out.bytes)
  .derivative()
  .multiply(-1)
  .divide(1048576)
  .lines(fill=2, width=1)
  .color(blue)
  .label("Outbound traffic")
  .legend(columns=2, position=nw)
```

:::{image} ../../images/kibana-timelion-math05.png
:alt: Final visualization that displays inbound and outbound network traffic
:class: screenshot
:::

 


##### Save and add the panel [save-the-network-timelion-panel]

Save the panel to the **Visualize Library** and add it to the dashboard, or add it to the dashboard without saving.

To save the panel to the **Visualize Library**:

1. Click **Save to library**.
2. Enter the **Title** and add any applicable [**Tags**](../find-and-organize/tags.md).
3. Make sure that **Add to Dashboard after saving** is selected.
4. Click **Save and return**.

To save the panel to the dashboard:

1. Click **Save and return**.
2. Add an optional title to the panel.

    1. In the panel header, click **No Title**.
    2. On the **Panel settings** window, select **Show title**.
    3. Enter the **Title**, then click **Save**.



#### Detect outliers and discover patterns over time [timelion-tutorial-create-visualizations-withconditional-logic-and-tracking-trends]

To easily detect outliers and discover patterns over time, modify the time series data with conditional logic and create a trend with a moving average.

With **Timelion** conditional logic, you can use the following operator values to compare your data:

`eq`
:   equal

`ne`
:   not equal

`lt`
:   less than

`lte`
:   less than or equal to

`gt`
:   greater than

`gte`
:   greater than or equal to


##### Define the functions [conditional-define-functions]

To chart the maximum value of `system.memory.actual.used.bytes`, enter the following in the **Timelion Expression** field, then click **Update**:

```text
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='max:system.memory.actual.used.bytes')
```


##### Track used memory [conditional-track-memory]

To track the amount of memory used, create two thresholds, then click **Update**:

```text
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='max:system.memory.actual.used.bytes'),
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='max:system.memory.actual.used.bytes')
  .if(gt,                             <1>
      11300000000,                    <2>
      .es(index=metricbeat-*,
          timefield='@timestamp',
          metric='max:system.memory.actual.used.bytes'),
      null)
    .label('warning')
    .color('#FFCC11'),
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='max:system.memory.actual.used.bytes')
  .if(gt,
      11375000000,
      .es(index=metricbeat-*,
          timefield='@timestamp',
          metric='max:system.memory.actual.used.bytes'),
      null)
  .label('severe')
  .color('red')
```

1. `if()` compares each point to a number. When the condition is `true`, adjust the styling. When the condition is `false`, use the default styling.
2. **Timelion** conditional logic for the *greater than* operator. In this example, the warning threshold is 11.3GB (`11300000000`), and the severe threshold is 11.375GB (`11375000000`). If the threshold values are too high or low for your machine, adjust the values.



##### Determine the trend [conditional-determine-trend]

To determine the trend, create a new data series, then click **Update**:

```text
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='max:system.memory.actual.used.bytes'),
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='max:system.memory.actual.used.bytes')
  .if(gt,11300000000,
      .es(index=metricbeat-*,
          timefield='@timestamp',
          metric='max:system.memory.actual.used.bytes'),
      null)
      .label('warning')
      .color('#FFCC11'),
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='max:system.memory.actual.used.bytes')
  .if(gt,11375000000,
      .es(index=metricbeat-*,
          timefield='@timestamp',
          metric='max:system.memory.actual.used.bytes'),
      null).
      label('severe')
      .color('red'),
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='max:system.memory.actual.used.bytes')
  .mvavg(10) <1>
```

1. `mvavg()` calculates the moving average over a specified period of time. In this example, `.mvavg(10)` creates a moving average with a window of 10 data points.



##### Customize and format the visualization [conditional-format-visualization]

Customize and format the visualization using the following functions, then click **Update**:

```text
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='max:system.memory.actual.used.bytes')
  .label('max memory')
  .title('Memory consumption over time'),
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='max:system.memory.actual.used.bytes')
  .if(gt,
      11300000000,
      .es(index=metricbeat-*,
          timefield='@timestamp',
          metric='max:system.memory.actual.used.bytes'),
      null)
    .label('warning')
    .color('#FFCC11')
    .lines(width=5),
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='max:system.memory.actual.used.bytes')
  .if(gt,
      11375000000,
      .es(index=metricbeat-*,
          timefield='@timestamp',
          metric='max:system.memory.actual.used.bytes'),
      null)
    .label('severe')
    .color('red')
    .lines(width=5),
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='max:system.memory.actual.used.bytes')
  .mvavg(10)
  .label('mvavg')
  .lines(width=2)
  .color(#5E5E5E)
  .legend(columns=4, position=nw)
```

:::{image} ../../images/kibana-timelion-conditional04.png
:alt: Final visualization that displays outliers and patterns over time
:class: screenshot
:::

 


##### Save and add the panel [save-the-outlier-timelion-panel]

Save the panel to the **Visualize Library** and add it to the dashboard, or add it to the dashboard without saving.

To save the panel to the **Visualize Library**:

1. Click **Save to library**.
2. Enter the **Title** and add any applicable [**Tags**](../find-and-organize/tags.md).
3. Make sure that **Add to Dashboard after saving** is selected.
4. Click **Save and return**.

To save the panel to the dashboard:

1. Click **Save and return**.
2. Add an optional title to the panel.

    1. In the panel header, click **No Title**.
    2. On the **Panel settings** window, select **Show title**.
    3. Enter the **Title**, then click **Save**.


For more information about **Timelion** conditions, refer to [I have but one .condition()](https://www.elastic.co/blog/timeseries-if-then-else-with-timelion).
