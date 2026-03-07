---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Okta Alerts Following Unusual Proxy Authentication" prebuilt detection rule.
---

# Okta Alerts Following Unusual Proxy Authentication

## Triage and analysis

### Investigating Okta Alerts Following Unusual Proxy Authentication

This rule correlates the first occurrences of authentication behind a proxy followed by an alert with subsequent Okta security alerts for the same user. Attackers frequently use proxy infrastructure (VPNs, Tor, residential proxies) to mask their origin when using stolen credentials, and their post-authentication activity often triggers additional detection rules.

By correlating the proxy alert with other Okta alerts using an EQL sequence, this rule identifies users whose proxy-based authentication was followed by suspicious activity within a 1-hour window.

#### Possible investigation steps
- Identify the affected user and review the correlated security alerts to understand what suspicious activity was detected after the proxy authentication.
- Examine the proxy source IP addresses and cross-reference with threat intelligence feeds for known malicious infrastructure.
- Review the time gap between the proxy authentication and subsequent alert generation.
- Review the user's recent Okta activity for signs of account takeover (MFA changes, new devices, unusual app access).
- Verify with the user whether they intentionally used a proxy or VPN during this session.

### False positive analysis
- Users who legitimately use VPN services for privacy or remote work may trigger this rule if they also trigger unrelated alerts.
- Security testing or red team exercises using proxy infrastructure combined with testing that triggers alerts.
- Corporate VPN egress points that Okta classifies as proxy infrastructure.

### Response and remediation
- If account compromise is suspected, immediately revoke all active sessions for the user.
- Reset the user's password and MFA factors.
- Review and revoke any OAuth tokens or API keys associated with the account.
- Block the source proxy IP at the network perimeter if confirmed malicious.
- Review the user's access to sensitive applications and data during the suspicious session.

