---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "M365 Identity User Brute Force Attempted" prebuilt detection rule.
---

# M365 Identity User Brute Force Attempted

## Triage and Analysis

### Investigating M365 Identity User Brute Force Attempted

Identifies brute-force authentication activity targeting Microsoft 365 user accounts using failed sign-in patterns that match password spraying, credential stuffing, or password guessing behavior. Adversaries may attempt brute-force authentication with credentials obtained from previous breaches, leaks, marketplaces or guessable passwords.

### Possible investigation steps

- Review `user_id_list`: Enumerates the user accounts targeted. Look for naming patterns or privilege levels (e.g., admins).
- Check `login_errors`: A consistent error such as `"InvalidUserNameOrPassword"` confirms a spray-style attack using one or a few passwords.
- Examine `ip_list` and `source_orgs`: Determine if the traffic originates from a known corporate VPN, datacenter, or suspicious ASN like hosting providers or anonymizers.
- Review `countries` and `unique_country_count`: Geographic anomalies (e.g., login attempts from unexpected regions) may indicate malicious automation.
- Validate `total_attempts` vs `duration_seconds`: A high frequency of login attempts over a short period may suggest automation rather than manual logins.
- Cross-reference with successful logins: Pivot to surrounding sign-in logs (`azure.signinlogs`) or risk detections (`identityprotection`) for any account that eventually succeeded.
- Check for multi-factor challenges or bypasses: Determine if any of the accounts were protected or if the attack bypassed MFA.

### False positive analysis

- IT administrators using automation tools (e.g., PowerShell) during account provisioning may trigger false positives if login attempts cluster.
- Penetration testing or red team simulations may resemble spray activity.
- Infrequent, low-volume login testing tools like ADFS testing scripts can exhibit similar patterns.

### Response and remediation

- Initiate an internal incident ticket and inform the affected identity/IT team.
- Temporarily disable impacted user accounts if compromise is suspected.
- Investigate whether any login attempts succeeded after the spray window.
- Block the offending IPs or ASN temporarily via firewall or conditional access policies.
- Rotate passwords for all targeted accounts and audit for password reuse.
- Enforce or verify MFA is enabled for all user accounts.
- Consider deploying account lockout or progressive delay mechanisms if not already enabled.

