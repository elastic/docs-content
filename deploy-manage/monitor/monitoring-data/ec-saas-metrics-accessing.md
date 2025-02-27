---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-saas-metrics-accessing.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-saas-metrics-accessing.html
applies_to:
  deployment:
    ess: all
---

# Access performance metrics [ec-saas-metrics-accessing]

Cluster performance metrics are available directly in the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body). The graphs on this page include a subset of {{ech}}-specific performance metrics.

For advanced views or production monitoring, [enable logging and monitoring](../stack-monitoring/elastic-cloud-stack-monitoring.md). The monitoring application provides more advanced views for Elasticsearch and JVM metrics, and includes a configurable retention period.

To access cluster performance metrics:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list. For example, you might want to select **Is unhealthy** and **Has master problems** to get a short list of deployments that need attention.

3. From your deployment menu, go to the **Performance** page.

The following metrics are available:


### CPU usage [ec_cpu_usage]

:::{image} ../../../images/cloud-metrics-cpu-usage.png
:alt: Graph showing CPU usage
:::

Shows the maximum usage of the CPU resources assigned to your Elasticsearch cluster, as a percentage. CPU resources are relative to the size of your cluster, so that a cluster with 32GB of RAM gets assigned twice as many CPU resources as a cluster with 16GB of RAM. All clusters are guaranteed their share of CPU resources, as {{ech}} infrastructure does not overcommit any resources. CPU credits permit boosting the performance of smaller clusters temporarily, so that CPU usage can exceed 100%.

::::{tip}
This chart reports the maximum CPU values over the sampling period. [Logs and Metrics](../stack-monitoring/elastic-cloud-stack-monitoring.md) ingested into [Stack Monitoring](visualizing-monitoring-data.md)'s "CPU Usage" instead reflects the average CPU over the sampling period. Therefore, you should not expect the two graphs to look exactly the same. When investigating [CPU-related performance issues](../../../troubleshoot/monitoring/performance.md), you should default to [Stack Monitoring](visualizing-monitoring-data.md).
::::



### CPU credits [ec_cpu_credits]

:::{image} ../../../images/cloud-metrics-cpu-credits.png
:alt: Graph showing available CPU credits
:::

Shows your remaining CPU credits, measured in seconds of CPU time. CPU credits enable the boosting of CPU resources assigned to your cluster to improve performance temporarily when it is needed most. For more details check [How to use vCPU to boost your instance](ec-vcpu-boost-instance.md).


### Number of requests [ec_number_of_requests]

:::{image} ../../../images/cloud-metrics-number-of-requests.png
:alt: Graph showing the number of requests
:::

Shows the number of requests that your cluster receives per second, separated into search requests and requests to index documents. This metric provides a good indicator of the volume of work that your cluster typically handles over time which, together with other performance metrics, helps you determine if your cluster is sized correctly. Also lets you check if there is a sudden increase in the volume of user requests that might explain an increase in response times.


### Search response times [ec_search_response_times]

:::{image} ../../../images/cloud-metrics-search-response-times.png
:alt: Graph showing search response times
:::

Indicates the amount of time that it takes for your Elasticsearch cluster to complete a search query, in milliseconds. Response times won’t tell you about the cause of a performance issue, but they are often a first indicator that something is amiss with the performance of your Elasticsearch cluster.


### Index response times [ec_index_response_times]

:::{image} ../../../images/cloud-metrics-index-response-times.png
:alt: Graph showing index response times
:::

Indicates the amount of time that it takes for your Elasticsearch cluster to complete an indexing operation, in milliseconds. Response times won’t tell you about the cause of a performance issue, but they are often a first indicator that something is amiss with the performance of your Elasticsearch cluster.


### Memory pressure per node [ec_memory_pressure_per_node]

:::{image} ../../../images/cloud-metrics-memory-pressure-per-node.png
:alt: Graph showing memory pressure per node
:::

Indicates the total memory used by the JVM heap over time. We’ve configured {{es}}'s garbage collector to keep memory usage below 75% for heaps of 8GB or larger. For heaps smaller than 8GB, the threshold is 85%. If memory pressure consistently remains above this threshold, you might need to resize your cluster or reduce memory consumption. Check [how high memory pressure can cause performance issues](../../../troubleshoot/monitoring/high-memory-pressure.md).


### GC overhead per node [ec_gc_overhead_per_node]

:::{image} ../../../images/cloud-metrics-gc-overhead-per-node.png
:alt: Graph showing the garbage collection overhead per node
:::

Indicates the overhead involved in JVM garbage collection to reclaim memory.


## Tips for working with performance metrics [ec_tips_for_working_with_performance_metrics]

Performance correlates directly with resources assigned to your cluster, and many of these metrics will show some sort of correlation with each other when you are trying to determine the cause of a performance issue. Take a look at some of the scenarios included in this section to learn how you can determine the cause of performance issues.

It is not uncommon for performance issues on {{ech}} to be caused by an undersized cluster that cannot cope with the workload it is being asked to handle. If your cluster performance metrics often shows high CPU usage or excessive memory pressure, consider increasing the size of your cluster soon to improve performance. This is especially true for clusters that regularly reach 100% of CPU usage or that suffer out-of-memory failures; it is better to resize your cluster early when it is not yet maxed out than to have to resize a cluster that is already overwhelmed. [Changing the configuration of your cluster](../../deploy/elastic-cloud/configure.md) may add some overhead if data needs to be migrated to the new nodes, which can increase the load on a cluster further and delay configuration changes.

To help diagnose high CPU usage you can also use the Elasticsearch [nodes hot threads API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-hot-threads), which identifies the threads on each node that have the highest CPU usage or that have been executing for a longer than normal period of time.

::::{tip}
Got an overwhelmed cluster that needs to be upsized? [Try enabling maintenance mode first](../../maintenance/ece/start-stop-routing-requests.md). It will likely help with configuration changes.
::::


Work with the metrics shown in **Cluster Performance Metrics** section to help you find the information you need:

* Hover on any part of a graph to get additional information. For example, hovering on a section of a graph that shows response times reveals the percentile that responses fall into at that point in time:

    :::{image} ../../../images/cloud-metrics-hover.png
    :alt: Hover over the metric graph
    :::

* Zoom in on a graph by drawing a rectangle to select a specific time window. As you zoom in one metric, other performance metrics change to show data for the same time window.

    :::{image} ../../../images/cloud-metrics-zoom.png
    :alt: Zoom the metric graph
    :::

* Pan around with ![Pan in a metric graph](../../../images/cloud-metrics-pan.png "") to make sure that you can get the right parts of a metric graph as you zoom in.
* Reset the metric graph axes with ![Reset the metric graph](../../../images/cloud-metrics-reset.png ""), which returns the graphs to their original scale.

Cluster performance metrics are shown per node and are color-coded to indicate which running Elasticsearch instance they belong to.


## Cluster restarts after out-of-memory failures [ec_cluster_restarts_after_out_of_memory_failures]

For clusters that suffer out-of-memory failures, it can be difficult to determine whether the clusters are in a completely healthy state afterwards. For this reason, {{ech}} automatically reboots clusters that suffer out-of-memory failures.

You will receive an email notification to let you know that a restart occurred. For repeated alerts, the emails are aggregated so that you do not receive an excessive number of notifications. Either [resizing your cluster to reduce memory pressure](../../deploy/elastic-cloud/ec-customize-deployment-components.md#ec-cluster-size) or reducing the workload that a cluster is being asked to handle can help avoid these cluster restarts.



