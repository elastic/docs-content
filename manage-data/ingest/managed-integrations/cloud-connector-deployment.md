---
navigation_title: Federated identity authentication
description: Use federated identity authentication, formerly cloud connectors, to connect Managed integrations to AWS, Azure, and Google Cloud without long-lived credentials.
applies_to:
  stack: ga 9.6+, preview 9.2-9.5
  serverless: ga
products:
  - id: fleet
  - id: observability
  - id: security
  - id: cloud-serverless
  - id: cloud-hosted
---

# Authenticate {{managed-integrations}} using a federated identity

Federated identity authentication lets {{managed-integrations}} connect to your {{aws}}, Azure, or {{gcp}} account without long-lived credentials such as access keys, client secrets, or service account keys. You create an identity in your cloud account (an IAM role on {{aws}}, a managed identity on Azure, or a service account on {{gcp}}) that trusts Elastic, and Elastic uses it to get short-lived credentials when it collects data. You can reuse a federated identity across multiple integrations, which helps you manage deployments that collect data from many cloud accounts.

{{managed-integrations}}, and therefore federated identities, are available on {{ech}} deployments and {{serverless-full}} projects.

:::{note}
:applies_to: stack: preview 9.2-9.3

In {{stack}} versions 9.2 and 9.3, federated identities are called cloud connectors, and appear in the {{kib}} UI as **Cloud Connectors**.
:::

## Integrations that support federated identity authentication [federated-identity-supported-integrations]

You can use federated identity authentication with these {{managed-integrations}}:

- **Cloud Security Posture Management (CSPM) and Asset Discovery** on {{aws}}, Azure, and {applies_to}`{ "serverless": "ga", "stack": "ga 9.6+, preview 9.4-9.5" }` {{gcp}}. For deployment instructions, refer to:
  - Asset Discovery: [Asset Discovery on Azure](/solutions/security/cloud/asset-disc-azure.md); [Asset Discovery on AWS](/solutions/security/cloud/asset-disc-aws.md)
  - CSPM: [CSPM on Azure](/solutions/security/cloud/get-started-with-cspm-for-azure.md); [CSPM on AWS](/solutions/security/cloud/get-started-with-cspm-for-aws.md)
- {applies_to}`{serverless: ga, stack: ga 9.6+}` **{{aws}} integrations** that offer the **Identity Federation** setup option: [AWS](integration-docs://reference/aws.md), [Amazon Bedrock](integration-docs://reference/aws_bedrock.md), [Amazon Bedrock AgentCore](integration-docs://reference/aws_bedrock_agentcore.md), [Amazon MQ](integration-docs://reference/aws_mq.md), [AWS Security Hub](integration-docs://reference/aws_securityhub.md), and [Custom AWS Logs](integration-docs://reference/aws_logs.md). To set one up, refer to [Set up federated identity for an AWS integration](#federated-identity-aws-setup).

::::{important}
:applies_to: stack: preview =9.2
In this version, to use cloud connector authentication for an AWS integration, your {{kib}} instance must be hosted on AWS. In other words, you must choose AWS hosting during {{kib}} setup. This is no longer required in later versions.
::::

## Set up federated identity for an AWS integration [federated-identity-aws-setup]

```{applies_to}
stack: ga 9.6+
serverless: ga
```

Use these steps for the {{aws}} integrations listed in [Integrations that support federated identity authentication](#federated-identity-supported-integrations). For CSPM and Asset Discovery, follow the deployment instructions for those integrations instead.

### Before you begin [federated-identity-aws-prerequisites]

To set up federated identity authentication for an {{aws}} integration, you need:

- An {{ech}} deployment or a {{serverless-full}} project.
- Permission in your {{aws}} account to create CloudFormation stacks and IAM roles.

### Create or select a federated identity [federated-identity-aws-steps]

1. In {{kib}}, go to **{{integrations}}** and select the integration, for example **AWS**.
2. Select **Add `<integration>`**.
3. In the **Deployment** section, select **Elastic Managed Integration**.
4. Under **Setup Access**, for **Preferred method**, select **Identity Federation**.
5. Create a new federated identity or reuse an existing one:
   - To create a new identity, on the **New Identity** tab:
     1. Enter a **Federated Identity Name**.
     2. Select **Launch CloudFormation**. The {{aws}} CloudFormation console opens with the stack parameters filled in. You can also expand **Steps to assume role** in {{kib}} for the same instructions.
     3. Sign in as an administrator to the {{aws}} account you want to onboard. Optionally, change the region you want to deploy the stack to.
     4. Select the checkbox for **I acknowledge that AWS CloudFormation might create IAM resources**, then select **Create stack**.
     5. When the stack status is `CREATE_COMPLETE`, open the **Outputs** tab and copy the `RoleArn` value.
     6. In {{kib}}, paste the value into **Role ARN**.
   - To reuse an identity, select the **Existing Identity** tab, then select the identity from the **Federated Identity Name** list.
6. Configure the rest of the integration, then save it.

## Federated identity names

```{applies_to}
stack: ga 9.6+, preview 9.3-9.5
serverless: ga
```

Federated identity names help you keep track of each identity's purpose and reuse it appropriately. For example, you could name two AWS identities `aws-prod` and `aws-testing`.

When you create a new federated identity you must name it:

- {applies_to}`{ "serverless": "ga", "stack": "ga 9.6+, preview 9.4-9.5" }` Enter the name in the **Federated Identity Name** field. When you're deploying an integration, select the **Existing Identity** tab to reuse an existing identity by name.
- {applies_to}`stack: preview =9.3` Enter the name in the **Cloud Connector Name** field. When you're deploying an integration, if you select **Existing Connection**, a dropdown menu with the names of existing cloud connectors appears.

To rename a federated identity, go to the tab that lists existing identities and click the **Edit** button next to the identity's name, then enter a new name.

Because names were introduced with {{stack}} version 9.3, federated identities created in earlier versions are named automatically:

  - AWS federated identities use their role ARN as the name.
  - Azure federated identities use their cloud connector ID as the name.
