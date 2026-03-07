---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS S3 Bucket Configuration Deletion" prebuilt detection rule.
---

# AWS S3 Bucket Configuration Deletion

## Triage and analysis

### Investigating AWS S3 Bucket Configuration Deletion

Amazon S3 is a scalable storage service where configurations like policies, replication, and encryption ensure data security and compliance. The detection rule monitors successful deletions of these configurations via the following APIs: `DeleteBucketPolicy`, `DeleteBucketReplication`, `DeleteBucketCors`, `DeleteBucketEncryption` or `DeleteBucketLifecycle`. These operations can be used by an adversary to remove visibility, erase governance or compliance controls, or prepare a bucket for destructive or exfiltration activity.  
Deleting or disabling important configurations may hamper audit trails, hide malicious changes, or reduce the ability for recovery. The detection of these deletes is therefore a potential indicator of defense evasion or impact techniques.

#### Possible investigation steps

- **Identify the Actor and Context**  
  - Review `aws.cloudtrail.user_identity.arn`, `aws.cloudtrail.user_identity.access_key_id` and `aws.cloudtrail.user_identity.type` to identify who performed the deletion.  
  - Determine whether the actor typically manages bucket configurations, or if this is an unusual identity for this kind of operation.  
  - Check `source.ip`, `user_agent.original`, `cloud.region` for anomalous behaviour (unfamiliar IPs, new tooling or region, off-hours actions).

- **Determine the Affected Bucket and Configuration Type**  
  - Examine `aws.cloudtrail.request_parameters` (and `aws.cloudtrail.resources.arn`) to identify the bucket and the sub-resource that was removed. 
  - Determine whether the bucket is used for critical data (audit logs, backups, data warehouse). If so, the deletion is higher risk.

- **Correlate with Other Activity to Establish Chain of Events**  
  - Search for preceding or concurrent CloudTrail events by the same actor or on the same bucket, e.g.:  
    - Removal of logging or access controls (`PutBucketLogging`, `PutBucketAcl`, `PutBucketPolicy`).  
    - Object-level actions soon after configuration removal (`DeleteObject`, `DeleteObjects`, `PutObject`, cross-account copy) that suggest data removal or exfiltration.  
  - Review for configuration additions or changes immediately prior (e.g., versioning disabled, replication removed) — could form part of a larger attack sequence.  

- **Evaluate Intent and Risk**  
  - Confirm whether the change is aligned with an approved change control process (maintenance, re-architecting, cost-optimization).  
  - If no documented justification, or if it affects buckets with sensitive or compliance-related data, treat it as potential malicious behavior.  
  - Prioritize buckets where configuration deletion significantly reduces visibility or recovery capability.

### False positive analysis

- **Scheduled Maintenance or Re-architecture**:  
  - Valid operations may include migrating buckets, retiring services, or reorganizing storage; verify through change logs.  
- **Automation/DevOps Activity**:  
  - Infrastructure-as-Code pipelines or lifecycle clean-up tasks may remove configurations; validate known automation scopes and service-principals.  
- **Test/Development Buckets**:  
  - Non-production environments may frequently change bucket configurations; document and consider whitelisting accordingly.

### Response and remediation

**Containment & Immediate Actions**  
- Temporarily restrict the IAM user or role that performed the deletion, especially for `DeleteBucketPolicy`, `DeleteBucketEncryption`, or `DeleteBucketLifecycle`. 
- Restore missing configurations as soon as possible (e.g., re-apply bucket policy, lifecycle rules, inventory configuration) to prevent further blind spots.

**Investigation & Scope Assessment**  
- Using CloudTrail and S3 Data Events, check object‐level activity from the timeframe immediately before and after the configuration deletion. Look for bulk deletes, new uploads, or copies to external accounts.  
- Check whether other buckets in the account suffered similar configuration changes – potentially part of a wider campaign.

**Recovery & Hardening**  
- Recover affected bucket configurations and ensure they match your organizational baseline and compliance standards (e.g., logging enabled, inventory configured, lifecycle rules active).  
- Enable AWS Config rules such as `s3-bucket-policy-check`, `s3-bucket-lifecycle-configuration-check`, `s3-bucket-logging-enabled` to monitor for unauthorized changes.  
- Apply least‐privilege for configuration deletion permissions; segregate duties so bucket config deletion can only be done via controlled workflows and require multi-step approval.

**Lessons Learned & Prevention**  
- Conduct a post-incident review to determine root cause (credential compromise, misconfigured automation, malicious insider) and strengthen monitoring, alerting and access controls accordingly.


