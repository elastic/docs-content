---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS CloudTrail Log Created" prebuilt detection rule.
---

# AWS CloudTrail Log Created

## Triage and analysis

### Investigating AWS CloudTrail Log Created

AWS CloudTrail is a service that enables governance, compliance, and operational and risk auditing of your AWS account. It logs API calls and related events, providing visibility into user activity. Adversaries may create new trails to capture sensitive data or cover their tracks. This detection identifies
`CreateTrail` calls so responders can verify destination ownership, encryption, and scope before accepting the change.

#### Possible investigation steps

- **Identify the actor and context**
  - Review `aws.cloudtrail.user_identity.arn`, `aws.cloudtrail.user_identity.type`, `user_agent.original`, `source.ip`.
  - Confirm a related change request exists (onboarding, architecture change).
- **Validate trail configuration**
  - In `aws.cloudtrail.request_parameters`, verify:
    - `S3BucketName`/`CloudWatchLogsLogGroupArn` belong to your org (no external accounts).
    - `IsMultiRegionTrail=true` and `IncludeGlobalServiceEvents=true` (as per your standard).
    - `KmsKeyId` is an approved CMK; log file validation enabled.
- **Correlate activity**
  - Look for `PutEventSelectors`, `PutInsightSelectors`, `StartLogging` following creation.
  - Check for prior enumeration: `DescribeTrails`, `ListBuckets`, `GetEventSelectors`.

### False positive analysis
- **Planned creation**: Onboarding or compliance initiatives often add trails. Validate via ticket and standard template.
- **Automation**: IaC or control-tower pipelines may create trails on account bootstrap.

### Response and remediation
- **If unauthorized**
  - Disable or delete the trail; verify and secure the destination S3/CloudWatch resources.
  - Review the actor’s recent changes and rotate credentials if compromise is suspected.
- **Hardening**
  - Restrict `cloudtrail:CreateTrail` to admin roles.
  - Use AWS Config / Security Hub controls to enforce multi-region, global events, and validated destinations.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).

