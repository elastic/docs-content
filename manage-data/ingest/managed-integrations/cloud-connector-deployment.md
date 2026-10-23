---
navigation_title: Federated identity authentication
description: Use federated identity authentication, formerly cloud connectors, to connect Managed integrations to AWS, Azure, and Google Cloud without long-lived credentials.
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

% VERIFY (GA version): Federated identity for CSPM and Asset Discovery is GA, and for AWS integrations it's
% technical preview in 9.6. The GA version 9.5 is assumed because agentless reached GA in 9.5. Confirm it.

Federated identity authentication lets {{managed-integrations}} connect to your {{aws}}, Azure, or {{gcp}} account without long-lived credentials such as access keys, client secrets, or service account keys. You create an identity in your cloud account (an IAM role on {{aws}}, a managed identity on Azure, or a service account on {{gcp}}) that trusts Elastic, and Elastic uses it to get short-lived credentials when it collects data.

{{managed-integrations}}, and therefore federated identities, are available on {{ech}} deployments and {{serverless-full}} projects.

:::{note}
:applies_to: stack: preview 9.2-9.3

In {{stack}} versions 9.2 and 9.3, federated identities are called cloud connectors, and appear in the {{kib}} UI as **Cloud Connectors**.
:::

## Integrations that support federated identity authentication [federated-identity-supported-integrations]

You can use federated identity authentication with these {{managed-integrations}}:

- **Cloud Security Posture Management (CSPM) and Asset Discovery** on {{aws}}, Azure, and {{gcp}}. For deployment instructions, refer to:
  - Asset Discovery: [Asset Discovery on Azure](/solutions/security/cloud/asset-disc-azure.md); [Asset Discovery on AWS](/solutions/security/cloud/asset-disc-aws.md)
  - CSPM: [CSPM on Azure](/solutions/security/cloud/get-started-with-cspm-for-azure.md); [CSPM on AWS](/solutions/security/cloud/get-started-with-cspm-for-aws.md)
