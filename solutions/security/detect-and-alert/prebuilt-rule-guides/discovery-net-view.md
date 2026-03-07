---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Windows Network Enumeration" prebuilt detection rule.
---

# Windows Network Enumeration

## Triage and analysis

### Investigating Windows Network Enumeration

After successfully compromising an environment, attackers may try to gain situational awareness to plan their next steps. This can happen by running commands to enumerate network resources, users, connections, files, and installed security software.

This rule looks for the execution of the `net` utility to enumerate servers in the environment that hosts shared drives or printers. This information is useful to attackers as they can identify targets for lateral movements and search for valuable shared data.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Investigate any abnormal account behavior, such as command executions, file creations or modifications, and network connections.

### False positive analysis

- Discovery activities are not inherently malicious if they occur in isolation. As long as the analyst did not identify suspicious activity related to the user or host, such alerts can be dismissed.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved hosts to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

