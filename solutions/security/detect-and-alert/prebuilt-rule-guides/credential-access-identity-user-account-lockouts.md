---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "M365 Identity User Account Lockouts" prebuilt detection rule.'
---

# M365 Identity User Account Lockouts

## Triage and Analysis

### Investigating M365 Identity User Account Lockouts

Detects a burst of Microsoft 365 user account lockouts within a short 5-minute window. A high number of IdsLocked login errors across multiple user accounts may indicate brute-force attempts for the same users resulting in lockouts.

This rule uses ESQL aggregations and thus has dynamically generated fields. Correlation of the values in the alert document may need to be performed to the original sign-in and Graph events for further context.

### Investigation Steps

- Review the `user_id_list`: Are specific naming patterns targeted (e.g., admin, helpdesk)?
- Examine `ip_list` and `source_orgs`: Look for suspicious ISPs or hosting providers.
- Check `duration_seconds`: A very short window with a high lockout rate often indicates automation.
- Confirm lockout policy thresholds with IAM or Entra ID admins. Did the policy trigger correctly?
- Use the `first_seen` and `last_seen` values to pivot into related authentication or audit logs.
- Correlate with any recent detection of password spraying or credential stuffing activity.
- Review the `request_type` field to identify which authentication methods were used (e.g., OAuth, SAML, etc.).
- Check for any successful logins from the same IP or ASN after the lockouts.

### False Positive Analysis

- Automated systems with stale credentials may cause repeated failed logins.
- Legitimate bulk provisioning or scripted tests could unintentionally cause account lockouts.
- Red team exercises or penetration tests may resemble the same lockout pattern.
- Some organizations may have a high volume of lockouts due to user behavior or legacy systems.

### Response Recommendations

- Notify affected users and confirm whether activity was expected or suspicious.
- Lock or reset credentials for impacted accounts.
- Block the source IP(s) or ASN temporarily using conditional access or firewall rules.
- Strengthen lockout and retry delay policies if necessary.
- Review the originating application(s) involved via `request_types`.
