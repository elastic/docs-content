---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious WerFault Child Process" prebuilt detection rule.'
---

# Suspicious WerFault Child Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious WerFault Child Process

WerFault.exe is a Windows error reporting tool that handles application crashes. Adversaries may exploit it by manipulating the SilentProcessExit registry key to execute malicious processes stealthily. The detection rule identifies unusual child processes of WerFault.exe, focusing on specific command-line arguments indicative of this abuse, while excluding known legitimate executables, thus highlighting potential threats.

### Possible investigation steps

- Review the command line arguments of the suspicious child process to confirm the presence of "-s", "-t", and "-c" flags, which indicate potential abuse of the SilentProcessExit mechanism.
- Examine the process executable path to ensure it is not one of the known legitimate executables ("?:\Windows\SysWOW64\Initcrypt.exe", "?:\Program Files (x86)\Heimdal\Heimdal.Guard.exe") that are excluded from the detection rule.
- Investigate the network connections established by the suspicious process to identify any unusual or unauthorized external communications.
- Analyze file writes and modifications made by the process to detect any unauthorized changes or potential indicators of compromise.
- Check the parent process tree to understand the context of how WerFault.exe was invoked and identify any preceding suspicious activities or processes.
- Correlate the event with other security alerts or logs from data sources like Elastic Endgame, Elastic Defend, Microsoft Defender for Endpoint, Sysmon, or SentinelOne to gather additional context and assess the scope of the potential threat.

### False positive analysis

- Legitimate software updates or installations may trigger WerFault.exe with command-line arguments similar to those used in the SilentProcessExit mechanism. Users should verify the digital signature of the executable and check if it aligns with known update processes.
- Security software or system management tools might use WerFault.exe for legitimate purposes. Users can create exceptions for these known tools by adding their executables to the exclusion list in the detection rule.
- Custom scripts or enterprise applications that utilize WerFault.exe for error handling could be flagged. Review the process details and, if verified as non-threatening, add these scripts or applications to the exclusion list.
- Frequent occurrences of the same process being flagged can indicate a benign pattern. Users should monitor these patterns and, if consistently verified as safe, update the rule to exclude these specific processes.

### Response and remediation

- Isolate the affected system from the network to prevent further potential malicious activity and lateral movement.
- Terminate the suspicious child process of WerFault.exe immediately to halt any ongoing malicious actions.
- Conduct a thorough review of the SilentProcessExit registry key to identify and remove any unauthorized entries that may have been used to execute the malicious process.
- Restore any altered or deleted files from a known good backup to ensure system integrity and recover any lost data.
- Update and run a full antivirus and anti-malware scan on the affected system to detect and remove any additional threats or remnants of the attack.
- Monitor network traffic and system logs for any signs of persistence mechanisms or further attempts to exploit the SilentProcessExit mechanism.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
