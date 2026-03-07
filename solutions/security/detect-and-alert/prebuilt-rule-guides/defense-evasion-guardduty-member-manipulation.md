---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS GuardDuty Member Account Manipulation" prebuilt detection rule.
---

# AWS GuardDuty Member Account Manipulation

## Triage and analysis

### Investigating AWS GuardDuty Member Account Manipulation

In AWS Organizations with GuardDuty enabled, a delegated administrator account receives and aggregates security findings from all member accounts. This centralized visibility is critical for detecting threats across the organization. Adversaries who compromise a member account may attempt to break this relationship to operate without triggering alerts visible to the security team.

This rule detects several API actions that manipulate GuardDuty member relationships:
- `DisassociateFromMasterAccount` / `DisassociateFromAdministratorAccount`: Member account breaks its connection to the administrator
- `DeleteMembers`: Administrator removes member accounts from GuardDuty
- `StopMonitoringMembers`: Administrator stops monitoring specific member accounts without fully removing them
- `DeleteInvitations`: Member account deletes pending invitations, preventing association

These actions are extremely rare in normal operations and can indicate either a compromised account or an attacker preparing to disable GuardDuty entirely.

### Possible investigation steps

- **Identify the actor**
  - Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.type` to determine who performed the action.
  - Determine whether the action originated from a member account (disassociation) or the administrator account (deletion/stop monitoring).

- **Review request context**
  - Check `aws.cloudtrail.request_parameters` to identify which member accounts were affected.
  - Determine the scope: single account or multiple accounts targeted.

- **Analyze source and access patterns**
  - Review `source.ip` and `user_agent.original` for anomalous access patterns.
  - Check if the action occurred outside normal business hours or maintenance windows.

- **Correlate with related activity**
  - Search for subsequent `DeleteDetector` API calls in the affected member accounts.
  - Look for other defense evasion indicators: CloudTrail modifications, Config rule deletions, Security Hub changes.
  - Check for privilege escalation or credential access events preceding this action.

- **Verify business justification**
  - Confirm with the identified user or team whether there was a legitimate organizational change.
  - Check for related change tickets or migration documentation.

### False positive analysis

- **Organizational restructuring**
  - Member relationships may change during account migrations or delegated administrator transitions.
  - Validate against documented organizational changes.

- **Account decommissioning**
  - Accounts being retired may be removed from GuardDuty before closure.
  - Confirm this aligns with account lifecycle management processes.

### Response and remediation

- **Immediate containment**
  - If unauthorized, immediately re-associate the affected member accounts with the administrator.
  - For `StopMonitoringMembers`, use `StartMonitoringMembers` to restore visibility.

- **Investigation**
  - Audit the affected member accounts for suspicious activity during the visibility gap.
  - Review CloudTrail for any actions taken while GuardDuty monitoring was disrupted.

- **Hardening**
  - Restrict `guardduty:DisassociateFromAdministratorAccount`, `guardduty:DeleteMembers`, and related permissions.
  - Use SCPs to prevent member accounts from disassociating from GuardDuty administrators.
  - Implement Security Hub controls to detect changes to GuardDuty organization configuration.

### Additional information
- **[AWS GuardDuty Multi-Account Documentation](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_accounts.html)**
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)**
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)**

