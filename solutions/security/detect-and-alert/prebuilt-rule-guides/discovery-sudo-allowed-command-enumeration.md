---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Sudo Command Enumeration Detected" prebuilt detection rule.
---

# Sudo Command Enumeration Detected

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Sudo Command Enumeration Detected

The sudo command in Linux environments allows users to execute commands with elevated privileges, typically as the root user. Attackers may exploit this by using the `sudo -l` command to list permissible commands, potentially identifying paths to escalate privileges. The detection rule identifies this behavior by monitoring for the execution of `sudo -l` from common shell environments, flagging potential misuse for privilege escalation.

### Possible investigation steps

- Review the process execution details to confirm the presence of the `sudo -l` command, ensuring the process name is "sudo" and the arguments include "-l" with an argument count of 2.
- Identify the parent process of the `sudo` command to determine the shell environment used, checking if it matches any of the specified shells like "bash", "dash", "sh", "tcsh", "csh", "zsh", "ksh", or "fish".
- Investigate the user account that executed the `sudo -l` command to assess if the activity aligns with their typical behavior or if it appears suspicious.
- Check for any recent changes in user permissions or sudoers configuration that might indicate unauthorized modifications.
- Correlate this event with other logs or alerts to identify any subsequent suspicious activities that might suggest privilege escalation attempts.

### False positive analysis

- System administrators frequently use the sudo -l command to verify their permissions. To reduce noise, consider excluding specific user accounts or groups known for legitimate use.
- Automated scripts or configuration management tools may execute sudo -l as part of routine checks. Identify these scripts and exclude their execution paths or parent processes from the rule.
- Some software installations or updates might invoke sudo -l to check permissions. Monitor and document these processes, then create exceptions for known benign software.
- Developers or testers might use sudo -l during debugging or testing phases. Coordinate with development teams to identify and exclude these activities when they are part of approved workflows.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement by the attacker.
- Review the sudoers file on the affected system to identify any unauthorized or suspicious entries that may have been added or modified, and revert any changes to their original state.
- Terminate any suspicious processes initiated by the user who executed the `sudo -l` command, especially if they are not part of normal operations.
- Reset the password of the user account involved in the alert to prevent further unauthorized access.
- Conduct a thorough review of system logs to identify any additional suspicious activity or commands executed by the user, and assess the scope of potential compromise.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems may be affected.
- Implement additional monitoring and alerting for similar `sudo -l` command executions across the environment to enhance detection and response capabilities.
