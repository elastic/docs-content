---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Scheduled Tasks AT Command Enabled" prebuilt detection rule.'
---

# Scheduled Tasks AT Command Enabled

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Scheduled Tasks AT Command Enabled

The AT command, a legacy Windows utility, schedules tasks for execution, often used for automation. Despite its deprecation post-Windows 8, it remains for compatibility, posing a security risk. Attackers exploit it to maintain persistence or move laterally. The detection rule monitors registry changes enabling this command, flagging potential misuse by checking specific registry paths and values indicative of enabling the AT command.

### Possible investigation steps

- Review the registry event logs to confirm the change in the registry path "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\Configuration\EnableAt" and verify if the value was set to "1" or "0x00000001".
- Identify the user account and process responsible for the registry change by examining the event logs for associated user and process information.
- Check for any scheduled tasks created or modified around the time of the registry change to determine if the AT command was used to schedule any tasks.
- Investigate the system for any signs of lateral movement or persistence mechanisms that may have been established using the AT command.
- Correlate the event with other security alerts or logs from data sources like Elastic Endgame, Elastic Defend, Sysmon, Microsoft Defender for Endpoint, or SentinelOne to gather additional context and assess the scope of potential malicious activity.

### False positive analysis

- System administrators or IT management tools may enable the AT command for legacy support or compatibility testing. Verify if the change aligns with scheduled maintenance or updates.
- Some enterprise environments might have legacy applications that rely on the AT command for task scheduling. Confirm with application owners if such dependencies exist and document them.
- Security software or monitoring tools might trigger registry changes as part of their normal operation. Cross-reference with logs from these tools to ensure the change is benign.
- If a specific user or system frequently triggers this alert without malicious intent, consider creating an exception for that user or system in your monitoring solution to reduce noise.
- Regularly review and update the list of exceptions to ensure they remain relevant and do not inadvertently allow malicious activity.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further lateral movement or persistence by the attacker.
- Review the registry changes identified in the alert to confirm unauthorized enabling of the AT command. Revert the registry setting to its secure state by setting the value to "0" or "0x00000000".
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious software or scripts.
- Investigate user accounts and permissions on the affected system to ensure no unauthorized accounts or privilege escalations have occurred. Reset passwords for any compromised accounts.
- Monitor network traffic and logs for any signs of data exfiltration or communication with known malicious IP addresses or domains.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
- Implement enhanced monitoring and alerting for similar registry changes across the network to detect and respond to future attempts promptly.
