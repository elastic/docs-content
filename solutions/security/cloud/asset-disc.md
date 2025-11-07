---
applies_to:
  stack: preview 9.1
  serverless:
    security: preview
---

# Cloud Asset Discovery

The Cloud Asset Discovery integration creates an up-to-date, unified inventory of your cloud resources from AWS, GCP, and Azure.

This feature currently supports agentless and agent-based deployments on Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure. 

For step-by-step getting started guides, refer to the following getting started guides:

* [Cloud Asset Discovery for AWS](/solutions/security/cloud/asset-disc-aws.md)
* [Cloud Asset Discovery for GCP](/solutions/security/cloud/asset-disc-gcp.md)
* [Cloud Asset Discovery for Azure](/solutions/security/cloud/asset-disc-azure.md)

## Requirements

* The Cloud Asset Discovery integration is available to all {{ecloud}} users. On-premise deployments require an [appropriate subscription](https://www.elastic.co/pricing) level.
* Cloud Asset Discovery supports only the AWS, GCP, and Azure commercial cloud platforms. Government cloud platforms are not supported. To request support for other platforms, [open a GitHub issue](https://github.com/elastic/kibana/issues/new/choose).


## How Cloud Asset Discovery works [cad-how-it-works]

Cloud Asset Discovery creates an up-to-date, unified inventory of your cloud resources from AWS, GCP, and Azure. Once you connect your cloud accounts, this integration automatically finds and lists your cloud services and assets, such as:

* **AWS:** S3 buckets, EC2 instances, EKS clusters, and more.
* **GCP:** Cloud Storage buckets, Compute Engine instances, Kubernetes clusters, and more.
* **Azure:** Virtual Machines, Blob Storage, Azure Kubernetes Service (AKS), and more.

Using the read-only credentials you will provide during the setup process, it will evaluate the configuration of resources in your environment every 24 hours. After each evaluation, the integration sends findings to Elastic.









