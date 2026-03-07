---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "M365 Exchange MFA Notification Email Deleted or Moved" prebuilt detection rule.
---

# M365 Exchange MFA Notification Email Deleted or Moved

## Triage and Analysis

### Investigating M365 Exchange MFA Notification Email Deleted or Moved

This rule detects when emails containing MFA enrollment or security notification keywords are deleted or moved to deleted items. Attackers who gain access to an account and register their own MFA device will often immediately delete the notification email to prevent the legitimate user from detecting the compromise.

#### Possible Investigation Steps

- Identify the user whose mailbox had the email deleted and determine if they recently enrolled a new MFA device.
- Review Azure AD sign-in logs for the user around the time of the deletion for authentication anomalies.
- Check Azure AD audit logs for recent MFA method registrations or changes for this user.
- Review the source IP address and determine if it matches the user's typical access patterns.
- Look for other suspicious mailbox activities from the same session (inbox rules, email forwarding).
- Determine if the user was aware of and initiated the MFA enrollment that generated the notification.

### False Positive Analysis

- Users may legitimately delete MFA notification emails after reviewing and confirming the enrollment.
- Some organizations have mailbox rules that automatically organize or delete notification emails.
- Consider creating exceptions for users who frequently manage MFA enrollments (IT help desk).

### Response and Remediation

- If unauthorized MFA enrollment is confirmed, immediately remove the attacker's MFA method from the account.
- Revoke all active sessions and refresh tokens for the affected user.
- Reset the user's credentials and require reauthentication.
- Review inbox rules for any malicious forwarding or deletion rules.
- Check for data exfiltration or other malicious activities during the compromise window.
- Implement conditional access policies to restrict MFA registration to trusted locations/devices.

