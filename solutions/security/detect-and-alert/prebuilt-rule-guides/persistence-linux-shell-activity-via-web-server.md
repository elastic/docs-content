---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Child Execution via Web Server" prebuilt detection rule.
---

# Suspicious Child Execution via Web Server

## Triage and analysis

### Investigating Suspicious Child Execution via Web Server

Adversaries may backdoor web servers with web shells to establish persistent access to systems. A web shell is a malicious script, often embedded into a compromised web server, that grants an attacker remote access and control over the server. This enables the execution of arbitrary commands, data exfiltration, and further exploitation of the target network.

This rule detects a web server process spawning script and command line interface programs, potentially indicating attackers executing commands using the web shell.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.
> This investigation guide uses [placeholder fields](https://www.elastic.co/guide/en/security/current/osquery-placeholder-fields.html) to dynamically pass alert data into Osquery queries. Placeholder fields were introduced in Elastic Stack version 8.7.0. If you're using Elastic Stack version 8.6.0 or earlier, you'll need to manually adjust this investigation guide's queries to ensure they properly run.

#### Possible investigation steps

- Investigate abnormal behaviors by the subject process such as network connections, file modifications, and any other spawned child processes.
  - Investigate listening ports and open sockets to look for potential reverse shells or data exfiltration.
    - $osquery_0
    - $osquery_1
  - Investigate the process information for malicious or uncommon processes/process trees.
    - $osquery_2
  - Investigate the process tree spawned from the user that is used to run the web application service. A user that is running a web application should not spawn other child processes.
    - $osquery_3
- Examine the command line to determine which commands or scripts were executed.
- Investigate other alerts associated with the user/host during the past 48 hours.
- If scripts or executables were dropped, retrieve the files and determine if they are malicious:
  - Use a private sandboxed malware analysis system to perform analysis.
    - Observe and collect information about the following activities:
      - Attempts to contact external domains and addresses.
        - Check if the domain is newly registered or unexpected.
        - Check the reputation of the domain or IP address.
      - File access, modification, and creation activities.
      - Cron jobs, services and other persistence mechanisms.
        - $osquery_4

### False positive analysis

- This activity is unlikely to happen legitimately. Any activity that triggered the alert and is not inherently malicious must be monitored by the security team.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- Remove and block malicious artifacts identified during triage.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Leverage the incident response data and logging to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

