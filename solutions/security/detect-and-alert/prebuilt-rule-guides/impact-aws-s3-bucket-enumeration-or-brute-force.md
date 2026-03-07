---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS S3 Bucket Enumeration or Brute Force" prebuilt detection rule.'
---

# AWS S3 Bucket Enumeration or Brute Force

## Triage and analysis

### Investigating AWS S3 Bucket Enumeration or Brute Force

This rule detects when many failed S3 operations (HTTP 403 AccessDenied) hit a single bucket from a single source address in a short window. This can indicate bucket name enumeration, object/key guessing, or brute-force style traffic intended to drive cost or probe for misconfigurations. 403 requests from outside the bucket owner’s account/organization are not billed, but 4XX from inside the owner’s account/org can still incur charges. Prioritize confirming who is making the calls and where they originate.

#### Possible investigation steps

- **Investigate in Timeline.** Investigate the alert in timeline (Take action -> Investigate in timeline) to retrieve and review all of the raw CloudTrail events that contributed to the threshold alert. Threshold alerts only display the grouped fields; Timeline provides a way to see individual event details such as request parameters, full error messages, and additional user context.  

- **Confirm entity & target.** Note the rule’s threshold and window. Identify the target bucket (`tls.client.server_name`) and the source (`source.address`). Verify the caller identity details via any available `aws.cloudtrail.user_identity` fields.  

- **Actor & session context.** In CloudTrail events, pivot 15–30 minutes around the spike for the same `source.address` or principal. Determine if the source is:
  - **External** to your account/organization (recon/cost DDoS risk is lower for you due to 2024 billing change).  
  - **Internal** (same account/org)—higher cost risk and possible misuse of internal automation.  

- **Bucket posture snapshot.** Record S3 Block Public Access, Bucket Policy, ACLs, and whether Versioning/Object Lock are enabled. Capture any recent `PutBucketPolicy`, `PutPublicAccessBlock`, `PutBucketVersioning`, or lifecycle changes.  

- **Blast radius.** Check for similar spikes to other buckets/regions, or parallel spikes from the same source. Review any GuardDuty S3 findings and AWS Config drift related to the bucket or principal.  

- **Business context.** Contact the bucket/app owner. Validate whether a migration, scanner, or broken job could legitimately cause bursts.  

### False positive analysis

- **Expected jobs / broken automation.** Data movers, posture scanners, or failed credentials can generate 403 storms. Validate with `userAgent`, ARNs, change windows, and environment (dev/stage vs prod).  
- **External probing.** Internet-origin enumeration often looks like uniform 403s from transient or cloud-provider IPs and typically has no business impact and no billing if outside your account/org. Tune thresholds or allowlist known scanners if appropriate.  

### Response and remediation

**Immediate, low-risk actions**
- **Preserve evidence.** Export CloudTrail records (±30 minutes) for the bucket and source address into an evidence bucket with restricted access.  
- **Notify owners.** Inform the bucket/application owner and security lead; confirm any maintenance windows.  

**Containment options**
- **External-origin spikes:** Verify Block Public Access is enforced and bucket policies are locked down. Optionally apply a temporary deny-all bucket policy allowing only IR/admin roles while scoping.  
- **Internal-origin spikes:** Identify the principal. Rotate access keys for IAM users, or restrict involved roles (temporary deny/SCP, remove risky policies). Pause broken jobs/pipelines until validated.  

**Scope & hunting**
- Review Timeline and CloudTrail for related events: `PutBucketPolicy`, `PutPublicAccessBlock`, `PutBucketVersioning`, lifecycle changes, unusual `PutObject`/`DeleteObject` volumes, or cross-account access.  
- Check GuardDuty S3 and Config drift findings for signs of tampering or lateral movement.  

**Recovery & hardening**
- If data impact suspected: with Versioning, restore known-good versions; otherwise, recover from backups/replicas.  
- Enable Versioning on critical buckets going forward; evaluate Object Lock legal hold if enabled.  
- Ensure Block Public Access, least-privilege IAM policies, CloudTrail data events for S3, and GuardDuty protections are consistently enforced.  

### Additional information

- [AWS S3 billing for error responses](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ErrorCodeBilling.html): see latest AWS docs on which error codes are billed.  
- [AWS announcement (Aug 2024)](https://aws.amazon.com/about-aws/whats-new/2024/05/amazon-s3-no-charge-http-error-codes/): 403s from outside the account/org are not billed.  
- [AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/): NIST-aligned template for evidence, containment, eradication, recovery, post-incident. 
- [AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/): Practical response steps for account and bucket-level abuse.
