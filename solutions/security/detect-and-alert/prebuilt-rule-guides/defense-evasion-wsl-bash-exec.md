---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious Execution via Windows Subsystem for Linux" prebuilt detection rule.'
---

# Suspicious Execution via Windows Subsystem for Linux

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Execution via Windows Subsystem for Linux

Windows Subsystem for Linux (WSL) allows users to run Linux binaries natively on Windows, providing a seamless integration of Linux tools. Adversaries may exploit WSL to execute Linux commands stealthily, bypassing traditional Windows security measures. The detection rule identifies unusual WSL activity by monitoring specific executable paths, command-line arguments, and parent-child process relationships, flagging deviations from typical usage patterns to uncover potential threats.

### Possible investigation steps

- Review the process command line and executable path to determine if the execution of bash.exe or any other Linux binaries is expected or authorized for the user or system in question.
- Investigate the parent-child process relationship, especially focusing on whether wsl.exe is the parent process and if it has spawned any unexpected child processes that are not wslhost.exe.
- Examine the command-line arguments used with wsl.exe for any suspicious or unauthorized commands, such as accessing sensitive files like /etc/shadow or /etc/passwd, or using network tools like curl.
- Check the user's activity history and system logs to identify any patterns of behavior that might indicate misuse or compromise, particularly focusing on any deviations from typical usage patterns.
- Correlate the alert with other security events or logs from data sources like Elastic Endgame, Microsoft Defender for Endpoint, or Sysmon to gather additional context and determine if this is part of a broader attack or isolated incident.

### False positive analysis

- Frequent use of WSL for legitimate development tasks may trigger alerts. Users can create exceptions for specific user accounts or directories commonly used for development to reduce noise.
- Automated scripts or tools that utilize WSL for system maintenance or monitoring might be flagged. Identify these scripts and whitelist their specific command-line patterns or parent processes.
- Docker-related processes may cause false positives due to their interaction with WSL. Exclude Docker executable paths from the detection rule to prevent unnecessary alerts.
- Visual Studio Code extensions that interact with WSL can generate alerts. Exclude known non-threatening extensions by specifying their command-line arguments in the exception list.
- Regular system updates or administrative tasks that involve WSL might be misidentified. Document these activities and adjust the detection rule to recognize them as benign.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified by the detection rule, such as those involving bash.exe or wsl.exe with unusual command-line arguments.
- Conduct a thorough review of the affected system's WSL configuration and installed Linux distributions to identify any unauthorized changes or installations.
- Remove any unauthorized or suspicious Linux binaries or scripts found within the WSL environment.
- Reset credentials for any accounts that may have been compromised, especially if sensitive files like /etc/shadow or /etc/passwd were accessed.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for WSL activities across the network to detect similar threats in the future, ensuring that alerts are promptly reviewed and acted upon.
