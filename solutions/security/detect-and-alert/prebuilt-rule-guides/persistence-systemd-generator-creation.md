---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Systemd Generator Created" prebuilt detection rule.
---

# Systemd Generator Created

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Systemd Generator Created

Systemd generators are scripts that systemd runs at boot or during configuration reloads to convert non-native configurations into unit files. Adversaries can exploit this by creating malicious generators to execute arbitrary code, ensuring persistence or escalating privileges. The detection rule identifies suspicious generator file creations or renames, excluding benign processes and file types, to flag potential abuse.

### Possible investigation steps

- Review the file path where the generator was created or renamed to determine if it is located in a standard systemd generator directory, such as /run/systemd/system-generators/ or /etc/systemd/user-generators/.
- Identify the process that created or renamed the generator file by examining the process.executable field, and determine if it is a known benign process or potentially malicious.
- Check the file extension and original extension fields to ensure the file is not a temporary or expected system file, such as those with extensions like "swp" or "dpkg-new".
- Investigate the history and behavior of the process that created the generator file, including any associated network connections or file modifications, to assess if it exhibits signs of malicious activity.
- Correlate the event with other security alerts or logs from the same host to identify any patterns or additional indicators of compromise that might suggest persistence or privilege escalation attempts.

### False positive analysis

- Package managers like dpkg, rpm, and yum can trigger false positives when they create or rename files in systemd generator directories during software installations or updates. To handle these, exclude processes associated with these package managers as specified in the rule.
- Automated system management tools such as Puppet and Chef may also create or modify generator files as part of their configuration management tasks. Exclude these processes by adding them to the exception list if they are part of your environment.
- Temporary files with extensions like swp, swpx, and swx, often created by text editors, can be mistakenly flagged. Ensure these extensions are included in the exclusion list to prevent unnecessary alerts.
- System updates or maintenance scripts that run as part of regular operations might create or modify generator files. Identify these scripts and add their executables to the exclusion list to reduce false positives.
- Custom scripts or tools that are part of legitimate administrative tasks may also trigger alerts. Review these scripts and consider excluding their executables if they are verified as non-malicious.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further execution of potentially malicious code and lateral movement.
- Terminate any suspicious processes associated with the creation or modification of systemd generator files to halt any ongoing malicious activity.
- Conduct a thorough review of the systemd generator directories to identify and remove any unauthorized or suspicious generator files.
- Restore any modified or deleted legitimate systemd generator files from a known good backup to ensure system integrity.
- Implement file integrity monitoring on systemd generator directories to detect unauthorized changes in the future.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Review and update access controls and permissions for systemd generator directories to limit the ability to create or modify files to authorized users only.
