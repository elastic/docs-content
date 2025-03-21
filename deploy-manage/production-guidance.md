---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-best-practices-data.html
  - https://www.elastic.co/guide/en/cloud/current/ec-planning.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-planning.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
---

# Production guidance

Running the {{stack}} in production requires careful planning to ensure resilience, performance, and scalability. This section outlines best practices and recommendations for optimizing {{es}} and {{kib}} in production environments.

You’ll learn how to design highly available and resilient deployments, implement best practices for managing workloads, and apply performance optimizations to handle scaling demands efficiently.

For {{es}}, this includes strategies for fault tolerance, data replication, and workload distribution to maintain stability under load. For {{kib}}, you’ll explore how to deploy multiple Kibana instances within the same environment and make informed decisions about scaling horizontally or vertically based on the task manager metrics, which provide insights into background task execution and resource consumption.

By following this guidance, you can ensure your {{stack}} deployment is robust, efficient, and prepared for production-scale workloads.

::::{note}
* In the context of {{es}} deployments, an `availability zone`, or simply `zone`, represents an isolated failure domain within your infrastructure. Depending on the design of your cluster, this could be a physically separate data center, a different section within the same data center, distinct server racks, or logically separated node groups. The goal of using availability zones is to minimize the risk of a single point of failure affecting the entire deployment.

* For example, in {{ech}}, availability zones correspond to the cloud provider’s availability zones. Each of these is typically a physically separate data center, ensuring redundancy and fault tolerance at the infrastructure level.
::::

## Deployment types

Production guidelines and concepts described in this section apply to all [deployment types](/deploy-manage/deploy.md#choosing-your-deployment-type)-including {{ech}}, {{ece}}, {{eck}}, and self-managed clusters-**except** {{serverless-full}}.

However, certain parts may be relevant only to self-managed clusters, as orchestration systems automate some of the configurations discussed here. Check the headers of each document or section to confirm whether the content applies to your deployment type.

::::{note}
**{{serverless-full}}** projects are fully managed and automatically scaled by Elastic. Your project’s performance and general data retention are controlled by the [Search AI Lake settings](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-ai-lake-settings).
::::

## Section overview

This section is divided into {{es}} and {{kib}} production-ready concepts and best practices.

**{{es}}**

* [](./production-guidance/getting-ready-for-production-elasticsearch.md)
  * [](./production-guidance/availability-and-resilience.md)
    * [](./production-guidance/availability-and-resilience/resilience-in-small-clusters.md)
    * [](./production-guidance/availability-and-resilience/resilience-in-larger-clusters.md)
    * [](./production-guidance/availability-and-resilience/resilience-in-ech.md)
  * [](./production-guidance/scaling-considerations.md)
  * [](./production-guidance/optimize-performance.md)

**{{kib}}**

  * [](./production-guidance/kibana-in-production-environments.md)
    * [](./production-guidance/kibana-task-manager-scaling-considerations.md)
    * [](./production-guidance/kibana-alerting-production-considerations.md)
    * [](./production-guidance/kibana-reporting-production-considerations.md)

## Other sections

Other sections of the documentation provide important guidance for running {{stack}} applications in production.

### Plan your data structure, availability, and formatting [ec_plan_your_data_structure_availability_and_formatting]

* Build a [data architecture](/manage-data/lifecycle/data-tiers.md) that best fits your needs. Based on your own access and retention policies, you can add warm, cold, and frozen data tiers, and automate deletion of old data.
* Make your data [highly available](/deploy-manage/tools.md) for production environments or otherwise critical data stores, and take regular [backup snapshots](./tools/snapshot-and-restore.md), or consider [](./tools/cross-cluster-replication.md) to replicate indices across clusters.
* Normalize event data to better analyze, visualize, and correlate your events by adopting the [Elastic Common Schema](asciidocalypse://docs/ecs/docs/reference/ecs-getting-started.md) (ECS). Elastic integrations use ECS out-of-the-box. If you are writing your own integrations, ECS is recommended.

### Optimize data storage and retention [ec_optimize_data_storage_and_retention]

* Once you have your data tiers deployed and you have data flowing, you can [manage the index lifecycle](/manage-data/lifecycle/index-lifecycle-management.md).

::::{tip}
[Elastic integrations](https://www.elastic.co/integrations) provide default index lifecycle policies, and you can [build your own policies for your custom integrations](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md).
::::

### Security and monitoring [security-and-monitoring] 

As with any enterprise system, you need tools to secure, manage, and monitor your deployments. Security, monitoring, and administrative features that are integrated into {{es}} enable you to use [Kibana](/get-started/the-stack.md) as a control center for managing a cluster.

[Learn about securing an {{es}} cluster](./security.md).

[Learn about monitoring your cluster](./monitor.md).
