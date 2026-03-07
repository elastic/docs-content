---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Dynamic Linker Copy" prebuilt detection rule.'
---

# Dynamic Linker Copy

## Triage and analysis

### Investigating Dynamic Linker Copy

The Linux dynamic linker is responsible for loading shared libraries required by executables at runtime. It is a critical component of the Linux operating system and should not be tampered with. 

Adversaries may attempt to copy the dynamic linker binary and create a backup copy before patching it to inject and preload malicious shared object files. This technique has been observed in recent Linux malware attacks and is considered highly suspicious or malicious.

The detection rule 'Dynamic Linker Copy' is designed to identify such abuse by monitoring for processes with names "cp" or "rsync" that involve copying the dynamic linker binary ("/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2") and modifying the "/etc/ld.so.preload" file. Additionally, the rule checks for the creation of new files with the "so" extension on Linux systems. By detecting these activities within a short time span (1 minute), the rule aims to alert security analysts to potential malicious behavior.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.
> This investigation guide uses [placeholder fields](https://www.elastic.co/guide/en/security/current/osquery-placeholder-fields.html) to dynamically pass alert data into Osquery queries. Placeholder fields were introduced in Elastic Stack version 8.7.0. If you're using Elastic Stack version 8.6.0 or earlier, you'll need to manually adjust this investigation guide's queries to ensure they properly run.

### Possible investigation steps

- Investigate the dynamic linker that was copied or altered.
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
- Investigate abnormal behaviors by the subject process/user such as network connections, file modifications, and any other spawned child processes.
  - Investigate listening ports and open sockets to look for potential command and control traffic or data exfiltration.
    - $osquery_3
    - $osquery_4
  - Identify the user account that performed the action, analyze it, and check whether it should perform this kind of action.
    - $osquery_5
- Investigate whether the user is currently logged in and active.
    - $osquery_6

### False positive analysis

- This activity is unlikely to happen legitimately. Benign true positives (B-TPs) can be added as exceptions if necessary.
- Any activity that triggered the alert and is not inherently malicious must be monitored by the security team.
- The security team should address any potential benign true positive (B-TP), as this configuration can put the user and the domain at risk.
- Try to understand the context of the execution by thinking about the user, machine, or business purpose. A small number of endpoints, such as servers with unique software, might appear unusual but satisfy a specific business need.

### Related Rules

- Modification of Dynamic Linker Preload Shared Object Inside A Container - 342f834b-21a6-41bf-878c-87d116eba3ee
- Modification of Dynamic Linker Preload Shared Object - 717f82c2-7741-4f9b-85b8-d06aeb853f4f
- Shared Object Created or Changed by Previously Unknown Process - aebaa51f-2a91-4f6a-850b-b601db2293f4

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
