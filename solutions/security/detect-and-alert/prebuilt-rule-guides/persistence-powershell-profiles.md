---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Persistence via PowerShell profile" prebuilt detection rule.'
---

# Persistence via PowerShell profile

## Triage and analysis

### Investigating Persistence via PowerShell profile

PowerShell profiles are scripts executed when PowerShell starts, customizing the user environment. They are commonly used in Windows environments for legitimate purposes, such as setting variables or loading modules. However, adversaries can abuse PowerShell profiles to establish persistence by inserting malicious code that executes each time PowerShell is launched.

This rule identifies the creation or modification of a PowerShell profile. It does this by monitoring file events on Windows systems, specifically targeting profile-related file paths and names, such as `profile.ps1` and `Microsoft.Powershell_profile.ps1`. By detecting these activities, security analysts can investigate potential abuse of PowerShell profiles for malicious persistence.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.

### Possible investigation steps

- Retrive and inspect the PowerShell profile content; look for suspicious DLL imports, collection or persistence capabilities, suspicious functions, encoded or compressed data, suspicious commands, and other potentially malicious characteristics.
- Identify the process responsible for the PowerShell profile creation/modification. Use the Elastic Defend events to examine all the activity of the subject process by filtering by the process's `process.entity_id`.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Evaluate whether the user needs to use PowerShell to complete tasks.
- Check for additional PowerShell and command-line logs that indicate that any suspicious command or function were run.
- Examine the host for derived artifacts that indicate suspicious activities:
  - Observe and collect information about the following activities in the alert subject host:
    - Attempts to contact external domains and addresses.
      - Use the Elastic Defend network events to determine domains and addresses contacted by the subject process by filtering by the process's `process.entity_id`.
      - Examine the DNS cache for suspicious or anomalous entries.
        - $osquery_0
    - Use the Elastic Defend registry events to examine registry keys accessed, modified, or created by the related processes in the process tree.
    - Examine the host services for suspicious or anomalous entries.
      - $osquery_1
      - $osquery_2
      - $osquery_3

### False positive analysis

- This is a dual-use mechanism, meaning its usage is not inherently malicious. Analysts can dismiss the alert if the script doesn't contain malicious functions or potential for abuse, no other suspicious activity was identified, and the user has business justifications to use PowerShell.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
  - If malicious activity is confirmed, perform a broader investigation to identify the scope of the compromise and determine the appropriate remediation steps.
- Isolate the involved hosts to prevent further post-compromise behavior.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- Remove and block malicious artifacts identified during triage.
- Reimage the host operating system or restore the compromised files to clean versions.
- Restrict PowerShell usage outside of IT and engineering business units using GPOs, AppLocker, Intune, or similar software.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
  - Consider enabling and collecting PowerShell logs such as transcription, module, and script block logging, to improve visibility into PowerShell activities.
