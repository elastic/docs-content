---
navigation_title: Profiling
description: Continuously profile CPU usage across your Linux hosts with OpenTelemetry profiling or Universal Profiling, and analyze stacktraces, flamegraphs, and functions in Kibana.
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/universal-profiling.html
applies_to:
  stack: ga
  serverless: preview
products:
  - id: observability
---

# Profiling [universal-profiling]

Elastic Profiling is a whole-system, always-on, continuous profiling solution that eliminates the need for code instrumentation, recompilation, on-host debug symbols, and service restarts. Leveraging eBPF technology, it operates within the Linux kernel space, capturing only the needed data with minimal overhead in an unobtrusive manner. For a quick overview, see the [Universal Profiling product page](https://www.elastic.co/observability/ebpf-continuous-code-profiling).

## Select how to collect profiling data [profiling-collection-options]

You can send profiling data to Elastic in two ways. Both populate the same views in {{kib}}:

* {applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` **OpenTelemetry profiling** uses the OpenTelemetry eBPF profiler, deployed with {{agent}}. It needs no setup step in {{kib}}: install the **OpenTelemetry Profiling** integration on your hosts and the data starts flowing. This is the recommended option for new deployments and the only option on {{obs-serverless}}. For the host requirements and the deployment steps, refer to [Get started with OpenTelemetry profiling](get-started-with-otel-profiling.md).
* **Universal Profiling** uses Elastic's original profiling agent and backend. It requires a one-time setup step in {{kib}} and isn't available on {{serverless-short}}. For the setup step and the agent installation, refer to [Get started with Universal Profiling](get-started-with-universal-profiling.md).

Both can run side by side in the same deployment. When they do, you select which data to look at with the [schema selector](#profiling-schema-selector).

The {{kib}} app is called **Profiling** (**Universal Profiling** in earlier versions). On this page, Universal Profiling refers to the original agent, its backend, and the data they produce.

On this page, you’ll find information on:

* inspecting data through [stacktraces](#profiling-stacktraces-intro), [flamegraphs](#profiling-flamegraphs-intro), and [functions](#profiling-functions-intro)
* [filtering](#profiling-filtering-intro) your data
* [selecting a profiling schema](#profiling-schema-selector) when you collect data in more than one way
* comparing time ranges through [differential views](#profiling-differential-views-intro)


## Inspecting data in {{kib}} [profiling-inspecting-data-in-kibana]

To open **Profiling** (or **Universal Profiling** in earlier versions), find **Infrastructure** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

Under **Profiling**, click **Stacktraces** to open the [stacktraces view](#profiling-stacktraces-intro).

::::{note}
Profiling currently only supports CPU profiling through stack sampling.
::::


From the **Stacktraces** view, you get an overview of all of your data. You can also use filtering queries in the search bar to slice your data into more detailed sections of your fleet. Time-based filters and property filters allow you to inspect portions of data and drill-down into how much CPU various parts of your infrastructure consume over time.

See [Filtering](#profiling-filtering-intro) for more on slicing data and [Differential views](#profiling-differential-views-intro) for more on comparing two time ranges to detect performance improvements or regressions.


### Debug symbols [profiling-debug-symbols-intro]

Your stacktrace can be:

* symbolized, showing the full source code’s filename and line number
* partially symbolized
* not symbolized

In the following screenshot, you can see that unsymbolized frames *do not* show a filename and line number, but a hexadecimal number such as `0x80d2f4` or `<unsymbolized>`.

For Universal Profiling data, adding symbols for unsymbolized frames is currently a manual operation. See [Add symbols for native frames](add-symbols-for-native-frames.md).

:::{image} /solutions/images/observability-profiling-stacktraces-unsymbolized.png
:alt: profiling stacktraces unsymbolized
:screenshot:
:::


### Stacktraces [profiling-stacktraces-intro]

The stacktraces view shows graphs of stacktraces grouped by threads, traces, hosts, deployments, and containers:

:::{image} /solutions/images/observability-profiling-stacktraces-default-view.png
:alt: profiling stacktraces default view
:screenshot:
:::


#### Overview [profiling-stacktraces-overview]

The different views on the stacktraces page show:

* {applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` **Executables:** stacktraces grouped by executable name
* **Threads:** stacktraces grouped by the process' thread name
* **Traces:** un-grouped stacktraces
* **Hosts:** stacktraces grouped by machine’s hostname or IP address
* **Deployments:** for Universal Profiling, stacktraces grouped by deployment name set by the container orchestration (e.g. {{k8s}} `ReplicaSet`, `DaemonSet`, or `StatefulSet` name). For OpenTelemetry profiling, this view groups by {{k8s}} pod name.
* **Containers:** stacktraces grouped by container name discovered by the host-agent

The stacktraces view provides valuable information that you can use to:

* Discover which container, deployed across multiple machines, is using the most CPU.
* Discover how much relative overhead comes from third-party software running on your machines.
* Detect unexpected CPU spikes across threads, and drill-down into a smaller time range to investigate further with a flamegraph.

Stacktraces are grouped based on the origin of collected stacktraces. You might find an empty view in containers and deployments if your host-agent deployment is profiling systems that do not run any containers or container orchestrators. In a deployment where Profiling is correctly receiving data from the profiling agents you should always see a graph in the threads, hosts, and traces view.


#### Navigating the stacktraces view [profiling-navigating-stacktraces]

Hover and click each of the stacked bar chart sections to show details. You can arrange the graph to display absolute values, or relative percentage values.

Below the top graph, there are individual graphs that show the individual trend-line for each of the items:

:::{image} /solutions/images/observability-profiling-stacktraces-smaller-graphs.png
:alt: profiling stacktraces smaller graphs
:screenshot:
:::

The percentage displayed in the top-right corner of every individual graph is the relative number of occurrences of every time over the total of samples in the group.

::::{note}
The displayed percentage is different from the percentage of CPU usage. Profiling is not meant to show absolute monitoring data. Instead, it allows for relative comparisons between software running in your infrastructure (for example, which is the most expensive?)
::::


The individual graphs are ordered in decreasing order, from top to bottom, left to right.

In the **Traces** tab, clicking **Show more** at the bottom of one of the individual graphs shows the full stacktrace.

:::{image} /solutions/images/observability-profiling-stacktraces-show-more.png
:alt: profiling stacktraces show more
:screenshot:
:::


### Flamegraphs [profiling-flamegraphs-intro]

The flamegraph view groups hierarchical data (stacktraces) into rectangles stacked onto or next to each other. The size of each rectangle represents the relative weight of a child compared to its parent.

:::{image} /solutions/images/observability-profiling-flamegraph-view.png
:alt: profiling flamegraph view
:screenshot:
:::


#### Overview [profiling-flamegraph-overview]

Flamegraphs provide immediate feedback on which parts of the software should be searched first for optimization opportunities, highlighting the hottest code paths across your entire infrastructure.

You can use flamegraphs to:

* detect unexpected usage of system calls or native libraries linked to your own software: Profiling is able to unwind stacktraces across user-space boundary into kernel-space
* inspect the call stacks of the most CPU-intensive application, detecting hot code paths and scouting for optimization opportunities
* find "deep" call stack, usually hinting areas where there are many indirections across classes or objects


#### Navigating the flamegraph view [profiling-navigating-flamegraph]

You can navigate a flamegraph on both the horizontal and vertical axes:

* Horizontal axes: every process that is sampled has at least a rectangle under the `root` frame. In Profiling flamegraphs, you will likely discover the existence of processes you don’t control, but that are eating a significant portion of your CPU resources.
* Vertical axes: traversing a process' call stack allows you to identify which parts of the process are executing most frequently. This allows pinpointing functions or methods that *should* be negligible but are instead a big portion of your call sites.

You can drag the graph up, down, right, or left to move the visible area.

You can zoom in and out of a subset of stacktraces, by clicking on individual frames or scrolling up in the colored view.

The summary square in the bottom-left corner of the graph lets you shift the visible area of the graph. The position of the summary square in the bottom-right corner adjusts when you drag the flamegraph, and moving the summary square adjusts the visible area in the bigger panel.

Hovering your mouse over a rectangle in the flamegraph displays the frame’s details in the window. To see more frame information, click on the **Show more information** icon after pinning the tooltip.

:::{image} /solutions/images/observability-profiling-flamegraph-detailed-view.png
:alt: profiling flamegraph detailed view
:screenshot:
:::

Below the graph area, you can use the search bar to find specific text in the flamegraph; here you can search binaries, function or file names, and move over the occurrences.


### Functions [profiling-functions-intro]

The functions view presents an ordered list of functions that Profiling samples most often. From this view, you can spot the functions that are running the most across your entire infrastructure, applying filters to drill down into individual components.

:::{image} /solutions/images/observability-profiling-functions-default-view.png
:alt: profiling functions default view
:screenshot:
:::


## Filtering [profiling-filtering-intro]

In all the Profiling views, the search bar accepts a filter in the {{kib}} Query Language [KQL](/explore-analyze/query-filter/languages/kql.md).

Most notably, you may want to filter on:

* `profiling.project.id`: the corresponding value of `project-id` host-agent flag, logical group of deployed host-agents (Universal Profiling data only)
* `process.thread.name`: the process' thread name, e.g. `python`, `java`, or `kauditd`
* `orchestrator.resource.name`: the name of the group of the containerized deployment as set by the orchestrator. For OpenTelemetry data, this field is an alias for `resource.attributes.k8s.pod.name`.
* `container.name`: the name of the single container instance, as set by the container engine
* `host.name` or `host.ip`: the machine’s hostname or IP address (useful for debugging issues on a single Virtual Machine)


## Select a profiling schema [profiling-schema-selector]
```{applies_to}
stack: preview 9.6+
serverless: preview
```

OpenTelemetry profiling and Universal Profiling store their data in different formats, called schemas, and the views show one schema at a time. The schema selector at the top of the **Stacktraces**, **Flamegraphs**, and **Functions** views, including the differential views, lets you pick which one to look at. The same selector appears in the profiling views embedded in **Applications** and **Infrastructure**.

:::{image} /solutions/images/observability-profiling-schema-selector.jpg
:alt: Profiling schema selector with OpenTelemetry selected.
:screenshot:
:::

The selector works as follows:

* It lists schemas that have data for the current time range and query. If neither schema has data, it shows **No schema available**. If your selected schema has no matching data but another schema does, the selector warns that the selected schema is unavailable. Select the other schema to view its data.
* By default, **OpenTelemetry** is selected. If only Universal Profiling data is available, **Universal Profiling** is selected instead.
* Your choice is stored in the page URL, so it survives reloads and stays with you as you move between the Profiling views.
* In the differential views, the baseline time range and query determine which schemas are available, and the comparison uses the same schema on both sides.

On {{serverless-short}}, only OpenTelemetry profiling is supported. The **Add profiling data** page shows only the OpenTelemetry instructions, and the selector shows **OpenTelemetry** when matching data is available, or **No schema available** when it is not.

**Storage explorer** covers Universal Profiling data only. Until you set up Universal Profiling, the **Storage explorer** link stays disabled. When a deployment has data in both schemas, a dismissible **OpenTelemetry profiling data isn't shown here yet** callout in **Storage explorer** reminds you that the view reports Universal Profiling data only. On {{serverless-short}}, the link is always disabled. To manage the retention of OpenTelemetry profiling data, refer to [Where profiles are stored](get-started-with-otel-profiling.md#profiling-otel-data-streams).


## Differential views [profiling-differential-views-intro]

The flamegraphs and functions views can be turned into differential views, comparing data from two distinct time ranges or across multiple dimensions.

When switching to **Differential flamegraph** or **Differential TopN functions** from the tabs at the top, you see two separate search bars and datetime pickers. The left-most filters represent the data you want to use as baseline for comparison, while the right-most filters represents the data that will be compared against the baseline.

Hitting refresh on each data filter triggers a frequency comparison that highlights the CPU usage change.

In differential functions, the right-most column of functions has green or orange score calculator that represents the relative difference of position as the heaviest CPU hitting functions.

:::{image} /solutions/images/observability-profiling-functions-differential-view.png
:alt: profiling functions differential view
:screenshot:
:::

In differential flamegraphs, the difference with the baseline is highlighted with color and hue. A vivid green colored rectangle indicates that a frame has been seen in *less* samples compared to the baseline, which means an improvement. A vivid red colored rectangle indicates a frame has been seen in more samples being recorded on CPU, indicating a potential performance regression.

:::{image} /solutions/images/observability-profiling-flamegraph-differential-view.png
:alt: profiling flamegraph differential view
:screenshot:
:::


## Resource constraints [profiling-resource-constraints]
```{applies_to}
serverless: unavailable
```

One of the key goals of Universal Profiling is to have net positive cost benefit for users: the cost of profiling and observing applications should not be higher than the savings produced by the optimizations.

In this spirit, both the host-agent and storage are engineered to use as little resources as possible.


### {{es}} storage [profiling-es-storage]

The Universal Profiling storage budget is predictable on a per-profiled-core basis. The data we generate, at the fixed sampling frequency of 20 Hz, will be stored in {{es}} at the rate of approximately 40 MB per core per day.


### Host-agent CPU and memory [profiling-host-agent-cpu-and-memory]

Because Universal Profiling provides whole-system continuous profiling, the resource usage of host-agent is highly correlated with the number of processes running on the machine.

We have recorded real-world, in-production host-agent deployments to be consuming between 0.5% and 1% of CPU time, with the process' memory being as low as 50 MB, and as high as 250 MB on busier hosts.
