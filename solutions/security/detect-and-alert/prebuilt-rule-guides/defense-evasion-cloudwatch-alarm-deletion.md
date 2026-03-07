---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS CloudWatch Alarm Deletion" prebuilt detection rule.
---

# AWS CloudWatch Alarm Deletion

## Triage and analysis

### Investigating AWS CloudWatch Alarm Deletion

Amazon CloudWatch is a monitoring and observability service that collects monitoring and operational data in the form of logs, metrics, and events for resources and applications. This data can be used to detect anomalous behavior in your environments, set alarms, visualize logs and metrics side by side, take automated actions, troubleshoot issues, and discover insights to keep your applications running smoothly.

Amazon CloudWatch Alarms monitor key metrics and trigger automated alerts or remediation workflows. Deleting these alarms disables monitoring of associated metrics and can delay detection of performance degradation or security incidents. Attackers may delete alarms to evade detection, suppress alerts, or disable security automation that responds to anomalies or policy violations.

This rule detects successful calls to the `DeleteAlarms` API via CloudTrail. These events should be rare and always associated with a valid change-control request or automation pipeline.

#### Possible investigation steps

- **Identify the actor**
  - Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.access_key_id` to determine who initiated the deletion.
  - Check whether this actor typically performs CloudWatch management or automation tasks.

- **Review request details**
  - Inspect `aws.cloudtrail.request_parameters` for the specific alarm names deleted. 
  - Determine whether the alarms were security-related (e.g., CloudTrail log delivery, GuardDuty finding rate, or IAM API monitoring alarms).
  - Cross-reference deleted alarms with your organization's list of critical monitoring configurations.

- **Analyze source and context**
  - Review `source.ip` and `user_agent.original` for anomalies such as external IPs, unusual user agents, or custom SDKs.
  - Determine whether the activity occurred during a known maintenance window or from a trusted automation host.
  - Examine `cloud.region` to identify whether alarms were deleted from unexpected regions.

- **Correlate with surrounding events**
  - Review CloudTrail events for related activity around the same time, such as:
    - `PutMetricAlarm`, `DisableAlarmActions`, or `DeleteLogGroup`
    - Changes to CloudTrail, Config, or GuardDuty configurations
    - IAM policy or permission modifications that could facilitate evasion
  - Identify whether the same actor has previously modified logging or monitoring infrastructure.

- **Assess impact and scope**
  - Determine which systems or detection workflows relied on the deleted alarms.
  - Review whether the deletion affected automated responses, notifications, or third-party integrations (e.g., SNS, Lambda, or PagerDuty).

### False positive analysis

- **Legitimate automation or redeployment**
  - Infrastructure as Code (IaC) frameworks such as Terraform or CloudFormation may delete and recreate alarms during updates.
  - Validate automation account roles and ensure alarm deletions are immediately followed by re-creation actions.
- **Operational maintenance**
  - Scheduled monitoring cleanup, regional deactivation, or test environment resets can trigger legitimate deletions. 
  - Verify timing and user identity against approved change management records.
- **Organizational migrations**
  - Security operations or DevOps teams may consolidate alarms during account merges or refactors. 
  - Confirm intent with relevant teams and exclude authorized administrative accounts as necessary.

### Response and remediation

- **Containment**
  - If the deletion was unauthorized, recreate the deleted alarms immediately using IaC templates or CloudFormation backups.
  - Re-enable any dependent automation or alerts that rely on those alarms.
  - Temporarily restrict CloudWatch modification privileges to designated IAM roles.

- **Investigation**
  - Review related CloudTrail logs for preceding IAM changes, STS activity, or anomalous role assumptions that might indicate compromised credentials.
  - Investigate whether any alerts were suppressed or delayed prior to the deletion.

- **Recovery and hardening**
  - Implement AWS Config rules to continuously monitor alarm existence and alert on `DeleteAlarms` API calls.
  - Restrict permissions to `cloudwatch:DeleteAlarms` and enforce MFA for users performing monitoring configuration changes.
  - Maintain IaC definitions for all critical alarms to support rapid restoration.
  - Audit IAM roles and automation accounts that manage CloudWatch configurations to ensure least privilege.
  - Integrate alarm configuration checks into your CI/CD validation workflows.

### Additional information

- **[AWS Config Rule – cloudwatch-alarm-action-check](https://docs.aws.amazon.com/config/latest/developerguide/cloudwatch-alarm-action-check.html)**
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).

