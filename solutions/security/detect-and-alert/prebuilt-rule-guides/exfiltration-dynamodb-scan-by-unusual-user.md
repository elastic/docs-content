---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS DynamoDB Scan by Unusual User" prebuilt detection rule.
---

# AWS DynamoDB Scan by Unusual User

## Triage and analysis

### Investigating AWS DynamoDB Scan by Unusual User

This rule identifies when an AWS DynamoDB table is scanned by a user who does not typically perform this action. Adversaries may use the Scan operation to collect sensitive information or exfiltrate data from DynamoDB tables. This rule detects unusual user activity by monitoring for the Scan action in CloudTrail logs.

This is a [New Terms](https://www.elastic.co/guide/en/security/current/rules-ui-create.html#create-new-terms-rule) rule that only flags when this behavior is observed for the first time.

#### Possible Investigation Steps

- Identify the Actor: Review the `aws.cloudtrail.user_identity.arn` field to identify the user who requested the subscription. Verify if this actor typically performs such actions and has the necessary permissions. It may be unusual for this activity to originate from certain user types, such as an assumed role or federated user.
- Review the Source IP: Check the `source.ip` field to determine the source of the request. If the request comes from an unexpected location or IP address, it may indicate a compromised account or unauthorized access.
- Analyze the Request Parameters: Examine the `aws.cloudtrail.request_parameters` field to understand the details of the Scan request. Look for any unusual parameters or patterns that may indicate malicious intent. This also details the DynamoDB table being scanned.
- Review Access Key: Check the `aws.cloudtrail.user_identity.access_key_id` field to identify the access key used for the request. Determine if this key is associated with a legitimate user or if it has been compromised.


### False Positive Analysis

- Historical User Actions: If the user has a history of scanning DynamoDB tables for legitimate purposes, this may not be a false positive. Review the user's activity logs to determine if this behavior is consistent with their normal actions.
- Automated Processes: Some automated processes or applications may perform scans on DynamoDB tables as part of their functionality. If the user is associated with such a process, this may not be a false positive.

### Response and Remediation

- Immediate Review and Reversal: If the Scan action is determined to be unauthorized, immediately revoke the user's access to the DynamoDB table and any associated resources. This may involve disabling the user's account or removing their permissions.
- Investigate Compromise: If the Scan action is determined to be malicious, investigate the source of the request and any potential compromise of the user's account. This may involve reviewing access logs, resetting passwords, and enabling multi-factor authentication (MFA) for the affected user. If export options were used with the CLI or SDK, they may have been saved locally or to a remote location.
- Review IAM Policies: Review the IAM policies associated with the user to ensure that they have the appropriate permissions for their role. If necessary, update the policies to restrict access to sensitive resources.
- Monitor for Future Activity: Continue to monitor the user's activity for any further suspicious behavior. Set up additional alerts or logging to detect any future unauthorized access attempts.

### Additional Information

For further guidance on managing and securing DynamoDB in AWS environments, refer to the [AWS DynamoDB documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/security.html) and AWS best practices for security.

