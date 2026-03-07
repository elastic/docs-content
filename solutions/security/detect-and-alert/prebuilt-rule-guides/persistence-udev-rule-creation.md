---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Systemd-udevd Rule File Creation" prebuilt detection rule.
---

# Systemd-udevd Rule File Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Systemd-udevd Rule File Creation

Systemd-udevd manages device nodes and handles kernel device events in Linux, using rule files to automate responses to hardware changes. Adversaries can exploit this by creating malicious rules that execute commands when specific devices are connected. The detection rule monitors the creation of these rule files, excluding legitimate processes, to identify potential abuse and ensure system integrity.

### Possible investigation steps

- Review the file path and name to determine if the rule file is located in a directory commonly used for udev rules, such as /etc/udev/rules.d/ or /lib/udev/.
- Examine the process executable that created or renamed the rule file to identify if it is a known legitimate process or an unexpected one, as specified in the query.
- Check the file extension and ensure it is .rules, confirming it is intended for udev rule configuration.
- Investigate the process name and path to determine if it matches any of the excluded legitimate processes or paths, which could indicate a false positive.
- Analyze the contents of the newly created or modified rule file to identify any suspicious or malicious commands that could be executed when a device is connected.
- Correlate the event with other system logs to identify any related activities or anomalies around the time of the rule file creation or modification.
- Assess the risk and impact of the rule file creation by considering the context of the system and any potential persistence mechanisms it might enable for an adversary.

### False positive analysis

- System updates and package installations can trigger rule file creations. Exclude processes like dpkg, rpm, and yum by adding them to the exception list to prevent false positives during legitimate system maintenance.
- Container management tools such as Docker and Podman may create or modify udev rules. Exclude these processes to avoid alerts when containers are being managed.
- Automated system configuration tools like Puppet and Chef can modify udev rules as part of their operations. Add these tools to the exception list to reduce noise from routine configuration changes.
- Snap package installations and updates can lead to rule file changes. Exclude snapd and related processes to prevent false positives during snap operations.
- Netplan and systemd processes may generate or modify udev rules as part of network configuration or system initialization. Exclude these processes to avoid unnecessary alerts during legitimate system activities.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further execution of malicious udev rules and potential lateral movement.
- Identify and review the newly created or modified udev rule files in the specified directories to determine if they contain malicious commands or payloads.
- Remove any unauthorized or malicious udev rule files to prevent them from executing on device connection events.
- Restore any affected system configurations or files from a known good backup to ensure system integrity.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection tools to identify and remove any additional malware or persistence mechanisms.
- Monitor the system for any further suspicious activity or attempts to recreate malicious udev rules, adjusting detection mechanisms as necessary.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected, ensuring comprehensive threat containment and remediation.
