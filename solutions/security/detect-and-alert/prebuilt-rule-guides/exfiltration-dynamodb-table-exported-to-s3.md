---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS DynamoDB Table Exported to S3" prebuilt detection rule.'
---

# AWS DynamoDB Table Exported to S3

## Triage and analysis

### Investigating AWS DynamoDB Table Exported to S3

This rule identifies when an AWS DynamoDB table is exported to S3. Adversaries may use the ExportTableToPointInTime operation to collect sensitive information or exfiltrate data from DynamoDB tables. This rule detects unusual user activity by monitoring for the ExportTableToPointInTime action in CloudTrail logs.

This is a New Terms rule that only flags when this behavior is observed for the first time.

#### Possible Investigation Steps
- Identify the Actor: Review the `aws.cloudtrail.user_identity.arn` field to identify the user who requested the export. Verify if this actor typically performs such actions and has the necessary permissions. It may be unusual for this activity to originate from certain user types, such as an assumed role or federated user.
- Review the Source IP: Check the `source.ip` field to determine the source of the request. If the request comes from an unexpected location or IP address, it may indicate a compromised account or unauthorized access.
- Review Access Key: Check the `aws.cloudtrail.user_identity.access_key_id` field to identify the access key used for the request. Determine if this key has been compromised.
- Analyze the Request Parameters: Examine the `aws.cloudtrail.request_parameters` field to understand the details of the ExportTableToPointInTime request. Look for any unusual parameters or patterns that may indicate malicious intent. This also details the DynamoDB table being exported.

### False Positive Analysis
- Historical User Actions: If the user has a history of exporting DynamoDB tables for legitimate purposes, this may be a false positive. Review the user's activity logs to determine if this behavior is consistent with their normal actions.
- Automated Processes: Some automated processes or applications may perform exports on DynamoDB tables as part of their functionality. If the user is associated with such a process, this may be a false positive.

### Response and Remediation
- Immediate Review and Reversal: If the ExportTableToPointInTime action is determined to be unauthorized, immediately revoke the user's access to the DynamoDB table and any associated resources. This may involve disabling the user's access keys or removing their permissions.
- Investigate Compromise: If the ExportTableToPointInTime action is determined to be malicious, investigate the source and destination of the request and any potential compromise of the user's account. If the destination S3 bucket is not known, it may be a sign of data exfiltration and may require incident response.
- Review IAM Policies: Review the IAM policies associated with the user to ensure that they have the appropriate permissions for their role. If necessary, update the policies to restrict access to sensitive resources.
- Monitor for Future Activity: Continue to monitor the user's activity for any further suspicious behavior. Set up additional alerts or logging to detect any future unauthorized access attempts.

### Additional Information

For further guidance on managing and securing DynamoDB in AWS environments, refer to the [AWS DynamoDB documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/security.html) and AWS best practices for security.
