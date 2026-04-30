---
navigation_title: Traffic scaling considerations
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/kibana-traffic-scaling-considerations.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
products:
  - id: kibana
---

# Scale {{kib}} for your traffic workload

::::{important}
This guidance does not apply to scaling {{kib}} for task manager. If you intend to optimize {{kib}} for alerting capabilities, see [](./kibana-task-manager-scaling-considerations.md).
::::

{{kib}}'s HTTP traffic is diverse and can be unpredictable. Traffic includes serving static assets like files, processing large search responses from {{es}}, and managing CRUD operations against complex domain objects like SLOs. The scale of the load created by each of these kinds of traffic will vary depending on your usage patterns. While difficult to predict, there are two important aspects to consider when provisioning CPU and memory resources for your {{kib}} instances:

* **Concurrency**: How many users you expect to be interacting with {{kib}} simultaneously. Concurrency performance is largely **CPU-bound**. Approaching this limit increases response times.
* **Request and response size**: The size of requests and responses you expect {{kib}} to service. Performance when managing large requests and responses is largely **memory-bound**. Approaching this limit increases response times and may cause {{kib}} to crash.

::::{tip}
On [{{serverless-full}}](../deploy/elastic-cloud/serverless.md) scaling {{kib}} is fully managed for you.
::::

