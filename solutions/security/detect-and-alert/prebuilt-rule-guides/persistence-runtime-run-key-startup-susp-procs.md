---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Execution of Persistent Suspicious Program" prebuilt detection rule.
---

# Execution of Persistent Suspicious Program

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Execution of Persistent Suspicious Program

Persistent programs, like scripts or rundll32, are often used by adversaries to maintain access to a system. These programs can be executed at startup, leveraging process lineage and command line arguments to evade detection. The detection rule identifies suspicious executions by monitoring the sequence of processes initiated after user logon, focusing on known malicious executables and unusual file paths, thus highlighting potential abuse of persistence mechanisms.

### Possible investigation steps

- Review the process lineage to confirm the sequence of userinit.exe, explorer.exe, and the suspicious child process. Verify if the child process was indeed launched shortly after user logon.
- Examine the command line arguments of the suspicious process to identify any unusual or malicious patterns, especially those involving known suspicious paths like C:\Users\*, C:\ProgramData\*, or C:\Windows\Temp\*.
- Check the original file name of the suspicious process against known malicious executables such as cscript.exe, wscript.exe, or PowerShell.EXE to determine if it matches any of these.
- Investigate the parent process explorer.exe to ensure it was not compromised or manipulated to launch the suspicious child process.
- Analyze the user account associated with the suspicious process to determine if it has been involved in any other suspicious activities or if it has elevated privileges that could be exploited.
- Review recent system changes or installations that might have introduced the suspicious executable or altered startup configurations.

### False positive analysis

- Legitimate administrative scripts or tools may trigger alerts if they are executed from common directories like C:\Users or C:\ProgramData. To manage this, create exceptions for known administrative scripts that are regularly used in your environment.
- Software updates or installations might use processes like PowerShell or RUNDLL32, leading to false positives. Identify and exclude these processes when they are part of a verified update or installation routine.
- Custom scripts or automation tasks that run at startup could be flagged. Document these tasks and exclude them from the rule if they are part of normal operations.
- Security or monitoring tools that use similar execution patterns may be mistakenly identified. Verify these tools and add them to an exclusion list to prevent unnecessary alerts.
- User-initiated actions that mimic suspicious behavior, such as running scripts from the command line, can cause false positives. Educate users on safe practices and adjust the rule to exclude known benign user actions.

### Response and remediation

- Isolate the affected host from the network to prevent further spread or communication with potential command and control servers.
- Terminate any suspicious processes identified in the alert, such as those executed by cscript.exe, wscript.exe, PowerShell.EXE, MSHTA.EXE, RUNDLL32.EXE, REGSVR32.EXE, RegAsm.exe, MSBuild.exe, or InstallUtil.exe.
- Remove any unauthorized or suspicious startup entries or scheduled tasks that may have been created to ensure persistence.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious files or remnants.
- Review and restore any modified system configurations or registry settings to their default or secure state.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for the affected host and similar systems to detect any recurrence or related suspicious activities.
