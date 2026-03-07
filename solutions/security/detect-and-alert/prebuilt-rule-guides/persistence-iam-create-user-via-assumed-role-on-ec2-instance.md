---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS IAM Create User via Assumed Role on EC2 Instance" prebuilt detection rule.
---

# AWS IAM Create User via Assumed Role on EC2 Instance

## Triage and analysis

### Investigating AWS IAM Create User via Assumed Role on EC2 Instance

This rule detects when an AWS Identity and Access Management (IAM) user is created through an assumed role on an EC2 instance. This action may indicate a potentially compromised instance where an adversary could be using the instance’s permissions to create a new IAM user, enabling persistent unauthorized access.

#### Possible Investigation Steps

- **Identify the Assumed Role and Initiating Instance**:
  - **Role and Instance**: Examine the `aws.cloudtrail.user_identity.arn` field to determine the specific EC2 instance and role used for this action (e.g., `arn:aws:sts::[account-id]:assumed-role/[role-name]/[instance-id]`). Verify if this behavior aligns with expected usage or represents an anomaly.

- **Analyze the Target IAM User**:
  - **New User Details**: Inspect `aws.cloudtrail.request_parameters` to see the username that was created. Validate if the user is expected or authorized.
  - **Review Creation Time and Context**: Compare the creation time (`@timestamp`) of the user with other activities from the same instance and role to assess if this creation was part of a larger chain of actions.

- **Check User Agent and Tooling**:
  - **User Agent Analysis**: Review `user_agent.original` to see if AWS CLI, SDK, or other tooling was used for this request. Identifiers such as `aws-cli`, `boto3`, or similar SDK names can indicate the method used, which may differentiate automation from interactive actions.
  - **Source IP and Location**: Use the `source.ip` and `source.geo` fields to identify the IP address and geographic location of the event. Verify if this aligns with expected access patterns for your environment.

- **Evaluate for Persistence Indicators**:
  - **Role Permissions**: Check the permissions associated with the assumed role (`arn:aws:iam::[account-id]:role/[role-name]`) to determine if creating IAM users is a legitimate activity for this role.
  - **Automated Role Patterns**: If the assumed role or instance typically creates IAM users for automation purposes, validate this action against historical records to confirm if the event is consistent with normal patterns.

- **Review Related CloudTrail Events**:
  - **Additional IAM Actions**: Investigate for other recent IAM or CloudTrail events tied to this role or instance, especially `CreateAccessKey` or `AttachUserPolicy` actions. These could signal further attempts to empower or utilize the newly created user.
  - **Correlate with Other Suspicious Activities**: Determine if other roles or instances recently initiated similar unusual actions, such as privilege escalations or data access.

### False Positive Analysis

- **Expected Automation**: Assumed roles may be used by legitimate automated systems that create users for specific workflows. Confirm if this event aligns with known automation activities.
- **Role Exceptions**: If this action is routine for specific roles, consider adding those roles to a monitored exception list for streamlined review.

### Response and Remediation

- **Immediate Access Review**: If user creation was unauthorized, restrict the assumed role’s permissions to prevent further user creation.
- **Delete Unauthorized Users**: Confirm and remove any unauthorized IAM users, adjusting IAM policies to reduce similar risks.
- **Enhance Monitoring and Alerts**: Enable enhanced logging or real-time alerts for this role or instance to detect further unauthorized access attempts.
- **Policy Update**: Consider updating IAM policies associated with roles on EC2 instances to limit sensitive actions like IAM user creation.

### Additional Information

For further guidance on managing IAM roles and permissions within AWS environments, refer to the [AWS IAM documentation](https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateUser.html) and AWS best practices for security.

