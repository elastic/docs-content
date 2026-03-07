---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID OAuth PRT Issuance to Non-Managed Device Detected" prebuilt detection rule.
---

# Entra ID OAuth PRT Issuance to Non-Managed Device Detected

## Triage and analysis

### Investigating Entra ID OAuth PRT Issuance to Non-Managed Device Detected

This rule identifies a sequence where a Microsoft Entra ID authenticates using a refresh token issued to the Microsoft Authentication Broker (MAB), followed by an authentication using a Primary Refresh Token (PRT) from the same unmanaged device. This behavior is uncommon for normal user activity and strongly suggests adversarial behavior, particularly when paired with OAuth phishing and device registration tools like ROADtx. The use of PRT shortly after a refresh token sign-in typically indicates the attacker has registered a virtual device and is now using the PRT to impersonate a registered user+device pair. The device in question is still marked as unmanaged, indicating it is not compliant with organizational policies and managed by Intune or other MDM solutions.

### Possible investigation steps
- Identify the user principal and device from `azure.signinlogs.properties.user_principal_name` and `azure.signinlogs.properties.device_detail.device_id`.
- Confirm the first sign-in event came from the Microsoft Auth Broker (`app_id`) with `incoming_token_type: refreshToken`.
- Ensure the device has a `trust_type` of "Azure AD joined" and that the `sign_in_session_status` is "unbound".
- Confirm the second sign-in used `incoming_token_type: primaryRefreshToken` and that the `resource_display_name` is not "Device Registration Service".
- Investigate any Microsoft Graph, Outlook, or SharePoint access occurring shortly after.
- Review conditional access policy outcomes and determine whether MFA or device compliance was bypassed.

### False positive analysis
- Legitimate device onboarding and sign-ins using hybrid-joined endpoints may trigger this rule.
- Rapid device provisioning in enterprise environments using MAB could generate similar token behavior.
- Use supporting signals, such as IP address changes, geolocation, or user agent anomalies, to reduce noise.

### Response and remediation
- Investigate other sign-in patterns and assess whether token abuse has occurred.
- Revoke PRT sessions via Microsoft Entra ID or Conditional Access.
- Remove or quarantine the suspicious device registration.
- Require password reset and enforce MFA.
- Audit and tighten device trust and conditional access configurations.

