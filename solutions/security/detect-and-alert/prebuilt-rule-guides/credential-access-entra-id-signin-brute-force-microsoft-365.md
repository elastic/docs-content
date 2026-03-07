---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID Sign-in Brute Force Attempted (Microsoft 365)" prebuilt detection rule.
---

# Entra ID Sign-in Brute Force Attempted (Microsoft 365)

## Triage and analysis

### Investigating Entra ID Sign-in Brute Force Attempted (Microsoft 365)

Identifies brute-force authentication activity against Microsoft 365 services using Entra ID sign-in logs. This detection groups and classifies failed sign-in attempts based on behavior indicative of password spraying, credential stuffing, or password guessing. The classification (`bf_type`) is included for immediate triage.

### Possible investigation steps

- Review `bf_type`: Classifies the brute-force behavior (`password_spraying`, `credential_stuffing`, `password_guessing`).
- Examine `user_id_list`: Review the identities targeted. Are they admins, service accounts, or external identities?
- Review `login_errors`: Multiple identical errors (e.g., `"Invalid grant..."`) suggest automated abuse or tooling.
- Check `ip_list` and `source_orgs`: Determine if requests came from known VPNs, hosting providers, or anonymized infrastructure.
- Validate `unique_ips` and `countries`: Multiple countries or IPs in a short window may indicate credential stuffing or distributed spray attempts.
- Compare `total_attempts` vs `duration_seconds`: High volume over a short duration supports non-human interaction.
- Inspect `user_agent.original` via `device_detail_browser`: Clients like `Python Requests` or `curl` are highly suspicious.
- Investigate `client_app_display_name` and `incoming_token_type`: Identify non-browser-based logins, token abuse or commonly mimicked clients like VSCode.
- Review `target_resource_display_name`: Confirm the service being targeted (e.g., SharePoint, Exchange). This may be what authorization is being attempted against.
- Pivot using `session_id` and `device_detail_device_id`: Determine if a single device is spraying multiple accounts.
- Check `conditional_access_status`: If "notApplied", determine whether conditional access is properly scoped.
- Correlate `user_principal_name` with successful sign-ins: Investigate surrounding logs for lateral movement or privilege abuse.

### False positive analysis

- Developer automation (e.g., CI/CD logins) or mobile sync errors may create noisy but benign login failures.
- Red team exercises or pentesting can resemble brute-force patterns.
- Legacy protocols or misconfigured service principals may trigger repeated login failures from the same IP or session.

### Response and remediation

- Notify identity or security operations teams to investigate further.
- Lock or reset affected user accounts if compromise is suspected.
- Block the source IP(s) or ASN temporarily using conditional access or firewall rules.
- Review tenant-wide MFA and conditional access enforcement.
- Audit targeted accounts for password reuse across systems or tenants.
- Enable lockout or throttling policies for repeated failed login attempts.

