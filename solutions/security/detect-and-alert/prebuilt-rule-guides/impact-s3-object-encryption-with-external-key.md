---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS S3 Object Encryption Using External KMS Key" prebuilt detection rule.
---

# AWS S3 Object Encryption Using External KMS Key

## Triage and analysis

### Investigating AWS S3 Object Encryption Using External KMS Key

This rule detects when an S3 `CopyObject` operation encrypts an object using a KMS key belonging to a different AWS account than the bucket owner. This behavior is unusual and a strong indicator of:

- Cloud ransomware techniques, where adversaries encrypt data using a key only they control.
- Cross-account privilege misuse, especially when an unauthorized principal has write access to S3.
- Misconfigured bucket permissions, enabling principals from another account to perform privileged copy operations.
- Early impact-stage activity in incidents where attackers prepare to destroy availability or deny the owner access.

The rule uses ESQL to identify cases where the `cloud.account.id` (bucket owner) differs from the dissected `kms_key_account_id` used for encrypting the new object version.


#### Possible investigation steps

**Identify the actor and access pathway**
- Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.access_key_id`.
- Check whether the caller is:
  - A legitimate cross-account automation role,  
  - A compromised IAM user or workload identity, or  
  - A federated identity behaving outside of normal patterns.
- Inspect `user_agent.original` to determine whether the action came from the AWS Console, CLI, SDK, or unusual tooling.

**Analyze the encryption behavior**
- Inspect the dissected KMS key fields:
  - `Esql.aws_cloudtrail_request_parameters_kms_key_account_id`
  - `Esql.aws_cloudtrail_request_parameters_kms_key_id`
- Confirm whether the external key:
  - Belongs to an attacker-controlled account,  
  - Is unknown to your organization, or  
  - Lives in a shared or security tooling account.

**Assess the objects affected**
- Review:
  - `Esql.aws_cloudtrail_request_parameters_target_bucket_name`
  - `Esql.aws_cloudtrail_request_parameters_target_object_key`
- Identify:
  - Whether objects were overwritten or new encrypted copies were created.
  - The sensitivity or criticality of the affected data.
  - Whether object versioning is enabled (important for recovery).

**Correlate surrounding access patterns**
Pivot in CloudTrail on:
- The same access key ID  
- The same IAM principal  
- Affected bucket ARN  

Look for:
- `DeleteObject` or `DeleteObjects` calls (common in ransomware behavior)
- Mass enumeration prior to the event (`ListObjectsV2`, `GetObject`)
- Other impact-stage actions (`PutBucketPolicy`, `PutBucketAcl`, disabling logging)
- Attempts to encrypt additional objects in rapid succession

**Evaluate bucket permissions and exposure**
Review:
- S3 bucket policy changes
- IAM roles with `s3:PutObject` or `s3:PutObjectAcl` permissions
- Whether unintended cross-account `Principal` entries exist
- Whether the KMS key policy explicitly trusts your account or a foreign one

**Validate business justification**
- Confirm with storage, data engineering, or application teams whether:
  - Any migration, transformation, or backup workflows should be encrypting objects cross-account.
  - Scheduled jobs or CI/CD pipelines were operating at the time of the event.

### False positive analysis

- **Expected cross-account encryption**  
  Many organizations use centralized encryption accounts or shared security accounts. Validate:
  - Whether the KMS key account is part of your AWS Organization
  - Whether the workflow, role, or application is documented
  - Whether the principal routinely performs CopyObject operations

### Response and remediation

**Contain and prevent further impact**
- Immediately restrict S3 write access for the principal involved.
- If the KMS key is attacker-controlled, the impacted objects may be unrecoverable without versioning.
- If object versioning is disabled, enable it on the affected bucket to strengthen future resilience.

**Investigate scope and severity**
- Identify:
  - Additional objects encrypted using external keys
  - Related suspicious actions (delete, modify, exfiltration events)
  - Whether any ransom markers or unauthorized files were uploaded
- Validate whether the external KMS key grants *decrypt* permission back to the bucket owner (rare in attacker use).

**Recover and secure the bucket**
- Restore accessible previous versions if versioning is enabled.
- Revoke unauthorized access key pairs or session credentials.
- Audit bucket policies, ACLs, and IAM conditions (`aws:PrincipalArn`, `aws:SourceAccount`, `aws:SourceArn`).
- Tighten cross-account access controls:
  - Remove unintended `Principal` clauses
  - Restrict KMS usage to known accounts
  - Enforce SCPs that block cross-account KMS use unless explicitly approved

**Long-term hardening**
- Integrate object-level access logging and S3 server access logging into security monitoring.
- Add AWS Config rules (or Security Hub controls) detecting:
  - Public buckets
  - Cross-account access to S3
  - KMS policies permitting foreign principals
- Document required cross-account workflows and add explicit allowlists.

### Additional information

- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).

