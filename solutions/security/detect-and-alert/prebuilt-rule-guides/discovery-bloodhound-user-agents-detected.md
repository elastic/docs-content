---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID Sign-in BloodHound Suite User-Agent Detected" prebuilt detection rule.
---

# Entra ID Sign-in BloodHound Suite User-Agent Detected

## Triage and analysis

This rule identifies potential enumeration activity using AzureHound, SharpHound, or BloodHound across Microsoft cloud services. These tools are often used by red teamers and adversaries to map users, groups, roles, applications, and access relationships within Microsoft Entra ID (Azure AD) and Microsoft 365.

The detection is based on known enumeration patterns, particularly the presence of suspicious user agent strings (e.g., `azurehound/`, `sharphound/`, `bloodhound/`) in various Azure and M365 logs. The rule monitors multiple log sources, including:

- Azure Graph API Activity Logs
- Microsoft 365 Audit Logs
- Entra ID Sign-in Logs
- Entra ID Audit Logs
- Azure Activity Logs

This ensures broader detection of credential abuse, token misuse, or unauthorized identity discovery activity from both interactive and non-interactive (API) sessions.

### Possible investigation steps

- Confirm the tool used via `user_agent.original`. Look for:
    - `azurehound/x.y.z`
    - `bloodhound/1.0`
    - `sharphound/1.0`
- Examine `url.original` or `url.path` to determine which APIs were accessed if Graph API activity logs. For example:
    - `/v1.0/organization`, `/v1.0/users`, `/v1.0/groups` may indicate user/group/tenant discovery.
- Identify the `user.id`, `user.name`, or `azure.auditlogs.properties.initiated_by.user.user_principal_name` fields to determine which identity executed the API request.
- Review `app_id`, `app_display_name`, or `client_id` to identify the application context (e.g., Azure CLI, Graph Explorer, unauthorized app).
- Check `http.request.method`, `http.response.status_code`, and `event.action` for enumeration patterns (many successful GETs in a short period) if Graph API activity logs.
- Investigate correlated sign-ins (`azure.signinlogs`) by the same user, IP, or app immediately preceding the API calls. Was MFA used? Is the location suspicious?
- Review `source.ip`, `client.geo.*`, and `network.*` fields to determine the origin of the requests. Flag unexpected IPs or ISPs.
- If the event originates in M365 Audit Logs, investigate cross-service activity: Exchange Online, Teams, SharePoint, or role escalations via Unified Audit.

### False positive analysis

- This activity may be benign if performed by red teams, internal security auditors, or known security tools under authorization.
- Automated monitoring solutions, cloud posture scanners, or legitimate Azure/M365 integrations may generate similar traffic. Review the `app_id` and user context.
- Developer activity in test tenants may include tool usage for learning or validation purposes.

### Response and remediation

- If confirmed malicious:
    - Revoke active sessions or tokens associated with the identified user/app.
    - Disable the account or rotate credentials immediately.
    - Review the role assignments (`Directory.Read.All`, `AuditLog.Read.All`, `Directory.AccessAsUser.All`) and remove excessive privileges.
    - Conduct historical analysis to determine how long enumeration has been occurring and what objects were queried.
    - Enable Conditional Access policies to require MFA for API and CLI-based access.
    - Validate audit logging and alerting is enabled across Microsoft Graph, Azure Activity Logs, and M365 workloads.

- If legitimate:
    - Document the source (e.g., red team operation, security tool).
    - Add appropriate allowlist conditions for service principal, user, source address or device if policy allows.


