---
navigation_title: Cloud connector authentication for agentless
applies_to:
  stack: preview 9.2
  serverless:
    security: preview
---

# Quickly authenticate agentless integrations using cloud connectors

Cloud connector authentication for agentless integrations allows you to quickly provide Elastic with access to your third-party cloud service provider accounts. Cloud connectors provide a simple, reusable means of authentication, making it easier to manage deployments with many integrations collecting data from multiple cloud security providers. This reduces your administrative burden by eliminating the need to keep track of credentials such as API keys or passwords. 

## Where is cloud connector authentication supported?

At the current stage of this technical preview, a limited selection of cloud providers and integrations are supported.

You can use cloud connector deployment to authenticate with AWS and Azure while deploying either Elastic's Cloud Security Posture Management (CSPM) or Asset Discovery integration. For deployment instructions, refer to:

- Asset Discovery: [Asset Discovery on Azure](/solutions/security/cloud/asset-disc-azure.md); [Asset Discovery on AWS](/solutions/security/cloud/asset-disc-aws.md)
- CSPM: [CSPM on Azure](/solutions/security/cloud/get-started-with-cspm-for-azure.md); [CSPM on AWS](/solutions/security/cloud/get-started-with-cspm-for-aws.md)

::::{important}
in order to use cloud connector for an AWS integration, your {{kib}} instance must be hosted on AWS. In other words, you must have chosen AWS hosting during {{kibana}} setup.
::::