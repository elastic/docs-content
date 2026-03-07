---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Network Connection via RunDLL32" prebuilt detection rule.
---

# Unusual Network Connection via RunDLL32

## Triage and analysis

### Investigating Unusual Network Connection via RunDLL32

RunDLL32 is a built-in Windows utility and also a vital component used by the operating system itself. The functionality provided by RunDLL32 to execute Dynamic Link Libraries (DLLs) is widely abused by attackers, because it makes it hard to differentiate malicious activity from normal operations.

This rule looks for external network connections established using RunDLL32 when the utility is being executed with no arguments, which can potentially indicate command and control activity.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Investigate the target host that RunDLL32 is communicating with.
  - Check if the domain is newly registered or unexpected.
  - Check the reputation of the domain or IP address.
- Identify the target computer and its role in the IT environment.
- Assess whether this behavior is prevalent in the environment by looking for similar occurrences across hosts.

### False positive analysis

- This activity is unlikely to happen legitimately. Benign true positives (B-TPs) can be added as exceptions if necessary.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved hosts to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Review the privileges assigned to the user to ensure that the least privilege principle is being followed.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

