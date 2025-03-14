---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-best-practices-data.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/scalability.html
---
$$$ec-best-practices-data$$$
# Production guidance [scalability]

% start bringing https://www.elastic.co/guide/en/elasticsearch/reference/current/scalability.html here
% try to merge https://www.elastic.co/guide/en/cloud/current/ec-planning.html and https://www.elastic.co/guide/en/cloud/current/ec-best-practices-data.html
% mention all deployment types! what the user needs to be aware for orchestrated deployments.

Many teams rely on {{es}} to run their key services. To keep these services running, you can design your {{es}} deployment to keep {{es}} available, even in case of large-scale outages. To keep it running fast, you also can design your deployment to be responsive to production workloads.

{{es}} is built to be always available and to scale with your needs. It does this using a [distributed architecture](./distributed-architecture.md). By distributing your cluster, you can keep Elastic online and responsive to requests.

In case of failure, {{es}} offers tools for [cross-cluster replication](./tools/cross-cluster-replication.md) and [cluster snapshots](./tools/snapshot-and-restore.md) that can help you fall back or recover quickly. You can also use cross-cluster replication to serve requests based on the geographic location of your users and your resources.

% not very relevant
{{es}} also offers security and monitoring tools to help you keep your cluster highly available.


Recommendations out there:
- Use multiple nodes and shards

## Section overview

Running the {{stack}} in production requires careful planning to ensure resilience, performance, and scalability. This section outlines best practices and recommendations for optimizing {{es}} and {{kib}} in production environments.

* High availability (HA) and resilience
  * Resilience in small clusters
  * Resilienve in larger clusters

* Performance optimizations:
  * Elasticsearch
    * General recomendations
    * Tune for indexing speed
    * Tune for search speed
    * Tune for approximate kNN search
    * Tune for disk usage
    * Size your shards
    * Use {{es}} for time series data
  * Kibana
    * Kibana task manager scaling considerations
    * Kibana alerting

* Scaling

For additional production-critical topics, refer to:

* [](./security.md)

* [](./tools.md)

* [](./monitor.md)



(Regardless if you are running a hosted or a self managed deployment, the content of this section allow you to understand and take key decisions when designing your clusters in the following areas:)

Cluster design tiene:
- design for resilience
- tune for xxx
- tune for xxx



## Deployment types

These concepts aren’t essential if you’re just getting started. How you [deploy {{es}}](/get-started/deployment-options.md) in production determines what you need to know:

* **Self-managed {{es}}**: You are responsible for setting up and managing nodes, clusters, shards, and replicas. This includes managing the underlying infrastructure, scaling, and ensuring high availability through failover and backup strategies.
* **Elastic Cloud**: Elastic can autoscale resources in response to workload changes. Choose from different deployment types to apply sensible defaults for your use case. A basic understanding of nodes, shards, and replicas is still important.
* **Elastic Cloud Serverless**: You don’t need to worry about nodes, shards, or replicas. These resources are 100% automated on the serverless platform, which is designed to scale with your workload.

(add ECE and ECK)


% discarded text (from ECH best practices)

## HA and Resilience

{{es}} and {{kib}} provide mechanisms for HA and resilience


### Use multiple nodes and shards

### CCR for disaster recovery and geo-proximity

## Performance tuning [cluster-design]

{{es}} offers many options that allow you to configure your cluster to meet your organization’s goals, requirements, and restrictions. You can review the following guides to learn how to tune your cluster to meet your needs:

::::{note}
In orchestrated deployments some of the settings mentioned in this section are not applicable. Refer to each of the section headers to understand whether is applicable to your deployment type.
::::

* [Designing for resilience](availability-and-resilience.md)
* [Tune for indexing speed](optimize-performance/indexing-speed.md)
* [Tune for search speed](optimize-performance/search-speed.md)
* [Tune for disk usage](optimize-performance/disk-usage.md)
* [Tune for time series data](../../manage-data/use-case-use-elasticsearch-to-manage-time-series-data.md)

Many {{es}} options come with different performance considerations and trade-offs. The best way to determine the optimal configuration for your use case is through [testing with your own data and queries](https://www.elastic.co/elasticon/conf/2016/sf/quantitative-cluster-sizing).


## Scaling

% from https://www.elastic.co/guide/en/cloud/current/ec-planning.html ?
This section provides some best practices for managing your data to help you set up a production environment that matches your workloads, policies, and deployment needs.


## Plan your data structure, availability, and formatting [ec_plan_your_data_structure_availability_and_formatting]

* Build a [data architecture](/manage-data/lifecycle/data-tiers.md) that best fits your needs. Your {{ech}} deployment comes with default hot tier {{es}} nodes that store your most frequently accessed data. Based on your own access and retention policies, you can add warm, cold, frozen data tiers, and automated deletion of old data.
* Make your data [highly available](/deploy-manage/tools.md) for production environments or otherwise critical data stores, and take regular [backup snapshots](tools/snapshot-and-restore.md).
* Normalize event data to better analyze, visualize, and correlate your events by adopting the [Elastic Common Schema](asciidocalypse://docs/ecs/docs/reference/ecs-getting-started.md) (ECS). Elastic integrations use ECS out-of-the-box. If you are writing your own integrations, ECS is recommended.


## Optimize data storage and retention [ec_optimize_data_storage_and_retention]

Once you have your data tiers deployed and you have data flowing, you can [manage the index lifecycle](/manage-data/lifecycle/index-lifecycle-management.md).

::::{tip}
[Elastic integrations](https://www.elastic.co/integrations) provide default index lifecycle policies, and you can [build your own policies for your custom integrations](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md).
::::


