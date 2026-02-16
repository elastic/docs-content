---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/cspm.html
  - https://www.elastic.co/guide/en/serverless/current/security-cspm.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Cloud security posture management

The Cloud Security Posture Management (CSPM) feature discovers and evaluates the services in your cloud environment — like storage, compute, IAM, and more — against configuration security guidelines defined by the [Center for Internet Security](https://www.cisecurity.org/) (CIS) to help you identify and remediate risks that could undermine the confidentiality, integrity, and availability of your cloud data.

This feature currently supports agentless and agent-based deployments on Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure. 

For step-by-step getting started guides, refer to:

* [CSPM for AWS](/solutions/security/cloud/get-started-with-cspm-for-aws.md)
* [CSPM for GCP](/solutions/security/cloud/get-started-with-cspm-for-gcp.md) 
* [CSPM for Azure](/solutions/security/cloud/get-started-with-cspm-for-azure.md).

::::{admonition} Requirements
* Minimum privileges vary depending on whether you need to read, write, or manage CSPM data and integrations. Refer to [CSPM privilege requirements](/solutions/security/cloud/cspm-privilege-requirements.md).
* The CSPM integration is available to all {{ecloud}} users. On-premise deployments require an [appropriate subscription](https://www.elastic.co/pricing) level.
* CSPM supports only the AWS, GCP, and Azure commercial cloud platforms, and AWS GovCloud. AWS GovCloud is only supported for agent-based deployments — agentless deployments do not work on this platform. Other government cloud platforms are not supported. To request support for other platforms, [open a GitHub issue](https://github.com/elastic/kibana/issues/new/choose).

::::

## How CSPM works [cspm-how-it-works]

Using the read-only credentials you will provide during the setup process, it will evaluate the configuration of resources in your environment every 24 hours. After each evaluation, the integration sends findings to Elastic. A high-level summary of the findings appears on the [Cloud Security Posture dashboard](/solutions/security/dashboards/cloud-security-posture-dashboard.md), and detailed findings appear on the [Findings page](/solutions/security/cloud/findings-page-2.md).









