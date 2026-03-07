---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "System V Init Script Created" prebuilt detection rule.
---

# System V Init Script Created

## Triage and analysis

### Investigating System V Init Script Created

The `/etc/init.d` directory is used in Linux systems to store the initialization scripts for various services and daemons that are executed during system startup and shutdown.

Attackers can abuse files within the `/etc/init.d/` directory to run scripts, commands or malicious software every time a system is rebooted by converting an executable file into a service file through the `systemd-sysv-generator`. After conversion, a unit file is created within the `/run/systemd/generator.late/` directory.

This rule looks for the creation of new files within the `/etc/init.d/` directory. Executable files in these directories will automatically run at boot with root privileges.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.
> This investigation guide uses [placeholder fields](https://www.elastic.co/guide/en/security/current/osquery-placeholder-fields.html) to dynamically pass alert data into Osquery queries. Placeholder fields were introduced in Elastic Stack version 8.7.0. If you're using Elastic Stack version 8.6.0 or earlier, you'll need to manually adjust this investigation guide's queries to ensure they properly run.
#### Possible Investigation Steps

- Investigate the file that was created or modified.
  - $osquery_0
- Investigate whether any other files in the `/etc/init.d/` or `/run/systemd/generator.late/` directories have been altered.
  - $osquery_1
  - $osquery_2
- Investigate the script execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence and whether they are located in expected locations.
  - $osquery_3
- Investigate syslog through the `sudo cat /var/log/syslog | grep 'LSB'` command to find traces of the LSB header of the script (if present). If syslog is being ingested into Elasticsearch, the same can be accomplished through Kibana.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Validate whether this activity is related to planned patches, updates, network administrator activity, or legitimate software installations.
- Investigate whether the altered scripts call other malicious scripts elsewhere on the file system. 
  - If scripts or executables were dropped, retrieve the files and determine if they are malicious:
    - Use a private sandboxed malware analysis system to perform analysis.
      - Observe and collect information about the following activities:
        - Attempts to contact external domains and addresses.
          - Check if the domain is newly registered or unexpected.
          - Check the reputation of the domain or IP address.
        - File access, modification, and creation activities.
        - Cron jobs, services and other persistence mechanisms.
            - $osquery_4

### False Positive Analysis

- If this activity is related to new benign software installation activity, consider adding exceptions — preferably with a combination of user and command line conditions.
- If this activity is related to a system administrator who uses init.d for administrative purposes, consider adding exceptions for this specific administrator user account. 
- Try to understand the context of the execution by thinking about the user, machine, or business purpose. A small number of endpoints, such as servers with unique software, might appear unusual but satisfy a specific business need.

### Related Rules

- Suspicious File Creation in /etc for Persistence - 1c84dd64-7e6c-4bad-ac73-a5014ee37042

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
- Delete the maliciously created service/init.d files or restore it to the original configuration.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Leverage the incident response data and logging to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

