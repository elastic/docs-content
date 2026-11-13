---
navigation_title: Federated identity authentication
description: Use federated identity authentication, formerly known as cloud connectors, with Elastic Managed integrations to avoid managing API keys directly for AWS and Azure integrations.
applies_to:
  stack: preview 9.2+
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Authenticate {{managed-integrations}} using a federated identity

Federated identity authentication for {{managed-integrations}} reduces the administrative burden of authenticating to third-party cloud service providers by eliminating the need to keep track of credentials such as API keys or passwords. Federated identities provide a reusable, secure-by-default means of authentication, helping you to manage deployments with many integrations collecting data from multiple cloud providers.

:::{note}
:applies_to: stack: preview 9.2-9.3

In {{stack}} versions 9.2 and 9.3, federated identities are called cloud connectors, and appear in the {{kib}} UI as **Cloud Connectors**.
:::

## Integrations that support federated identity authentication

Federated identity authentication currently supports deployments of Elastic's Cloud Security Posture Management (CSPM) and Asset Discovery integrations to AWS and Azure. For deployment instructions, refer to:

- Asset Discovery: [Asset Discovery on Azure](/solutions/security/cloud/asset-disc-azure.md); [Asset Discovery on AWS](/solutions/security/cloud/asset-disc-aws.md)
- CSPM: [CSPM on Azure](/solutions/security/cloud/get-started-with-cspm-for-azure.md); [CSPM on AWS](/solutions/security/cloud/get-started-with-cspm-for-aws.md)

::::{important}
:applies_to: stack: preview =9.2
In this version, to use cloud connector authentication for an AWS integration, your {{kib}} instance must be hosted on AWS. In other words, you must choose AWS hosting during {{kib}} setup. This is no longer required in later versions.
::::

## Federated identity names

```{applies_to}
stack: preview 9.3+
serverless: preview
```

Federated identity names help you keep track of each identity's purpose and reuse it appropriately. For example, you could name two AWS identities `aws-prod` and `aws-testing`.

When you create a new federated identity you must name it:

- {applies_to}`{serverless: preview, stack: preview 9.4+}` Enter the name in the **Federated Identity Name** field. When you're deploying an integration, select the **Existing Identity** tab to reuse an existing identity by name.
- {applies_to}`stack: preview =9.3` Enter the name in the **Cloud Connector Name** field. When you're deploying an integration, if you select **Existing Connection**, a dropdown menu with the names of existing cloud connectors appears.

To rename a federated identity, go to the tab that lists existing identities and click the **Edit** button next to the identity's name, then enter a new name.

Because names were introduced with {{stack}} version 9.3, federated identities created in earlier versions are named automatically:

  - AWS federated identities use their role ARN as the name.
  - Azure federated identities use their cloud connector ID as the name.
