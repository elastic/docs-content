---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-processing-and-performance.html
---

# Processing and performance [apm-processing-and-performance]

APM Server performance depends on a number of factors: memory and CPU available, network latency, transaction sizes, workload patterns, agent and server settings, versions, and protocol.

We tested several scenarios to help you understand how to size the APM Server so that it can keep up with the load that your Elastic APM agents are sending:

* Using the *CPU Optimized* hardware template on AWS, GCP and Azure on {{ecloud}} with the following instances (for more details see [Hardware Profiles](../../../deploy-manage/deploy/elastic-cloud/ec-configure-deployment-settings.md#ec-hardware-profiles)):

    * AWS: c6gd
    * Azure: fsv2
    * GCP: n2.68x32x45

* For each hardware template, testing with several sizes: 1 GB, 4 GB, 8 GB, and 32 GB.
* For each size, using a fixed number of APM agents: 10 agents for 1 GB, 30 agents for 4 GB, 60 agents for 8 GB, and 240 agents for 32 GB.
* In all scenarios, using medium sized events. Events include [transactions](../../../solutions/observability/apps/transactions.md) and [spans](../../../solutions/observability/apps/spans.md).

::::{note}
You will also need to scale up {{es}} accordingly, potentially with an increased number of shards configured. For more details on scaling {{es}}, refer to the [{{es}} documentation](../../../deploy-manage/index.md).
::::


The results below include numbers for a synthetic workload. You can use the results of our tests to guide your sizing decisions, however, **performance will vary based on factors unique to your use case** like your specific setup, the size of APM event data, and the exact number of agents.

| Profile / Cloud | AWS | Azure | GCP |
| --- | --- | --- | --- |
| **1 GB**<br>(10 agents) | 15,000<br>events/second | 14,000<br>events/second | 17,000<br>events/second |
| **4 GB**<br>(30 agents) | 29,000<br>events/second | 26,000<br>events/second | 35,000<br>events/second |
| **8 GB**<br>(60 agents) | 50,000<br>events/second | 34,000<br>events/second | 48,000<br>events/second |
| **16 GB**<br>(120 agents) | 96,000<br>events/second | 57,000<br>events/second | 90,000<br>events/second |
| **32 GB**<br>(240 agents) | 133,000<br>events/second | 89,000<br>events/second | 143,000<br>events/second |

Don’t forget that the APM Server is stateless. Several instances running do not need to know about each other. This means that with a properly sized {{es}} instance, APM Server scales out linearly.

::::{note}
RUM deserves special consideration. The RUM agent runs in browsers, and there can be many thousands reporting to an APM Server with very variable network latency.
::::


Alternatively or in addition to scaling the APM Server, consider decreasing the ingestion volume. Read more in [Reduce storage](../../../solutions/observability/apps/reduce-storage.md).

