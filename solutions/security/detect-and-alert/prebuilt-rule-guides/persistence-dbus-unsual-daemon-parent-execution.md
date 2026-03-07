---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual D-Bus Daemon Child Process" prebuilt detection rule.'
---

# Unusual D-Bus Daemon Child Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual D-Bus Daemon Child Process

The D-Bus daemon is a crucial component in Linux environments, facilitating inter-process communication by allowing applications to exchange information. Adversaries may exploit this by spawning unauthorized child processes to execute malicious code or gain elevated privileges. The detection rule identifies anomalies by monitoring child processes of the D-Bus daemon, excluding known benign processes and paths, thus highlighting potential threats.

### Possible investigation steps

- Review the process details to identify the unusual child process spawned from the dbus-daemon, focusing on the process name and executable path to determine if it is known or potentially malicious.
- Examine the command-line arguments (process.args) of the unusual child process to understand its intended function and assess if it aligns with typical usage patterns.
- Investigate the parent process arguments (process.parent.args) to confirm whether the dbus-daemon was running in a session context or another mode that might explain the unusual child process.
- Check the process start time and correlate it with other system events or logs to identify any related activities or anomalies occurring around the same time.
- Look into the user context under which the unusual child process was executed to determine if it was initiated by a legitimate user or potentially compromised account.
- Search for any network connections or file modifications associated with the unusual child process to identify potential data exfiltration or lateral movement activities.

### False positive analysis

- Known benign processes such as gnome-keyring-daemon and abrt-dbus may trigger the rule. Users can exclude these processes by adding them to the exception list in the detection rule.
- Processes executed from common library paths like /usr/lib/ or /usr/local/lib/ are typically non-threatening. Users should review these paths and consider excluding them if they are consistently generating false positives.
- The dbus-daemon with the --session argument is generally safe. Users can ensure this argument is included in the exception criteria to prevent unnecessary alerts.
- Specific applications like software-properties-dbus and serviceHelper.py are known to be benign. Users should verify these applications' legitimacy in their environment and exclude them if they are frequently flagged.
- Regularly review and update the exception list to include any new benign processes or paths that are identified over time, ensuring the rule remains effective without generating excessive false positives.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement by the adversary.
- Terminate any suspicious child processes spawned by the dbus-daemon that are not recognized as legitimate or necessary for system operations.
- Conduct a thorough review of the affected system's logs to identify any unauthorized access or changes made by the suspicious process.
- Restore any altered or compromised system files from a known good backup to ensure system integrity.
- Update and patch the affected system and any related software to close vulnerabilities that may have been exploited.
- Implement stricter access controls and monitoring on the dbus-daemon to prevent unauthorized process execution in the future.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
