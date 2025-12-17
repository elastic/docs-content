---
navigation_title: Cloud connector authentication for agentless
applies_to:
  stack: preview 9.2
  serverless:
    security: preview
---

# Authenticate agentless integrations using cloud connectors

Cloud connector authentication for agentless integrations reduces the administrative burden of authentating to third-party cloud service providers by eliminating the need to keep track of credentials such as API keys or passwords. Cloud connectors provide a reusable, secure-by-default means of authentication, helping you to manage deployments with many integrations collecting data from multiple cloud security providers. 

## Integrations that support cloud connector deployment

Cloud connector authentication currently supports deployments of Elastic's Cloud Security Posture Management (CSPM) and Asset Discovery integrations to AWS and Azure. For deployment instructions, refer to:

- Asset Discovery: [Asset Discovery on Azure](/solutions/security/cloud/asset-disc-azure.md); [Asset Discovery on AWS](/solutions/security/cloud/asset-disc-aws.md)
- CSPM: [CSPM on Azure](/solutions/security/cloud/get-started-with-cspm-for-azure.md); [CSPM on AWS](/solutions/security/cloud/get-started-with-cspm-for-aws.md)

::::{important}
{applies_to}`stack: removed 9.3`{applies_to}`serverless: removed` To use cloud connector authentication for an AWS integration, your {{kib}} instance must be hosted on AWS. In other words, you must have chosen AWS hosting during {{kib}} setup.
::::

## Cloud connector names
```{applies_to}
stack: preview 9.3
serverless: preview
```
Cloud connector names help you keep track of each connector's purpose and reuse it appropriately. For example, you could name two AWS connectors `aws-prod` and `aws-testing`. 

When you create a new cloud connector you must name it. When you're deploying an integration with a cloud connector, if you select **Existing connection** a dropdown menu with the names of existing cloud connectors appears. 

To rename a connector, go to the **Existing connection** dropdown menu and click the **Edit** button next to its name, then enter a new name.

Because cloud connector names were introduced with {{stack}} version 9.3, cloud connectors created in earlier versions have default names:

  - For AWS cloud connectors: `Cloud Connector RoleARN`.
  - For Azure cloud connectors: `Cloud Connector ID`. 