---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Renaming of OpenSSH Binaries" prebuilt detection rule.'
---

# Renaming of OpenSSH Binaries

## Triage and analysis

### Investigating Renaming of OpenSSH Binaries

OpenSSH is a widely used suite of secure networking utilities based on the Secure Shell (SSH) protocol, which provides encrypted communication sessions over a computer network.

Adversaries may exploit OpenSSH by modifying its binaries, such as `/usr/bin/scp`, `/usr/bin/sftp`, `/usr/bin/ssh`, `/usr/sbin/sshd`, or `libkeyutils.so`, to gain unauthorized access or exfiltrate SSH credentials.

The detection rule 'Modification of OpenSSH Binaries' is designed to identify such abuse by monitoring file changes in the Linux environment. It triggers an alert when a process, modifies any of the specified OpenSSH binaries or libraries. This helps security analysts detect potential malicious activities and take appropriate action.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.
> This investigation guide uses [placeholder fields](https://www.elastic.co/guide/en/security/current/osquery-placeholder-fields.html) to dynamically pass alert data into Osquery queries. Placeholder fields were introduced in Elastic Stack version 8.7.0. If you're using Elastic Stack version 8.6.0 or earlier, you'll need to manually adjust this investigation guide's queries to ensure they properly run.

### Possible investigation steps

- Investigate the script execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence and whether they are located in expected locations.
  - $osquery_0
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
            - $osquery_1
- Investigate abnormal behaviors by the subject process/user such as network connections, file modifications, and any other spawned child processes.
  - Investigate listening ports and open sockets to look for potential command and control traffic or data exfiltration.
    - $osquery_2
    - $osquery_3
  - Identify the user account that performed the action, analyze it, and check whether it should perform this kind of action.
    - $osquery_4
- Investigate whether the user is currently logged in and active.
    - $osquery_5

### False positive analysis

- Regular users should not need to modify OpenSSH binaries, which makes false positives unlikely. In the case of authorized benign true positives (B-TPs), exceptions can be added.
- If this activity is related to new benign software installation activity, consider adding exceptions — preferably with a combination of user and command line conditions.
- If this activity is related to a system administrator that performed these actions for administrative purposes, consider adding exceptions for this specific administrator user account. 
- Try to understand the context of the execution by thinking about the user, machine, or business purpose. A small number of endpoints, such as servers with unique software, might appear unusual but satisfy a specific business need.

### Response and Remediation

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
