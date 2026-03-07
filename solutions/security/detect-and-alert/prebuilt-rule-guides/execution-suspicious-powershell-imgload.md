---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious PowerShell Engine ImageLoad" prebuilt detection rule.
---

# Suspicious PowerShell Engine ImageLoad

## Triage and analysis

### Investigating Suspicious PowerShell Engine ImageLoad

PowerShell is one of the main tools system administrators use for automation, report routines, and other tasks. This makes it available for use in various environments, and creates an attractive way for attackers to execute code.

Attackers can use PowerShell without having to execute `PowerShell.exe` directly. This technique, often called "PowerShell without PowerShell," works by using the underlying System.Management.Automation namespace and can bypass application allowlisting and PowerShell security features.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Investigate abnormal behaviors observed by the subject process, such as network connections, registry or file modifications, and any spawned child processes.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Inspect the host for suspicious or abnormal behavior in the alert timeframe.
- Retrieve the implementation (DLL, executable, etc.) and determine if it is malicious:
  - Use a private sandboxed malware analysis system to perform analysis.
    - Observe and collect information about the following activities:
      - Attempts to contact external domains and addresses.
      - File and registry access, modification, and creation activities.
      - Service creation and launch activities.
      - Scheduled task creation.
  - Use the PowerShell `Get-FileHash` cmdlet to get the files' SHA-256 hash values.
    - Search for the existence and reputation of the hashes in resources like VirusTotal, Hybrid-Analysis, CISCO Talos, Any.run, etc.

### False positive analysis

- This activity can happen legitimately. Some vendors have their own PowerShell implementations that are shipped with some products. These benign true positives (B-TPs) can be added as exceptions if necessary after analysis.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved hosts to prevent further post-compromise behavior.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- Remove and block malicious artifacts identified during triage.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

