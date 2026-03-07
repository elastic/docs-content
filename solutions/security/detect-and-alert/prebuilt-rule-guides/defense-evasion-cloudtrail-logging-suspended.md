---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS CloudTrail Log Suspended" prebuilt detection rule.
---

# AWS CloudTrail Log Suspended

## Triage and analysis

### Investigating AWS CloudTrail Log Suspended

AWS CloudTrail is a service that enables governance, compliance, and operational and risk auditing of your AWS account. It logs API calls and related events, providing visibility into user activity. This rule identifies the suspension of an AWS log trail using the `StopLogging` API. Attackers can do this to cover their tracks and impact security monitoring that relies on this source.

#### Possible investigation steps
- **Actor & scope**
  - Identify `aws.cloudtrail.user_identity.arn`, `user_agent.original`, `source.ip`.
  - Determine which trail stopped and whether it’s multi-region or organization-wide.
- **Timing and impact**
  - When did logging stop and resume (if at all)? Are there overlapping detections indicating activity during the gap?
- **Correlate activity**
  - Search for sensitive API activity around the stop event (IAM changes, S3 policy changes, EC2 exports, KMS changes).
  - Check for preceding `UpdateTrail` (e.g., destination change) and subsequent `DeleteTrail`.

### False positive analysis
- **Planned suspensions**: Rare; verify maintenance tickets and ensure post-change validation.

### Response and remediation
- Restart logging (`StartLogging`) immediately.
- Investigate actor’s recent activity; rotate credentials if suspicious.
- Validate trail configuration, destination bucket/CMK, and event selectors.
- Hardening: Limit `cloudtrail:StopLogging` to break-glass roles; alert on any future stops; enforce via AWS Config/SCPs.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).

