---
navigation_title: Deployment or Cluster
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-deployment-view.html
applies_to:
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

# Deployment or Cluster view in AutoOps [ec-autoops-deployment-view]

The **Deployment** view (for {{ECH}} deployments) or **Cluster** view (for ECE, ECK, and self-managed clusters), is the event control panel that allows you to see which issues are affecting the {{es}} cluster and get a list of action items to address them.

## Events over time [ec-autoops-events-over-time]

The **Events Over Time** panel lists all the recent events the {{es}} cluster has triggered, ordered by criticality. It also gives a color-coded heat map to help understand when and how often a particular event happened. Click on any mosaic to get details about a particular event, for example the specific node/index/shard affected, event time and duration, and a detailed description of the actions you can take to mitigate that event.

Refer to [AutoOps events](ec-autoops-events.md) for more details.


## Open events [ec-autoops-open-events]

The **Open Events** panel lists open events sorted by severity and time. When the conditions that triggered the event no longer exist, the event is automatically set to close and appear in the **Events History** panel. Closing an event does not necessarily indicate that the customer resolved the issue, but rather that AutoOps no longer detects it.


## Events History [ec-events-history]

The **Events History** panel lists events that happened at some point and that have been triggered, but some conditions changed and are no longer active. For example, when your cluster experiences a peak in search rate, that might trigger a "Too many tasks on queue" event. Now, your cluster is more relaxed in terms of search rate, so this event is no longer an issue, but it was recorded for historical reasons. Events history is also sorted by severity first and then by time.


## Resources [ec-deployment-resources]

The **Resources** panel provides a quick overview of {{es}} cluster resource usage. The resources are presented based on their respective data tiers and include JVM memory usage, CPU usage, and storage usage over time. You can view essential cluster information such as the {{es}} version, total number of nodes, total number of shards, and total volume of used storage.

:::{image} /deploy-manage/images/cloud-autoops-deployment-resources.png
:screenshot:
:alt: Screenshot showing the Resources panel in the AutoOps Deployment or Cluster view
:::


## Performance [ec-deployment-performance]

The **Performance** panel shows key performance metrics, aggregated at both the cluster level and the selected tier levels:

:::{image} /deploy-manage/images/cloud-autoops-deployment-performance.png
:screenshot:
:alt: Screenshot showing the Performance panel in the AutoOps Deployment or Cluster view
:::

* **Search rate**: The number of search requests executed per second across all shards in the deployment or cluster, as well as within the selected data tiers.
* **Search latency**: The average latency of search operations across all shards in the deployment or cluster, and within the selected data tiers.
* **Indexing rate**: The number of documents indexed per second across all shards in the deployment or cluster, as well as within the selected data tiers.
* **Indexing latency**: The average latency of indexing operations across all shards in the deployment or cluster, and within the selected data tiers.
