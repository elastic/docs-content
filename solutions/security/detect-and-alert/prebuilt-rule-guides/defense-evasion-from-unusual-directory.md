---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Process Execution from an Unusual Directory" prebuilt detection rule.
---

# Process Execution from an Unusual Directory

## Triage and analysis

### Investigating Process Execution from an Unusual Directory

This rule identifies processes that are executed from suspicious default Windows directories. Adversaries may abuse this technique by planting malware in trusted paths, making it difficult for security analysts to discern if their activities are malicious or take advantage of exceptions that may apply to these paths.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.

### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes, examining their executable files for prevalence, location, and valid digital signatures.
- Investigate any abnormal behavior by the subject process, such as network connections, registry or file modifications, and any spawned child processes.
- Examine arguments and working directory to determine the program's source or the nature of the tasks it is performing.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Inspect the host for suspicious or abnormal behavior in the alert timeframe.
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

- If this activity is expected and noisy in your environment, consider adding exceptions — preferably with a combination of executable and signature conditions.

### Related Rules

- Unusual Windows Path Activity - 445a342e-03fb-42d0-8656-0367eb2dead5
- Execution from Unusual Directory - Command Line - cff92c41-2225-4763-b4ce-6f71e5bda5e6

### Response and Remediation

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

