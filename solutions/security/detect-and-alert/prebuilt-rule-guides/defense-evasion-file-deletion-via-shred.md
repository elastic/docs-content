---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "File Deletion via Shred" prebuilt detection rule.'
---

# File Deletion via Shred

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating File Deletion via Shred

The `shred` command in Linux is used to securely delete files by overwriting them, making recovery difficult. Adversaries exploit this to erase traces of malicious activity, hindering forensic analysis. The detection rule identifies suspicious use of `shred` by monitoring its execution with specific arguments, excluding benign processes like `logrotate`, to flag potential defense evasion attempts.

### Possible investigation steps

- Review the process execution details to confirm the use of the `shred` command with suspicious arguments such as "-u", "--remove", "-z", or "--zero".
- Identify the user account associated with the `shred` process to determine if the activity aligns with expected behavior for that user.
- Investigate the parent process of `shred` to ensure it is not `logrotate` and assess whether the parent process is legitimate or potentially malicious.
- Examine the timeline of events leading up to and following the `shred` execution to identify any related suspicious activities or file modifications.
- Check for any other alerts or logs related to the same host or user to identify patterns or additional indicators of compromise.
- Assess the impact of the file deletion by determining which files were targeted and whether they are critical to system operations or security.

### False positive analysis

- Logrotate processes may trigger false positives as they use shred for legitimate log file management. Exclude logrotate as a parent process in detection rules to prevent these alerts.
- System maintenance scripts that securely delete temporary files using shred can cause false positives. Identify and whitelist these scripts to reduce unnecessary alerts.
- Backup or cleanup operations that involve shredding old data might be flagged. Review and exclude these operations if they are part of routine system management.
- User-initiated file deletions for privacy or space management can appear suspicious. Educate users on the implications of using shred and consider excluding known user actions if they are frequent and benign.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity or data exfiltration.
- Terminate any active `shred` processes that are not associated with legitimate applications like `logrotate` to halt ongoing file deletion.
- Conduct a thorough review of recent system logs and file access records to identify any additional malicious activities or files that may have been created or modified by the adversary.
- Restore any critical files that were deleted using `shred` from the most recent backup, ensuring the integrity and security of the backup source.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring on the affected system and similar environments to detect any future unauthorized use of `shred` or similar file deletion tools.
- Review and update endpoint security configurations to prevent unauthorized execution of file deletion commands by non-administrative users.
