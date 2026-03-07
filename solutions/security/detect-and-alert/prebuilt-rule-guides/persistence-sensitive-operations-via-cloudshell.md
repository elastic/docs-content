---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS Sensitive IAM Operations Performed via CloudShell" prebuilt detection rule.
---

# AWS Sensitive IAM Operations Performed via CloudShell

## Triage and analysis

### Investigating AWS Sensitive IAM Operations Performed via CloudShell

AWS CloudShell is a browser-based shell environment that provides instant command-line access to AWS resources without requiring local CLI installation or credential configuration. While this is convenient for legitimate administrators, it also provides adversaries with a powerful tool if they gain access to a compromised AWS console session. Attackers can use CloudShell to perform sensitive operations without leaving artifacts on their local systems.

This rule detects high-risk IAM operations performed via CloudShell, including credential creation, user management, and policy attachment. These actions are commonly seen in post-compromise scenarios where attackers establish persistence or escalate privileges.

### Possible investigation steps

- **Identify the actor**
  - Review `aws.cloudtrail.user_identity.arn` to determine which IAM principal performed the action.
  - Check `source.ip` and `source.geo` fields to verify the request origin matches expected administrator locations.
  - Investigate the console login event that established the CloudShell session.

- **Analyze the specific action**
  - Review `event.action` to understand exactly what operation was performed.
  - For `CreateAccessKey` or `CreateUser`, identify the target principal and assess whether this was authorized.
  - For policy attachments, review which policies were attached and to which entities.

- **Review request and response details**
  - Examine `aws.cloudtrail.request_parameters` for specifics like user names, policy ARNs, or role configurations.
  - Check `aws.cloudtrail.response_elements` for created resource identifiers.

- **Correlate with surrounding activity**
  - Search for preceding events such as `ConsoleLogin` from the same session or IP address.
  - Look for MFA bypass indicators or unusual login patterns before CloudShell usage.
  - Check for subsequent use of any created credentials or roles.

- **Assess the broader context**
  - Determine if this CloudShell usage pattern is typical for this user.
  - Review recent access patterns for the console session that initiated CloudShell.

### False positive analysis

- Routine administrative tasks using CloudShell are common in some organizations. Create baseline profiles for users who regularly use CloudShell.
- Infrastructure automation testing may involve CloudShell for quick validation. Verify with the user.


### Response and remediation

- If unauthorized, immediately terminate the console session and revoke any created credentials.
- Rotate credentials for any IAM users or roles that may have been compromised.
- Review and remove any unauthorized users, access keys, roles, or policy attachments.
- Consider restricting CloudShell access via SCPs or IAM policies for sensitive accounts.
- Implement session duration limits to reduce the window of opportunity for console session abuse.

### Additional information

- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)**
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 

