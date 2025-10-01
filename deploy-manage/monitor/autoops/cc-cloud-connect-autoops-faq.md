---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: FAQ
products:
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# AutoOps for self-managed clusters FAQ

Find answers to your questions about AutoOps for ECE, ECK, and self-managed clusters.

**General questions**
* [Why should I use AutoOps for my clusters?](#why-autoops)
* [Does this feature require additional payment?](#additional-payment)
* [Is there an added cost for shipping metrics data to {{ecloud}}?](#autoops-metrics-cost)
* [Which versions of {{es}} does AutoOps support?](#es-versions)
* [Which deployment types can be connected to AutoOps through Cloud Connect?](#deployment-types)

**Questions about setting up**
* [Can I use Cloud Connect to connect my {{ech}} clusters to AutoOps?](#cc-autoops-ech)
* [Can I use AutoOps for my clusters if my environment is air-gapped?](#autoops-air-gapped)
* [Can I use macOS to install {{agent}} for this feature?](#macos-install)
* [Do I have to define an Elastic IP address to enable the agent to send data to {{ecloud}}?](#elastic-ip-address)

**Questions about collected metrics and data**
* [Where are AutoOps metrics stored?](#autoops-metrics-storage)
* [What information does {{agent}} extract from my cluster?](#extracted-info)
* [How does AutoOps gather data from my cluster and ensure its security?](#data-gathering)

## General questions
$$$why-autoops$$$ **Why should I use AutoOps for my clusters?** 
:   AutoOps simplifies the operation of your {{es}} clusters by providing real-time monitoring, performance insights, and issue detection. It helps you identify and resolve problems like ingestion bottlenecks and unbalanced shards, reducing manual effort and preventing performance issues. 

$$$additional-payment$$$ **Does this feature require additional payment?**
:   :::{include} /deploy-manage/_snippets/autoops-cc-payment-faq.md
::: 

$$$autoops-metrics-cost$$$ **Is there an added cost for shipping metrics data to {{ecloud}}?**
:   Elastic does not charge extra for this service, but your cloud service provider (CSP) might. When sending metrics data from your cluster in a CSP region to {{ecloud}}, shipping costs will be determined by your agreement with that CSP. 

    You can [choose the CSP region where your data is stored](#autoops-metrics-storage). 

$$$es-versions$$$ **Which versions of {{es}} does AutoOps support?**
:   AutoOps is compatible with [supported {{es}} versions](https://www.elastic.co/support/eol) (7.17.x and above).

$$$deployment-types$$$ **Which deployment types can be connected to AutoOps through Cloud Connect?**
:   You can connect to AutoOps on a standalone {{stack}}, ECE ({{ece}}), or ECK ({{eck}}) deployment.

## Questions about setting up
$$$cc-autoops-ech$$$ **Can I use Cloud Connect to connect my {{ech}} clusters to AutoOps?**
:   :::{include} /deploy-manage/_snippets/autoops-cc-ech-faq.md
:::

$$$autoops-air-gapped$$$ **Can I use AutoOps for my clusters if my environment is air-gapped?**
:   Not at this time. AutoOps is currently only available as a cloud service and you need an internet connection to send metrics to {{ecloud}}. For air-gapped environments, we plan to offer a locally deployable version in the future.

$$$macos-install$$$ **Can I use macOS to install {{agent}} for this feature?**
:   macOS is not a supported platform for installing {{agent}} and connecting your clusters to AutoOps.

$$$elastic-ip-address$$$ **Do I have to define an Elastic IP address to enable the agent to send data to {{ecloud}}?**
:   You may need to define an IP address if your organization’s settings will block the agent from sending out data. 

    To enable IP ranges, {{ecloud}} offers a selection of static IP addresses. All traffic directed to {{ecloud}} deployments, whether originating from the public internet, your private cloud network through the public internet, or your on-premise network through the public internet utilizes Ingress Static IPs as the network destination. 

:   For more information, refer to [](/deploy-manage/security/elastic-cloud-static-ips.md).

## Questions about collected metrics and data
$$$autoops-metrics-storage$$$ **Where are AutoOps metrics stored?**
:   You can choose where to store your metrics from the following AWS regions:

    :::{include} ../_snippets/autoops-cc-regions.md
    :::

$$$extracted-info$$$ **What information does {{agent}} extract from my cluster?**
:   {{agent}} only extracts and sends cluster metrics to {{ecloud}}, not the underlying data within your cluster. The following metrics are collected:

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

$$$data-gathering$$$ **How does AutoOps gather data from my cluster and ensure its security?**
:   AutoOps gathers data from your cluster using two protocols:
    * **HTTP request**: Made to our Cloud Connected API to register your cluster with {{ecloud}} and gather registration-related data.
    * **OpenTelemetry Protocol (OTLP)**: Used to gather all other operational data.

    Each channel is authenticated through an API key or token to ensure your data's security. The following table offers more details: 

    | Protocol | Data extracted | Port | Authentication method | 
    | --- | --- | --- | --- |
    | HTTP |  Basic cluster information from the `/` endpoint <br><br> License information from the `/_license` endpoint | **443**: standard HTTPS port | Uses an {{ecloud}} API key which is limited for use with Cloud Connect only. |
    | OTLP over HTTP | Operational information | **443**: standard HTTPS port | Uses an AutoOps token which is functionally equivalent to an API key. |
