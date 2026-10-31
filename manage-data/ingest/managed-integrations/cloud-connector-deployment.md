---
navigation_title: Federated identity authentication
description: Use federated identity authentication, formerly cloud connectors, to connect Elastic Managed integrations to AWS, Azure, and Google Cloud without long-lived credentials.
applies_to:
  stack: ga 9.5+, preview 9.2-9.4
  serverless: ga
products:
  - id: fleet
  - id: observability
  - id: security
  - id: cloud-serverless
  - id: cloud-hosted
---

# Authenticate {{managed-integrations}} using a federated identity

Federated identity authentication lets {{managed-integrations}} connect to your {{aws}}, Azure, or {{gcp}} account without long-lived credentials such as access keys, client secrets, or service account keys. You create an identity in your cloud account (an IAM role on {{aws}}, a managed identity on Azure, or a service account on {{gcp}}) that trusts Elastic, and Elastic uses it to get short-lived credentials when it collects data.

On Azure and {{gcp}}, federated identity is available for CSPM and Cloud Asset Discovery. On {{aws}}, it's also available for several other integrations. For details, refer to [Integrations that support federated identity authentication](#federated-identity-supported-integrations).

{{managed-integrations}}, and therefore federated identities, are available on {{ech}} deployments and {{serverless-full}} projects.

:::{note}
:applies_to: stack: preview 9.2-9.3

In {{stack}} versions 9.2 and 9.3, federated identities are called cloud connectors, and appear in the {{kib}} UI as **Cloud Connectors**.
:::

## Integrations that support federated identity authentication [federated-identity-supported-integrations]

You can use federated identity authentication with these {{managed-integrations}}:

- **Cloud Security Posture Management (CSPM)** and **Cloud Asset Discovery** on {{aws}}, Azure, and {{gcp}}. For deployment instructions, refer to:
  - Cloud Asset Discovery: [Asset Discovery on Azure](/solutions/security/cloud/asset-disc-azure.md); [Asset Discovery on AWS](/solutions/security/cloud/asset-disc-aws.md)
  - CSPM: [CSPM on Azure](/solutions/security/cloud/get-started-with-cspm-for-azure.md); [CSPM on AWS](/solutions/security/cloud/get-started-with-cspm-for-aws.md)
- {applies_to}`{serverless: preview, stack: unavailable}` **{{aws}} integrations** that offer the **Identity Federation** setup option: [AWS](integration-docs://reference/aws.md), [Amazon Bedrock](integration-docs://reference/aws_bedrock.md), [Amazon Bedrock AgentCore](integration-docs://reference/aws_bedrock_agentcore.md), [Amazon MQ](integration-docs://reference/aws_mq.md), [AWS Security Hub](integration-docs://reference/aws_securityhub.md), and [Custom AWS Logs](integration-docs://reference/aws_logs.md). To set one up, refer to [Set up federated identity for an AWS integration](#federated-identity-aws-setup).

  In the [AWS](integration-docs://reference/aws.md) integration, federated identity works with most, but not all, data streams. For example, it isn’t available for AWS CloudTrail, Amazon VPC Flow Logs, or AWS WAF. Check the integration’s documentation for the data streams you need.

::::{important}
:applies_to: stack: preview =9.2
In this version, to use cloud connector authentication for an AWS integration, your {{kib}} instance must be hosted on AWS. In other words, you must choose AWS hosting during {{kib}} setup. This is no longer required in later versions.
::::

## Set up federated identity for an AWS integration [federated-identity-aws-setup]

```{applies_to}
serverless: preview
stack: unavailable
```


Use these steps for the {{aws}} integrations listed in [Integrations that support federated identity authentication](#federated-identity-supported-integrations). For CSPM and Cloud Asset Discovery, follow the deployment instructions for those integrations instead. To set up several AWS services at once, use the [guided AWS onboarding flow](/manage-data/ingest/aws-guided-onboarding.md), which includes these steps.

### How it works [federated-identity-aws-how-it-works]

When you create a federated identity, {{kib}} generates an AWS CloudFormation template for the integrations you're setting up and opens it in the AWS console with the stack parameters that identify your Elastic organization and project already filled in. The stack creates:

- An IAM OpenID Connect (OIDC) identity provider for Elastic, if your AWS account doesn't have one yet. Every stack in the account that uses the same provider shares it.
- A Lambda function, with its execution role and a CloudWatch log group, that checks whether your account already has the OIDC provider and creates it if needed.
- An IAM role that only your Elastic project can assume.
- IAM policies that grant the role the permissions required by the integrations you enabled.

Because the role can only be assumed by the project it was created for, you can reuse a federated identity across integrations in the same project, but not across projects. When you add an integration that needs more permissions, you update the stack to add them. For details, refer to [Update a federated identity's stack](#federated-identity-aws-update).

### Before you begin [federated-identity-aws-prerequisites]

To set up federated identity authentication for an {{aws}} integration, you need:

- An {{serverless-full}} project.
- Administrator access to the {{aws}} account you want to onboard.

### Create or select a federated identity [federated-identity-aws-steps]

1. In {{kib}}, go to **{{integrations}}** and start adding the integration as an {{managed-integration}}, as described in [Enable an {{managed-integration}}](/manage-data/ingest/managed-integrations/enable-managed-integration.md). Make sure you select the **Elastic Managed Integration** deployment option.
2. Under **Setup Access**, for **Preferred method**, select **Identity Federation**.
3. Create a new federated identity or reuse an existing one:

   :::{include} /manage-data/_snippets/aws-federated-identity-steps.md
   :::

4. Configure the rest of the integration, then save it.

### Update a federated identity's stack [federated-identity-aws-update]

An identity's IAM role only has the permissions for the integrations it was set up for. When you select an identity on the **Existing Identity** tab and it doesn't have the permissions the integrations need, a **CloudFormation stack update required** callout appears, and you need to update the stack before you can complete setup. When Elastic updates the IAM role template, a **CloudFormation stack upgrade available** callout appears in the identity's details.

To update the stack:

1. In the callout, select **Update CloudFormation stack**. The {{aws}} CloudFormation console opens the stack update with **Replace existing template** selected and the new template filled in.
2. Go through the update steps in the {{aws}} console, then select **Submit**.
3. Return to {{kib}} and continue setting up the integration. Data from the new integrations starts arriving after the stack update completes.

## Federated identity names

```{applies_to}
stack: ga 9.5+, preview 9.3-9.4
serverless: ga
```

Federated identity names help you keep track of each identity's purpose and reuse it appropriately. For example, you could name two AWS identities `aws-prod` and `aws-testing`.

When you create a new federated identity you must name it:

- {applies_to}`{ "serverless": "ga", "stack": "ga 9.5+, preview =9.4" }` Enter the name in the **Federated Identity Name** field. When you're deploying an integration, select the **Existing Identity** tab to reuse an existing identity by name.
- {applies_to}`stack: preview =9.3` Enter the name in the **Cloud Connector Name** field. When you're deploying an integration, if you select **Existing Connection**, a dropdown menu with the names of existing cloud connectors appears.

To rename a federated identity, go to the tab that lists existing identities and click the **Edit** button next to the identity's name, then enter a new name.

Because names were introduced with {{stack}} version 9.3, federated identities created in earlier versions are named automatically:

  - AWS federated identities use their role ARN as the name.
  - Azure federated identities use their cloud connector ID as the name.
