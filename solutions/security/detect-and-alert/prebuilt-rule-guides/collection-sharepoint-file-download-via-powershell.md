---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "M365 SharePoint/OneDrive File Access via PowerShell" prebuilt detection rule.
---

# M365 SharePoint/OneDrive File Access via PowerShell

## Triage and Analysis

### Investigating M365 SharePoint/OneDrive File Access via PowerShell

This rule detects file downloads and access from OneDrive or SharePoint using PowerShell-based user agents. Threat actors commonly use device code phishing to obtain OAuth tokens, then use native PowerShell or PnP PowerShell modules to enumerate and exfiltrate files from SharePoint and OneDrive. FileAccessed events are included because adversaries may read file content via the Graph API `/content` endpoint and save locally, bypassing traditional download events.

#### Possible Investigation Steps

- Identify the user whose token was used and determine if they typically use PowerShell for file operations.
- Review the OAuth application/client ID used to authenticate. Look for public client IDs that may indicate device code phishing.
- Check the source IP address and compare with the user's typical access locations.
- Identify which SharePoint site or OneDrive was accessed.
- Correlate with Azure AD sign-in logs to determine if device code authentication was used.
- Look for rapid sequential file downloads from the same session, which may indicate bulk data exfiltration.
- Check for search activity from the same user/session that may indicate reconnaissance before download.

### False Positive Analysis

- IT administrators legitimately using PnP PowerShell for site management, migration, or backup operations.
- Automated scripts using PowerShell for legitimate data processing or synchronization tasks.
- Consider creating exceptions for known automation service accounts.

### Response and Remediation

- If unauthorized activity is confirmed, immediately revoke the OAuth token and terminate active sessions for the affected user.
- Reset the user's credentials and require reauthentication with MFA.
- Review all files accessed during the session to assess data exposure.
- Implement conditional access policies to restrict device code authentication flow.
- Consider blocking public client IDs that are not needed for business operations.
- Review and audit OAuth application permissions in your tenant.

