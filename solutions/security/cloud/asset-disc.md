---
applies_to:
  stack: preview
  serverless:
    security: preview
---

# Cloud asset discovery

The Cloud Asset Discovery integration (CAD) creates an up-to-date, unified inventory of your cloud resources from AWS, GCP, and Azure.

This feature currently supports agentless and agent-based deployments on Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure. For step-by-step getting started guides, refer to [Get started with CAD for AWS](/solutions/security/cloud/asset-disc-aws.md), [Get started with CAD for GCP](/solutions/security/cloud/asset-disc-gcp.md), or [Get started with CAD for Azure](/solutions/security/cloud/asset-disc-azure.md).

::::{admonition} Requirements
* The CSPM integration is available to all {{ecloud}} users. On-premise deployments require an [Enterprise subscription](https://www.elastic.co/pricing).
* CSPM supports only the AWS, GCP, and Azure commercial cloud platforms. Government cloud platforms are not supported. To request support for other platforms, [open a GitHub issue](https://github.com/elastic/kibana/issues/new/choose).

::::

## How cad works [cad-how-it-works]

Using the read-only credentials you will provide during the setup process, it will evaluate the configuration of resources in your environment every 24 hours. After each evaluation, the integration sends findings to Elastic.









