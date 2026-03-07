---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS CloudTrail Log Deleted" prebuilt detection rule.
---

# AWS CloudTrail Log Deleted

## Triage and analysis

### Investigating AWS CloudTrail Log Deleted

AWS CloudTrail is a service that enables governance, compliance, and operational and risk auditing of your AWS account. It logs API calls and related events, providing visibility into user activity. This rule identifies the deletion of an AWS log trail using the `DeleteTrail` API. Deleting a trail can eliminate visibility and is a strong indicator of defense evasion or sabotage.

#### Possible investigation steps
- **Actor & target**
  - Identify `aws.cloudtrail.user_identity.arn`, `user_agent.original`, `source.ip`.
  - Confirm which trail was deleted (name/ARN, multi-region/organization status) from `aws.cloudtrail.request_parameters`.
- **Blast radius**
  - Determine whether it was the only trail or if organization/multi-region coverage remains.
  - Review preceding `StopLogging` or `UpdateTrail` and subsequent high-risk actions (IAM, S3, KMS, EC2 exports).
- **Data preservation**
  - Verify S3 destinations and CloudWatch log groups for retained historical logs and file integrity validation.

### False positive analysis
- **Planned deletion**: Validate with tickets and decommissioning plans; ensure replacement/alternate trails exist.

### Response and remediation
- Recreate or re-enable compliant multi-region (or organization) trails immediately.
- Investigate the actor’s recent activity; rotate creds if compromise is suspected.
- Validate destination bucket policies, CMK policies, and event selectors for all active trails.
- Hardening: Restrict `cloudtrail:DeleteTrail` and enforce guardrails via AWS Config/SCPs; alert on future deletions.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).

