---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS S3 Bucket Policy Added to Share with External Account" prebuilt detection rule.
---

# AWS S3 Bucket Policy Added to Share with External Account

## Triage and analysis

### Investigating AWS S3 Bucket Policy Added to Share with External Account

This rule detects when an S3 bucket policy is modified using the `PutBucketPolicy` API call to include an external AWS account ID.
It compares the bucket’s `recipient_account_id` to any account IDs included in the policy’s `Effect=Allow` statement, triggering
an alert if the two do not match.  

Adversaries may exploit this to backdoor a bucket and exfiltrate sensitive data by granting permissions to another AWS account
they control, enabling ongoing access to the bucket’s contents even if IAM credentials are rotated or revoked.

This detection specifically focuses on policy-based sharing and does not alert when:
- The account ID appears within the bucket or object name being shared.
- The account owner explicitly matches the policy’s condition keys on something other than an ARN or account id (i.e. IP address).
  
To fully monitor for suspicious sharing behavior, use this rule in combination with detections for:
- Unusual PutBucketPolicy requests
- Cross-account object access (e.g., `GetObject`, `PutObject`)
- Changes to bucket ACLs or access points

#### Possible investigation steps

- **Identify the Actor and Context**
  - Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.access_key_id` to identify who made the change.
  - Determine if the identity typically manages S3 bucket policies.  
  - Examine `aws.cloudtrail.resources.arn` to determine which bucket is being shared.

- **Analyze the Policy Change**
  - Review `aws.cloudtrail.request_parameters` to extract the policy JSON and identify the external AWS account ID(s) referenced.  
  - Check for `Effect=Allow` statements granting broad permissions such as `"Action": "s3:*"` or `"Resource": "*"`.  
  - Verify if the added principals correspond to known partners or external vendors.
  - If AWS account ID(s) were only part of `Effect=Deny` statements, then this rule can be closed as a false positive. 

- **Review Context and Source**
  - Check `source.ip`, `source.geo`, and `user_agent.original` for anomalies — such as new IP ranges, access from unfamiliar geographies, or use of programmatic clients (`boto3`, `aws-cli`).

- **Correlate with Related Activity**
  - Search CloudTrail for subsequent activity by the external AWS account ID(s):
    - `GetObject`, `ListBucket`, or `PutObject` events that indicate data access or exfiltration.
  - Look for additional configuration changes by the same actor, such as:
    - `PutBucketAcl`, `PutBucketVersioning`, or `PutBucketReplication` — often part of a larger bucket compromise chain.
  - Determine if multiple buckets were modified in quick succession.

- **Validate Intent**
  - Review internal change requests or documentation to confirm whether this external sharing was approved.  
  - If no approval exists, escalate immediately for potential compromise.

### False positive analysis

- **Authorized Cross-Account Access**
  - Some organizations legitimately share S3 buckets across accounts within a trusted AWS Organization or partner accounts.  
  - Validate whether the external account ID belongs to a known entity or service provider and is documented in your allowlist.
- **Automation or Deployment Pipelines**
  - Continuous integration/deployment pipelines may temporarily attach cross-account policies for replication or staging.  
  - Verify the `user_agent.original` or role name — automation often includes identifiable strings.
- **Naming and Rule Logic Limitations**
  - This rule excludes detections where the account ID appears in the bucket resource ARN (e.g., `mybucket-123456789012`).  
  - Such patterns are common in automated provisioning. For those scenarios, rely on complementary rules that directly monitor `PutBucketPolicy` events against those buckets.

### Response and remediation

- **Immediate Review and Containment**
  - If unauthorized sharing is confirmed, use the AWS CLI or Console to delete or revert the modified policy (`aws s3api delete-bucket-policy` or restore from version control).  
  - Remove external principals and reapply the correct bucket policy.  
  - Rotate access keys for the actor involved, especially if API access came from unexpected locations or tools.

- **Investigation and Scoping**
  - Identify whether data was accessed by the external account via `GetObject` or `ListBucket` operations.  
  - Search CloudTrail logs for other buckets modified by the same actor or IP within the same timeframe.
  - Use AWS Config to review version history of affected bucket policies and detect similar cross-account permissions.

- **Recovery and Hardening**
  - Restrict `s3:PutBucketPolicy` to a limited set of administrative roles using least privilege.
  - Enable AWS Config rule `s3-bucket-policy-grantee-check` to monitor for unauthorized policy additions.
  - Use AWS GuardDuty or Security Hub findings to correlate policy changes with data exfiltration or credential compromise events.
  - Apply service control policies (SCPs) to block cross-account sharing unless explicitly approved.

### Additional information
  - **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
  - **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
  - **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).

