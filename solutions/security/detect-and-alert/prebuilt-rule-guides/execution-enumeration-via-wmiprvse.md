---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Enumeration Command Spawned via WMIPrvSE" prebuilt detection rule.'
---

# Enumeration Command Spawned via WMIPrvSE

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Enumeration Command Spawned via WMIPrvSE

Windows Management Instrumentation (WMI) is a powerful framework for managing data and operations on Windows systems. Adversaries exploit WMI to execute enumeration commands stealthily, leveraging the WMI Provider Service (WMIPrvSE) to gather system and network information. The detection rule identifies suspicious command executions initiated by WMIPrvSE, focusing on common enumeration tools while excluding benign use cases, thus highlighting potential malicious activity.

### Possible investigation steps

- Review the process command line details to understand the specific enumeration command executed and its arguments, focusing on the process.command_line field.
- Investigate the parent process to confirm it is indeed WMIPrvSE by examining the process.parent.name field, ensuring the execution context aligns with potential misuse of WMI.
- Check the user context under which the process was executed to determine if it aligns with expected administrative activity or if it suggests unauthorized access.
- Correlate the event with other logs or alerts from the same host to identify any preceding or subsequent suspicious activities, such as lateral movement or privilege escalation attempts.
- Assess the network activity from the host around the time of the alert to identify any unusual outbound connections or data exfiltration attempts.
- Verify if the process execution is part of a known and legitimate administrative task or script by consulting with system administrators or reviewing change management records.

### False positive analysis

- Routine administrative tasks using WMI may trigger the rule, such as network configuration checks or system diagnostics. To manage this, identify and exclude specific command patterns or arguments that are part of regular maintenance.
- Security tools like Tenable may use WMI for legitimate scans, which can be mistaken for malicious activity. Exclude processes with arguments related to known security tools, such as "tenable_mw_scan".
- Automated scripts or scheduled tasks that perform system enumeration for inventory or monitoring purposes can cause false positives. Review and whitelist these scripts by excluding their specific command lines or parent processes.
- Certain enterprise applications may use WMI for legitimate operations, such as querying system information. Identify these applications and create exceptions based on their process names or command line arguments.
- Regular use of network utilities by IT staff for troubleshooting can be flagged. Implement exclusions for known IT user accounts or specific command line patterns used during these activities.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified as being spawned by WMIPrvSE, especially those matching the enumeration tools listed in the detection query.
- Conduct a thorough review of recent WMI activity on the affected system to identify any additional unauthorized or suspicious commands executed.
- Reset credentials for any accounts that may have been compromised or used in the suspicious activity to prevent further unauthorized access.
- Restore the system from a known good backup if any malicious activity is confirmed and cannot be remediated through other means.
- Implement additional monitoring on the affected system and network to detect any recurrence of similar suspicious activities.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if the threat has spread to other systems.
