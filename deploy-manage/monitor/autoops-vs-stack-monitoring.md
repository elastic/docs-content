---
applies_to:
  serverless:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
navigation_title: AutoOps vs. Stack Monitoring
products:
  - id: cloud-hosted
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# AutoOps and Stack Monitoring comparison

This page provides a detailed comparison of AutoOps and Stack Monitoring to help you decide which solution is better suited to your needs.

## Review the main differences
Review how these tools differ in their provisioning, set up procedure, method of access, and capabilities.

### Resource provisioning and billing

#### AutoOps [ao-resource]
AutoOps stores and backs up your monitoring data internally on {{ecloud}} infrastructure so you don’t need to think about provisioning, sizing, and availability. The data is retained for 10 days by default. Using AutoOps is free for {{ecloud}} customers and is offered to [all subscription tiers](https://www.elastic.co/subscriptions/cloud).

#### Stack Monitoring [sm-resource]
With Stack Monitoring, you are responsible for storing your monitoring data. This requires provisioning the necessary resources based on your performance and retention needs as well as paying for the allocated resources. The default retention period is six days.

### Setup

#### AutoOps [ao-setup]
On {{ech}} and {{serverless-full}}, AutoOps is set up and enabled automatically in all supported [regions](/deploy-manage/monitor/autoops/ec-autoops-regions.md), with no action required from you.

:::{image} /deploy-manage/images/cloud-autoops-setup.png
:alt: Diagram showing AutoOps setup in Elastic Cloud
:::

For {{ece}} (ECE), {{eck}} (ECK), and self-managed clusters, you need to [connect your cluster to AutoOps](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md). This involves installing {{agent}} to ship your monitoring metrics to {{ecloud}} through [](/deploy-manage/cloud-connect.md). Since you can only access AutoOps from the {{ecloud}} UI, you need an {{ecloud}} account for this service.

:::{image} /deploy-manage/images/self-managed-autoops-setup.png
:alt: Diagram showing AutoOps setup for ECE, ECK, and self-managed clusters
:::

:::{note}
AutoOps will be available for self-managed air-gapped environments (ECE, ECK, or standard stack deployments) in the future.
:::

#### Stack Monitoring [sm-setup]
Stack Monitoring is a {{kib}} application that can be enabled on self-managed clusters on your premises, {{ech}} deployments, {{ece}} (ECE), and {{eck}} (ECK). Stack Monitoring is not available on {{serverless-full}} since Elastic takes care of monitoring and managing your {{serverless-short}} projects.

Depending on your deployment model, there is [some setting up](/deploy-manage/monitor/stack-monitoring.md#configure-and-use-stack-monitoring) involved to enable Stack Monitoring. You need to configure an agent, specify which logs and metrics you want to collect from all your {{stack}} components, and where to send them.

You can store your Stack Monitoring logs and metrics in the following ways:

* Within the monitored cluster itself:

  :::{image} /deploy-manage/images/stack-monitoring-self-monitoring-cluster-setup.png
  :alt: Diagram showing Stack Monitoring setup on a self-monitoring cluster in Elastic Cloud
  :::

* Within a dedicated monitoring cluster, if you are concerned about resiliency and availability:

  :::{image} /deploy-manage/images/stack-monitoring-dedicated-cluster-setup.png
  :alt: Diagram showing Stack Monitoring setup on a dedicated monitoring cluster in Elastic Cloud
  :::

### Availability

#### AutoOps [ao-availability]
AutoOps lives in {{ecloud}}, so you need to have an {{ecloud}} account to access it. Once logged in, you can access AutoOps from your [{{ech}} deployments](/deploy-manage/monitor/autoops/ec-autoops-how-to-access.md), [{{serverless-short}} projects](/deploy-manage/monitor/autoops/access-autoops-for-serverless.md), or [connect your self-managed clusters](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md) to it.

#### Stack Monitoring [sm-availability]
Once setup is complete, you can access the Stack Monitoring UI inside {{kib}}, where you can monitor all your {{stack}} components.

### Investigations and root cause analysis

#### AutoOps [ao-investigations]
The AutoOps agent captures a pre-defined set of {{es}} metrics, but doesn’t fetch any logs. AutoOps then performs multi-metrics analysis and correlations to identify issues and potential root causes. When issues are detected, AutoOps raises [events](/deploy-manage/monitor/autoops/ec-autoops-events.md) and [notifies](/deploy-manage/monitor/autoops/ec-autoops-notifications-settings.md) you accordingly. When the issue is resolved, AutoOps automatically closes the event.

For each raised event, AutoOps provides insights into the affected resources (cluster, node, index, shard, etc.), background information on the detected problem, and step-by-step guides to help you diagnose and remediate the identified issues. Most detection rules can be [customized](/deploy-manage/monitor/autoops/ec-autoops-event-settings.md) by adjusting thresholds, durations, index patterns, data tiers, and more.

#### Stack Monitoring [sm-investigations]
The Stack Monitoring UI displays the [metrics](/deploy-manage/monitor/monitoring-data/elasticsearch-metrics.md) of your monitored {{stack}} components over time. Logs can be viewed, searched, and filtered in Discover. You can enable a pre-defined set of alerts that are triggered when specific thresholds are crossed. You can also configure your own [alerts](/deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md) on any collected metrics or log messages. However, Stack Monitoring does not offer any further investigation, correlations, or root cause analyses.

## Compare capabilities
The following tables provide a detailed comparison of AutoOps and Stack Monitoring features.

### AutoOps-only features
The following features are only available in AutoOps.

| Features | AutoOps | Stack Monitoring | Description |
|---|---|---|---|
| **Elasticsearch** | | | |
| Pre-built customizable alerts | ✅ | ❌ | AutoOps offers hundreds of multi-metric customizable alerts on {{es}} specific issues. Stack Monitoring supports some pre-built alerts, but you can build more if needed. |
| Multi metrics analysis | ✅ | ❌ | Advanced detection rules built on multiple metrics. |
| Performance tuning insights | ✅ | ❌ | Insights on tuning configurations and data structures for better {{es}} performance. |
| Root cause analysis | ✅ | ❌ | Identification of what went wrong including identifying the affected resources (clusters, nodes, indices, shards). |
| Resolution paths | ✅ | ❌ | Recommendations and suggestions to mitigate detected problems. |
| Knowledge base | ✅ | ❌ | Embedded knowledge base including links to articles and more information. |
| Multi-cluster dashboard | ✅ | ❌ | AutoOps dashboard is better equipped to handle a large number of clusters compared to the Clusters listing page in Stack Monitoring. |
| Events timeline | ✅ | ❌ | Comprehensive timeline of all raised events, organized by severity. |
| Data-tier specific insights | ✅ | ❌ | Visibility into data-tier resource utilization and performance insights per data tier. |
| Node-to-node comparison | ✅ | ❌ | Nodes listing and details combined into the same view for easier node-to-node resource and performance comparison. |
| Index-to-index comparison | ✅ | ❌ | Index listing and details combined into the same view for easier index-to-index resource and performance comparison. |
| Shards load heatmap | ✅ | ❌ | Node/index matrix showing shard activity on different selectable metrics. |
| Template optimizer | ✅ | ❌ | Template/mapping analysis. |
| Slow DSL query analysis | ✅ | ❌ | Identification of reasons for increased latency for DSL queries. |
| Advanced customizations | ✅ | ❌ | Customization and dismissal of detection rules on specific deployments. |
| Notification history | ✅ | ❌ | Comprehensive and curated notification history and reports. |

### Common features
The following features are common between AutoOps and Stack Monitoring, sometimes with slight variations.

| Features | AutoOps | Stack Monitoring | Description |
|---|---|---|---|
| **Elasticsearch** | | | |
| Clusters listing | ✅ | ✅ | Listing of all monitored clusters. |
| Cluster overview | ✅ | ✅ | Overview of each monitored cluster. |
| ES overview | ✅ | ✅ | Cluster-level performance metrics. |
| ES nodes list | ✅ | ✅ | Listing of all Elasticsearch nodes. |
| ES node details | ✅ | ✅ | Details on a specific node. |
| ES indices list | ✅ | ✅ | Listing of all {{es}} indices. AutoOps allows sorting indices by search and indexing latency metrics, but Stack Monitoring doesn’t, making it difficult to identify slow indices. |
| ES index details | ✅ | ✅ | Details on a specific index. |
| Single metric detection | ✅ | ✅ | Basic single-metric detection rules. |
| Simple alert customization | ✅ | ✅ | Basic customization of alerts. |
| Alerts and notifications | ✅ | ✅ | Stack Monitoring provides [27 configurable connectors](kibana://reference/connectors-kibana.md) for alerts and notifications. AutoOps supports [7 of them](/deploy-manage/monitor/autoops/ec-autoops-notifications-settings.md#ec-built-in-connectors) and the email connector doesn’t require setting up an email server. |

### Stack Monitoring-only features (coming soon to AutoOps) 
The following features are currently only available in Stack Monitoring. These features will be available in AutoOps over time and any new features will primarily be added to AutoOps.

| Features | AutoOps | Stack Monitoring | Description |
|---|---|---|---|
| **Elasticsearch** | | | |
| Ingest pipeline | ❌ | ✅ | Stack Monitoring supports ingest pipeline monitoring via a link to ad hoc dashboards. These are provided by the {{agent}} {{es}} integration which needs to be installed. |
| CCR | ❌ | ✅ | Insights into CCR metrics. |
| Machine Learning jobs | ❌ | ✅ | Insights into ML job statistics. |
| Raw monitoring data | ❌ | ✅ | Availability of raw monitoring data. |
| **Other Stack components** | | | |
| Basic {{kib}} monitoring | ❌ | ✅ | More advanced {{kib}} monitoring is coming soon to AutoOps. |
| Basic Logstash monitoring | ❌ | ✅ | Logstash monitoring in the Stack Monitoring UI has been [superseded](logstash://reference/monitoring-logstash-with-elastic-agent.md) by the ad hoc dashboards shipped via the {{agent}} Logstash integration. |
| Basic APM server monitoring | ❌ | ✅ | Standard monitoring of APM servers |
| Basic integration server monitoring | ❌ | ✅ | Standard monitoring of integration servers |

## Choose between AutoOps and Stack Monitoring

Keep using Stack Monitoring if you:

* are running the {{stack}} on-premise, air-gapped or otherwise
* need to control monitoring data retention
* need monitoring coverage for {{stack}} components other than {{es}}
* have deployments in a region where AutoOps is not available yet

Start using AutoOps if you want:

* easier monitoring of your {{ecloud}} deployments
* clear guidance and troubleshooting advice when issues arise
* to efficiently monitor a large number of deployments
* a comprehensive picture of the historical health of your deployments
* your events and alerts to be highly customizable
* an advanced notification system tailored for specific clusters and alert conditions
* simplified interactions with Elastic Support


