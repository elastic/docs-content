---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Entra ID User Sign-in Brute Force Attempted" prebuilt detection rule.'
---

# Entra ID User Sign-in Brute Force Attempted

## Triage and analysis

### Investigating Entra ID User Sign-in Brute Force Attempted

This rule detects brute-force authentication activity in Entra ID sign-in logs. It classifies failed sign-in attempts into behavior types such as password spraying, credential stuffing, or password guessing. The classification (`bf_type`) helps prioritize triage and incident response.

### Possible investigation steps

- Review `bf_type`: Determines the brute-force technique being used (`password_spraying`, `credential_stuffing`, or `password_guessing`).
- Examine `user_id_list`: Identify if high-value accounts (e.g., administrators, service principals, federated identities) are being targeted.
- Review `login_errors`: Repetitive error types like `"Invalid Grant"` or `"User Not Found"` suggest automated attacks.
- Check `ip_list` and `source_orgs`: Investigate if the activity originates from suspicious infrastructure (VPNs, hosting providers, etc.).
- Validate `unique_ips` and `countries`: Geographic diversity and IP volume may indicate distributed or botnet-based attacks.
- Compare `total_attempts` vs `duration_seconds`: High rate of failures in a short time period implies automation.
- Analyze `user_agent.original` and `device_detail_browser`: User agents like `curl`, `Python`, or generic libraries may indicate scripting tools.
- Investigate `client_app_display_name` and `incoming_token_type`: Detect potential abuse of legacy or unattended login mechanisms.
- Inspect `target_resource_display_name`: Understand what application or resource the attacker is trying to access.
- Pivot using `session_id` and `device_detail_device_id`: Determine if a device is targeting multiple accounts.
- Review `conditional_access_status`: If not enforced, ensure Conditional Access policies are scoped correctly.

### False positive analysis

- Legitimate automation (e.g., misconfigured scripts, sync processes) can trigger repeated failures.
- Internal red team activity or penetration tests may mimic brute-force behaviors.
- Certain service accounts or mobile clients may generate repetitive sign-in noise if not properly configured.

### Response and remediation

- Notify your identity security team for further analysis.
- Investigate and lock or reset impacted accounts if compromise is suspected.
- Block offending IPs or ASNs at the firewall, proxy, or using Conditional Access.
- Confirm MFA and Conditional Access are enforced for all user types.
- Audit targeted accounts for credential reuse across services.
- Implement account lockout or throttling for failed sign-in attempts where possible.
