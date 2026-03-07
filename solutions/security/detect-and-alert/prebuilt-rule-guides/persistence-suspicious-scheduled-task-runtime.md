---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious Execution via Scheduled Task" prebuilt detection rule.'
---

# Suspicious Execution via Scheduled Task

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Execution via Scheduled Task

Scheduled tasks in Windows automate routine tasks, but adversaries exploit them for persistence and execution of malicious programs. By examining process lineage and command line usage, the detection rule identifies suspicious executions initiated by scheduled tasks. It flags known malicious executables and unusual file paths, while excluding benign processes, to pinpoint potential threats effectively.

### Possible investigation steps

- Review the process lineage to confirm the parent process is "svchost.exe" with arguments containing "Schedule" to verify the execution was initiated by a scheduled task.
- Examine the command line arguments and file paths of the suspicious process to identify any unusual or unauthorized file locations, such as those listed in the query (e.g., "C:\Users\*", "C:\ProgramData\*").
- Check the original file name of the process against the list of known suspicious executables (e.g., "PowerShell.EXE", "Cmd.Exe") to determine if it matches any commonly abused binaries.
- Investigate the user context under which the process was executed, especially if it deviates from expected system accounts or known service accounts.
- Correlate the event with other security logs or alerts to identify any related suspicious activities or patterns that might indicate a broader attack campaign.
- Assess the risk and impact of the detected activity by considering the severity and risk score provided, and determine if immediate containment or remediation actions are necessary.

### False positive analysis

- Scheduled tasks running legitimate scripts or executables like cmd.exe or cscript.exe in system directories may trigger false positives. To manage this, create exceptions for these processes when they are executed from known safe directories such as C:\Windows\System32.
- PowerShell scripts executed by the system account (S-1-5-18) for administrative tasks can be mistakenly flagged. Exclude these by specifying exceptions for PowerShell executions with arguments like -File or -PSConsoleFile when run by the system account.
- Legitimate software installations or updates using msiexec.exe by the system account may be incorrectly identified as threats. Mitigate this by excluding msiexec.exe processes initiated by the system account.
- Regular maintenance tasks or scripts stored in common directories like C:\ProgramData or C:\Windows\Temp might be flagged. Review these tasks and exclude known benign scripts or executables from these paths.
- Custom scripts or administrative tools that mimic suspicious executables (e.g., PowerShell.EXE, RUNDLL32.EXE) but are part of routine operations should be reviewed and excluded if verified as safe.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further spread of any potential malicious activity.
- Terminate any suspicious processes identified by the detection rule, especially those matching the flagged executables and paths.
- Conduct a thorough review of scheduled tasks on the affected system to identify and disable any unauthorized or suspicious tasks.
- Remove any malicious files or executables found in the suspicious paths listed in the detection rule.
- Restore the system from a known good backup if malicious activity is confirmed and system integrity is compromised.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for scheduled tasks and the flagged executables to detect similar threats in the future.
