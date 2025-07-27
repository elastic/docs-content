---
applies_to:
  deployment:
    self:
navigation_title: FAQ
---

# Cloud connected AutoOps FAQ

Find answers to your questions about AutoOps as a cloud connected service.

:::{dropdown} Why should I use AutoOps with Cloud Connect?

$$$cc-autoops-why$$$

AutoOps simplifies the operation of your {{es}} clusters by providing real-time monitoring, performance insights, and issue detection. It helps you identify and resolve problems like ingestion bottlenecks and unbalanced shards, reducing manual effort and preventing performance issues. 

When you need support, AutoOps gives the Elastic team real-time visibility into your cluster, leading to faster resolutions. 

Using AutoOps with Cloud Connect lets you access all these features in your self-managed cluster without the operational overhead of managing their infrastructure.
:::

:::{dropdown} Which versions of {{es}} does AutoOps support?

$$$cc-autoops-es-version$$$

AutoOps is compatible with all [supported {{es}} versions](https://www.elastic.co/support/eol).
:::

:::{dropdown} Which deployment types can be connected to AutoOps?

$$$cc-autoops-deployment-types$$$

You can connect to AutoOps on a standalone Elastic Stack, ECE (Elastic Cloud Enterprise), or ECK (Elastic Cloud on Kubernetes) deployment.
:::

:::{dropdown} Can I use AutoOps with Cloud Connect if my environment is air-gapped?

$$$cc-autoops-air-gapped$$$

Not at this time. AutoOps is currently only available as a cloud service and you need an internet connection to send metrics to the {{ecloud}}. For air-gapped environments, we plan to offer a locally deployable version in the future.
:::

:::{dropdown} Do I have to define an Elastic IP address to enable the agent to send data to the {{ecloud}}?

$$$cc-autoops-elastic-ip$$$

You may need to define an IP address if your organization’s settings will block the agent from sending out data. 

To enable IP ranges, {{ecloud}} offers a selection of static IP addresses. All traffic directed to {{ecloud}} deployments, whether originating from the public internet, your private cloud network through the public internet, or your on-premise network through the public internet utilizes Ingress Static IPs as the network destination. 

For more information, refer to [](/deploy-manage/security/elastic-cloud-static-ips.md).
:::

:::{dropdown} Where are AutoOps metrics stored, and does it cost extra to ship metrics to the {{ecloud}}?

$$$cc-autoops-collected-metrics$$$

You can choose the CSP and region in which your cluster metrics will be stored from a list of [available regions](/deploy-manage/monitor/autoops/ec-autoops-regions.md). 

Shipping metrics to the {{ecloud}} may come at an additional cost. For example, when sending metrics data from your cluster in a CSP region to the {{ecloud}}, shipping costs will be determined by your agreement with that CSP.
:::

:::{dropdown} What information does the Elastic Agent extract from my cluster?

$$$cc-autoops-collected-metrics$$$

The Elastic Agent only extracts cluster metrics and sends them to the {{ecloud}}. For a list of these metrics, refer to [](/deploy-manage/monitor/autoops/cc-collected-metrics.md).
:::


