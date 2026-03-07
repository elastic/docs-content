---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Shared Object Created by Previously Unknown Process" prebuilt detection rule.'
---

# Shared Object Created by Previously Unknown Process

## Triage and analysis

### Investigating Shared Object Created by Previously Unknown Process

A shared object file is a compiled library file (typically with a .so extension) that can be dynamically linked to executable programs at runtime, allowing for code reuse and efficient memory usage. The creation of a shared object file involves compiling code into a dynamically linked library that can be loaded by other programs at runtime.

Malicious actors can leverage shared object files to execute unauthorized code, inject malicious functionality into legitimate processes, or bypass security controls. This allows malware to persist on the system, evade detection, and potentially compromise the integrity and confidentiality of the affected system and its data.

This rule monitors the creation of shared object files by previously unknown processes through the usage of the new terms rule type.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.
> This investigation guide uses [placeholder fields](https://www.elastic.co/guide/en/security/current/osquery-placeholder-fields.html) to dynamically pass alert data into Osquery queries. Placeholder fields were introduced in Elastic Stack version 8.7.0. If you're using Elastic Stack version 8.6.0 or earlier, you'll need to manually adjust this investigation guide's queries to ensure they properly run.

#### Possible Investigation Steps

- Investigate the shared object that was created or modified through OSQuery.
  - $osquery_0
  - $osquery_1
- Investigate the script execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence and whether they are located in expected locations.
  - $osquery_2
- Investigate other alerts associated with the user/host during the past 48 hours.
- Validate the activity is not related to planned patches, updates, network administrator activity, or legitimate software installations.
- Investigate whether the altered scripts call other malicious scripts elsewhere on the file system. 
  - If scripts or executables were dropped, retrieve the files and determine if they are malicious:
    - Use a private sandboxed malware analysis system to perform analysis.
      - Observe and collect information about the following activities:
        - Attempts to contact external domains and addresses.
          - Check if the domain is newly registered or unexpected.
          - Check the reputation of the domain or IP address.
        - File access, modification, and creation activities.
        - Cron jobs, services and other persistence mechanisms.
            - $osquery_3
- Investigate abnormal behaviors by the subject process/user such as network connections, file modifications, and any other spawned child processes.
  - Investigate listening ports and open sockets to look for potential command and control traffic or data exfiltration.
    - $osquery_4
    - $osquery_5
  - Identify the user account that performed the action, analyze it, and check whether it should perform this kind of action.
    - $osquery_6
- Investigate whether the user is currently logged in and active.
    - $osquery_7

### False Positive Analysis

- If this activity is related to new benign software installation activity, consider adding exceptions — preferably with a combination of user and command line conditions.
- If this activity is related to a system administrator that performed these actions for administrative purposes, consider adding exceptions for this specific administrator user account. 
- Try to understand the context of the execution by thinking about the user, machine, or business purpose. A small number of endpoints, such as servers with unique software, might appear unusual but satisfy a specific business need.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Leverage the incident response data and logging to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
