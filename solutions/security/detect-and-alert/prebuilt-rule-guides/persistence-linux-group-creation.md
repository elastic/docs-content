---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Linux Group Creation" prebuilt detection rule.
---

# Linux Group Creation

## Triage and analysis

### Investigating Linux Group Creation

The `groupadd` and `addgroup` commands are used to create new user groups in Linux-based operating systems.

Attackers may create new groups to maintain access to victim systems or escalate privileges by assigning a compromised account to a privileged group.

This rule identifies the usages of `groupadd` and `addgroup` to create new groups.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.
> This investigation guide uses [placeholder fields](https://www.elastic.co/guide/en/security/current/osquery-placeholder-fields.html) to dynamically pass alert data into Osquery queries. Placeholder fields were introduced in Elastic Stack version 8.7.0. If you're using Elastic Stack version 8.6.0 or earlier, you'll need to manually adjust this investigation guide's queries to ensure they properly run.

#### Possible investigation steps

- Investigate whether the group was created succesfully.
  - $osquery_0
- Identify if a user account was added to this group after creation.
  - $osquery_1
- Investigate whether the user is currently logged in and active.
  - $osquery_2
- Identify the user account that performed the action and whether it should perform this kind of action.
- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence and whether they are located in expected locations.
  - $osquery_3
- Investigate other alerts associated with the user/host during the past 48 hours.

### False positive analysis

- Group creation is a common administrative task, so there is a high chance of the activity being legitimate. Before investigating further, verify that this activity is not benign.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- Remove and block malicious artifacts identified during triage.
- Review the privileges assigned to the involved users to ensure that the least privilege principle is being followed.
- Delete the created group and, in case an account was added to this group, delete the account.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Leverage the incident response data and logging to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

