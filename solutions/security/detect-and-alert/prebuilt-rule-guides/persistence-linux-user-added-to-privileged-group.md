---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Linux User Added to Privileged Group" prebuilt detection rule.
---

# Linux User Added to Privileged Group

## Triage and analysis

### Investigating Linux User Added to Privileged Group

The `usermod`, `adduser`, and `gpasswd` commands can be used to assign user accounts to new groups in Linux-based operating systems.

Attackers may add users to a privileged group in order to escalate privileges or establish persistence on a system or domain.

This rule identifies the usages of `usermod`, `adduser` and `gpasswd` to assign user accounts to a privileged group.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.
> This investigation guide uses [placeholder fields](https://www.elastic.co/guide/en/security/current/osquery-placeholder-fields.html) to dynamically pass alert data into Osquery queries. Placeholder fields were introduced in Elastic Stack version 8.7.0. If you're using Elastic Stack version 8.6.0 or earlier, you'll need to manually adjust this investigation guide's queries to ensure they properly run.

#### Possible investigation steps

- Investigate whether the user was succesfully added to the privileged group.
  - $osquery_0
- Investigate whether the user is currently logged in and active.
  - $osquery_1
- Retrieve information about the privileged group to which the user was added.
  - $osquery_2
- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence and whether they are located in expected locations.
  - $osquery_3
- Identify the user account that performed the action and whether it should perform this kind of action.
- Investigate other alerts associated with the user/host during the past 48 hours.

### False positive analysis

- Adding accounts to a group is a common administrative task, so there is a high chance of the activity being legitimate. Before investigating further, verify that this activity is not benign.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- Review the privileges assigned to the involved users to ensure that the least privilege principle is being followed.
- Delete the account that seems to be involved in malicious activity.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

