---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS GuardDuty Detector Deletion" prebuilt detection rule.
---

# AWS GuardDuty Detector Deletion

## Triage and analysis

### Investigating AWS GuardDuty Detector Deletion

Amazon GuardDuty is a continuous threat detection service that analyzes CloudTrail, DNS, and VPC Flow Logs to identify malicious activity and compromised resources. Deleting a GuardDuty detector stops this monitoring entirely and permanently removes all historical findings for the affected AWS account. This rule detects successful `DeleteDetector` API calls, which may represent an attacker attempting to impair defenses and evade detection. Such actions should be rare and always performed under controlled administrative change processes.

#### Possible investigation steps

- **Identify the actor**
  - Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.type` to determine who initiated the deletion.
  - Verify whether this principal normally performs GuardDuty configuration or administrative tasks.

- **Review request context**
  - Check `aws.cloudtrail.request_parameters` and `cloud.region` to confirm the targeted GuardDuty detector and scope of impact.
  - Determine whether multiple detectors or member accounts were affected (especially in delegated admin organizations).

- **Analyze source and access patterns**
  - Review `source.ip`, `user_agent.original` and `source.geo` fields for anomalous or previously unseen access locations or automation clients.
  - Check whether the deletion occurred outside standard maintenance windows or during a concurrent suspicious activity window.

- **Correlate with preceding or related activity**
  - Search for earlier GuardDuty configuration changes:
    - `StopMonitoringMembers`, `DisassociateMembers`, or `DeleteMembers`
    - IAM role or policy modifications reducing GuardDuty privileges
  - Look for other defense evasion indicators such as CloudTrail suspension, Security Hub configuration changes, or disabling of AWS Config rules.

- **Review historical GuardDuty findings**
  - Examine prior GuardDuty alerts and findings (if still retrievable) to determine whether the deletion followed significant detection activity.
  - Use centralized logs or security data lakes to recover findings removed from the console.

### False positive analysis

- **Authorized administrative actions**
  - Verify whether the deletion corresponds to legitimate account decommissioning, region cleanup, or migration activity.
- **Automation or IaC**
  - GuardDuty may be disabled temporarily during infrastructure provisioning or teardown in automated environments. 
    Confirm via CI/CD logs or Infrastructure-as-Code templates.
- **Organizational configuration changes**
  - Large organizations might consolidate GuardDuty under a delegated administrator account, causing detectors to be deleted in member accounts. 
    Validate these actions against security architecture changes.

### Response and remediation

- **Containment and restoration**
  - If unauthorized, immediately re-enable GuardDuty in the affected account and region using the `CreateDetector` API or AWS console.
  - Verify that findings aggregation and member account associations are restored to expected configurations.

- **Investigation**
  - Review CloudTrail for related privilege escalation or resource tampering events around the deletion time.
  - Assess whether any attacker activity occurred during the monitoring gap between deletion and restoration.

- **Recovery and hardening**
  - Restrict `guardduty:DeleteDetector` permissions to a limited administrative role.
  - Implement AWS Config rules or Security Hub controls to alert on changes to GuardDuty detectors or configuration states.
  - Enforce least privilege IAM policies, ensuring operational automation cannot disable GuardDuty outside maintenance workflows.
  - Document approved GuardDuty maintenance activities and correlate them with change tickets for traceability.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).

