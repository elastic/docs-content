---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID User Reported Suspicious Activity" prebuilt detection rule.
---

# Entra ID User Reported Suspicious Activity

## Triage and Analysis

### Investigating Entra ID User Reported Suspicious Activity

This rule detects when a user in Microsoft Entra ID reports suspicious activity associated with their account. This feature is often used to report MFA fatigue or unsolicited push notifications, and is logged during authentication flows involving methods like Microsoft Authenticator. Such events may indicate that an attacker attempted unauthorized access and triggered a push that was denied or flagged by the user.

### Possible investigation steps

- Review the `azure.auditlogs.identity` field to identify the reporting user.
- Confirm that `event.action` is `"Suspicious activity reported"` and the result was `"success"`.
- Check the `azure.auditlogs.properties.additional_details` array for `AuthenticationMethod`, which shows how the login attempt was performed (e.g., `PhoneAppNotification`).
- Look at the `azure.auditlogs.properties.initiated_by.user.userPrincipalName` and `displayName` to confirm which user reported the suspicious activity.
- Investigate recent sign-in activity (`signinlogs`) for the same user. Focus on:
  - IP address geolocation and ASN.
  - Device, operating system, and browser.
  - MFA prompt patterns or unusual login attempts.
- Determine whether the user actually initiated a login attempt, or if it was unexpected and aligns with MFA fatigue or phishing attempts.
- Correlate this report with any risky sign-in detections, conditional access blocks, or password resets in the past 24–48 hours.

### False positive analysis

- Users unfamiliar with MFA push notifications may mistakenly report legitimate sign-in attempts.
- Shared accounts or device switching can also trigger unintended notifications.
- Legitimate travel or network changes might confuse users into thinking activity was malicious.

### Response and remediation

- Contact the user to validate the suspicious activity report and assess whether they were targeted or tricked by a malicious actor.
- If the report is confirmed to be valid:
  - Reset the user’s credentials immediately.
  - Revoke active sessions and refresh tokens.
  - Review their activity across Microsoft 365 services for signs of compromise.
- If other users report similar behavior around the same time, assess for a broader MFA fatigue campaign or targeted phishing.
- Consider tuning conditional access policies to require number matching or stronger MFA mechanisms.
- Educate users on reporting suspicious MFA prompts and following up with IT/security teams promptly.

