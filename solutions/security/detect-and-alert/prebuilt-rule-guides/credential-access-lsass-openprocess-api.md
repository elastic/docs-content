---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "LSASS Process Access via Windows API" prebuilt detection rule.
---

# LSASS Process Access via Windows API

## Triage and analysis

### Investigating LSASS Process Access via Windows API

The Local Security Authority Subsystem Service (LSASS) is a critical Windows component responsible for managing user authentication and security policies. Adversaries may attempt to access the LSASS handle to dump credentials from its memory, which can be used for lateral movement and privilege escalation.

This rule identifies attempts to access LSASS by monitoring for specific API calls (OpenProcess, OpenThread) targeting the "lsass.exe" process.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.

### Possible investigation steps

- Investigate other alerts associated with the user/host during the past 48 hours.
- Investigate the process execution chain (parent process tree) of the process that accessed the LSASS handle.
  - Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
  - Determine the first time the process executable was seen in the environment and if this behavior happened in the past.
  - Validate the activity is not related to planned patches, updates, network administrator activity, or legitimate software installations.
  - Investigate any abnormal behavior by the subject process, such as network connections, DLLs loaded, registry or file modifications, and any spawned child processes.
- Assess the access rights (`process.Ext.api.parameters.desired_access`field) requested by the process. This [Microsoft documentation](https://learn.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights) may be useful to help the interpretation.
- If there are traces of LSASS memory being successfully dumped, investigate potentially compromised accounts. Analysts can do this by searching for login events (e.g., 4624) to the target host.
- Examine the host for derived artifacts that indicate suspicious activities:
  - Analyze the executables of the processes using a private sandboxed analysis system.
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


### False positive analysis

- If this rule is noisy in your environment due to expected activity, consider adding exceptions — preferably with a combination of `process.executable`, `process.code_signature.subject_name` and `process.Ext.api.parameters.desired_access_numeric` conditions.

### Related Rules

- Suspicious Lsass Process Access - 128468bf-cab1-4637-99ea-fdf3780a4609
- Potential Credential Access via DuplicateHandle in LSASS - 02a4576a-7480-4284-9327-548a806b5e48
- LSASS Memory Dump Handle Access - 208dbe77-01ed-4954-8d44-1e5751cb20de

### Response and Remediation

- Initiate the incident response process based on the outcome of the triage.
  - If malicious activity is confirmed, perform a broader investigation to identify the scope of the compromise and determine the appropriate remediation steps.
- Isolate the involved host to prevent further post-compromise behavior.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- Remove and block malicious artifacts identified during triage.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Reimage the host operating system or restore the compromised files to clean versions.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

