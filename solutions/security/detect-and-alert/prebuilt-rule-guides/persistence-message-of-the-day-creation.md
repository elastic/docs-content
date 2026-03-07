---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Message-of-the-Day (MOTD) File Creation" prebuilt detection rule.'
---

# Message-of-the-Day (MOTD) File Creation

## Triage and analysis

### Investigating Message-of-the-Day (MOTD) File Creation

The message-of-the-day (MOTD) is used to display a customizable system-wide message or information to users upon login in Linux.

Attackers can abuse message-of-the-day (motd) files to run scripts, commands or malicious software every time a user connects to a system over SSH or a serial connection, by creating a new file within the `/etc/update-motd.d/` directory. Executable files in these directories automatically run with root privileges.

This rule identifies the creation of new files within the `/etc/update-motd.d/` directory.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.
> This investigation guide uses [placeholder fields](https://www.elastic.co/guide/en/security/current/osquery-placeholder-fields.html) to dynamically pass alert data into Osquery queries. Placeholder fields were introduced in Elastic Stack version 8.7.0. If you're using Elastic Stack version 8.6.0 or earlier, you'll need to manually adjust this investigation guide's queries to ensure they properly run.

#### Possible Investigation Steps

- Investigate the file that was created or modified.
  - $osquery_0
- Investigate whether any other files in the `/etc/update-motd.d/` directory have been altered.
  - $osquery_1
  - $osquery_2
- Investigate the script execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence and whether they are located in expected locations.
  - $osquery_3
- Investigate other alerts associated with the user/host during the past 48 hours.
- Investigate whether the modified scripts call other malicious scripts elsewhere on the file system.
  - If scripts or executables were dropped, retrieve the files and determine if they are malicious:
    - Use a private sandboxed malware analysis system to perform analysis.
      - Observe and collect information about the following activities:
        - Attempts to contact external domains and addresses.
          - Check if the domain is newly registered or unexpected.
          - Check the reputation of the domain or IP address.
        - File access, modification, and creation activities.
        - Cron jobs, services and other persistence mechanisms.
            - $osquery_4

### Related Rules

- Process Spawned from Message-of-the-Day (MOTD) - 4ec47004-b34a-42e6-8003-376a123ea447

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
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Delete the MOTD files or restore their original configuration.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Leverage the incident response data and logging to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
