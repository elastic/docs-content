---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Evasion via Filter Manager" prebuilt detection rule.'
---

# Potential Evasion via Filter Manager

## Triage and analysis

### Investigating Potential Evasion via Filter Manager

A file system filter driver, or minifilter, is a specialized type of filter driver designed to intercept and modify I/O requests sent to a file system or another filter driver. Minifilters are used by a wide range of security software, including EDR, antivirus, backup agents, encryption products, etc.

Attackers may try to unload minifilters to avoid protections such as malware detection, file system monitoring, and behavior-based detections.

This rule identifies the attempt to unload a minifilter using the `fltmc.exe` command-line utility, a tool used to manage and query the filter drivers loaded on Windows systems.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.

#### Possible investigation steps

- Identify the user account that performed the action and whether it should perform this kind of action.
- Examine the command line event to identify the target driver.
  - Identify the minifilter's role in the environment and if it is security-related. Microsoft provides a [list](https://learn.microsoft.com/en-us/windows-hardware/drivers/ifs/allocated-altitudes) of allocated altitudes that may provide more context, such as the manufacturer.
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Examine the host for derived artifacts that indicate suspicious activities:
  - Observe and collect information about the following activities in the alert subject host:
    - Attempts to contact external domains and addresses.
      - Use the Elastic Defend network events to determine domains and addresses contacted by the subject process by filtering by the process' `process.entity_id`.
      - Examine the DNS cache for suspicious or anomalous entries.
        - $osquery_0
    - Use the Elastic Defend registry events to examine registry keys accessed, modified, or created by the related processes in the process tree.
    - Examine the host services for suspicious or anomalous entries.
      - $osquery_1
      - $osquery_2
      - $osquery_3

### False positive analysis

- This mechanism can be used legitimately. Analysts can dismiss the alert if the administrator is aware of the activity and there are justifications for the action.

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
