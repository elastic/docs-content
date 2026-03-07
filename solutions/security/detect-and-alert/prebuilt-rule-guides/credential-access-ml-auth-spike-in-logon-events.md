---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Spike in Logon Events" prebuilt detection rule.
---

# Spike in Logon Events

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in Logon Events
The 'Spike in Logon Events' detection leverages machine learning to identify anomalies in authentication patterns, signaling potential threats like password spraying or brute force attacks. Adversaries exploit these methods to gain unauthorized access by overwhelming systems with login attempts. This rule detects unusual surges in successful logins, indicating possible credential access tactics, and aids in preemptive threat mitigation.

### Possible investigation steps

- Review the timestamp and source of the spike in logon events to determine the time frame and systems affected.
- Analyze the user accounts involved in the spike to identify any patterns or anomalies, such as accounts with multiple logins from different locations or IP addresses.
- Check for any recent changes in user permissions or roles that could explain the increase in logon events.
- Investigate the IP addresses associated with the logon events to identify any known malicious sources or unusual geographic locations.
- Correlate the logon events with other security alerts or logs, such as failed login attempts, to identify potential password spraying or brute force activities.
- Assess whether there are any concurrent alerts or indicators of compromise that could suggest a broader attack campaign.

### False positive analysis

- High-volume legitimate logins from automated systems or scripts can trigger false positives. Identify and whitelist these systems to prevent unnecessary alerts.
- Scheduled batch processes or system maintenance activities may cause spikes in logon events. Exclude these known activities by setting up exceptions based on time and source.
- Users with roles that require frequent logins, such as IT administrators or customer support agents, might be flagged. Create user-based exceptions for these roles to reduce false positives.
- Integration with third-party services that authenticate frequently can lead to detection triggers. Review and exclude these services from the rule to avoid misclassification.
- Consider adjusting the sensitivity of the machine learning model if certain patterns are consistently flagged as anomalies but are verified as legitimate.

### Response and remediation

- Immediately isolate the affected user accounts to prevent further unauthorized access. This can be done by disabling the accounts or resetting passwords.
- Conduct a thorough review of recent authentication logs to identify any other accounts that may have been compromised or targeted.
- Implement multi-factor authentication (MFA) for all user accounts to add an additional layer of security against unauthorized access.
- Notify the security operations team to monitor for any further suspicious logon activities and to ensure that the threat is contained.
- Escalate the incident to the incident response team if there is evidence of a broader attack or if sensitive data may have been accessed.
- Review and update access controls and permissions to ensure that users have the minimum necessary access to perform their roles.
- Enhance monitoring and alerting mechanisms to detect similar spikes in logon events in the future, ensuring rapid response to potential threats.
