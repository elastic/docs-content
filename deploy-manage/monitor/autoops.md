---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops.html
applies_to:
  deployment:
    ess: all
---

# AutoOps [ec-autoops]

AutoOps diagnoses issues in Elasticsearch by analyzing hundreds of metrics, providing root-cause analysis and accurate resolution paths. With AutoOps, customers can prevent and resolve issues, cut down administration time, and optimize resource utilization.

:::{image} ../../images/cloud-autoops-overview-page.png
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

AutoOps currently has a four-day retention period for all Cloud Hosted customers.


## AutoOps scope [ec_autoops_scope]

AutoOps currently monitors only {{es}}, not the entire {{stack}}. Any deployment information pertains solely to {{es}}. AutoOps supports {{es}} version according to the [supported Elastic Stack versions](https://www.elastic.co/support/eol). There are plans to expand AutoOps monitoring to the entire stack.














