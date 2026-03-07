---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Suspicious File Edit" prebuilt detection rule.
---

# Potential Suspicious File Edit

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Suspicious File Edit

In Linux environments, text editors create temporary swap files (.swp) during file editing. Adversaries exploit this by editing critical system files to maintain persistence or escalate privileges. The detection rule identifies the creation of .swp files in sensitive directories, signaling potential unauthorized file edits, thus alerting analysts to investigate further.

### Possible investigation steps

- Review the alert details to identify the specific file path and name of the .swp file that triggered the alert, focusing on the directories and files listed in the query.
- Check the system logs and recent user activity to determine if there was any legitimate reason for editing the file, such as a scheduled maintenance or update.
- Investigate the user account associated with the file creation event to verify if the user has the necessary permissions and if their activity aligns with their role.
- Examine the contents of the original file (if accessible) and compare it with known baselines or backups to identify any unauthorized changes or anomalies.
- Look for other suspicious activities on the host, such as unusual login attempts, privilege escalation events, or the presence of other temporary files in sensitive directories.
- Assess the system for signs of persistence mechanisms or privilege escalation attempts, especially if the .swp file is associated with critical system files like /etc/shadow or /etc/passwd.

### False positive analysis

- Editing non-sensitive files in monitored directories can trigger alerts. Users can create exceptions for specific directories or files that are frequently edited by authorized personnel.
- System administrators performing routine maintenance or updates may inadvertently create .swp files in sensitive directories. Implementing a whitelist for known maintenance activities can reduce false positives.
- Automated scripts or applications that open files in monitored directories for legitimate purposes can cause alerts. Identifying and excluding these processes from monitoring can help manage false positives.
- Developers working on configuration files in their home directories might trigger alerts. Excluding specific user directories or known development environments can mitigate these occurrences.
- Regular system updates or package installations might create temporary .swp files. Monitoring these activities and correlating them with update schedules can help distinguish between legitimate and suspicious activities.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement by the adversary.
- Terminate any suspicious processes associated with the creation of the .swp files in sensitive directories to halt any ongoing malicious activity.
- Restore the affected files from a known good backup to ensure system integrity and remove any unauthorized changes.
- Conduct a thorough review of user accounts and permissions, especially those with elevated privileges, to identify and revoke any unauthorized access.
- Implement additional monitoring on the affected system and similar environments to detect any further attempts to edit critical files.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are compromised.
- Review and update system hardening measures, such as file permissions and access controls, to prevent similar incidents in the future.