CPU and memory boundedness often interact in important ways. If CPU-bound activity is reaching its limit, memory pressure will likely increase as {{kib}} has less time for activities like garbage collection. If memory-bound activity is reaching its limit, there may be more CPU work to free claimed memory, increasing CPU pressure. [Tracking CPU and memory metrics over time](#advanced-scaling-using-stack-monitoring-metrics) can be very useful for understanding where your {{kib}} is experiencing a bottleneck.

::::{note}
Traffic to {{kib}} often comes in short bursts or spikes that can overwhelm an underprovisioned {{kib}} instance. In production environments, an overwhelmed {{kib}} instance will typically return 502 or 503 error responses.

Load balancing helps to mitigate traffic spikes by horizontally scaling your {{kib}} deployments and improving {{kib}}'s availability. To learn more about load balancing, refer to [](./kibana-load-balance-traffic.md).
::::

## Before you start [_before_sizing_kibana]

{{es}} is the search engine and backing database of {{kib}}. Any performance issues in {{es}} will manifest in {{kib}}. Additionally, while Elastic tries to mitigate this possibility, {{kib}} may be sending requests to {{es}} that degrade performance if {{es}} is underprovisioned.

### Is the {{es}} cluster correctly sized?

Follow [the production guidance for {{es}}](./elasticsearch-in-production-environments.md).

### What requests is {{kib}} sending to {{es}}?

In user interfaces like Dashboards or Discover, you can view the full query that {{kib}} is sending to {{es}}. This is a good way to get an idea of the volume of data and work a {{kib}} visualization or dashboard is creating for {{es}}. Dashboards with many visualizations will generate higher load for {{es}} and {{kib}}.

## Basic scaling using number of concurrent users

Follow this strategy if you know the maximum number of expected concurrent users.

Start {{kib}} on **1 vCPU** and **2GB** of memory. This should comfortably serve a set of 10 concurrent users performing analytics activities like browsing dashboards.

If you are experiencing performance issues, you can scale {{kib}} vertically by adding the following resources for every 10 additional concurrent users:
* 1 vCPU
* 2GB of memory

These amounts are a safe minimum to ensure that {{kib}} is not resource-starved for common analytics use cases.

It is recommended to scale vertically to a maximum of **8.4 vCPU** and **8GB** of memory.

You should also combine vertical scaling with horizontal scaling to handle greater concurrency or bursty traffic. Refer to [](./kibana-load-balance-traffic.md) for guidance.

### Scaling examples

| Concurrent users | Minimum vCPU | Minimum memory | ECH and ECE deployment examples |
| --- | --- | --- | --- |
| 50 | 5 vCPU | 10GB | • {{kib}} size per zone of 16GB RAM and 8 vCPU in 1 availability zone (creates 2 x 8GB nodes)<br><br>• {{kib}} size per zone of 8GB RAM and up to 8 vCPU across 2 availability zones<br><br>• {{kib}} size per zone of 4GB RAM and up to 8 vCPU across 3 availability zones |
| 100 | 10 vCPU | 20GB | • {{kib}} size per zone of 24 GB RAM and 12 vCPU in 1 availability zone (creates 3 x 8GB nodes)<br><br>• {{kib}} size per zone of 8GB RAM and up to 8 vCPU across 3 availability zones<br><br>|

Refer to the [guidance on adjusting {{kib}}'s allocated resources](#adjust-resource-allocations) once you have determined sizing.

## Advanced scaling using stack monitoring metrics

Building on the simple strategy outlined above, we can identify where {{kib}} is resource constrained more precisely. **Self-managed** and **{{eck}}** users manage CPU and memory allocations independently and can further tailor resources based on performance metrics.

### Gather usage information [_monitoring-kibana-metrics]

In order to understand the impact of your usage patterns on a single {{kib}} instance, use the [stack monitoring](../monitor/stack-monitoring.md) feature.

Using stack monitoring, you can gather the following metrics for your {{kib}} instance:

* **Event loop delay (ELD) in milliseconds:** A Node.js concept that roughly translates to the number of milliseconds by which processing of events is delayed due to CPU-intensive activities.
* **Heap size in bytes:** The amount of bytes currently held in memory dedicated to {{kib}}'s heap space.
* **HTTP connections:** The number of sockets that the {{kib}} server has open.

### Scale CPU using ELD metrics [kibana-traffic-load-cpu-sizing]

Event loop delay (ELD) is an important metric for understanding whether {{kib}} is engaged in CPU-bound activity.

**As a general target, ELD should be below ~220ms 95% of the time**. Higher delays may mean {{kib}} is CPU-starved. Sporadic increases above 200ms may mean that {{kib}} is periodically processing CPU-intensive activities like large responses from {{es}}, whereas consistently high ELD may mean {{kib}} is struggling to service tasks and requests.

Before increasing CPU resources, consider the impact of ELD on user experience. If users are able to use {{kib}} without the frustration that comes from a blocked CPU, provisioning additional CPU resources will not be impactful, although having spare resources in case of unexpected spikes is useful.

Monitoring {{kib}}'s ELD over time is a solid strategy for knowing when additional CPU resource is needed based on your usage patterns.

Refer to the [guidance on adjusting {{kib}}'s allocated resources](#adjust-resource-allocations) once you have determined vCPU sizing.

### Scale memory using heap size metrics [kibana-traffic-load-memory-sizing]

Heap size is an important metric to track. If {{kib}}'s heap size grows beyond the heap limit, {{kib}} will crash. By monitoring heap size, you can help ensure that {{kib}} has enough memory available.

Self-managed users must provision memory to the host that {{kib}} is running on as well as configure allocated heap. See [the guidance on configuring {{kib}} memory](./kibana-configure-memory.md).

Refer to the [guidance on adjusting {{kib}}'s allocated resources](#adjust-resource-allocations) once you have determined memory sizing.

## Adjust resource allocations for {{kib}} [adjust-resource-allocations]
The way that you alter the resources allocated to your {{kib}} instance depends on your deployment type:
* **[{{ech}}](/deploy-manage/deploy/elastic-cloud/ec-customize-deployment-components.md) and [{{ece}}](/deploy-manage/deploy/elastic-cloud/configure.md):** Users can adjust {{kib}}'s memory by viewing their deployment and editing the {{kib}} instance's resource configuration. In these environments, size increments are predetermined.
* **{{eck}}:** Users can configure pod memory and CPU resources. Refer to [](../deploy/cloud-on-k8s/manage-compute-resources.md).
* **Self-managed:** Users must provision memory to the host that {{kib}} is running on as well as configure allocated heap. See [the guidance on configuring {{kib}} memory](./kibana-configure-memory.md).

:::{note}
For {{eck}} and self-managed deployments, Node.js suggests allocating 80% of available host memory to heap, assuming that {{kib}} is the only server process running on the (virtual) host. This allows for memory resources to be used for other activities, for example, allowing for HTTP sockets to be allocated.
:::