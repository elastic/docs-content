---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Explorer Child Process" prebuilt detection rule.
---

# Suspicious Explorer Child Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Explorer Child Process

Windows Explorer, a core component of the Windows OS, manages file and folder navigation. Adversaries exploit its trusted status to launch malicious scripts or executables, often using DCOM to start processes like PowerShell or cmd.exe. The detection rule identifies such anomalies by monitoring child processes of Explorer with specific characteristics, excluding known benign activities, to flag potential threats.

### Possible investigation steps

- Review the process details to confirm the suspicious child process was indeed started by explorer.exe with the specific parent arguments indicating DCOM usage, such as "-Embedding".
- Check the process command line arguments and execution context to identify any potentially malicious scripts or commands being executed by the child process.
- Investigate the parent process explorer.exe to determine if it was started by a legitimate user action or if there are signs of compromise, such as unusual user activity or recent phishing attempts.
- Correlate the event with other security logs or alerts from data sources like Microsoft Defender for Endpoint or Sysmon to identify any related suspicious activities or patterns.
- Examine the network activity associated with the suspicious process to detect any unauthorized data exfiltration or communication with known malicious IP addresses.
- Assess the system for any additional indicators of compromise, such as unexpected changes in system files or registry keys, which might suggest a broader attack.

### False positive analysis

- Legitimate software installations or updates may trigger the rule when they use scripts or executables like PowerShell or cmd.exe. Users can create exceptions for known software update processes by identifying their specific command-line arguments or parent process details.
- System administrators often use scripts for maintenance tasks that might be flagged by this rule. To prevent false positives, administrators should document and exclude these routine scripts by specifying their unique process arguments or execution times.
- Some enterprise applications may use DCOM to launch processes for legitimate purposes. Users should identify these applications and exclude their specific process signatures or parent-child process relationships from the rule.
- Automated testing environments might execute scripts or commands that resemble suspicious activity. Users can mitigate false positives by excluding processes that are part of known testing frameworks or environments.
- Certain security tools or monitoring software may use similar techniques to gather system information. Users should verify and exclude these tools by confirming their process names and execution patterns.

### Response and remediation

- Isolate the affected system from the network to prevent further spread of the potential threat and to contain any malicious activity.
- Terminate the suspicious child process identified in the alert, such as cscript.exe, wscript.exe, powershell.exe, rundll32.exe, cmd.exe, mshta.exe, or regsvr32.exe, to stop any ongoing malicious actions.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious files or processes.
- Review and analyze the parent process explorer.exe and its command-line arguments to understand how the malicious process was initiated and to identify any potential persistence mechanisms.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if the threat is part of a larger attack campaign.
- Implement additional monitoring and alerting for similar suspicious activities involving explorer.exe to enhance detection capabilities and prevent recurrence.
- Review and update endpoint security policies to restrict the execution of potentially malicious scripts or executables from explorer.exe, especially when initiated via DCOM.
