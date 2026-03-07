---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AdFind Command Activity" prebuilt detection rule.
---

# AdFind Command Activity

## Triage and analysis

### Investigating AdFind Command Activity

[AdFind](http://www.joeware.net/freetools/tools/adfind/) is a freely available command-line tool used to retrieve information from Active Directory (AD). Network discovery and enumeration tools like `AdFind` are useful to adversaries in the same ways they are effective for network administrators. This tool provides quick ability to scope AD person/computer objects and understand subnets and domain information. There are many [examples](https://thedfirreport.com/category/adfind/) of this tool being adopted by ransomware and criminal groups and used in compromises.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Examine the command line to determine what information was retrieved by the tool.
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate other alerts associated with the user/host during the past 48 hours.

### False positive analysis

- This rule has a high chance to produce false positives as it is a legitimate tool used by network administrators.
- If this rule is noisy in your environment due to expected activity, consider adding exceptions — preferably with a combination of user and command line conditions.
- Malicious behavior with `AdFind` should be investigated as part of a step within an attack chain. It doesn't happen in isolation, so reviewing previous logs/activity from impacted machines can be very telling.

### Related rules

- Windows Network Enumeration - 7b8bfc26-81d2-435e-965c-d722ee397ef1
- Enumeration of Administrator Accounts - 871ea072-1b71-4def-b016-6278b505138d
- Enumeration Command Spawned via WMIPrvSE - 770e0c4d-b998-41e5-a62e-c7901fd7f470

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

