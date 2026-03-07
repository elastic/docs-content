---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Entra ID Protection Admin Confirmed Compromise" prebuilt detection rule.'
---

# Entra ID Protection Admin Confirmed Compromise

## Triage and analysis

This rule detects when an administrator has manually confirmed a user or sign-in as compromised in Microsoft Entra ID Protection. This is a critical security event that requires immediate investigation and response.

### Possible investigation steps

- Review the `azure.identityprotection.properties.risk_detail` field to determine if the compromise was confirmed at the sign-in level (`adminConfirmedSigninCompromised`) or user level (`adminConfirmedUserCompromised`).
- Check the `azure.identityprotection.properties.user_principal_name` field to identify the compromised user account.
- Review the `azure.identityprotection.properties.user_display_name` field for additional user identification information.
- Examine the `azure.identityprotection.properties.risk_level` field to understand the severity level assigned to the risk event.
- Check the `azure.identityprotection.properties.risk_state` field to verify the current state of the risk (should be confirmed as compromised).
- Review the `azure.correlation_id` field to correlate this event with other related security events, including the original risk detections that led to the admin confirmation.
- Investigate the timeline of events leading up to the admin confirmation by reviewing Entra ID sign-in logs and audit logs for the affected user.
- Check for any suspicious activities associated with the user account, including:
    - Unusual sign-in locations or IP addresses
    - Access to sensitive resources or applications
    - Changes to user profile, permissions, or MFA settings
    - Bulk email sending or data exfiltration activities
- Review the `azure.identityprotection.properties.additional_info` field for any additional context provided by the administrator or Entra ID Protection.
- Identify which administrator confirmed the compromise by reviewing Entra ID audit logs for risk state changes.

### False positive analysis

- Security testing or penetration testing exercises may result in administrators confirming test accounts as compromised. If this is expected behavior, consider excluding specific test accounts or implementing a testing account naming convention to filter.
- Incident response drills or tabletop exercises may involve marking accounts as compromised for training purposes. Coordinate with security teams to identify planned exercises.

### Response and remediation

- Immediately reset the password for the compromised user account and require the user to set a new password upon next sign-in.
- Revoke all active sessions and authentication tokens for the compromised account, including:
    - Primary refresh tokens (PRTs)
    - OAuth tokens
    - Session cookies
    - Application-specific passwords
- Review and revoke any suspicious OAuth consent grants or application permissions added by the compromised account.
- Enable or enforce multi-factor authentication (MFA) for the affected user account if not already enabled.
- Review all activities performed by the compromised account, including:
    - Email forwarding rules or inbox rules
    - File access and downloads
    - Changes to security settings or permissions
    - Creation of new users or service principals
- Assess the scope of the compromise by identifying any lateral movement or privilege escalation activities.
- Consider disabling the account temporarily until the investigation is complete and all remediation steps are verified.
- Implement conditional access policies to prevent future compromises, such as requiring MFA from untrusted locations or blocking legacy authentication.
- Review and strengthen identity protection policies and risk-based conditional access rules.
- Document the incident, including the timeline, scope of compromise, and remediation actions taken.
- Conduct a post-incident review to identify gaps in security controls and implement improvements to prevent similar incidents.
