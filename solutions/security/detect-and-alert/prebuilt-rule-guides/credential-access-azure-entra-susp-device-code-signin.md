---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID OAuth Device Code Flow with Concurrent Sign-ins" prebuilt detection rule.
---

# Entra ID OAuth Device Code Flow with Concurrent Sign-ins

## Triage and analysis

### Investigating Entra ID OAuth Device Code Flow with Concurrent Sign-ins

### Possible investigation steps

- Review the sign-in logs to assess the context and reputation of the source.ip address.
- Investigate the user account associated with the successful sign-in to determine if the activity aligns with expected behavior or if it appears suspicious.
- Check for any recent changes or anomalies in the user's account settings or permissions that could indicate compromise.
- Review the history of sign-ins for the user to identify any patterns or unusual access times that could suggest unauthorized access.
- Assess the device from which the sign-in was attempted to ensure it is a recognized and authorized device for the user.

### Response and remediation

- Immediately revoke the compromised Primary Refresh Tokens (PRTs) to prevent further unauthorized access. This can be done through the Azure portal by navigating to the user's account and invalidating all active sessions.
- Enforce a password reset for the affected user accounts to ensure that any credentials potentially compromised during the attack are no longer valid.
- Implement additional Conditional Access policies that require device compliance checks and restrict access to trusted locations or devices only, to mitigate the risk of future PRT abuse.
- Conduct a thorough review of the affected accounts' recent activity logs to identify any unauthorized actions or data access that may have occurred during the compromise.
- Escalate the incident to the security operations team for further investigation and to determine if there are any broader implications or additional compromised accounts.
- Enhance monitoring by configuring alerts for unusual sign-in patterns or device code authentication attempts from unexpected locations or devices, to improve early detection of similar threats.
- Coordinate with the incident response team to perform a post-incident analysis and update the incident response plan with lessons learned from this event.
