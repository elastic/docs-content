---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Microsoft Graph Request User Impersonation by Unusual Client" prebuilt detection rule.
---

# Microsoft Graph Request User Impersonation by Unusual Client

## Triage and analysis

### Investigating Microsoft Graph Request User Impersonation by Unusual Client

This rule detects the first observed occurrence of a Microsoft Graph API request by a specific client application ID (`azure.graphactivitylogs.properties.app_id`) in combination with a user principal object ID (`azure.graphactivitylogs.properties.user_principal_object_id`) and tenant ID (`azure.tenant_id`) within the last 14 days. This may indicate unauthorized access following a successful phishing attempt, token theft, or abuse of OAuth workflows.

Adversaries frequently exploit legitimate Microsoft or third-party application IDs to avoid raising suspicion during initial access. By using pre-consented or trusted apps to interact with Microsoft Graph, attackers can perform actions on behalf of users without triggering conventional authentication alerts or requiring additional user interaction.

### Possible investigation steps

- Review `azure.graphactivitylogs.properties.user_principal_object_id` and correlate with recent sign-in logs for the associated user.
- Determine whether `azure.graphactivitylogs.properties.app_id` is a known and approved application in your environment.
- Investigate the `user_agent.original` field for signs of scripted access (e.g., automation tools or libraries).
- Check the source IP address (`source.ip`) and geolocation data (`source.geo.*`) for unfamiliar origins.
- Inspect `azure.graphactivitylogs.properties.scopes` to understand the level of access being requested by the app.
- Examine any follow-up Graph API activity from the same `app_id` or `user_principal_object_id` for signs of data access or exfiltration.
- Correlate with device or session ID fields (`azure.graphactivitylogs.properties.c_sid`, if present) to detect persistent or repeat activity.

### False positive analysis

- First-time use of a legitimate Microsoft or enterprise-approved application.
- Developer or automation workflows initiating new Graph API requests.
- Valid end-user activity following device reconfiguration or new client installation.
- Maintain an allowlist of expected `app_id` values and known developer tools.
- Suppress detections from known good `user_agent.original` strings or approved source IP ranges.
- Use device and identity telemetry to distinguish trusted vs. unknown activity sources.
- Combine with session risk or sign-in anomaly signals where available.

### Response and remediation

- Reach out to the user and verify whether they authorized the application access.
- Revoke active OAuth tokens and reset credentials if unauthorized use is confirmed.
- Search for additional Graph API calls made by the same `app_id` or `user_principal_object_id`.
- Investigate whether sensitive resources (mail, files, Teams, contacts) were accessed.
- Apply Conditional Access policies to limit Graph API access by app type, IP, or device state.
- Restrict user consent for third-party apps and enforce admin approval workflows.
- Monitor usage of new or uncommon `app_id` values across your tenant.
- Provide user education on OAuth phishing tactics and reporting suspicious prompts.

