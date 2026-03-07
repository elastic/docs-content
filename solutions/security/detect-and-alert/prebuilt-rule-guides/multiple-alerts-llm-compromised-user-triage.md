---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "LLM-Based Compromised User Triage by User" prebuilt detection rule.'
---

# LLM-Based Compromised User Triage by User

## Triage and analysis

### Investigating LLM-Based Compromised User Triage by User

Start by reviewing the `Esql.summary` field which contains the LLM's assessment of why this user was flagged. The
`Esql.confidence` score (0.7-1.0) indicates certainty - scores above 0.9 suggest strong indicators of compromise. Pay
attention to whether alerts span multiple hosts (`Esql.host_name_count_distinct`) as this often indicates lateral movement or
credential reuse.

### Possible investigation steps

- Review `Esql.kibana_alert_rule_name_values` to understand what detection rules triggered for this user.
- Check `Esql.user_email_values` and `user.email` to verify user identity and correlate with directory services.
- Check `Esql.host_name_values` to identify all hosts where the user triggered alerts - multi-host activity is suspicious.
- Examine `Esql.source_ip_values` for geographic anomalies or impossible travel scenarios.
- Review `Esql.kibana_alert_rule_threat_tactic_name_values` for concerning progressions (e.g., Initial Access followed by Credential Access).
- Query authentication logs for the user to identify unusual login times, locations, or failed attempts.
- Check if the user has recently had password resets, MFA changes, or permission modifications.
- Correlate with HR/identity systems to verify the user's expected access patterns and current employment status.

### False positive analysis

- IT administrators and service accounts may legitimately trigger alerts across multiple hosts.
- Travel or VPN usage can create geographic anomalies that appear suspicious.
- Automated service accounts may generate clustered alerts during scheduled tasks.
- Users in security or development roles may trigger alerts during legitimate testing activities.

### Response and remediation

- For high-confidence verdicts (>0.9), consider immediate account suspension pending investigation.
- Force password reset and MFA re-enrollment if credential compromise is suspected.
- Review and revoke any suspicious OAuth tokens, API keys, or session tokens for the user.
- Check for persistence mechanisms the attacker may have established using the compromised credentials.
- Audit all actions performed by the user during the alert window for data access or exfiltration.
- If lateral movement is confirmed, expand investigation to all hosts the user accessed.
