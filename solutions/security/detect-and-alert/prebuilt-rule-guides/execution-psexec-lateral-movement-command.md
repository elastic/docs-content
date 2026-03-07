---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "PsExec Network Connection" prebuilt detection rule.'
---

# PsExec Network Connection

## Triage and analysis

### Investigating PsExec Network Connection

PsExec is a remote administration tool that enables the execution of commands with both regular and SYSTEM privileges on Windows systems. Microsoft develops it as part of the Sysinternals Suite. Although commonly used by administrators, PsExec is frequently used by attackers to enable lateral movement and execute commands as SYSTEM to disable defenses and bypass security protections.

This rule identifies PsExec execution by looking for the creation of `PsExec.exe`, the default name for the utility, followed by a network connection done by the process.

#### Possible investigation steps

- Check if the usage of this tool complies with the organization's administration policy.
- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Identify the target computer and its role in the IT environment.
- Investigate what commands were run, and assess whether this behavior is prevalent in the environment by looking for similar occurrences across hosts.

### False positive analysis

- This mechanism can be used legitimately. As long as the analyst did not identify suspicious activity related to the user or involved hosts, and the tool is allowed by the organization's policy, such alerts can be dismissed.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
  - Prioritize cases involving critical servers and users.
- Isolate the involved hosts to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Review the privileges assigned to the user to ensure that the least privilege principle is being followed.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
