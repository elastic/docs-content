---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS STS Role Assumption by User" prebuilt detection rule.'
---

# AWS STS Role Assumption by User

## Triage and analysis

### Investigating AWS STS Role Assumption by User

This rule detects when a user assumes a role in AWS Security Token Service (STS), receiving temporary credentials to access AWS resources. While often used for legitimate purposes, this action can be leveraged by adversaries to obtain unauthorized access, escalate privileges, or move laterally within an AWS environment.

### Possible investigation steps

- **Identify the User and Assumed Role**:
  - **User Identity**: Check `aws.cloudtrail.user_identity.arn` for details about the initiator of the `AssumeRole` action.
  - **Role Assumed**: Review `aws.cloudtrail.resources.arn` to confirm the role assumed and ensure it aligns with the user’s standard permissions.
  - **Session Name**: Note `aws.cloudtrail.flattened.request_parameters.roleSessionName` for context on the purpose of the session.
  - **Expiration Time**: Use `aws.cloudtrail.flattened.response_elements.credentials.expiration` to confirm the credential expiration.

- **Inspect User Agent and Source Information**:
  - **User Agent**: Analyze the `user_agent.original` field to identify if specific tooling or SDKs like AWS CLI, Boto3, or custom agents were used.
  - **Source IP and Geolocation**: Examine `source.ip` and `source.geo` fields to determine the origin of the request, confirming if it aligns with expected locations.

- **Correlate with Related Events**:
  - **Identify Patterns**: Review related CloudTrail events for unusual access patterns, such as resource access or sensitive actions following this `AssumeRole` action.
  - **Filter High-Volume Roles**: If this role or user has a high volume of access, evaluate `roleArn` or `user_agent` values for common patterns and add trusted entities as exceptions.

- **Review the Privileges of the Assumed Role**:
  - **Permissions**: Examine permissions associated with the `roleArn` to assess its access scope.
  - **Authorized Usage**: Confirm if the role is used frequently for administrative purposes and if this aligns with the user’s regular responsibilities.

### False positive analysis

- **Automated Processes and Applications**: Applications or scheduled tasks may assume roles regularly for operational purposes. Validate the consistency of the `user_agent` or `roleArn` with known automated workflows.
- **Standard IAM Policy Usage**: Confirm if the user or application routinely assumes new roles for normal operations by reviewing historical activity.

### Response and remediation

- **Terminate Unauthorized Sessions**: If the role assumption is deemed unauthorized, revoke the session by modifying IAM policies or the permissions associated with the assumed role.
- **Strengthen Monitoring and Alerts**: Implement additional monitoring for specific high-risk roles, especially those with elevated permissions.
- **Regularly Manage Exceptions**: Regularly review high-volume roles and user agent patterns to refine alerts, minimizing noise by adding trusted patterns as exceptions.
- **Incident Response**: If confirmed as malicious, follow incident response protocols for containment, investigation, and remediation.

### Additional information

For more details on managing and securing AWS STS in your environment, refer to the [AWS STS documentation](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html).
