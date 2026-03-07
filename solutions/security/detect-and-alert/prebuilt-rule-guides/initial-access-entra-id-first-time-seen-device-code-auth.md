---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Entra ID OAuth Device Code Grant by Unusual User" prebuilt detection rule.'
---

# Entra ID OAuth Device Code Grant by Unusual User

## Triage and analysis

### Investigating Entra ID OAuth Device Code Grant by Unusual User

This rule detects the first instance of a user authenticating via the **DeviceCode** authentication protocol within a **14-day window**. The **DeviceCode** authentication workflow is designed for devices that lack keyboards, such as IoT devices and smart TVs. However, adversaries can abuse this mechanism by phishing users and stealing authentication tokens, leading to unauthorized access.

### Possible Investigation Steps

#### Identify the User and Authentication Details
- **User Principal Name (UPN)**: Review `azure.signinlogs.properties.user_principal_name` to identify the user involved in the authentication event.
- **User ID**: Check `azure.signinlogs.properties.user_id` for a unique identifier of the affected account.
- **Authentication Protocol**: Confirm that `azure.signinlogs.properties.authentication_protocol` is set to `deviceCode`.
- **Application Used**: Verify the application through `azure.signinlogs.properties.app_display_name` and `azure.signinlogs.properties.app_id` to determine if it is an expected application.

#### Review the Source IP and Geolocation
- **Source IP Address**: Check `source.ip` and compare it with previous authentication logs to determine whether the login originated from a trusted or expected location.
- **Geolocation Details**: Analyze `source.geo.city_name`, `source.geo.region_name`, and `source.geo.country_name` to confirm whether the login location is suspicious.
- **ASN / ISP Details**: Review `source.as.organization.name` to check if the IP is associated with a known organization or cloud provider.

#### Examine Multi-Factor Authentication (MFA) and Conditional Access
- **MFA Enforcement**: Review `azure.signinlogs.properties.applied_conditional_access_policies` to determine if MFA was enforced during the authentication.
- **Conditional Access Policies**: Check `azure.signinlogs.properties.conditional_access_status` to understand if conditional access policies were applied and if any controls were bypassed.
- **Authentication Method**: Look at `azure.signinlogs.properties.authentication_details` to confirm how authentication was satisfied (e.g., MFA via claim in token).

#### Validate Device and Client Details
- **Device Information**: Review `azure.signinlogs.properties.device_detail.browser` to determine if the login aligns with the expected behavior of a device that lacks a keyboard.
- **User-Agent Analysis**: Inspect `user_agent.original` for anomalies, such as an unexpected operating system or browser.
- **Client Application**: Verify `azure.signinlogs.properties.client_app_used` to confirm whether the login was performed using a known client.

#### Investigate Related Activities
- **Correlate with Phishing Attempts**: Check if the user recently reported phishing attempts or suspicious emails.
- **Monitor for Anomalous Account Activity**: Look for recent changes in the user's account settings, including password resets, role changes, or delegation of access.
- **Check for Additional DeviceCode Logins**: Review if other users in the environment have triggered similar authentication events within the same timeframe.

## False Positive Analysis

- **Legitimate Device Enrollment**: If the user is setting up a new device (e.g., a smart TV or kiosk), this authentication may be expected.
- **Automation or Scripting**: Some legitimate applications or scripts may leverage the `DeviceCode` authentication protocol for non-interactive logins.
- **Shared Devices in Organizations**: In cases where shared workstations or conference room devices are in use, legitimate users may trigger alerts.
- **Travel and Remote Work**: If the user is traveling or accessing from a new location, confirm legitimacy before taking action.

## Response and Remediation

- **Revoke Suspicious Access Tokens**: Immediately revoke any access tokens associated with this authentication event.
- **Investigate the User’s Recent Activity**: Review additional authentication logs, application access, and recent permission changes for signs of compromise.
- **Reset Credentials and Enforce Stronger Authentication**:
  - Reset the affected user’s credentials.
  - Enforce stricter MFA policies for sensitive accounts.
  - Restrict `DeviceCode` authentication to only required applications.
- **Monitor for Further Anomalies**:
  - Enable additional logging and anomaly detection for DeviceCode logins.
  - Set up alerts for unauthorized access attempts using this authentication method.
- **Educate Users on Phishing Risks**: If phishing is suspected, notify the affected user and provide security awareness training on how to recognize and report phishing attempts.
- **Review and Adjust Conditional Access Policies**:
  - Limit `DeviceCode` authentication to approved users and applications.
  - Implement stricter geolocation-based authentication restrictions.
