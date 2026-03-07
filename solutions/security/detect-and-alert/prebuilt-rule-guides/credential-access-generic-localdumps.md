---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Full User-Mode Dumps Enabled System-Wide" prebuilt detection rule.'
---

# Full User-Mode Dumps Enabled System-Wide

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Full User-Mode Dumps Enabled System-Wide

Full user-mode dumps are a diagnostic feature in Windows that captures detailed information about application crashes, aiding in troubleshooting. However, attackers can exploit this by triggering dumps of sensitive processes like LSASS to extract credentials. The detection rule identifies registry changes enabling this feature system-wide, flagging potential misuse by excluding legitimate system processes, thus alerting analysts to suspicious activity.

### Possible investigation steps

- Review the registry path HKLM\SOFTWARE\Microsoft\Windows\Windows Error Reporting\LocalDumps\DumpType to confirm if the value is set to "2" or "0x00000002", indicating full user-mode dumps are enabled.
- Check for any recent changes to the registry key by examining the modification timestamps and identifying the user or process responsible for the change.
- Investigate the context of the alert by reviewing recent process execution logs to identify any suspicious processes that may have triggered the dump, especially those not matching the legitimate svchost.exe process with user IDs S-1-5-18, S-1-5-19, or S-1-5-20.
- Analyze any generated dump files for sensitive information, such as credentials, and determine if they were accessed or exfiltrated by unauthorized users or processes.
- Correlate the alert with other security events or logs, such as Sysmon or Microsoft Defender for Endpoint, to identify any related suspicious activities or patterns that could indicate a broader attack.

### False positive analysis

- Legitimate system processes like svchost.exe may trigger the rule if they are not properly excluded. Ensure that the exclusion for svchost.exe is correctly configured by verifying the process executable path and user IDs.
- Custom applications that require full user-mode dumps for legitimate debugging purposes might be flagged. Identify these applications and create specific registry subkey exclusions to prevent false positives.
- System administrators performing routine maintenance or diagnostics might enable full user-mode dumps temporarily. Document these activities and consider creating temporary exceptions during maintenance windows.
- Security tools or monitoring software that simulate crash scenarios for testing purposes could trigger the rule. Verify the legitimacy of these tools and add them to an exclusion list if they are part of regular security operations.
- Updates or patches from software vendors that modify registry settings for error reporting might be misinterpreted as suspicious. Monitor update schedules and correlate any rule triggers with known update activities to avoid unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further credential access or lateral movement by the attacker.
- Terminate any unauthorized processes that are generating full user-mode dumps, especially those related to LSASS, to stop further credential dumping.
- Conduct a thorough review of the registry settings on the affected system to ensure that the full user-mode dumps feature is disabled unless explicitly required for legitimate purposes.
- Change all credentials that may have been exposed, particularly those associated with high-privilege accounts, to mitigate the risk of unauthorized access.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and alerting for similar registry changes across the network to detect and respond to future attempts promptly.
- Review and update endpoint protection configurations to ensure they are capable of detecting and blocking similar credential dumping techniques.
