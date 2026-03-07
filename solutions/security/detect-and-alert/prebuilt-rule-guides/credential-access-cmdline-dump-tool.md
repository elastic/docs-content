---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Credential Access via Windows Utilities" prebuilt detection rule.
---

# Potential Credential Access via Windows Utilities

## Triage and analysis

### Investigating Potential Credential Access via Windows Utilities

Local Security Authority Server Service (LSASS) is a process in Microsoft Windows operating systems that is responsible for enforcing security policy on the system. It verifies users logging on to a Windows computer or server, handles password changes, and creates access tokens.

The `Ntds.dit` file is a database that stores Active Directory data, including information about user objects, groups, and group membership.

This rule looks for the execution of utilities that can extract credential data from the LSASS memory and Active Directory `Ntds.dit` file.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Investigate abnormal behaviors observed by the subject process, such as network connections, registry or file modifications, and any spawned child processes.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Examine the command line to identify what information was targeted.
- Identify the target computer and its role in the IT environment.

### False positive analysis

- This activity is unlikely to happen legitimately. Any activity that triggered the alert and is not inherently malicious must be monitored by the security team.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- If the host is a domain controller (DC):
  - Activate your incident response plan for total Active Directory compromise.
  - Review the privileges assigned to users that can access the DCs, to ensure that the least privilege principle is being followed and to reduce the attack surface.
- Isolate the involved hosts to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

