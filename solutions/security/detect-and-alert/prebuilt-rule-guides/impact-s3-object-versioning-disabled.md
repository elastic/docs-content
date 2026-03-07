---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS S3 Object Versioning Suspended" prebuilt detection rule.
---

# AWS S3 Object Versioning Suspended

## Triage and analysis

### Investigating AWS S3 Object Versioning Suspended

This rule detects when object versioning for an S3 bucket is suspended. S3 object versioning protects against data loss by maintaining prior versions of objects, allowing recovery if they are deleted or overwritten.  
Adversaries with access to a misconfigured or compromised S3 bucket may disable versioning to inhibit recovery efforts, conceal data destruction, or prepare for ransomware-like activity.  
This rule uses [EQL](https://www.elastic.co/guide/en/security/current/rules-ui-create.html#create-eql-rule) to detect use of the `PutBucketVersioning` API operation where the request parameters include `Status=Suspended`.

#### Possible investigation steps

- **Identify the Actor**  
  - Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.access_key_id` to determine who performed the action.  
  - Verify whether this user or role has a legitimate operational reason to modify bucket versioning and whether such actions are common for this identity.

- **Analyze the Source and Context**  
  - Review `source.ip` and `user_agent.original` to assess the origin of the request.  
  - Check for unusual geographic locations, IP ranges, or clients that do not typically manage storage configurations.  

- **Evaluate the Affected Resource**  
  - Review `aws.cloudtrail.resources.arn` or `aws.cloudtrail.request_parameters` to identify which bucket’s versioning was modified.  
  - Determine whether this bucket contains critical or regulated data (logs, backups, audit evidence, etc.) that would be impacted by versioning suspension.

- **Correlate with Related Activity**  
  - Search for additional CloudTrail events performed by the same actor or IP address within the same timeframe, such as:  
    - `DeleteObject`, `DeleteObjects`, or `PutBucketLifecycle` events (potential data destruction).  
    - `PutBucketPolicy` or `PutBucketAcl` changes (permission manipulation).  
  - Review other detections related to S3 buckets or IAM changes to determine if this event is part of a larger sequence of destructive or unauthorized actions.

- **Validate Intent**  
  - Confirm whether this configuration change aligns with approved maintenance or automation activity (e.g., cost optimization, test environment reset).  
  - If no corresponding change request or justification exists, treat this as a potential defense evasion or impact event.

### False positive analysis

- **Legitimate Administrative Actions**  
  - Administrators or infrastructure automation tools may suspend versioning during migrations or lifecycle testing. Confirm through change management documentation.  
- **Automation and Pipelines**  
  - Verify whether Infrastructure-as-Code tools (e.g., Terraform, CloudFormation) or backup lifecycle scripts routinely modify versioning states.  
  - Exclude predictable automation identities where justified, while ensuring strong audit controls remain in place.

### Response and remediation

**Containment and Validation**  
- Re-enable versioning immediately for the affected bucket using the AWS Console or CLI (`aws s3api put-bucket-versioning --bucket my-bucket --versioning-configuration Status=Enabled`).  
- Verify the change with `get-bucket-versioning` to confirm the bucket is restored to “Enabled.”  
- Identify IAM users or roles with `s3:PutBucketVersioning` permissions and restrict access to trusted administrators only.  
- Preserve relevant CloudTrail, Config, and CloudWatch logs for the timeframe of the change to ensure integrity of investigation evidence.

**Investigation and Scoping**  
- Search CloudTrail for related actions by the same user or IP, including `DeleteObject`, `PutBucketLifecycle`, or `PutBucketPolicy`, to determine whether versioning suspension preceded object deletion or policy manipulation.  
- Review S3 access logs or Data Events for deleted, overwritten, or newly uploaded files after versioning suspension.  
- Validate if the change corresponds to an authorized change request or approved pipeline deployment.

**Recovery and Hardening**  
- If object loss or overwrites occurred, attempt recovery using cross-region replication, AWS Backup, or previous snapshot copies.  
- Enable S3 Object Lock and MFA Delete on critical buckets to prevent future tampering.  
- Configure the AWS Config rule `s3-bucket-versioning-enabled` to continuously monitor for versioning suspension and trigger automated alerts.  
- Review IAM and service control policies to ensure the principle of least privilege is enforced for all S3 management actions.  
- Document findings and update incident response procedures to include versioning protection as part of ransomware and data destruction prevention strategies.


### Additional information
- AWS Documentation: [Using Versioning in S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)  
- API Reference: [PutBucketVersioning](https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketVersioning.html)  
- [AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)
- [AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)

