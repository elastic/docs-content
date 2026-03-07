---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS SNS Topic Message Publish by Rare User" prebuilt detection rule.
---

# AWS SNS Topic Message Publish by Rare User

## Triage and Analysis

### Investigating AWS SNS Topic Message Publish by Rare User

This rule identifies when a message is published to an SNS topic by a user who has rarely or never published messages before. This activity could indicate adversarial actions, such as using SNS topics for phishing campaigns, data exfiltration, or lateral movement within an AWS environment.

This is a [New Terms](https://www.elastic.co/guide/en/security/current/rules-ui-create.html#create-new-terms-rule) rule that only flags when this behavior is observed for the first time by a user or role.

#### Possible Investigation Steps

- **Identify the Actor and Resource**:
  - **User Identity and Role**: Examine the `aws.cloudtrail.user_identity.arn` to identify the user or role responsible for publishing the SNS message. Verify whether this actor is authorized to publish messages to SNS topics.
  - **Access Key Details**: Review the `aws.cloudtrail.user_identity.access_key_id` to determine the access key used.
  - **SNS Topic ARN**: Analyze `aws.cloudtrail.resources.arn` to confirm whether the SNS topic is critical, sensitive, or used for authorized purposes.

- **Evaluate the Context of the SNS Message**:
  - **Published Message Details**: AWS redacts the message content in CloudTrail logs, but you can view the message ID, subject, and other metadata. Investigate the message details for any indicators of malicious content.
  - **Message Recipients**: Investigate the subscriptions associated with the SNS topic to identify if messages were sent to unauthorized or unexpected recipients.

- **Analyze Source Information**:
  - **Source IP Address**: Examine the `source.ip` field to identify the origin of the activity. Unusual IP addresses or geolocations may indicate unauthorized access.
  - **User Agent**: Review `user_agent.original` to determine the tool or client used for publishing the SNS message. Automated tools or unexpected clients (e.g., `Boto3` from an unknown host) may signify misuse.

- **Review Historical Activity**:
  - **Actor’s Past Behavior**: Identify whether the user has published messages to SNS topics before. Review similar past events for context.
  - **Frequency and Patterns**: Examine the time and frequency of messages published by the same user or to the same SNS topic to detect anomalies.

- **Correlate with Other Events**:
  - **IAM or CloudTrail Events**: Look for events such as `AssumeRole`, `CreateAccessKey`, or other API actions associated with the same user ARN.
  - **Unusual IAM Role Activity**: Determine if the actor has assumed roles or performed administrative tasks atypical for their role.

### False Positive Analysis

- **Routine Operational Use**:
  - Confirm if the publishing activity aligns with standard operational tasks or automation scripts.
  - Validate whether new or rare users were recently granted permissions for publishing messages to SNS topics.

- **Testing or Monitoring Scripts**:
  - Automated testing or monitoring tools may trigger this rule if configured to publish messages to SNS topics.

### Response and Remediation

- **Immediate Action**:
  - If unauthorized activity is confirmed, disable the access key or IAM role associated with the user.
  - Restrict or remove permissions from the SNS topic to prevent further misuse.

- **Review Policies and Subscriptions**:
  - Audit the IAM policies tied to the user and SNS topic to ensure appropriate permissions.
  - Validate the subscriptions of the SNS topic to confirm all endpoints are authorized.

- **Enhance Monitoring and Alerting**:
  - Set up additional logging or alerting for SNS publish actions, especially from rare or unknown users.
  - Monitor for similar actions across other SNS topics within the environment.

- **Conduct a Root Cause Analysis**:
  - Investigate how the user or role gained access to publish messages to the SNS topic.
  - Determine if other AWS resources or services have been affected.

### Additional Information

For more information on SNS topic management and securing AWS resources, refer to:
- [AWS SNS Publish API Documentation](https://docs.aws.amazon.com/sns/latest/api/API_Publish.html)
- [AWS CloudTrail Documentation](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference.html)

