---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-best-practices-data.html
---

# Production guidance [ec-best-practices-data]

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


