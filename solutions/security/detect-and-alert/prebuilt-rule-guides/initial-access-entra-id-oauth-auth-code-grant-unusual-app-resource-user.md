---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Entra ID OAuth Authorization Code Grant for Unusual User, App, and Resource" prebuilt detection rule.'
---

# Entra ID OAuth Authorization Code Grant for Unusual User, App, and Resource

## Triage and analysis

### Investigating Entra ID OAuth Authorization Code Grant for Unusual User, App, and Resource

This New Terms rule detects the first occurrence of an OAuth 2.0 authorization code grant flow for a specific combination of client application ID, target resource ID, and user principal within the last 14 days. When a user has never used a particular app+resource combination and it involves FOCI applications or legacy Azure AD, this may indicate OAuth phishing attacks like ConsentFix.

The rule is particularly effective at catching attacks where adversaries use stolen OAuth codes with first-party apps to access resources the victim has never accessed before. For example, if a non-developer suddenly uses Azure CLI to access legacy AAD for the first time, this is highly suspicious regardless of other factors.

### Possible investigation steps

- Review `azure.signinlogs.properties.user_principal_name` to identify the affected user and determine if they are a developer who would legitimately use these tools.
- Check `azure.signinlogs.properties.app_display_name` to confirm which application was used. Azure CLI or PowerShell access by non-technical users is suspicious.
- Examine `azure.signinlogs.properties.resource_id` to identify the target resource. Legacy AAD (`00000002-0000-0000-c000-000000000000`) access is unusual for most users.
- Analyze `source.ip` and `source.geo.*` for geographic anomalies. ConsentFix attackers exchange codes from different IPs than the victim.
- Review `azure.signinlogs.properties.is_interactive` - if this is a non-interactive sign-in shortly after an interactive one from a different IP, it indicates token replay.
- Correlate with other sign-in events using `azure.signinlogs.properties.session_id` to identify the full OAuth flow sequence.
- Pivot to `azure.graphactivitylogs` to search for subsequent Graph API or AAD API activity from unusual locations.
- Check `azure.auditlogs` for device registration events around the same timeframe.

### False positive analysis

- Developers or IT administrators legitimately using Azure CLI, PowerShell, or VS Code for the first time to access specific resources.
- Users onboarding to new development environments or receiving new tooling.
- Automation scripts that run with user-delegated permissions for the first time.
- Consider the user's role and typical activity patterns when evaluating alerts.

### Response and remediation

- Contact the user to confirm if they initiated the OAuth flow and used the detected application.
- If unauthorized, immediately revoke all refresh tokens for the user via Microsoft Entra ID.
- Review recent activity from the same `session_id` for signs of data access or enumeration.
- Block the source IP if confirmed malicious.
- Implement Conditional Access policies to restrict OAuth flows for these applications to compliant devices.
- Educate users about OAuth phishing and the risks of pasting authorization codes.
