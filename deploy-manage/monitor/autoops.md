---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops.html
applies_to:
  serverless:
  deployment:
    ess: all
    self:
    ece:
    eck:
products:
  - id: cloud-hosted
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# AutoOps [ec-autoops]

AutoOps diagnoses issues in {{es}} by analyzing hundreds of metrics, providing root-cause analysis and accurate resolution paths. With AutoOps, customers can prevent and resolve issues, cut down administration time, and optimize resource utilization.

:::{image} /deploy-manage/images/cloud-autoops-overview-page.png
:screenshot:
:alt: Screenshot showing the Overview page in AutoOps
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

## AutoOps availability

In the [regions](/deploy-manage/monitor/autoops/ec-autoops-regions.md) where it has been rolled out, AutoOps is automatically available in [{{ech}} deployments](/deploy-manage/monitor/autoops/ec-autoops-how-to-access.md) and [{{serverless-full}} projects](/deploy-manage/monitor/autoops/autoops-for-serverless.md), and can be set up for [ECE, ECK, and self-managed clusters](/deploy-manage/monitor/autoops/cc-autoops-as-cloud-connected.md).

AutoOps is currently not available for air-gapped environments since it is a cloud service and you need an internet connection to send metrics to {{ecloud}}. However, we plan to offer a locally deployable version in the future.

## AutoOps retention period [ec_autoops_retention_period]

AutoOps currently has a 10 day retention period.


## AutoOps scope [ec_autoops_scope]

AutoOps currently monitors only {{es}}, not the entire {{stack}}. Any deployment information pertains solely to {{es}}. AutoOps is compatible with [supported {{es}} versions](https://www.elastic.co/support/eol)(7.17.x and above). We plan to expand AutoOps monitoring to the entire stack in the future.

## Section overview

In this section, you'll find the following information:

* How to [use AutoOps in your {{ech}} deployments](/deploy-manage/monitor/autoops/ec-autoops-how-to-access.md).
* How to [use AutoOps in your {{serverless-full}} projects](/deploy-manage/monitor/autoops/autoops-for-serverless.md).
* How to [connect your ECE, ECK, or self-managed clusters](/deploy-manage/monitor/autoops/cc-autoops-as-cloud-connected.md) to AutoOps.
* [Regions](/deploy-manage/monitor/autoops/ec-autoops-regions.md) where AutoOps is available.
* What [events](/deploy-manage/monitor/autoops/ec-autoops-events.md) are and how you can configure [event settings](/deploy-manage/monitor/autoops/ec-autoops-event-settings.md) and [notifications](/deploy-manage/monitor/autoops/ec-autoops-notifications-settings.md).
* Which [views](/deploy-manage/monitor/autoops/views.md) AutoOps offers to gain insight into your deployment.
* [Frequently asked questions](/deploy-manage/monitor/autoops/ec-autoops-faq.md) about AutoOps.
