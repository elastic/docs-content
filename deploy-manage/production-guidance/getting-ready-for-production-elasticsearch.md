---
navigation_title: Run Elasticsearch in production
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/scalability.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
---

# Getting ready for production [scalability]

Many teams rely on {{es}} to run their key services. To keep these services running, you can [design your {{es}} deployment for resilience](./availability-and-resilience.md), to keep {{es}} available even in case of large-scale outages. To keep it running fast, you can also design your deployment with [performance optimizations](./optimize-performance.md) that make it responsive to production workloads.

{{es}} is built to be always available and to scale with your needs. It does this using a [distributed architecture](/deploy-manage/distributed-architecture.md). By distributing your cluster, you can keep Elastic online and responsive to requests.

In case of failure, {{es}} offers tools for [cross-cluster replication](../tools/cross-cluster-replication.md) and [cluster snapshots](../tools/snapshot-and-restore.md) that can help you fall back or recover quickly. You can also use cross-cluster replication to serve requests based on the geographic location of your users and your resources.

{{es}} also offers security and monitoring tools to help you keep your cluster highly available.

## Use multiple nodes and shards [use-multiple-nodes-shards] 

When you move to production, you need to introduce multiple nodes and shards to your cluster. Nodes and shards are what make {{es}} distributed and scalable. The size and number of these nodes and shards depends on your data, your use case, and your budget.

These concepts aren’t essential if you’re just getting started. How you [deploy {{es}}](../../get-started/deployment-options.md) in production determines what you need to know:

* **Self-managed {{es}}**: You are responsible for setting up and managing nodes, clusters, shards, and replicas. This includes managing the underlying infrastructure, scaling, and ensuring high availability through failover and backup strategies.
* **Elastic Cloud**: Elastic can autoscale resources in response to workload changes. Choose from different deployment types to apply sensible defaults for your use case. A basic understanding of nodes, shards, and replicas is still important.
* **Elastic Cloud Serverless**: You don’t need to worry about nodes, shards, or replicas. These resources are 100% automated on the serverless platform, which is designed to scale with your workload.

Learn more about [nodes and shards](../distributed-architecture/clusters-nodes-shards.md).


## CCR for disaster recovery and geo-proximity [ccr-disaster-recovery-geo-proximity] 

To effectively distribute read and write operations across nodes, the nodes in a cluster need good, reliable connections to each other. To provide better connections, you typically co-locate the nodes in the same data center or nearby data centers.

Co-locating nodes in a single location exposes you to the risk of a single outage taking your entire cluster offline. To maintain high availability, you can prepare a second cluster that can take over in case of disaster by implementing cross-cluster replication (CCR).

CCR provides a way to automatically synchronize indices from your primary cluster to a secondary remote cluster that can serve as a hot backup. If the primary cluster fails, the secondary cluster can take over.

You can also use CCR to create secondary clusters to serve read requests in geo-proximity to your users.

Learn more about [cross-cluster replication](../tools/cross-cluster-replication.md) and about [designing for resilience](./availability-and-resilience.md).

::::{tip} 
You can also take [snapshots](../tools/snapshot-and-restore.md) of your cluster that can be restored in case of failure.
::::

## Cluster design and performance optimizations [cluster-design] 

{{es}} offers many options that allow you to configure your cluster to meet your organization’s goals, requirements, and restrictions. You can review the following guides to learn how to tune your cluster to meet your needs:

::::{note}
In orchestrated deployments, some of the settings mentioned in the referenced documents may not apply. Check the section headers to determine whether a topic is relevant to your deployment type.
::::

* [Designing for resilience](./availability-and-resilience.md)
* [Performance optimizations](./optimize-performance.md) 

Many {{es}} options come with different performance considerations and trade-offs. The best way to determine the optimal configuration for your use case is through [testing with your own data and queries](https://www.elastic.co/elasticon/conf/2016/sf/quantitative-cluster-sizing).
