---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Command Execution via ForFiles" prebuilt detection rule.'
---

# Command Execution via ForFiles

## Triage and analysis

### Investigating Command Execution via ForFiles

### Possible investigation steps

- Identify the user account that performed the action and whether it should perform this kind of action.
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Validate the activity is not related to planned patches, updates, network administrator activity, or legitimate software installations.
- Assess whether this behavior is prevalent in the environment by looking for similar occurrences across hosts.

### False positive analysis

- This is a dual-use tool, meaning its usage is not inherently malicious. Analysts can dismiss the alert if the administrator is aware of the activity, no other suspicious activity was identified.

### Response and Remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
