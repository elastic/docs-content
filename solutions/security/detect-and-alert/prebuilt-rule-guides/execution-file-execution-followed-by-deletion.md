---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "File Creation, Execution and Self-Deletion in Suspicious Directory" prebuilt detection rule.
---

# File Creation, Execution and Self-Deletion in Suspicious Directory

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating File Creation, Execution and Self-Deletion in Suspicious Directory

In Linux environments, temporary directories like `/tmp` and `/var/tmp` are often used for storing transient files. Adversaries exploit these directories to execute malicious payloads and erase traces by creating, running, and deleting files swiftly. The detection rule identifies this pattern by monitoring file creation, execution, and deletion events within these directories, flagging suspicious activities that align with common malware behaviors.

### Possible investigation steps

- Review the file creation event details, focusing on the file path and name to determine if it matches known malicious patterns or if it is a legitimate file.
- Examine the process execution event, paying attention to the process name and parent process name to identify if the execution was initiated by a suspicious or unauthorized shell.
- Investigate the user.id and host.id associated with the events to determine if the activity aligns with expected user behavior or if it indicates potential compromise.
- Check for any network activity or connections initiated by the process to identify potential data exfiltration or communication with command and control servers.
- Analyze the deletion event to confirm whether the file was removed by a legitimate process or if it was part of a self-deletion mechanism used by malware.
- Correlate these events with any other alerts or logs from the same host or user to identify patterns or additional indicators of compromise.

### False positive analysis

- Development and testing activities in temporary directories can trigger false positives. Exclude specific paths or processes related to known development tools or scripts that frequently create, execute, and delete files in these directories.
- Automated system maintenance scripts may perform similar actions. Identify and whitelist these scripts by their process names or paths to prevent unnecessary alerts.
- Backup or deployment tools like Veeam or Spack may use temporary directories for legitimate operations. Add exceptions for these tools by specifying their executable paths or process names.
- Temporary file operations by legitimate applications such as web servers or database services might be flagged. Monitor and exclude these applications by their known behaviors or specific file paths they use.
- Regular system updates or package installations can involve temporary file handling. Recognize and exclude these activities by identifying the associated package manager processes or update scripts.

### Response and remediation

- Isolate the affected host immediately to prevent further spread of the potential malware. Disconnect it from the network to contain the threat.
- Terminate any suspicious processes identified in the alert, especially those executed from temporary directories, to stop any ongoing malicious activity.
- Conduct a thorough examination of the affected directories (/tmp, /var/tmp, etc.) to identify and remove any remaining malicious files or scripts.
- Restore any affected systems from a known good backup to ensure that no remnants of the malware remain.
- Update and patch the affected system to close any vulnerabilities that may have been exploited by the threat actor.
- Enhance monitoring and logging on the affected host and similar systems to detect any recurrence of this behavior, focusing on file creation, execution, and deletion events in temporary directories.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems may be compromised.
