---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "User Account Creation" prebuilt detection rule.'
---

# User Account Creation

## Triage and analysis

### Investigating User Account Creation

Attackers may create new accounts (both local and domain) to maintain access to victim systems.

This rule identifies the usage of `net.exe` to create new accounts.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Identify if the account was added to privileged groups or assigned special privileges after creation.
- Investigate other alerts associated with the user/host during the past 48 hours.

### False positive analysis

- Account creation is a common administrative task, so there is a high chance of the activity being legitimate. Before investigating further, verify that this activity is not benign.

### Related rules

- Creation of a Hidden Local User Account - 2edc8076-291e-41e9-81e4-e3fcbc97ae5e
- Windows User Account Creation - 38e17753-f581-4644-84da-0d60a8318694

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- Delete the created account.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
