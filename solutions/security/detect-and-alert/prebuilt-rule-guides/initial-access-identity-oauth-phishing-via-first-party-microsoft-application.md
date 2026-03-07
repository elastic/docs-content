---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "M365 Identity OAuth Phishing via First-Party Microsoft Application" prebuilt detection rule.'
---

# M365 Identity OAuth Phishing via First-Party Microsoft Application

## Triage and analysis

### Investigating M365 Identity OAuth Phishing via First-Party Microsoft Application

This rule detects OAuth authorization activity where FOCI (Family of Client IDs) applications access Microsoft Graph or legacy Azure AD resources. Adversaries exploit these trusted first-party apps in phishing campaigns like ConsentFix to steal authorization codes and exchange them for tokens from attacker infrastructure. The rule specifically looks for `OAuth2:Authorize` requests with `Redirect` status, which indicates the user was redirected after authorization and the OAuth code was exposed.

The rule uses split detection logic: developer tools (Azure CLI, VSCode, PowerShell) accessing either Graph or legacy AAD are flagged, while any FOCI app accessing legacy AAD is flagged since this deprecated API is rarely used legitimately and attackers target it for stealth.

### Possible investigation steps

- Review `o365.audit.UserId` to identify the impacted account and validate whether the user expected to authorize the application.
- Check `o365.audit.ActorIpAddress` for unexpected IPs, especially outside corporate ranges or from proxy/VPN networks.
- Examine `user_agent.original` and `o365.audit.DeviceProperties` for suspicious patterns (automation tools, headless browsers, unusual browser/OS combinations).
- Confirm `o365.audit.Target.ID` to identify the resource being accessed. Legacy AAD (`00000002-0000-0000-c000-000000000000`) access is unusual for most users.
- Review `o365.audit.ExtendedProperties.RequestType` and `ResultStatusDetail` - `OAuth2:Authorize` with `Redirect` indicates the OAuth code was exposed to the user.
- Look for subsequent `OAuth2:Token` events from different IPs using the same `o365.audit.UserId`, which indicates token exchange from attacker infrastructure.
- Pivot to `azure.graphactivitylogs` to check for follow-up Graph API activity (mailbox enumeration, file access) from unfamiliar locations.
- Correlate with `azure.signinlogs` for additional sign-in context and device details.

### False positive analysis

- Developers or IT users intentionally using Visual Studio Code, Azure CLI, or Azure PowerShell to connect to Microsoft 365.
- Legitimate VS Code extensions that sync or query Graph API data (calendars, tasks, cloud-hosted notebooks).
- Enterprise automation or CI/CD pipelines using these tools with user-delegated permissions.
- Exclude known user agents and hosts that regularly use these applications against Graph.
- Whitelist specific source IPs or devices tied to developer machines.

### Response and remediation

- Contact the user to confirm if they expected this login or may have shared an OAuth code via phishing page, Signal, or WhatsApp.
- If unauthorized, revoke all refresh tokens for the user and reset credentials.
- Review recent Microsoft Graph activity (email, file access, Teams) for signs of data exfiltration.
- Block or restrict future use of OAuth tokens from unknown apps or IPs via Conditional Access.
- Check `azure.auditlogs` for device registration events and remove any unauthorized registrations.
- Educate users about OAuth phishing techniques and the risks of sharing authorization codes.
