---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/analyze-hosts.html
  - https://www.elastic.co/guide/en/serverless/current/observability-analyze-hosts.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Analyze and compare hosts [observability-analyze-hosts]

We’d love to get your feedback! [Tell us what you think!](https://docs.google.com/forms/d/e/1FAIpQLScRHG8TIVb1Oq8ZhD4aks3P1TmgiM58TY123QpDCcBz83YC6w/viewform)

The **Hosts** page provides a metrics-driven view of your infrastructure backed by an easy-to-use interface called Lens. On the **Hosts** page, you can view health and performance metrics to help you quickly:

* Analyze and compare hosts without having to build new dashboards.
* Identify which hosts trigger the most alerts.
* Troubleshoot and resolve issues quickly.
* View historical data to rule out false alerts and identify root causes.
* Filter and search the data to focus on the hosts you care about the most.

To access the **Hosts** page in:
- **Elastic Stack,** find **Infrastructure** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
- **Serverless,** go to **Infrastructure → Hosts** in your Elastic Observability Serverless project.

:::{image} /solutions/images/serverless-hosts.png
:alt: Screenshot of the Hosts page
:screenshot:
:::

To learn more about the metrics shown on this page, refer to the [Metrics reference](/reference/observability/metrics-reference.md) documentation.

::::{note}
**Don’t see any metrics?**


If you haven’t added data yet, click **Add data → Host** and select how you want to monitor your host—OpenTelemetry or Elastic Agent.

For more on collecting host data, refer to:
* [OpenTelemetry](elastic-agent://reference/edot-collector/config/configure-metrics-collection.md#process-metrics)
* [Elastic System integration](integration-docs://reference/system.md)

::::


The **Hosts** page provides several ways to view host metrics:

* Overview tiles show the number of hosts returned by your search plus averages of key metrics, including CPU usage, normalized load, and memory usage. Max disk usage is also shown.
* The Host limit controls the maximum number of hosts shown on the page. The default is 50, which means the page shows data for the top 50 hosts based on the most recent timestamps. You can increase the host limit to see data for more hosts, but doing so may impact query performance.
* The Hosts table shows a breakdown of metrics for each host along with an alert count for any hosts with active alerts. You may need to page through the list or change the number of rows displayed on each page to see all of your hosts.
* Each host name is an active link to a [host details](/solutions/observability/infra-and-hosts/analyze-compare-hosts.md#view-host-details) page, where you can explore enhanced metrics and other observability data related to the selected host.
* Table columns are sortable, but note that the sorting behavior is applied to the already returned data set.
* The tabs at the bottom of the page show an overview of the metrics, logs, and alerts for all hosts returned by your search.

::::{tip}
For more information about creating and viewing alerts, refer to [Alerting](/solutions/observability/incident-management/alerting.md).

::::



## Filter the Hosts view [analyze-hosts-filter-view]

The **Hosts** page provides several mechanisms for filtering the data on the page:

* Enter a search query using [{{kib}} Query Language](/explore-analyze/query-filter/languages/kql.md) to show metrics that match your search criteria. For example, to see metrics for hosts running on linux, enter `host.os.type : "linux"`. Otherwise you’ll see metrics for all your monitored hosts (up to the number of hosts specified by the host limit).
* Select additional criteria to filter the view:

    * In the **Operating System** list, select one or more operating systems to include (or exclude) metrics for hosts running the selected operating systems.
    * In the **Cloud Provider** list, select one or more cloud providers to include (or exclude) metrics for hosts running on the selected cloud providers.
    * In the **Service Name** list, select one or more service names to include (or exclude) metrics for the hosts running the selected services. Services must be instrumented by APM to be filterable. This filter is useful for comparing different hosts to determine whether a problem lies with a service or the host that it is running on.

        ::::{tip}
        Filtered results are sorted by *document count*. Document count is the number of events received by Elastic for the hosts that match your filter criteria.

        ::::

* Change the date range in the time filter, or click and drag on a visualization to change the date range.
* Within a visualization, click a point on a line and apply filters to set other visualizations on the page to the same time and/or host.

% Stateful only for filtering data?

To learn more about filtering data in {{kib}}, refer to [{{kib}} concepts](/explore-analyze/query-filter/filtering.md).


## View metrics [analyze-hosts-inspect-data]

On the **Metrics** tab, view metrics trending over time, including CPU usage, normalized load, memory usage, disk usage, and other metrics related to disk IOPs and throughput. Place your cursor over a line to view metrics at a specific point in time. From within each visualization, you can choose to open the visualization in Lens.

To see metrics for a specific host, refer to [View host details](/solutions/observability/infra-and-hosts/analyze-compare-hosts.md#view-host-details).


### Open in Lens [analyze-hosts-open-in-lens]

Metrics visualizations are powered by Lens, meaning you can continue your analysis in Lens if you require more flexibility. Hover your cursor over a visualization, then click the ellipsis icon in the upper-right corner to open the visualization in Lens.

:::{image} /solutions/images/serverless-hosts-open-in-lens.png
:alt: Screenshot showing option to open in Lens
:screenshot:
:::

In Lens, you can examine all the fields and formulas used to create the visualization, make modifications to the visualization, and save your changes.

For more information about using Lens, refer to the [{{kib}} documentation about Lens](/explore-analyze/visualize/lens.md).


## View logs [analyze-hosts-view-logs]

On the **Logs** tab of the **Hosts** page, view logs for the systems you are monitoring and search for specific log entries. This view shows logs for all of the hosts returned by the current query.

:::{image} /solutions/images/serverless-hosts-logs.png
:alt: Screenshot showing Logs view
:screenshot:
:::

To see logs for a specific host, refer to [View host details](/solutions/observability/infra-and-hosts/analyze-compare-hosts.md#view-host-details).

### View enhanced logs [analyze-hosts-view-enhanced-logs]
```{applies_to}
stack: preview 9.0
```

For an enhanced logs view with additional information including the log pattern, the number of events for each log, change type, and the time the change occurred, turn on the `observability:newLogsOverview` [advanced setting](kibana://reference/advanced-settings.md#kibana-search-settings).


## View alerts [analyze-hosts-view-alerts]

On the **Alerts** tab of the **Hosts** page, view active alerts to pinpoint problems. Use this view to figure out which hosts triggered alerts and identify root causes. This view shows alerts for all of the hosts returned by the current query.

From the **Actions** menu, you can choose to:

* Add the alert to a new or existing case.
* View rule details.
* View alert details.

:::{image} /solutions/images/serverless-hosts-view-alerts.png
:alt: Screenshot showing Alerts view
:screenshot:
:::

To see alerts for a specific host, refer to [View host details](/solutions/observability/infra-and-hosts/analyze-compare-hosts.md#view-host-details).

::::{note}
**Why are alerts missing from the Hosts page?**

If your rules are triggering alerts that don’t appear on the **Hosts** page, edit the rules and make sure they are correctly configured to associate the host name with the alert:

* For Metric threshold or Custom threshold rules, select `host.name` in the **Group alerts by** field.
* For Inventory rules, select **Host** for the node type under **Conditions**.

To learn more about creating and managing rules, refer to [Alerting](/solutions/observability/incident-management/alerting.md).

::::

## Select the data collection schema[host-schema-selector]
```{applies_to}
stack: ga 9.2
serverless: ga
```

The **Schema** menu shows the available data collection schemas for the current query. If host data from both the Elastic System integration and OpenTelemetry is available, the schema defaults to **OpenTelemetry**. Select **Elastic System Integration** to see host data collected by the Elastic System integration.


## View host details [view-host-details]

Without leaving the **Hosts** page, you can view enhanced metrics relating to each host running in your infrastructure. In the list of hosts, find the host you want to monitor, then click the **Toggle dialog with details** icon ![expand icon](/solutions/images/serverless-expand-icon.png "") to display the host details overlay.

{applies_to}`{stack: "ga 9.2", serverless: "ga"}` The host details overlay adapts according to the [selected schema](#host-schema-selector). When viewing host data collected using OpenTelemetry, you see the following differences:

* Anomaly detection isn't available for OpenTelemetry hosts, so there is no **Anomalies** tab.
* The Lens charts use the [OpenTelemetry field calculation formulas](/reference/observability/observability-host-metrics.md#open-telemetry-host-metrics).

::::{tip}
To expand the overlay and view more detail, click **Open as page** in the upper-right corner.

::::

The host details overlay contains the following tabs:

:::::{dropdown} Overview
The **Overview** tab displays key metrics about the selected host, such as CPU usage, normalized load, memory usage, and max disk usage.

Change the time range to view metrics over a specific period of time.

Expand each section to view more detail related to the selected host, such as metadata, active alerts, services detected on the host, and metrics.

Hover over a specific time period on a chart to compare the various metrics at that given time.

Click **Show all** to drill down into related data.

:::{image} /solutions/images/serverless-overview-overlay.png
:alt: Host overview
:screenshot:
:::

:::::


:::::{dropdown} Metadata
The **Metadata** tab lists all the meta information relating to the host, including host, cloud, and agent information.

This information can help when investigating events—for example, when filtering by operating system or architecture.

:::{image} /solutions/images/serverless-metadata-overlay.png
:alt: Host metadata
:screenshot:
:::

:::::


:::::{dropdown} Metrics
The **Metrics** tab shows host metrics organized by type and is more complete than the view available in the *Overview* tab.

:::{image} /solutions/images/serverless-metrics-overlay.png
:alt: Metrics
:screenshot:
:::

:::::


:::::{dropdown} Processes
:::{note}
{applies_to}`{stack: "ga 9.2", serverless: "ga"}`
To view processes for OpenTelemetry hosts, you need to configure the EDOT collector to send process metrics. Refer to [Process metrics](elastic-agent://reference/edot-collector/config/configure-metrics-collection.md#process-metrics) for more information.
:::

The **Processes** tab lists the total number of processes (`system.process.summary.total`) running on the host, along with the total number of processes in these various states:

* Running (`system.process.summary.running`)
* Sleeping (`system.process.summary.sleeping`)
* Stopped (`system.process.summary.stopped`)
* Idle (`system.process.summary.idle`)
* Dead (`system.process.summary.dead`)
* Zombie (`system.process.summary.zombie`)
* Unknown (`system.process.summary.unknown`)

The processes listed in the **Top processes** table are based on an aggregation of the top CPU and the top memory consuming processes. The number of top processes is controlled by `process.include_top_n.by_cpu` and `process.include_top_n.by_memory`.

|  |  |
| --- | --- |
| **Command** | Full command line that started the process, including the absolute path to the executable, and all the arguments (`system.process.cmdline`). |
| **PID** | Process id (`process.pid`). |
| **User** | User name (`user.name`). |
| **CPU** | The percentage of CPU time spent by the process since the last event (`system.process.cpu.total.pct`). |
| **Time** | The time the process started (`system.process.cpu.start_time`). |
| **Memory** | The percentage of memory (`system.process.memory.rss.pct`) the process occupied in main memory (RAM). |
| **State** | The current state of the process and the total number of processes (`system.process.state`). Expected values are: `running`, `sleeping`, `dead`, `stopped`, `idle`, `zombie`, and `unknown`. |

:::{image} /solutions/images/serverless-processes-overlay.png
:alt: Host processes
:screenshot:
:::

:::::

% Stateful only for Profiling

:::::{dropdown} Universal Profiling
The **Universal Profiling** tab shows CPU usage down to the application code level. From here, you can find the sources of resource usage, and identify code that can be optimized to reduce infrastructure costs. The Universal Profiling tab has the following views.

|     |     |
| --- | --- |
| **Flamegraph** | A visual representation of the functions that consume the most resources. Each rectangle represents a function. The rectangle width represents the time spent in the function. The number of stacked rectangles represents the stack depth, or the number of functions called to reach the current function. |
| **Top 10 Functions** | A list of the most expensive lines of code on your host. See the most frequently sampled functions, broken down by CPU time, annualized CO2, and annualized cost estimates. |

For more on Universal Profiling, refer to the [Universal Profiling](/solutions/observability/infra-and-hosts/universal-profiling.md) docs.

:::{image} /solutions/images/observability-universal-profiling-overlay.png
:alt: Host Universal Profiling
:screenshot:
:::

:::::


:::::{dropdown} Logs
The **Logs** tab displays logs relating to the host that you have selected. By default, the logs tab displays the following columns.

|  |  |
| --- | --- |
| **Timestamp** | The timestamp of the log entry from the `timestamp` field. |
| **Message** | The message extracted from the document. The content of this field depends on the type of log message. If no special log message type is detected, the [Elastic Common Schema (ECS)](ecs://reference/ecs-base.md) base field, `message`, is used. |

To view the logs in the {{logs-app}} for a detailed analysis, click **Open in Logs**.

:::{image} /solutions/images/serverless-logs-overlay.png
:alt: Host logs
:screenshot:
:::

:::::


:::::{dropdown} Anomalies
:::{note}
{applies_to}`{stack: "ga 9.2", serverless: "ga"}` Anomaly detection isn't available for OpenTelemetry hosts. When the **Schema** is set to OpenTelemetry, this tab isn't available.
:::

The **Anomalies** tab displays a list of each single metric {{anomaly-detect}} job for the specific host. By default, anomaly jobs are sorted by time, showing the most recent jobs first.

Along with the name of each anomaly job, detected anomalies with a severity score equal to 50 or higher are listed. These scores represent a severity of "warning" or higher in the selected time period. The **summary** value represents the increase between the actual value and the expected ("typical") value of the host metric in the anomaly record result.

To drill down and analyze the metric anomaly, select **Actions** → **Open in Anomaly Explorer**. You can also select **Actions** → **Show in Inventory** to view the host Inventory page, filtered by the specific metric.

:::{image} /solutions/images/serverless-anomalies-overlay.png
:alt: Anomalies
:screenshot:
:::

:::::


:::::{dropdown} Osquery
::::{note}

**For Observability serverless projects**, one of the following roles is required to use Osquery.

* **Admin:** Has full access to project configuration, including the ability to install, manage, and run Osquery queries through {{agent}}. This role supports both ad hoc (live) queries and scheduled queries against monitored hosts. Admins can view and analyze the results directly in {{es}}.
* **Editor:** Has limited access. Editors can run pre-configured queries, but may have restricted permissions for setting up and scheduling new queries, especially queries that require broader access or permissions adjustments.
* **Viewer**: Has read-only access to data, including viewing Osquery results if configured by a user with higher permissions. Viewers cannot initiate or schedule Osquery queries themselves.

To learn more about roles, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


::::{important}
You must have an active [{{agent}}](/reference/fleet/install-elastic-agents.md) with an assigned agent policy that includes the [Osquery Manager](https://docs.elastic.co/en/integrations/osquery_manager.html) integration.

::::


The **Osquery** tab allows you to build SQL statements to query your host data. You can create and run live or saved queries against the {{agent}}. Osquery results are stored in {{es}} so that you can use the {{stack}} to search, analyze, and visualize your host metrics. To create saved queries and add scheduled query groups, refer to [Osquery](/solutions/security/investigate/osquery.md).

To view more information about the query, click the **Status** tab. A query status can result in `success`, `error` (along with an error message), or `pending` (if the {{agent}} is offline).

Other options include:

* View in Discover to search, filter, and view information about the structure of host metric fields. To learn more, refer to [Discover](/explore-analyze/discover.md).
* View in Lens to create visualizations based on your host metric fields. To learn more, refer to [Lens](/explore-analyze/visualize/lens.md).
* View the results in full screen mode.
* Add, remove, reorder, and resize columns.
* Sort field names in ascending or descending order.

:::{image} /solutions/images/serverless-osquery-overlay.png
:alt: Osquery
:screenshot:
:::

:::::


::::{note}
The metrics shown on the **Hosts** page are also available when viewing hosts on the **Infrastructure inventory** page.

::::



## Why am I seeing dashed lines in charts? [analyze-hosts-why-dashed-lines]

There are a few reasons why you may see dashed lines in your charts.

* [The chart interval is too short](/solutions/observability/infra-and-hosts/analyze-compare-hosts.md#dashed-interval)
* [Data is missing](/solutions/observability/infra-and-hosts/analyze-compare-hosts.md#dashed-missing)
* [The chart interval is too short and data is missing](/solutions/observability/infra-and-hosts/analyze-compare-hosts.md#observability-analyze-hosts-the-chart-interval-is-too-short-and-data-is-missing)


### The chart interval is too short [dashed-interval]

In this example, the data emission rate is lower than the Lens chart interval. A dashed line connects the known data points to make it easier to visualize trends in the data.

:::{image} /solutions/images/serverless-hosts-dashed.png
:alt: Screenshot showing dashed chart
:screenshot:
:::

The chart interval is automatically set depending on the selected time duration. To fix this problem, change the selected time range at the top of the page.

::::{tip}
Want to dig in further while maintaining the selected time duration? Hover over the chart you’re interested in and select **Options** → **Open in Lens**. Once in Lens, you can adjust the chart interval temporarily. Note that this change is not persisted in the **Hosts** view.

::::



### Data is missing [dashed-missing]

A solid line indicates that the chart interval is set appropriately for the data transmission rate. In this example, a solid line turns into a dashed line—indicating missing data. You may want to investigate this time period to determine if there is an outage or issue.

:::{image} /solutions/images/serverless-hosts-missing-data.png
:alt: Screenshot showing missing data
:screenshot:
:::


### The chart interval is too short and data is missing [observability-analyze-hosts-the-chart-interval-is-too-short-and-data-is-missing]

In the example shown in the screenshot, the data emission rate is lower than the Lens chart interval **and** there is missing data.

This missing data can be hard to spot at first glance. The green boxes outline regular data emissions, while the missing data is outlined in pink. Similar to the above scenario, you may want to investigate the time period with the missing data to determine if there is an outage or issue.

:::{image} /solutions/images/serverless-hosts-dashed-and-missing.png
:alt: Screenshot showing dashed lines and missing data
:screenshot:
:::


## Troubleshooting [observability-analyze-hosts-troubleshooting]


### What does *this host has been detected by APM* mean? [observability-analyze-hosts-what-does-mean]

In the Hosts view, you might see a question mark icon (![Question mark icon](/solutions/images/serverless-questionInCircle.svg "")) before a host name with a tooltip note stating that the host has been detected by APM.

When a host is detected by APM, but is not collecting full metrics (for example, through the [Elastic System integration](integration-docs://reference/system/index.md)), it will be listed as a host with the partial metrics collected by APM.


### I don’t recognize a host name and I see a question mark icon next to it [observability-analyze-hosts-i-dont-recognize-a-host-name-and-i-see-a-question-mark-icon-next-to-it]

This could mean that the APM agent has not been configured to use the correct host name. Instead, the host name might be the container name or the Kubernetes pod name.

To get the correct host name, you need to set some additional configuration options, specifically `system.kubernetes.node.name` as described in [Kubernetes data](/solutions/observability/apm/managed-intake-service-event-api.md#kubernetes-data).

### I don't see all of my host data [observability-analyze-hosts-i-dont-see-all-of-my-host-data]
```{applies_to}
stack: ga 9.2
serverless: ga
```

If you have host data from both the Elastic System integration and OpenTelemetry (OTel), the selector defaults to OTel. If you want to see Elastic System integration data for your current query, select **Elastic System Integration** from the **Schema** selector.