---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Microsoft Diagnostics Wizard Execution" prebuilt detection rule.
---

# Suspicious Microsoft Diagnostics Wizard Execution

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Microsoft Diagnostics Wizard Execution

The Microsoft Diagnostics Troubleshooting Wizard (MSDT) is a legitimate tool used for diagnosing and resolving issues within Windows environments. However, adversaries can exploit MSDT to execute malicious commands by manipulating its process arguments, effectively using it as a proxy for harmful activities. The detection rule identifies such abuse by monitoring for unusual execution patterns, such as atypical file paths, unexpected parent processes, and non-standard executable locations, which are indicative of potential misuse. This proactive detection helps in mitigating risks associated with defense evasion tactics.

### Possible investigation steps

- Review the process arguments to identify any suspicious patterns, such as "IT_RebrowseForFile=*", "ms-msdt:/id", "ms-msdt:-id", or "*FromBase64*", which may indicate malicious intent.
- Examine the parent process of msdt.exe to determine if it was launched by an unexpected or potentially malicious process like cmd.exe, powershell.exe, or mshta.exe.
- Check the file path of the msdt.exe executable to ensure it matches the standard locations (?:\Windows\system32\msdt.exe or ?:\Windows\SysWOW64\msdt.exe) and investigate any deviations.
- Investigate the user account associated with the process execution to determine if the activity aligns with their typical behavior or if it appears suspicious.
- Correlate the event with other security alerts or logs from data sources like Microsoft Defender for Endpoint or Sysmon to identify any related malicious activities or patterns.
- Assess the risk score and severity of the alert to prioritize the investigation and determine if immediate action is required to mitigate potential threats.

### False positive analysis

- Legitimate troubleshooting activities by IT staff using MSDT may trigger alerts. To manage this, create exceptions for known IT user accounts or specific machines frequently used for diagnostics.
- Automated scripts or software updates that utilize MSDT for legitimate purposes can cause false positives. Identify these scripts and whitelist their execution paths or parent processes.
- Custom diagnostic tools that leverage MSDT might be flagged. Review these tools and exclude their specific process arguments or executable paths if they are verified as safe.
- Non-standard installations of MSDT in custom environments could be misidentified. Ensure that any legitimate non-standard paths are documented and excluded from monitoring.
- Frequent use of MSDT in virtualized environments for testing purposes may lead to alerts. Consider excluding these environments or specific virtual machines from the rule.

### Response and remediation

- Isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate the suspicious msdt.exe process to stop any ongoing malicious execution.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious files or processes.
- Review and analyze the process arguments and parent processes associated with the msdt.exe execution to identify potential entry points or related malicious activities.
- Restore any affected files or system components from a known good backup to ensure system integrity.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are compromised.
- Implement enhanced monitoring and logging for msdt.exe and related processes to detect and respond to similar threats in the future.
