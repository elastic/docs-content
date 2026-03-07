---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious DLL Loaded for Persistence or Privilege Escalation" prebuilt detection rule.
---

# Suspicious DLL Loaded for Persistence or Privilege Escalation

## Triage and analysis

### Investigating Suspicious DLL Loaded for Persistence or Privilege Escalation

Attackers can execute malicious code by abusing missing modules that processes try to load, enabling them to escalate privileges or gain persistence. This rule identifies the loading of a non-Microsoft-signed DLL that is missing on a default Windows installation or one that can be loaded from a different location by a native Windows process.

#### Possible investigation steps

- Examine the DLL signature and identify the process that created it.
  - Investigate any abnormal behaviors by the process such as network connections, registry or file modifications, and any spawned child processes.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Retrieve the DLL and determine if it is malicious:
  - Use a private sandboxed malware analysis system to perform analysis.
    - Observe and collect information about the following activities:
      - Attempts to contact external domains and addresses.
      - File and registry access, modification, and creation activities.
      - Service creation and launch activities.
      - Scheduled task creation.
  - Use the PowerShell Get-FileHash cmdlet to get the files' SHA-256 hash values.
    - Search for the existence and reputation of the hashes in resources like VirusTotal, Hybrid-Analysis, CISCO Talos, Any.run, etc.

### False positive analysis

- This activity is unlikely to happen legitimately. Any activity that triggered the alert and is not inherently malicious must be monitored by the security team.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors like reverse shells, reverse proxies, or droppers that attackers could use to reinfect the system.
- Remove and block malicious artifacts identified during triage.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

