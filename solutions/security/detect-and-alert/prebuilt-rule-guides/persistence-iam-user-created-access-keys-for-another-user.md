---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS IAM User Created Access Keys For Another User" prebuilt detection rule.
---

# AWS IAM User Created Access Keys For Another User

## Triage and analysis

### Investigating AWS IAM User Created Access Keys For Another User

AWS IAM access keys are long-term credentials that grant programmatic access to AWS resources. The `iam:CreateAccessKey` permission allows an IAM principal to generate new access keys for an existing IAM user.  
While this operation can be legitimate (for example, credential rotation), it can also be abused to establish persistence or privilege escalation if one user creates keys for another account without authorization.

This rule identifies `CreateAccessKey` API calls where the calling user (`aws.cloudtrail.user_identity.arn`) differs from the target user (`aws.cloudtrail.request_parameters.userName`), indicating one IAM identity creating credentials for another.

#### Possible investigation steps

- **Confirm both user identities and intent.**  
  Identify the calling user (who performed `CreateAccessKey`) and the target user (whose access key was created). Contact both account owners or application teams to confirm if this operation was expected.

- **Review CloudTrail event details.**  
  Check the following fields directly in the alert or corresponding CloudTrail record:  
  - `source.ip` — does it align with expected corporate ranges or known admin automation?  
  - `user_agent.original` — AWS Console, CLI, SDK, or custom client? Unexpected user agents (for example, non-SDK scripts) may indicate manual or unauthorized use.  
  - `source.geo` fields — verify the location details are expected for the identity.

- **Correlate with related IAM activity.**  
  In CloudTrail, search for subsequent or nearby events such as:  
  - `AttachUserPolicy`, `AttachGroupPolicy`, `UpdateAssumeRolePolicy`, or `CreateUser`.  
  These can indicate privilege escalation or lateral movement.  
  Also review whether the same principal recently performed `CreateAccessKey` for multiple users or repeated this action across accounts.

- **Inspect the new access key’s usage.**  
  Search for the newly created key ID (`aws.cloudtrail.response_elements.accessKey.accessKeyId`) in CloudTrail events following creation. Determine if it was used from unusual IP addresses, geographies, or services.  

- **Assess the risk of credential compromise.**  
  If you suspect malicious behavior, consider the following indicators:  
  - A non-admin user invoking `CreateAccessKey` for another user.  
  - Creation outside of normal automation pipelines.  
  - Use of the new key from a different IP or AWS account soon after creation.

- **Scope related activity.**  
  Review all activity from the calling user in the past 24–48 hours, focusing on `iam:*` API calls and resource creation events.  
  Correlate any S3, EC2, or KMS access attempts made using the new key to identify potential impact or data exposure.

### False positive analysis

- **Expected credential rotation.**  
  Some environments delegate credential rotation responsibilities to centralized automation or specific admin roles. Confirm if the calling user is authorized for such actions.  
- **Administrative workflows.**  
  Account provisioning systems may legitimately create keys on behalf of users. Check for standard tags, automation tools, or user agents that indicate managed operations.  
- **Service-linked roles or external IAM automation.**  
  Some AWS services create or rotate credentials automatically. Validate if the caller is a service-linked role or an automation IAM role used by a known deployment process.

### Response and remediation

**Immediate containment**
- Deactivate or delete the access key from the target IAM user immediately using the AWS Console, CLI, or API (`DeleteAccessKey`).  
- Rotate or reset credentials for both the calling and target users to eliminate possible compromise.  
- Restrict risky principals. Temporarily deny `iam:CreateAccessKey` and `iam:UpdateAccessKey` permissions for non-administrative roles while scoping the incident.  
- Enable or confirm MFA on both accounts involved, if not already enforced.

**Evidence preservation**
- Export all related `CreateAccessKey`, `DeleteAccessKey`, and `UpdateAccessKey` events within ±30 minutes of the alert to an evidence bucket.  
- Preserve CloudTrail, GuardDuty, and AWS Config data for the same period.  
- Record key event details: caller ARN, target user, `accessKeyId`, `source.ip`, `userAgent`, and timestamps.

**Scoping and investigation**
- Search CloudTrail for usage of the new access key ID after creation. Identify any API activity or data access tied to it.  
- Review IAM policy changes, group modifications, or new role assumptions around the same time.  
- Determine if any additional credentials or trust policy changes were made by the same actor.  
- Check for GuardDuty findings referencing anomalous credential usage or suspicious API behavior.

**Recovery and hardening**
- Remove or disable any unauthorized keys and re-enable only verified credentials.  
- Implement least-privilege IAM policies to limit which users can perform `CreateAccessKey`.  
- Monitor for future `CreateAccessKey` events where `userIdentity.arn != request_parameters.userName`.  
- Ensure Cloudtrail, GuardDuty and Security Hub are active across all regions.  
- Educate administrative users on secure key rotation processes and the risk of cross-user key creation.  

### Additional information

- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/):** Reference “Credential Compromise” and “IAM Misuse” procedures for containment and recovery.  
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/):** See “Identity Access Review” and “Unauthorized Access Key Creation” for example response flows.  
- **AWS Documentation:** [Best practices for managing access keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).  
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).  

