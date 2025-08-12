---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: FAQ
---

# AutoOps for self-managed clusters FAQ

Find answers to your questions about AutoOps for ECE, ECK, and self-managed clusters.

:::{dropdown} Why should I use AutoOps for my clusters?

AutoOps simplifies the operation of your {{es}} clusters by providing real-time monitoring, performance insights, and issue detection. It helps you identify and resolve problems like ingestion bottlenecks and unbalanced shards, reducing manual effort and preventing performance issues. 

When you need support, AutoOps gives the Elastic team real-time visibility into your cluster, leading to faster resolutions. 

Using AutoOps for your ECE, ECK, and self-managed clusters lets you access all these capabilities without the operational overhead of managing their infrastructure.
:::

:::{dropdown} Does this feature require additional payment?

:::{include} /deploy-manage/_snippets/autoops-cc-payment-faq.md
:::

:::

:::{dropdown} Which versions of {{es}} does AutoOps support?

AutoOps is compatible with all [supported {{es}} versions](https://www.elastic.co/support/eol).
:::

:::{dropdown} Which deployment types can be connected to AutoOps?

You can connect to AutoOps on a standalone {{stack}}, ECE ({{ece}}), or ECK ({{eck}}) deployment.
:::

:::{include} /deploy-manage/_snippets/autoops-cc-ech-faq.md
:::

:::{dropdown} Can I use AutoOps for my clusters if my environment is air-gapped?

Not at this time. AutoOps is currently only available as a cloud service and you need an internet connection to send metrics to {{ecloud}}. For air-gapped environments, we plan to offer a locally deployable version in the future.
:::

:::{dropdown} Can I use macOS to install {{agent}} for this feature?

macOS is not a supported platform for installing {{agent}} and connecting your clusters to AutoOps.
:::

:::{dropdown} Do I have to define an Elastic IP address to enable the agent to send data to {{ecloud}}?

You may need to define an IP address if your organization’s settings will block the agent from sending out data. 

To enable IP ranges, {{ecloud}} offers a selection of static IP addresses. All traffic directed to {{ecloud}} deployments, whether originating from the public internet, your private cloud network through the public internet, or your on-premise network through the public internet utilizes Ingress Static IPs as the network destination. 

For more information, refer to [](/deploy-manage/security/elastic-cloud-static-ips.md).
:::

:::{dropdown} Where are AutoOps metrics stored, and does it cost extra to ship metrics to {{ecloud}}?

You can choose the CSP and region in which your cluster metrics will be stored from a list of [available regions](/deploy-manage/monitor/autoops/ec-autoops-regions.md). 

Shipping metrics to {{ecloud}} may come at an additional cost. For example, when sending metrics data from your cluster in a CSP region to {{ecloud}}, shipping costs will be determined by your agreement with that CSP.
:::

:::{dropdown} What information does {{agent}} extract from my cluster?

{{agent}} only extracts and sends cluster metrics to {{ecloud}}, not the underlying data within your cluster. The following metrics are collected:

| API | Description | Collected data |
| --- | --- | --- |
| [_cat/shards](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-shards) | Returns detailed information about the shards within the cluster | Shard states, node allocation, index names, sizes, and replica information |
| [_nodes/stats](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats) | Retrieves statistics from cluster nodes including JVM, OS, process, and transport metrics | CPU usage, memory utilization, thread pools, file system stats |
| [_cluster/settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-settings) | Returns the settings configured for the cluster | Persistent and transient settings such as cluster-wide configurations |
| [_cluster/health](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health) | Provides information about the overall health of the cluster | Status (green/yellow/red), number of nodes, number of shards |
| [_cat/template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-templates) | Lists all index templates in the cluster | Template names, patterns, and basic settings |
| [_index_template](/manage-data/data-store/templates.md) | Retrieves composable index templates | Index settings, mappings, and aliases |
| [_component_template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-component-template) | Fetches component templates used for building index templates | Metadata for re-usable mappings and settings |
| [_tasks](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-tasks) | Displays information about currently running tasks on the cluster | Task descriptions, start times, running nodes, and execution details |
| [_template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-template) | Retrieves legacy index templates | Similar to composable index templates but in older format |
| [_resolve/index/*](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-resolve-index) | Resolves index, data stream, and alias names to their current definitions | Mappings between names and underlying data objects |
:::


