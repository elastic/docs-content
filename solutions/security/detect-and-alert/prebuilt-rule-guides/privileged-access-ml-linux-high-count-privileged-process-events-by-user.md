---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Spike in Privileged Command Execution by a User" prebuilt detection rule.
---

# Spike in Privileged Command Execution by a User

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in Privileged Command Execution by a User

Machine learning models are employed to monitor and analyze user behavior, specifically focusing on the execution of privileged commands. These models identify anomalies that may suggest unauthorized access attempts. Adversaries often exploit valid accounts to escalate privileges and access sensitive systems. The detection rule leverages ML to flag unusual spikes in command execution, indicating potential misuse of privileged access.

### Possible investigation steps

- Review the specific user account associated with the spike in privileged command execution to determine if the activity aligns with their typical behavior or job role.
- Analyze the timeline of the command execution spike to identify any patterns or specific times when the activity occurred, which may correlate with known maintenance windows or unusual access times.
- Cross-reference the commands executed with known privileged command lists to assess whether the commands are typical for the user's role or indicative of potential misuse.
- Check for any recent changes in the user's access rights or group memberships that might explain the increase in privileged command execution.
- Investigate any recent login activity for the user, including source IP addresses and devices, to identify any anomalies or unauthorized access attempts.
- Review any associated alerts or logs for the same user or system around the time of the spike to gather additional context or corroborating evidence of potential unauthorized access.

### False positive analysis

- Routine administrative tasks by IT staff may trigger the rule. To manage this, create exceptions for known maintenance windows or specific user accounts that regularly perform these tasks.
- Automated scripts or scheduled jobs that execute privileged commands can be mistaken for anomalies. Identify and whitelist these scripts or jobs to prevent false alerts.
- Users with newly assigned roles that require elevated privileges might cause a temporary spike in command execution. Monitor these users initially and adjust the model's sensitivity or add exceptions as needed.
- Software updates or installations that require elevated permissions can lead to false positives. Document these events and exclude them from the anomaly detection criteria.
- Training or onboarding sessions where users are learning to use new systems with privileged access can result in increased command execution. Temporarily adjust thresholds or exclude these users during the training period.

### Response and remediation

- Immediately isolate the affected user account to prevent further execution of privileged commands. This can be done by disabling the account or changing its password.
- Review recent privileged command execution logs to identify any unauthorized or suspicious activities performed by the user. Focus on commands that could alter system configurations or access sensitive data.
- Conduct a thorough investigation to determine if the user's credentials have been compromised. This may involve checking for signs of phishing attacks or unauthorized access from unusual locations or devices.
- If unauthorized access is confirmed, reset the affected user's credentials and any other accounts that may have been accessed using the compromised credentials.
- Notify the security team and relevant stakeholders about the incident, providing details of the detected anomaly and actions taken so far.
- Implement additional monitoring on the affected systems and user accounts to detect any further suspicious activities or attempts to regain unauthorized access.
- Review and update access controls and permissions to ensure that users have the minimum necessary privileges, reducing the risk of privilege escalation in the future.
