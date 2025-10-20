---
navigation_title: Cloud connector authentication for agentless
applies_to:
  stack: preview 9.2
  serverless:
    security: preview
---

# Authenticate agentless integrations using cloud connectors

Cloud connector authentication for agentless integrations reduces the administrative burden of authentating to third-party cloud service providers by eliminating the need to keep track of credentials such as API keys or passwords. Cloud connectors provide a reusable, secure-by-default means of authentication, helping you to manage deployments with many integrations collecting data from multiple cloud security providers. 

## Where is cloud connector authentication supported?

At the current stage of this technical preview, a limited selection of cloud providers and integrations are supported.

You can use cloud connector deployment to authenticate with AWS and Azure while deploying either Elastic's Cloud Security Posture Management (CSPM) or Asset Discovery integration. For deployment instructions, refer to:

- Asset Discovery: [Asset Discovery on Azure](/solutions/security/cloud/asset-disc-azure.md); [Asset Discovery on AWS](/solutions/security/cloud/asset-disc-aws.md)
- CSPM: [CSPM on Azure](/solutions/security/cloud/get-started-with-cspm-for-azure.md); [CSPM on AWS](/solutions/security/cloud/get-started-with-cspm-for-aws.md)

::::{important}
In order to use cloud connector for an AWS integration, your {{kib}} instance must be hosted on AWS. In other words, you must have chosen AWS hosting during {{kib}} setup.
::::