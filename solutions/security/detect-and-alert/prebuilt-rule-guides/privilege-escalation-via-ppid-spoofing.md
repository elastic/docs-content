---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Privileges Elevation via Parent Process PID Spoofing" prebuilt detection rule.
---

# Privileges Elevation via Parent Process PID Spoofing

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Privileges Elevation via Parent Process PID Spoofing

Parent Process ID (PPID) spoofing is a technique where adversaries manipulate the PPID of a process to disguise its origin, often to bypass security measures or gain elevated privileges. This is particularly concerning in Windows environments where processes can inherit permissions from their parent. The detection rule identifies suspicious process creation patterns, such as unexpected PPID values and elevated user IDs, while filtering out known legitimate processes and trusted signatures, to flag potential privilege escalation attempts.

### Possible investigation steps

- Review the process creation event details, focusing on the process.parent.Ext.real.pid and user.id fields to confirm if the PPID spoofing led to privilege escalation to SYSTEM.
- Examine the process.executable and process.parent.executable paths to determine if the process is known or expected in the environment, and check against the list of excluded legitimate processes.
- Investigate the process.code_signature fields to verify if the process is signed by a trusted entity and if the signature is valid, especially if the process is not excluded by the rule.
- Check the historical activity of the involved user.id and process.parent.executable to identify any unusual patterns or recent changes in behavior.
- Correlate the alert with other security events or logs to identify any related suspicious activities or potential lateral movement attempts within the network.

### False positive analysis

- Processes related to Windows Error Reporting such as WerFault.exe and Wermgr.exe can trigger false positives. These are legitimate system processes and can be excluded by verifying their signatures and paths.
- Logon utilities like Utilman.exe spawning processes such as osk.exe, Narrator.exe, or Magnify.exe may appear suspicious but are often legitimate. Exclude these by confirming their usage context and ensuring they are executed by trusted users.
- Third-party software like TeamViewer, Cisco WebEx, and Dell Inc. may cause false positives due to their legitimate use of process creation. Verify the code signature and trust status to exclude these processes.
- Windows Update processes involving MpSigStub.exe and wuauclt.exe can be mistakenly flagged. Confirm these are part of regular update activities and exclude them based on their known paths and parent processes.
- Remote support and management tools such as LogMeIn, GoToAssist, and Chrome Remote Desktop may be flagged. Ensure these are installed and used by authorized personnel and exclude them by their executable paths.
- Netwrix Corporation's processes like adcrcpy.exe may be flagged if they are part of legitimate auditing activities. Verify the code signature and exclude these processes if they are part of authorized Netwrix Auditor operations.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes identified by the alert, especially those with spoofed PPIDs or elevated privileges, to stop potential malicious activities.
- Review and revoke any unauthorized user accounts or privileges that may have been created or escalated during the incident.
- Conduct a thorough forensic analysis of the affected system to identify any additional indicators of compromise or persistence mechanisms.
- Restore the system from a known good backup if necessary, ensuring that all malicious artifacts are removed and system integrity is maintained.
- Implement additional monitoring and logging on the affected system and network to detect any recurrence of similar activities.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if broader organizational impacts exist.
