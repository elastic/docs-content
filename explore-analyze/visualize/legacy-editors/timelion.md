---
description: Query time series data with Timelion expression language. Pull data from multiple indices, perform cross-series math, and visualize results with chained functions.
applies_to:
  stack: deprecated 7.10
  serverless: unavailable
products:
  - id: kibana
---
  
# Timelion [timelion]

Timelion is a time series visualization tool that uses an expression language to define charts through chained functions. While deprecated since version 7.10, it remains available in some deployments for existing visualizations. For new work, use Lens or TSVB instead.

Timelion's expression language lets you query multiple indices, perform mathematical operations across time series, and combine data sources in ways that standard visualizations don't support. You build visualizations by chaining functions together with a simple dot notation.

**Timelion** is driven by a simple expression language that you use to:

* Retrieve time series data from one or more indices
* Perform math across two or more time series
* Visualize the results

![Timelion](/explore-analyze/images/kibana-timelion.png "")


## Timelion expressions [_timelion_expressions]

Timelion functions always start with a dot, followed by the function name, followed by parentheses containing all the parameters to the function.

The `.es` (or `.elasticsearch` if you are a fan of typing long words) function gathers data from {{es}} and draws it over time. By default the .es function will just count the number of documents, resulting in a graph showing the amount of documents over time.


## Function parameters [_function_parameters]

Functions can have multiple parameters, and so does the `.es` function. Each parameter has a name, that you can use inside the parentheses to set its value. The parameters also have an order, which is shown by the autocompletion or the documentation (using the Docs button in the top menu).

If you don’t specify the parameter name, timelion assigns the values to the parameters in the order, they are listed in the documentation.

The fist parameter of the .es function is the parameter q (for query), which is a Query String used to filter the data for this series. You can also explicitly reference this parameter by its name, and I would always recommend doing so as soon as you are passing more than one parameter to the function. The following two expressions are thus equivalent:

Multiple parameters are separated by a comma. The .es function has another parameter called index, that can be used to specify a {{data-source}} for this series, so the query won’t be executed against all indexes (or whatever you changed the setting to).

If the value of your parameter contains spaces or commas you have to put the value in single or double quotes. You can omit these quotes otherwise.


### .yaxis() function [customize-data-series-y-axis]

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



## Tutorial: Create visualizations with Timelion [_tutorial_create_visualizations_with_timelion]

You collected data from your operating system using Metricbeat, and you want to visualize and analyze the data on a dashboard. To create panels of the data, use **Timelion** to create a time series visualization,


## Add the data and create the dashboard [_add_the_data_and_create_the_dashboard_2]

Set up Metricbeat, then create the dashboard.

1. To set up Metricbeat, go to [Metricbeat quick start: installation and configuration](beats://reference/metricbeat/metricbeat-installation-configuration.md)
2. Go to **Dashboards**.
3. On the **Dashboards** page, click **Create dashboard**.

You can only add Timelion visualizations to a dashboard if they're already saved in the **Visualize Library**, using the **Add from library** option.

## Create a Timelion visualization [_open_and_set_up_timelion]

$$$timelion-tutorial-create-time-series-visualizations$$$

1. Go to the **Visualize Library** and select **Create visualization**.
2. In the **Legacy** tab, select **Aggregation-based**, then **Timelion**.
3. Make sure the [time filter](../../query-filter/filtering.md) is **Last 7 days**.

### Define the functions [define-the-functions]

To track the real-time percentage of CPU, enter the following in the **Timelion Expression** field, then click **Update**:

```text
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='avg:system.cpu.user.pct')
```


### Compare the data [compare-the-data]

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


### Add label names [add-label-names]

To easily distinguish between the two data sets, add label names, then click **Update**:

```text
.es(offset=-1h,index=metricbeat-*,
    timefield='@timestamp',
    metric='avg:system.cpu.user.pct').label('last hour'),
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='avg:system.cpu.user.pct').label('current hour')
```


### Add a title [add-a-title]

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


### Change the appearance of the chart lines [change-the-chart-type]

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


### Change the line colors [change-the-line-colors]

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


### Adjust the legend [make-adjustments-to-the-legend]

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

:::{image} /explore-analyze/images/kibana-timelion-customize04.png
:alt: Final time series visualization
:screenshot:
:::

 


### Save and add the panel [save-the-timelion-panel]

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



## Visualize the inbound and outbound network traffic [timelion-tutorial-create-visualizations-with-mathematical-functions]

To create a visualization for inbound and outbound network traffic, use mathematical functions.


## Define the functions [mathematical-functions-define-functions]

To start tracking the inbound and outbound network traffic, enter the following in the **Timelion Expression** field, then click **Update**:

```text
.es(index=metricbeat*,
    timefield=@timestamp,
    metric=max:system.network.in.bytes)
```


## Plot the rate of change [mathematical-functions-plot-change]

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



## Change the data metric [mathematical-functions-convert-data]

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



## Customize and format the visualization [mathematical-functions-add-labels]

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

:::{image} /explore-analyze/images/kibana-timelion-math05.png
:alt: Final visualization that displays inbound and outbound network traffic
:screenshot:
:::

 


### Save and add the panel [save-the-network-timelion-panel]

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



## Detect outliers and discover patterns over time [timelion-tutorial-create-visualizations-withconditional-logic-and-tracking-trends]

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


### Define the functions [conditional-define-functions]

To chart the maximum value of `system.memory.actual.used.bytes`, enter the following in the **Timelion Expression** field, then click **Update**:

```text
.es(index=metricbeat-*,
    timefield='@timestamp',
    metric='max:system.memory.actual.used.bytes')
```


### Track used memory [conditional-track-memory]

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



### Determine the trend [conditional-determine-trend]

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



### Customize and format the visualization [conditional-format-visualization]

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

:::{image} /explore-analyze/images/kibana-timelion-conditional04.png
:alt: Final visualization that displays outliers and patterns over time
:screenshot:
:::

 


### Save and add the panel [save-the-outlier-timelion-panel]

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


For more information about **Timelion** conditions, refer to [I have but one .condition()](https://www.elastic.co/blog/timeseries-if-then-else-with-timelion).
