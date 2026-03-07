---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "M365 Identity OAuth Flow by User Sign-in to Device Registration" prebuilt detection rule.
---

# M365 Identity OAuth Flow by User Sign-in to Device Registration

## Triage and analysis

### Investigating M365 Identity OAuth Flow by User Sign-in to Device Registration

### Possible investigation steps
- Review the two UserLoggedIn logs to confirm that they come from different source.ip values and are associated to the same account.
- Verify all events associated to the source.ip of the the second event in the sequence.
- Investiguate the details of the new device that was added by reviewing the o365.audit.ModifiedProperties.Device_DisplayName.NewValue attribute.
- Investigate the user account associated with the successful sign-in to determine if this activity aligns with expected behavior or if it appears suspicious.
- Review the history of sign-ins for the user to identify any patterns or unusual access times that could suggest unauthorized access.
- Assess the device from which the sign-in was attempted to ensure it is a recognized and authorized device for the user.

### False positive analysis
- Both authentcation events of the sequence are originatng from the same source.ip.
- User using multiple devices and attempted to add a new device post an OAuth code authentication.

### Response and remediation
- Immediately revoke the compromised Primary Refresh Tokens (PRTs) to prevent further unauthorized access. This can be done through the Azure portal by navigating to the user's account and invalidating all active sessions.
- Enforce a password reset for the affected user accounts to ensure that any credentials potentially compromised during the attack are no longer valid.
- Implement additional Conditional Access policies that require device compliance checks and restrict access to trusted locations or devices only, to mitigate the risk of future PRT abuse.
- Conduct a thorough review of the affected accounts' recent activity logs to identify any unauthorized actions or data access that may have occurred during the compromise.
- Escalate the incident to the security operations team for further investigation and to determine if there are any broader implications or additional compromised accounts.
- Enhance monitoring by configuring alerts for unusual sign-in patterns or device code authentication attempts from unexpected locations or devices, to improve early detection of similar threats.
- Coordinate with the incident response team to perform a post-incident analysis and update the incident response plan with lessons learned from this event.
