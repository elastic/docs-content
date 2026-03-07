---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Active Directory Discovery using AdExplorer" prebuilt detection rule.'
---

# Active Directory Discovery using AdExplorer

## Triage and analysis

### Investigating Active Directory Discovery using AdExplorer

Active Directory Explorer (AD Explorer) is an advanced Active Directory (AD) viewer and editor. AD Explorer also includes the ability to save snapshots of an AD database for off-line viewing and comparisons.

#### Possible investigation steps

- Identify the user account that performed the action and whether it should perform this kind of action.
- Verify any file creation, this may indicate the creation of an AD snapshot.
- Identify when the AdExplorer binary was dropped and by what process reviewing file creation events.
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate other alerts associated with the user/host during the past 48 hours.

### False positive analysis

- This rule has a high chance to produce false positives as it is a legitimate tool used by system administrators.
- If this rule is noisy in your environment due to expected activity, consider adding exceptions — preferably with a combination of user and process path conditions.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
