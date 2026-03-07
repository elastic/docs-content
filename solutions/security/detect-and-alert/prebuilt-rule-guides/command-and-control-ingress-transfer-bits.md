---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Ingress Transfer via Windows BITS" prebuilt detection rule.
---

# Ingress Transfer via Windows BITS

## Triage and analysis

### Investigating Ingress Transfer via Windows BITS

Windows Background Intelligent Transfer Service (BITS) is a technology that allows the transfer of files between a client and a server, which makes it a dual-use mechanism, being used by both legitimate apps and attackers. When malicious applications create BITS jobs, files are downloaded or uploaded in the context of the service host process, which can bypass security protections, and it helps to obscure which application requested the transfer.

This rule identifies such abuse by monitoring for file renaming events involving "svchost.exe" and "BIT*.tmp" on Windows systems.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.

### Possible investigation steps

- Gain context into the BITS transfer.
  - Try to determine the process that initiated the BITS transfer.
    - Search `bitsadmin.exe` processes and examine their command lines.
    - Look for unusual processes loading `Bitsproxy.dll` and other BITS-related DLLs.
  - Try to determine the origin of the file.
    - Inspect network connections initiated by `svchost.exe`.
    - Inspect `Microsoft-Windows-Bits-Client/Operational` Windows logs, specifically the event ID 59, for unusual events.
      - Velociraptor can be used to extract these entries using the [bitsadmin artifact](https://docs.velociraptor.app/exchange/artifacts/pages/bitsadmin/).
    - Check the reputation of the remote server involved in the BITS transfer, such as its IP address or domain, using threat intelligence platforms or online reputation services.
    - Check if the domain is newly registered or unexpected.
    - Use the identified domain as an indicator of compromise (IoCs) to scope other compromised hosts in the environment.
  - [BitsParser](https://github.com/fireeye/BitsParser) can be used to parse BITS database files to extract BITS job information.
- Examine the details of the dropped file, and whether it was executed.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Examine the host for derived artifacts that indicate suspicious activities:
  - Analyze the involved executables using a private sandboxed analysis system.
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

- Known false positives for the rule include legitimate software and system updates that use BITS for downloading files.

### Related Rules

- Persistence via BITS Job Notify Cmdline - c3b915e0-22f3-4bf7-991d-b643513c722f
- Unsigned BITS Service Client Process - 9a3884d0-282d-45ea-86ce-b9c81100f026
- Bitsadmin Activity - 8eec4df1-4b4b-4502-b6c3-c788714604c9

### Response and Remediation

- Initiate the incident response process based on the outcome of the triage.
  - If malicious activity is confirmed, perform a broader investigation to identify the scope of the compromise and determine the appropriate remediation steps.
- Isolate the involved hosts to prevent further post-compromise behavior.
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

