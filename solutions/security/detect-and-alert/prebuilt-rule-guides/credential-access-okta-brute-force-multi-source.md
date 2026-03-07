---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Okta Brute Force (Multi-Source)" prebuilt detection rule.
---

# Potential Okta Brute Force (Multi-Source)

## Triage and analysis

### Investigating Potential Okta Brute Force (Multi-Source)

This rule identifies a single user account receiving failed authentication attempts from multiple unique source IPs. This pattern indicates attackers rotating through proxy infrastructure to evade IP-based detection while targeting a specific account.

#### Possible investigation steps
- Identify the targeted user account and determine if it has elevated privileges or sensitive access.
- Review the geographic distribution of source IPs for anomalies such as multiple countries or unusual locations.
- Examine the ASN ownership of source IPs for signs of proxy, VPN, or cloud infrastructure.
- Check if Okta flagged any of the sources as known threats or proxies.
- Determine if any authentication attempts succeeded following the failed attempts.
- Review the user's recent activity for signs of account compromise.

### False positive analysis
- Users traveling internationally with mobile devices may generate failed attempts from multiple locations.
- Service accounts accessed from distributed legitimate infrastructure may trigger this rule.
- Corporate VPN exit nodes spread across regions could appear as multiple IPs for a single user.

### Response and remediation
- If attack is confirmed, reset the user's password immediately.
- Review and potentially reset MFA for the targeted account.
- Block attacking IP addresses at the network perimeter.
- Consider implementing geo-restrictions for the targeted account if dispersed access is not expected.
- Monitor for any successful authentication that may indicate compromise.

