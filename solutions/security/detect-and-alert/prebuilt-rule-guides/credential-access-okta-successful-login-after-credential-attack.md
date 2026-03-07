---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Okta Successful Login After Credential Attack" prebuilt detection rule.
---

# Okta Successful Login After Credential Attack

## Triage and analysis

### Investigating Okta Successful Login After Credential Attack

This rule correlates credential attack alerts with subsequent successful authentication for the same user account. The correlation is user-centric, capturing IP rotation scenarios where attackers may login from a different IP after obtaining credentials.

#### Possible investigation steps
- Identify the user account and review the timeline between the attack and successful login.
- Compare the attack source IPs versus the login source IP to identify potential IP rotation.
- Review the original credential attack alert to understand the scope and nature of the attack.
- Check the authentication method used and whether MFA was required and satisfied.
- Review the session activity following the successful login for signs of account takeover.
- Verify with the user if the login was legitimate.

### False positive analysis
- Users experiencing legitimate login issues may trigger attack alerts before successfully authenticating.
- Automated password reset flows where a user fails multiple times then succeeds after resetting may trigger this rule.
- The rule correlates on user identity only, so it fires when a user is targeted and later logs in, even if from different IPs.

### Response and remediation
- If compromise is suspected, reset the user's password and revoke all active sessions.
- Reset MFA if the attacker may have enrolled their own device.
- Block the source IP at the network perimeter.
- Review the user's recent activity for signs of lateral movement or data access.
- Check for persistence mechanisms such as new OAuth apps, API tokens, or enrolled devices.

