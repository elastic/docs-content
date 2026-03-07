---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "M365 Identity OAuth Flow by First-Party Microsoft App from Multiple IPs" prebuilt detection rule.'
---

# M365 Identity OAuth Flow by First-Party Microsoft App from Multiple IPs

## Triage and analysis

### Investigating M365 Identity OAuth Flow by First-Party Microsoft App from Multiple IPs

This rule detects when the same user authenticates to Microsoft Graph or legacy Azure AD using FOCI applications from multiple IP addresses within a 30-minute window. This pattern is a strong indicator of OAuth code/token theft attacks like ConsentFix, where the victim completes the OAuth authorize flow on their device (first IP), and the attacker exchanges the stolen authorization code for tokens from their infrastructure (second IP).

The rule aggregates events by user, application, and resource, requiring both `OAuth2:Authorize` and `OAuth2:Token` requests from at least 2 different IPs to fire - this indicates the code was generated on one IP and exchanged on another.

### Possible investigation steps

- Review `o365.audit.UserId` to identify the affected user and determine if they are a high-value target.
- Analyze `Esql.source_ip_values` to see all unique IP addresses used within the 30-minute window. Determine whether these originate from different geographic regions, cloud providers (AWS, Azure, GCP), or anonymizing infrastructure (Tor, VPNs).
- Use `Esql.time_window_date_trunc` to pivot into raw events and reconstruct the full sequence of resource access events with exact timestamps.
- Check `Esql.source_as_organization_name_values` for unfamiliar ASN organizations that may indicate attacker infrastructure.
- Review `Esql.o365_audit_ApplicationId_values` to confirm which first-party application was used.
- Pivot to `azure.auditlogs` to check for device join or registration events around the same timeframe, which may indicate persistence attempts.
- Correlate with `azure.identityprotection` to identify related risk detections such as anonymized IP access or token replay.
- Search for additional sign-ins from the IPs involved across other users to determine if this is part of a broader campaign.

### False positive analysis

- Developers or IT administrators working across environments (office, home, cloud VMs) may produce similar behavior.
- Users on VPN who switch servers or traveling between networks may show multiple IPs.
- Mobile users moving between cellular and WiFi networks during the time window.
- Consider correlating with device compliance status to distinguish managed vs. unmanaged access.

### Response and remediation

- If confirmed unauthorized, immediately revoke all refresh tokens for the affected user via Entra ID.
- Remove any devices registered during this session by checking `azure.auditlogs` for `Add device` events.
- Notify the user and determine whether they may have shared an OAuth code via phishing.
- Block the attacker IPs at the perimeter and add to threat intel feeds.
- Implement Conditional Access policies to restrict OAuth flows for these applications to compliant devices and approved locations.
- Monitor for follow-on activity like lateral movement, privilege escalation, or data exfiltration via Graph API.
