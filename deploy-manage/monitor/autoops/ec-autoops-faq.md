---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-faq.html
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
navigation_title: FAQ
---

# AutoOps FAQ [ec-autoops-faq]

Whether you are using AutoOps in your [{{ech}} deployment](/deploy-manage/monitor/autoops/ec-autoops-how-to-access.md), [{{serverless-short}} project](/deploy-manage/monitor/autoops/autoops-for-serverless.md), or [self-managed cluster](/deploy-manage/monitor/autoops/cc-autoops-as-cloud-connected.md), find answers to some common questions about it on this page.

**General AutoOps questions**
* [What does AutoOps do?](#what-is-autoops)
* [Where is AutoOps available?](#autoops-deployment-types)
* [Why can't I see AutoOps in some deployments and projects?](#cant-see-autoops)
* [How is AutoOps licensed?](#autoops-license)
* [Does AutoOps monitor the entire {{stack}}?](#autoops-monitoring)
* [Can AutoOps automatically resolve issues?](#autoops-issue-resolution)
* [Which versions of {{es}} are supported in AutoOps for {{ech}} and self-managed clusters?](#autoops-supported-versions)
* [How long does Elastic retain AutoOps data?](#autoops-data-retention)
* [Where are AutoOps metrics stored, and does AutoOps affect customer ECU usage?](#autoops-metrics-storage)
* [Has AutoOps replaced Stack Monitoring?](#autoops-vs-stack-monitoring)

**Questions about AutoOps for self-managed clusters**
* [Does AutoOps for self-managed clusters incur additional costs?](#additional-payment)
* [Does shipping metrics data to {{ecloud}} incur additional costs?](#autoops-metrics-cost)
* [Which deployment types can be connected to AutoOps through Cloud Connect?](#deployment-types)

**Setting up AutoOps for self-managed clusters**
* [Can I use Cloud Connect to connect my {{ech}} clusters to AutoOps?](#cc-autoops-ech)
* [Can I use AutoOps for my clusters if my environment is air-gapped?](#autoops-air-gapped)
* [Can I use macOS to install {{agent}} for this feature?](#macos-install)
* [Do I have to define an Elastic IP address to enable the agent to send data to {{ecloud}}?](#elastic-ip-address)

**Collected metrics and data in AutoOps for self-managed clusters**
* [Where are metrics stored in AutoOps for self-managed clusters?](#sm-autoops-metrics-storage)
* [What information does {{agent}} gather from my cluster?](#extracted-info)
* [How does AutoOps gather data from my cluster and ensure its security?](#data-gathering)
* [Can I view the data gathered by {{agent}}?](#data-viewing-config)

## General AutoOps questions

$$$what-is-autoops$$$**What does AutoOps do?**
:   AutoOps for {{es}} simplifies cluster management by providing performance recommendations, resource utilization and cost insights, real-time issue detection, and resolution paths. By analyzing hundreds of {{es}} metrics, your configuration, and usage patterns, AutoOps provides operational and monitoring recommendations that reduce administration time and hardware costs.

$$$autoops-deployment-types$$$**Where is AutoOps available?**
:   In the [regions](ec-autoops-regions.md) where it has been rolled out, AutoOps is automatically available in [{{ech}} deployments](/deploy-manage/monitor/autoops/ec-autoops-how-to-access.md) and can be set up for [ECE, ECK, and self-managed clusters](/deploy-manage/monitor/autoops/cc-autoops-as-cloud-connected.md) through [Cloud Connect](/deploy-manage/cloud-connect.md). 

$$$cant-see-autoops$$$**Why can't I see AutoOps in some deployments and projects?**
AutoOps is rolling out in phases across CSPs and [regions](/deploy-manage/monitor/autoops/ec-autoops-regions.md), so you may not see it if your deployment or project is in a region where AutoOps is not available yet. AutoOps is currently not available in Azure and GCP.

$$$autoops-license$$$**How is AutoOps licensed?**
:   For {{ech}} deployments and {{serverless-short}} projects, AutoOps is available to {{ecloud}} customers at all subscription levels at no additional cost, and it does not consume ECU.
    :::{include} /deploy-manage/_snippets/autoops-cc-payment-faq.md
    ::: 

$$$autoops-monitoring$$$**Does AutoOps monitor the entire {{stack}}?**
:   AutoOps is currently limited to {{es}} (not {{kib}}, Logstash, or Beats).

$$$autoops-issue-resolution$$$**Can AutoOps automatically resolve issues?**
:   AutoOps only analyzes metrics and is a read-only solution.

$$$autoops-supported-versions$$$**Which versions of {{es}} are supported in AutoOps for {{ech}} and self-managed clusters?**
:   AutoOps is compatible with [supported {{es}} versions](https://www.elastic.co/support/eol) (7.17.x and above).

$$$autoops-data-retention$$$**How long does Elastic retain AutoOps data?**
:   AutoOps has a 10 day retention period.

$$$autoops-metrics-storage$$$**Where are AutoOps metrics stored, and does AutoOps affect customer ECU usage?**
:   AutoOps metrics are stored internally within the Elastic infrastructure, not on customer deployments. Using AutoOps does not consume customer ECU.

$$$autoops-vs-stack-monitoring$$$**Has AutoOps replaced Stack Monitoring?**
:   Currently, AutoOps has many of the same features as Stack Monitoring as well as several new ones. However, it only provides insights on {{es}} and analyzes metrics, not logs. Read more in [](/deploy-manage/monitor/autoops-vs-stack-monitoring.md).

## Questions about AutoOps for self-managed clusters

$$$additional-payment$$$ **Does AutoOps for self-managed clusters incur additional costs?**
:   :::{include} /deploy-manage/_snippets/autoops-cc-payment-faq.md
::: 

$$$autoops-metrics-cost$$$ **Does shipping metrics data to {{ecloud}} incur additional costs?**
:   Elastic does not charge extra for this service, but your cloud service provider (CSP) might. When sending metrics data from your cluster in a CSP region to {{ecloud}}, shipping costs are determined by your agreement with that CSP. 

    You can [choose the CSP region where your data is stored](#sm-autoops-metrics-storage).

$$$deployment-types$$$ **Which deployment types can be connected to AutoOps through Cloud Connect?**
:   You can connect to AutoOps on a standalone {{stack}}, ECE ({{ece}}), or ECK ({{eck}}) deployment, both on-premise and in private cloud environments.

### Setting up AutoOps for self-managed clusters

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

### Collected metrics and data in AutoOps for self-managed clusters

$$$sm-autoops-metrics-storage$$$ **Where are metrics stored in AutoOps for self-managed clusters?**
:   You can choose where to store your metrics from the following AWS regions:

    :::{include} ../_snippets/autoops-cc-regions.md
    :::

$$$extracted-info$$$ **What information does {{agent}} gather from my cluster?**
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

    Each channel is authenticated using an API key or token to ensure your data's security. The following table offers more details: 

    | Protocol | Data extracted | Port | Authentication method | 
    | --- | --- | --- | --- |
    | HTTP |  Basic cluster information from the `/` endpoint <br><br> License information from the `/_license` endpoint | **443**: standard HTTPS port | Uses an {{ecloud}} API key which is limited for use with Cloud Connect only. |
    | OTLP over HTTP | Operational information | **443**: standard HTTPS port | Uses an AutoOps token which is functionally equivalent to an API key. |

$$$data-viewing-config$$$**Can I view the data gathered by {{agent}}?**
:   You can use the `autoops_es_debug.yaml` config file to export and review a sample of the data gathered from your cluster and sent to Elastic Cloud.