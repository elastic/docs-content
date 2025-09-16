---
navigation_title: Kibana traffic scaling considerations
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

# {{kib}} traffic scaling guide [kibana-traffic-scaling-considerations]

::::{important}
On [serverless](../deploy/elastic-cloud/serverless.md) scaling {{kib}} is fully managed for you.
::::

## Introduction [_introduction]

{{kib}}'s HTTP traffic is diverse and can be unpredictable. Traffic includes serving static assets like files, processing large search responses from {{es}} and managing CRUD operations against complex domain objects like SLOs. The scale of the load created by each of these kinds of traffic will vary depending on your usage patterns. While difficult to predict, there are 2 important aspects to consider when provisioning CPU and memory resources for your {{kib}} instances:

1. Concurrency: how many users do you expect to be interacting with {{kib}} simultaneously which is largely **CPU bound**
2. Request and response size: how large (usually measured in bytes) are the requests and responses you expect to {{kib}} to service which largely **memory bound**

::::{important}
The nature of traffic is not only diverse, but also unpredictable. Traffic to {{kib}} often comes in short bursts or spikes that can overwhelm an underprovisioned {{kib}}. In production environments an overwhelmed {{kib}} will typically manifest as 502 or 503 error responses from {{kib}}.

A valuable strategy known as load balancing helps to mitigate this bursty nature of traffic by horizontally scaling your {{kib}} deployments and improving {{kib}}'s availability. See the guide on [load balancing traffic](./kibana-load-balance-traffic.md). The rest of this guide will focus on provisioning CPU and memory (also known as vertically scaling) a single Kibana for handling your traffic load, but is not a replacement for load balancing traffic.
::::

::::{important}
CPU and memory boundedness often interact in important ways. If CPU-bound activity is reaching it's limit memory pressure will likely increase as {{kib}} has less time for activities like garbage collection. If memory-bound activity is reaching it's limit there may be more CPU work to free claimed memory, increasing CPU pressure.
::::

### Before scaling {{kib}} for traffic... [_before_sizing_kibana]

#### Is the {{es}} cluster correctly sized?

Follow [the production guidance for {{es}} first](./elasticsearch-in-production-environments.md). {{es}} is the search engine and backing database of {{kib}}. Any performance issues in {{es}} will manifest in {{kib}}. Additionally, while we try to mitigate this possibility, {{kib}} may be sending requests to {{es}} that degrade performance if {{es}} is underprovisioned.

#### What requests is {{kib}} sending to {{es}}?

In user interfaces like Dashboards or Discover one can see the full query that {{kib}} is sending to {{es}}. This is a good way to get an idea of the volume of data and work a {{kib}} visualization or dashboard is creating for {{es}}.

### A simple sizing strategy

As a general starting point, {{kib}} on **1 CPU** and **1.5GB** of memory should comfortably serve a set of 10 concurrent users performing analytics activities like browsing dashboards. If you are experiencing performance issues, doubling the provisioned resources per 10 concurrent users is a simple and safe strategy for ensuring {{kib}} is not resource starved.

**{{ece}}, {{ech}} and {{eck}** users can adjust {{kib}}'s memory by viewing their deployment and editing the {{kib}} instance's resource configuration.

**Self-managed** control the means for provisioning more and less memory to a {{kib}} instance.

**Serverless** manages {{kib}}'s resources automatically.

### A more sophisticated sizing strategy

Please note, there is a [separate guide for sizing Kibana for reporting use cases](./kibana-reporting-production-considerations.md).

#### Monitoring [_monitoring-kibana-metrics]

In order to understand the impact of your usage patterns on **a {{kib}} instance** use the Stack Monitoring feature. The rest of this guide will assume you have visibility into the following important metrics for a {{kib}} instance:

1. Event loop delay (ELD) in milliseconds - this is a Node.js concept that roughly translates to: the number of milliseconds by which processing of events is delayed due to CPU intensive activities
2. Memory size in bytes - the amount of bytes currently on the heap
3. HTTP connections - the number of sockets that the Kibana server has open

::::{important}
See [the guide for {{kib}} deployed on {{ech}} or {{ece}}](../monitor/stack-monitoring/ece-ech-stack-monitoring.md) or the [the guide for self-managed {{kib}}](../monitor/stack-monitoring/kibana-monitoring-self-managed.md).

On [serverless](../deploy/elastic-cloud/serverless.md) scaling {{kib}} is fully managed for you.
::::

##### CPU [kibana-traffic-load-cpu-sizing]

Event loop delay (ELD) is an important metric for understanding whether Kibana is engaged in CPU-bound activity.

**As a general target ELD should be below 200ms 95% of the time**. Higher delays may mean {{kib}} is CPU starved. Sporadic increases above 200ms may mean that Kibana is periodically processing CPU intensive activities like large responses from Elasticsearch. It is important to consider the impact of ELD on user experience. If users are able to use {{kib}} without the frustration that comes from a blocked CPU provisioning additional CPU resources will not be impactful. However, monitoring ELD over time is a solid strategy for ensuring your Kibana is not exhausting CPU resources.

**{{ece}}, {{ech}} and {{eck}** users can adjust {{kib}}'s CPU and memory by viewing their deployment and editing the {{kib}} instance's resource configuration.

**Self-managed** users are responsible for managing CPU.

##### Memory [kibana-traffic-load-memory-sizing]

Heap size relative is an important metric to track. If {{kib}}'s heap size grows beyond the heap limit {{kib}} will crash. By monitoring heap size you can help ensure that {{kib}} has enough memory available.

**{{ece}}, {{ech}} and {{eck}** users can adjust {{kib}}'s CPU and memory by viewing their deployment and editing the {{kib}} instance's resource configuration.

**Self-managed** users must provision memory to the host that {{kib}} is running on as well as configure allocated heap, see [the guidance on configuring {{kib}} memory](./kibana-configure-memory.md). **Note:** Node.js suggests allocating 80% of available memory to heap. This allows for memory resources to be used for other activities, for example: allowing for HTTP sockets to allocated.

