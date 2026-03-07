---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Remote File Download via PowerShell" prebuilt detection rule.'
---

# Remote File Download via PowerShell

## Triage and analysis

### Investigating Remote File Download via PowerShell

Attackers commonly transfer tooling or malware from external systems into a compromised environment using the command and control channel. However, they can also abuse signed utilities to drop these files.

PowerShell is one of system administrators' main tools for automation, report routines, and other tasks. This makes it available for use in various environments and creates an attractive way for attackers to execute code and perform actions. This rule correlates network and file events to detect downloads of executable and script files performed using PowerShell.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.
> This investigation guide uses the [Investigate Markdown Plugin](https://www.elastic.co/guide/en/security/current/interactive-investigation-guides.html) introduced in Elastic Stack version 8.8.0. Older Elastic Stack versions will display unrendered Markdown in this guide.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Evaluate whether the user needs to use PowerShell to complete tasks.
- Investigate other alerts associated with the user/host during the past 48 hours.
  - $investigate_0
  - $investigate_1
- Check the reputation of the domain or IP address used to host the downloaded file.
- Examine the host for derived artifacts that indicate suspicious activities:
  - Analyze the file using a private sandboxed analysis system.
  - Observe and collect information about the following activities in both the sandbox and the alert subject host:
    - Attempts to contact external domains and addresses.
      - Use the Elastic Defend network events to determine domains and addresses contacted by the subject process by filtering by the process' `process.entity_id`.
        - $investigate_2
      - Examine the DNS cache for suspicious or anomalous entries.
        - $osquery_0
    - Use the Elastic Defend registry events to examine registry keys accessed, modified, or created by the related processes in the process tree.
    - Examine the host services for suspicious or anomalous entries.
      - $osquery_1
      - $osquery_2
      - $osquery_3
  - Retrieve the files' SHA-256 hash values using the PowerShell `Get-FileHash` cmdlet and search for the existence and reputation of the hashes in resources like VirusTotal, Hybrid-Analysis, CISCO Talos, Any.run, etc.
- Investigate potentially compromised accounts. Analysts can do this by searching for login events (for example, 4624) to the target host after the registry modification.

### False positive analysis

- Administrators can use PowerShell legitimately to download executable and script files. Analysts can dismiss the alert if the Administrator is aware of the activity and the triage has not identified suspicious or malicious files.

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
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
