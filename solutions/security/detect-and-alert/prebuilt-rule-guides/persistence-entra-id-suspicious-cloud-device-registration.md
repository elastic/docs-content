---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Entra ID Unusual Cloud Device Registration" prebuilt detection rule.'
---

# Entra ID Unusual Cloud Device Registration

## Triage and analysis

### Investigating Entra ID Unusual Cloud Device Registration

This rule detects a sequence of Microsoft Entra ID audit events consistent with cloud device registration abuse via ROADtools or similar automation frameworks. The activity includes three correlated events:

1. Add device operation from the Device Registration Service using suspicious user-agents (`Dsreg/*`, `DeviceRegistrationClient`, or `Microsoft.OData.Client/*`).
2. Addition of a registered user with an `enterprise registration` URN.
3. Assignment of a registered owner to the device.

This pattern has been observed in OAuth phishing and PRT abuse campaigns where adversaries silently register a cloud device to obtain persistent, trusted access.

### Possible investigation steps

- Identify the user principal associated with the device registration.
- Review the `azure.auditlogs.identity` field to confirm the Device Registration Service initiated the request.
- Check the user-agent in `azure.auditlogs.properties.additional_details.value`. Known attack tooling signatures include:
  - `Dsreg/10.0 (Windows X.X.X)` - ROADtools Windows device registration
  - `DeviceRegistrationClient` - ROADtools MacOS/Android device registration
  - `Microsoft.OData.Client/*` - .NET-based tools or Graph SDK
- Examine the OS version in the modified properties to identify potentially suspicious or outdated versions.
- Verify the URN in the new value field (`urn:ms-drs:enterpriseregistration.windows.net`) is not being misused.
- Use `azure.correlation_id` to pivot across all three steps of the registration flow.
- Pivot to `azure.signinlogs` to detect follow-on activity using the new device, such as sign-ins involving refresh or primary refresh tokens.
- Look for signs of persistence or lateral movement enabled by the newly registered device.
- Identify the registered device name by reviewing `azure.auditlogs.properties.target_resources.0.display_name` and confirm it's expected for the user or organization.
- Use the correlation ID `azure.correlation_id` to pivot into registered user events from Entra ID audit logs and check `azure.auditlogs.properties.target_resources.0.user_principal_name` to identify the user associated with the device registration.
- Review any activity for this user from Entra ID sign-in logs, where the incoming token type is a `primaryRefreshToken`.

### False positive analysis

- Some MDM, autopilot provisioning flows, or third-party device management tools may generate similar sequences. Validate against known provisioning tools, expected rollout windows, and device inventory.
- Investigate whether the device name, OS version, and registration details align with normal IT workflows.
- Check if the user-agent corresponds to legitimate automation or tooling used by your organization.

### Response and remediation

- If confirmed malicious, remove the registered device from Entra ID.
- Revoke refresh tokens and primary refresh tokens associated with the user and device.
- Disable the user account and initiate password reset and identity verification procedures.
- Review audit logs and sign-in activity for additional indicators of persistence or access from the rogue device.
- Tighten conditional access policies to restrict device registration and enforce compliance or hybrid join requirements.
