---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Windows Script Executing PowerShell" prebuilt detection rule.
---

# Windows Script Executing PowerShell

## Triage and analysis

### Investigating Windows Script Executing PowerShell

The Windows Script Host (WSH) is an Windows automation technology, which is ideal for non-interactive scripting needs, such as logon scripting, administrative scripting, and machine automation.

Attackers commonly use WSH scripts as their initial access method, acting like droppers for second stage payloads, but can also use them to download tools and utilities needed to accomplish their goals.

This rule looks for the spawn of the `powershell.exe` process with `cscript.exe` or `wscript.exe` as its parent process.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Investigate commands executed by the spawned PowerShell process.
- If unsigned files are found on the process tree, retrieve them and determine if they are malicious:
  - Use a private sandboxed malware analysis system to perform analysis.
    - Observe and collect information about the following activities:
      - Attempts to contact external domains and addresses.
      - File and registry access, modification, and creation activities.
      - Service creation and launch activities.
      - Scheduled task creation.
  - Use the PowerShell Get-FileHash cmdlet to get the files' SHA-256 hash values.
    - Search for the existence and reputation of the hashes in resources like VirusTotal, Hybrid-Analysis, CISCO Talos, Any.run, etc.
- Determine how the script file was delivered (email attachment, dropped by other processes, etc.).
- Investigate other alerts associated with the user/host during the past 48 hours.

### False positive analysis

- The usage of these script engines by regular users is unlikely. In the case of authorized benign true positives (B-TPs), exceptions can be added.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- Remove and block malicious artifacts identified during triage.
- If the malicious file was delivered via phishing:
  - Block the email sender from sending future emails.
  - Block the malicious web pages.
  - Remove emails from the sender from mailboxes.
  - Consider improvements to the security awareness program.
- Reimage the host operating system and restore compromised files to clean versions.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

