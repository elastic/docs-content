---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS SQS Queue Purge" prebuilt detection rule.'
---

# AWS SQS Queue Purge

## Triage and analysis

### Investigating AWS SQS Queue Purge

AWS SQS is a managed message queuing service commonly used to decouple services and buffer events across distributed and serverless architectures. Purging a queue removes all pending messages and cannot be undone. While this may be required for maintenance or testing, adversaries may abuse this action to disrupt operations, delete forensic evidence, or evade detection by removing queued security or audit events.

### Possible investigation steps

**Identify the actor**
- Review `aws.cloudtrail.user_identity.arn` and `access_key_id` to determine who initiated the purge. Confirm whether this identity typically manages SQS resources and whether the action aligns with their role.

**Review the affected queue**
- Identify the purged queue using `aws.cloudtrail.request_parameters` or `aws.cloudtrail.resources.arn`. Determine the purpose of the queue and whether it supports critical workflows, security tooling, or monitoring pipelines.

**Evaluate the context of the action**
- Review the `@timestamp` to determine when the purge occurred and whether it aligns with maintenance windows or
  deployment activity.
- Examine `source.ip` and `user_agent.original` for anomalies such as unexpected locations, automation tools, or
  unfamiliar clients.

**Correlate related activity**
- Search for other CloudTrail events from the same identity before and after the purge, including IAM changes, credential activity, or additional SQS operations.
- Look for signs of follow-on behavior such as queue deletion, policy updates, or attempts to suppress logging.

**Validate intent**
- Confirm with the queue owner or application team whether the purge was intentional, approved, and expected. If no clear business justification exists, treat the activity as potentially suspicious.

### False positive analysis

- Queue purges performed during routine maintenance, incident recovery, or test resets may be legitimate.
- Automated jobs or cleanup scripts may regularly purge queues as part of normal operation.

### Response and remediation

- If the purge was unauthorized, immediately restrict SQS permissions for the affected identity and investigate for credential compromise.
- Assess operational impact and determine whether downstream systems were disrupted or lost critical data.
- Review recent activity to identify any additional attempts to evade detection or disable monitoring.
- Reinforce least-privilege IAM policies to limit which identities can perform `PurgeQueue`.
- Enhance monitoring and alerting for destructive SQS actions, especially in production environments.
- Work with application teams to document approved purge workflows and ensure adequate guardrails are in place.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **[AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/)**
