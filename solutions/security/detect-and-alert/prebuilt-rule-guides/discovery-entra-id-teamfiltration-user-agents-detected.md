---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID Sign-in TeamFiltration User-Agent Detected" prebuilt detection rule.
---

# Entra ID Sign-in TeamFiltration User-Agent Detected

## Triage and analysis

Identifies potential enumeration or password spraying activity using TeamFiltration tool. TeamFiltration is an open-source enumeration, password spraying and exfiltration tool designed for Entra ID and Microsoft 365. Adversaries are known to use TeamFiltration in-the-wild to enumerate users, groups, and roles, as well as to perform password spraying attacks against Microsoft Entra ID and Microsoft 365 accounts. This rule detects the use of TeamFiltration by monitoring for specific user-agent strings associated with the tool in Azure and Microsoft 365 logs.

The detection is based on TeamFiltration's hardcoded user agent string and/or the use of `Electron` by monitoring multiple log sources, including:

- Azure Graph API Activity Logs
- Microsoft 365 Audit Logs
- Entra ID Sign-in Logs
- Entra ID Audit Logs
- Azure Activity Logs

### Possible investigation steps

- Confirm the tool used via `user_agent.original`.
- Identify the `user.id`, `user.name`, or `azure.signinlogs.properties.user_principal_name` fields to determine which identity executed the API requests or sign-in attempts.
- Review `app_id`, `app_display_name`, or `client_id` to identify the application context (e.g., Azure CLI, Graph Explorer, unauthorized app). TeamFiltration uses a list of FOCI compliant applications to perform enumeration and password spraying. TeamFiltration uses Microsoft Teams client ID `1fec8e78-bce4-4aaf-ab1b-5451cc387264` for enumeration.
- Check `http.request.method`, `http.response.status_code`, and `event.action` for enumeration patterns (many successful GETs in a short period) if Graph API activity logs.
- Investigate correlated sign-ins (`azure.signinlogs`) by the same user, IP, or app immediately preceding the API calls. Was MFA used? Is the location suspicious?
- Review `source.ip` or `client.geo.*` fields to determine the origin of the requests. Flag unexpected IPs or ISPs. Check the for the use of several source addresses originating from Amazon ASNs (e.g., `AS16509`, `AS14618`, `AS14618`) which are commonly used by TeamFiltration as it proxies requests through FireProx and Amazon API Gateway.
- If the event originates in M365 Audit Logs, investigate cross-service activity: Exchange Online, Teams, SharePoint, or role escalations via Unified Audit.

### False positive analysis

- This activity may be benign if performed by red teams, internal security auditors, or known security tools under authorization.

### Response and remediation

- If confirmed malicious:
    - Identify successful sign-in attempts or API calls made by the user or app.
    - Revoke active sessions or tokens associated with the identified user/app.
    - Disable the account or rotate credentials immediately.
    - Review the role assignments (`Directory.Read.All`, `AuditLog.Read.All`, `Directory.AccessAsUser.All`) and remove excessive privileges.
    - Conduct historical analysis to determine how long enumeration has been occurring and what objects were queried.
    - Enable Conditional Access policies to require MFA for API and CLI-based access.
    - Validate audit logging and alerting is enabled across Microsoft Graph, Azure Activity Logs, and M365 workloads.

- If legitimate:
    - Document the source or user (e.g., red team operation, security tool).
    - Add appropriate allowlist conditions for service principal, user, source address or device if policy allows.


