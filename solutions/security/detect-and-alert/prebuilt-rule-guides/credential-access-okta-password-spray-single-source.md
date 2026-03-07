---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Okta Password Spray (Single Source)" prebuilt detection rule.'
---

# Potential Okta Password Spray (Single Source)

## Triage and analysis

### Investigating Potential Okta Password Spray (Single Source)

This rule identifies a single source IP attempting authentication against multiple user accounts with repeated attempts per user over time. This pattern indicates password spraying where attackers try common passwords while pacing attempts to avoid lockouts.

#### Possible investigation steps
- Identify the source IP and determine if it belongs to known proxy, VPN, or cloud infrastructure.
- Review the list of targeted user accounts and check if any authentications succeeded.
- Analyze the timing of attempts to determine if they are paced to avoid lockout thresholds.
- Check if Okta flagged the source as a known threat or proxy.
- Examine user agent strings for signs of automation or consistent tooling across attempts.
- Review the geographic location and ASN of the source IP for anomalies.

### False positive analysis
- Corporate proxies or VPN exit nodes may aggregate traffic from multiple legitimate users with login issues.
- Automated processes or misconfigured applications retrying authentication may trigger this rule.
- Password rotation events may cause legitimate widespread authentication failures.

### Response and remediation
- If attack is confirmed, block the source IP at the network perimeter.
- Notify targeted users and enforce password resets for accounts that may have been compromised.
- Enable or strengthen MFA for targeted accounts.
- Consider implementing CAPTCHA or additional friction for suspicious authentication patterns.
- Review Okta sign-on policies to ensure lockout thresholds are appropriately configured.
