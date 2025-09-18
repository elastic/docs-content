---
Traffic scaling considerations
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
On [serverless](../deploy/elastic-cloud/serverless.md) scaling {{kib}} is fully managed for you.
::::

## Introduction [_introduction]

{{kib}}'s HTTP traffic is diverse and can be unpredictable. Traffic includes serving static assets like files, processing large search responses from {{es}} and managing CRUD operations against complex domain objects like SLOs. The scale of the load created by each of these kinds of traffic will vary depending on your usage patterns. While difficult to predict, there are 2 important aspects to consider when provisioning CPU and memory resources for your {{kib}} instances:

1. Concurrency: how many users do you expect to be interacting with {{kib}} simultaneously, which is largely **CPU-bound**
2. Request and response size: how large (usually measured in bytes) are the requests and responses you expect {{kib}} to service, which is largely **memory-bound**

::::{important}
The nature of traffic is not only diverse, but also unpredictable. Traffic to {{kib}} often comes in short bursts or spikes that can overwhelm an underprovisioned {{kib}}. In production environments, an overwhelmed {{kib}} will typically manifest as 502 or 503 error responses from {{kib}}.

Load balancing helps to mitigate this bursty nature of traffic by horizontally scaling your {{kib}} deployments and improving {{kib}}'s availability. See the guide on [load balancing traffic](./kibana-load-balance-traffic.md).
::::

::::{important}
CPU and memory boundedness often interact in important ways. If CPU-bound activity is reaching its limit, memory pressure will likely increase as {{kib}} has less time for activities like garbage collection. If memory-bound activity is reaching its limit, there may be more CPU work to free claimed memory, increasing CPU pressure.
::::

### Answer the following questions before sizing Kibana up or down [_before_sizing_kibana]

#### Is the {{es}} cluster correctly sized?

Follow [the production guidance for {{es}} first](./elasticsearch-in-production-environments.md). {{es}} is the search engine and backing database of {{kib}}. Any performance issues in {{es}} will manifest in {{kib}}. Additionally, while we try to mitigate this possibility, {{kib}} may be sending requests to {{es}} that degrade performance if {{es}} is underprovisioned.

#### What requests is {{kib}} sending to {{es}}?

In user interfaces like Dashboards or Discover, one can see the full query that {{kib}} is sending to {{es}}. This is a good way to get an idea of the volume of data and work a {{kib}} visualization or dashboard is creating for {{es}}. Dashboards with many visualizations will generate higher load for {{es}} and {{kib}}.

### A simple sizing strategy

Follow this strategy if you know the max number of expected concurrent users.

Start {{kib}} on **2.1 vCPU** and **2GB** of memory. This should comfortably serve a set of 10 concurrent users performing analytics activities like browsing dashboards. If you are experiencing performance issues, adding an additional **2.1 vCPUs** and **2GB** per 10 concurrent users is a safe _minimum_ to ensure {{kib}} is not resource-starved for common analytics use cases. This is known as **vertical scaling** and should typically be employed up to a maximum of **8.4 vCPU** and **8GB** of memory. In combination, it is recommended to employ **horizontal scaling** as outlined in the guide on [load balancing traffic](./kibana-load-balance-traffic.md).

Consider these examples:

* {{kib}} to should serve 50 concurrent users: **10.5 vCPU** and **10GB** of memory which on {{ech}} and {{ece}} translates to: **2 {{kib}} instances of 8.4 vCPU and 8GB memory each** or **3 {{kib}} instances of 8.4 vCPU and 4GB memory each**
* {{kib}} to serve 100 concurrent users you would need **25.2 vCPU** and **20GB** of memory which on {{ech}} and {{ece}} translates to: **3 {{kib}} instances of 8.4 vCPU and 8GB memory each**.

::::{important}
This advice does not apply to scaling {{kib}} for task manager. If you intend to use {{kib}} alerting capabilities see [task manager scaling guidance](./kibana-task-manager-scaling-considerations.md).
::::

**{{ece}}, {{ech}}, and {{eck}}** users can adjust {{kib}}'s memory by viewing their deployment and editing the {{kib}} instance's resource configuration. Note: size increments are predetermined.

**Self-managed** users must provision memory to the host that {{kib}} is running on as well as configure allocated heap. See [the guidance on configuring {{kib}} memory](./kibana-configure-memory.md). **Note:** Node.js suggests allocating 80% of available host memory to heap, assuming that Kibana is the only server process running on the (virtual) host. This allows for memory resources to be used for other activities, for example: allowing for HTTP sockets to be allocated.

**Serverless** manages {{kib}}'s resources automatically.

### A more sophisticated sizing strategy

::::{important}
On [serverless](../deploy/elastic-cloud/serverless.md) scaling and configuring {{kib}} is fully managed for you.
::::

Building on the simple strategy outlined above, we can make more precise adjustments to resource allocations. **Self-managed** users manage their CPU and memory allocations independently and can employ the strategy below to further tailor resources based on performance metrics.

#### Monitoring [_monitoring-kibana-metrics]

In order to understand the impact of your usage patterns on **a single {{kib}} instance** use the Stack Monitoring feature. See [the guide for {{kib}} deployed on {{ech}} or {{ece}}](../monitor/stack-monitoring/ece-ech-stack-monitoring.md) or the [the guide for self-managed {{kib}}](../monitor/stack-monitoring/kibana-monitoring-self-managed.md).

The rest of this guide will assume you have visibility into the following important metrics for a {{kib}} instance:

1. Event loop delay (ELD) in milliseconds - this is a Node.js concept that roughly translates to the number of milliseconds by which processing of events is delayed due to CPU-intensive activities
2. Heap size in bytes - the amount of bytes currently held in memory dedicated to {{kib}}'s heap space
3. HTTP connections - the number of sockets that the Kibana server has open

##### CPU [kibana-traffic-load-cpu-sizing]

Event loop delay (ELD) is an important metric for understanding whether Kibana is engaged in CPU-bound activity.

**As a general target, ELD should be at below ~200ms 95% of the time**. Higher delays may mean {{kib}} is CPU-starved. Sporadic increases above 200ms may mean that Kibana is periodically processing CPU-intensive activities like large responses from Elasticsearch, whereas consistently high ELD may mean Kibana is struggling to service tasks and requests.

Before increasing CPU resources, consider the impact of ELD on user experience. If users are able to use {{kib}} without the frustration that comes from a blocked CPU, provisioning additional CPU resources will not be impactful, although having spare resources in case of unexpected spikes is useful.

Monitoring {{kib}}'s ELD over time is a solid strategy for knowing when additional CPU resource is needed based on your usage patterns.

##### Memory [kibana-traffic-load-memory-sizing]

Heap size is an important metric to track. If {{kib}}'s heap size grows beyond the heap limit, {{kib}} will crash. By monitoring heap size, you can help ensure that {{kib}} has enough memory available.

**Self-managed** users must provision memory to the host that {{kib}} is running on as well as configure allocated heap. See [the guidance on configuring {{kib}} memory](./kibana-configure-memory.md). **Note:** Node.js suggests allocating 80% of available memory to heap. This allows for memory resources to be used for other activities, for example: allowing for HTTP sockets to be allocated.

