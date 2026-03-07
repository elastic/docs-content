---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Systemd Shell Execution During Boot" prebuilt detection rule.'
---

# Systemd Shell Execution During Boot

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Systemd Shell Execution During Boot

Systemd is a critical component in Linux, managing system and service initialization during boot. Adversaries may exploit systemd to execute shell commands at startup, ensuring persistence and potential privilege escalation. The detection rule identifies suspicious shell executions by monitoring processes initiated by systemd, focusing on those with specific characteristics indicative of unauthorized activity.

### Possible investigation steps

- Review the process details to confirm the parent process is indeed systemd and the command line used is "/sbin/init" to ensure the alert is not a false positive.
- Examine the specific shell process name (e.g., bash, sh, etc.) and its arguments to identify any unusual or suspicious commands being executed.
- Investigate the history and configuration of the systemd service or unit file associated with the suspicious process to determine if it has been modified or created recently.
- Check for any recent changes or anomalies in the initramfs or GRUB bootloader configurations that could indicate tampering or unauthorized modifications.
- Correlate the alert with other security events or logs from the same host to identify any patterns or additional indicators of compromise that might suggest a broader attack or persistence mechanism.

### False positive analysis

- Legitimate system maintenance scripts may trigger this rule if they are executed by systemd during boot. Users can create exceptions for known maintenance scripts by identifying their specific command lines and excluding them from the detection rule.
- Custom user scripts that are intentionally set to run at boot for automation purposes might be flagged. To handle this, users should document these scripts and adjust the rule to exclude their specific process names or command lines.
- Some Linux distributions may use shell scripts for legitimate boot-time operations. Users should verify the distribution's default boot scripts and exclude them if they are known to be safe and necessary for system operation.
- System updates or package installations that modify boot processes could cause false positives. Users should monitor for these events and temporarily adjust the rule to prevent unnecessary alerts during known update windows.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious shell processes identified as being executed by systemd during boot to halt potential malicious activity.
- Conduct a thorough review of systemd service files and configurations to identify and remove any unauthorized or malicious entries.
- Restore any modified system files or configurations from a known good backup to ensure system integrity.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring on the affected system and similar environments to detect any recurrence of the threat.
- Review and update access controls and permissions to limit the ability of unauthorized users to modify systemd configurations or execute shell commands during boot.
