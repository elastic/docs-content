---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Print Spooler Child Process" prebuilt detection rule.'
---

# Unusual Print Spooler Child Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Print Spooler Child Process

The Print Spooler service, integral to Windows environments, manages print jobs and interactions with printers. Adversaries may exploit vulnerabilities in this service to escalate privileges, gaining unauthorized access or control. The detection rule identifies suspicious child processes spawned by the Print Spooler, excluding known legitimate processes, to flag potential exploitation attempts, focusing on unusual command lines and integrity levels.

### Possible investigation steps

- Review the process details to identify the unusual child process spawned by spoolsv.exe, focusing on the process name and command line arguments to understand its purpose and potential malicious intent.
- Check the integrity level of the process using the fields process.Ext.token.integrity_level_name or winlog.event_data.IntegrityLevel to confirm if it is running with elevated privileges, which could indicate an exploitation attempt.
- Investigate the parent-child relationship by examining the process tree to determine if there are any other suspicious processes associated with the same parent process, spoolsv.exe.
- Cross-reference the process executable path against known legitimate software paths to ensure it is not a false positive, especially if the executable is not listed in the exclusion paths.
- Analyze recent system logs and security events around the time of the alert to identify any other anomalous activities or patterns that could be related to the potential exploitation attempt.
- If the process is confirmed suspicious, isolate the affected system to prevent further exploitation and conduct a deeper forensic analysis to understand the scope and impact of the incident.

### False positive analysis

- Legitimate print-related processes like splwow64.exe, PDFCreator.exe, and acrodist.exe may trigger alerts. These are excluded in the rule to prevent false positives.
- System processes such as msiexec.exe, route.exe, and WerFault.exe are known to be legitimate child processes of the Print Spooler and are excluded to reduce false alerts.
- Commands involving net.exe for starting or stopping services are common in administrative tasks and are excluded to avoid unnecessary alerts.
- Command-line operations involving cmd.exe or powershell.exe that reference .spl files or system paths are often legitimate and are excluded to minimize false positives.
- Network configuration changes using netsh.exe, such as adding port openings or rules, are typical in network management and are excluded to prevent false alerts.
- Registration of PrintConfig.dll via regsvr32.exe is a known legitimate operation and is excluded to avoid false positives.
- Executables from known paths like CutePDF Writer and GPLGS are excluded to prevent alerts from common, non-threatening applications.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further exploitation or lateral movement by the adversary.
- Terminate any suspicious child processes spawned by the Print Spooler service that do not match known legitimate processes or command lines.
- Conduct a thorough review of the system's security logs to identify any unauthorized access or privilege escalation attempts related to the Print Spooler service.
- Apply the latest security patches and updates to the Windows operating system and specifically to the Print Spooler service to mitigate known vulnerabilities.
- Restore the system from a clean backup if any unauthorized changes or malicious activities are confirmed.
- Monitor the system closely for any recurrence of similar suspicious activities, ensuring enhanced logging and alerting are in place for spoolsv.exe and its child processes.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on other systems within the network.
