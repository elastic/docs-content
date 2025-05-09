---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/exploratory-data-visualizations.html
applies_to:
  stack: all
  serverless:
    observability: all
products:
  - id: observability
---

# Explore data [exploratory-data-visualizations]

The **Explore data** view in {{kib}} enables you to select and filter result data in any dimension, and look for the cause or impact of performance problems.

Based on your synthetic monitoring, user experience, and mobile experience data, you can create multi-series visualizations of performance and device distributions, key performance indicators (KPI) over time, and core web vitals of your web applications.

:::{image} /troubleshoot/images/observability-exploratory-view.png
:alt: Explore {{data-source}} for Monitor duration
:screenshot:
:::


## Explore {{data-source}} [explore-data-view]

You can use the Explore {{data-source}} to filter your data and build multi-series visualizations that help you clarify what’s essential, and examine the cause or impact of performance difficulties. You can compare different time periods, different cohorts, and even different data types.

Hover over the chart to display crosshairs with specific metric data. To drill down into a specific time period, click and drag a selection then click **Apply changes**.

To add visualizations to an existing case, click **Add to case** from the toolbar.

To customize a visualization further, click **Open in Lens** from the toolbar to modify visualizations with the drag and drop editor. To learn more, see [Lens](../../explore-analyze/visualize/lens.md).


## What report types are available? [report-types]

| Report type | Description |
| --- | --- |
| KPI over time | The KPI over time histogram represents the performance indicators based on themetric you select, such as page views or monitor duration. |
| Performance distribution | The Performance distribution time-series chart enables you to examine theperceived performance of your web applications based on the metric you select. |
| Core web vitals | The Core web vitals chart is a graphical representation of key metrics, such asloading performance, load responsiveness, and visual stability, for each of yourweb applications.<br>To learn more about metrics such as Largest contentful paint, Interaction to next paint,and Cumulative layout shift, see [{{user-experience}} metrics](/solutions/observability/applications/user-experience.md#user-experience-metrics). |
| Device distribution | The Device distribution chart displays device information such as OS, carrier name, and connection type. |

For a breakdown of which data types are available for which reports, see [What data types can I explore?](#data-types)

You can create multi-series visualizations for each report type, but you cannot combine different report types in one visualization. To change the report type for your visualization, click **Remove series** and then **Add series**.


## Create multi-series visualizations [create-multi-series-visualizations]

The Explore {{data-source}} is currently enabled for the following apps:

* Uptime
* {{user-experience}}

To create a multi-series visualization:

1. Click **Explore data** from a compatible app.

    * The report type will default to the most appropriate for the app, but you can edit the series or add more series to the visualization. For example, if you click **Explore Data** from the {{uptime-app}}, the `Synthetics monitoring` data type and `Monitor duration` report metric will be preselected.

2. Click **Add series** to define an additional series for the visualization.
3. Click **Select data type** and choose from the following options:

    * Synthetics monitoring
    * User experience (RUM)
    * Mobile experience

4. Click **Select report metric** and select the options and filters you need. You will see a **Missing…​** warning if required fields (highlighted with red underline) are incomplete.
5. Click **Apply changes** to see the updated visualization, or repeat the **Add series** process to expand the visualization.
6. To add the visualization to an existing case, click **Add to case** and select the correct case.


## Synthetic Monitoring [explore-data-synthetics]

Based on the Uptime data you are sending to your deployment, you can create various visualizations relating to monitor durations, pings over time, or any of the [available data types](#data-types).

:::{image} /troubleshoot/images/observability-exploratory-view-uptime.png
:alt: Explore data for Uptime
:screenshot:
:::

|     |     |
| --- | --- |
| **Monitor duration** | The Uptime monitor duration time-series chart displays the timing for each check that {{heartbeat}} performed.<br>This visualization helps you to gain insights into how quickly requests resolve by the targeted endpointand give you a sense of how frequently a host or endpoint was down in your selected time span. |
| **Pings histogram** | The Uptime pings chart is a graphical representation of the check statuses over time. |


## {{user-experience}} [explore-data-user-experience]

Based on the {{user-experience}} data from your instrumented applications, you can create detailed visualizations for performance distributions, key performance indicators (KPI) over time, and for core web vitals of your web applications.

:::{image} /troubleshoot/images/observability-exploratory-view-ux-page-load-time.png
:alt: Explore data for {{user-experience}} (page load time)
:screenshot:
:::

|     |     |
| --- | --- |
| **KPI over time** | The KPI over time histogram represents the performance indicators based onthe metric you select.<br>By default, the `Page views` metric is selected. |
| **Performance distribution** | The Performance distribution time-series chart enables you to examine the perceivedperformance of your web applications based on the metric you select.<br>By default, the `Page load time` metric is selected. |
| **Core web vitals** | The Core web vitals chart is a graphical representation of key metrics, such asload performance, load responsiveness, and visual stability, for each of your web applications.<br>By default, the `Largest contentful paint` metric is selected. Hover over the chart to display crosshairswith performance indicators for each web application: `poor`, `average`, and `good`. |


## What data types can I explore? [data-types]

The following table shows which data types are available for each report type:

| Data type | Synthetics monitoring | User experience (RUM) | Mobile experience |
| --- | --- | --- | --- |
| Monitor duration | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |  |  |
| Up Pings | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |  |  |
| Down Pings | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |  |  |
| Step duration | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |  |  |
| DOM content loaded | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |  |  |
| Document complete (onLoad) | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |  |  |
| Largest contentful paint | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |  |
| First contentful paint | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |  |
| Page load time | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |  |
| Cumulative layout shift | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |  |
| Page views |  | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |  |
| Backend time |  | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |  |
| Total blocking time |  | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |  |
| Interaction to next paint |  | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |  |
| Latency |  |  | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| Throughput |  |  | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| System memory usage |  |  | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| CPU usage |  |  | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| Number of devices |  |  | ![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png "") |
| System CPU usage |  |  |  |
| Docker CPU usage |  |  |  |
| K8s pod CPU usage |  |  |  |

