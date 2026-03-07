---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kernel Module Load via Built-in Utility" prebuilt detection rule.'
---

# Kernel Module Load via Built-in Utility

## Triage and analysis

### Investigating Kernel Module Load via Built-in Utility

Threat actors with root privileges may abuse pre-installed binaries to load loadable kernel modules (LKMs), which are object files that extend the functionality of the kernel. 

Threat actors can abuse this utility to load rootkits, granting them full control over the system and the ability to evade security products.

The detection rule 'Kernel Module Load via Built-in Utility' is designed to identify instances where these binaries are used to load a kernel object file (with a .ko extension) on a Linux system. This activity is uncommon and may indicate suspicious or malicious behavior.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.
> This investigation guide uses [placeholder fields](https://www.elastic.co/guide/en/security/current/osquery-placeholder-fields.html) to dynamically pass alert data into Osquery queries. Placeholder fields were introduced in Elastic Stack version 8.7.0. If you're using Elastic Stack version 8.6.0 or earlier, you'll need to manually adjust this investigation guide's queries to ensure they properly run.

### Possible investigation steps

- Investigate the kernel object file that was loaded.
  - $osquery_1
- Investigate the script execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence and whether they are located in expected locations.
  - $osquery_2
- Investigate the kernel ring buffer for any warnings or messages, such as tainted or out-of-tree kernel module loads through `dmesg`.
- Investigate syslog for any unusual segfaults or other messages. Rootkits may be installed on targets with different architecture as expected, and could potentially cause segmentation faults. 
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
- Investigate abnormal behaviors by the subject process/user such as network connections, file modifications, and any other spawned child processes.
  - Investigate listening ports and open sockets to look for potential command and control traffic or data exfiltration.
    - $osquery_3
    - $osquery_4
  - Identify the user account that performed the action, analyze it, and check whether it should perform this kind of action.
    - $osquery_5
- Investigate whether the user is currently logged in and active.
    - $osquery_6

### False positive analysis

- If this activity is related to new benign software installation activity, consider adding exceptions — preferably with a combination of user and command line conditions.
- If this activity is related to a system administrator who uses cron jobs for administrative purposes, consider adding exceptions for this specific administrator user account. 
- Try to understand the context of the execution by thinking about the user, machine, or business purpose. A small number of endpoints, such as servers with unique software, might appear unusual but satisfy a specific business need.

### Related Rules

- Kernel Driver Load - 3e12a439-d002-4944-bc42-171c0dcb9b96
- Tainted Out-Of-Tree Kernel Module Load - 51a09737-80f7-4551-a3be-dac8ef5d181a
- Tainted Kernel Module Load - 05cad2fb-200c-407f-b472-02ea8c9e5e4a
- Attempt to Clear Kernel Ring Buffer - 2724808c-ba5d-48b2-86d2-0002103df753
- Enumeration of Kernel Modules via Proc - 80084fa9-8677-4453-8680-b891d3c0c778
- Suspicious Modprobe File Event - 40ddbcc8-6561-44d9-afc8-eefdbfe0cccd
- Kernel Module Removal - cd66a5af-e34b-4bb0-8931-57d0a043f2ef
- Enumeration of Kernel Modules - 2d8043ed-5bda-4caf-801c-c1feb7410504

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
