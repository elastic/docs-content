---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "M365 Exchange Mailbox High-Risk Permission Delegated" prebuilt detection rule.
---

# M365 Exchange Mailbox High-Risk Permission Delegated

## Triage and Analysis

### Investigating M365 Exchange Mailbox High-Risk Permission Delegated

This rule detects the delegation of mailbox permissions in Microsoft 365 Exchange. This behavior may indicate that an adversary is attempting to gain access to another user's mailbox or send messages on behalf of that user.

### Possible Investigation Steps
- `user.id` and `o365.audit.Parameters.Identity`: Determine which account was delegated access and which account performed the delegation. Review both for unusual activity.
- `event.action`: Indicates the type of permission granted. Review which delegation action was taken.
- `o365.audit.Parameters.AccessRights` or `GrantSendOnBehalfTo`: Confirm the exact permission granted.
- `@timestamp` and `event.ingested`: Review the timing of the delegation and whether it aligns with user activity or known business events.
- `source.ip` and `source.geo`: Validate that the source IP and location are expected for the admin or account performing the action.
- `user_agent.original`: If present, review to identify any automation, script, or unexpected interface used to assign the permissions.

#### FullAccess (`Add-MailboxPermission`)
- `o365.audit.Parameters.Identity`: The mailbox being accessed.
- `o365.audit.Parameters.User`: The user granted FullAccess.
- Review for subsequent mailbox logins or message rules created by the grantee.

#### SendAs (`Add-RecipientPermission`)
- `o365.audit.Parameters.Identity`: The account the grantee is allowed to impersonate.
- `o365.audit.Parameters.Trustee`: The user who was granted the ability to send as the identity.
- Search for recent messages sent "as" the identity and validate whether the activity was legitimate.

#### SendOnBehalf (`Set-Mailbox`)
- `o365.audit.Parameters.GrantSendOnBehalfTo`: The user allowed to send on behalf of the mailbox owner.
- Check for outbound emails or meeting requests with "on behalf of" headers.

### False Positive Analysis

- Delegation to Assistants: Executive or admin assistants often receive FullAccess or SendOnBehalf permissions.
- Shared Mailboxes: Teams or departments may share access to mailboxes for operational efficiency.
- Automated Admin Actions: System or service accounts may perform these actions as part of onboarding or automation.
- Project-Based Access: Temporary access granted for short-term collaboration.
- Maintain an allowlist of known delegation relationships.

### Response and Remediation

If the delegation is determined to be unauthorized or suspicious:

- Revoke the delegated permissions immediately to prevent further access.
- Reset credentials for the impacted accounts if compromise is suspected.
- Review mailbox rules and sent items to detect abuse.
- Alert impacted users and advise on suspicious activity to watch for.
- Audit audit logs around the delegation for additional attacker actions (e.g., MFA disablement, mailbox rule creation, login from foreign IPs).
- Review conditional access, role-based access control, and app permissions to reduce the attack surface.
- Harden delegation policies by requiring approvals, limiting delegation to specific groups, or implementing Just-in-Time (JIT) access for mailboxes.

