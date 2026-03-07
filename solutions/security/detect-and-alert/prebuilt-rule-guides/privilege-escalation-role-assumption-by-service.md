---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS STS Role Assumption by Service" prebuilt detection rule.
---

# AWS STS Role Assumption by Service

## Triage and analysis

### Investigating AWS STS Role Assumption by Service

This rule identifies instances where AWS STS (Security Token Service) is used to assume a role, granting temporary credentials for AWS resource access. While this action is often legitimate, it can be exploited by adversaries to obtain unauthorized access, escalate privileges, or move laterally within an AWS environment.

#### Possible Investigation Steps

- **Identify the Actor and Assumed Role**:
  - **User Identity**: Review the `aws.cloudtrail.user_identity.invoked_by` field to determine which service initiated the `AssumeRole` action.
  - **Role Assumed**: Check the `aws.cloudtrail.resources.arn` field to confirm the assumed role and ensure it aligns with expected responsibilities.
  - **Session Name**: Observe the `aws.cloudtrail.flattened.request_parameters.roleSessionName` for context on the session's intended purpose, if available.
 - **Expiration Time**: Verify `aws.cloudtrail.flattened.response_elements.credentials.expiration` to determine when the credentials expire or expired.

- **Inspect the User Agent for Tooling Identification**:
  - **User Agent Details**: Review the `user_agent.original` field to identify the tool or SDK used for the role assumption. Indicators include:
    - **AWS SDKs (e.g., Boto3)**: Often used in automated workflows or scripts.
    - **AWS CLI**: Suggests command-line access, potentially indicating direct user interaction.
    - **Custom Tooling**: Unusual user agents may signify custom or suspicious tools.

- **Contextualize with Related Events**:
  - **Review Event Patterns**: Check surrounding CloudTrail events to see if other actions coincide with this `AssumeRole` activity, such as attempts to access sensitive resources.
  - **Identify High-Volume Exceptions**: Due to the potential volume of `AssumeRole` events, determine common, legitimate `roleArn` values or `user_agent` patterns, and consider adding these as exceptions to reduce noise.

- **Evaluate the Privilege Level of the Assumed Role**:
  - **Permissions**: Inspect permissions associated with the assumed role to understand its access level.
  - **Authorized Usage**: Confirm whether the role is typically used for administrative purposes and if the assuming entity frequently accesses it as part of regular responsibilities.

### False Positive Analysis

- **Automated Workflows and Applications**: Many applications or scheduled tasks may assume roles for standard operations. Check user agents and ARNs for consistency with known workflows.
- **Routine AWS Service Actions**: Historical data may reveal if the same service assumes new roles regularly as part of authorized operations.

### Response and Remediation

- **Revoke Unauthorized Sessions**: If unauthorized, consider revoking the session by adjusting IAM policies or permissions associated with the assumed role.
- **Enhance Monitoring and Alerts**: Set up enhanced monitoring for high-risk roles, especially those with elevated privileges.
- **Manage Exceptions**: Regularly review and manage high-frequency roles and user agent patterns, adding trusted ARNs and user agents to exception lists to minimize alert fatigue.
- **Incident Response**: If malicious behavior is identified, follow incident response protocols, including containment, investigation, and remediation.

### Additional Information

For more information on managing and securing AWS STS, refer to the [AWS STS documentation](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) and AWS security best practices.

