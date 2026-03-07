---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential System Tampering via File Modification" prebuilt detection rule.'
---

# Potential System Tampering via File Modification

## Triage and analysis

### Investigating Potential System Tampering via File Modification

This rule identifies attempts to delete or modify critical files used during the boot process to prevent the system from booting.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes.
- Assess all deleted or modified system critical files and perform a complete recovery of those files to prevent system booting issues.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Identify the user account that performed the action and whether it should perform this kind of action, if not immedialy disable the account.

### False positive analysis

- Analysts can dismiss the alert if the administrator is aware of the activity, no other suspicious activity was identified, and there are justifications for the execution.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
  - Prioritize cases involving critical servers and users.
- Isolate the involved hosts to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- If important data was encrypted, deleted, or modified, activate your data recovery plan.
    - Perform data recovery locally or restore the backups from replicated copies (cloud, other servers, etc.).
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Review the privileges assigned to the user to ensure that the least privilege principle is being followed.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
