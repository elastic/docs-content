---
navigation_title: Run Elasticsearch in production
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/scalability.html
  - https://www.elastic.co/guide/en/cloud/current/ec-planning.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-planning.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
---

% pending to determine if we should link to Kibana-load-balancing across multiple ES nodes from the es prod docs
% pending to link reference architectures

# Run {{es}} in production [scalability]

Many teams rely on {{es}} to run their key services. To ensure these services remain available and responsive under production workloads, you can design your deployment with the appropriate level of resilience, and apply performance optimizations tailored to your environment and use case.

{{es}} is built to be always available and to scale with your needs. It does this using a [distributed architecture](/deploy-manage/distributed-architecture.md). By distributing your cluster, you can keep Elastic online and responsive to requests.

In cases where built-in resilience mechanisms aren't enough, {{es}} offers tools—such as [cross-cluster replication](../tools/cross-cluster-replication.md) and [snapshot and restore](../tools/snapshot-and-restore.md)—to help you fall back or recover quickly. You can also use cross-cluster replication to serve requests based on the geographic location of your users and resources.

{{es}} also offers [authentication and authorization](/deploy-manage/users-roles.md), [security](/deploy-manage/security.md) and [monitoring tools](/deploy-manage/monitor.md) to help you keep your cluster highly available and secure.

In this section you'll learn (TBD, work in progress):

* [Designing for resilience](./availability-and-resilience.md)

  When you move to production, you need to introduce multiple nodes and shards to your cluster.
  
  Nodes and shards are what make {{es}} [resilient](./availability-and-resilience.md) and [scalable](./scaling-considerations.md).
  
  The size and number of these nodes and [shards](./optimize-performance/size-shards.md) depends on your data, your use case, and your budget.

* [Scaling considerations](./scaling-considerations.md)

* [Performance optimizations](./optimize-performance.md) 

::::{important}
In orchestrated deployments, some of the settings mentioned in the referenced documents may not apply. Check the section headers to determine whether a topic is relevant to your deployment type.
::::

TBD / decide what to do with these sentences:

Many {{es}} options come with different performance considerations and trade-offs. The best way to determine the optimal configuration for your use case is through [testing with your own data and queries](https://www.elastic.co/elasticon/conf/2016/sf/quantitative-cluster-sizing).

Learn more about [nodes and shards](../distributed-architecture/clusters-nodes-shards.md) and [reference architectures](/deploy-manage/reference-architectures.md).


## Responsibilities and deployment types

Your responsibilities when running {{es}} in production depend on the [deployment type](/deploy-manage/deploy.md#choosing-your-deployment-type). Depending on the platform, some aspects—like scaling or cluster configuration—are managed for you, while others may require your attention and knowledge:

* **Self-managed {{es}}**: You are responsible for setting up and managing nodes, clusters, shards, and replicas. This includes managing the underlying infrastructure, scaling, and ensuring high availability through failover and backup strategies.

* **{{ech}}**: Elastic can [autoscale](../autoscaling.md) resources in response to workload changes. Choose from different hardware profiles and deployment architectures to apply sensible defaults for your use case. A good understanding of nodes, shards, and replicas is important, as you are still responsible for managing your data and ensuring cluster performance.

* **{{serverless-full}}**: You don’t need to worry about nodes, shards, or replicas. These resources are 100% automated on the serverless platform, which is designed to scale with your workload.

  Your project’s performance and general data retention are controlled by the [Search AI Lake settings](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-ai-lake-settings).

  ::::{note}
  For {{ech}} and {{serverless-short}} refer to [shared responsibility](https://www.elastic.co/cloud/shared-responsibility)
  ::::

* **{{ece}}**: (TBD)

* **{{eck}}**: ECK is a self-managed orchestrator.

## Other sections

Other sections of the documentation offer valuable guidance and recommendations for running {{es}} in production.

### Plan your data structure and formatting [ec_plan_your_data_structure_availability_and_formatting]

* Build a [data architecture](/manage-data/lifecycle/data-tiers.md) that best fits your needs. Based on your own access and retention policies, you can add warm, cold, and frozen data tiers, and automate deletion of old data.
* Normalize event data to better analyze, visualize, and correlate your events by adopting the [Elastic Common Schema](asciidocalypse://docs/ecs/docs/reference/ecs-getting-started.md) (ECS). Elastic integrations use ECS out-of-the-box. If you are writing your own integrations, ECS is recommended.

### Optimize data storage and retention [ec_optimize_data_storage_and_retention]

Besides the optimizations suggested in [](./optimize-performance/disk-usage.md):

* Once you have your data tiers deployed and you have data flowing, you can [manage the index lifecycle](/manage-data/lifecycle/index-lifecycle-management.md).

::::{tip}
[Elastic integrations](https://www.elastic.co/integrations) provide default index lifecycle policies, and you can [build your own policies for your custom integrations](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md).
::::

### Security and monitoring [security-and-monitoring] 

As with any enterprise system, you need tools to secure, manage, and monitor your deployments. Security, monitoring, and administrative features that are integrated into {{es}} enable you to use [Kibana](/get-started/the-stack.md) as a control center for managing a cluster.

* [Learn about securing an {{es}} cluster](../security.md)

* [Learn about authentication and authorization in {{es}} and {{kib}}](../users-roles.md)

* [Learn about monitoring your cluster](../monitor.md)
