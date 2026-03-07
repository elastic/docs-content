---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "UAC Bypass Attempt via Privileged IFileOperation COM Interface" prebuilt detection rule.'
---

# UAC Bypass Attempt via Privileged IFileOperation COM Interface

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating UAC Bypass Attempt via Privileged IFileOperation COM Interface

The IFileOperation COM interface is a Windows component used for file operations with elevated privileges. Adversaries exploit this by side-loading malicious DLLs into processes like dllhost.exe, bypassing UAC to gain elevated permissions stealthily. The detection rule identifies such attempts by monitoring changes in specific DLLs loaded into high-integrity processes, filtering out benign system paths to reduce false positives.

### Possible investigation steps

- Review the alert details to confirm the process name is "dllhost.exe" and verify the integrity level of the process to ensure it is running with high or system integrity.
- Check the file name involved in the alert to see if it matches any of the known malicious DLLs such as "wow64log.dll", "comctl32.dll", "DismCore.dll", "OskSupport.dll", "duser.dll", or "Accessibility.ni.dll".
- Investigate the file path of the loaded DLL to ensure it does not originate from benign system paths like "C:\Windows\SoftwareDistribution\" or "C:\Windows\WinSxS\".
- Analyze the parent process of "dllhost.exe" to determine how it was initiated and whether it aligns with expected behavior or indicates potential compromise.
- Review recent system changes or installations that might have introduced the suspicious DLL, focusing on any unauthorized or unexpected software installations.
- Correlate the event with other security logs or alerts from data sources such as Elastic Endgame, Elastic Defend, Sysmon, Microsoft Defender for Endpoint, or SentinelOne to identify any related suspicious activities or patterns.
- Assess the risk and impact of the potential UAC bypass attempt and determine if further containment or remediation actions are necessary.

### False positive analysis

- System updates and installations can trigger false positives due to legitimate changes in DLLs. Exclude paths related to Windows updates and installations, such as C:\Windows\SoftwareDistribution\* and C:\Windows\WinSxS\*.
- Certain legitimate software may use DLLs like comctl32.dll or duser.dll in a manner that mimics side-loading. Identify and whitelist these applications if they are known and trusted within your environment.
- Security software or system management tools might perform operations that resemble UAC bypass attempts. Review and exclude these tools if they are verified as safe and necessary for your operations.
- Regularly review and update the list of known benign DLLs and paths to ensure that new legitimate software does not trigger false positives.
- Monitor for patterns of repeated false positives from specific processes or paths and consider creating exceptions for these scenarios after thorough validation.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or lateral movement.
- Terminate the dllhost.exe process if it is confirmed to be involved in the UAC bypass attempt to stop any ongoing malicious activity.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any malicious DLLs or associated malware.
- Review and restore any modified system files or settings to their original state to ensure system integrity.
- Apply any pending security patches and updates to the operating system and installed software to mitigate known vulnerabilities.
- Monitor the network for any signs of similar activity or attempts to exploit the IFileOperation COM interface on other systems.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
