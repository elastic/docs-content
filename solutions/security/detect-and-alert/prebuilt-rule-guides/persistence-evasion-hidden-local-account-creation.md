---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Creation of a Hidden Local User Account" prebuilt detection rule.
---

# Creation of a Hidden Local User Account

## Triage and analysis

### Investigating Creation of a Hidden Local User Account

Attackers can create accounts ending with a `$` symbol to make the account hidden to user enumeration utilities and bypass detections that identify computer accounts by this pattern to apply filters.

This rule uses registry events to identify the creation of local hidden accounts.

#### Possible investigation steps

- Identify the user account that performed the action and whether it should perform this kind of action.
- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Investigate other alerts associated with the user/host during the past 48 hours.

### False positive analysis

- This activity is unlikely to happen legitimately. Benign true positive (B-TPs) can be added as exceptions if necessary.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved hosts to prevent further post-compromise behavior.
- Delete the hidden account.
- Review the privileges assigned to the involved users to ensure that the least privilege principle is being followed.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

