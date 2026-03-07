---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Execution via Windows Subsystem for Linux" prebuilt detection rule.
---

# Execution via Windows Subsystem for Linux

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Execution via Windows Subsystem for Linux

Windows Subsystem for Linux (WSL) allows users to run Linux binaries natively on Windows, providing a seamless integration of Linux tools. Adversaries may exploit WSL to execute malicious scripts or binaries, bypassing traditional Windows security mechanisms. The detection rule identifies suspicious executions initiated by WSL processes, excluding known safe executables, to flag potential misuse for defense evasion.

### Possible investigation steps

- Review the process details to identify the executable path and determine if it matches any known malicious or suspicious binaries not listed in the safe executables.
- Investigate the parent process, specifically wsl.exe or wslhost.exe, to understand how the execution was initiated and if it aligns with expected user behavior or scheduled tasks.
- Check the user account associated with the process execution to verify if the activity is consistent with the user's typical behavior or if the account may have been compromised.
- Analyze the event dataset, especially if it is from crowdstrike.fdr, to gather additional context about the process execution and any related activities on the host.
- Correlate the alert with other security events or logs from data sources like Microsoft Defender for Endpoint or SentinelOne to identify any related suspicious activities or patterns.
- Assess the risk score and severity in the context of the organization's environment to prioritize the investigation and response actions accordingly.

### False positive analysis

- Legitimate administrative tasks using WSL may trigger alerts. Users can create exceptions for known administrative scripts or binaries that are frequently executed via WSL.
- Development environments often use WSL for compiling or testing code. Exclude specific development tools or scripts that are regularly used by developers to prevent unnecessary alerts.
- Automated system maintenance scripts running through WSL can be mistaken for malicious activity. Identify and whitelist these scripts to reduce false positives.
- Security tools or monitoring solutions that leverage WSL for legitimate purposes should be identified and excluded from detection to avoid interference with their operations.
- Frequent use of WSL by specific users or groups for non-malicious purposes can be managed by creating user-based exceptions, allowing their activities to proceed without triggering alerts.

### Response and remediation

- Isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious processes identified as being executed via WSL that are not part of the known safe executables list.
- Conduct a thorough review of the affected system's WSL configuration and installed Linux distributions to identify unauthorized changes or installations.
- Remove any unauthorized or malicious scripts and binaries found within the WSL environment.
- Restore the system from a known good backup if malicious activity has compromised system integrity.
- Update and patch the system to ensure all software, including WSL, is up to date to mitigate known vulnerabilities.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
