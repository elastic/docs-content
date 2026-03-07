---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Privilege Escalation via Root Crontab File Modification" prebuilt detection rule.'
---

# Privilege Escalation via Root Crontab File Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Privilege Escalation via Root Crontab File Modification

Crontab files in macOS are used to schedule tasks, often requiring elevated privileges for execution. Adversaries exploit this by modifying the root crontab file, enabling unauthorized code execution with root access. The detection rule identifies suspicious modifications to this file, excluding legitimate crontab processes, to flag potential privilege escalation attempts.

### Possible investigation steps

- Review the alert details to confirm the file path involved is /private/var/at/tabs/root, as this is the specific file path targeted by the rule.
- Examine the process that modified the root crontab file by checking the process executable path. Ensure it is not /usr/bin/crontab, which is excluded as a legitimate process.
- Investigate the user account associated with the process that made the modification to determine if it has legitimate access or if it might be compromised.
- Check for any recent changes or anomalies in user account activity or permissions that could indicate unauthorized access or privilege escalation attempts.
- Correlate this event with other security alerts or logs from the same host to identify any patterns or additional suspicious activities that might suggest a broader attack campaign.
- Assess the risk and impact of the modification by determining if any unauthorized or malicious tasks have been scheduled in the crontab file.

### False positive analysis

- System maintenance tasks or updates may modify the root crontab file. To handle these, users can create exceptions for known maintenance processes that are verified as safe.
- Administrative scripts that require scheduled tasks might trigger this rule. Users should document and exclude these scripts if they are part of regular, authorized operations.
- Backup or monitoring software that interacts with crontab files could cause false positives. Verify these applications and exclude their processes if they are legitimate and necessary for system operations.
- Custom automation tools used by IT departments might modify crontab files. Ensure these tools are reviewed and whitelisted if they are part of approved workflows.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or execution of malicious tasks.
- Review the modified root crontab file to identify any unauthorized or suspicious entries and remove them to stop any malicious scheduled tasks.
- Conduct a thorough investigation to determine how the crontab file was modified, focusing on identifying any exploited vulnerabilities or unauthorized access points.
- Reset credentials and review permissions for any accounts that may have been compromised or used in the attack to prevent further unauthorized access.
- Apply security patches and updates to the operating system and any vulnerable applications to close exploited vulnerabilities.
- Monitor the system and network for any signs of continued unauthorized activity or attempts to modify crontab files, using enhanced logging and alerting mechanisms.
- Escalate the incident to the appropriate internal security team or external cybersecurity experts if the threat persists or if there is evidence of a broader compromise.
