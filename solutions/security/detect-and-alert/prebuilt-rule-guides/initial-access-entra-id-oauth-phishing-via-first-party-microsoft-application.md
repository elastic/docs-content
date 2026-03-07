---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Entra ID OAuth Phishing via First-Party Microsoft Application" prebuilt detection rule.'
---

# Entra ID OAuth Phishing via First-Party Microsoft Application

## Triage and analysis

### Investigating Entra ID OAuth Phishing via First-Party Microsoft Application

This rule detects OAuth authorization activity where FOCI (Family of Client IDs) applications access Microsoft Graph or legacy Azure AD resources. Adversaries exploit these trusted first-party apps in phishing campaigns like ConsentFix to steal authorization codes and exchange them for tokens from attacker infrastructure. Because first-party apps are pre-consented and cannot be blocked, attackers use them to bypass consent prompts and access user data without triggering typical OAuth alerts.

The rule uses split detection logic: developer tools (Azure CLI, VSCode, PowerShell) accessing either Graph or legacy AAD are flagged, while any FOCI app accessing legacy AAD is flagged since this deprecated API is rarely used legitimately and attackers target it for stealth.

### Possible investigation steps

- Review `azure.signinlogs.properties.user_principal_name` to identify the affected user and determine if they are a high-value target (privileged roles, executives, IT admins).
- Analyze `source.ip` and `source.geo.*` for geographic anomalies. ConsentFix attackers exchange codes from different IPs than the victim's location.
- Check `azure.signinlogs.properties.app_display_name` to confirm which first-party application was used. Azure CLI or PowerShell access by non-developers is suspicious.
- Examine `azure.signinlogs.properties.resource_id` to identify the target resource. Legacy AAD (`00000002-0000-0000-c000-000000000000`) access is unusual for most users.
- Review `azure.signinlogs.properties.is_interactive` - non-interactive sign-ins shortly after interactive ones from different IPs indicate token replay.
- Correlate with other sign-in events using `azure.signinlogs.properties.session_id` to identify the full OAuth flow sequence.
- Pivot to `azure.graphactivitylogs` to search for subsequent Graph API activity from the same session or user from unusual locations.
- Check `azure.auditlogs` for device registration events around the same timeframe, which may indicate persistence attempts.

### False positive analysis

- Developers or IT administrators legitimately using Azure CLI, PowerShell, or VS Code to access Microsoft Graph or Azure AD.
- Enterprise automation or CI/CD pipelines using these tools with user-delegated permissions.
- Users working from multiple locations (VPN, travel) may show different IPs.
- Consider excluding known developer machines, managed devices, or specific user groups that regularly use these tools.
- Maintain an allowlist of expected source IPs tied to corporate infrastructure or developer environments.

### Response and remediation

- Contact the user immediately to confirm if they initiated the OAuth flow and used the detected application.
- If unauthorized, revoke all refresh tokens for the user via Microsoft Entra ID portal or PowerShell.
- Review the user's recent Microsoft Graph activity (email access, file downloads, Teams messages) for signs of data exfiltration.
- Block the source IP if confirmed malicious.
- Check for any devices registered during this session via `azure.auditlogs` and remove unauthorized device registrations.
- Implement Conditional Access policies to restrict OAuth flows for these applications to compliant devices only.
- Educate users about OAuth phishing and the risks of pasting authorization codes into websites.
