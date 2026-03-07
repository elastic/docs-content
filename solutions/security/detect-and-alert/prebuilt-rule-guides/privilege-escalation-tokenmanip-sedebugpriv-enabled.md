---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "SeDebugPrivilege Enabled by a Suspicious Process" prebuilt detection rule.
---

# SeDebugPrivilege Enabled by a Suspicious Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating SeDebugPrivilege Enabled by a Suspicious Process

SeDebugPrivilege is a powerful Windows privilege allowing processes to debug and modify other processes, typically reserved for system-level tasks. Adversaries exploit this to escalate privileges, bypassing security controls by impersonating system processes. The detection rule identifies suspicious processes enabling SeDebugPrivilege, excluding known legitimate processes, to flag potential privilege escalation attempts.

### Possible investigation steps

- Review the event logs for the specific event.provider "Microsoft-Windows-Security-Auditing" and event.action "Token Right Adjusted Events" to gather more details about the process that enabled SeDebugPrivilege.
- Identify the process name from winlog.event_data.ProcessName and determine if it is known or expected in the environment. Investigate any unknown or suspicious processes.
- Check the winlog.event_data.SubjectUserSid to identify the user account associated with the process. Investigate if this account has a history of suspicious activity or if it should have the ability to enable SeDebugPrivilege.
- Analyze the parent process of the suspicious process to understand how it was initiated and if it was spawned by a legitimate or malicious process.
- Correlate the timestamp of the event with other security events or alerts to identify any related activities or patterns that could indicate a broader attack or compromise.
- Investigate the network activity of the suspicious process to determine if it is communicating with any known malicious IP addresses or domains.

### False positive analysis

- Legitimate system maintenance tasks may trigger the rule, such as Windows Update or system diagnostics. Users can monitor the timing of these tasks and correlate them with alerts to determine if they are the cause.
- Software installations or updates using msiexec.exe might be flagged. Consider excluding msiexec.exe from the rule if it is frequently used in your environment for legitimate purposes.
- Administrative tools like taskhostw.exe and mmc.exe can sometimes enable SeDebugPrivilege during normal operations. Evaluate the necessity of these tools in your environment and exclude them if they are regularly used by trusted administrators.
- Temporary files created by legitimate applications, such as DismHost.exe in user temp directories, may be flagged. Review the context of these files and exclude them if they are part of routine application behavior.
- Regularly review and update the exclusion list to include any new legitimate processes that are identified as false positives, ensuring the rule remains effective without generating unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate the suspicious process identified in the alert to stop any ongoing malicious activity and prevent privilege escalation.
- Conduct a thorough review of the affected system's event logs, focusing on the "Token Right Adjusted Events" to identify any additional unauthorized privilege changes or suspicious activities.
- Reset credentials for any accounts that may have been compromised or used by the suspicious process, especially those with elevated privileges.
- Restore the affected system from a known good backup to ensure any malicious changes are removed and the system is returned to a secure state.
- Implement additional monitoring on the affected system and similar systems to detect any recurrence of the threat, focusing on processes attempting to enable SeDebugPrivilege.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
