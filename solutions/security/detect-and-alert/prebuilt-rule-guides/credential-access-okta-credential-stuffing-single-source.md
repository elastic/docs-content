---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Okta Credential Stuffing (Single Source)" prebuilt detection rule.
---

# Potential Okta Credential Stuffing (Single Source)

## Triage and analysis

### Investigating Potential Okta Credential Stuffing (Single Source)

This rule identifies a single source IP attempting authentication against many user accounts with minimal attempts per user. This pattern indicates credential stuffing where attackers rapidly test breached username and password pairs.

#### Possible investigation steps
- Identify the source IP and determine if it belongs to known proxy, VPN, or cloud infrastructure.
- Review the list of targeted user accounts and check if any authentications succeeded.
- Examine the user agent strings for signs of automation or scripting tools.
- Check if Okta flagged the source as a known threat or proxy.
- Determine if any targeted accounts have elevated privileges or access to sensitive systems.
- Review the geographic location and ASN of the source IP for anomalies.

### False positive analysis
- Corporate proxies or VPN exit nodes may aggregate traffic from multiple legitimate users.
- Shared systems such as kiosks or conference room computers may have multiple users authenticating.
- Legitimate SSO integrations may generate multiple authentication attempts from a single source.

### Response and remediation
- If attack is confirmed, block the source IP at the network perimeter.
- Reset passwords for any accounts that may have been compromised.
- Enable or strengthen MFA for targeted accounts.
- Review Okta sign-on policies to add additional friction for suspicious authentication patterns.
- If this is a known legitimate source, consider adding an exception for the IP or ASN.

