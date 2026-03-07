---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Okta MFA Bombing via Push Notifications" prebuilt detection rule.
---

# Potential Okta MFA Bombing via Push Notifications

## Triage and analysis

### Investigating Potential Okta MFA Bombing via Push Notifications

Multi-Factor Authentication (MFA) is an effective method to prevent unauthorized access. However, some adversaries may abuse the system by repeatedly sending MFA push notifications until the user unwittingly approves the access.

This rule detects when a user denies MFA Okta Verify push notifications twice, followed by a successful authentication event within a 10-minute window. This sequence could indicate an adversary's attempt to bypass the Okta MFA policy.

#### Possible investigation steps:

- Identify the user who received the MFA notifications by reviewing the `user.email` field.
- Identify the time, source IP, and geographical location of the MFA requests and the subsequent successful login.
- Review the `event.action` field to understand the nature of the events. It should include two `user.mfa.okta_verify.deny_push` actions and one `user.authentication.sso` action.
- Ask the user if they remember receiving the MFA notifications and subsequently logging into their account.
- Check if the MFA requests and the successful login occurred during the user's regular activity hours.
- Look for any other suspicious activity on the account around the same time.
- Identify whether the same pattern is repeated for other users in your organization. Multiple users receiving push notifications simultaneously might indicate a larger attack.

### False positive analysis:

- Determine if the MFA push notifications were legitimate. Sometimes, users accidentally trigger MFA requests or deny them unintentionally and later approve them.
- Check if there are known issues with the MFA system causing false denials.

### Response and remediation:

- If unauthorized access is confirmed, initiate your incident response process.
- Alert the user and your IT department immediately.
- If possible, isolate the user's account until the issue is resolved.
- Investigate the source of the unauthorized access.
- If the account was accessed by an unauthorized party, determine the actions they took after logging in.
- Consider enhancing your MFA policy to prevent such incidents in the future.
- Encourage users to report any unexpected MFA notifications immediately.
- Review and update your incident response plans and security policies based on the findings from the incident.

