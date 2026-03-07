---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual File Creation - Alternate Data Stream" prebuilt detection rule.
---

# Unusual File Creation - Alternate Data Stream

## Triage and analysis

### Investigating Unusual File Creation - Alternate Data Stream

Alternate Data Streams (ADS) are file attributes only found on the NTFS file system. In this file system, files are built up from a couple of attributes; one of them is $Data, also known as the data attribute.

The regular data stream, also referred to as the unnamed data stream since the name string of this attribute is empty, contains the data inside the file. So any data stream that has a name is considered an alternate data stream.

Attackers can abuse these alternate data streams to hide malicious files, string payloads, etc. This rule detects the creation of alternate data streams on highly targeted file types.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.

#### Possible investigation steps

- Retrieve the contents of the alternate data stream, and analyze it for potential maliciousness. Analysts can use the following PowerShell cmdlet to accomplish this:
  - `Get-Content C:\Path\To\file.exe -stream SampleAlternateDataStreamName`
- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Investigate any abnormal behavior by the subject process such as network connections, registry or file modifications, and any spawned child processes.
- Investigate other alerts associated with the user/host during the past 48 hours.
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
- Investigate potentially compromised accounts. Analysts can do this by searching for login events (for example, 4624) to the target host after the registry modification.


### False positive analysis

- If this activity is expected and noisy in your environment, consider adding exceptions — preferably with a combination of process executable and file conditions.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
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

