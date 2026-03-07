---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Entra ID OAuth Device Code Grant by Microsoft Authentication Broker" prebuilt detection rule.'
---

# Entra ID OAuth Device Code Grant by Microsoft Authentication Broker

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Entra ID OAuth Device Code Grant by Microsoft Authentication Broker

Entra ID Device Code Authentication allows users to authenticate devices using a code, facilitating seamless access to Azure resources. Adversaries exploit this by compromising Primary Refresh Tokens (PRTs) to bypass multi-factor authentication and Conditional Access policies. The detection rule identifies unauthorized access attempts by monitoring successful sign-ins using device code authentication linked to a specific broker client application ID, flagging potential misuse.

### Possible investigation steps

- Review the sign-in logs to confirm the use of device code authentication by checking the field azure.signinlogs.properties.authentication_protocol for the value deviceCode.
- Verify the application ID involved in the sign-in attempt by examining azure.signinlogs.properties.conditional_access_audiences.application_id and ensure it matches 29d9ed98-a469-4536-ade2-f981bc1d605e.
- Investigate the user account associated with the successful sign-in to determine if the activity aligns with expected behavior or if it appears suspicious.
- Check for any recent changes or anomalies in the user's account settings or permissions that could indicate compromise.
- Review the history of sign-ins for the user to identify any patterns or unusual access times that could suggest unauthorized access.
- Assess the device from which the sign-in was attempted to ensure it is a recognized and authorized device for the user.

### False positive analysis

- Legitimate device code authentication by trusted applications or users may trigger the rule. Review the application ID and user context to confirm legitimacy.
- Frequent access by automated scripts or services using device code authentication can be mistaken for unauthorized access. Identify and document these services, then create exceptions for known application IDs.
- Shared devices in environments with multiple users may cause false positives if device code authentication is used regularly. Implement user-specific logging to differentiate between legitimate and suspicious activities.
- Regular maintenance or updates by IT teams using device code authentication might be flagged. Coordinate with IT to schedule these activities and temporarily adjust monitoring rules if necessary.
- Ensure that any exceptions or exclusions are regularly reviewed and updated to reflect changes in the environment or application usage patterns.

### Response and remediation

- Immediately revoke the compromised Primary Refresh Tokens (PRTs) to prevent further unauthorized access. This can be done through the Azure portal by navigating to the user's account and invalidating all active sessions.
- Enforce a password reset for the affected user accounts to ensure that any credentials potentially compromised during the attack are no longer valid.
- Implement additional Conditional Access policies that require device compliance checks and restrict access to trusted locations or devices only, to mitigate the risk of future PRT abuse.
- Conduct a thorough review of the affected accounts' recent activity logs to identify any unauthorized actions or data access that may have occurred during the compromise.
- Escalate the incident to the security operations team for further investigation and to determine if there are any broader implications or additional compromised accounts.
- Enhance monitoring by configuring alerts for unusual sign-in patterns or device code authentication attempts from unexpected locations or devices, to improve early detection of similar threats.
- Coordinate with the incident response team to perform a post-incident analysis and update the incident response plan with lessons learned from this event.
