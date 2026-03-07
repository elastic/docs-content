---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Loadable Kernel Module Configuration File Creation" prebuilt detection rule.
---

# Loadable Kernel Module Configuration File Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Loadable Kernel Module Configuration File Creation

Loadable Kernel Modules (LKMs) are components that can be dynamically loaded into the Linux kernel to extend its functionality without rebooting. Adversaries exploit this by creating or altering LKM configuration files to ensure their malicious modules load at startup, achieving persistence. The detection rule identifies suspicious file creation or renaming activities in key directories, excluding benign processes, to flag potential threats.

### Possible investigation steps

- Review the file path and name to determine if it matches any known or expected LKM configuration files, focusing on paths like /etc/modules, /etc/modprobe.d/*, and others specified in the query.
- Examine the process executable responsible for the file creation or renaming to identify if it is a known or trusted application, especially if it is not in the list of excluded executables.
- Check the process name and executable path for any anomalies or signs of masquerading, particularly if they are not in the list of excluded names or paths.
- Investigate the user account associated with the process to determine if it has legitimate access or if it might be compromised.
- Correlate the event with other recent system activities to identify any patterns or additional suspicious behavior, such as other file modifications or network connections.
- Review system logs for any related entries that might provide additional context or evidence of malicious activity.
- Assess the risk and impact of the detected activity on the system's security posture and determine if further containment or remediation actions are necessary.

### False positive analysis

- System package managers like dpkg, rpm, and yum may trigger false positives when they update or install legitimate kernel modules. To handle this, exclude these processes by adding them to the exception list in the detection rule.
- Automated system management tools such as Puppet, Chef, and Ansible can create or modify LKM configuration files during routine operations. Exclude these processes by specifying their executables in the exception criteria.
- Temporary files created by text editors or system processes, such as those with extensions like swp or swx, can be mistaken for suspicious activity. Exclude these file extensions to reduce false positives.
- Processes running from specific directories like /nix/store or /snap may be part of legitimate software installations. Add these paths to the exclusion list to prevent unnecessary alerts.
- Scheduled tasks or cron jobs that involve file operations in the monitored directories might be flagged. Identify and exclude these processes by their names or paths to minimize false positives.

### Response and remediation

- Isolate the affected system from the network to prevent further propagation of the malicious loadable kernel module.
- Terminate any suspicious processes identified in the alert that are associated with the creation or modification of LKM configuration files.
- Remove or revert any unauthorized changes to LKM configuration files in the specified directories to prevent the malicious module from loading on reboot.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious components.
- Review system logs and the history of executed commands to identify the initial vector of compromise and any other affected systems.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are compromised.
- Implement additional monitoring and alerting for similar suspicious activities to enhance detection and response capabilities for future incidents.
