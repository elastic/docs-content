---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/view-infrastructure-metrics.html
  - https://www.elastic.co/guide/en/serverless/current/observability-view-infrastructure-metrics.html
---

# View infrastructure metrics by resource type [observability-view-infrastructure-metrics]

The **Infrastructure Inventory** page provides a metrics-driven view of your entire infrastructure grouped by the resources you are monitoring. All monitored resources emitting a core set of infrastructure metrics are displayed to give you a quick view of the overall health of your infrastructure.

To open **Infrastructure inventory**, find **Infrastructure** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} ../../../images/observability-metrics-app.png
:alt: Infrastructure UI in {kib}
:class: screenshot
:::

To learn more about the metrics shown on this page, refer to the [Metrics reference](https://www.elastic.co/guide/en/serverless/current/observability-metrics-reference.html).

::::{admonition} Don’t see any metrics?
:class: note

If you haven’t added data yet, click **Add data** to search for and install an Elastic integration.

Need help getting started? Follow the steps in [Get started with system metrics](../../../solutions/observability/infra-and-hosts/get-started-with-system-metrics.md).

::::


## Filter the Inventory view [filter-resources]

To get started with your analysis, select the type of resources you want to show in the high-level view. From the **Show** menu, select one of the following:

* **Hosts** — the default
* **Kubernetes Pods**
* **Docker Containers** — shows *all* containers, not just Docker
* **AWS** — includes EC2 instances, S3 buckets, RDS databases, and SQS queues

When you hover over each resource in the waffle map, the metrics specific to that resource are displayed.

You can sort by resource, group the resource by specific fields related to it, and sort by either name or metric value. For example, you can filter the view to display the memory usage of your Kubernetes pods, grouped by namespace, and sorted by the memory usage value.

:::{image} ../../../images/observability-kubernetes-filter.png
:alt: Kubernetes pod filtering
:class: screenshot
:::

You can also use the search bar to create structured queries using [{{kib}} Query Language](../../../explore-analyze/query-filter/languages/kql.md). For example, enter `host.hostname : "host1"` to view only the information for `host1`.

To examine the metrics for a specific time, use the time filter to select the date and time.


## View host metrics [analyze-hosts-inventory]

By default the **Infrastructure Inventory** page displays a waffle map that shows the hosts you are monitoring and the current CPU usage for each host. Alternatively, you can click the **Table view** icon ![table view icon](../../../images/observability-table-view-icon.png "") to switch to a table view.

Without leaving the **Infrastructure Inventory** page, you can view enhanced metrics relating to each host running in your infrastructure. On the waffle map, select a host to display the host details overlay.

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

:::{image} ../../../images/observability-overview-overlay.png
:alt: Host overview
:class: screenshot
:::

:::::


:::::{dropdown} Metadata
The **Metadata** tab lists all the meta information relating to the host, including host, cloud, and agent information.

This information can help when investigating events—for example, when filtering by operating system or architecture.

:::{image} ../../../images/observability-metadata-overlay.png
:alt: Host metadata
:class: screenshot
:::

:::::


:::::{dropdown} Metrics
The **Metrics** tab shows host metrics organized by type and is more complete than the view available in the *Overview* tab.

:::{image} ../../../images/serverless-metrics-overlay.png
:alt: Metrics
:class: screenshot
:::

:::::


:::::{dropdown} Processes
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

:::{image} ../../../images/serverless-processes-overlay.png
:alt: Host processes
:class: screenshot
:::

% Stateful only for Profiling

:::::

:::::{dropdown} **Universal Profiling**
The **Universal Profiling** tab shows CPU usage down to the application code level. From here, you can find the sources of resource usage, and identify code that can be optimized to reduce infrastructure costs. The Universal Profiling tab has the following views.

|     |     |
| --- | --- |
| **Flamegraph** | A visual representation of the functions that consume the most resources. Each rectangle represents a function. The rectangle width represents the time spent in the function. The number of stacked rectangles represents the stack depth, or the number of functions called to reach the current function. |
| **Top 10 Functions** | A list of the most expensive lines of code on your host. See the most frequently sampled functions, broken down by CPU time, annualized CO2, and annualized cost estimates. |

For more on Universal Profiling, refer to the [Universal Profiling](../../../solutions/observability/infra-and-hosts/universal-profiling.md) docs.

:::{image} ../../../images/observability-universal-profiling-overlay.png
:alt: Host Universal Profiling
:class: screenshot
:::

:::::


:::::{dropdown} Logs
The **Logs** tab displays logs relating to the host that you have selected. By default, the logs tab displays the following columns.

|  |  |
| --- | --- |
| **Timestamp** | The timestamp of the log entry from the `timestamp` field. |
| **Message** | The message extracted from the document. The content of this field depends on the type of log message. If no special log message type is detected, the [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/current/ecs-base.html) base field, `message`, is used. |

To view the logs in the {{logs-app}} for a detailed analysis, click **Open in Logs**.

:::{image} ../../../images/observability-logs-overlay.png
:alt: Host logs
:class: screenshot
:::

:::::


:::::{dropdown} Anomalies
The **Anomalies** tab displays a list of each single metric {{anomaly-detect}} job for the specific host. By default, anomaly jobs are sorted by time, showing the most recent jobs first.

Along with the name of each anomaly job, detected anomalies with a severity score equal to 50 or higher are listed. These scores represent a severity of "warning" or higher in the selected time period. The **summary** value represents the increase between the actual value and the expected ("typical") value of the host metric in the anomaly record result.

To drill down and analyze the metric anomaly, select **Actions** → **Open in Anomaly Explorer**. You can also select **Actions** → **Show in Inventory** to view the host Inventory page, filtered by the specific metric.

:::{image} ../../../images/serverless-anomalies-overlay.png
:alt: Anomalies
:class: screenshot
:::

:::::


:::::{dropdown} Osquery

::::{admonition} Required role
:class: note

**For Observability serverless projects**, one of the following roles is required to use Osquery.

* **Admin:** Has full access to project configuration, including the ability to install, manage, and run Osquery queries through {{agent}}. This role supports both ad hoc (live) queries and scheduled queries against monitored hosts. Admins can view and analyze the results directly in {{es}}.
* **Editor:** Has limited access. Editors can run pre-configured queries, but may have restricted permissions for setting up and scheduling new queries, especially queries that require broader access or permissions adjustments.
* **Viewer**: Has read-only access to data, including viewing Osquery results if configured by a user with higher permissions. Viewers cannot initiate or schedule Osquery queries themselves.

To learn more about roles, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


::::{important}
You must have an active [{{agent}}](https://www.elastic.co/guide/en/fleet/current/elastic-agent-installation.html) with an assigned agent policy that includes the [Osquery Manager](https://docs.elastic.co/en/integrations/osquery_manager.html) integration.

::::


The **Osquery** tab allows you to build SQL statements to query your host data. You can create and run live or saved queries against the {{agent}}. Osquery results are stored in {{es}} so that you can use the {{stack}} to search, analyze, and visualize your host metrics. To create saved queries and add scheduled query groups, refer to [Osquery](../../../solutions/security/investigate/osquery.md).

To view more information about the query, click the **Status** tab. A query status can result in `success`, `error` (along with an error message), or `pending` (if the {{agent}} is offline).

Other options include:

* View in Discover to search, filter, and view information about the structure of host metric fields. To learn more, refer to [Discover](../../../explore-analyze/discover.md).
* View in Lens to create visualizations based on your host metric fields. To learn more, refer to [Lens](../../../explore-analyze/visualize/lens.md).
* View the results in full screen mode.
* Add, remove, reorder, and resize columns.
* Sort field names in ascending or descending order.

:::{image} ../../../images/observability-osquery-overlay.png
:alt: Osquery
:class: screenshot
:::

:::::


::::{note}
These metrics are also available when viewing hosts on the **Hosts** page.

::::



## View container metrics [analyze-containers-inventory]

When you select **Docker containers**, the **Infrastructure inventory** page displays a waffle map that shows the containers you are monitoring and the current CPU usage for each container. Alternatively, you can click the **Table view** icon ![Table view icon](../../../images/serverless-table-view-icon.png "") to switch to a table view.

Without leaving the **Infrastructure inventory** page, you can view enhanced metrics relating to each container running in your infrastructure.

::::{admonition} Why do some containers report 0% or null (-) values in the waffle map?
:class: note

The waffle map shows *all* monitored containers, including containerd, provided that the data collected from the container has the `container.id` field. However, the waffle map currently only displays metrics for Docker fields. This display problem will be resolved in a future release.

::::


On the waffle map, select a container to display the container details overlay.

::::{tip}
To expand the overlay and view more detail, click **Open as page** in the upper-right corner.

::::


The container details overlay contains the following tabs:

:::::{dropdown} Overview
The **Overview** tab displays key metrics about the selected container, such as CPU, memory, network, and disk usage. The metrics shown may vary depending on the type of container you’re monitoring.

Change the time range to view metrics over a specific period of time.

Expand each section to view more detail related to the selected container, such as metadata, active alerts, and metrics.

Hover over a specific time period on a chart to compare the various metrics at that given time.

Click **Show all** to drill down into related data.

:::{image} ../../../images/observability-overview-overlay-containers.png
:alt: Container overview
:class: screenshot
:::

:::::


:::::{dropdown} Metadata
The **Metadata** tab lists all the meta information relating to the container:

* Host information
* Cloud information
* Agent information

All of this information can help when investigating events—for example, filtering by operating system or architecture.

:::{image} ../../../images/observability-metadata-overlay-containers.png
:alt: Container metadata
:class: screenshot
:::

:::::


:::::{dropdown} Metrics
The **Metrics** tab shows container metrics organized by type.

:::{image} ../../../images/observability-metrics-overlay-containers.png
:alt: Metrics
:class: screenshot
:::

:::::


:::::{dropdown} Logs
The **Logs** tab displays logs relating to the container that you have selected. By default, the logs tab displays the following columns.

|  |  |
| --- | --- |
| **Timestamp** | The timestamp of the log entry from the `timestamp` field. |
| **Message** | The message extracted from the document. The content of this field depends on the type of log message. If no special log message type is detected, the [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/current/ecs-base.html) base field, `message`, is used. |

To view the logs in the {{logs-app}} for a detailed analysis, click **Open in Logs**.

:::{image} ../../../images/observability-logs-overlay-containers.png
:alt: Container logs
:class: screenshot
:::

:::::



## View metrics for other resources [analyze-resource-metrics]

When you have searched and filtered for a specific resource, you can drill down to analyze the metrics relating to it. For example, when viewing Kubernetes Pods in the high-level view, click the Pod you want to analyze and select **Kubernetes Pod metrics** to see detailed metrics:

:::{image} ../../../images/observability-pod-metrics.png
:alt: Kubernetes pod metrics
:class: screenshot
:::


## Add custom metrics [custom-metrics]

If the predefined metrics displayed on the Inventory page for each resource are not sufficient for your specific use case, you can add and define custom metrics.

Select your resource, and from the **Metric** filter menu, click **Add metric**.

:::{image} ../../../images/serverless-add-custom-metric.png
:alt: Add custom metrics
:class: screenshot
:::


% Stateful only for Uptime

## Integrate with Logs, Uptime, and APM [apm-uptime-integration]

Depending on the features you have installed and configured, you can view logs or traces relating to a specific resource. For example, in the high-level view, when you click a Kubernetes Pod resource, you can choose:

* **Kubernetes Pod logs** to [view corresponding logs](../../../solutions/observability/logs.md) in the {{logs-app}}.
* **Kubernetes Pod APM traces** to [view corresponding APM traces](../../../solutions/observability/apps/application-performance-monitoring-apm.md) in the {{apm-app}}.
* **Kubernetes Pod in Uptime** to [view related uptime information](../../../solutions/observability/apps/synthetic-monitoring.md) in the {{uptime-app}}.