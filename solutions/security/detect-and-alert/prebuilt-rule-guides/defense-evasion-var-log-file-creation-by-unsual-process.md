---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "File Creation in /var/log via Suspicious Process" prebuilt detection rule.'
---

# File Creation in /var/log via Suspicious Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating File Creation in /var/log via Suspicious Process

In Linux environments, the `/var/log` directory is crucial for storing system logs, which are essential for monitoring and troubleshooting. Adversaries may exploit this by creating files in this directory using executables from insecure locations, aiming to conceal their activities. The detection rule identifies such suspicious file creations by monitoring processes from world-writable or hidden paths, flagging potential evasion tactics.

### Possible investigation steps

- Review the process executable path to determine if it originates from a world-writable or hidden location such as /tmp, /var/tmp, /dev/shm, or similar directories. This can indicate potential malicious activity.
- Examine the process name and its parent process to understand the context of the file creation and identify if it is associated with known legitimate or suspicious activities.
- Check the file path in /var/log to see if the created file has any unusual naming conventions or lacks a file extension, which might suggest an attempt to hide or disguise the file.
- Investigate the user account under which the process was executed to determine if it has the necessary permissions and if the activity aligns with the user's typical behavior.
- Correlate the event with other logs or alerts from the same host to identify any related suspicious activities or patterns that could indicate a broader compromise.
- Assess the risk and impact of the file creation by considering the severity and risk score provided, and prioritize further actions based on this assessment.

### False positive analysis

- System maintenance scripts or legitimate applications may create temporary log files in /var/log using executables from directories like /tmp or /var/tmp. To handle this, identify and whitelist these known processes by their executable paths.
- Automated backup or monitoring tools might generate files in /var/log as part of their routine operations. Review these tools and exclude their processes from the rule to prevent unnecessary alerts.
- Development or testing environments often involve scripts that create log files in /var/log for debugging purposes. Consider excluding these environments from the rule or creating specific exceptions for known development processes.
- Some system updates or package installations might temporarily use world-writable directories for executable scripts that interact with /var/log. Monitor these activities and create exceptions for trusted update processes to reduce false positives.

### Response and remediation

- Isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious processes identified as originating from world-writable or hidden paths, especially those involved in file creation within /var/log.
- Conduct a thorough review of the files created in /var/log to determine if they contain malicious content or scripts, and remove any unauthorized files.
- Restore any affected system files or logs from a known good backup to ensure system integrity and continuity of logging.
- Implement stricter permissions on directories like /tmp, /var/tmp, and /dev/shm to prevent unauthorized execution of processes from these locations.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems are compromised.
- Update and enhance monitoring rules to detect similar suspicious activities in the future, focusing on process execution from insecure locations and unauthorized file creation in critical directories.
