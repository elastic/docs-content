---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Network Connection via Signed Binary" prebuilt detection rule.'
---

# Network Connection via Signed Binary

## Triage and analysis

### Investigating Network Connection via Signed Binary

By examining the specific traits of Windows binaries (such as process trees, command lines, network connections, registry modifications, and so on) it's possible to establish a baseline of normal activity. Deviations from this baseline can indicate malicious activity, such as masquerading and deserve further investigation.

This rule looks for the execution of `expand.exe`, `extrac32.exe`, `ieexec.exe`, or `makecab.exe` utilities, followed by a network connection to an external address. Attackers can abuse utilities to execute malicious files or masquerade as those utilities to bypass detections and evade defenses.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.

#### Possible investigation steps

- Investigate other alerts associated with the user/host during the past 48 hours.
- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
  - Investigate any abnormal behavior by the subject process such as network connections, registry or file modifications, and any spawned child processes.
  - Investigate the file digital signature and process original filename, if suspicious, treat it as potential malware.
- Investigate the target host that the signed binary is communicating with.
  - Check if the domain is newly registered or unexpected.
  - Check the reputation of the domain or IP address.
- Assess whether this behavior is prevalent in the environment by looking for similar occurrences across hosts.
- Examine the host for derived artifacts that indicate suspicious activities:
  - Analyze the process executable using a private sandboxed analysis system.
  - Observe and collect information about the following activities in both the sandbox and the alert subject host:
    - Attempts to contact external domains and addresses.
      - Use the Elastic Defend network events to determine domains and addresses contacted by the subject process by filtering by the process' `process.entity_id`.
      - Examine the DNS cache for suspicious or anomalous entries.
        - $osquery_0
    - Use the Elastic Defend registry events to examine registry keys accessed, modified, or created by the related processes in the process tree.
    - Examine the host services for suspicious or anomalous entries.
      - $osquery_1
      - $osquery_2
      - $osquery_3
  - Retrieve the files' SHA-256 hash values using the PowerShell `Get-FileHash` cmdlet and search for the existence and reputation of the hashes in resources like VirusTotal, Hybrid-Analysis, CISCO Talos, Any.run, etc.

### False positive analysis

- If this activity is expected and noisy in your environment, consider adding exceptions — preferably with a combination of destination IP address and command line conditions.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- Remove and block malicious artifacts identified during triage.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
