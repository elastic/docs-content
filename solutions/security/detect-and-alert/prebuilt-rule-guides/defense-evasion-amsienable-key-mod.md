---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Modification of AmsiEnable Registry Key" prebuilt detection rule.'
---

# Modification of AmsiEnable Registry Key

## Triage and analysis

### Investigating Modification of AmsiEnable Registry Key

The Windows Antimalware Scan Interface (AMSI) is a versatile interface standard that allows your applications and services to integrate with any antimalware product on a machine. AMSI integrates with multiple Windows components, ranging from User Account Control (UAC) to VBA macros and PowerShell.

Since AMSI is widely used across security products for increased visibility, attackers can disable it to evade detections that rely on it.

This rule monitors the modifications to the Software\Microsoft\Windows Script\Settings\AmsiEnable registry key.

#### Possible investigation steps

- Identify the user account that performed the action and whether it should perform this kind of action.
- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Investigate the execution of scripts and macros after the registry modification.
- Retrieve scripts or Microsoft Office files and determine if they are malicious:
  - Use a private sandboxed malware analysis system to perform analysis.
    - Observe and collect information about the following activities:
      - Attempts to contact external domains and addresses.
      - File and registry access, modification, and creation activities.
      - Service creation and launch activities.
      - Scheduled task creation.
  - Use the PowerShell Get-FileHash cmdlet to get the files' SHA-256 hash values.
    - Search for the existence and reputation of the hashes in resources like VirusTotal, Hybrid-Analysis, CISCO Talos, Any.run, etc.
- Use process name, command line, and file hash to search for occurrences on other hosts.

### False positive analysis

- This modification should not happen legitimately. Any potential benign true positive (B-TP) should be mapped and monitored by the security team as these modifications expose the host to malware infections.

### Related rules

- Microsoft Windows Defender Tampering - fe794edd-487f-4a90-b285-3ee54f2af2d3

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved hosts to prevent further post-compromise behavior.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- Remove and block malicious artifacts identified during triage.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Delete or set the key to its default value.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
