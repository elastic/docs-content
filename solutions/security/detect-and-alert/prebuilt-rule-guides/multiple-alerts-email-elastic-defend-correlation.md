---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Elastic Defend and Email Alerts Correlation" prebuilt detection rule.'
---

# Elastic Defend and Email Alerts Correlation

## Triage and analysis
### Investigating Elastic Defend and Email Alerts Correlation

This rule correlates any Elastic Defend alert with an email security related alert by target user name.

### Possible investigation steps
- Review the alert details to identify the specific host and users involved.
- Investigate the individual alerts for the target user name and see if they are related.
- Review all emails received from Esql.source_user_name and if there are other impacted users.
- Correlate the alert data with other logs and telemetry from the host, such as process creation, network connections, and file modifications, to gather additional context.
- Assess the impact and scope of the potential compromise by determining if other hosts or systems have similar alerts or related activity.

### False positive analysis
- Legitimate email marked as suspicious.
- Legitimate file or behavior marked as suspicious by Elastic Defend.
- Unrelated alerts where the target user name is too generic.

### Response and remediation
- Isolate the affected host from the network immediately to prevent further lateral movement by the adversary.
- Conduct a thorough forensic analysis of the host.
- Remove any identified malicious software or unauthorized access tools from the host, ensuring all persistence mechanisms are eradicated.
- Restore the host from a known good backup if necessary, ensuring that the backup is free from compromise.
- Monitor the host and network for any signs of re-infection or further suspicious activity, using enhanced logging and alerting based on the identified attack patterns.
- Escalate the incident to the appropriate internal or external cybersecurity teams for further investigation and potential legal action if the attack is part of a larger campaign.
