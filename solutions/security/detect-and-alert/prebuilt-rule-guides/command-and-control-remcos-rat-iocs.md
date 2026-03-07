---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential REMCOS Trojan Execution" prebuilt detection rule.'
---

# Potential REMCOS Trojan Execution

## Triage and analysis

### Investigating Potential REMCOS Trojan Execution

Remcos RAT is used by attackers to perform actions on infected machines remotely.

### Possible investigation steps

- Review the origin of the REMCOS file and the execution chain to identify the initial vector..
- Examine if the process is set to persist in the affected system via scheduled task, Startup folder or Run key.
- Check the network, files and child processes activity associated with the every suspicious process in the execution chain of REMCOS.
- Correlate the event with other security alerts or logs from data sources like Elastic Defend or Microsoft Defender for Endpoint to gather additional context and identify any related malicious activities.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the attacker.
- Terminate any suspicious processes identified in the alert, such as PowerShell, cmd.exe, or other flagged executables, to halt any ongoing malicious activity.
- Review and revoke any unauthorized user accounts or privileges that may have been created or modified using tools like net.exe or schtasks.exe.
- Conduct a thorough scan of the affected system using endpoint protection tools to identify and remove any malware or unauthorized software installed by the attacker.
- Restore the system from a known good backup if any critical system files or configurations have been altered or compromised.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for ScreenConnect and other remote access tools to detect similar activities in the future, ensuring that alerts are promptly reviewed and acted upon.
