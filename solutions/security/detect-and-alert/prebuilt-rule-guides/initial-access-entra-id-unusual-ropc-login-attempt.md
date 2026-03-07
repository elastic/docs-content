---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID OAuth ROPC Grant Login Detected" prebuilt detection rule.
---

# Entra ID OAuth ROPC Grant Login Detected

## Triage and analysis

### Investigating Entra ID OAuth ROPC Grant Login Detected

This rule detects unusual login attempts using the Resource Owner Password Credentials (ROPC) flow in Microsoft Entra ID. ROPC allows applications to obtain tokens by directly providing user credentials, bypassing multi-factor authentication (MFA). This method is less secure and can be exploited by adversaries to gain access to user accounts, especially during enumeration or password spraying.

### Possible investigation steps
- Review the `azure.signinlogs.properties.user_principal_name` field to identify the user principal involved in the ROPC login attempt. Check if this user is expected to use ROPC or if it is an unusual account for this type of authentication.
- Analyze the `azure.signinlogs.properties.authentication_protocol` field to confirm that the authentication protocol is indeed ROPC. This protocol is typically used in legacy applications or scripts that do not support modern authentication methods.
- Check the `user_agent.original` field to identify potentially abused open-source tools or scripts that may be using ROPC for unauthorized access such as TeamFiltration or other enumeration tools.
- Review the `azure.signinlogs.properties.app_display_name` or `azure.signinlogs.properties.app_id` to determine which application is attempting the ROPC login. FOCI applications are commonly used for enumeration and password spraying.
- Investigate the `azure.signinlogs.properties.client_ip` to identify the source of the login attempt. Check if the IP address is associated with known malicious activity or if it is a legitimate user location.
- Review the `azure.signinlogs.properties.authentication_details` field for any additional context on the authentication attempt, such as whether it was successful or if there were any errors.
- Examine the `azure.signinlogs.properties.applied_conditional_access_policies` to see if any conditional access policies were applied during the login attempt. If no policies were applied, this could indicate a potential bypass of security controls.
- Identify the resource requested access to by checking the `azure.signinlogs.properties.resource_display_name` or `azure.signinlogs.properties.resource_id`. This can help determine if the login attempt was targeting sensitive resources or applications such as Exchange Online, SharePoint, or Teams.

### False positive analysis
- Legitimate applications or scripts that use ROPC for automation purposes may trigger this rule.
- Some legacy applications may still rely on ROPC for authentication, especially in environments where modern authentication methods are not fully implemented.
- Internal security tools or scripts that perform automated tasks using ROPC may generate false positives if they are not properly whitelisted or excluded from the rule.

### Response and remediation
- If the ROPC login attempt is confirmed to be malicious, immediately block the user account and reset the password to prevent further unauthorized access.
- Consider enforcing multi-factor authentication (MFA) for the user account to enhance security and prevent future unauthorized access attempts.
- Review and update conditional access policies to restrict the use of ROPC for sensitive accounts or applications, ensuring that MFA is required for all login attempts.
- Investigate the source of the ROPC login attempt, including the application and IP address, to determine if there are any additional indicators of compromise or ongoing malicious activity.
- Monitor the user account and related resources for any further suspicious activity or unauthorized access attempts, and take appropriate actions to mitigate any risks identified.
- Educate users about the risks associated with ROPC and encourage them to use more secure authentication methods, such as OAuth 2.0 or OpenID Connect, whenever possible.

