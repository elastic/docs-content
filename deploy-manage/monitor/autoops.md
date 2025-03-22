---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops.html
applies_to:
  deployment:
    ess: all
---

# AutoOps [ec-autoops]

AutoOps diagnoses issues in Elasticsearch by analyzing hundreds of metrics, providing root-cause analysis and accurate resolution paths. With AutoOps, customers can prevent and resolve issues, cut down administration time, and optimize resource utilization.

AutoOps is currently only available for [{{ech}} deployments](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md).

:::{image} /deploy-manage/images/cloud-autoops-overview-page.png
:alt: The Overview page
:::


## AutoOps key features [ec_autoops_key_features]

* Real-time root-cause analysis for hundreds of issues.
* Accurate resolution paths and customized recommendations.
* Insight into what occurred and detailed views into nodes, index, shards, and templates.
* Wide range of insights, including:

    * Cluster status, node failures, and shard sizes.
    * High CPU, memory, disk usage, and other resource-related metrics.
    * Misconfigurations and possible optimizations.
    * Insights on data structure, shards, templates, and mapping optimizations.
    * Unbalanced loads between nodes.
    * Indexing latency, rejections, search latency, high index/search queues, and slow queries.
    * Resource utilization.



## Additional capabilities [ec_additional_capabilities]

* Multi-deployment dashboard to quickly spot issues across all clusters.
* Possibility to customize event triggers and connect to different notification services such as PagerDuty, Slack, MS Teams, and webhooks.
* Long-term reports for sustained evaluation. This feature is currently not available and will be rolled out shortly.


## AutoOps retention period [ec_autoops_retention_period]

AutoOps currently has a four-day retention period for all {{ech}} customers.


## AutoOps scope [ec_autoops_scope]

AutoOps currently monitors only {{es}}, not the entire {{stack}}. Any deployment information pertains solely to {{es}}. AutoOps supports {{es}} versions according to the [supported {{es}} versions](https://www.elastic.co/support/eol). There are plans to expand AutoOps monitoring to the entire stack.


## Section overview

In this section, you'll find the following information:

* How to [open AutoOps](/deploy-manage/monitor/autoops/ec-autoops-how-to-access.md) for your deployment.
* The contents of [AutoOps events](/deploy-manage/monitor/autoops/ec-autoops-events.md).
* The [views](/deploy-manage/monitor/autoops/views.md) AutoOps offers to gain insight into facets of your deployment.
* [Notification settings](/deploy-manage/monitor/autoops/ec-autoops-notifications-settings.md) that allow you to specify when and how to be notified.
* [Event settings](/deploy-manage/monitor/autoops/ec-autoops-event-settings.md) that allow you to fine-tune when events are triggered, and a method to [dismiss](/deploy-manage/monitor/autoops/ec-autoops-dismiss-event.md) certain categories of events.
* The [regions](/deploy-manage/monitor/autoops/ec-autoops-regions.md) where AutoOps is available.
* Additional [frequently asked questions](/deploy-manage/monitor/autoops/ec-autoops-faq.md).
