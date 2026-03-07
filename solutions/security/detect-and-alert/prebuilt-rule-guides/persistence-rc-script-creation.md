---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "rc.local/rc.common File Creation" prebuilt detection rule.'
---

# rc.local/rc.common File Creation

## Triage and analysis

### Investigating rc.local/rc.common File Creation

The `rc.local` file executes custom commands or scripts during system startup on Linux systems. `rc.local` has been deprecated in favor of the use of `systemd services`, and more recent Unix distributions no longer leverage this method of on-boot script execution.

There might still be users that use `rc.local` in a benign matter, so investigation to see whether the file is malicious is vital.

Detection alerts from this rule indicate the creation of a new `/etc/rc.local` file.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.
> This investigation guide uses [placeholder fields](https://www.elastic.co/guide/en/security/current/osquery-placeholder-fields.html) to dynamically pass alert data into Osquery queries. Placeholder fields were introduced in Elastic Stack version 8.7.0. If you're using Elastic Stack version 8.6.0 or earlier, you'll need to manually adjust this investigation guide's queries to ensure they properly run.

#### Possible Investigation Steps

- Identify the user account that performed the action and whether it should perform this kind of action.
- Investigate the file that was created or modified.
  - $osquery_0
- Investigate the script execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence and whether they are located in expected locations.
  - $osquery_1
- Investigate whether the `/lib/systemd/system/rc-local.service` and `/run/systemd/generator/multi-user.target.wants/rc-local.service` files were created through the `systemd-rc-local-generator` located at `/usr/lib/systemd/system-generators/systemd-rc-local-generator`.
  - $osquery_2
  - In case the file is not present here, `sudo systemctl status rc-local` can be executed to find the location of the rc-local unit file.
  - If `rc-local.service` is found, manual investigation is required to check for the rc script execution. Systemd will generate syslogs in case of the execution of the rc-local service. `sudo cat /var/log/syslog | grep "rc-local.service|/etc/rc.local Compatibility"` can be executed to check for the execution of the service.
    - If logs are found, it's likely that the contents of the `rc.local` file have been executed. Analyze the logs. In case several syslog log files are available, use a wildcard to search through all of the available logs.
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
            - $osquery_3

### False Positive Analysis

- If this activity is related to new benign software installation activity, consider adding exceptions — preferably with a combination of user and command line conditions.
- If this activity is related to a system administrator who uses `rc.local` for administrative purposes, consider adding exceptions for this specific administrator user account.
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
- Delete the `service/rc.local` files or restore their original configuration.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Leverage the incident response data and logging to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
