---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Attempt to Install Kali Linux via WSL" prebuilt detection rule.'
---

# Attempt to Install Kali Linux via WSL

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Attempt to Install Kali Linux via WSL

Windows Subsystem for Linux (WSL) allows users to run Linux distributions on Windows, providing a seamless integration of Linux tools. Adversaries may exploit WSL to install Kali Linux, a penetration testing distribution, to evade detection by traditional Windows security tools. The detection rule identifies suspicious processes and file paths associated with Kali Linux installations, flagging potential misuse for defense evasion.

### Possible investigation steps

- Review the process details to confirm the presence of "wsl.exe" with arguments indicating an attempt to install or use Kali Linux, such as "-d", "--distribution", "-i", or "--install".
- Check the file paths associated with the Kali Linux installation, such as "?:\Users\*\AppData\Local\packages\kalilinux*" or "?:\Program Files*\WindowsApps\KaliLinux.*\kali.exe", to verify if the installation files exist on the system.
- Investigate the user account associated with the process to determine if the activity aligns with their typical behavior or if it appears suspicious.
- Correlate the event with other security logs or alerts from data sources like Microsoft Defender for Endpoint or Sysmon to identify any related suspicious activities or patterns.
- Assess the risk and impact of the detected activity by considering the context of the environment and any potential threats posed by the use of Kali Linux on the system.

### False positive analysis

- Legitimate use of Kali Linux for development or educational purposes may trigger the rule. Users can create exceptions for specific user accounts or groups known to use Kali Linux for authorized activities.
- Automated scripts or deployment tools that install or configure Kali Linux as part of a legitimate IT process might be flagged. Consider whitelisting these scripts or processes by their hash or path.
- Security researchers or IT professionals conducting penetration testing on a Windows machine may cause false positives. Implement user-based exclusions for these professionals to prevent unnecessary alerts.
- System administrators testing WSL features with various Linux distributions, including Kali, could inadvertently trigger the rule. Establish a policy to document and approve such activities, then exclude them from detection.
- Training environments where Kali Linux is used to teach cybersecurity skills might be mistakenly flagged. Set up environment-specific exclusions to avoid disrupting educational activities.

### Response and remediation

- Immediately isolate the affected system from the network to prevent any potential lateral movement or data exfiltration.
- Terminate any suspicious processes related to the Kali Linux installation attempt, specifically those involving `wsl.exe` with arguments indicating a Kali distribution.
- Remove any unauthorized installations of Kali Linux by deleting associated files and directories, such as those found in `AppData\\Local\\packages\\kalilinux*` or `Program Files*\\WindowsApps\\KaliLinux.*`.
- Conduct a thorough review of user accounts and permissions on the affected system to ensure no unauthorized access or privilege escalation has occurred.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement additional monitoring and alerting for similar activities across the network, focusing on WSL usage and installation attempts of known penetration testing tools.
- Review and update endpoint protection configurations to enhance detection and prevention capabilities against similar threats, leveraging data sources like Microsoft Defender for Endpoint and Sysmon.
