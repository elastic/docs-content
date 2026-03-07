---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Microsoft Graph Request Email Access by Unusual User and Client" prebuilt detection rule.'
---

# Microsoft Graph Request Email Access by Unusual User and Client

## Triage and analysis

### Investigating Microsoft Graph Request Email Access by Unusual User and Client

This rule detects instances where a previously unseen or rare Microsoft Graph application client ID accesses email-related APIs, such as `/me/messages`, `/sendMail`, or `/mailFolders/inbox/messages`. These accesses are performed via delegated user credentials using common OAuth scopes like `Mail.Read`, `Mail.ReadWrite`, `Mail.Send`, or `email`. This activity may indicate unauthorized use of a newly consented or compromised application to read or exfiltrate mail content. This is a New Terms rule that only signals if the application ID (`azure.graphactivitylogs.properties.app_id`) and user principal object ID (`azure.graphactivitylogs.properties.user_principal_object_id`) have not been seen doing this activity in the last 14 days.

### Possible Investigation Steps:

- `azure.graphactivitylogs.properties.app_id`: Investigate the application ID involved. Is it known and sanctioned in your tenant? Pivot to Azure Portal → Enterprise Applications → Search by App ID to determine app details, publisher, and consent status.
- `azure.graphactivitylogs.properties.scopes`: Review the scopes requested by the application. Email-related scopes such as `Mail.ReadWrite` and `Mail.Send` are especially sensitive and suggest the app is interacting with mail content.
- `url.path` / `azure.graphactivitylogs.properties.requestUri`: Determine exactly which mail-related APIs were accessed (e.g., reading inbox, sending messages, enumerating folders).
- `user.id`: Identify the user whose credentials were used. Determine if the user recently consented to a new app, clicked a phishing link, or reported suspicious activity.
- `user_agent.original`: Check for suspicious automation tools (e.g., `python-requests`, `curl`, non-browser agents), which may suggest scripted access.
- `source.ip` and `client.geo`: Investigate the source IP and geography. Look for unusual access from unexpected countries, VPS providers, or anonymizing services.
- `http.request.method`: Determine intent based on HTTP method — `GET` (reading), `POST` (sending), `PATCH`/`DELETE` (modifying/removing messages).
- `token_issued_at` and `@timestamp`: Determine how long the token has been active and whether access is ongoing or recent.
- `azure.graphactivitylogs.properties.c_sid`: Use the session correlation ID to identify other related activity in the same session. This may help identify if the app is accessing multiple users' mailboxes or if the same user is accessing multiple apps.
- Correlate with Microsoft Entra ID (`azure.auditlogs` and `azure.signinlogs`) to determine whether:
  - The app was recently granted admin or user consent
  - Risky sign-ins occurred just prior to or after mail access
  - The same IP or app ID appears across multiple users

### False Positive Analysis

- New legitimate apps may appear after a user consents via OAuth. Developers, third-party tools, or IT-supplied utilities may access mail APIs if users consent.
- Users leveraging Microsoft development environments (e.g., Visual Studio Code) may trigger this behavior with delegated `.default` permissions.
- Admin-approved apps deployed via conditional access may trigger similar access logs if not previously seen in detection baselines.

### Response and Remediation

- If access is unauthorized or unexpected:
  - Revoke the app's consent in Azure AD via the Enterprise Applications blade.
  - Revoke user refresh tokens via Microsoft Entra or PowerShell.
  - Investigate the user's session and alert them to possible phishing or OAuth consent abuse.
- Review and restrict risky OAuth permissions in Conditional Access and App Governance policies.
- Add known, trusted app IDs to a detection allowlist to reduce noise in the future.
- Continue monitoring the app ID for additional usage across the tenant or from suspicious IPs.
