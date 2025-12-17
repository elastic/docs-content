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

Cloud connector authentication currently supports deployments of Elastic's Cloud Security Posture Management (CSPM) and Asset Discovery integrations to AWS and Azure. For deployment instructions, refer to:

- Asset Discovery: [Asset Discovery on Azure](/solutions/security/cloud/asset-disc-azure.md); [Asset Discovery on AWS](/solutions/security/cloud/asset-disc-aws.md)
- CSPM: [CSPM on Azure](/solutions/security/cloud/get-started-with-cspm-for-azure.md); [CSPM on AWS](/solutions/security/cloud/get-started-with-cspm-for-aws.md)

::::{important}
{applies_to}`stack: removed 9.3` To use cloud connector authentication for an AWS integration, your {{kib}} instance must be hosted on AWS. In other words, you must have chosen AWS hosting during {{kib}} setup.
::::