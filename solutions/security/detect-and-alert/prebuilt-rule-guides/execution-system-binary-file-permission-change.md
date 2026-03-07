---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "System Binary Path File Permission Modification" prebuilt detection rule.'
---

# System Binary Path File Permission Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating System Binary Path File Permission Modification

In Linux environments, system binary paths contain critical executables. Adversaries may exploit these by altering file permissions to execute malicious payloads. The detection rule monitors processes like `chmod` and `chown` in key directories, flagging suspicious permission changes. It excludes benign activities, focusing on unauthorized modifications to prevent potential execution of harmful scripts.

### Possible investigation steps

- Review the process details to identify the exact command executed, focusing on the process name and arguments, especially those involving `chmod` or `chown` in critical directories like `/bin`, `/usr/bin`, and `/lib`.
- Examine the parent process information, including the executable path and command line, to determine if the process was initiated by a known or trusted application, excluding those like `udevadm`, `systemd`, or `sudo`.
- Check the user account associated with the process to verify if the action was performed by an authorized user or if there are signs of compromised credentials.
- Investigate the file or directory whose permissions were modified to assess its importance and potential impact, focusing on changes to permissions like `4755`, `755`, or `777`.
- Correlate the event with other security alerts or logs to identify any related suspicious activities, such as unauthorized access attempts or unexpected script executions.
- Review recent changes or updates in the system that might explain the permission modification, ensuring they align with legitimate administrative tasks or software installations.

### False positive analysis

- System updates and package installations often involve legitimate permission changes in system binary paths. Users can exclude processes with parent executables located in directories like /var/lib/dpkg/info to reduce noise from these activities.
- Administrative scripts or automation tools may execute chmod or chown commands as part of routine maintenance. Exclude processes with parent names such as udevadm, systemd, or sudo to prevent these from being flagged.
- Container initialization processes might trigger permission changes. Exclude processes with parent command lines like runc init to avoid false positives related to container setups.
- Temporary script executions during software installations can cause permission modifications. Exclude processes with parent arguments matching patterns like /var/tmp/rpm-tmp.* to filter out these benign events.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or execution of malicious payloads.
- Terminate any suspicious processes identified as executing `chmod` or `chown` commands in critical system binary paths.
- Revert any unauthorized file permission changes to their original state to ensure system integrity and prevent execution of malicious scripts.
- Conduct a thorough review of system logs and process execution history to identify any additional unauthorized activities or related threats.
- Escalate the incident to the security operations team for further investigation and to determine if the threat has spread to other systems.
- Implement additional monitoring on the affected system and similar environments to detect any recurrence of unauthorized permission modifications.
- Review and update access controls and permissions policies to minimize the risk of unauthorized modifications in critical system directories.
