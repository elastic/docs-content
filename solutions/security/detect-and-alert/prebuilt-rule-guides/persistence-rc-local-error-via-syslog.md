---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious rc.local Error Message" prebuilt detection rule.'
---

# Suspicious rc.local Error Message

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious rc.local Error Message

The rc.local script is crucial in Linux systems, executing commands at boot. Adversaries may exploit this by inserting malicious scripts to gain persistence. The detection rule monitors syslog for specific error messages linked to rc.local, such as "Connection refused," indicating potential tampering. This proactive monitoring helps identify unauthorized modifications, mitigating persistent threats.

### Possible investigation steps

- Review the syslog entries for the specific error messages "Connection refused," "No such file or directory," or "command not found" associated with the rc.local process to understand the context and frequency of these errors.
- Check the rc.local file for any recent modifications or unusual entries that could indicate tampering or unauthorized changes.
- Investigate the source of the error messages by identifying any related processes or network connections that might have triggered the "Connection refused" error.
- Examine the system's boot logs and startup scripts to identify any anomalies or unauthorized scripts that may have been introduced.
- Cross-reference the timestamps of the error messages with other system logs to identify any correlated suspicious activities or changes in the system.

### False positive analysis

- Legitimate software updates or installations may modify the rc.local file, triggering error messages. Users can create exceptions for known update processes by identifying the specific software and excluding its related syslog entries.
- Custom scripts or administrative tasks that intentionally modify rc.local for legitimate purposes might cause false alerts. Document these scripts and add them to an exclusion list to prevent unnecessary alerts.
- Network configuration changes can lead to temporary "Connection refused" errors. If these changes are expected, users should temporarily adjust the monitoring rule to ignore these specific messages during the maintenance window.
- System misconfigurations or missing dependencies might result in "No such file or directory" or "command not found" errors. Regularly audit system configurations and ensure all necessary files and commands are correctly installed to minimize these false positives.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or spread of potential malware.
- Review the rc.local file for unauthorized modifications and restore it from a known good backup if tampering is confirmed.
- Conduct a thorough scan of the system using updated antivirus and anti-malware tools to identify and remove any malicious scripts or software.
- Check for additional persistence mechanisms by reviewing other boot or logon initialization scripts and scheduled tasks.
- Escalate the incident to the security operations team for further investigation and to determine if other systems are affected.
- Implement enhanced monitoring on the affected system and similar systems to detect any future unauthorized changes to boot scripts.
- Review and update access controls and permissions to ensure that only authorized personnel can modify critical system files like rc.local.
