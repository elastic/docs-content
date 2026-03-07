---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Google SecOps External Alerts" prebuilt detection rule.
---

# Google SecOps External Alerts

Triage and analysis

### Investigating Google SecOps External Alerts

Google SecOps provides a robust framework for monitoring and managing security operations within cloud environments. The rule leverages specific event identifiers to flag suspicious alerts, enabling analysts to swiftly investigate potential threats and mitigate risks.

### Possible investigation steps

- Examine the timeline of events leading up to and following the alert to identify any unusual patterns or activities that may indicate malicious behavior.
- Cross-reference the alert with other security logs and alerts to determine if it is part of a broader attack pattern or isolated incident.
- Investigate the source and destination IP addresses involved in the alert to assess their legitimacy and check for any known malicious activity associated with them.
- Analyze user activity associated with the alert to identify any unauthorized access or privilege escalation attempts.
- Consult the Google SecOps investigation guide and resources tagged in the alert for specific guidance on handling similar threats.

### False positive analysis

- Alerts triggered by routine administrative actions can be false positives. Review the context of the alert to determine if it aligns with known maintenance activities.
- Automated scripts or tools that interact with Google SecOps may generate alerts. Identify these scripts and consider creating exceptions for their expected behavior.
- Frequent alerts from specific IP addresses or user accounts that are known to be secure can be excluded by adding them to an allowlist.
- Alerts resulting from testing or development environments should be reviewed and, if deemed non-threatening, excluded from triggering further alerts.
- Regularly update and review exception lists to ensure they reflect current non-threatening behaviors and do not inadvertently exclude genuine threats.

### Response and remediation

- Immediately isolate affected systems or accounts identified in the Google SecOps alert to prevent further unauthorized access or data exfiltration.
- Conduct a thorough review of the alert details to identify any compromised credentials or access tokens and reset them promptly.
- Implement network segmentation or access control measures to limit the spread of potential threats within the environment.
- Review and update firewall rules and security group settings to block any suspicious IP addresses or domains associated with the alert.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional resources are needed.
- Document the incident, including all actions taken, and update incident response plans to incorporate lessons learned from this event.
- Enhance monitoring and detection capabilities by tuning existing alerts and deploying additional rules to detect similar activities in the future.

