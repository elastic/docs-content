---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "M365 Exchange Inbox Phishing Evasion Rule Created" prebuilt detection rule.'
---

# M365 Exchange Inbox Phishing Evasion Rule Created

## Triage and Analysis

### Investigating M365 Exchange Inbox Phishing Evasion Rule Created

This detection identifies the creation of potentially malicious inbox rules in Microsoft 365. These rules automatically delete or move emails with specific keywords such as "invoice", "payment", "security", or "phish". Adversaries often use these rules post-compromise to conceal warning emails, alerts from security tools, or responses from help desk teams, thereby evading detection and maintaining access.

This is a new terms rule that alerts only when the combination of `user.id` and `source.ip` has not performed this activity in the last 14 days.

### Possible investigation steps

- Review the `user.id` and `user.email` fields to identify the user account that created the inbox rule.
- Confirm the rule creation action in `event.action` is `New-InboxRule` and that the `event.outcome` is `success`.
- Investigate the `o365.audit.Parameters.SubjectContainsWords` field for sensitive or suspicious keywords such as:
  - `invoice`, `payment`, `reset`, `phish`, `login`, `fraud`, `alert`, etc.
- Check if the rule performs any of the following:
  - `MoveToFolder`: suspicious folders like `RSS Feeds`, `Junk Email`, or `Deleted Items`.
  - `DeleteMessage`: if present, suggests the rule is meant to hide communications.
- Review the `source.ip` and `source.geo.*` fields to validate whether the IP address and location match expected user behavior.
- Examine whether the rule was created via a suspicious interface like Exchange Admin or through external automation.
- Check for recent sign-in anomalies, credential changes, or unusual mailbox activity for the user (e.g., email forwarding, MFA prompts).

### False positive analysis

- Some rules may be created by users for legitimate purposes (e.g., moving newsletters).
- Outlook plugins or automated email management tools could create rules that resemble this behavior.
- Newly onboarded employees might configure rules for personal filtering without malicious intent.

### Response and remediation

- If the rule is determined to be malicious:
  - Remove the inbox rule immediately.
  - Review the user’s mailbox for signs of data theft or additional manipulation (e.g., auto-forwarding, altered reply-to addresses).
  - Investigate surrounding activity such as MFA changes, token refreshes, or admin role assignments.
  - Revoke tokens and initiate a password reset for the compromised user.
- If broader compromise is suspected:
  - Review audit logs for other inbox rule creations across the tenant.
  - Check whether other users from the same source IP performed similar activity.
  - Educate the user on safe email handling and rule creation best practices.
- Strengthen detection:
  - Enable Microsoft Defender for Office 365 Safe Rules.
  - Use mailbox auditing and DLP policies to monitor hidden inbox activity.
