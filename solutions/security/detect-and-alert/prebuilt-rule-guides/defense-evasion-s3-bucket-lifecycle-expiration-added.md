---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS S3 Bucket Expiration Lifecycle Configuration Added" prebuilt detection rule.
---

# AWS S3 Bucket Expiration Lifecycle Configuration Added

## Triage and analysis

### Investigating AWS S3 Bucket Expiration Lifecycle Configuration Added

This rule detects when a lifecycle expiration policy is added to an S3 bucket via the `PutBucketLifecycle` or `PutBucketLifecycleConfiguration` API. Note: `PutBucketLifecycleConfiguration` is the newer supported API call, however both of these API calls show up as `PutBucketLifecycle` in Cloudtrail [ref](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cloudtrail-logging-s3-info.html#cloudtrail-bucket-level-tracking).
Lifecycle expiration automatically deletes objects after a defined period (`Expiration:Days`), which can be leveraged by adversaries to erase logs, exfiltration evidence, or security artifacts before detection and response teams can review them.

Because deletion is automated and often silent, detecting the initial configuration event is critical.

#### Possible investigation steps

**Identify the actor and execution context**

- **Principal and Identity Type**:  
  Review `aws.cloudtrail.user_identity.arn`, `aws.cloudtrail.user_identity.type`, and `aws.cloudtrail.user_identity.access_key_id`.  
  Determine if the actor is an IAM user, role, or automation service account.  
  - Unusual: temporary credentials, federated roles, or previously inactive accounts.
- **Source Information**:  
  Review `source.ip`, `cloud.region`, and `user_agent.original` for unexpected geolocations, tool usage (CLI, SDK, automation service), or newly-observed hosts.
- **Timestamp correlation**:  
  Use `@timestamp` to check if this activity occurred during change windows or off-hours.

**Examine the lifecycle configuration details**
- Extract details from `aws.cloudtrail.request_parameters`:
  - `Expiration`: Number of days until deletion (e.g., `Days=1` indicates rapid expiry).  
  - `Prefix`: If limited to certain object paths (e.g., `/logs/`, `/tmp/`).  
  - `Status`: `Enabled` vs. `Disabled`.  
  - `ID` or rule name: May reveal purpose (“cleanup-test”, “delete-logs”).
- Determine the affected bucket from `aws.cloudtrail.resources.arn` or `aws.cloudtrail.resources.type`.  
  Cross-check the bucket’s purpose (e.g., log storage, data lake, analytics export, threat forensics).  
  - High-risk if the bucket contains audit, CloudTrail, or application logs.

**Correlate with related AWS activity**
Use AWS CloudTrail search or your SIEM to pivot for:
- **Prior suspicious activity**:
  - `DeleteObject`, `PutBucketPolicy`, `PutBucketAcl`, or `PutBucketLogging` changes to disable visibility.
  - IAM changes such as `AttachUserPolicy` or `CreateAccessKey` that may have enabled this modification.
- **Subsequent changes**:
  - `PutBucketLifecycle` events in other buckets (repeated pattern).  
  - Rapid `DeleteObject` events or object expiration confirmations.
- **Cross-account activity**:
  - Lifecycle rules followed by replication or cross-account copy events may indicate lateral exfiltration setup.

**Assess intent and risk**
- Verify if the actor has a valid business case for altering object retention.  
- If the bucket is used for security, compliance, or audit data, treat this as potential defense evasion.  
- Evaluate whether the lifecycle rule removes data faster than your retention policy permits.

### False positive analysis

- **Cost optimization**: Storage teams may automate lifecycle policies to reduce cost on infrequently accessed data.
- **Compliance enforcement**: Organizations implementing legal retention policies may set expiration for specific datasets.
- **Automation and IaC pipelines**: Terraform or CloudFormation templates often apply `PutBucketLifecycle` during resource deployment.

### Response and remediation

**Containment and validation**
**Revert or disable** the lifecycle configuration if it is unauthorized:  
   - Use the AWS Console or CLI (`delete-bucket-lifecycle` or `put-bucket-lifecycle-configuration --lifecycle-configuration Disabled`).
**Preserve evidence**:  
   - Copy existing objects (especially logs or forensic data) before they expire.  
   - Enable object versioning or replication to protect against loss.

**Investigation**
Review CloudTrail and S3 Access Logs for the same bucket:
   - Identify who and what performed previous deletions.
   - Determine whether any objects of investigative value have already been removed.
Search for other S3 buckets where similar lifecycle configurations were added in a short timeframe.

**Recovery and hardening**
Implement guardrails:
   - Use AWS Config rules like `s3-bucket-lifecycle-configuration-check` to monitor lifecycle changes.
   - Restrict `s3:PutLifecycleConfiguration` to specific administrative roles.
   - Enable [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html) on log or evidence buckets to enforce immutability.
Enable Security Hub and GuardDuty findings for additional anomaly detection on S3 data management activity.

### Additional information

- **AWS Documentation**  
  - [S3 Lifecycle Configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-expire-general-considerations.html)  
  - [DeleteBucketLifecycle API Reference](https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteBucketLifecycle.html)
- **AWS Playbooks**  
  - [Data Exposure and Exfiltration Response](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/IRP-PersonalDataBreach.md)  
  - [AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/main)

