---
navigation_title: Run {{es}} in production
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/scalability.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-planning.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
products:
  - id: elasticsearch
  - id: cloud-hosted
---

# Run {{es}} in production [scalability]

Many teams rely on {{es}} to run their key services. To ensure these services remain available and responsive under production workloads, you can design your deployment with the appropriate level of resilience, and apply performance optimizations tailored to your environment and use case.

{{es}} is built to be always available and to scale with your needs. It does this using a [distributed architecture](/deploy-manage/distributed-architecture.md). By distributing your cluster, you can keep Elastic online and responsive to requests.

In cases where built-in resilience mechanisms aren't enough, {{es}} offers tools, such as [cross-cluster replication](../tools/cross-cluster-replication.md) and [snapshot and restore](../tools/snapshot-and-restore.md), to help you fall back or recover quickly. You can also use cross-cluster replication to serve requests based on the geographic location of your users and resources.

Explore the following topics to learn how to build, scale, and optimize your production deployment:

* [Designing for resilience](./availability-and-resilience.md): Learn the foundations of resilience in {{es}} and what it takes to keep your deployment available during hardware failures, outages, or node disruptions. This section covers key concepts like multiple nodes, shards, and replicas, and how to combine them to build resilient architectures.

* [Scaling considerations](./scaling-considerations.md): Understand when and how to scale your {{es}} deployment effectively. This section explains how to monitor cluster health, optimize performance, and make informed scaling decisions, whether you’re scaling manually in self-managed environments or relying on autoscaling in orchestrated deployments.

* [Performance optimizations](./optimize-performance.md): Learn how to improve {{es}} performance across different use cases, including indexing, search, disk usage, and approximate kNN. This section provides targeted recommendations to help you tune your cluster based on workload patterns and resource constraints.

## Deployment models and operational responsibilities

Your responsibilities when running {{es}} in production depend on the [deployment type](/deploy-manage/deploy.md#choosing-your-deployment-type). Depending on the platform, some aspects, such as scaling or cluster configuration, are managed for you, while others might require your attention and knowledge:

* **Self-managed {{es}}**: You are responsible for setting up and managing nodes, clusters, shards, and replicas. This includes managing the underlying infrastructure, scaling, and ensuring high availability through failover and backup strategies.

* **{{ech}}**: Elastic can [autoscale](../autoscaling.md) resources in response to workload changes. You can choose from different hardware profiles and deployment architectures to apply sensible defaults for your use case. A good understanding of nodes, shards, and replicas is important, as you are still responsible for managing your data and ensuring cluster performance. Also review the [plan for production](../../deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md) for how to plan your deployment for production.

* **{{ece}}**: Similar to {{ech}}, ECE manages {{es}} deployments and automates cluster operations, including scaling and orchestration. However, you are responsible for maintaining the platform itself, including the ECE hosts, operating system updates, and software upgrades. At the deployment level, you must also manage data, monitor performance, and handle shard strategies and capacity planning.

* **{{eck}}**: ECK gives you powerful orchestration capabilities for running {{es}} on Kubernetes. It simplifies lifecycle management, component configuration, upgrades, and supports [autoscaling](../autoscaling.md). However, you're still responsible for the Kubernetes environment and managing the {{es}} deployments themselves. That includes infrastructure sizing, sharding strategies, performance monitoring, and availability planning. Think of ECK as similar to a self-managed environment, but with orchestration and automation benefits.

* **{{serverless-full}}**: You don’t need to worry about nodes, shards, or replicas. These resources are 100% automated on the serverless platform, which is designed to scale with your workload. Project performance and data retention are controlled through the [Search AI Lake settings](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-ai-lake-settings).

::::{note}
To understand what Elastic manages and what you're responsible for in {{ech}} and {{serverless-short}}, refer to [{{ecloud}} responsibilities](https://www.elastic.co/cloud/shared-responsibility). It outlines the security, availability, and operational responsibilities between Elastic and you.
::::

## Additional guidance for production environments

The following topics, covered in other sections of the documentation, offer valuable guidance for running {{es}} in production.

### Plan your data structure and formatting [ec_plan_your_data_structure_availability_and_formatting]

* Build a [data architecture](/manage-data/lifecycle/data-tiers.md) that best fits your needs. Based on your own access and retention policies, you can add warm, cold, and frozen data tiers, and automate deletion of old data.
* Normalize event data to better analyze, visualize, and correlate your events by adopting the [Elastic Common Schema](ecs://reference/ecs-getting-started.md) (ECS). Elastic integrations use ECS out-of-the-box. If you are writing your own integrations, ECS is recommended.
* Consider [data streams](/manage-data/data-store/data-streams.md) and [index lifecycle management](/manage-data/lifecycle/index-lifecycle-management.md) to manage and retain your data efficiently over time.

  ::::{tip}
  [Elastic integrations](https://www.elastic.co/integrations) provide default index lifecycle policies, and you can [build your own policies for your custom integrations](/manage-data/lifecycle/index-lifecycle-management/ilm-tutorials.md).
  ::::

### Security and monitoring [security-and-monitoring]

As with any enterprise system, you need tools to secure, manage, and monitor your deployments. Security, monitoring, and administrative features that are integrated into {{es}} enable you to use [Kibana](/get-started/the-stack.md) as a control center for managing a cluster.

* [Learn about securing an {{es}} cluster](../security.md)

* [Learn about authentication and authorization in {{es}} and {{kib}}](../users-roles.md)

* [Learn about monitoring your cluster](../monitor.md)
