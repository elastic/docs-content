---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Linux Restricted Shell Breakout via Linux Binary(s)" prebuilt detection rule.
---

# Linux Restricted Shell Breakout via Linux Binary(s)

## Triage and analysis

### Investigating Linux Restricted Shell Breakout via Linux Binary(s)
Detection alerts from this rule indicate that a Linux utility has been abused to breakout of restricted shells or
environments by spawning an interactive system shell.
Here are some possible avenues of investigation:
- Examine the entry point to the host and user in action via the Analyse View.
  - Identify the session entry leader and session user
- Examine the contents of session leading to the abuse via the Session View.
  - Examine the command execution pattern in the session, which may lead to suspricous activities
- Examine the execution of commands in the spawned shell.
  - Identify imment threat to the system from the executed commands
  - Take necessary incident response actions to contain any malicious behviour caused via this execution.

### Related rules

- A malicious spawned shell can execute any of the possible MITTRE ATT&CK vectors mainly to impair defences.
- Hence its adviced to enable defence evasion and privilige escalation rules accordingly in your environment

### Response and remediation

Initiate the incident response process based on the outcome of the triage.

- If the triage releaved suspicious netwrok activity from the malicious spawned shell,
  - Isolate the involved host to prevent further post-compromise behavior.
- If the triage identified malware execution via the maliciously spawned shell,
  - Search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- If the triage revelaed defence evasion for imparing defenses
  - Isolate the involved host to prevent further post-compromise behavior.
  - Identified the disabled security guard components on the host and take necessary steps in renebaling the same.
  - If any tools have been disbaled / uninstalled or config tampered work towards reenabling the same.
- If the triage revelaed addition of persistence mechanism exploit like auto start scripts
  - Isolate further login to the systems that can initae auto start scripts.
  - Identify the auto start scripts and disable and remove the same from the systems
- If the triage revealed data crawling or data export via remote copy
  - Investigate credential exposure on systems compromised / used / decoded by the attacker during the data crawling
  - Intiate compromised credential deactivation and credential rotation process for all exposed crednetials.
  - Investiagte if any IPR data was accessed during the data crawling and take appropriate actions.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

