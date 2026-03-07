---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Persistence via File Modification" prebuilt detection rule.'
---

# Potential Persistence via File Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Persistence via File Modification

File Integrity Monitoring (FIM) is crucial for detecting unauthorized changes to critical files, often targeted by adversaries for persistence. Attackers may modify cron jobs, systemd services, or shell configurations to maintain access or escalate privileges. The detection rule monitors these files for updates, flagging potential persistence attempts by identifying suspicious modifications outside normal operations.

### Possible investigation steps

- Review the file path from the alert to determine which specific file was modified and assess its role in the system, focusing on paths commonly used for persistence such as cron jobs, systemd services, or shell configurations.
- Check the timestamp of the modification event to correlate it with any known legitimate changes or scheduled maintenance activities, ensuring the modification was not part of normal operations.
- Investigate the user or process responsible for the modification by examining the associated user ID or process ID, and verify if the user or process has legitimate reasons to alter the file.
- Analyze recent login and session activity for the user or process involved in the modification to identify any unusual patterns or unauthorized access attempts.
- Cross-reference the modification event with other security logs or alerts to identify any related suspicious activities, such as privilege escalation attempts or unauthorized access to sensitive files.
- If the modified file is a configuration file, review its contents for any unauthorized or suspicious entries that could indicate persistence mechanisms, such as new cron jobs or altered systemd service configurations.

### False positive analysis

- Routine system updates or package installations may modify files monitored by the rule, such as those in /etc/cron.d or /etc/systemd/system. To manage these, consider excluding specific file paths or extensions like dpkg-new and dpkg-remove during known maintenance windows.
- User-specific configuration changes, such as updates to shell profiles in /home/*/.bashrc, can trigger alerts. Implement exceptions for user directories where frequent legitimate changes occur, ensuring these are well-documented and reviewed regularly.
- Automated scripts or management tools that update system configurations, like /etc/ssh/sshd_config, can cause false positives. Identify these tools and create exceptions for their expected file modification patterns.
- Temporary files created during system operations, such as /var/spool/cron/crontabs/tmp.*, may be flagged. Exclude these temporary paths to reduce noise while maintaining security oversight.
- Regular updates to known_hosts files in /home/*/.ssh/known_hosts can be mistaken for suspicious activity. Exclude these files from monitoring to prevent unnecessary alerts while ensuring SSH configurations are still monitored.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the attacker.
- Review the specific file modifications flagged by the alert to determine if they are unauthorized or malicious. Restore any altered files to their last known good state using backups or system snapshots.
- Change all passwords and SSH keys associated with the affected system to prevent unauthorized access using compromised credentials.
- Conduct a thorough scan of the system for additional indicators of compromise, such as unauthorized user accounts or unexpected running processes, and remove any malicious artifacts found.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if other systems may be affected.
- Implement additional monitoring on the affected system and similar systems to detect any further unauthorized file modifications or suspicious activities.
- Review and update access controls and permissions on critical files and directories to minimize the risk of unauthorized modifications in the future.
