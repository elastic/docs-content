---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Enumerating Domain Trusts via NLTEST.EXE" prebuilt detection rule.'
---

# Enumerating Domain Trusts via NLTEST.EXE

## Triage and analysis

### Investigating Enumerating Domain Trusts via NLTEST.EXE

Active Directory (AD) domain trusts define relationships between domains within a Windows AD environment. In this setup, a "trusting" domain permits users from a "trusted" domain to access resources. These trust relationships can be configurable as one-way, two-way, transitive, or non-transitive, enabling controlled access and resource sharing across domains.

This rule identifies the usage of the `nltest.exe` utility to enumerate domain trusts. Attackers can use this information to enable the next actions in a target environment, such as lateral movement.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Investigate other alerts associated with the user/host during the past 48 hours.

### False positive analysis

- Discovery activities are not inherently malicious if they occur in isolation and are done within the user business context (e.g., an administrator in this context). As long as the analyst did not identify suspicious activity related to the user or host, such alerts can be dismissed.

### Related rules

- Enumerating Domain Trusts via DSQUERY.EXE - 06a7a03c-c735-47a6-a313-51c354aef6c3

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved hosts to prevent further post-compromise behavior.
- Restrict PowerShell usage outside of IT and engineering business units using GPOs, AppLocker, Intune, or similar software.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
