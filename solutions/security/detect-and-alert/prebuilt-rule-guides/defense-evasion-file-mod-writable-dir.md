---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "File Permission Modification in Writable Directory" prebuilt detection rule.'
---

# File Permission Modification in Writable Directory

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating File Permission Modification in Writable Directory

In Linux environments, writable directories like /tmp or /var/tmp are often used for temporary file storage. Adversaries exploit these by modifying file permissions to execute malicious payloads. The detection rule identifies non-root users altering permissions in these directories using commands like chmod or chown, excluding benign processes, to flag potential threats. This helps in identifying unauthorized permission changes indicative of defense evasion tactics.

### Possible investigation steps

- Review the process details to identify the non-root user who executed the permission modification command (chattr, chgrp, chmod, or chown) in the specified writable directories (/dev/shm, /tmp, or /var/tmp).
- Examine the parent process of the detected command to determine if it is associated with any known malicious activity or if it deviates from typical user behavior, ensuring it is not one of the excluded benign processes (apt-key, update-motd-updates-available, apt-get).
- Investigate the specific file or directory whose permissions were altered to assess its legitimacy and check for any associated suspicious files or payloads.
- Analyze recent activities by the identified user to detect any other anomalous behavior or unauthorized access attempts that could indicate a broader compromise.
- Cross-reference the event with other security logs and alerts to identify any correlated incidents or patterns that might suggest a coordinated attack or persistent threat.

### False positive analysis

- System updates and maintenance scripts may trigger permission changes in writable directories. Exclude processes like apt-key, update-motd-updates-available, and apt-get to reduce noise from legitimate system activities.
- Development and testing environments often involve frequent permission changes by non-root users. Consider excluding specific user accounts or processes known to be part of regular development workflows.
- Automated backup or synchronization tools might modify file permissions as part of their operations. Identify and exclude these tools if they are verified to be non-threatening.
- Custom scripts or applications that require permission changes for functionality should be reviewed and, if deemed safe, added to an exception list to prevent false alerts.
- Regularly review and update the exclusion list to ensure it reflects current operational practices and does not inadvertently allow malicious activities.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious processes identified in the alert that are associated with unauthorized permission changes.
- Revert any unauthorized file permission changes in the writable directories to their original state to prevent execution of malicious payloads.
- Conduct a thorough scan of the affected directories (/dev/shm, /tmp, /var/tmp) for any malicious files or payloads and remove them.
- Review user accounts and permissions to ensure that only authorized users have access to modify file permissions in sensitive directories.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for file permission changes in writable directories to detect similar threats in the future.
