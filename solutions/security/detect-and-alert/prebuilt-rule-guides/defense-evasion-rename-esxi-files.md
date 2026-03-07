---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Renaming of ESXI Files" prebuilt detection rule.
---

# Suspicious Renaming of ESXI Files

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Renaming of ESXI Files

VMware ESXi files are critical for virtual machine operations, storing configurations and states. Adversaries may rename these files to evade detection or disrupt services, a tactic known as masquerading. The detection rule identifies renaming events of specific VMware file types on Linux systems, flagging potential malicious activity by monitoring deviations from expected file extensions.

### Possible investigation steps

- Review the alert details to identify the specific file that was renamed, including its original and new name, to understand the nature of the change.
- Check the timestamp of the rename event to correlate it with other activities on the system, such as user logins or other file operations, to identify potential patterns or anomalies.
- Investigate the user account or process responsible for the rename action by examining system logs or user activity to determine if the action was authorized or suspicious.
- Analyze the system for any other recent rename events involving VMware-related files to assess if this is an isolated incident or part of a broader pattern.
- Examine the system for signs of compromise or unauthorized access, such as unexpected processes, network connections, or changes in system configurations, to identify potential threats.
- Consult with relevant stakeholders, such as system administrators or security teams, to verify if the rename action was part of a legitimate maintenance or operational task.

### False positive analysis

- Routine maintenance or administrative tasks may involve renaming VMware ESXi files for organizational purposes. To manage this, identify and exclude specific users or processes that regularly perform these tasks from triggering alerts.
- Automated backup or snapshot processes might rename files temporarily as part of their operation. Review and whitelist these processes to prevent unnecessary alerts.
- Development or testing environments often involve frequent renaming of virtual machine files for configuration testing. Consider excluding these environments from the rule or setting up a separate monitoring profile with adjusted thresholds.
- System updates or patches might include scripts that rename files as part of the update process. Verify and exclude these scripts if they are known and trusted.
- Custom scripts or tools used by IT teams for managing virtual machines may rename files as part of their functionality. Ensure these scripts are documented and excluded from triggering the rule.

### Response and remediation

- Immediately isolate the affected Linux system from the network to prevent further unauthorized access or potential spread of malicious activity.
- Verify the integrity of the renamed VMware ESXi files by comparing them with known good backups or snapshots, and restore any altered files from a secure backup if necessary.
- Conduct a thorough review of recent system logs and user activity to identify any unauthorized access or actions that may have led to the file renaming.
- Revert any unauthorized changes to system configurations or permissions that may have facilitated the renaming of critical files.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement additional monitoring on the affected system and similar environments to detect any further attempts at file masquerading or other suspicious activities.
- Review and update access controls and permissions for VMware ESXi files to ensure only authorized users have the ability to rename or modify these files.
