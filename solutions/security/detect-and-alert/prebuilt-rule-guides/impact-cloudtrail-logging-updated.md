---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS CloudTrail Log Updated" prebuilt detection rule.
---

# AWS CloudTrail Log Updated

## Triage and analysis

### Investigating AWS CloudTrail Log Updated

AWS CloudTrail is a service that enables governance, compliance, and operational and risk auditing of your AWS account. It logs API calls and related events, providing visibility into user activity. Trail modifications can be used by attackers to redirect logs to non-approved buckets, drop regions, or disable valuable selectors. This rule identifies a modification on CloudTrail settings using the `UpdateTrail` API. 

#### Possible investigation steps
- **Actor and context**
  - Check `aws.cloudtrail.user_identity.arn`, `user_agent.original`, `source.ip`; verify approved change.
- **Assess the modification**
  - In `aws.cloudtrail.request_parameters`, note changes to:
    - `S3BucketName`, `CloudWatchLogsLogGroupArn`, `KmsKeyId`
    - `IsMultiRegionTrail`, `IncludeGlobalServiceEvents`
    - Event or insight selectors (management vs data events)
- **Correlate**
  - Look for preceding `StopLogging` or following `DeleteTrail`.
  - Review concurrent IAM policy edits or role changes by the same actor.

### False positive analysis
- **Planned changes**: Baseline drift during region onboarding or encryption rotation.
- **Automation**: IaC pipelines updating trails as templates evolve.

### Response and remediation
- **If unauthorized**
  - Revert to baseline; validate destination ownership and KMS policy.
  - Investigate time ranges where visibility may have been reduced.
- **Hardening**
  - Constrain `cloudtrail:UpdateTrail`, require approvals, and monitor with AWS Config rules.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).

