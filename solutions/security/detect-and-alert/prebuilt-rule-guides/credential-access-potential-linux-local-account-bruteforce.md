---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Linux Local Account Brute Force Detected" prebuilt detection rule.
---

# Potential Linux Local Account Brute Force Detected

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Linux Local Account Brute Force Detected

In Linux environments, the 'su' command is used to switch user accounts, often requiring a password. Adversaries exploit this by attempting numerous logins with various passwords to gain unauthorized access. The detection rule identifies suspicious activity by monitoring rapid, repeated 'su' command executions from a single process, excluding common legitimate parent processes, indicating potential brute force attempts.

### Possible investigation steps

- Review the process execution details to identify the parent process of the 'su' command, focusing on any unusual or unauthorized parent processes not listed in the exclusion list.
- Analyze the frequency and pattern of the 'su' command executions from the identified process to determine if they align with typical user behavior or indicate a brute force attempt.
- Check the user account targeted by the 'su' command attempts to assess if it is a high-value or sensitive account that might be of interest to adversaries.
- Investigate the source host (host.id) to determine if there are any other suspicious activities or anomalies associated with it, such as unusual network connections or other security alerts.
- Correlate the event timestamps with other logs or alerts to identify any concurrent suspicious activities that might indicate a coordinated attack effort.

### False positive analysis

- Legitimate administrative scripts or automation tools may trigger the rule if they execute the 'su' command frequently. To mitigate this, identify and whitelist these scripts or tools by adding their parent process names to the exclusion list.
- Scheduled tasks or cron jobs that require switching users might be misidentified as brute force attempts. Review and exclude these tasks by specifying their parent process names in the exclusion criteria.
- Development or testing environments where frequent user switching is part of normal operations can generate false positives. Consider excluding these environments from monitoring or adjust the detection threshold to better fit the operational context.
- Continuous integration or deployment systems that use the 'su' command for user context switching can be mistaken for brute force attempts. Add these systems' parent process names to the exclusion list to prevent false alerts.

### Response and remediation

- Immediately isolate the affected host to prevent further unauthorized access or lateral movement within the network.
- Terminate the suspicious process identified by the detection rule to stop ongoing brute force attempts.
- Reset passwords for the targeted user accounts to prevent unauthorized access using potentially compromised credentials.
- Review and update the password policy to enforce strong, complex passwords and consider implementing account lockout mechanisms after a certain number of failed login attempts.
- Conduct a thorough review of the affected system for any signs of successful unauthorized access or additional malicious activity, such as new user accounts or scheduled tasks.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems may be affected.
- Enhance monitoring and logging on the affected host and similar systems to detect and respond to future brute force attempts more effectively.
