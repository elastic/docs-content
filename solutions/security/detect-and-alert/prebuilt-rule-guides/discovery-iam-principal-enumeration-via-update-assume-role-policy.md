---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS IAM Principal Enumeration via UpdateAssumeRolePolicy" prebuilt detection rule.
---

# AWS IAM Principal Enumeration via UpdateAssumeRolePolicy

## Triage and analysis

### Investigating AWS IAM Principal Enumeration via UpdateAssumeRolePolicy

This rule detects bursts of failed attempts to update an IAM role’s trust policy — typically resulting in `MalformedPolicyDocumentException` errors — which can indicate enumeration of IAM principals.  
Adversaries who have obtained valid AWS credentials may attempt to identify roles or accounts that can be assumed by repeatedly modifying a role’s trust relationship using guessed `Principal` ARNs.  
When these principals are invalid, IAM rejects the request, creating a recognizable sequence of failed `UpdateAssumeRolePolicy` events.

Because this is a threshold rule, it triggers when the number of failures exceeds a defined count within a short period. This pattern suggests brute-force-style enumeration rather than normal misconfiguration.

#### Possible investigation steps

- **Validate the context of the threshold trigger**
  - Review the `@timestamp` range for when the burst occurred and the number of failed attempts in the threshold window.
  - Identify whether all failures targeted the same `RoleName` or multiple roles — targeting a single role is often indicative of brute-force enumeration.
  - Confirm the source identity and IP address (`aws.cloudtrail.user_identity.arn`, `source.ip`, `user_agent.original`) to determine whether these calls originated from a known automation process or an unexpected host.

- **Correlate with other IAM activity**
  - Look for any subsequent successful `UpdateAssumeRolePolicy` or `AssumeRole` calls, which may indicate the attacker eventually discovered a valid principal.
  - Search for reconnaissance-related API calls (`ListRoles`, `ListUsers`, `GetCallerIdentity`) before the threshold event — these often precede enumeration bursts.
  - Investigate whether other suspicious role- or identity-related actions occurred near the same timeframe, such as `CreateRole`, `PutRolePolicy`, or `AttachRolePolicy`.

- **Identify infrastructure patterns**
  - Examine the `user_agent.original` field — the presence of automation frameworks or penetration tools (e.g., “Boto3”, “Pacu”) may signal offensive tooling.
  - Review the `source.ip` or `cloud.account.id` fields to see whether this account may be acting as attacker-controlled infrastructure attempting to enumerate roles in other environments.

- **Validate authorization**
  - Confirm with your DevOps or Cloud IAM teams whether any expected testing, migration, or cross-account role configuration changes were planned for this time period.
  - If the identity performing these actions does not typically manage IAM roles or trust relationships, escalate for investigation as a possible credential compromise.

### False positive analysis

- **Legitimate automation retries**
  - Continuous integration or configuration management systems may retry failed IAM API calls during deployment rollouts.  
    If the same IAM role was being updated as part of a known change, validate the timing and source identity before closing as benign.
- **Misconfigured scripts or infrastructure drift**
  - Scripts that deploy trust policies using outdated or invalid ARNs can cause repetitive failures that mimic brute-force patterns.  
    Review the `RoleName` and `Principal` ARNs included in the failed requests to confirm if they correspond to known but outdated configurations.

### Response and remediation

- **Immediate review and containment**
  - Investigate whether the source account is being used for offensive operations or compromised automation.
  - Disable or suspend the IAM user or access key responsible for the enumeration burst.
  - If activity originated from a workload or CI/CD system, audit its access keys and environment variables for compromise.

- **Investigation and scoping**
  - Review CloudTrail logs for other IAM or STS actions from the same source in the preceding and following 24 hours.
  - Check for any successful privilege changes (`PutRolePolicy`, `AttachRolePolicy`, or `AssumeRole`) by the same identity.
  - Determine if other roles in the same account experienced similar failed updates or bursts.

- **Recovery and hardening**
  - Rotate credentials for any identities involved.
  - Limit permissions to modify trust policies (`iam:UpdateAssumeRolePolicy`) to a small set of administrative roles.
  - Enable AWS Config rule `iam-role-trust-policy-check` to detect overly permissive or unusual trust relationships.
  - Use AWS GuardDuty or Security Hub to monitor for subsequent privilege escalation or reconnaissance findings.
  - Review the event against AWS Incident Response Playbook guidance (containment > investigation > recovery > hardening).

### Additional information
  - **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
  - **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
  - **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/)

