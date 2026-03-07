---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Entra ID Protection - Risk Detection - Sign-in Risk" prebuilt detection rule.'
---

# Entra ID Protection - Risk Detection - Sign-in Risk

## Triage and analysis

This rule detects sign-in risk detection events via Microsoft Entra ID Protection. It identifies various risk event types such as anonymized IP addresses, unlikely travel, password spray, and more. These events can indicate potential malicious activity or compromised accounts.

### Possible investigation steps

- Review the `azure.identityprotection.properties.risk_event_type` field to understand the specific risk event type detected.
- Check the `azure.identityprotection.properties.risk_level` field to determine the severity of the risk event.
- Check the `azure.identityprotection.properties.risk_detail` field for additional context on the risk event.
- Review the `azure.correlation_id` field to correlate this event with other related events in your environment.
- Review the `azure.identityprotection.properties.additional_info` field for any additional information provided by Entra ID Protection.
- Review the `azure.identityprotection.properties.detection_timing_type` field to understand when the risk event was detected. Offline detections may indicate a delayed response to a potential threat while real-time detections indicate immediate risk assessment.
- Check the `azure.identityprotection.properties.user_principal_name` field to identify the user account associated with the risk event. This can help determine if the account is compromised or if the risk event is expected behavior for that user. Triage the user account with other events from Entra ID audit or sign-in logs to identify any suspicious activity or patterns.

### False positive analysis

- Users accessing their accounts from anonymized IP addresses, such as VPNs or Tor, may trigger this rule. If this is expected behavior in your environment, consider adjusting the rule or adding exceptions for specific users or IP ranges.
- Users who frequently travel or access their accounts from different geographic locations may trigger this rule due to the unlikely travel detection mechanism. If this is expected behavior, consider adjusting the rule or adding exceptions for specific users.
- Users who have recently changed their passwords may trigger this rule due to the password spray detection mechanism. If this is expected behavior, consider adjusting the rule or adding exceptions for specific users.

### Response and remediation
- Investigate the user account associated with the risk event to determine if it has been compromised or if the risk event is expected behavior.
- If the risk event indicates a compromised account, take appropriate actions such as resetting the password, enabling multi-factor authentication, or disabling the account temporarily.
- Review authentication material such as primary refresh tokens (PRTs) or OAuth tokens to ensure they have not been compromised. If necessary, revoke these tokens to prevent further access.
- Implement sign-in risk policies in Entra ID Protection to automatically respond to risk events, such as requiring multi-factor authentication or blocking sign-ins from risky locations.
- Ensure multi-factor authentication is enabled for all user accounts to provide an additional layer of security against compromised accounts.
- Consider using high risk detections and conditional access evaluations to enforce stricter security measures for accounts or enable access revocation.
