---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Behavior - Detected - Elastic Defend" prebuilt detection rule.
---

# Behavior - Detected - Elastic Defend

## Triage and analysis

### Investigating Behavior - Detected - Elastic Defend

Malicious behavior protection is a foundational feature which can be used to protect against all manner of attacks on the endpoint. For example, it provides coverage against phishing such as malicious macros, many malware families based on their activities, privilege escalation attacks such as user account control bypasses (UAC), credential theft, and much more. It works by consuming an unfiltered feed of all events that are captured on the system (process, file, registry, network, dns, etc). These events are processed against a routinely updated set of rules written by Elastic threat experts. From there, malicious behaviors are identified and offending processes are terminated. The protection operates on the event stream asynchronously, but has been designed to be extremely efficient and typically requires just milliseconds (under standard load) to stop malicious activity.

### Possible investigation steps

- Assess whether this activity is prevalent in your environment by looking for similar occurrences across hosts.
- Verify the detailed activity of the process that triggered the alert (process tree, child process, process arguments, network, files, libraries and registry events).
- Verify the activity of the `user.name` associated with the alert (local or remote actity, privileged or standard user).
- Particular attention should be paid to instances where the same process is triggering multiple alerts (more than 2 or 3) within a short period of time.
- Even the the process is signed by a valid certificate, verify the if it's running from the expected location or if it's loading any suspicious libraries or any sign of code injection.

### False positive analysis

- Same alert observed on a high number of hosts with similar details.
- High count of the same alert on a specific host over a long period of time.

### Response and Remediation

- Initiate the incident response process based on the outcome of the triage.
  - If malicious activity is confirmed, perform a broader investigation to identify the scope of the compromise and determine the appropriate remediation steps.
- Implement Elastic Endpoint Security to detect and prevent further post exploitation activities in the environment.
   - Contain the affected system by isolating it from the network to prevent further spread of the attack.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- Remove and block malicious artifacts identified during triage.
- Restore the affected system to its operational state by applying any necessary patches, updates, or configuration changes.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

