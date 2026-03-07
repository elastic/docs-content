---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Entra ID User Sign-in with Unusual Non-Managed Device" prebuilt detection rule.'
---

# Entra ID User Sign-in with Unusual Non-Managed Device

## Triage and analysis

### Investigating Entra ID User Sign-in with Unusual Non-Managed Device

This rule detects when a Microsoft Entra ID user signs in from a device that is not typically used by the user, which may indicate potential compromise or unauthorized access attempts. This rule detects unusual sign-in activity by comparing the device used for the sign-in against the user's typical device usage patterns. Adversaries may create and register a new device to obtain a Primary Refresh Token (PRT) and maintain persistent access.

### Possible investigation steps
- Review the `azure.signinlogs.properties.user_principal_name` field to identify the user associated with the sign-in.
- Check the `azure.signinlogs.properties.device_detail.device_id` field to identify the device used for the sign-in.
- Review `azure.signinlogs.properties.incoming_token_type` to determine what tpe of security token was used for the sign-in, such as a Primary Refresh Token (PRT).
- Examine `azure.signinlogs.category` to determine if these were non-interactive or interactive sign-ins.
- Check the geolocation of the sign-in by reviewing `source.geo.country_name` and `source.geo.city_name` to identify the location of the device used for the sign-in. If these are unusual for the user, it may indicate a potential compromise.
- Review `azure.signinlogs.properties.app_id` to determine which client application was used for the sign-in. If the application is not recognized or expected, it may indicate unauthorized access. Adversaries use first-party client IDs to blend in with legitimate traffic.
- Examine `azure.signinlogs.properties.resource_id` to determine what resource the security token has in scope and/or is requesting access to. If the resource is not recognized or expected, it may indicate unauthorized access. Excessive access to Graph API is common post-compromise behavior.
- Review the identity protection risk status by checking `azure.signinlogs.properties.risk_level` and `azure.signinlogs.properties.risk_detail` to determine if the sign-in was flagged as risky by Entra ID Protection.

### False positive analysis
- Legitimate users may sign in from new devices, such as when using a new laptop or mobile device. If this is expected behavior, consider adjusting the rule or adding exceptions for specific users or device IDs.
- Environments where users frequently change devices, such as in a corporate setting with rotating hardware, may generate false positives.
- Users may use both an endpoint and mobile device for sign-ins, which could trigger this rule.

### Response and remediation
- If the sign-in is confirmed to be suspicious or unauthorized, take immediate action to revoke the access token and prevent further access.
- Disable the user account temporarily to prevent any potential compromise or unauthorized access.
- Review the user's recent sign-in activity and access patterns to identify any potential compromise or unauthorized access.
- If the user account is compromised, initiate a password reset and enforce multi-factor authentication (MFA) for the user.
- Review the conditional access policies in place to ensure they are sufficient to prevent unauthorized access to sensitive resources.
- Identify the registered Entra ID device by reviewing `azure.signinlogs.properties.device_detail.display_name` and confirm it is expected for the user or organization. If it is not expected, consider removing the device registration.
- Consider adding exceptions for verified devices that are known to be used by the user to reduce false-positives.
