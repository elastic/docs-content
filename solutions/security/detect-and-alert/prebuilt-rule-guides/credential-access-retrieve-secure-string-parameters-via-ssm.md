---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS Systems Manager SecureString Parameter Request with Decryption Flag" prebuilt detection rule.'
---

# AWS Systems Manager SecureString Parameter Request with Decryption Flag

## Triage and analysis

### Investigating AWS Systems Manager SecureString Parameter Request with Decryption Flag

This rule detects when an AWS resource accesses SecureString parameters within AWS Systems Manager (SSM) with the decryption flag set to true. SecureStrings are encrypted using a KMS key, and accessing these with decryption can indicate attempts to access sensitive data.

Adversaries may target SecureStrings to retrieve sensitive information such as encryption keys, passwords, and other credentials that are stored securely. Accessing these parameters with decryption enabled is particularly concerning because it implies the adversary is attempting to bypass the encryption to obtain plain text values that can be immediately used or exfiltrated. This behavior might be part of a larger attack strategy aimed at escalating privileges or moving laterally within an environment to access protected data or critical infrastructure.

#### Possible Investigation Steps

- **Review the Access Event**: Identify the specific API call (`GetParameter` or `GetParameters`) that triggered the rule. Examine the `request_parameters` for `withDecryption` set to true and the name of the accessed parameter.
- **Verify User Identity and Access Context**: Check the `aws.cloudtrail.user_identity` details to understand who accessed the parameter and their role within the organization. This includes checking the ARN and access key ID to determine if the access was authorized.
    - **User ID**: Review the `user.name` field to identify the specific user or role that initiated the API call. Note that the ARN associated may be an assumed role and may not directly correspond to a human user.
- **Contextualize with User Behavior**: Assess whether the access pattern fits the user’s normal behavior or job responsibilities. Investigate any out-of-pattern activities around the time of the event.
- **Analyze Geographic and IP Context**: Using the `source.ip` and `source.geo` information, verify if the request came from a trusted location or if there are any anomalies that suggest a compromised account.
- **Inspect Related CloudTrail Events**: Look for other related events in CloudTrail to see if there was unusual activity before or after this event, such as unusual login attempts, changes to permissions, or other API calls that could indicate broader unauthorized actions.

### False Positive Analysis

- **Legitimate Administrative Use**: Verify if the decryption of SecureString parameters is a common practice for the user’s role, particularly if used in automation scripts or deployment processes like those involving Terraform or similar tools.
- **Authorized Access**: Ensure that the user or role has a legitimate reason to access the SecureString parameters and that the access is part of their expected job responsibilities.

### Response and Remediation

- **Immediate Verification**: Contact the user or team responsible for the API call to verify their intent and authorization.
- **Review and Revise Permissions**: If the access was unauthorized, review the permissions assigned to the user or role to ensure they align with the principle of least privilege.
- **Audit Parameter Access Policies**: Ensure that policies governing access to SecureString parameters are strict and audit logs are enabled to track access with decryption.
- **Incident Response**: If suspicious activity is confirmed, follow through with your organization's incident response plan to mitigate any potential security issues.
- **Enhanced Monitoring and Alerting**: Strengthen monitoring rules to detect unusual accesses to SecureString parameters, especially those that involve decryption.

### Additional Information

This rule focuses solely on SecureStrings in AWS Systems Manager (SSM) parameters. SecureStrings are encrypted using an AWS Key Management Service (KMS) key. When a user accesses a SecureString parameter, they can specify whether the parameter should be decrypted. If the user specifies that the parameter should be decrypted, the decrypted value is returned in the response.
