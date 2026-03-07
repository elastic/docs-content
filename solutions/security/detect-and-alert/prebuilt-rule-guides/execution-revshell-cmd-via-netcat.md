---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Command Shell via NetCat" prebuilt detection rule.'
---

# Potential Command Shell via NetCat

## Triage and analysis

### Investigating Potential Command Shell via NetCat

Attackers may abuse the NetCat utility to execute commands remotely using the builtin Windows Command Shell interpreters.

#### Possible investigation steps

- Verify if the user is authorized to use the Netcat utility.
- Investigate the process execution chain (parent process tree) and how the netcat binary was dropped.
- Review the network connections made by the parent process and check their reputation.
- Investiguate all child processes spawned by the Cmd or Powershell instance.
- Examine the host for other alerts within the same period.

### False positive analysis

- IT Support or system amdinistrator authorized activity using NetCat.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- Remove and block malicious artifacts identified during triage.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
