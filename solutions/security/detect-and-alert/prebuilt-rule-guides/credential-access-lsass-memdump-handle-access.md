---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "LSASS Memory Dump Handle Access" prebuilt detection rule.
---

# LSASS Memory Dump Handle Access

## Triage and analysis

### Investigating LSASS Memory Dump Handle Access

Local Security Authority Server Service (LSASS) is a process in Microsoft Windows operating systems that is responsible for enforcing security policy on the system. It verifies users logging on to a Windows computer or server, handles password changes, and creates access tokens.

Adversaries may attempt to access credential material stored in LSASS process memory. After a user logs on, the system generates and stores a variety of credential materials in LSASS process memory. This is meant to facilitate single sign-on (SSO) ensuring a user isn’t prompted each time resource access is requested. These credential materials can be harvested by an adversary using administrative user or SYSTEM privileges to conduct lateral movement using [alternate authentication material](https://attack.mitre.org/techniques/T1550/).

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Investigate other alerts associated with the user/host during the past 48 hours.
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

- There should be very few or no false positives for this rule. If this activity is expected or noisy in your environment, consider adding exceptions — preferably with a combination of user and command line conditions.
- If the process is related to antivirus or endpoint detection and response solutions, validate that it is installed on the correct path and signed with the company's valid digital signature.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- Scope compromised credentials and disable the accounts.
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

