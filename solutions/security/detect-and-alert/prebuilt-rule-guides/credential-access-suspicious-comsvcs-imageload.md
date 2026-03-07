---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Credential Access via Renamed COM+ Services DLL" prebuilt detection rule.'
---

# Potential Credential Access via Renamed COM+ Services DLL

## Triage and analysis

### Investigating Potential Credential Access via Renamed COM+ Services DLL

COMSVCS.DLL is a Windows library that exports the MiniDump function, which can be used to dump a process memory. Adversaries may attempt to dump LSASS memory using a renamed COMSVCS.DLL to bypass command-line based detection and gain unauthorized access to credentials.

This rule identifies suspicious instances of rundll32.exe loading a renamed COMSVCS.DLL image, which can indicate potential abuse of the MiniDump function for credential theft.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.

### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Investigate any abnormal behavior by the subject process, such as network connections, registry or file modifications, and any spawned child processes.
- Identify the process that created the DLL using file creation events.
   - Inspect the file for useful metadata, such as file size and creation or modification time.
- Examine the host for derived artifacts that indicate suspicious activities:
  - Analyze the process executable and DLL using a private sandboxed analysis system.
  - Observe and collect information about the following activities in both the sandbox and the alert subject host:
    - Attempts to contact external domains and addresses.
      - Use the Elastic Defend network events to determine domains and addresses contacted by the subject process by filtering by the process's `process.entity_id`.
      - Examine the DNS cache for suspicious or anomalous entries.
        - $osquery_0
    - Use the Elastic Defend registry events to examine registry keys accessed, modified, or created by the related processes in the process tree.
    - Examine the host services for suspicious or anomalous entries.
      - $osquery_1
      - $osquery_2
      - $osquery_3
  - Retrieve the files' SHA-256 hash values using the PowerShell `Get-FileHash` cmdlet and search for the existence and reputation of the hashes in resources like VirusTotal, Hybrid-Analysis, CISCO Talos, Any.run, etc.
- Assess whether this behavior is prevalent in the environment by looking for similar occurrences across hosts.
- Look for the presence of relevant artifacts on other systems. Identify commonalities and differences between potentially compromised systems.

### False positive analysis

- False positives may include legitimate instances of rundll32.exe loading a renamed COMSVCS.DLL image for non-malicious purposes, such as during software development, testing, or troubleshooting.

### Related Rules

- Potential Credential Access via LSASS Memory Dump - 9960432d-9b26-409f-972b-839a959e79e2
- Suspicious Module Loaded by LSASS - 3a6001a0-0939-4bbe-86f4-47d8faeb7b97
- Suspicious Lsass Process Access - 128468bf-cab1-4637-99ea-fdf3780a4609
- LSASS Process Access via Windows API - ff4599cb-409f-4910-a239-52e4e6f532ff

### Response and Remediation

- Initiate the incident response process based on the outcome of the triage.
  - If malicious activity is confirmed, perform a broader investigation to identify the scope of the compromise and determine the appropriate remediation steps.
- Implement Elastic Endpoint Security to detect and prevent further post exploitation activities in the environment.
   - Contain the affected system by isolating it from the network to prevent further spread of the attack.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- Remove and block malicious artifacts identified during triage.
- Restore the affected system to its operational state by applying any necessary patches, updates, or configuration changes.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