- {applies_to}`{serverless: preview, stack: preview 9.6+}` **{{aws}} integrations** that offer the **Identity Federation** setup option: [AWS](integration-docs://reference/aws.md), [Amazon Bedrock](integration-docs://reference/aws_bedrock.md), [Amazon Bedrock AgentCore](integration-docs://reference/aws_bedrock_agentcore.md), [Amazon MQ](integration-docs://reference/aws_mq.md), [AWS Security Hub](integration-docs://reference/aws_securityhub.md), and [Custom AWS Logs](integration-docs://reference/aws_logs.md). To set one up, refer to [Set up federated identity for an AWS integration](#federated-identity-aws-setup).

  In the [AWS](integration-docs://reference/aws.md) integration, federated identity works with most data streams, but not with these: Amazon API Gateway logs and metrics, Amazon CloudFront logs, AWS CloudTrail, Amazon EMR logs and metrics, AWS Network Firewall logs, Amazon MSK metrics, Amazon Kinesis Data Streams, NAT gateway, Amazon Redshift, Amazon Route 53 Resolver logs, Amazon S3 Storage Lens, Amazon S3 server access logs, AWS usage, Amazon VPC Flow Logs, AWS VPN, and AWS WAF.

  Federated identity isn't available for the AWS CloudWatch (OpenTelemetry) integration, which the [guided AWS onboarding flow](/manage-data/ingest/aws-guided-onboarding.md) uses for metrics when you choose the **OTel-native** data format.

% VERIFY (GCP): The CSPM and Asset Discovery packages added GCP cloud connector support before 9.6. Engineering
% says GCP and Azure onboarding changes aren't part of the 9.6 delivery. Confirm the Stack version GCP support
% started in, then add an applies_to tag for it.
% VERIFY (AWS data streams): From the integrations repo (main, Oct 22 2026): the six packages offer the
% `identity_federation` option, and in the `aws` package the 18 data streams listed have no
% `supports_identity_federation` check in their stream templates. `aws_cloudwatch_input_otel` has no
% `identity_federation` option. Confirm the list and that it applies to 9.6.

::::{important}
:applies_to: stack: preview =9.2
In this version, to use cloud connector authentication for an AWS integration, your {{kib}} instance must be hosted on AWS. In other words, you must choose AWS hosting during {{kib}} setup. This is no longer required in later versions.
::::

## Set up federated identity for an AWS integration [federated-identity-aws-setup]

```{applies_to}
stack: preview 9.6+
serverless: preview
```


Use these steps for the {{aws}} integrations listed in [Integrations that support federated identity authentication](#federated-identity-supported-integrations). For CSPM and Asset Discovery, follow the deployment instructions for those integrations instead. To set up several AWS services at once, use the [guided AWS onboarding flow](/manage-data/ingest/aws-guided-onboarding.md), which includes these steps.

### How it works [federated-identity-aws-how-it-works]

When you create a federated identity, {{kib}} generates an AWS CloudFormation template for the integrations you're setting up and opens it in the AWS console with the stack parameters that identify your Elastic organization and deployment or project already filled in. The stack creates:

- An IAM OpenID Connect (OIDC) identity provider for Elastic, if your AWS account doesn't have one yet. Every stack in the account that uses the same provider shares it.
- An IAM role that only your Elastic deployment or project can assume.
- IAM policies that grant the role the permissions required by the integrations you enabled.

Because the role can only be assumed by the deployment or project it was created for, you can reuse a federated identity across integrations in the same deployment or project, but not across deployments or projects. When you add an integration that needs more permissions, you update the stack to add them. For details, refer to [Update a federated identity's stack](#federated-identity-aws-update).

### Before you begin [federated-identity-aws-prerequisites]

To set up federated identity authentication for an {{aws}} integration, you need:

- An {{ech}} deployment or a {{serverless-full}} project.
- Administrator access to the {{aws}} account you want to onboard.

### Create or select a federated identity [federated-identity-aws-steps]

1. In {{kib}}, go to **{{integrations}}** and start adding the integration as an {{managed-integration}}, as described in [Enable an {{managed-integration}}](/manage-data/ingest/managed-integrations/enable-managed-integration.md). Make sure you select the **Elastic Managed Integration** deployment option.
2. Under **Setup Access**, for **Preferred method**, select **Identity Federation**.
3. Create a new federated identity or reuse an existing one:
   - To create a new identity, on the **New Identity** tab:
     1. Enter a **Federated Identity Name**.
     2. Select **Launch CloudFormation**. The {{aws}} CloudFormation console opens with the stack parameters filled in. You can also expand **Steps to assume role** in {{kib}} for the same instructions.
     3. Sign in as an administrator to the {{aws}} account you want to onboard. Optionally, change the region you want to deploy the stack to.
     4. Enter a **Stack name**. Don't change the parameters that {{kib}} filled in.
     5. Select the checkbox for **I acknowledge that AWS CloudFormation might create IAM resources with custom names**, then select **Create stack**.
     6. When the stack status is `CREATE_COMPLETE`, open the **Outputs** tab.
     7. In {{kib}}, paste the `RoleArn` output value into **Role ARN**. Optionally, paste the `StackId` output value into **CloudFormation stack ARN** so {{kib}} can link directly to the stack.
     8. Select **Create Identity**.
   - To reuse an identity, select the **Existing Identity** tab, then select the identity from the **Federated Identity Name** list. If the identity doesn't have the permissions the integration needs, update its stack as described in [Update a federated identity's stack](#federated-identity-aws-update).
4. Configure the rest of the integration, then save it.

% VERIFY (generic path): The demo videos show these identity steps in the guided AWS onboarding flow only. The
% integration policy path (Setup Access) uses the same Kibana component, but it hasn't been checked in the UI.

### Update a federated identity's stack [federated-identity-aws-update]

An identity's IAM role only has the permissions for the integrations it was set up for. If you select an existing identity for an integration that needs more permissions, {{kib}} asks you to update the identity's CloudFormation stack before you can complete setup. {{kib}} can also show **CloudFormation stack upgrade available** on an identity when Elastic has updated the IAM role template.

To update the stack:

1. In {{kib}}, select **Update CloudFormation stack**. The {{aws}} CloudFormation console opens the stack update with **Replace existing template** selected and the new template filled in.
2. Go through the update steps in the {{aws}} console, then select **Submit**.
3. Return to {{kib}} and continue setting up the integration. Data from the new integrations starts arriving after the stack update completes.

% VERIFY (update flow): The demo shows the "CloudFormation stack update opened" callout after selecting
% **Update CloudFormation stack**. The code also has a "CloudFormation stack update required" callout shown
% before that, and a message saying Kibana can't open the update when the identity's stack ARN isn't recorded.
% In the demo, the update opened even though no stack ARN was entered. Confirm when a stack ARN is required,
% whether the update callout appears in the integration policy flow or only in guided onboarding, and where
% users add a stack ARN to an existing identity.

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
