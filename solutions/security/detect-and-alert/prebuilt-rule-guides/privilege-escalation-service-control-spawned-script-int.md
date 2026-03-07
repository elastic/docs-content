---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Service Control Spawned via Script Interpreter" prebuilt detection rule.
---

# Service Control Spawned via Script Interpreter

## Triage and analysis

### Investigating Service Control Spawned via Script Interpreter

Windows services are background processes that run with SYSTEM privileges and provide specific functionality or support to other applications and system components.

The `sc.exe` command line utility is used to manage and control Windows services on a local or remote computer. Attackers may use `sc.exe` to create, modify, and start services to elevate their privileges from administrator to SYSTEM.

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Examine the command line, registry changes events, and Windows events related to service activities (for example, 4697 and/or 7045) for suspicious characteristics.
  - Examine the created and existent services, the executables or drivers referenced, and command line arguments for suspicious entries.
    - $osquery_0
    - $osquery_1
    - $osquery_2
  - Retrieve the referenced files' SHA-256 hash values using the PowerShell `Get-FileHash` cmdlet and search for the existence and reputation of the hashes in resources like VirusTotal, Hybrid-Analysis, CISCO Talos, Any.run, etc.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Assess whether this behavior is prevalent in the environment by looking for similar occurrences across hosts.

### False positive analysis

- This activity is not inherently malicious if it occurs in isolation. As long as the analyst did not identify suspicious activity related to the user, host, and service, such alerts can be dismissed.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Delete the service or restore it to the original configuration.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

