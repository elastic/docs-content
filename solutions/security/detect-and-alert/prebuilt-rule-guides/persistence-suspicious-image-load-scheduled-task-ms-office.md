---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Image Load (taskschd.dll) from MS Office" prebuilt detection rule.
---

# Suspicious Image Load (taskschd.dll) from MS Office

## Triage and analysis

### Investigating Suspicious Image Load (taskschd.dll) from MS Office

Microsoft Office, a widely used suite of productivity applications, is frequently targeted by attackers due to its popularity in corporate environments. These attackers exploit its extensive capabilities, like macro scripts in Word and Excel, to gain initial access to systems. They often use Office documents as delivery mechanisms for malware or phishing attempts, taking advantage of their trusted status in professional settings.

`taskschd.dll` provides Command Object Model (COM) interfaces for the Windows Task Scheduler service, allowing developers to programmatically manage scheduled tasks.

This rule looks for an MS Office process loading `taskschd.dll`, which may indicate an adversary abusing COM to configure a scheduled task. This can happen as part of a phishing attack, when a malicious office document registers the scheduled task to download the malware "stage 2" or to establish persistent access.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.

### Possible investigation steps

- Analyze the host's scheduled tasks and explore the related Windows events to determine if tasks were created or deleted (Event IDs 4698 and 4699).
- Investigate any abnormal behavior by the subject process, such as network connections, registry or file modifications, and spawned child processes.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Inspect the host for suspicious or abnormal behavior in the alert timeframe.
- Examine the files downloaded during the past 24 hours.
  - Identify files that are related or can be executed in MS Office.
  - Identify and analyze macros that these documents contain.
    - Identify suspicious traits in the office macros, such as encoded or encrypted sections.
- Retrieve the suspicious files identified in the previous step and determine if they are malicious:
  - Analyze the file using a private sandboxed analysis system.
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

- This activity is unlikely to happen legitimately. Any activity that triggered the alert and is not inherently malicious must be monitored by the security team.

### Related Rules

- Suspicious WMI Image Load from MS Office - 891cb88e-441a-4c3e-be2d-120d99fe7b0d

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
  - If the malicious file was delivered via phishing:
    - Block the email sender from sending future emails.
    - Block the malicious web pages.
    - Remove emails from the sender from mailboxes.
    - Consider improvements to the security awareness program.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

