---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Spike in Network Traffic To a Country" prebuilt detection rule.'
---

# Spike in Network Traffic To a Country

## Triage and analysis

### Investigating Spike in Network Traffic To a Country

Monitoring network traffic for anomalies is a good methodology for uncovering various potentially suspicious activities. For example, data exfiltration or infected machines may communicate with a command-and-control (C2) server in another country your company doesn't have business with.

This rule uses a machine learning job to detect a significant spike in the network traffic to a country, which can indicate reconnaissance or enumeration activities, an infected machine being used as a bot in a DDoS attack, or potentially data exfiltration.

#### Possible investigation steps

- Identify the specifics of the involved assets, such as role, criticality, and associated users.
- Investigate other alerts associated with the involved assets during the past 48 hours.
- Examine the data available and determine the exact users and processes involved in those connections.
- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Consider the time of day. If the user is a human (not a program or script), did the activity occurs during working hours?
- If this activity is suspicious, contact the account owner and confirm whether they are aware of it.

### False positive analysis

- Understand the context of the connections by contacting the asset owners. If this activity is related to a new business process or newly implemented (approved) technology, consider adding exceptions — preferably with a combination of user and source conditions.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved hosts to prevent further post-compromise behavior.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
  - Remove and block malicious artifacts identified during triage.
- Consider implementing temporary network border rules to block or alert connections to the target country, if relevant.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
