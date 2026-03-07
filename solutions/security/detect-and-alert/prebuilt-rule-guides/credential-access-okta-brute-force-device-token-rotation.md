---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Okta Brute Force (Device Token Rotation)" prebuilt detection rule.'
---

# Potential Okta Brute Force (Device Token Rotation)

## Triage and analysis

### Investigating Potential Okta Brute Force (Device Token Rotation)

This rule identifies excessive unique device token hashes generated for a single user account, indicating automated brute force tooling that fails to persist browser cookies between authentication attempts.

#### Possible investigation steps
- Identify the targeted user account and determine if it has elevated privileges or sensitive access.
- Review the source IP and check if it belongs to known proxy, VPN, or cloud infrastructure.
- Examine user agent strings for signs of automation, scripting tools, or inconsistent browser fingerprints.
- Check if Okta flagged the source as a known threat or proxy.
- Determine if any authentication attempts succeeded following the failed attempts.
- Review the user's recent activity for signs of account compromise.

### False positive analysis
- Users experiencing login issues may generate multiple device tokens through repeated legitimate attempts.
- Automated testing or monitoring tools that do not persist cookies may trigger this rule.
- Browser extensions or privacy tools that clear cookies between requests may cause device token rotation.

### Response and remediation
- If attack is confirmed, reset the user's password immediately.
- Block the source IP at the network perimeter.
- Review and potentially reset MFA for the targeted account.
- Monitor for any successful authentication that may indicate compromise.
- Contact the user to verify if they experienced legitimate login issues.
