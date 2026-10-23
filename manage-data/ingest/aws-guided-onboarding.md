---
navigation_title: AWS guided onboarding
description: Use the guided AWS onboarding flow in Kibana to select AWS services, choose how Elastic collects their data, deploy, and confirm that data arrives.
applies_to:
  stack: preview 9.6+
  serverless: preview
products:
  - id: fleet
  - id: observability
  - id: security
  - id: cloud-serverless
  - id: cloud-hosted
type: how-to
---

# Set up AWS data collection with guided onboarding [aws-guided-onboarding]

The guided AWS onboarding flow in {{kib}} sets up several AWS services at once. Select the services you want to monitor, choose how Elastic collects their data, deploy, and confirm that data is arriving. The flow also installs the prebuilt dashboards, Discover sessions, and alerting rule templates for those services.

Depending on the service and the deployment method you choose, the flow collects data in the following ways:

- **{{managed-integrations}}**: Elastic runs the collectors for you. Elastic authenticates to your AWS account with a [federated identity](/manage-data/ingest/managed-integrations/cloud-connector-deployment.md) or an access key pair. For more information, refer to [{{managed-integrations}}](/manage-data/ingest/managed-integrations/managed-integrations.md).
- **Elastic Cloud Forwarder**: A CloudFormation stack in your AWS account forwards logs from S3 buckets or CloudWatch log groups to Elastic. For more information, refer to the [Elastic Cloud Forwarder](opentelemetry://reference/edot-cloud-forwarder/index.md).
- **{{agent}}**: You enroll a self-managed {{agent}} on a host that has access to your AWS environment.

The flow has four steps: [Services](#aws-onboarding-services), [Service Settings](#aws-onboarding-settings), [Authenticate & Deploy](#aws-onboarding-deploy), and [Detect & Review](#aws-onboarding-detect).

## Before you begin [aws-onboarding-before-you-begin]

To use the guided AWS onboarding flow, you need:

- Administrator access to the AWS account you want to collect data from. The flow opens AWS CloudFormation to create IAM resources and, for some services, the Elastic Cloud Forwarder.
- The `Fleet: All` and `Integrations: All` [{{kib}} privileges](/reference/fleet/fleet-roles-privileges.md).

## Select services [aws-onboarding-services]

1. Select **Add data**, then select **Amazon Web Services**.
1. In the **Services** step, select the AWS services you want to monitor. Services are grouped by category, and you can filter the list to **Logs** or **Metrics**.
1. Select **Next**.

Some services don't support {{managed-integrations}} and can only be collected with a self-managed {{agent}}. If you select any of these, the step lists them and tells you that you configure {{agent}} in the later steps.

The **Data format** setting controls which services the step lists. **ECS-compatible** is the default and has the broadest content coverage. **OTel-native** lists services that use OpenTelemetry semantic conventions. Identity Federation is only available for ECS-compatible services. With **OTel-native**, {{managed-integrations}} authenticate with access keys, and log services are deployed with the Elastic Cloud Forwarder.

% VERIFY (data format and federation): From the Kibana code (main, Oct 2026): the service list is filtered by
% data format, and the OTel-native metrics services use the AWS CloudWatch (OpenTelemetry) input package
% (`aws_cloudwatch_input_otel`), which has no Identity Federation option. Confirm with engineering whether
% federation support for OTel-native services is planned.

## Configure service settings [aws-onboarding-settings]

1. In the **Service Settings** step, select a **Global AWS region**. This is required and applies to all services. You can't change it after the services are deployed. To use a different region, start a new session.
2. If a service needs more settings, the step shows **Some services need your input**. Select the service and provide the required settings.
3. Select **Next**.

## Authenticate and deploy [aws-onboarding-deploy]

The **Authenticate & Deploy** step shows the **Deployment method** for your services. To change it, select **Edit**, choose a method, then select **Save**:

- **Elastic Managed Integrations**: Elastic collects the data for you, with no {{agent}} required.
- **Agent-based**: You enroll a self-managed {{agent}} that has access to your AWS environment. Use this for VPC-internal services, credentials that can't leave your account, or log files on disk.

You can't change the deployment method after the services are deployed. To choose a different method, start a new session.

With **Elastic Managed Integrations**, the step deploys each service in one of two ways, depending on the service:

- Services that run as {{managed-integrations}} appear in the **Managed Integrations** section.
- Log services that are collected from S3 buckets or CloudWatch log groups, such as Amazon S3 access logs, appear in the **Elastic Cloud Forwarder** section.

You don't choose between these sections. Each service appears in the section that supports it.

### Deploy {{managed-integrations}} [aws-onboarding-deploy-managed]

1. In the **Managed Integrations** section, for **Preferred method**, select how Elastic authenticates to your AWS account:
   - **Identity Federation**: Elastic assumes an IAM role in your account. You don't enter long-lived credentials.
   - **Access Keys**: Enter an AWS access key pair.

   **Identity Federation** is available only when every service in the **Managed Integrations** section supports it. If any selected service doesn't, only **Access Keys** is available. For the integrations and data streams that support Identity Federation, refer to [Integrations that support federated identity authentication](/manage-data/ingest/managed-integrations/cloud-connector-deployment.md#federated-identity-supported-integrations).
2. If you chose **Identity Federation**, create a new federated identity or select an existing one:
   - To create a new identity, on the **New Identity** tab, enter a **Federated Identity Name**, then select **Launch CloudFormation** and create the stack in the AWS console. Paste the `RoleArn` stack output into **Role ARN**, optionally paste the `StackId` output into **CloudFormation stack ARN**, then select **Create Identity**.
   - To reuse an identity, select the **Existing Identity** tab, then select the identity from the **Federated Identity Name** list. If the identity needs permissions for the services you selected, select **Update CloudFormation stack** and apply the update in the AWS console.

   For the detailed steps, what the stack creates, and how stack updates work, refer to [Set up federated identity for an AWS integration](/manage-data/ingest/managed-integrations/cloud-connector-deployment.md#federated-identity-aws-setup).
3. Select **Deploy integrations**. When the deployment finishes, the **Managed Integrations** section shows **Done**. Select **Next**.

### Deploy with the Elastic Cloud Forwarder [aws-onboarding-deploy-ecf]

In the **Elastic Cloud Forwarder** section, select **Launch CloudFormation**. The AWS console opens with the forwarder's CloudFormation template and most of its parameters filled in, based on the services, settings, and data format you chose. To complete the stack, including creating the Elastic API key it needs, refer to the [Elastic Cloud Forwarder](opentelemetry://reference/edot-cloud-forwarder/index.md) documentation for AWS.

When the stack is created, the section shows **Done**.

% VERIFY (services): Confirm which services use the forwarder and whether the list differs by data format.
% The code routes CloudTrail, VPC Flow Logs, WAF, S3 access logs, and ELB (OTel only) to it, plus
% CrowdStrike FDR with a dedicated template.

### Deploy with an {{agent}} [aws-onboarding-deploy-agent]

If you chose **Agent-based**, the **Where to add this integration?** section appears:

1. For **Preferred method**, choose how {{agent}} authenticates to AWS, for example **Direct access keys**, and enter the credentials.
2. Under **Hosts**, select **Create a new agent policy** and enter a **New agent policy name**, or select **Use an existing agent policy**. When you create a policy, **Collect system logs and metrics** is selected by default.
3. Select **Add agent**, then follow the steps to install and enroll {{agent}} on a host that has access to your AWS environment. For more information, refer to [Install {{agent}}s](/reference/fleet/install-elastic-agents.md).

Credentials you enter for agent-based deployments aren't saved between sessions, so you have to enter them again if you return later.

% VERIFY: Confirm the full list of agent-based authentication methods, and that the install link is the right target.

## Detect data and review content [aws-onboarding-detect]

After you deploy, the **Detect & Review** step checks in the background whether data is arriving for each service. You don't have to wait for it to complete.

- **Deployment summary** shows the deployment method, region, and either the federated identity, the Cloud Forwarder stack and version, or the agent policy and enrolled agents. Each service shows whether it's receiving data.
- **Installed content** lists the dashboards, Discover sessions, and alerting rule templates installed for your services. You can search the list and open each item from it. You can remove what you don't need, or reinstall it later from the integration's **Assets** tab. Required assets can't be removed.

For agent-based deployments, data appears only after an {{agent}} is enrolled. You can continue without one and add an agent later from {{fleet}}.

Select **Finish** to close the flow, or **Take me to my data** to open the data.

% VERIFY: Confirm where **Take me to my data** leads, and the status values a service can have.
% VERIFY (resume or change a deployment, not yet documented): The code saves a deployment record and supports
% reopening a deployment with a `deploymentId` URL parameter to edit it. Confirm how users get back to a saved
% deployment from the UI, what can be edited after deployment, and how removing services cleans up policies.

## Related pages [aws-onboarding-related]

- [Authenticate {{managed-integrations}} using a federated identity](/manage-data/ingest/managed-integrations/cloud-connector-deployment.md)
- [{{managed-integrations}}](/manage-data/ingest/managed-integrations/managed-integrations.md)
- [Elastic Cloud Forwarder](opentelemetry://reference/edot-cloud-forwarder/index.md)
- [Amazon Web Services (AWS) monitoring](/solutions/observability/cloud/amazon-web-services-aws-monitoring.md)
