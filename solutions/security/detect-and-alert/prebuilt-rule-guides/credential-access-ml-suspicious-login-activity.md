---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Login Activity" prebuilt detection rule.'
---

# Unusual Login Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Login Activity
The 'Unusual Login Activity' detection leverages machine learning to identify anomalies in authentication patterns, flagging potential brute force attacks. Adversaries exploit credential access by attempting numerous logins to gain unauthorized entry. This rule assesses login frequency and patterns, alerting analysts to deviations indicative of credential abuse, thus enhancing threat detection and identity audit processes.

### Possible investigation steps

- Review the source IP addresses associated with the unusual login attempts to determine if they are known or suspicious.
- Check the user accounts involved in the alert for any recent changes or unusual activity, such as password resets or privilege escalations.
- Analyze the timestamps of the login attempts to identify patterns or timeframes that may indicate automated or scripted attacks.
- Correlate the login attempts with other security events or logs to identify any concurrent suspicious activities, such as failed login attempts or access to sensitive resources.
- Investigate the geographic locations of the login attempts to see if they align with the user's typical login behavior or if they suggest potential compromise.
- Assess the risk score and severity of the alert in the context of the organization's security posture and any ongoing threats or incidents.

### False positive analysis

- High login activity from automated scripts or scheduled tasks can trigger false positives. Identify and whitelist these known scripts to prevent unnecessary alerts.
- Employees using shared accounts may cause an increase in login attempts. Implement user-specific accounts and monitor shared account usage to reduce false positives.
- Frequent logins from IT personnel conducting routine maintenance can be misinterpreted as unusual activity. Exclude these users or adjust thresholds for specific roles to minimize false alerts.
- Users with legitimate reasons for high login frequency, such as customer support staff, should be identified and their activity patterns analyzed to adjust detection parameters accordingly.
- Remote workers using VPNs or accessing systems from multiple locations might trigger alerts. Consider location-based exceptions for known remote access points to avoid false positives.

### Response and remediation

- Immediately isolate the affected user accounts to prevent further unauthorized access and contain the threat.
- Reset passwords for the compromised accounts and enforce multi-factor authentication (MFA) to enhance security.
- Conduct a thorough review of recent login activity and access logs to identify any unauthorized access or data exfiltration.
- Notify the security operations team to monitor for any further suspicious activity and ensure continuous surveillance of the affected systems.
- Escalate the incident to the incident response team if there is evidence of data compromise or if the attack persists despite initial containment efforts.
- Implement additional monitoring rules to detect similar brute force attempts in the future, focusing on login frequency and patterns.
- Review and update access controls and authentication policies to prevent recurrence, ensuring they align with best practices for credential security.
