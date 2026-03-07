---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS EC2 Export Task" prebuilt detection rule.
---

# AWS EC2 Export Task

## Triage and analysis

### Investigating AWS EC2 Export Task

The APIs `CreateInstanceExportTask`, `ExportImage`, and `CreateStoreImageTask` allow the export of a running or stopped EC2 instance (or its AMI/image) to external storage (e.g., S3) or image formats. While often used for migration, cloning or backup, adversaries can leverage these actions to copy full VM state or images out of the environment for exfiltration.

#### Possible investigation steps

**Identify the actor and context**  
   - Check `aws.cloudtrail.user_identity.arn`, `aws.cloudtrail.user_identity.type`, `aws.cloudtrail.user_identity.access_key_id` to identify who made the call.  
   - Verify `user_agent.original`, `source.ip` and `@timestamp` to determine whether the action is by known automation, trusted operator, or an unexpected identity or location.  
   - Confirm `cloud.account.id` and `cloud.region` match the expected account/region for export tasks.

**Examine the specific export/image task details**  
   - Review `aws.cloudtrail.request_parameters` for details such as the `InstanceId`, `TargetEnvironment`, `S3Bucket`, `S3Key`, `DiskImageFormat`, `ContainerFormat`. 
   - Check `aws.cloudtrail.response_elements` for the resulting export task ID and status.  
   - Determine whether the exported instance or image contained sensitive workloads (e.g., production databases, critical systems) via instance tags or asset inventory.

**Pivot to related API calls/events**  
   - Look for follow-on tasks such as:  
     - S3 bucket writes or cross-account bucket ACL changes (`PutBucketAcl`/`PutBucketPolicy`) referencing the export S3 bucket or key.  
     - `CopyImage`, `ModifyImageAttribute`, or `ShareImage` events if the exported image is copied or shared.  
     - Network or usage anomalies in the region or from the S3 bucket (large downloads from the exported object).  
   - Check for preceding suspicious actions that could indicate compromise: `AssumeRole`, `CreateAccessKey`, `AttachUserPolicy`, or unusual `Describe*` operations.

**Assess legitimacy and risk**  
   - Confirm whether this export was authorized (via change ticket or migration workflow) and whether the principal has a documented justification for VM export.  
   - If unauthorized, assess what was exported, where it is stored, how it may be transferred or used externally, and the data risk exposure.

### False positive analysis

- Legitimate migration or backup workflows may trigger these export/image APIs.  
- Development/test environments may export VM images or instances for sandbox cloning.  
- Known automation tools may create exports at scheduled times.  

### Response and remediation

- Immediately identify and disable or isolate any object/resource created by the export (e.g., the S3 bucket/object, image ID) that is suspected of unauthorized use.  
- Revoke the access credentials (`aws.cloudtrail.user_identity.access_key_id`) used if they show unusual activity.  
- Rotate keys, enforce MFA, and review IAM permissions for the principal.  
- Audit the exported VM/image: review its contents if possible, check whether it has been moved off-account.  
- Strengthen monitoring: set alerts for subsequent large data transfers from the S3 export location, cross-account sharing of exported images, or anomalous AMI imports.  
- Update policy: restrict who can perform exports, monitor export actions via AWS Config or CloudTrail, tag and track export tasks and their destinations.

